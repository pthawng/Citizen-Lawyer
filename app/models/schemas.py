from datetime import date
from pydantic import BaseModel, Field


class ArticleMetadata(BaseModel):
    article_id: str = Field(..., description="e.g., Điều 12")
    law_name: str = Field(..., description="e.g., Bộ luật Dân sự")
    year: int = Field(..., description="Year of issuance")
    effective_date: date | None = None
    expiry_date: date | None = None
    legal_hierarchy: int = Field(
        1, description="Priority level: 1 (highest) to N"
    )


class ArticleChunk(BaseModel):
    content: str
    metadata: ArticleMetadata
    score: float | None = None


class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1)
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    citations: list[str]
    trace_id: str | None = None
