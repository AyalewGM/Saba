from ..models.asr import ASRModel

class ASRService:
    def __init__(self, model: ASRModel):
        self.model = model

    async def transcribe(self, file):
        return await self.model.transcribe(file)

    async def transcribe_bytes(self, data: bytes) -> str:
        return await self.model.transcribe_bytes(data)


asr_model = ASRModel()
asr_service = ASRService(asr_model)
