# orchestrator.py
# ### Agentic orchestrator: LLM plans, MCP tools act, Streamlit displays

from __future__ import annotations

import asyncio
import json
import traceback
from dataclasses import dataclass, field
from typing import Any, Dict, List

from llm_client import plan_with_llm
from mcp_multi_client import MCPMultiClient
from config import load_llm_config, load_mcp_server_configs


@dataclass
class ToolLogEntry:
    """One tool call log entry."""
    step: int
    tool_name: str
    server_name: str
    arguments: Dict[str, Any]
    success: bool
    result_preview: str
    error: str | None = None


@dataclass
class OrchestratorResult:
    """Final result for UI consumption."""
    final_answer: str
    tool_logs: List[ToolLogEntry] = field(default_factory=list)
    messages_trace: List[Dict[str, Any]] = field(default_factory=list)


class AgenticOrchestrator:
    """
    ### High-level agent
    - Uses LLM to select tools and arguments
    - Calls MCP tools
    - Handles errors and logs every step
    """

    def __init__(self, max_steps: int = 6) -> None:
        self.max_steps = max_steps
        self.llm_cfg = load_llm_config()
        self.mcp_server_configs = load_mcp_server_configs()
        self.tool_logs: List[ToolLogEntry] = []

    # ### Core run method
    async def run(self, user_goal: str) -> OrchestratorResult:
        async with MCPMultiClient(self.mcp_server_configs) as mcp_client:
            tools_for_llm = mcp_client.build_llm_tools_spec()

            # Initial conversation
            messages: List[Dict[str, Any]] = [
                {
                    "role": "system",
                    "content": (
                        "You are an AI agent that must use tools via MCP when useful. "
                        "You have access to multiple tools from different servers. "
                        "You may call tools multiple times to achieve the user's goal. "
                        "Always try to be precise and avoid hallucinations: "
                        "if you need external data, call an appropriate tool."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"User goal:\n{user_goal}\n\n"
                        "Work step by step. If you need a tool, use tool calls. "
                        "When you have enough information, answer directly."
                    ),
                },
            ]

            final_answer = ""
            self.tool_logs.clear()

            for step in range(1, self.max_steps + 1):
                # Ask LLM what to do next
                assistant_msg = plan_with_llm(messages, tools_for_llm)
                tool_calls = assistant_msg.get("tool_calls") or []

                # If no tools requested → final answer
                if not tool_calls:
                    content = assistant_msg.get("content") or ""
                    final_answer = content if isinstance(content, str) else json.dumps(
                        content
                    )
                    messages.append(
                        {
                            "role": "assistant",
                            "content": final_answer,
                        }
                    )
                    break

                # Otherwise execute each requested tool (simple sequential version)
                messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "I will now call tools to gather more information "
                            "before giving a final answer."
                        ),
                    }
                )

                for tc in tool_calls:
                    f_info = tc.get("function") or {}
                    llm_tool_name = f_info.get("name")
                    raw_args = f_info.get("arguments") or "{}"

                    try:
                        args = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                    except json.JSONDecodeError:
                        args = {}
                        error_text = (
                            f"Invalid JSON arguments from LLM for tool {llm_tool_name}: {raw_args}"
                        )
                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=llm_tool_name or "UNKNOWN",
                                server_name="UNKNOWN",
                                arguments={},
                                success=False,
                                result_preview="",
                                error=error_text,
                            )
                        )
                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    f"Tool call failed because of invalid arguments. "
                                    f"Details: {error_text}. "
                                    "Please fix the arguments or choose another tool."
                                ),
                            }
                        )
                        continue

                    # Call MCP tool
                    try:
                        # We need server name for logging → we look into MCP client registry
                        # (MCPMultiClient stores ToolDescriptor with llm_name)
                        td = mcp_client.tools.get(llm_tool_name)
                        server_name = td.server_name if td else "UNKNOWN"

                        result = await mcp_client.call_tool(llm_tool_name, args)
                        preview = str(result)[:500]

                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=llm_tool_name or "UNKNOWN",
                                server_name=server_name,
                                arguments=args,
                                success=True,
                                result_preview=preview,
                            )
                        )

                        # Inject tool result back into conversation (ReAct style)
                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    f"Tool '{llm_tool_name}' (server '{server_name}') "
                                    f"returned the following result:\n{preview}\n\n"
                                    "Use this information to move closer to the goal."
                                ),
                            }
                        )

                    except Exception as e:  # noqa: BLE001
                        error_text = f"Tool execution failed: {e}"
                        self.tool_logs.append(
                            ToolLogEntry(
                                step=step,
                                tool_name=llm_tool_name or "UNKNOWN",
                                server_name="UNKNOWN",
                                arguments=args,
                                success=False,
                                result_preview="",
                                error=error_text + "\n" + traceback.format_exc()[:500],
                            )
                        )
                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    f"Tool '{llm_tool_name}' failed with error: {error_text}. "
                                    "Do NOT retry the same call blindly. Either adjust the parameters "
                                    "or choose another tool, or explain the limitation to the user."
                                ),
                            }
                        )

            # Fallback if no final answer
            if not final_answer:
                final_answer = (
                    "I could not fully complete the task within the maximum number of steps. "
                    "Please check the tool log for partial progress."
                )

            return OrchestratorResult(
                final_answer=final_answer,
                tool_logs=list(self.tool_logs),
                messages_trace=messages,
            )
