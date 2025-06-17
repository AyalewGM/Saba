from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from tempfile import NamedTemporaryFile
import shutil

from .models.asr import ASRModel
from .models.tts import TTSModel

app = FastAPI(title="saba")

# Initialize models
asr_model = ASRModel()
tts_model = TTSModel()

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded")
    text = await asr_model.transcribe(file)
    return {"transcript": text}

@app.post("/synthesize")
async def synthesize(text: str = Form(...)):
    if not text:
        raise HTTPException(status_code=400, detail="Text is empty")
    out_file = await tts_model.synthesize(text)
    return FileResponse(out_file, media_type="audio/wav", filename="output.wav")
