from sqlalchemy import select, or_
from app.db import SessionLocal
from app.models import Document


def ingest_document(title: str, content: str) -> int:
    with SessionLocal() as db:
        doc = Document(title=title, content=content)
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return doc.id


def search_documents(query: str, top_k: int = 3) -> list[dict]:
    """Simple teaching RAG retriever.

    This version uses PostgreSQL text matching so the project works immediately.
    It is intentionally designed so students can replace it later with
    embeddings + pgvector.
    """
    words = [w.strip().lower() for w in query.split() if len(w.strip()) > 2]

    with SessionLocal() as db:
        if not words:
            rows = db.scalars(select(Document).limit(top_k)).all()
        else:
            conditions = []
            for word in words:
                pattern = f"%{word}%"
                conditions.append(Document.content.ilike(pattern))
                conditions.append(Document.title.ilike(pattern))

            rows = db.scalars(
                select(Document).where(or_(*conditions)).limit(top_k)
            ).all()

        return [
            {"id": r.id, "title": r.title, "content": r.content}
            for r in rows
        ]
