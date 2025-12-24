import os
from fastapi import Request, HTTPException
from fastapi.responses import StreamingResponse
from app.config import AUDIO_DIR
from app.utils.range import parse_range

def file_iterator(path, start, end, chunk_size=1024 * 1024):
    with open(path, "rb") as f:
        f.seek(start)
        remaining = end - start + 1
        while remaining > 0:
            data = f.read(min(chunk_size, remaining))
            if not data:
                break
            remaining -= len(data)
            yield data

def stream_audio_file(filename: str, request: Request):
    file_path = os.path.join(AUDIO_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(404, "Audio not found")

    file_size = os.path.getsize(file_path)
    range_header = request.headers.get("range")

    start, end = parse_range(range_header, file_size)

    headers = {
        "Accept-Ranges": "bytes",
        "Content-Type": "audio/mpeg",
        "Content-Length": str(end - start + 1),
    }

    status_code = 200
    if range_header:
        headers["Content-Range"] = f"bytes {start}-{end}/{file_size}"
        status_code = 206

    return StreamingResponse(
        file_iterator(file_path, start, end),
        headers=headers,
        status_code=status_code,
    )
