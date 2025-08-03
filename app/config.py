"""Configuration management for Saba voice assistant."""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for ML models."""
    name: str
    path: str
    language: str
    sample_rate: int = 16000


@dataclass
class SabaConfig:
    """Main configuration class for Saba."""
    
    # ASR Models - prioritizing Amharic-capable models
    asr_models: Dict[str, ModelConfig] = None
    
    # TTS Models - prioritizing Amharic-capable models  
    tts_models: Dict[str, ModelConfig] = None
    
    # Default models
    default_asr_model: str = "whisper_amharic"
    default_tts_model: str = "espnet_amharic"
    
    # Application settings
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Wake word settings
    wake_word: str = "ሳባ"  # "Saba" in Amharic
    wake_word_threshold: float = 0.5
    
    def __post_init__(self):
        if self.asr_models is None:
            self.asr_models = {
                "whisper_amharic": ModelConfig(
                    name="openai/whisper-base",  # Base model, can be fine-tuned for Amharic
                    path="openai/whisper-base",
                    language="am",  # Amharic language code
                    sample_rate=16000
                ),
                "wav2vec2_amharic": ModelConfig(
                    name="facebook/wav2vec2-base-960h",  # Can be fine-tuned for Amharic
                    path="facebook/wav2vec2-base-960h", 
                    language="am",
                    sample_rate=16000
                ),
                "whisper_multilingual": ModelConfig(
                    name="openai/whisper-small",  # Better multilingual support
                    path="openai/whisper-small",
                    language="am",
                    sample_rate=16000
                )
            }
            
        if self.tts_models is None:
            self.tts_models = {
                "espnet_amharic": ModelConfig(
                    name="espnet/amharic_tts",  # Placeholder for future Amharic TTS model
                    path="tts_models/multilingual/multi-dataset/xtts_v2",  # Multilingual model
                    language="am",
                    sample_rate=22050
                ),
                "coqui_multilingual": ModelConfig(
                    name="tts_models/multilingual/multi-dataset/xtts_v2",
                    path="tts_models/multilingual/multi-dataset/xtts_v2",
                    language="am",
                    sample_rate=22050
                ),
                "festival_amharic": ModelConfig(
                    name="festival_amharic",  # Placeholder for Festival-based Amharic TTS
                    path="models/festival_amharic",
                    language="am",
                    sample_rate=16000
                )
            }


def get_config() -> SabaConfig:
    """Get the application configuration."""
    return SabaConfig(
        host=os.getenv("SABA_HOST", "0.0.0.0"),
        port=int(os.getenv("SABA_PORT", "8000")),
        debug=os.getenv("SABA_DEBUG", "false").lower() == "true",
        default_asr_model=os.getenv("SABA_ASR_MODEL", "whisper_amharic"),
        default_tts_model=os.getenv("SABA_TTS_MODEL", "espnet_amharic"),
        wake_word=os.getenv("SABA_WAKE_WORD", "ሳባ"),
        wake_word_threshold=float(os.getenv("SABA_WAKE_THRESHOLD", "0.5"))
    )


# Global configuration instance
config = get_config()