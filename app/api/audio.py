from fastapi import APIRouter, Request, HTTPException
from app.services.stream_service import stream_audio_file

router = APIRouter()

@router.get("/{filename}")
async def audio(filename: str, request: Request):
    return stream_audio_file(filename, request)
