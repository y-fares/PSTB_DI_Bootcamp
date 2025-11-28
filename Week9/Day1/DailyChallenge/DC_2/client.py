import asyncio
import sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Use local server.py with this interpreter to avoid PATH conflicts
SERVER_PATH = Path(__file__).parent / "server.py"
server_params = StdioServerParameters(
    command=sys.executable, args=[str(SERVER_PATH)], env=None
)

def extract_content(payload):
    if hasattr(payload, "contents"):
        contents = payload.contents
        if contents:
            first = contents[0]
            if hasattr(first, "text"):
                return first.text
            if isinstance(first, dict) and "text" in first:
                return first["text"]
            return str(first)
    if hasattr(payload, "content"):
        return payload.content
    return str(payload)


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            resources = await session.list_resources()
            print("Resources:")
            for res in resources.resources:
                print(f"- {res.uri} ({res.name or ''})")

            tools = await session.list_tools()
            print("Tools:")
            for tool in tools.tools:
                print(f"- {tool.name}")

            cities = await session.read_resource("cities://list")
            print("cities://list ->")
            print(extract_content(cities))

            weather = await session.call_tool("get_weather", {"city": "Paris"})
            print("get_weather(Paris) ->", extract_content(weather))


if __name__ == "__main__":
    asyncio.run(run())
