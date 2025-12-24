from fastapi import FastAPI
from app.api.audio import router as audio_router

app = FastAPI(title="Audio Streaming Server")

app.include_router(audio_router, prefix="/audio")
