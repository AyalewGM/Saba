# saba

Saba is an Amharic speech and text application providing speech-to-text and text-to-speech services.

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

## Architecture

The project follows a minimal layered structure:

- **Models** – wrappers around ML models in `app/models`.
- **Services** – business logic in `app/services`.
- **Controllers** – FastAPI routers located in `app/controllers`.
- **main** – application setup that registers routers.

## Training

You can fine-tune the ASR model on your own dataset using the provided
`app/train_asr.py` script. The dataset must contain `audio` and `text` columns.

Install the optional training dependencies and run:

```bash
python -m app.train_asr --dataset /path/to/dataset --output ./asr_model
```

After training, load the saved model by passing the output directory to
`ASRModel`:

```python
from app.models.asr import ASRModel
asr = ASRModel(model="./asr_model")
```
