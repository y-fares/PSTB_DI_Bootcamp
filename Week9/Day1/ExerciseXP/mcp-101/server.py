# server.py
from mcp.server.fastmcp import FastMCP

# Create the MCP server with a name
mcp = FastMCP("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


@mcp.resource("greeting://{name}")
def greet(name: str) -> str:
    """Return a greeting string for the given name."""
    return f"Hello, {name}!"


if __name__ == "__main__":
    # Start the server loop over STDIO
    # This works with: mcp run server.py
    mcp.run()
