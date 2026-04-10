from fastapi import FastAPI
from app.api import chat
from app.core.settings import settings

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(chat.router, prefix=settings.API_V1_STR)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
