from pathlib import Path
from tempfile import NamedTemporaryFile

from TTS.api import TTS

class TTSModel:
    def __init__(self, model_name: str = "tts_models/en/ljspeech/tacotron2-DDC"):
        self.tts = TTS(model_name)

    async def synthesize(self, text: str) -> str:
        with NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            self.tts.tts_to_file(text=text, file_path=tmp.name)
        return tmp.name
