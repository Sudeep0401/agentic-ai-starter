from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    session_id: str = Field(default="default", max_length=100)


class AgentResponse(BaseModel):
    answer: str
    tool_calls: list[dict] = []
    iterations: int
    status: str


class MemoryMessage(BaseModel):
    role: str
    content: str = Field(min_length=1)


class DocumentIn(BaseModel):
    title: str
    content: str = Field(min_length=1)


class SearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
