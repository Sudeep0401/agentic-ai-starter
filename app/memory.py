from sqlalchemy import select
from app.db import SessionLocal
from app.models import ConversationMessage


class Memory:
    """Short-term conversation state backed by PostgreSQL."""

    def add(self, session_id: str, role: str, content: str) -> None:
        with SessionLocal() as db:
            db.add(
                ConversationMessage(
                    session_id=session_id,
                    role=role,
                    content=content,
                )
            )
            db.commit()

    def get(self, session_id: str, limit: int = 20) -> list[dict]:
        with SessionLocal() as db:
            rows = db.scalars(
                select(ConversationMessage)
                .where(ConversationMessage.session_id == session_id)
                .order_by(ConversationMessage.created_at.desc())
                .limit(limit)
            ).all()

        rows.reverse()
        return [{"role": r.role, "content": r.content} for r in rows]
