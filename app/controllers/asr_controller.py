from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect

from ..services.asr_service import asr_service

router = APIRouter()

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    text = await asr_service.transcribe(file)
    return {"transcript": text}


@router.websocket("/transcribe_ws")
async def transcribe_ws(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_bytes()
            text = await asr_service.transcribe_bytes(data)
            await ws.send_text(text)
    except WebSocketDisconnect:
        pass
