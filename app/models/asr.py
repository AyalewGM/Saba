from tempfile import NamedTemporaryFile

from transformers import pipeline

class ASRModel:
    def __init__(self, model_name: str = "openai/whisper-base"):
        self.pipe = pipeline("automatic-speech-recognition", model=model_name)

    async def transcribe(self, file):
        with NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            result = self.pipe(tmp.name)
        return result.get("text", "")
