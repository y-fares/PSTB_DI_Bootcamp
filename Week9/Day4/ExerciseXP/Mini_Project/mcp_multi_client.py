# mcp_multi_client.py
# ### Async MCP multi-server client using the official MCP Python SDK

from __future__ import annotations

from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any, Dict, List

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

from config import MCPServerConfig, load_mcp_server_configs


@dataclass
class ToolDescriptor:
    """Metadata for a tool, mapped to an LLM-exposed name."""
    llm_name: str               # namespaced name exposed to LLM
    server_name: str            # MCP server logical name
    tool_name: str              # tool name as exposed by MCP server
    description: str
    input_schema: Dict[str, Any]


class MCPMultiClient:
    """
    ### Manage multiple MCP server sessions
    - Connects to multiple servers via stdio
    - Discovers tools
    - Provides a unified `call_tool` API
    """

    def __init__(self, server_configs: List[MCPServerConfig] | None = None) -> None:
        self.server_configs = server_configs or load_mcp_server_configs()
        self._exit_stack: AsyncExitStack | None = None
        self.sessions: Dict[str, ClientSession] = {}
        self.tools: Dict[str, ToolDescriptor] = {}  # llm_name -> ToolDescriptor

    async def __aenter__(self) -> "MCPMultiClient":
        self._exit_stack = AsyncExitStack()
        for cfg in self.server_configs:
            server_params = StdioServerParameters(
                command=cfg.command,
                args=cfg.args,
                env=cfg.env,
            )
            read_stream, write_stream = await self._exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            session = ClientSession(read_stream, write_stream)
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
        """Discover tools on all MCP servers and build a registry."""
        for server_name, session in self.sessions.items():
            result: types.ListToolsResult = await session.list_tools()
            for tool in result.tools:
                llm_name = f"{server_name}__{tool.name}"
                input_schema = tool.inputSchema or {
                    "type": "object",
                    "properties": {},
                    "required": [],
                }
                td = ToolDescriptor(
                    llm_name=llm_name,
                    server_name=server_name,
                    tool_name=tool.name,
                    description=tool.description or "",
                    input_schema=input_schema,
                )
                self.tools[llm_name] = td

    def build_llm_tools_spec(self) -> List[Dict[str, Any]]:
        """Convert MCP tools into OpenAI-style tools for the LLM."""
        tools_for_llm: List[Dict[str, Any]] = []

        for td in self.tools.values():
            properties = td.input_schema.get("properties", {})
            required = td.input_schema.get("required", [])

            tools_for_llm.append(
                {
                    "type": "function",
                    "function": {
                        "name": td.llm_name,
                        "description": td.description,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required,
                        },
                    },
                }
            )

        return tools_for_llm

    async def call_tool(self, llm_tool_name: str, arguments: Dict[str, Any]) -> str:
        """Call one tool by its LLM-exposed name and return text content."""
        td = self.tools.get(llm_tool_name)
        if not td:
            raise ValueError(f"Unknown tool name from LLM: {llm_tool_name}")

        session = self.sessions.get(td.server_name)
        if not session:
            raise RuntimeError(f"No active MCP session for server '{td.server_name}'.")

        result = await session.call_tool(td.tool_name, arguments=arguments)

        # Flatten text content from MCP result
        parts: List[str] = []
        for item in result.content:
            # TextContent case
            if hasattr(item, "text"):
                parts.append(item.text)
            elif isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                # fallback
                parts.append(str(item))

        return "\n".join(parts)
