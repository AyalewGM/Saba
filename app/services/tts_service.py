from ..models.tts import TTSModel

class TTSService:
    def __init__(self, model: TTSModel):
        self.model = model

    async def synthesize(self, text: str) -> str:
        return await self.model.synthesize(text)


tts_model = TTSModel()
tts_service = TTSService(tts_model)
