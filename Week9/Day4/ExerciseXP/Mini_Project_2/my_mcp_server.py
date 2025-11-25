# my_mcp_server.py
# ### Your personal MCP server with 2 non-trivial tools

from __future__ import annotations
import json
import re
from mcp.server import Server
from mcp.types import Tool

server = Server("my_insights_server")


# ---------------------------------------------------------------------------
# Tool 1: clean_text
# ---------------------------------------------------------------------------
@server.tool(
    Tool(
        name="clean_text",
        description=(
            "Clean and normalize raw text. "
            "Removes HTML, excessive whitespace, and common artifacts. "
            "Useful before running LLM analysis."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Raw messy text"},
                "lowercase": {"type": "boolean", "default": False},
            },
            "required": ["text"],
        },
    )
)
async def clean_text_tool(text: str, lowercase: bool = False):
    """Basic text preprocessing: HTML tags, spacing, unicode cleanup."""
    cleaned = re.sub(r"<[^>]+>", " ", text)          # remove HTML
    cleaned = re.sub(r"\s+", " ", cleaned).strip()   # collapse whitespace
    cleaned = cleaned.encode("utf-8", "ignore").decode()

    if lowercase:
        cleaned = cleaned.lower()

    return cleaned


# ---------------------------------------------------------------------------
# Tool 2: generate_insights
# ---------------------------------------------------------------------------
@server.tool(
    Tool(
        name="generate_insights",
        description=(
            "Generate structured insights from a cleaned text. "
            "Extracts: key points, risks, next steps. "
            "Produces a JSON summary."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Clean input text"},
            },
            "required": ["text"],
        },
    )
)
async def generate_insights(text: str):
    """Extract simple structured 'insights' heuristically (no LLM used here)."""
    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    key_points = [s for s in sentences if len(s.split()) > 6][:5]
    risks = [s for s in sentences if "risk" in s.lower() or "issue" in s.lower()]
    steps = ["Review context", "Validate assumptions", "Propose improvements"]

    insights = {
        "key_points": key_points,
        "risks": risks[:5],
        "recommended_steps": steps,
    }

    return json.dumps(insights, indent=2)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    server.run()
