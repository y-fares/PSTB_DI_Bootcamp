# config.py
# ### Central configuration for LLM backend and MCP servers

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List


# ### LLM configuration dataclass
@dataclass
class LLMConfig:
    backend: str          # "groq" or "ollama"
    model: str
    base_url: str
    api_key: str


# ### MCP server configuration dataclass
@dataclass
class MCPServerConfig:
    name: str             # logical name, used for namespacing tools
    command: str          # e.g. "npx" or "python"
    args: List[str]       # command arguments for the server
    env: dict | None = None


# ### Load LLM configuration from environment variables
def load_llm_config() -> LLMConfig:
    backend = os.getenv("LLM_BACKEND", "groq").lower()

    if backend == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("GROQ_API_KEY is required when LLM_BACKEND='groq'.")

        return LLMConfig(
            backend="groq",
            model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            api_key=api_key,
        )

    if backend == "ollama":
        # Ollama OpenAI-compatible endpoint
        return LLMConfig(
            backend="ollama",
            model=os.getenv("LLM_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            # Ollama ignores the key but OpenAI client requires one
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        )

    raise ValueError(f"Unsupported LLM_BACKEND: {backend}")


# ### Load MCP servers configuration from env
# You **must** adapt these to match the actual community servers you choose.
def load_mcp_server_configs() -> List[MCPServerConfig]:
    """
    Minimal example:
    - MCP_GITHUB_ARGS="--stdio @modelcontextprotocol/server-github"
    - MCP_FILES_ARGS="--stdio @modelcontextprotocol/server-filesystem /tmp"

    Adjust commands/args according to each server README.
    """

    servers: List[MCPServerConfig] = []

    # #### Example third-party server 1 (e.g. GitHub MCP server)
    github_args = os.getenv("MCP_GITHUB_ARGS")
    if github_args:
        servers.append(
            MCPServerConfig(
                name="github",
                command=os.getenv("MCP_GITHUB_CMD", "npx"),
                args=github_args.split(),
                env=None,
            )
        )

    # #### Example third-party server 2 (e.g. filesystem / CSV / notes)
    files_args = os.getenv("MCP_FILES_ARGS")
    if files_args:
        servers.append(
            MCPServerConfig(
                name="files",
                command=os.getenv("MCP_FILES_CMD", "npx"),
                args=files_args.split(),
                env=None,
            )
        )

    # #### Your own MCP server (custom tools)
    local_args = os.getenv("MCP_LOCAL_ARGS")
    if local_args:
        servers.append(
            MCPServerConfig(
                name="local_insights",
                command=os.getenv("MCP_LOCAL_CMD", "python"),
                args=local_args.split(),
                env=None,
            )
        )

    if not servers:
        raise RuntimeError(
            "No MCP servers configured. "
            "Set at least MCP_GITHUB_ARGS and MCP_FILES_ARGS (and optionally MCP_LOCAL_ARGS)."
        )

    return servers
