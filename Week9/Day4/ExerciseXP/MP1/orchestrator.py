# orchestrator.py
# ### Agentic orchestrator: LLM plans with tool_calls, MCP executes

from __future__ import annotations

import asyncio
import json
import traceback
from dataclasses import dataclass, field
from typing import Any, Dict, List

from openai import OpenAI

from config import load_llm_config, load_mcp_server_configs
from mcp_multi_client import MCPMultiClient


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


class AgenticOrchestrator:
    """
    ### High-level agent
    - Uses OpenAI-style tool_calls to choose actions
    - Uses MCP servers as tool implementations
    """

    def __init__(self, max_steps: int = 8) -> None:
        self.max_steps = max_steps
        self.llm_cfg = load_llm_config()
        self.client = OpenAI(
            api_key=self.llm_cfg.api_key,
            base_url=self.llm_cfg.base_url,
        )
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
                        "You are an AI agent that must use tools via MCP when helpful. "
                        "You have access to multiple tools from different servers. "
                        "You may call tools multiple times. "
                        "When you have enough information, answer the user directly."
                    ),
                },
                {
                    "role": "user",
                    "content": user_goal,
                },
            ]

            final_answer = ""

            for step in range(1, self.max_steps + 1):
                completion = self.client.chat.completions.create(
                    model=self.llm_cfg.model,
                    messages=messages,
                    tools=tools_for_llm,
                    tool_choice="auto",
                    temperature=0.2,
                )

                msg = completion.choices[0].message

                # If the model wants to call tools
                if msg.tool_calls:
                    # Add assistant message with tool_calls to the history
                    assistant_msg_for_history: Dict[str, Any] = {
                        "role": "assistant",
                        "content": msg.content,
                        "tool_calls": [],
                    }

                    for tc in msg.tool_calls:
                        assistant_msg_for_history["tool_calls"].append(
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                        )

                    messages.append(assistant_msg_for_history)

                    # Execute each tool call sequentially
                    for tc in msg.tool_calls:
                        tool_name = tc.function.name
                        raw_args = tc.function.arguments or "{}"

                        try:
                            args = (
                                json.loads(raw_args)
                                if isinstance(raw_args, str)
                                else raw_args
                            )
                        except json.JSONDecodeError:
                            error_text = (
                                f"Invalid JSON arguments from LLM for tool {tool_name}: "
                                f"{raw_args}"
                            )
                            self.tool_logs.append(
                                ToolLogEntry(
                                    step=step,
                                    tool_name=tool_name,
                                    server_name="UNKNOWN",
                                    arguments={},
                                    success=False,
                                    result_preview="",
                                    error=error_text,
                                )
                            )
                            # Inject error feedback as a tool response
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tc.id,
                                    "name": tool_name,
                                    "content": error_text,
                                }
                            )
                            continue

                        try:
                            td = mcp_client.tools.get(tool_name)
                            server_name = td.server_name if td else "UNKNOWN"

                            result_str = await mcp_client.call_tool(tool_name, args)
                            preview = result_str[:600]

                            self.tool_logs.append(
                                ToolLogEntry(
                                    step=step,
                                    tool_name=tool_name,
                                    server_name=server_name,
                                    arguments=args,
                                    success=True,
                                    result_preview=preview,
                                )
                            )

                            # Append tool result as a "tool" role message
                            messages.append(
                                {
                                    "role": "tool",
                                    "tool_call_id": tc.id,
                                    "name": tool_name,
                                    "content": preview,
                                }
                            )

                        except Exception as e:  # noqa: BLE001
                            error_text = (
                                f"Tool execution failed: {e}\n"
                                f"{traceback.format_exc()[:500]}"
                            )

                            self.tool_logs.append(
                                ToolLogEntry(
                                    step=step,
                                    tool_name=tool_name,
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
                                    "tool_call_id": tc.id,
                                    "name": tool_name,
                                    "content": (
                                        "Tool failed with error. "
                                        "You should adapt your strategy or explain the limitation.\n"
                                        + error_text
                                    ),
                                }
                            )

                    # After executing tools, loop again (the model will see tool outputs)
                    continue

                # No tool_calls => final answer
                if msg.content:
                    final_answer = msg.content
                    break

            if not final_answer:
                final_answer = (
                    "I could not fully complete the task within the maximum number of steps. "
                    "Check the tool logs for partial results."
                )

            return OrchestratorResult(
                final_answer=final_answer,
                tool_logs=list(self.tool_logs),
            )


# Small helper to run from CLI
def run_agent_sync(user_goal: str) -> OrchestratorResult:
    orchestrator = AgenticOrchestrator()
    return asyncio.run(orchestrator.run(user_goal))
