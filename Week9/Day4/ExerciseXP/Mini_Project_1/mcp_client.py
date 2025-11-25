# mcp_client.py

import subprocess
import json
from typing import Any, Dict, Tuple

class MCPConnection:
    """
    Simple wrapper around an MCP server running over STDIO.
    """

    def __init__(self, name: str, command: str):
        """
        command: shell command to start the MCP server, e.g. 'python mcp_insights_server/server.py'
        """
        self.name = name
        self.proc = subprocess.Popen(
            command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._id_counter = 0

    def _next_id(self) -> int:
        self._id_counter += 1
        return self._id_counter

    def send_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send a JSON-RPC request and wait for a single JSON line response.
        """
        req_id = self._next_id()
        request = {"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}

        assert self.proc.stdin is not None
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()

        assert self.proc.stdout is not None
        line = self.proc.stdout.readline()
        response = json.loads(line)
        return response

    def list_tools(self) -> Dict[str, Any]:
        """
        Get the tools list from this MCP server.
        """
        return self.send_request("tools/list", {})

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a MCP tool with arguments.
        """
        return self.send_request("tools/call", {"name": name, "arguments": arguments})

    def close(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()

