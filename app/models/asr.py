from tempfile import NamedTemporaryFile

from transformers import pipeline

from ..config import config

class ASRModel:
    def __init__(self, model: str = None, language: str = "am"):
        """Initialize the speech recognition pipeline.

        Parameters
        ----------
        model:
            HuggingFace model name or path to a local checkpoint.
            If None, uses the default model from config.
        language:
            Language code for the ASR model (default: "am" for Amharic).
        """
        if model is None:
            model_config = config.asr_models[config.default_asr_model]
            model = model_config.path
            
        self.language = language
        self.model_name = model
        
        # Initialize the pipeline with language settings for Amharic
        pipeline_kwargs = {"model": model}
        
        # For Whisper models, we can specify the language
        if "whisper" in model.lower():
            # Whisper supports forced language decoding
            self.pipe = pipeline(
                "automatic-speech-recognition", 
                model=model,
                generate_kwargs={"language": "amharic", "task": "transcribe"}
            )
        else:
            self.pipe = pipeline("automatic-speech-recognition", **pipeline_kwargs)

    async def transcribe(self, file):
        """Transcribe an uploaded audio file."""
        with NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            
            # For Amharic, we might want to preprocess or post-process
            result = self.pipe(tmp.name)
            text = result.get("text", "")
            
            # Post-process for Amharic if needed
            return self._post_process_amharic_text(text)

    async def transcribe_bytes(self, data: bytes) -> str:
        """Transcribe raw audio bytes."""
        with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(data)
            tmp.flush()
            
            result = self.pipe(tmp.name)
            text = result.get("text", "")
            
            # Post-process for Amharic if needed
            return self._post_process_amharic_text(text)
            
    def _post_process_amharic_text(self, text: str) -> str:
        """Post-process transcribed text for better Amharic handling."""
        if not text:
            return text
            
        # Basic cleanup and normalization for Amharic text
        text = text.strip()
        
        # Remove common transcription artifacts
        text = text.replace("  ", " ")  # Multiple spaces
        
        # Handle common Amharic transcription issues
        # (These would be refined based on actual model performance)
        replacements = {
            # Common mistranscriptions that might occur
            "saba": "ሳባ",
            "ethiopia": "ኢትዮጵያ",
            "amharic": "አማርኛ",
        }
        
        text_lower = text.lower()
        for eng, amh in replacements.items():
            if eng in text_lower:
                # Only replace if the text seems to be mixed language
                text = text.replace(eng, amh)
                
        return text
