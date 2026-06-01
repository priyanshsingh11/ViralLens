from fastapi import APIRouter, HTTPException, status
from app.schemas.retrieve import RetrieveRequest, RetrieveResponse
from app.services.retrieval.retrieval_service import RetrievalService

router = APIRouter()
retrieval_service = RetrievalService()

@router.post("/retrieve", response_model=RetrieveResponse)
def retrieve_chunks(request: RetrieveRequest):
    try:
        response_data = retrieval_service.retrieve_context(
            question=request.question,
            video_ids=request.video_ids,
            top_k=request.top_k
        )
        return RetrieveResponse(**response_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during retrieval: {str(e)}"
        )
