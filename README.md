# Saba: Speech-to-Text and Text-to-Speech Platform for Amharic

**Saba** is an open-source project focused on building a natural voice assistant that understands and speaks **Amharic**. Inspired by platforms like Amazon Alexa and Google Assistant, Saba aims to bridge the gap for Amharic speakers by providing an intuitive, AI-powered voice interface in their native language.

---

## Vision
To enable Amharic speakers to interact with technology through speech recognition and synthesis, fostering digital inclusivity and accessibility.

---

## Features
- **Speech-to-Text (STT):** Converts spoken Amharic into written text using ASR models like Whisper and wav2vec2.
- **Text-to-Speech (TTS):** Converts Amharic text into natural-sounding speech using TTS engines like Coqui and ESPnet.
- **Language-first:** Designed specifically with a focus on Amharic language and cultural context.
- **Modular Design:** Built for future expansion (e.g., calendar integration, reminders, smart home control).

---

## Tech Stack
- **Languages:** Python
- **STT Engines:** OpenAI Whisper, Facebook wav2vec2
- **TTS Engines:** Coqui TTS, ESPnet
- **Libraries & Tools:**
  - PyTorch
  - Hugging Face Transformers
  - Gradio (demo UI)
  - Flask or FastAPI (APIs)

---

## Project Status
- ✅ Speech-to-text pipeline in Amharic *(in progress)*
- ✅ Text-to-speech generation in Amharic *(in progress)*
- ⏳ Real-time voice interface *(planned)*
- ⏳ Skill integration (weather, Q&A, basic commands) *(planned)*
- ⏳ Wake-word detection and conversational flow *(planned)*

---

## Project Structure
```
Saba/
├── stt/        # Speech-to-text pipeline
├── tts/        # Text-to-speech pipeline
├── data/       # Datasets and preprocessing
├── api/        # REST or WebSocket API
├── ui/         # Gradio or Web frontend (optional)
├── models/     # Fine-tuned ASR and TTS models
└── README.md
```

---

## Development Setup
To set up the project locally:

### 1. Clone the repository
```bash
git clone https://github.com/AyalewGM/Saba.git
cd Saba
```

### 2. (Optional) Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

Proceed to run demos or start development as described in documentation.

---

## Architecture
The project follows a minimal layered structure:
- **Models:** ML wrappers in `app/models`
- **Services:** Business logic in `app/services`
- **Controllers:** FastAPI routers in `app/controllers`
- **main:** Application setup and router registration

---

## Training
You can fine-tune the ASR model with your own dataset using the provided script:
```bash
python -m app.train_asr --dataset /path/to/dataset --output ./asr_model
```
After training, load the saved model as follows:
```python
from app.models.asr import ASRModel
asr = ASRModel(model="./asr_model")
```

---

## Contributing
This project is in its early stages. Contributions are welcome, especially from:
- Developers fluent in Amharic
- Machine learning engineers
- Linguists passionate about speech technology

Please open an issue or pull request to share ideas or improvements.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
If you’re interested in collaborating or supporting this project, feel free to reach out:
- **Creator:** Ayalew Getachew Mersha
- **Email:** ayalew.mersha@gmail.com
- **GitHub:** [AyalewGM](https://github.com/AyalewGM)
- **LinkedIn:** https://www.linkedin.com/in/ayalew-mersha/

---

## Frontend Demo
A simple React-based interface is provided in `frontend/index.html`. Start the backend server and open this file in your browser. You can upload audio for transcription or enter text for speech generation. React is loaded from a CDN—no build step required.
```
