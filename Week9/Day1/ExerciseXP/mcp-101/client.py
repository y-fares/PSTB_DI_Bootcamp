# client.py
import asyncio

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


# Parameters for starting the server over STDIO via the `mcp` CLI
server_params = StdioServerParameters(
    command="mcp",              # Use the MCP CLI executable
    args=["run", "server.py"],  # Run our local server file
    env=None,                   # Default environment
)


async def run() -> None:
    """Connect to the MCP server, discover features, and call them."""
    # Open the stdio connection: this spawns `mcp run server.py`
    async with stdio_client(server_params) as (read, write):
        # Create a client session over the MCP streams
        async with ClientSession(read, write) as session:
            # Handshake with the server (capabilities, etc.)
            await session.initialize()

            # ----- List resources -----
            resources = await session.list_resources()
            print("Resources URIs:", [r.uri for r in resources.resources])

            # ----- List tools -----
            tools = await session.list_tools()
            print("Tools names:", [t.name for t in tools.tools])

            # ----- Read greeting://hello -----
            resource_result = await session.read_resource("greeting://hello")
            first_block = resource_result.contents[0]

            if isinstance(first_block, types.TextContent):
                print("Greeting content:", first_block.text)
            else:
                print("Greeting raw content:", first_block)

            # ----- Call add(a=1, b=7) -----
            tool_result = await session.call_tool("add", arguments={"a": 1, "b": 7})

            # Prefer structured output if available
            if tool_result.structuredContent and "result" in tool_result.structuredContent:
                value = tool_result.structuredContent["result"]
                print("add(1, 7) result (structured):", value)
            else:
                # Fallback: unstructured content
                content_block = tool_result.content[0]
                if isinstance(content_block, types.TextContent):
                    print("add(1, 7) result (text):", content_block.text)
                else:
                    print("add(1, 7) raw result:", content_block)


if __name__ == "__main__":
    asyncio.run(run())
