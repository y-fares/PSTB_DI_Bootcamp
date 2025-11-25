# test_mcp.py
# ### Test MCP servers: discovery + simple composition example (no LLM)

from __future__ import annotations

import asyncio

from config import load_mcp_server_configs
from mcp_multi_client import MCPMultiClient


async def main() -> None:
    configs = load_mcp_server_configs()
    print("Configured servers:")
    for cfg in configs:
        print(f"- {cfg.name}: {cfg.command} {' '.join(cfg.args)}")

    async with MCPMultiClient(configs, debug=True) as client:
        print("\nDiscovered tools:")
        for name, td in client.tools.items():
            print(f"- {name} (server={td.server_name})")

        # Minimal end-to-end composition demo (no LLM yet):
        # 1) Use local_insights__clean_text
        # 2) Use local_insights__generate_insights
        if "local_insights__clean_text" in client.tools and "local_insights__generate_insights" in client.tools:
            print("\nRunning local_insights tools pipeline:")
            raw = "This  is   a   demo  text. There might be a potential risk here."
            cleaned = await client.call_tool(
                "local_insights__clean_text",
                {"text": raw, "lowercase": True},
            )
            print("Cleaned text:", cleaned)

            insights = await client.call_tool(
                "local_insights__generate_insights",
                {"text": cleaned},
            )
            print("Insights JSON:\n", insights)


if __name__ == "__main__":
    asyncio.run(main())
