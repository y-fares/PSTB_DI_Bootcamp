# test_mcp.py
# ### Quick check that MCP servers are reachable and expose tools

from __future__ import annotations

import asyncio

from config import load_mcp_server_configs
from mcp_multi_client import MCPMultiClient


async def main():
    configs = load_mcp_server_configs()
    print("Configured servers:")
    for cfg in configs:
        print(f"- {cfg.name}: {cfg.command} {' '.join(cfg.args)}")

    async with MCPMultiClient(configs) as client:
        print("\nDiscovered tools:")
        for name, td in client.tools.items():
            print(f"- {name} (server={td.server_name})")
            print(f"  description: {td.description}")


if __name__ == "__main__":
    asyncio.run(main())
