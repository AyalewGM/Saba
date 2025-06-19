from tempfile import NamedTemporaryFile

from transformers import pipeline

class ASRModel:
    def __init__(self, model: str = "openai/whisper-base"):
        """Initialize the speech recognition pipeline.

        Parameters
        ----------
        model:
            HuggingFace model name or path to a local checkpoint.
        """
        self.pipe = pipeline("automatic-speech-recognition", model=model)

    async def transcribe(self, file):
        with NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp.flush()
            result = self.pipe(tmp.name)
        return result.get("text", "")
