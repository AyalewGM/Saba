# Saba: Speech-to-Text and Text-to-Speech Platform for Amharic

**Saba** is an open-source project focused on building a natural voice assistant that understands and speaks **Amharic**. Inspired by platforms like Amazon Alexa and Google Assistant, Saba aims to bridge the gap in voice technology for underrepresented languages—starting with Amharic.

---

## Vision

Our goal is to create an intuitive, AI-powered voice interface in Amharic, enabling users to interact with technology using their native language through speech recognition and synthesis.

---

## Features

- **Speech-to-Text (STT)**: Converts spoken Amharic into written text using ASR models such as Whisper and wav2vec2.
- **Text-to-Speech (TTS)**: Converts Amharic text into natural-sounding speech using TTS engines like Coqui and ESPnet.
- **Language-first**: Designed specifically with a focus on the Amharic language and cultural context.
- **Modular Design**: Built for future expansion into skills such as calendar integration, reminders, or smart home control.

---

## Tech Stack

- **Languages**: Python
- **STT Engines**: OpenAI Whisper, Facebook wav2vec2
- **TTS Engines**: Coqui TTS, ESPnet
- **Libraries & Tools**:
  - PyTorch
  - Hugging Face Transformers
  - Gradio (for demo UI)
  - Flask or FastAPI (for APIs)

---

## Current Status

- ✅ Speech-to-text pipeline in Amharic *(in progress)*
- ✅ Text-to-speech generation in Amharic *(in progress)*
- ⏳ Real-time voice interface *(planned)*
- ⏳ Skill integration (weather, Q&A, basic commands) *(planned)*
- ⏳ Wake-word detection and conversational flow *(planned)*

---

## 📁 Project Structure (Tentative)

```
Saba/
├── stt/        # Speech-to-text pipeline
├── tts/        # Text-to-speech pipeline
├── data/       # Datasets and preprocessing
├── api/        # REST or WebSocket API
├── ui/         # Optional Gradio or Web frontend
├── models/     # Fine-tuned ASR and TTS models
└── README.md
```

---

## 🚀 Development Setup

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

Run a demo or start development as described in the documentation.

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

If you’re interested in collaborating or supporting this project, feel free to reach out.

**Creator**: Ayalew Getachew Mersha  
GitHub: [AyalewGM](https://github.com/AyalewGM)Saba
Speech-to-Text and Text-to-Speech Platform for Amharic
