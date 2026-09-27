from fastapi import FastAPI, HTTPException
from app.db import init_db
from app.schemas import (
    AgentRequest,
    AgentResponse,
    DocumentIn,
    MemoryMessage,
    SearchRequest,
)
from app.agent.loop import Agent
from app.memory import Memory
from app.rag import ingest_document, search_documents


app = FastAPI(
    title="Agentic AI Starter",
    version="0.1.0",
    description="Teaching-ready FastAPI Agentic AI starter project.",
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/agent/run", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    try:
        result = Agent().run(
            session_id=request.session_id,
            message=request.message,
        )
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/memory/{session_id}")
def add_memory(session_id: str, message: MemoryMessage):
    Memory().add(session_id, message.role, message.content)
    return {"status": "stored"}


@app.get("/memory/{session_id}")
def get_memory(session_id: str):
    return {"messages": Memory().get(session_id)}


@app.post("/rag/ingest")
def rag_ingest(document: DocumentIn):
    doc_id = ingest_document(document.title, document.content)
    return {"document_id": doc_id}


@app.post("/rag/search")
def rag_search(request: SearchRequest):
    return {
        "query": request.query,
        "results": search_documents(request.query, request.top_k),
    }
