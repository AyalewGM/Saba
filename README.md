# saba

saba is an Amharic speech and text application providing speech-to-text and text-to-speech services.

## Development Setup

1. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the development server:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /healthcheck` – check application status.
- `POST /transcribe` – upload an audio file (`multipart/form-data`) and receive a transcript.
- `POST /synthesize` – submit text and receive synthesized speech in WAV format.
