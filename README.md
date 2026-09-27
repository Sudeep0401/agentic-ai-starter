# Agentic AI Starter Project

Teaching-ready starter project covering:

- FastAPI
- LLM connection (OpenAI-compatible client)
- Agent loop
- Calculator tool
- Web/search-style tool
- Conversation memory
- PostgreSQL
- pgvector-ready RAG storage
- RAG retrieval
- Guarded tool execution
- pytest tests
- Docker Compose

## 1. Local setup

Requirements:
- Python 3.11+
- uv
- Docker Desktop
- Git
- An LLM API key

Copy environment file:

```bash
cp .env.example .env
```

Put your API key in `.env`.

Install dependencies:

```bash
uv sync
```

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Run the API:

```bash
uv run uvicorn app.main:app --reload
```

Open:
- API: http://127.0.0.1:8000
- Swagger: http://127.0.0.1:8000/docs

## 2. Run tests

```bash
uv run pytest
```

Tests do not require a live LLM because the agent's LLM client is mocked.

## 3. Run the full stack

```bash
docker compose up --build
```

Then open http://127.0.0.1:8000/docs.

## 4. Try the API

POST `/agent/run`

```json
{
  "message": "Calculate 25 * 40",
  "session_id": "class-demo-1"
}
```

POST `/memory/{session_id}`

```json
{
  "role": "user",
  "content": "My favorite language is Python."
}
```

POST `/rag/ingest`

```json
{
  "title": "Agent Notes",
  "content": "An AI agent can observe, reason, plan and act using tools."
}
```

POST `/rag/search`

```json
{
  "query": "What can an AI agent do?",
  "top_k": 3
}
```

## Teaching sequence

1. `app/agent/loop.py` — agent loop
2. `app/tools/calculator.py` — deterministic tool
3. `app/tools/search.py` — external HTTP-style tool
4. `app/memory.py` — short-term + PostgreSQL memory
5. `app/rag.py` — document storage and simple retrieval
6. `app/llm.py` — LLM adapter
7. `app/main.py` — FastAPI
8. `tests/` — automated testing

## Safety note

The search tool is deliberately a simple demo tool. Do not expose arbitrary URL fetching or shell/database write tools to an untrusted model without authentication, authorization, validation, rate limits, and human approval where appropriate.
