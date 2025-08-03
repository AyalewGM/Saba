from pathlib import Path
from tempfile import NamedTemporaryFile

from TTS.api import TTS

from ..config import config

class TTSModel:
    def __init__(self, model_name: str = None, language: str = "am"):
        """Initialize Text-to-Speech model.
        
        Parameters
        ----------
        model_name:
            TTS model name or path. If None, uses default from config.
        language:
            Language code (default: "am" for Amharic).
        """
        if model_name is None:
            model_config = config.tts_models[config.default_tts_model]
            model_name = model_config.path
            
        self.language = language
        self.model_name = model_name
        
        # Initialize TTS with Amharic-friendly settings
        try:
            self.tts = TTS(model_name)
        except Exception as e:
            # Fallback to multilingual model if Amharic-specific model fails
            print(f"Failed to load {model_name}, falling back to multilingual model: {e}")
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    async def synthesize(self, text: str, speaker: str = None) -> str:
        """Synthesize speech from text.
        
        Parameters
        ----------
        text:
            Text to synthesize (preferably in Amharic).
        speaker:
            Speaker ID or voice name (optional).
            
        Returns
        -------
        str:
            Path to the generated audio file.
        """
        # Preprocess text for better Amharic synthesis
        processed_text = self._preprocess_amharic_text(text)
        
        with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            try:
                # For multilingual models, try to specify language
                if hasattr(self.tts, 'synthesize'):
                    # Some TTS models support language specification
                    if speaker:
                        self.tts.tts_to_file(
                            text=processed_text, 
                            file_path=tmp.name,
                            speaker=speaker,
                            language=self.language
                        )
                    else:
                        self.tts.tts_to_file(
                            text=processed_text, 
                            file_path=tmp.name,
                            language=self.language
                        )
                else:
                    # Fallback for simpler TTS models
                    self.tts.tts_to_file(text=processed_text, file_path=tmp.name)
                    
            except Exception as e:
                # If language-specific synthesis fails, try without language specification
                print(f"Language-specific synthesis failed, trying default: {e}")
                self.tts.tts_to_file(text=processed_text, file_path=tmp.name)
                
        return tmp.name
        
    def _preprocess_amharic_text(self, text: str) -> str:
        """Preprocess text for better Amharic TTS."""
        if not text:
            return text
            
        # Basic preprocessing for Amharic text
        text = text.strip()
        
        # Handle mixed language text - extract Amharic parts
        # For now, just clean up common issues
        
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Handle punctuation for better speech synthesis
        text = text.replace(".", "።")  # Use Amharic period
        text = text.replace("?", "፧")  # Use Amharic question mark
        text = text.replace("!", "፤")  # Use Amharic exclamation
        
        # If text contains both Amharic and English, prioritize Amharic
        # This is a simple heuristic - in production, you'd want better language detection
        has_amharic = any(ord(char) >= 0x1200 and ord(char) <= 0x137F for char in text)
        if has_amharic:
            # Keep only Amharic parts for better synthesis
            # This is a simplified approach
            pass
            
        return text
