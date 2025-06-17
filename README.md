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

## Frontend Usage

A simple React-based interface is provided in `frontend/index.html`. Start the
backend server and open this file in your browser. The page allows you to upload
an audio file for transcription or enter text to generate speech without any
build step because React is loaded from a CDN.
