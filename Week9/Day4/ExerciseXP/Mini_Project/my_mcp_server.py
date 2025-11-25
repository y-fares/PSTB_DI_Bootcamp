# my_mcp_server.py
# ### Your personal MCP server with 2 non-trivial tools

from __future__ import annotations

import json
import re

from mcp.server import Server
from mcp.types import Tool

server = Server("my_insights_server")


@server.tool(
    Tool(
        name="clean_text",
        description=(
            "Clean and normalize raw text. "
            "Removes HTML, excessive whitespace, and common artifacts. "
            "Useful before running LLM analysis or saving notes."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Raw messy text that may contain HTML or weird spacing.",
                },
                "lowercase": {
                    "type": "boolean",
                    "description": "If true, convert text to lowercase.",
                    "default": False,
                },
            },
            "required": ["text"],
        },
    )
)
async def clean_text_tool(text: str, lowercase: bool = False) -> str:
    """Basic text preprocessing: strip HTML, collapse whitespace, normalize encoding."""
    if not text.strip():
        raise ValueError("Input text is empty. Provide non-empty text for cleaning.")

    cleaned = re.sub(r"<[^>]+>", " ", text)          # remove HTML
    cleaned = re.sub(r"\s+", " ", cleaned).strip()   # collapse whitespace
    cleaned = cleaned.encode("utf-8", "ignore").decode()

    if lowercase:
        cleaned = cleaned.lower()

    return cleaned


@server.tool(
    Tool(
        name="generate_insights",
        description=(
            "Generate structured insights from a cleaned text. "
            "Returns JSON with: key_points, risks, recommended_steps."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Clean input text in natural language.",
                },
            },
            "required": ["text"],
        },
    )
)
async def generate_insights(text: str) -> str:
    """Extract simple structured 'insights' heuristically (no LLM, deterministic)."""
    if not text.strip():
        raise ValueError("Input text is empty. Provide non-empty text for analysis.")

    sentences = [s.strip() for s in re.split(r"[.!?]", text) if s.strip()]

    key_points = [s for s in sentences if len(s.split()) > 6][:7]
    risks = [s for s in sentences if any(w in s.lower() for w in ["risk", "issue", "problem"])]
    steps = [
        "Review current context.",
        "Validate assumptions with available data.",
        "Identify concrete next actions.",
    ]

    insights = {
        "key_points": key_points,
        "risks": risks[:7],
        "recommended_steps": steps,
        "meta": {
            "num_sentences": len(sentences),
            "num_key_points": len(key_points),
            "num_risks": len(risks),
        },
    }

    return json.dumps(insights, indent=2)


if __name__ == "__main__":
    server.run()
