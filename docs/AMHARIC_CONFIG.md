# Amharic Language Configuration

This document describes how Saba is configured to work with the Amharic language.

## Current Configuration

### ASR (Speech-to-Text) Models

1. **whisper_amharic** (default)
   - Base model: `openai/whisper-base`
   - Language: Amharic (`am`)
   - Features: Forced Amharic decoding, post-processing for common transcription issues

2. **wav2vec2_amharic** 
   - Base model: `facebook/wav2vec2-base-960h`
   - Can be fine-tuned for Amharic using the provided training script

3. **whisper_multilingual**
   - Base model: `openai/whisper-small`
   - Better multilingual support

### TTS (Text-to-Speech) Models

1. **espnet_amharic** (default)
   - Multilingual model with Amharic support
   - Path: `tts_models/multilingual/multi-dataset/xtts_v2`

2. **coqui_multilingual**
   - Coqui multilingual TTS model

3. **festival_amharic**
   - Placeholder for future Festival-based Amharic TTS

## Language-Specific Features

### ASR Post-Processing
- Automatic correction of common English-to-Amharic mistranscriptions
- Text normalization for Amharic script
- Mixed language handling

### TTS Pre-Processing
- Amharic punctuation conversion (`.` → `።`, `?` → `፧`)
- Language detection and prioritization
- Text cleaning for better synthesis

### Wake Word Detection
- Default wake word: "ሳባ" (Saba in Amharic)
- Supports multiple variations: "ሳባ", "saba", "ሳባን"
- Configurable confidence threshold

## Skills Framework

### Amharic Skills
1. **Greeting Skill**: Handles greetings in Amharic
2. **Weather Skill**: Weather queries (placeholder)
3. **Q&A Skill**: Basic question answering

### Skill Keywords
- Amharic question words: ማን, ምን, መቼ, የት, እንዴት, ለምን
- Weather terms: ሰማይ, ዝናብ, ፀሐይ, ንፋስ, ሙቀት, ቅዝቃዜ
- Greeting patterns: ሰላም, እንዴት ነህ, ጤና ይስጥልኝ

## Environment Variables

Configure Saba using these environment variables:

```bash
SABA_HOST=0.0.0.0
SABA_PORT=8000
SABA_DEBUG=false
SABA_ASR_MODEL=whisper_amharic
SABA_TTS_MODEL=espnet_amharic
SABA_WAKE_WORD=ሳባ
SABA_WAKE_THRESHOLD=0.5
```

## Future Improvements

1. **Custom Amharic Models**: Train dedicated ASR and TTS models on Amharic data
2. **Better Language Detection**: Improve mixed language handling
3. **Pronunciation Dictionary**: Add Amharic pronunciation rules
4. **Regional Dialects**: Support for different Amharic dialects
5. **Cultural Context**: Incorporate Ethiopian cultural context in responses