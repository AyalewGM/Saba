# Saba Usage Guide

This guide explains how to use the enhanced Saba Amharic Voice Assistant.

## Quick Start

### 1. Installation

```bash
git clone https://github.com/AyalewGM/Saba.git
cd Saba
pip install -r requirements.txt
```

### 2. Running the Application

```bash
# Start the backend server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Open frontend/index.html in your browser
# Or visit http://localhost:8000/static/index.html
```

## Features

### Voice Assistant Chat

The new voice assistant provides conversational AI in Amharic:

1. **Wake Word Detection**: Say "ሳባ" (Saba) to start a conversation
2. **Multi-turn Conversations**: Maintain context across multiple exchanges
3. **Skill-based Responses**: Specialized handlers for different types of queries

#### Example Conversations:

```
User: ሳባ
Saba: ሰላም! እንዴት ልረዳሽ? (Hello! How can I help you?)

User: ማን ነህ?
Saba: ሳባ እኔ ነኝ፣ የአማርኛ ድምጽ ረዳት። (I am Saba, an Amharic voice assistant.)

User: ሰማይ ምን ይመስላል?
Saba: ይቅርታ፣ የሰማይ ሁኔታ አገልግሎት አሁንም እየተገነባ ነው። (Sorry, weather service is still under development.)
```

### Available Skills

#### 1. Greeting Skill
- **Triggers**: ሰላም, hello, hi, እንዴት ነህ, ጤና ይስጥልኝ
- **Function**: Responds to greetings in Amharic
- **Example**: "ሰላም" → "ሰላም! እንዴት ነህ? ሳባ እኔ ነኝ..."

#### 2. Question Answering Skill  
- **Triggers**: ማን, ምን, መቼ, የት, እንዴት, ለምን, who, what, when, where, how, why
- **Function**: Answers basic questions about Saba
- **Example**: "ማን ነህ?" → "ሳባ እኔ ነኝ፣ የአማርኛ ድምጽ ረዳት።"

#### 3. Weather Skill (Placeholder)
- **Triggers**: ሰማይ, ዝናብ, ፀሐይ, ንፋስ, weather, rain, sun, wind
- **Function**: Weather queries (currently returns placeholder response)
- **Example**: "ሰማይ" → "ይቅርታ፣ የሰማይ ሁኔታ አገልግሎት አሁንም እየተገነባ ነው።"

## API Endpoints

### Voice Assistant Endpoints

- `POST /api/voice/chat` - Text-based chat
- `POST /api/voice/chat/audio` - Audio-based chat
- `POST /api/voice/wake` - Manually trigger wake word
- `POST /api/voice/end` - End conversation
- `GET /api/voice/status` - Get assistant status
- `GET /api/voice/config` - Get configuration

### Traditional STT/TTS Endpoints

- `POST /api/transcribe` - Transcribe audio file
- `POST /api/synthesize` - Generate speech from text
- `WebSocket /api/transcribe_ws` - Real-time transcription

## Configuration

### Environment Variables

```bash
export SABA_HOST=0.0.0.0
export SABA_PORT=8000
export SABA_DEBUG=false
export SABA_ASR_MODEL=whisper_amharic
export SABA_TTS_MODEL=espnet_amharic
export SABA_WAKE_WORD=ሳባ
export SABA_WAKE_THRESHOLD=0.5
```

### Available Models

#### ASR Models:
- `whisper_amharic` (default) - OpenAI Whisper with Amharic settings
- `wav2vec2_amharic` - Facebook wav2vec2 for Amharic
- `whisper_multilingual` - Whisper small with better multilingual support

#### TTS Models:
- `espnet_amharic` (default) - Multilingual TTS with Amharic support
- `coqui_multilingual` - Coqui multilingual TTS
- `festival_amharic` - Placeholder for Festival Amharic TTS

## Frontend Usage

### Voice Assistant Interface

1. **Chat Section**: Type messages or use the voice interface
2. **Wake Word Button**: Manually trigger conversation start
3. **Status Indicator**: Shows listening/conversation state
4. **Skills Display**: Lists available voice assistant skills

### Traditional Interface

1. **Speech-to-Text**: Upload audio files or use live recording
2. **Text-to-Speech**: Enter text (Amharic or English) for synthesis
3. **Download**: Save transcriptions as text files

## Development

### Adding New Skills

```python
from app.skills import Skill, SkillResponse

class MySkill(Skill):
    def __init__(self):
        super().__init__("my_skill")
        
    def can_handle(self, text: str, context: dict) -> bool:
        return "my_keyword" in text.lower()
        
    async def handle(self, text: str, context: dict) -> SkillResponse:
        return SkillResponse(
            text="My response in Amharic and English",
            speech="ለTTS የሚሰጠው ጽሑፍ"
        )
        
    @property
    def description(self) -> str:
        return "Description of my skill"

# Register the skill
from app.skills import skill_manager
skill_manager.register_skill(MySkill())
```

### Training Custom Models

Use the provided training script to fine-tune models on Amharic data:

```bash
python -m app.train_asr --dataset /path/to/amharic_dataset --output ./custom_amharic_model
```

## Troubleshooting

### Common Issues

1. **Wake word not detected**: Check microphone permissions and threshold settings
2. **Poor transcription quality**: Try different ASR models or adjust audio quality
3. **TTS not working**: Verify TTS model installation and language settings
4. **Skills not responding**: Check skill keywords and language detection

### Debugging

Run the test script to validate functionality:

```bash
python test_functionality.py
```

Check logs for detailed error messages when running the server.

## Future Enhancements

1. **Custom Amharic ASR/TTS Models**: Train models specifically on Amharic data
2. **Regional Dialect Support**: Handle different Amharic dialects
3. **External API Integration**: Weather, news, calendar services
4. **Improved NLU**: Better intent recognition and entity extraction
5. **Mobile App**: Native mobile applications for iOS/Android

## Contributing

See the main README for contribution guidelines. When adding Amharic-specific features:

1. Test with Amharic text inputs
2. Consider cultural context in responses
3. Use appropriate Amharic fonts and encoding
4. Validate with native Amharic speakers