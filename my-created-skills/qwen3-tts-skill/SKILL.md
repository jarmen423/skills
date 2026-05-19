---
name: qwen3-tts
description: Build text-to-speech applications using Qwen3-TTS, a powerful speech generation system supporting voice clone, voice design, and custom voice synthesis. Use when creating TTS applications, generating speech from text, cloning voices from audio samples, designing new voices via natural language descriptions, or fine-tuning TTS models. Supports 10 languages (Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian).
---

# Qwen3-TTS

Build text-to-speech applications using Qwen3-TTS from Alibaba Qwen. Reference the local repository at `D:\code\qwen3-tts` for source code and examples.

## Quick Reference

| Task | Model | Method |
|------|-------|--------|
| Custom voice with preset speakers | CustomVoice | `generate_custom_voice()` |
| Design new voice via description | VoiceDesign | `generate_voice_design()` |
| Clone voice from audio sample | Base | `generate_voice_clone()` |
| Encode/decode audio | Tokenizer | `encode()` / `decode()` |

## Environment Setup

```bash
# Create fresh environment
conda create -n qwen3-tts python=3.12 -y
conda activate qwen3-tts

# Install package
pip install -U qwen-tts

# Optional: FlashAttention 2 for reduced GPU memory
pip install -U flash-attn --no-build-isolation
```

## Available Models

| Model | Features |
|-------|----------|
| `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | 9 preset speakers, instruction control |
| `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign` | Create voices from natural language descriptions |
| `Qwen/Qwen3-TTS-12Hz-1.7B-Base` | Voice cloning, fine-tuning base |
| `Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice` | Smaller custom voice model |
| `Qwen/Qwen3-TTS-12Hz-0.6B-Base` | Smaller base model for cloning/fine-tuning |
| `Qwen/Qwen3-TTS-Tokenizer-12Hz` | Audio encoder/decoder |

## Task Workflows

### 1. Custom Voice Generation

Use preset speakers with optional style instructions.

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# Single generation
wavs, sr = model.generate_custom_voice(
    text="Hello, how are you today?",
    language="English",  # Or "Auto" for auto-detection
    speaker="Ryan",
    instruct="Speak with enthusiasm",  # Optional style control
)
sf.write("output.wav", wavs[0], sr)

# Batch generation
wavs, sr = model.generate_custom_voice(
    text=["First sentence.", "Second sentence."],
    language=["English", "English"],
    speaker=["Ryan", "Aiden"],
    instruct=["Happy tone", "Calm tone"],
)
```

**Available Speakers:**

| Speaker | Description | Native Language |
|---------|-------------|-----------------|
| Vivian | Bright, edgy young female | Chinese |
| Serena | Warm, gentle young female | Chinese |
| Uncle_Fu | Low, mellow mature male | Chinese |
| Dylan | Youthful Beijing male | Chinese (Beijing) |
| Eric | Lively Chengdu male | Chinese (Sichuan) |
| Ryan | Dynamic male with rhythmic drive | English |
| Aiden | Sunny American male | English |
| Ono_Anna | Playful Japanese female | Japanese |
| Sohee | Warm Korean female | Korean |

### 2. Voice Design

Create new voices from natural language descriptions.

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

wavs, sr = model.generate_voice_design(
    text="Welcome to our presentation today.",
    language="English",
    instruct="Professional male voice, warm baritone, confident and clear",
)
sf.write("designed_voice.wav", wavs[0], sr)
```

### 3. Voice Cloning

Clone a voice from a reference audio sample (3+ seconds recommended).

```python
model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# Direct cloning
wavs, sr = model.generate_voice_clone(
    text="This is the cloned voice speaking.",
    language="English",
    ref_audio="path/to/reference.wav",  # Or URL or (numpy_array, sr) tuple
    ref_text="Transcript of the reference audio.",
)
sf.write("cloned.wav", wavs[0], sr)

# Reusable clone prompt (for multiple generations)
prompt = model.create_voice_clone_prompt(
    ref_audio="path/to/reference.wav",
    ref_text="Transcript of the reference audio.",
)
wavs, sr = model.generate_voice_clone(
    text="Another sentence with the same voice.",
    language="English",
    voice_clone_prompt=prompt,
)
```

### 4. Voice Design + Clone Workflow

Design a voice, then reuse it across multiple generations.

```python
# Step 1: Design the voice
design_model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

ref_text = "Sample text for the reference audio."
ref_wavs, sr = design_model.generate_voice_design(
    text=ref_text,
    language="English",
    instruct="Young energetic male, tenor range",
)

# Step 2: Create reusable clone prompt
clone_model = Qwen3TTSModel.from_pretrained(
    "Qwen/Qwen3-TTS-12Hz-1.7B-Base",
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

prompt = clone_model.create_voice_clone_prompt(
    ref_audio=(ref_wavs[0], sr),
    ref_text=ref_text,
)

# Step 3: Generate multiple outputs with consistent voice
for sentence in ["First line.", "Second line.", "Third line."]:
    wavs, sr = clone_model.generate_voice_clone(
        text=sentence,
        language="English",
        voice_clone_prompt=prompt,
    )
```

### 5. Audio Tokenization

Encode and decode audio for transport or processing.

```python
from qwen_tts import Qwen3TTSTokenizer
import soundfile as sf

tokenizer = Qwen3TTSTokenizer.from_pretrained(
    "Qwen/Qwen3-TTS-Tokenizer-12Hz",
    device_map="cuda:0",
)

# Encode audio (accepts path, URL, numpy array, or base64)
enc = tokenizer.encode("path/to/audio.wav")

# Decode back to waveform
wavs, sr = tokenizer.decode(enc)
sf.write("reconstructed.wav", wavs[0], sr)
```

## Generation Parameters

Common parameters for all `generate_*` methods:

```python
wavs, sr = model.generate_custom_voice(
    text="...",
    language="Auto",
    speaker="Ryan",
    max_new_tokens=2048,
    do_sample=True,
    top_k=50,
    top_p=1.0,
    temperature=0.9,
    repetition_penalty=1.05,
)
```

## Web UI Demo

Launch local Gradio demo:

```bash
# CustomVoice demo
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --ip 0.0.0.0 --port 8000

# VoiceDesign demo
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign --ip 0.0.0.0 --port 8000

# Base (voice clone) demo - requires HTTPS for microphone
qwen-tts-demo Qwen/Qwen3-TTS-12Hz-1.7B-Base --ip 0.0.0.0 --port 8000 \
  --ssl-certfile cert.pem --ssl-keyfile key.pem --no-ssl-verify
```

## Supported Languages

Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian

Pass `language="Auto"` for automatic detection, or specify explicitly for best quality.

## References

- **Fine-tuning guide**: See [references/finetuning.md](references/finetuning.md) for training custom speakers
- **API details**: See [references/api-reference.md](references/api-reference.md) for complete method signatures
- **Local repo**: `D:\code\qwen3-tts` contains source code and examples
