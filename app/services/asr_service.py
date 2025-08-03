from ..models.asr import ASRModel
from ..config import config

class ASRService:
    def __init__(self, model: ASRModel = None):
        if model is None:
            # Use configured default Amharic model
            model = ASRModel()
        self.model = model

    async def transcribe(self, file):
        return await self.model.transcribe(file)

    async def transcribe_bytes(self, data: bytes) -> str:
        return await self.model.transcribe_bytes(data)


# Initialize with Amharic-optimized model
asr_model = ASRModel()
asr_service = ASRService(asr_model)
