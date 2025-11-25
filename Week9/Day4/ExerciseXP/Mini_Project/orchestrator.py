# orchestrator.py
# ### Agentic orchestrator: LLM plans, MCP executes, multi-server composition

from __future__ import annotations

import asyncio
import json
import traceback
from dataclasses import dataclass, field
from typing import Any, Dict, List

from config import load_llm_config, load_mcp_server_configs
from llm_client import plan_with_llm
from mcp_multi_client import MCPMultiClient, ToolDescriptor


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
    - Lets the LLM decide which tool to use, in which order.
    - Logs every tool call and handles errors robustly.
    """

    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps
        self.llm_cfg = load_llm_config()
        self.server_configs = load_mcp_server_configs()
        self.tool_logs: List[ToolLogEntry] = []

    async def run(self, user_goal: str) -> OrchestratorResult:
        self.tool_logs.clear()

        async with MCPMultiClient(self.server_configs, debug=False) as mcp_client:
            tools_for_llm = mcp_client.build_llm_tools_spec()

            # System prompt: high-level, does NOT script specific sequences
            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI agent that can use external tools via MCP.\n"
                        "You will be given a list of tools with their descriptions.\n"
                        "Your job is to plan and execute multi-step strategies using those tools\n"
                        "when they are helpful for the user's goal. You decide which tools to use\n"
                        "and in what order, based on their description and the current context.\n\n"
                        "General advice:\n"
                        "- Use filesystem tools if you need to inspect or read local content.\n"
                        "- Use web/search tools if you need information from the internet.\n"
                        "- Use local_insights tools to clean and analyze text once you have it.\n"
                        "- You can call tools multiple times and combine them.\n"
                        "- When you have enough information, provide a clear final answer.\n"
                        "Avoid hallucinations. If tools fail, adapt your plan and consider alternatives."
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

                # If no tools requested, treat as final answer
                if not tool_calls:
                    content = assistant_msg.get("content") or ""
                    final_answer = (
                        content
                        if isinstance(content, str)
                        else json.dumps(content, ensure_ascii=False)
                    )
                    break

                # Record the planning step (optional context)
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
                    tool_call_id = tc.get("id", "")

                    # Decode arguments safely
                    try:
                        args = (
                            json.loads(raw_args)
                            if isinstance(raw_args, str)
                            else raw_args
                        )
                        if not isinstance(args, dict):
                            raise ValueError("Tool arguments must be a JSON object.")
                    except Exception as e:  # noqa: BLE001
                        error_text = (
                            f"Invalid arguments for tool '{tool_name}': {raw_args}. "
                            f"Parse error: {e}"
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
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": (
                                    "Tool arguments were invalid JSON or not an object. "
                                    f"Error: {error_text}. "
                                    "Please adjust the call or choose another tool."
                                ),
                            }
                        )
                        continue

                    # Retrieve tool descriptor for validation
                    td: ToolDescriptor | None = mcp_client.tools.get(tool_name)
                    server_name = td.server_name if td else "UNKNOWN"
                    required_fields = td.input_schema.get("required", []) if td else []

                    # Simple schema-based validation
                    missing = [r for r in required_fields if r not in args]
                    if missing:
                        error_text = (
                            f"Missing required parameters for tool '{tool_name}': {missing}"
                        )
                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=tool_name or "UNKNOWN",
                                server_name=server_name,
                                arguments=args,
                                success=False,
                                result_preview="",
                                error=error_text,
                            )
                        )
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": (
                                    f"The call to tool '{tool_name}' is missing required "
                                    f"params {missing}. Please fix the arguments or pick "
                                    "a different tool."
                                ),
                            }
                        )
                        continue

                    # Call MCP tool
                    try:
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

                        # Feed result back as tool message
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": preview,
                            }
                        )

                    except Exception as e:  # noqa: BLE001
                        tb = traceback.format_exc(limit=3)
                        error_text = (
                            f"Tool '{tool_name}' (server='{server_name}') failed.\n"
                            f"Arguments: {args}\n"
                            f"Error: {e}\n"
                            f"Traceback (truncated):\n{tb}"
                        )
                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=tool_name or "UNKNOWN",
                                server_name=server_name,
                                arguments=args,
                                success=False,
                                result_preview="",
                                error=error_text,
                            )
                        )

                        # Send rich error context back to the LLM to allow re-planning
                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call_id,
                                "name": tool_name,
                                "content": (
                                    "The tool call failed. Here is what happened:\n"
                                    + error_text
                                    + "\nPlease adapt your strategy. "
                                      "Do not retry the same call blindly."
                                ),
                            }
                        )

            if not final_answer:
                final_answer = (
                    "I could not fully complete the task within the maximum number of steps. "
                    "Check the tool logs for partial progress and intermediate results."
                )

            return OrchestratorResult(
                final_answer=final_answer,
                tool_logs=list(self.tool_logs),
            )


def run_agent_sync(user_goal: str) -> OrchestratorResult:
    orchestrator = AgenticOrchestrator()
    return asyncio.run(orchestrator.run(user_goal))
