# ElevenLabs Integration Skill

## Overview
This skill provides instructions and reference for integrating ElevenLabs AI voice technology, including:
- Text-to-Speech generation with v3 audio tags
- Voice cloning from audio/video files or URLs
- Audio isolation for cleaning noisy uploads

## Audio Tags (v3)

ElevenLabs v3 models support audio tags in square brackets that control emotional delivery:

### Emotional Directions
- `[happy]`, `[sad]`, `[excited]`, `[angry]`
- `[whisper]`, `[annoyed]`, `[appalled]`
- `[thoughtful]`, `[surprised]`, `[nervous]`
- `[sarcastic]`, `[dramatic]`, `[calm]`

### Non-Verbal Sounds
- `[laughing]`, `[chuckles]`, `[sighs]`
- `[clears throat]`, `[short pause]`, `[long pause]`
- `[exhales sharply]`, `[inhales deeply]`
- `[muttering]`, `[yawning]`

### Usage Examples
```
[excited] Hello everyone, welcome to the stream!
I can't believe you did that! [laughing]
[whisper] Don't tell anyone, but... [pause] I have a secret.
[nervous][whisper] I'm not sure about this...
```

### Best Practices
1. **Tag Combinations**: Combine multiple tags for complex delivery
2. **Voice Matching**: Match tags to voice character (serious voices may not respond to playful tags)
3. **Text Structure**: Use natural speech patterns and proper punctuation
4. **Experimentation**: Infer new tags beyond the standard list

## API Endpoints

### Text-to-Speech
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
```

### Voice Cloning
```
POST https://api.elevenlabs.io/v1/voices/add
```

### Audio Isolation
```
POST https://api.elevenlabs.io/v1/audio-isolation
```
Removes background noise from audio files. Use before voice cloning for better results.

## Models

| Model ID | Description |
|----------|-------------|
| `eleven_turbo_v2_5` | Fast, supports audio tags |
| `eleven_multilingual_v2` | Multi-language support |
| `eleven_monolingual_v1` | Legacy English only |
