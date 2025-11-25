# mcp_multi_client.py
# ### Async MCP multi-server client using the official MCP Python SDK

from __future__ import annotations

from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

from config import MCPServerConfig, load_mcp_server_configs


@dataclass
class ToolDescriptor:
    """Metadata for a tool, mapped to an LLM-exposed name."""
    llm_name: str
    server_name: str
    tool_name: str
    description: str
    input_schema: Dict[str, Any]


class MCPMultiClient:
    """
    Manages:
    - external MCP servers (filesystem + web)
    - personal MCP server (local_insights)
    """

    def __init__(
        self,
        server_configs: Optional[List[MCPServerConfig]] = None,
        debug: bool = True,
    ) -> None:
        self.server_configs = server_configs or load_mcp_server_configs()
        self._exit_stack: Optional[AsyncExitStack] = None
        self.sessions: Dict[str, ClientSession] = {}
        self.tools: Dict[str, ToolDescriptor] = {}
        self.debug = debug

    async def __aenter__(self) -> "MCPMultiClient":
        self._exit_stack = AsyncExitStack()

        for cfg in self.server_configs:
            if self.debug:
                print(f"[MCP] Starting server '{cfg.name}' with: {cfg.command} {' '.join(cfg.args)}")

            server_params = StdioServerParameters(
                command=cfg.command,
                args=cfg.args,
                env=cfg.env,
            )

            read, write = await self._exit_stack.enter_async_context(
                stdio_client(server_params)
            )

            session = ClientSession(read, write)
            await session.initialize()

            self.sessions[cfg.name] = session

        await self._discover_tools()
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
        self.sessions.clear()
        self.tools.clear()

    async def _discover_tools(self) -> None:
        """Discover tools from ALL servers (external + local_insights)."""

        for server_name, session in self.sessions.items():
            result: types.ListToolsResult = await session.list_tools()

            if self.debug:
                print(f"[MCP] Server '{server_name}' → {len(result.tools)} tools")

            for tool in result.tools:
                llm_name = f"{server_name}__{tool.name}"

                td = ToolDescriptor(
                    llm_name=llm_name,
                    server_name=server_name,
                    tool_name=tool.name,
                    description=tool.description or "",
                    input_schema=tool.inputSchema
                    or {"type": "object", "properties": {}, "required": []},
                )

                self.tools[llm_name] = td

                if self.debug:
                    print(f"  → registered tool: {llm_name}")

    def build_llm_tools_spec(self) -> List[Dict[str, Any]]:
        """Expose MCP tools in OpenAI-style function-calling format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": td.llm_name,
                    "description": td.description,
                    "parameters": td.input_schema,
                },
            }
            for td in self.tools.values()
        ]

    async def call_tool(self, llm_tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool based on its LLM-exposed name."""
        td = self.tools.get(llm_tool_name)
        if not td:
            raise ValueError(f"Unknown tool: {llm_tool_name}")

        session = self.sessions[td.server_name]

        if self.debug:
            print(f"\n[MCP] Calling {llm_tool_name} with args={arguments}")

        result = await session.call_tool(td.tool_name, arguments=arguments)

        # flatten results
        outputs = []
        for item in result.content:
            if hasattr(item, "text"):
                outputs.append(item.text)
            elif isinstance(item, dict) and "text" in item:
                outputs.append(str(item["text"]))
            else:
                outputs.append(str(item))

        return "\n".join(outputs)
