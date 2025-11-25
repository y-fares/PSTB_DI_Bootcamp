# orchestrator.py

import os
import json
from typing import Any, Dict, List
from mcp_client import MCPConnection
import requests

# Simple history structure
class StepLog:
    def __init__(self, step: int, server: str, tool: str, args: Dict[str, Any], result_summary: str):
        self.step = step
        self.server = server
        self.tool = tool
        self.args = args
        self.result_summary = result_summary

def call_ollama(system_prompt: str, user_prompt: str) -> str:
    """
    Call Ollama locally as LLM backend.
    """
    base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.environ.get("OLLAMA_MODEL", "llama3")

    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
    }

    resp = requests.post(f"{base_url}/api/generate", json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    # Ollama returns 'response' in chunks sometimes, keep it simple here
    return data.get("response", "")

def build_tools_description(servers: Dict[str, MCPConnection]) -> str:
    """
    Ask each server for its tools and build a human-readable description for the LLM.
    """
    lines = []
    for name, conn in servers.items():
        resp = conn.list_tools()
        tools = resp.get("result", {}).get("tools", [])
        for t in tools:
            t_name = t.get("name")
            desc = t.get("description", "")
            lines.append(f"- [{name}] {t_name}: {desc}")
    return "\n".join(lines)

def orchestrate(user_goal: str, servers: Dict[str, MCPConnection], max_steps: int = 6) -> Dict[str, Any]:
    """
    Main orchestration loop:
    - Ask LLM which tool to call next, given the goal and history.
    - Call that tool via MCP.
    - Log and repeat until LLM returns a final answer.
    """
    history: List[StepLog] = []
    tools_desc = build_tools_description(servers)

    system_prompt = (
        "You are an orchestration agent. "
        "You have access to several tools exposed via MCP servers. "
        "At each step, decide either to call a tool or to return the final answer.\n\n"
        "You MUST respond in strict JSON with the following schema:\n"
        "{\n"
        '  "action": "tool" | "final_answer",\n'
        '  "server": "<server_name>",\n'
        '  "tool_name": "<tool_name>",\n'
        '  "arguments": { ... },\n'
        '  "final": "<string or null>"\n'
        "}\n"
        "If action == 'final_answer', ignore server/tool_name/arguments and put the final answer in 'final'.\n"
    )

    for step in range(1, max_steps + 1):
        history_str = "\n".join(
            f"Step {h.step}: server={h.server}, tool={h.tool}, args={h.args}, result={h.result_summary}"
            for h in history
        )

        user_prompt = f"""
User goal:
{user_goal}

Available tools:
{tools_desc}

History so far:
{history_str if history_str else "No previous steps."}

Decide the next action.
"""

        raw = call_ollama(system_prompt, user_prompt)

        # Try to parse JSON from the model output
        try:
            # Sometimes model adds text around JSON, so we try to extract braces.
            start = raw.find("{")
            end = raw.rfind("}")
            parsed = json.loads(raw[start:end+1])
        except Exception:
            # Fallback: treat it as final answer
            return {
                "final_answer": f"Model failed to produce valid JSON. Raw output:\n{raw}",
                "steps": history,
            }

        action = parsed.get("action")
        if action == "final_answer":
            return {"final_answer": parsed.get("final", ""), "steps": history}

        server_name = parsed.get("server")
        tool_name = parsed.get("tool_name")
        arguments = parsed.get("arguments", {})

        if server_name not in servers:
            # Log error and ask again in next loop
            history.append(
                StepLog(step, server_name or "UNKNOWN", tool_name or "UNKNOWN", arguments, "Invalid server name")
            )
            continue

        conn = servers[server_name]

        try:
            resp = conn.call_tool(tool_name, arguments)
            result = resp.get("result") or resp.get("error", {})
            # Summarize result for history (avoid huge payloads)
            summary = str(result)[:300]
            history.append(StepLog(step, server_name, tool_name, arguments, summary))
        except Exception as e:
            # On failure, log and continue – LLM will see the failure in history
            history.append(StepLog(step, server_name, tool_name, arguments, f"ERROR: {str(e)}"))

    # If max_steps reached:
    return {
        "final_answer": "Reached max_steps without explicit final answer.",
        "steps": history,
    }

