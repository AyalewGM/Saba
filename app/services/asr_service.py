from ..models.asr import ASRModel

class ASRService:
    def __init__(self, model: ASRModel):
        self.model = model

    async def transcribe(self, file):
        return await self.model.transcribe(file)


asr_model = ASRModel()
asr_service = ASRService(asr_model)
