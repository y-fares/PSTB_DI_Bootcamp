# HTTP Web Search Briefing Bot (Python version)

## 1. Prerequisites

- Python 3.10+
- `pip`
- A Tavily API key (or change the search API)
- A local LLM over HTTP (e.g. Ollama)

## 2. Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install fastapi uvicorn requests
