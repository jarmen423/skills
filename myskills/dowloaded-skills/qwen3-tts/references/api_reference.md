# Qwen3-TTS API Reference

## Qwen3TTSModel

The main class for text-to-speech generation.

### Initialization

```python
from qwen_tts import Qwen3TTSModel

model = Qwen3TTSModel.from_pretrained(
    pretrained_model_name_or_path: str,
    device_map: str = "auto",
    dtype: torch.dtype = torch.bfloat16,
    attn_implementation: str = "flash_attention_2"
)
```

**Parameters:**
- `pretrained_model_name_or_path`: HuggingFace model ID or local path.
- `device_map`: Device to load model on (e.g., "cuda:0", "auto").
- `dtype`: Model data type (recommended: `torch.bfloat16` or `torch.float16` for FlashAttention).
- `attn_implementation`: Attention implementation (recommended: `flash_attention_2`).

### generate_custom_voice

Generate speech using a preset speaker.

```python
wavs, sr = model.generate_custom_voice(
    text: Union[str, List[str]],
    language: Union[str, List[str]] = "Auto",
    speaker: Union[str, List[str]],
    instruct: Optional[Union[str, List[str]]] = None,
    **kwargs
)
```

**Parameters:**
- `text`: Input text or list of texts.
- `language`: Target language (e.g., "English", "Chinese") or "Auto".
- `speaker`: Name of preset speaker (e.g., "Ryan", "Vivian").
- `instruct`: Optional style instruction text.
- `**kwargs`: Generation parameters (max_new_tokens, top_p, etc.).

**Returns:**
- `wavs`: List of numpy arrays containing audio waveforms.
- `sr`: Sample rate (int).

### generate_voice_design

Generate speech with a voice defined by a natural language description.

```python
wavs, sr = model.generate_voice_design(
    text: Union[str, List[str]],
    language: Union[str, List[str]] = "Auto",
    instruct: Union[str, List[str]],
    **kwargs
)
```

**Parameters:**
- `text`: Input text or list of texts.
- `language`: Target language.
- `instruct`: Description of the desired voice (e.g., "Young male voice, fast pace").
- `**kwargs`: Generation parameters.

### generate_voice_clone

Generate speech by cloning a voice from reference audio.

```python
wavs, sr = model.generate_voice_clone(
    text: Union[str, List[str]],
    language: Union[str, List[str]] = "Auto",
    ref_audio: Optional[Union[str, List[str], Tuple[np.ndarray, int]]] = None,
    ref_text: Optional[Union[str, List[str]]] = None,
    voice_clone_prompt: Optional[Union[Dict, List]] = None,
    x_vector_only_mode: bool = False,
    **kwargs
)
```

**Parameters:**
- `text`: Input text or list of texts.
- `language`: Target language.
- `ref_audio`: Path, URL, or (audio_array, sr) tuple for reference audio.
- `ref_text`: Transcript of the reference audio (improves quality).
- `voice_clone_prompt`: Pre-computed prompt from `create_voice_clone_prompt` (alternative to passing ref_audio/ref_text).
- `x_vector_only_mode`: If True, uses only speaker embedding (ref_text not required) but may have lower quality.
- `**kwargs`: Generation parameters.

### create_voice_clone_prompt

Pre-compute features for voice cloning to reuse across multiple generations.

```python
prompt = model.create_voice_clone_prompt(
    ref_audio: Union[str, Tuple[np.ndarray, int]],
    ref_text: Optional[str] = None,
    x_vector_only_mode: bool = False
)
```

**Returns:**
- A prompt object (dict or list) to be passed to `generate_voice_clone`.

## Qwen3TTSTokenizer

Class for encoding and decoding audio using the Qwen3-TTS tokenizer.

### Initialization

```python
from qwen_tts import Qwen3TTSTokenizer

tokenizer = Qwen3TTSTokenizer.from_pretrained(
    pretrained_model_name_or_path: str,
    device_map: str = "auto"
)
```

### encode

Encode audio into discrete codes.

```python
codes = tokenizer.encode(
    audio: Union[str, np.ndarray, List[str], List[np.ndarray]],
    sr: Optional[int] = None
)
```

**Parameters:**
- `audio`: Path, URL, or numpy array (waveform). If numpy array, `sr` must be provided.

**Returns:**
- `codes`: Object containing audio codes.

### decode

Decode codes back into audio.

```python
wavs, sr = tokenizer.decode(
    codes: Union[Dict, List[Dict], object]
)
```

**Parameters:**
- `codes`: Output from `encode` or dict/list format.

**Returns:**
- `wavs`: List of audio waveforms.
- `sr`: Sample rate.
