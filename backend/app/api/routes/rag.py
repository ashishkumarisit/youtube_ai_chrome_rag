from fastapi import APIRouter, HTTPException
from app.models.schemas import AskRequest, AskResponse
from app.services.rag_service import RAGService

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])
service = RAGService()

@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        return service.ask(request.video_id, request.question)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
