# llm_client.py
# ### LLM wrapper using OpenAI-compatible API (Groq or Ollama)

from __future__ import annotations

from typing import Any, Dict, List

from openai import OpenAI
from config import load_llm_config

import logging

logger = logging.getLogger("llm_client")


_llm_cfg = load_llm_config()

client = OpenAI(
    api_key=_llm_cfg.api_key,
    base_url=_llm_cfg.base_url,
)


def plan_with_llm(
    messages: List[Dict[str, Any]],
    tools_for_llm: List[Dict[str, Any]],
    max_tokens: int = 800,
    temperature: float = 0.2,
) -> Dict[str, Any]:
    """
    Call the LLM (GroqCloud or Ollama) with:
    - conversation messages
    - available tools (OpenAI-style tool schema)

    Returns the assistant message dict, including potential `tool_calls`.
    """

    logger.info(
        "Calling LLM backend=%s model=%s with %d messages and %d tools",
        _llm_cfg.backend,
        _llm_cfg.model,
        len(messages),
        len(tools_for_llm),
    )

    try:
        response = client.chat.completions.create(
            model=_llm_cfg.model,
            messages=messages,
            tools=tools_for_llm,
            tool_choice="auto",
            temperature=temperature,
            max_tokens=max_tokens,
        )
    except Exception as e:  # noqa: BLE001
        logger.exception("LLM call failed")
        raise RuntimeError(f"LLM call failed: {e}") from e

    msg = response.choices[0].message.to_dict()
    logger.info("LLM returned role=%s, has_tool_calls=%s",
                msg.get("role"), bool(msg.get("tool_calls")))
    return msg
