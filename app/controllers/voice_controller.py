"""Voice assistant controller for conversational interactions."""

from fastapi import APIRouter, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from typing import Optional

from ..wake_word import voice_assistant
from ..skills import skill_manager
from ..services.asr_service import asr_service
from ..services.tts_service import tts_service
from ..config import config

router = APIRouter()


@router.post("/voice/chat")
async def voice_chat(text: str = Form(...)):
    """Handle voice chat input (text-based for now)."""
    try:
        # Process through voice assistant core
        response_text = await voice_assistant.process_voice_input(text)
        
        if response_text is None:
            # No response (wake word not detected, etc.)
            return JSONResponse({
                "status": "listening",
                "message": "Waiting for wake word..."
            })
        
        return JSONResponse({
            "status": "success",
            "response": response_text,
            "conversation_active": voice_assistant.conversation.is_active
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice input: {str(e)}")


@router.post("/voice/chat/audio")
async def voice_chat_audio(file: UploadFile = File(...)):
    """Handle voice chat with audio input."""
    try:
        # First transcribe the audio
        transcript = await asr_service.transcribe(file)
        
        if not transcript.strip():
            return JSONResponse({
                "status": "error",
                "message": "Could not transcribe audio"
            })
        
        # Process through voice assistant
        response_text = await voice_assistant.process_voice_input(transcript)
        
        if response_text is None:
            return JSONResponse({
                "status": "listening", 
                "transcript": transcript,
                "message": "Waiting for wake word..."
            })
            
        # Generate speech response
        audio_file = await tts_service.synthesize(response_text)
        
        return JSONResponse({
            "status": "success",
            "transcript": transcript,
            "response": response_text,
            "audio_url": f"/audio/{audio_file.split('/')[-1]}",
            "conversation_active": voice_assistant.conversation.is_active
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing voice audio: {str(e)}")


@router.post("/voice/wake")
async def trigger_wake_word():
    """Manually trigger wake word detection (for testing)."""
    try:
        voice_assistant.conversation.start_conversation()
        return JSONResponse({
            "status": "success",
            "message": "Wake word triggered, conversation started"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering wake word: {str(e)}")


@router.post("/voice/end")
async def end_conversation():
    """End the current conversation."""
    try:
        voice_assistant.conversation.end_conversation()
        return JSONResponse({
            "status": "success",
            "message": "Conversation ended"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error ending conversation: {str(e)}")


@router.get("/voice/status")
async def get_voice_status():
    """Get current voice assistant status."""
    return JSONResponse({
        "wake_word": config.wake_word,
        "is_listening": voice_assistant.wake_detector.is_listening,
        "conversation_active": voice_assistant.conversation.is_active,
        "session_id": voice_assistant.conversation.session_id,
        "available_skills": skill_manager.list_skills()
    })


@router.get("/voice/config")
async def get_voice_config():
    """Get voice assistant configuration."""
    return JSONResponse({
        "asr_models": {name: {
            "name": model.name,
            "language": model.language,
            "sample_rate": model.sample_rate
        } for name, model in config.asr_models.items()},
        "tts_models": {name: {
            "name": model.name, 
            "language": model.language,
            "sample_rate": model.sample_rate
        } for name, model in config.tts_models.items()},
        "default_asr": config.default_asr_model,
        "default_tts": config.default_tts_model,
        "wake_word": config.wake_word,
        "wake_threshold": config.wake_word_threshold
    })


@router.post("/voice/skills/{skill_name}")
async def test_skill(skill_name: str, text: str = Form(...)):
    """Test a specific skill directly."""
    try:
        # Find the skill
        skill = None
        for s in skill_manager.skills:
            if s.name == skill_name:
                skill = s
                break
                
        if not skill:
            raise HTTPException(status_code=404, detail=f"Skill '{skill_name}' not found")
            
        # Test if skill can handle the input
        if not skill.can_handle(text, {}):
            return JSONResponse({
                "status": "not_handled",
                "message": f"Skill '{skill_name}' cannot handle this input"
            })
            
        # Process with the skill
        response = await skill.handle(text, {})
        
        return JSONResponse({
            "status": "success",
            "skill": skill_name,
            "input": text,
            "response": response.text,
            "speech": response.speech,
            "end_conversation": response.end_conversation
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error testing skill: {str(e)}")