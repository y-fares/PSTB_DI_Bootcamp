# server.py
"""
### HTTP Web Search Briefing Bot server

Exposes JSON HTTP endpoints:

- GET /tools
- POST /tools/search_web
- POST /tools/fetch_readable
- POST /tools/summarize_with_citations
- POST /tools/save_markdown
"""

import os
import re
import json
from datetime import datetime
from typing import List

import requests
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, HttpUrl

# ### Configuration (via environment variables)

MCP_HTTP_TOKEN = os.getenv("MCP_HTTP_TOKEN", "dev-token")  # simple Bearer auth

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # web search API key (Tavily here)
TAVILY_URL = "https://api.tavily.com/search"

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")  # Ollama by default
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")

OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ### FastAPI app

app = FastAPI(title="HTTP Web Search Briefing Bot")

security = HTTPBearer()


def check_auth(credentials: HTTPAuthorizationCredentials = Depends(security)) -> None:
    """Check Bearer token against MCP_HTTP_TOKEN."""
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid auth scheme",
        )
    if credentials.credentials != MCP_HTTP_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )


# ### Pydantic models


class ToolInfo(BaseModel):
    """Information about a tool and its input schema."""
    name: str
    input_schema: dict


class ToolsResponse(BaseModel):
    """List of tools."""
    tools: List[ToolInfo]


class SearchRequest(BaseModel):
    """Input for /tools/search_web."""
    query: str
    k: int = 5


class SearchResult(BaseModel):
    """Single web search result."""
    title: str
    url: HttpUrl
    snippet: str
    source: str


class SearchResponse(BaseModel):
    """Output for /tools/search_web."""
    results: List[SearchResult]


class FetchReadableRequest(BaseModel):
    """Input for /tools/fetch_readable."""
    url: HttpUrl


class FetchReadableResponse(BaseModel):
    """Output for /tools/fetch_readable."""
    url: HttpUrl
    title: str
    text: str


class Doc(BaseModel):
    """Single document passed to the summarizer."""
    title: str
    url: HttpUrl
    text: str


class SummarizeRequest(BaseModel):
    """Input for /tools/summarize_with_citations."""
    topic: str
    docs: List[Doc]


class SourceInfo(BaseModel):
    """Source metadata with index for inline citations."""
    i: int
    title: str
    url: HttpUrl


class SummarizeResponse(BaseModel):
    """Output for /tools/summarize_with_citations."""
    bullets: List[str]
    sources: List[SourceInfo]


class SaveMarkdownRequest(BaseModel):
    """Input for /tools/save_markdown."""
    filename: str
    content: str


class SaveMarkdownResponse(BaseModel):
    """Output for /tools/save_markdown."""
    path: str


# ### Helper functions


def strip_html(html: str) -> str:
    """Very simple HTML to text: remove tags and compress spaces."""
    text = re.sub(r"<script.*?</script>", "", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_title(html: str) -> str:
    """Extract <title> tag from HTML."""
    m = re.search(r"<title>(.*?)</title>", html, flags=re.IGNORECASE | re.DOTALL)
    if not m:
        return ""
    title = m.group(1)
    title = re.sub(r"\s+", " ", title)
    return title.strip()


def call_tavily(query: str, k: int) -> List[SearchResult]:
    """Call Tavily API and normalize results."""
    if not TAVILY_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="TAVILY_API_KEY is not set.",
        )

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": k,
        "search_depth": "basic",
    }

    try:
        resp = requests.post(TAVILY_URL, json=payload, timeout=10)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Tavily request failed: {e}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Tavily error {resp.status_code}: {resp.text[:200]}",
        )

    data = resp.json()
    results = []
    for item in data.get("results", []):
        url = item.get("url") or "https://example.com"
        snippet = item.get("content") or item.get("snippet") or ""
        results.append(
            SearchResult(
                title=item.get("title", ""),
                url=url,
                snippet=snippet[:500],
                source="tavily",
            )
        )
    return results


def call_llm_summarize(topic: str, docs: List[Doc]) -> str:
    """Call local LLM (Ollama or compatible) to get a bullet summary text."""
    # Build a compact context for the model
    docs_summary_parts = []
    for idx, doc in enumerate(docs, start=1):
        snippet = doc.text[:2000]
        docs_summary_parts.append(
            f"Source [{idx}] - {doc.title} ({doc.url}):\n{snippet}\n"
        )

    context_block = "\n\n".join(docs_summary_parts)

    prompt = f"""
You are a briefing assistant.

Topic: {topic}

You are given several sources with indices [1], [2], ...

Task:
- Write exactly 5 bullet points.
- Each bullet <= 200 characters.
- Use inline citation markers like [1], [2], [1][3] at the end of sentences.
- Cover the main ideas across all sources.
- Answer in plain Markdown bullets, example:

- A short point with [1][2]
- Another point with [3]

Sources:
{context_block}
""".strip()

    # Ollama /api/chat
    url = f"{LLM_BASE_URL.rstrip('/')}/api/chat"
    body = {
        "model": LLM_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }

    try:
        resp = requests.post(url, json=body, timeout=60)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {e}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"LLM error {resp.status_code}: {resp.text[:200]}",
        )

    data = resp.json()
    # Ollama /api/chat final response: data["message"]["content"]
    content = data.get("message", {}).get("content", "")
    if not content:
        raise HTTPException(status_code=502, detail="Empty LLM response.")
    return content


def parse_bullets(text: str) -> List[str]:
    """Extract bullet lines from LLM text and enforce 5 bullets <= 200 chars."""
    lines = text.splitlines()
    bullets = []
    for line in lines:
        line = line.strip()
        if line.startswith("- "):
            bullet = line[2:].strip()
            if len(bullet) > 200:
                bullet = bullet[:197] + "..."
            bullets.append(bullet)
    if not bullets:
        # Fallback: use whole text as one bullet if parsing fails
        bullet = text.strip()
        if len(bullet) > 200:
            bullet = bullet[:197] + "..."
        bullets = [bullet]

    # Enforce exactly 5 bullets
    if len(bullets) > 5:
        bullets = bullets[:5]
    else:
        while len(bullets) < 5:
            bullets.append("Additional detail not provided by the model.")
    return bullets


def sanitize_filename(name: str) -> str:
    """Keep a safe filename: letters, digits, dash, underscore, dot."""
    name = name.strip()
    name = re.sub(r"[^A-Za-z0-9._-]", "_", name)
    if not name:
        name = "brief.md"
    if not name.endswith(".md"):
        name = name + ".md"
    return name


# ### Endpoints


@app.get("/tools", response_model=ToolsResponse)
def list_tools(_: None = Depends(check_auth)) -> ToolsResponse:
    """List available tool names and their input schemas."""
    tools = [
        ToolInfo(
            name="search_web",
            input_schema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer"},
                },
                "required": ["query"],
            },
        ),
        ToolInfo(
            name="fetch_readable",
            input_schema={
                "type": "object",
                "properties": {
                    "url": {"type": "string", "format": "uri"},
                },
                "required": ["url"],
            },
        ),
        ToolInfo(
            name="summarize_with_citations",
            input_schema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string"},
                    "docs": {"type": "array"},
                },
                "required": ["topic", "docs"],
            },
        ),
        ToolInfo(
            name="save_markdown",
            input_schema={
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "content": {"type": "string"},
                },
                "required": ["filename", "content"],
            },
        ),
    ]
    return ToolsResponse(tools=tools)


@app.post(
    "/tools/search_web",
    response_model=SearchResponse,
)
def search_web(request: SearchRequest, _: None = Depends(check_auth)) -> SearchResponse:
    """Search the web via Tavily and return normalized results."""
    if request.k <= 0:
        raise HTTPException(status_code=400, detail="k must be > 0")
    results = call_tavily(request.query, request.k)
    return SearchResponse(results=results)


@app.post(
    "/tools/fetch_readable",
    response_model=FetchReadableResponse,
)
def fetch_readable(
    request: FetchReadableRequest,
    _: None = Depends(check_auth),
) -> FetchReadableResponse:
    """Fetch a web page and return a simplified readable text."""
    try:
        resp = requests.get(str(request.url), timeout=15)
    except requests.RequestException as e:
        raise HTTPException(status_code=502, detail=f"Fetch failed: {e}")

    if resp.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Fetch error {resp.status_code}",
        )

    html = resp.text
    title = extract_title(html) or str(request.url)
    text = strip_html(html)
    if not text:
        raise HTTPException(status_code=502, detail="No readable text extracted.")
    return FetchReadableResponse(url=request.url, title=title, text=text)


@app.post(
    "/tools/summarize_with_citations",
    response_model=SummarizeResponse,
)
def summarize_with_citations(
    request: SummarizeRequest,
    _: None = Depends(check_auth),
) -> SummarizeResponse:
    """Call LLM to create a 5-bullet briefing with inline citations."""
    if not request.docs:
        raise HTTPException(status_code=400, detail="docs must not be empty")

    llm_text = call_llm_summarize(request.topic, request.docs)
    bullets = parse_bullets(llm_text)

    sources = [
        SourceInfo(i=idx, title=doc.title, url=doc.url)
        for idx, doc in enumerate(request.docs, start=1)
    ]
    return SummarizeResponse(bullets=bullets, sources=sources)


@app.post(
    "/tools/save_markdown",
    response_model=SaveMarkdownResponse,
)
def save_markdown(
    request: SaveMarkdownRequest,
    _: None = Depends(check_auth),
) -> SaveMarkdownResponse:
    """Save Markdown content to disk and return the file path."""
    filename = sanitize_filename(request.filename)
    path = os.path.join(OUTPUT_DIR, filename)

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(request.content)
    except OSError as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    return SaveMarkdownResponse(path=os.path.abspath(path))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,                  # <--- PAS "server:app", mais directement l'objet app
        host="0.0.0.0",
        port=8000,
        reload=False,         # pas de reloader intégré ici
    )
