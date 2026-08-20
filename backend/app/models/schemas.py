from pydantic import BaseModel, Field

class AskRequest(BaseModel):
    video_id: str = Field(..., min_length=5, max_length=30)
    question: str = Field(..., min_length=2, max_length=2000)

class Source(BaseModel):
    video_id: str
    chunk_id: int | None = None
    start: float | None = None
    duration: float | None = None

class AskResponse(BaseModel):
    answer: str
    video_id: str
    sources: list[Source]
    vector_store: str
