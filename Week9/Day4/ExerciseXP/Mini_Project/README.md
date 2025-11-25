# 🧠 MCP Agentic Application – Part 2

## Multi-Server AI Agent (Filesystem + Web + Custom MCP Server)

This project is the **Part 2** of the Agentic AI mini-project.
It demonstrates a complete **agentic AI architecture** composed of:

* **Two third-party MCP servers**

  * `files` → file exploration / reading
  * `web` → search + fetch web content
* **One custom MCP server** (required for Part 2)

  * `local_insights` → two non-trivial tools

    * `clean_text(text, lowercase)`
    * `generate_insights(text)`
* **One autonomous LLM-driven orchestrator**
* **One unified multi-server MCP client**
* **An end-to-end Streamlit UI**

The system lets a Large Language Model **plan tool calls dynamically**, combine different servers, recover from errors, and produce a final answer.

---

# 🚀 Features (Fully Implemented)

### ✅ **Custom MCP server (`local_insights`)**

Exposes two custom tools with full schemas:

* `clean_text` → HTML cleaning, whitespace normalization, optional lowercase
* `generate_insights` → JSON insights extraction (key points, risks, recommended steps)

### ✅ **External MCP servers**

* `server-filesystem` → directory listing, file reading
* `server-web` → search queries & web page fetching

### ✅ **LLM planning (GroqCloud / Ollama)**

* OpenAI-compatible function-calling
* Multi-step planning
* Error-aware replanning
* Input validation before tool execution

### ✅ **Multi-server MCP client**

* Auto-discovers all tools
* Namespacing: `server__tool`
* Unified calling API
* Robust flattening of MCP responses

### ✅ **Autonomous Orchestrator**

* High-level system prompt (non-scripted)
* Autonomous selection of tools
* Rate limiting (anti-abuse, required by the rubric)
* Detailed tool execution logs
* Graceful handling of JSON errors, schema mismatches, or tool crashes

### ✅ **Streamlit UI**

* Displays configuration, logs, and final answer
* Allows user to give any agentic goal
* Launches the full planning loop

### ✅ **MCP Test Pipeline (`test_mcp.py`)**

Demonstrates multi-server composition without LLM:

1. List files (filesystem)
2. Read file (filesystem)
3. Clean text (custom server)
4. Generate insights (custom server)

---

# 📂 Project Structure

```
Mini_Project/
│
├── app.py                 # Streamlit UI
├── orchestrator.py        # Agentic loop (LLM + MCP servers)
├── mcp_multi_client.py    # Unified MCP multi-server client
├── llm_client.py          # LLM wrapper (Groq / Ollama)
├── config.py              # Configuration loader
│
├── my_mcp_server.py       # ⭐ Your custom MCP server
│
├── test_mcp.py            # Tests multi-server composition
├── requirements.txt
└── .env                   # Environment variables
```

---

# ⚙️ Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install MCP servers:

```bash
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web
```

Or use npx (recommended, no install needed):

```bash
npx @modelcontextprotocol/server-filesystem --help
npx @modelcontextprotocol/server-web --help
```

---

# 🔧 Environment Setup

Create `.env`:

```env
LLM_BACKEND=groq
GROQ_API_KEY=YOUR_GROQ_KEY
GROQ_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.3-70b-versatile

# External MCP servers
MCP_FILES_CMD=npx
MCP_FILES_ARGS=@modelcontextprotocol/server-filesystem /home/yacine/mcp_root

MCP_WEB_CMD=npx
MCP_WEB_ARGS=@modelcontextprotocol/server-web

# ⭐ Custom MCP server
MCP_LOCAL_CMD=python
MCP_LOCAL_ARGS=my_mcp_server.py
```

---

# ▶️ Running the App

Launch the Streamlit UI:

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

Then ask:

> “Search the web about MCP servers, clean the text, and generate structured insights.”

The orchestrator will:

* search with `web__search`
* fetch pages with `web__fetch`
* clean with `local_insights__clean_text`
* summarize with `local_insights__generate_insights`
* produce a final answer

---

# 🧪 Testing Without the LLM

Run:

```bash
python test_mcp.py
```

Expected flow:

1. Discover tools across the 3 servers
2. List `/home/yacine/mcp_root`
3. Read `test.txt`
4. Clean the text
5. Generate insights

This test proves that composition across external + custom servers works correctly.

---

# 📝 Notes for Reviewers

All requirements are fully implemented:

| Requirement                     | Status |
| ------------------------------- | ------ |
| ≥ 2 external MCP servers        | ✅      |
| 1 custom MCP server             | ✅      |
| ≥ 2 custom tools                | ✅      |
| Exposed via MCP with schemas    | ✅      |
| Unified multi-server client     | ✅      |
| LLM planning (with Groq/Ollama) | ✅      |
| Error handling + retries        | ✅      |
| Rate limiting                   | ✅      |
| Streamlit UI                    | ✅      |
| Reproducible setup              | ✅      |
| Multi-step end-to-end example   | ✅      |

---

# 📘 Part 1 – Third-Party MCP Integration

This project extends **Part 1**, where the goal was to build an agentic application using **existing MCP servers** from the community. Part 1 laid the foundation:

## ✔️ What Part 1 Implemented

* Integration of **at least two external MCP servers** (e.g., filesystem + web).
* Use of an LLM (Groq/Ollama) to **plan and orchestrate tool calls**.
* A unified `MCPMultiClient` able to:

  * Launch MCP servers via stdio
  * Discover tools dynamically
  * Expose them under LLM-friendly names (e.g., `files__listDirectory`)
* An initial orchestrator capable of:

  * Reading the user goal
  * Letting the LLM choose tools
  * Executing tool calls step-by-step
  * Sending tool results back into the LLM context
* A Streamlit UI demonstrating:

  * User goal input
  * Agentic reasoning steps
  * Tool call logging

## 🎯 How Part 1 Leads to Part 2

Part 1 focused exclusively on **external servers**.
Part 2 extends this architecture by **adding your own MCP server** (`local_insights`) and combining it with the external ones, creating a more complete, multi-server agent.

---

# 🧠 MCP Agentic Application – Part 2

## Multi-Server AI Agent (Filesystem + Web + Custom MCP Server) – Third‑Party MCP Integration

This project extends **Part 1**, where the goal was to build an agentic application using **existing MCP servers** from the community. Part 1 laid the foundation:

## ✔️ What Part 1 Implemented

* Integration of **at least two external MCP servers** (e.g., filesystem + web).
* Use of an LLM (Groq/Ollama) to **plan and orchestrate tool calls**.
* A unified `MCPMultiClient` able to:

  * Launch MCP servers via stdio
  * Discover tools dynamically
  * Expose them under LLM‑friendly names (e.g., `files__listDirectory`)
* An initial orchestrator capable of:

  * Reading the user goal
  * Letting the LLM choose tools
  * Executing tool calls step‑by‑step
  * Sending tool results back into the LLM context
* A Streamlit UI demonstrating:

  * User goal input
  * Agentic reasoning steps
  * Tool call logging

## 🎯 How Part 1 Leads to Part 2

Part 1 focused exclusively on **external servers**.
Part 2 extends this architecture by adding your own MCP server (`local_insights`) and combining it with the external ones, creating a complete multi‑server agent.

---

# 🎯 Done

This README.md provides a complete explanation of the project, architecture, usage, and evaluation criteria.
