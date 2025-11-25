# app.py
# ### Streamlit UI for the MCP agentic application

from __future__ import annotations

import streamlit as st

from config import load_llm_config
from orchestrator import run_agent_sync


def main() -> None:
    # Simple init flag to éviter les bugs de session_state
    if "init" not in st.session_state:
        st.session_state["init"] = True

    st.set_page_config(page_title="MCP Agentic App", layout="wide")

    st.title("🔧 MCP Agentic Application")

    # Petit indicateur pour être sûr que l'app se charge
    st.markdown("✅ **App loaded.** If you see this, Streamlit is running correctly.")

    # Affichage de la config LLM
    try:
        llm_cfg = load_llm_config()
        st.markdown(
            f"""
            ### Configuration
            - **LLM backend:** `{llm_cfg.backend}`
            - **Model:** `{llm_cfg.model}`
            """
        )
    except Exception as e:  # si la config LLM foire, on le voit dans l'UI
        st.error("Error while loading LLM configuration.")
        st.exception(e)
        return

    st.markdown("### User goal")
    user_goal = st.text_area(
        "Describe what you want the agent to do:",
        height=150,
        placeholder="Example: Search the web for recent news on MCP and summarize key trends...",
    )

    if st.button("Run agent", type="primary"):
        if not user_goal.strip():
            st.error("Please provide a non-empty goal.")
        else:
            with st.spinner("Running agent with MCP tools..."):
                try:
                    result = run_agent_sync(user_goal)
                except Exception as e:
                    st.error("Agent crashed while running.")
                    st.exception(e)
                    return

            st.subheader("✅ Final answer")
            st.write(result.final_answer)

            st.subheader("🔍 Tool calls log")
            if not result.tool_logs:
                st.write("No tool calls were recorded.")
            else:
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


# Avec Streamlit, on appelle main() directement (le script est exécuté comme __main__)
main()
