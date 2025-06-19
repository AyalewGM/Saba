from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse

from ..services.tts_service import tts_service

router = APIRouter()

@router.post("/synthesize")
async def synthesize(text: str = Form(...)):
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")
    out_file = await tts_service.synthesize(text)
    return FileResponse(out_file, media_type="audio/wav", filename="output.wav")
