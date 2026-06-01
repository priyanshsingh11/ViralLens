from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    environment: str

@router.get("/health", response_model=HealthResponse)
def health_check():
    from app.core.config import settings
    return HealthResponse(status="ok", environment=settings.ENVIRONMENT)
