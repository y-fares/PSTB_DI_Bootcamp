# mcp_insights_server/server.py

import sys
import json
from typing import Any, Dict

def summarize_insights(context: str) -> str:
    """
    Summarize and structure insights coming from various tools.
    """
    # Very simple implementation, you can improve it later.
    # For the bootcamp it's fine if this is rule-based or if it calls an LLM.
    lines = context.split("\n")
    cleaned = [l.strip() for l in lines if l.strip()]
    bullet_points = "\n".join(f"- {l}" for l in cleaned[:10])

    return f"## Insights summary\n\n{bullet_points}\n"

def handle_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handle a single JSON-RPC request coming from the MCP host.
    """
    method = request.get("method")
    req_id = request.get("id")

    if method == "tools/list":
        # Describe the tools exposed by this server
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "summarize_insights",
                        "description": "Summarize raw data and web results into a concise report.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "context": {"type": "string"}
                            },
                            "required": ["context"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        params = request.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "summarize_insights":
            context = args.get("context", "")
            result = summarize_insights(context)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"output": result}
            }

    # Default: method not found
    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method {method} not found"
        }
    }

def main():
    """
    Minimal MCP-compatible JSON-RPC loop over STDIN/STDOUT.
    """
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
            response = handle_request(request)
        except Exception as e:
            # Fallback error format
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32000, "message": str(e)},
            }
        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()

