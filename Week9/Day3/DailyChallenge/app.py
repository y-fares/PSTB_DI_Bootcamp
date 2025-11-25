"""
# Agentic RAG – Streamlit Frontend

This Streamlit app:
- Loads API keys and LangSmith config from a `.env` file
- Exposes a simple text box + "Submit" button
- Returns a **simulated** response for now
- Tries to load `agentic_rag.ipynb` as text (preview only)

The actual agent / RAG pipeline should live in `agentic_rag.ipynb`.
"""

import os
from pathlib import Path
from textwrap import shorten

import streamlit as st
from dotenv import load_dotenv

# -----------------------------
# Environment & configuration
# -----------------------------

# Load variables from .env into os.environ
load_dotenv()

# Core API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# LangSmith / LangChain tracing configuration
# These are read by LangChain internally when you build the real agent.
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")

# Make sure they’re also set in the process env (for LangChain)
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
if LANGCHAIN_ENDPOINT:
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT
if LANGCHAIN_PROJECT:
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
if LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY


def _bool_env(value: str) -> bool:
    """Convert common truthy strings to boolean."""
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


# -----------------------------
# Backend stub (to be replaced)
# -----------------------------

def call_agentic_rag_backend(query: str) -> str:
    """
    Placeholder for the real Agentic RAG pipeline.

    In the notebook `agentic_rag.ipynb`, you should eventually expose a function
    (e.g. via a Python module or an API) and call it from here instead of this stub.
    """
    tracing_status = "ON" if _bool_env(LANGCHAIN_TRACING_V2) else "OFF"

    # This is just a fake answer for now.
    simulated_answer = (
        "🔧 [SIMULATED RESPONSE]\n\n"
        "The real Agentic RAG pipeline is not wired yet.\n\n"
        f"- Your query (truncated): `{shorten(query, width=160, placeholder='…')}`\n"
        f"- LangSmith tracing: **{tracing_status}**\n"
        "- GROQ / Tavily / Google tools not yet invoked here.\n"
    )
    return simulated_answer


def load_agentic_notebook_preview(max_chars: int = 1500) -> str:
    """
    Try to load `agentic_rag.ipynb` as raw text (JSON).

    This is just for debugging / visibility in the UI.
    """
    nb_path = Path("agentic_rag.ipynb")
    if not nb_path.exists():
        return "agentic_rag.ipynb not found in current directory."

    try:
        raw = nb_path.read_text(encoding="utf-8", errors="ignore")
        if len(raw) > max_chars:
            return raw[:max_chars] + "\n\n...[truncated preview]..."
        return raw
    except Exception as exc:  # noqa: BLE001
        return f"Error reading agentic_rag.ipynb: {exc}"


# -----------------------------
# Streamlit UI
# -----------------------------

def main() -> None:
    """Main entry point for the Streamlit app UI."""
    st.set_page_config(page_title="Agentic RAG Demo", page_icon="🧠")

    st.title("🧠 Agentic RAG – Streamlit Frontend")
    st.write(
        "This is a **scaffold**: the real agent logic lives in "
        "`agentic_rag.ipynb` and will be plugged in later."
    )

    # Sidebar: show which keys are present (without printing their values).
    st.sidebar.header("Environment status")

    def _status(name: str, value: str | None) -> None:
        icon = "✅" if value else "⚠️"
        st.sidebar.write(f"{icon} `{name}`: {'set' if value else 'missing'}")

    _status("GOOGLE_API_KEY", GOOGLE_API_KEY)
    _status("TAVILY_API_KEY", TAVILY_API_KEY)
    _status("GROQ_API_KEY", GROQ_API_KEY)
    _status("LANGCHAIN_API_KEY", LANGCHAIN_API_KEY)

    st.sidebar.markdown("---")
    st.sidebar.write("**LangSmith / LangChain tracing**")
    st.sidebar.write(f"- `LANGCHAIN_TRACING_V2`: `{LANGCHAIN_TRACING_V2}`")
    st.sidebar.write(
        f"- `LANGCHAIN_ENDPOINT`: `{LANGCHAIN_ENDPOINT or 'not set'}`"
    )
    st.sidebar.write(f"- `LANGCHAIN_PROJECT`: `{LANGCHAIN_PROJECT or 'not set'}`")

    # Main input area
    user_query = st.text_area(
        "Ask something to the Agentic RAG system:",
        placeholder="e.g. 'Summarize the latest design of my RAG pipeline and suggest improvements.'",
        height=160,
    )

    if st.button("Submit", type="primary"):
        if not user_query.strip():
            st.warning("Please enter a query before submitting.")
        else:
            with st.spinner("Thinking with a simulated backend..."):
                try:
                    response = call_agentic_rag_backend(user_query)
                    st.markdown("### Response")
                    st.markdown(response)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Unexpected error while calling backend: {exc}")

    # Notebook preview for debugging
    with st.expander("📓 agentic_rag.ipynb – raw preview"):
        st.caption(
            "This is just a text preview of the notebook file. "
            "The real RAG / agent code should live there."
        )
        preview = load_agentic_notebook_preview()
        st.code(preview, language="json")


if __name__ == "__main__":
    main()
