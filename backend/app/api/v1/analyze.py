from fastapi import APIRouter, HTTPException, status, BackgroundTasks
from app.schemas.analyze import AnalyzeRequest, AnalyzeResponse
from app.services.ingestion import VideoIngestionService
from app.core.errors import ExtractionError, InvalidUrlError

router = APIRouter()
ingestion_service = VideoIngestionService()

@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_videos(request: AnalyzeRequest, background_tasks: BackgroundTasks):
    try:
        videoA, videoB = ingestion_service.process_multiple_videos(
            youtube_url=request.youtube_url,
            instagram_url=request.instagram_url,
            background_tasks=background_tasks
        )
        return AnalyzeResponse(
            videoA=videoA,
            videoB=videoB,
            status="completed"
        )
    except InvalidUrlError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except ExtractionError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during analysis."
        )
