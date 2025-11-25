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
    llm_name: str               # namespaced name exposed to LLM (e.g. local_insights__clean_text)
    server_name: str            # MCP server logical name (e.g. local_insights)
    tool_name: str              # tool name as exposed by MCP server (e.g. clean_text)
    description: str
    input_schema: Dict[str, Any]


class MCPMultiClient:
    """
    ### Manage multiple MCP server sessions
    - Connects to multiple servers via stdio
    - Discovers tools (including your local_insights server)
    - Provides a unified `call_tool` API for the orchestrator
    """

    def __init__(
        self,
        server_configs: Optional[List[MCPServerConfig]] = None,
        debug: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        server_configs : Optional[List[MCPServerConfig]]
            Pre-loaded configs (mainly used for tests). If None, `load_mcp_server_configs()`
            is called and will enforce:
            - ≥ 2 external servers (e.g. files + web)
            - 1 local server (local_insights) for your custom tools.
        debug : bool
            If True, print basic information about servers and tools discovery.
        """
        self.server_configs = server_configs or load_mcp_server_configs()
        self._exit_stack: AsyncExitStack | None = None
        self.sessions: Dict[str, ClientSession] = {}
        self.tools: Dict[str, ToolDescriptor] = {}  # llm_name -> ToolDescriptor
        self.debug = debug

    async def __aenter__(self) -> "MCPMultiClient":
        self._exit_stack = AsyncExitStack()

        # Connect to each configured MCP server
        for cfg in self.server_configs:
            if self.debug:
                print(f"[MCPMultiClient] Connecting to server '{cfg.name}' "
                      f"with command: {cfg.command} {' '.join(cfg.args)}")

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
        """
        Discover tools on all MCP servers and build a registry.

        Each tool is exposed to the LLM under a namespaced name:
        - Example: server 'local_insights' + tool 'clean_text'
          => llm_name = 'local_insights__clean_text'
        This is what the LLM will call in tool_calls.
        """
        for server_name, session in self.sessions.items():
            result: types.ListToolsResult = await session.list_tools()

            if self.debug:
                print(f"[MCPMultiClient] Server '{server_name}' exposes {len(result.tools)} tools.")

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

                if self.debug:
                    print(f"  - Registered tool '{llm_name}' "
                          f"(server={server_name}, original_name={tool.name})")

    def build_llm_tools_spec(self) -> List[Dict[str, Any]]:
        """
        Convert MCP tools into OpenAI-style tools for the LLM.

        This is what you pass as `tools=...` to the LLM (Groq / Ollama)
        so it can plan and emit proper tool_calls.
        """
        tools_for_llm: List[Dict[str, Any]] = []

        for td in self.tools.values():
            properties = td.input_schema.get("properties", {})
            required = td.input_schema.get("required", [])

            tools_for_llm.append(
                {
                    "type": "function",
                    "function": {
                        "name": td.llm_name,  # e.g. local_insights__generate_insights
                        "description": td.description,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                            "required": required,
                        },
                    },
                }
            )

        if self.debug:
            print(f"[MCPMultiClient] Built LLM tools spec with {len(tools_for_llm)} tools.")

        return tools_for_llm

    async def call_tool(self, llm_tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        Call one tool by its LLM-exposed name and return text content.

        Parameters
        ----------
        llm_tool_name : str
            Namespaced tool name, e.g. 'local_insights__clean_text'.
        arguments : Dict[str, Any]
            Arguments dictionary that must match the tool's input schema.

        Returns
        -------
        str
            Flattened textual result (joined from MCP content parts).
        """
        td = self.tools.get(llm_tool_name)
        if not td:
            raise ValueError(
                f"Unknown tool name from LLM: '{llm_tool_name}'. "
                "Check that the tool was correctly discovered and namespaced."
            )

        session = self.sessions.get(td.server_name)
        if not session:
            raise RuntimeError(
                f"No active MCP session for server '{td.server_name}' "
                f"(tool '{llm_tool_name}')."
            )

        if self.debug:
            print(f"[MCPMultiClient] Calling tool '{llm_tool_name}' on server '{td.server_name}' "
                  f"with args: {arguments}")

        result = await session.call_tool(td.tool_name, arguments=arguments)

        # Flatten text content from MCP result
        parts: List[str] = []
        for item in result.content:
            # TextContent-like objects
            if hasattr(item, "text"):
                parts.append(item.text)
            elif isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                # Fallback: stringify the whole item
                parts.append(str(item))

        output = "\n".join(parts)

        if self.debug:
            preview = output[:200].replace("\n", " ")
            print(f"[MCPMultiClient] Tool '{llm_tool_name}' returned: {preview}...")

        return output
