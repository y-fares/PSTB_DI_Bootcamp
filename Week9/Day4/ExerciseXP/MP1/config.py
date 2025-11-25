# config.py
# ### Central configuration for LLM backend and MCP servers

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load .env file at import time
load_dotenv()

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
    env: Optional[Dict[str, str]] = None


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
        return LLMConfig(
            backend="ollama",
            model=os.getenv("LLM_MODEL", "llama3.1"),
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
        )

    raise ValueError(f"Unsupported LLM_BACKEND: {backend}")


# ### Load MCP servers configuration from env
def load_mcp_server_configs() -> List[MCPServerConfig]:
    servers: List[MCPServerConfig] = []

    files_args = os.getenv("MCP_FILES_ARGS")
    if files_args:
        servers.append(
            MCPServerConfig(
                name="files",
                command=os.getenv("MCP_FILES_CMD", "npx"),
                args=files_args.split(),
            )
        )

    web_args = os.getenv("MCP_WEB_ARGS")
    if web_args:
        servers.append(
            MCPServerConfig(
                name="web",
                command=os.getenv("MCP_WEB_CMD", "npx"),
                args=web_args.split(),
            )
        )

    local_args = os.getenv("MCP_LOCAL_ARGS")
    if local_args:
        servers.append(
            MCPServerConfig(
                name="local",
                command=os.getenv("MCP_LOCAL_CMD", "python"),
                args=local_args.split(),
            )
        )

    if len(servers) < 2:
        raise RuntimeError(
            "You must configure at least 2 MCP servers via env vars "
            "(e.g. MCP_FILES_ARGS and MCP_WEB_ARGS)."
        )

    return servers
