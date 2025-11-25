# llm_client.py
# ### LLM wrapper using OpenAI-compatible API (Groq or Ollama)

from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI  # pip install openai
from config import load_llm_config


# ### Initialize global LLM client and config
_llm_cfg = load_llm_config()

client = OpenAI(
    api_key=_llm_cfg.api_key,
    base_url=_llm_cfg.base_url,
)


# ### Call LLM with tools to decide the next action
def plan_with_llm(
    messages: List[Dict[str, Any]],
    tools_for_llm: List[Dict[str, Any]],
    max_tokens: int = 800,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Call the LLM with:
    - current conversation messages
    - available tools (OpenAI-style tool schema)

    Returns the raw assistant message including potential tool_calls.
    """

    response = client.chat.completions.create(
        model=_llm_cfg.model,
        messages=messages,
        tools=tools_for_llm,
        tool_choice="auto",
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Single choice for simplicity
    return response.choices[0].message.to_dict()
