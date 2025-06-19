from fastapi import FastAPI

from .controllers.asr_controller import router as asr_router
from .controllers.tts_controller import router as tts_router
from .services.asr_service import asr_service
from .services.tts_service import tts_service

app = FastAPI(title="saba")

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(asr_router)
app.include_router(tts_router)
