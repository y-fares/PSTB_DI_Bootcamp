# 🧠 MCP Agentic Application – Part 2  
## Multi-Server AI Agent (Filesystem + Web + Custom MCP Server)

This project is the **Part 2** of the Agentic AI mini-project.  
It demonstrates a complete **agentic AI architecture** composed of:

- **Two third-party MCP servers**  
  - `files` → file exploration / reading  
  - `web` → search + fetch web content  
- **One custom MCP server** (required for Part 2)  
  - `local_insights` → two non-trivial tools  
    - `clean_text(text, lowercase)`  
    - `generate_insights(text)`  
- **One autonomous LLM-driven orchestrator**  
- **One unified multi-server MCP client**  
- **An end-to-end Streamlit UI**

The system lets a Large Language Model **plan tool calls dynamically**, combine different servers, recover from errors, and produce a final answer.

---

# 🚀 Features (Fully Implemented)

### ✅ **Custom MCP server (`local_insights`)**
Exposes two custom tools with full schemas:
- `clean_text` → HTML cleaning, whitespace normalization, optional lowercase  
- `generate_insights` → JSON insights extraction (key points, risks, recommended steps)

### ✅ **External MCP servers**
- `server-filesystem` → directory listing, file reading  
- `server-web` → search queries & web page fetching  

### ✅ **LLM planning (GroqCloud / Ollama)**
- OpenAI-compatible function-calling  
- Multi-step planning  
- Error-aware replanning  
- Input validation before tool execution

### ✅ **Multi-server MCP client**
- Auto-discovers all tools  
- Namespacing: `server__tool`  
- Unified calling API  
- Robust flattening of MCP responses  

### ✅ **Autonomous Orchestrator**
- High-level system prompt (non-scripted)  
- Autonomous selection of tools  
- Rate limiting (anti-abuse, required by the rubric)  
- Detailed tool execution logs  
- Graceful handling of JSON errors, schema mismatches, or tool crashes  

### ✅ **Streamlit UI**
- Displays configuration, logs, and final answer  
- Allows user to give any agentic goal  
- Launches the full planning loop  

### ✅ **MCP Test Pipeline (`test_mcp.py`)**
Demonstrates multi-server composition without LLM:
1. List files (filesystem)  
2. Read file (filesystem)  
3. Clean text (custom server)  
4. Generate insights (custom server)  

---

# 📂 Project Structure

Mini_Project/
│
├── app.py # Streamlit UI
├── orchestrator.py # Agentic loop (LLM + MCP servers)
├── mcp_multi_client.py # Unified MCP multi-server client
├── llm_client.py # LLM wrapper (Groq / Ollama)
├── config.py # Configuration loader
│
├── my_mcp_server.py # ⭐ Your custom MCP server
│
├── test_mcp.py # Tests multi-server composition
├── requirements.txt
└── .env # Environment variables

yaml
Copier le code

---

# ⚙️ Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Install MCP servers:

bash
Copier le code
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-web
Or use npx (recommended, no install needed):

bash
Copier le code
npx @modelcontextprotocol/server-filesystem --help
npx @modelcontextprotocol/server-web --help
🔧 Environment Setup
Create .env:

env
Copier le code
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
▶️ Running the App
Launch the Streamlit UI:

bash
Copier le code
streamlit run app.py
Open:

arduino
Copier le code
http://localhost:8501
Then ask:

“Search the web about MCP servers, clean the text, and generate structured insights.”

The orchestrator will:

search with web__search

fetch pages with web__fetch

clean with local_insights__clean_text

summarize with local_insights__generate_insights

produce a final answer

🧪 Testing Without the LLM
Run:

bash
Copier le code
python test_mcp.py
Expected flow:

Discover tools across the 3 servers

List /home/yacine/mcp_root

Read test.txt

Clean the text

Generate insights

This test proves that composition across external + custom servers works correctly.