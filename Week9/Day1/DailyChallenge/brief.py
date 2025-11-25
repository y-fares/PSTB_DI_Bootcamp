"""
Usage:
    python brief.py "your topic"

The script:
1. Calls /tools/search_web
2. Picks up to 3 different domains and calls /tools/fetch_readable
3. Calls /tools/summarize_with_citations
4. Builds a Markdown briefing
5. Calls /tools/save_markdown and prints the saved path
"""

import os
import sys
from datetime import date
from urllib.parse import urlparse

import requests

# Server base URL and auth
SERVER_BASE_URL = os.getenv("BRIEF_SERVER_URL", "http://localhost:8000")
MCP_HTTP_TOKEN = os.getenv("MCP_HTTP_TOKEN", "dev-token")


def auth_headers() -> dict:
    """Return HTTP headers with Bearer token."""
    return {
        "Authorization": f"Bearer {MCP_HTTP_TOKEN}",
        "Content-Type": "application/json",
    }


def api_post(path: str, payload: dict) -> dict:
    """Helper for POST requests with basic error checking."""
    url = SERVER_BASE_URL.rstrip("/") + path
    resp = requests.post(url, headers=auth_headers(), json=payload, timeout=60)
    if resp.status_code >= 400:
        raise RuntimeError(f"POST {path} failed: {resp.status_code} {resp.text[:200]}")
    return resp.json()


def select_three_domains(results: list) -> list:
    """Pick at most 3 results with distinct domains."""
    picked = []
    seen_domains = set()
    for item in results:
        url = item["url"]
        domain = urlparse(url).netloc
        if domain not in seen_domains:
            seen_domains.add(domain)
            picked.append(item)
        if len(picked) >= 3:
            break
    return picked


def main() -> None:
    """Run the full briefing pipeline."""
    if len(sys.argv) < 2:
        print("Usage: python brief.py \"your topic\"")
        sys.exit(1)

    topic = sys.argv[1].strip()
    if not topic:
        print("Topic must not be empty.")
        sys.exit(1)

    # 1) Search web
    search_payload = {"query": topic, "k": 8}
    search_data = api_post("/tools/search_web", search_payload)
    results = search_data.get("results", [])
    if not results:
        print("No search results.")
        sys.exit(1)

    picked = select_three_domains(results)
    if not picked:
        print("Could not pick any domains.")
        sys.exit(1)

    # 2) Fetch readable versions
    docs = []
    for item in picked:
        url = item["url"]
        fetch_payload = {"url": url}
        fetch_data = api_post("/tools/fetch_readable", fetch_payload)
        docs.append(
            {
                "title": fetch_data["title"],
                "url": fetch_data["url"],
                "text": fetch_data["text"],
            }
        )

    # 3) Summarize with citations
    summarize_payload = {"topic": topic, "docs": docs}
    summary_data = api_post("/tools/summarize_with_citations", summarize_payload)

    bullets = summary_data.get("bullets", [])
    sources = summary_data.get("sources", [])

    # 4) Build Markdown briefing
    today_str = date.today().isoformat()
    filename = f"brief_{today_str}.md"

    lines = []
    lines.append(f"# Briefing: {topic}")
    lines.append("")
    for b in bullets:
        lines.append(f"- {b}")
    lines.append("")
    lines.append("## Sources")
    lines.append("")

    for s in sources:
        idx = s["i"]
        title = s["title"]
        url = s["url"]
        lines.append(f"{idx}. [{title}]({url})")

    content = "\n".join(lines)

    # 5) Save via server
    save_payload = {"filename": filename, "content": content}
    save_data = api_post("/tools/save_markdown", save_payload)

    path = save_data.get("path")
    print(path)
    # Pas plus, le sujet impose juste "prints the saved path".


if __name__ == "__main__":
    main()
