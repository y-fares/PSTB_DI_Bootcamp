# orchestrator.py
# ### Agentic orchestrator: LLM plans, MCP executes (files + web + local_insights)

from __future__ import annotations

import asyncio
import json
import traceback
from dataclasses import dataclass, field
from typing import Any, Dict, List

from config import load_llm_config, load_mcp_server_configs
from llm_client import plan_with_llm
from mcp_multi_client import MCPMultiClient


@dataclass
class ToolLogEntry:
    step: int
    tool_name: str
    server_name: str
    arguments: Dict[str, Any]
    success: bool
    result_preview: str
    error: str | None = None


@dataclass
class OrchestratorResult:
    final_answer: str
    tool_logs: List[ToolLogEntry] = field(default_factory=list)


class AgenticOrchestrator:
    """
    High-level agent:
    - Discovers tools from external servers + local_insights server.
    - Uses LLM tool_calls to choose actions.
    - Handles errors and logs each step.
    """

    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps
        self.llm_cfg = load_llm_config()
        self.server_configs = load_mcp_server_configs()
        self.tool_logs: List[ToolLogEntry] = []

    async def run(self, user_goal: str) -> OrchestratorResult:
        self.tool_logs.clear()

        async with MCPMultiClient(self.server_configs) as mcp_client:
            tools_for_llm = mcp_client.build_llm_tools_spec()

            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI agent that must use tools via MCP.\n"
                        "You have three types of servers available:\n"
                        "- 'files': to read and list files in /home/yacine/mcp_root.\n"
                        "- 'web': to search and fetch web pages.\n"
                        "- 'local_insights': to clean text and generate structured insights.\n"
                        "Typical flow: use 'web' or 'files' to collect raw text/data, then\n"
                        "use 'local_insights__clean_text' and 'local_insights__generate_insights'\n"
                        "to transform and summarize it.\n"
                        "Always include required arguments (e.g. path for filesystem tools).\n"
                        "Work step by step. Stop when you can provide a clear final answer."
                    ),
                },
                {
                    "role": "user",
                    "content": user_goal,
                },
            ]

            final_answer = ""

            for step in range(1, self.max_steps + 1):
                assistant_msg = plan_with_llm(messages, tools_for_llm)
                tool_calls = assistant_msg.get("tool_calls") or []

                # No tool calls => final answer
                if not tool_calls:
                    content = assistant_msg.get("content") or ""
                    final_answer = (
                        content
                        if isinstance(content, str)
                        else json.dumps(content, ensure_ascii=False)
                    )
                    break

                # Log the decision step (optional)
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_msg.get("content") or "",
                        "tool_calls": tool_calls,
                    }
                )

                # Execute each tool call sequentially
                for tc in tool_calls:
                    f_info = tc.get("function") or {}
                    tool_name = f_info.get("name")
                    raw_args = f_info.get("arguments") or "{}"

                    try:
                        args = (
                            json.loads(raw_args)
                            if isinstance(raw_args, str)
                            else raw_args
                        )
                    except json.JSONDecodeError:
                        error_text = (
                            f"Invalid JSON arguments from LLM for tool {tool_name}: {raw_args}"
                        )
                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=tool_name or "UNKNOWN",
                                server_name="UNKNOWN",
                                arguments={},
                                success=False,
                                result_preview="",
                                error=error_text,
                            )
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.get("id", ""),
                                "name": tool_name,
                                "content": error_text,
                            }
                        )
                        continue

                    try:
                        td = mcp_client.tools.get(tool_name)
                        server_name = td.server_name if td else "UNKNOWN"

                        result_str = await mcp_client.call_tool(tool_name, args)
                        preview = result_str[:800]

                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=tool_name or "UNKNOWN",
                                server_name=server_name,
                                arguments=args,
                                success=True,
                                result_preview=preview,
                            )
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.get("id", ""),
                                "name": tool_name,
                                "content": preview,
                            }
                        )

                    except Exception as e:
                        error_text = (
                            f"Tool '{tool_name}' failed with error: {e}\n"
                            f"Arguments were: {args}\n"
                            f"{traceback.format_exc()[:500]}"
                        )

                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=tool_name or "UNKNOWN",
                                server_name="UNKNOWN",
                                arguments=args,
                                success=False,
                                result_preview="",
                                error=error_text,
                            )
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tc.get("id", ""),
                                "name": tool_name,
                                "content": (
                                    "Tool execution failed. Do not retry blindly with the "
                                    "same parameters. Either adjust the call or choose a "
                                    "different tool.\n"
                                    + error_text
                                ),
                            }
                        )

            if not final_answer:
                final_answer = (
                    "I could not fully complete the task within the maximum number of steps. "
                    "Check the tool logs for partial progress and insights."
                )

            return OrchestratorResult(
                final_answer=final_answer,
                tool_logs=list(self.tool_logs),
            )


def run_agent_sync(user_goal: str) -> OrchestratorResult:
    orchestrator = AgenticOrchestrator()
    return asyncio.run(orchestrator.run(user_goal))
