from ..models.tts import TTSModel
from ..config import config

class TTSService:
    def __init__(self, model: TTSModel = None):
        if model is None:
            # Use configured default Amharic model
            model = TTSModel()
        self.model = model

    async def synthesize(self, text: str, speaker: str = None) -> str:
        return await self.model.synthesize(text, speaker)


# Initialize with Amharic-optimized model
tts_model = TTSModel()
tts_service = TTSService(tts_model)
