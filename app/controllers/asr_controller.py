from fastapi import APIRouter, UploadFile, File, HTTPException

from ..services.asr_service import asr_service

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    text = await asr_service.transcribe(file)
    return {"transcript": text}
