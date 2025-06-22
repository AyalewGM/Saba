import pytest
from fastapi.testclient import TestClient

from app.main import app, asr_service, tts_service

client = TestClient(app)

class DummyASR:
    async def transcribe(self, file):
        return "dummy transcript"

    async def transcribe_bytes(self, data: bytes) -> str:
        return "chunk"

class DummyTTS:
    async def synthesize(self, text: str) -> str:
        from tempfile import NamedTemporaryFile
        with NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            tmp.write(b'DUMMY')
        return tmp.name


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_transcribe(monkeypatch, tmp_path):
    monkeypatch.setattr(asr_service, "transcribe", DummyASR().transcribe)
    audio_file = tmp_path / "sample.wav"
    audio_file.write_bytes(b"0" * 10)
    with audio_file.open("rb") as f:
        response = client.post("/transcribe", files={"file": ("sample.wav", f, "audio/wav")})
    assert response.status_code == 200
    assert response.json() == {"transcript": "dummy transcript"}


def test_synthesize(monkeypatch):
    monkeypatch.setattr(tts_service, "synthesize", DummyTTS().synthesize)
    response = client.post("/synthesize", data={"text": "hello"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/wav"


def test_transcribe_ws(monkeypatch):
    monkeypatch.setattr(asr_service, "transcribe_bytes", DummyASR().transcribe_bytes)
    with client.websocket_connect("/transcribe_ws") as websocket:
        websocket.send_bytes(b"data")
        text = websocket.receive_text()
        assert text == "chunk"
