from fastapi import APIRouter, Form, HTTPException
from fastapi.responses import FileResponse

from ..services.tts_service import tts_service

router = APIRouter()

@router.post("/synthesize")
async def synthesize(text: str = Form(...), speaker: str = Form(None)):
    """Synthesize speech from text with optional speaker selection."""
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")
    
    try:
        # Use the updated service method with speaker parameter
        out_file = await tts_service.synthesize(text, speaker)
        return FileResponse(out_file, media_type="audio/wav", filename="output.wav")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {str(e)}")
