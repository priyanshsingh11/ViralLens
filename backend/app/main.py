from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import health, analyze, chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include Routers
app.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])
app.include_router(analyze.router, prefix=settings.API_V1_STR, tags=["Analyze"])
app.include_router(chat.router, prefix=settings.API_V1_STR, tags=["Chat"])

@app.get("/")
def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}
