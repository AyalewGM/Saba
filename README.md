# Saba

Speech-to-Text and Text-to-Speech Platform for Amharic

Saba is an open-source project focused on building a natural voice assistant that understands and speaks Amharic. Inspired by platforms like Amazon Alexa and Google Assistant, Saba aims to bridge the gap in voice technology for underrepresented languages—starting with Amharic.

## 🌍 Vision

To create an intuitive, AI-powered voice interface in Amharic, enabling users to interact with technology using their native language—through speech recognition and synthesis.

## 🚀 Features

- 🎙️ **Speech-to-Text (STT)** – Converts spoken Amharic into written text using ASR models like Whisper and wav2vec2.
- 🔊 **Text-to-Speech (TTS)** – Converts Amharic text into natural-sounding speech using TTS engines like Coqui and ESPnet.
- 🌐 **Language-first** – Built with a strong focus on the Amharic language and cultural context.
- 📦 **Modular design** for future expansion into skills like calendar integration, reminders, or smart home control.

## 📚 Tech Stack

- **Languages:** Python
- **STT Engines:** OpenAI Whisper, Facebook wav2vec2
- **TTS Engines:** Coqui TTS, ESPnet
- **Tools & Libraries:** PyTorch, Hugging Face Transformers, Gradio (for demo UI), Flask/FastAPI (for APIs)

## 🔧 Current Status

We are currently building and fine-tuning the following components:

- Speech-to-text pipeline in Amharic
- Text-to-speech generation in Amharic
- Real-time voice interface
- Skill integration (weather, questions, basic commands)
- Wake-word detection and conversational flow

## 📂 Project Structure (tentative)

```
Saba/
├── stt/               # Speech-to-text pipeline
├── tts/               # Text-to-speech pipeline
├── data/              # Datasets and preprocessing
├── api/               # REST or WebSocket API
├── ui/                # Optional Gradio or Web frontend
├── models/            # Fine-tuned ASR and TTS models
└── README.md
```

## 👤 Contributing

This project is in its early stages. Contributions are welcome—especially from developers fluent in Amharic, ML engineers, and linguists passionate about speech tech.

## 📩 Contact

Feel free to reach out if you'd like to collaborate or support the mission.

Creator: Ayalew Getachew Mersha  
Email: [your-email@example.com]  
LinkedIn: [Your LinkedIn] (optional)

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
