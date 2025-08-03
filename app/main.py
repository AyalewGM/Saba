from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .controllers.asr_controller import router as asr_router
from .controllers.tts_controller import router as tts_router
from .controllers.voice_controller import router as voice_router
from .services.asr_service import asr_service
from .services.tts_service import tts_service
from .config import config
from .wake_word import voice_assistant

app = FastAPI(
    title="Saba - Amharic Voice Assistant",
    description="Speech-to-Text and Text-to-Speech Platform for Amharic",
    version="1.0.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthcheck")
def healthcheck():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "Saba Amharic Voice Assistant",
        "version": "1.0.0",
        "wake_word": config.wake_word,
        "asr_model": config.default_asr_model,
        "tts_model": config.default_tts_model
    }

@app.on_event("startup")
async def startup_event():
    """Initialize voice assistant on startup."""
    voice_assistant.start_listening()
    print(f"Saba voice assistant started. Wake word: {config.wake_word}")

@app.on_event("shutdown") 
async def shutdown_event():
    """Cleanup on shutdown."""
    voice_assistant.stop_listening()

# Include routers
app.include_router(asr_router, prefix="/api", tags=["Speech-to-Text"])
app.include_router(tts_router, prefix="/api", tags=["Text-to-Speech"])
app.include_router(voice_router, prefix="/api", tags=["Voice Assistant"])

# Serve static files (for frontend)
# app.mount("/static", StaticFiles(directory="frontend"), name="static")
