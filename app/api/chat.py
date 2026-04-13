from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.rag.pipeline import RAGPipeline
from app.core.dependencies import get_rag_pipeline

router = APIRouter(prefix="/chat", tags=["Legal AI"])


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    pipeline: RAGPipeline = Depends(get_rag_pipeline)
):
    try:
        response = await pipeline.answer(request.query)
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()  # In chi tiết lỗi ra Terminal để debug
        raise HTTPException(status_code=500, detail=str(e))
