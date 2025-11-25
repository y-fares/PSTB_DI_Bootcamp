# app.py
# ### Streamlit UI for the agentic MCP application

from __future__ import annotations

import asyncio
from typing import List

import streamlit as st  # pip install streamlit

from orchestrator import AgenticOrchestrator, OrchestratorResult
from config import load_llm_config


# ### Synchronous wrapper for the async orchestrator
def run_agent_sync(user_goal: str) -> OrchestratorResult:
    orchestrator = AgenticOrchestrator()
    return asyncio.run(orchestrator.run(user_goal))


# ### Streamlit layout
def main() -> None:
    st.set_page_config(page_title="MCP Agentic App", layout="wide")

    llm_cfg = load_llm_config()

    st.title("🔧 MCP Agentic Application")

    st.markdown(
        f"""
        ### Configuration
        - **LLM backend:** `{llm_cfg.backend}`
        - **Model:** `{llm_cfg.model}`
        """
    )

    st.markdown("### User goal")
    user_goal = st.text_area(
        "Describe what you want the agent to do:",
        height=150,
        placeholder="Example: Analyse this GitHub repo, open existing issues and propose a refactoring plan...",
    )

    if st.button("Run agent", type="primary"):

        if not user_goal.strip():
            st.error("Please provide a non-empty goal.")
        else:
            with st.spinner("Running agent with MCP tools..."):
                result = run_agent_sync(user_goal)

            st.subheader("✅ Final answer")
            st.write(result.final_answer)

            st.subheader("🔍 Tool calls log")
            for log in result.tool_logs:
                with st.expander(
                    f"Step {log.step} – {log.tool_name} "
                    f"({'OK' if log.success else 'ERROR'})"
                ):
                    st.markdown(f"**Server:** `{log.server_name}`")
                    st.markdown("**Arguments:**")
                    st.json(log.arguments)
                    st.markdown("**Result preview:**")
                    st.text(log.result_preview)
                    if log.error:
                        st.markdown("**Error:**")
                        st.code(log.error)

            st.subheader("🧠 Raw messages trace (for debugging)")
            with st.expander("Show messages"):
                st.json(result.messages_trace)


if __name__ == "__main__":
    main()
