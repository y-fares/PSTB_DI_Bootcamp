# app.py

import os
import streamlit as st
from mcp_client import MCPConnection
from orchestrator import orchestrate

st.set_page_config(page_title="Smart Data Scout", layout="wide")

st.title("🧠 Smart Data Scout (MCP Agent)")

user_goal = st.text_area("Describe your goal:", height=120, value="Find recent information about Tesla and summarize the main trends.")

if st.button("Run agent"):
    # Start MCP connections based on env
    # You will set these commands according to the third-party servers you chose.
    web_cmd = os.environ.get("MCP_WEB_CMD", "python mcp_web_server.py")
    files_cmd = os.environ.get("MCP_FILES_CMD", "python mcp_files_server.py")
    insights_cmd = os.environ.get("MCP_INSIGHTS_CMD", "python mcp_insights_server/server.py")

    servers = {
        "web": MCPConnection("web", web_cmd),
        "files": MCPConnection("files", files_cmd),
        "insights": MCPConnection("insights", insights_cmd),
    }

    try:
        result = orchestrate(user_goal, servers, max_steps=6)
        final_answer = result["final_answer"]
        steps = result["steps"]

        st.subheader("Final Answer")
        st.markdown(final_answer)

        st.subheader("Tool Call Log")
        for h in steps:
            with st.expander(f"Step {h.step} - {h.server}.{h.tool}"):
                st.write("**Arguments:**")
                st.json(h.args)
                st.write("**Result summary:**")
                st.write(h.result_summary)

    finally:
        # Always close MCP processes
        for conn in servers.values():
            conn.close()

