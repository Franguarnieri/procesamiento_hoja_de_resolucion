from fastapi import FastAPI, File, HTTPException, UploadFile

from app.models import HojaDeResolucionResponse
from app.pipeline import process_image

app = FastAPI(title="Hoja de Resolución Processor")

_ALLOWED_TYPES = {"image/jpeg", "image/png", "image/tiff", "image/tif"}
_MAX_BYTES = 20 * 1024 * 1024  # 20 MB


@app.post("/process", response_model=HojaDeResolucionResponse)
async def process(file: UploadFile = File(...)) -> HojaDeResolucionResponse:
    if file.content_type not in _ALLOWED_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported image format: {file.content_type}",
        )

    raw_bytes = await file.read()

    if len(raw_bytes) > _MAX_BYTES:
        raise HTTPException(status_code=413, detail="Image too large (max 20 MB)")

    try:
        return process_image(raw_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
