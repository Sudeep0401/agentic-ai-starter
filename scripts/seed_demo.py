from app.db import init_db
from app.rag import ingest_document

init_db()

docs = [
    (
        "Agent Basics",
        "An AI agent can observe context, reason about a goal, use tools, "
        "update state, and act iteratively."
    ),
    (
        "Agent Memory",
        "Short-term memory keeps recent conversation state. Long-term memory "
        "stores information that can be retrieved later."
    ),
    (
        "Agentic RAG",
        "Agentic RAG allows an agent to decide when retrieval is needed, "
        "generate a query, retrieve knowledge, evaluate the result, and "
        "retrieve again when necessary."
    ),
]

for title, content in docs:
    print("Inserted:", ingest_document(title, content))
