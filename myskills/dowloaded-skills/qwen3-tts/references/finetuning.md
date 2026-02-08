# Fine-Tuning Qwen3-TTS

Fine-tuning allows you to adapt the Qwen3-TTS base model (1.7B or 0.6B) to a specific speaker using your own dataset.

## Prerequisites

1.  **Install dependencies**:
    ```bash
    pip install qwen-tts
    ```

2.  **Clone the repository** (needed for training scripts):
    ```bash
    git clone https://github.com/QwenLM/Qwen3-TTS.git
    cd Qwen3-TTS/finetuning
    ```

## Workflow

### 1. Prepare Data (JSONL)

Create a `train_raw.jsonl` file where each line is a JSON object with:
*   `audio`: Path to the target speaker's audio file (wav).
*   `text`: Transcript of the audio.
*   `ref_audio`: Path to a reference audio file for the speaker (ideally the same file for all samples to ensure consistency).

```jsonl
{"audio": "./data/utt0001.wav", "text": "Transcript for first file.", "ref_audio": "./data/ref.wav"}
{"audio": "./data/utt0002.wav", "text": "Transcript for second file.", "ref_audio": "./data/ref.wav"}
```

### 2. Extract Audio Codes

Run the `prepare_data.py` script to convert audio into discrete codes for training.

```bash
python prepare_data.py \
  --device cuda:0 \
  --tokenizer_model_path Qwen/Qwen3-TTS-Tokenizer-12Hz \
  --input_jsonl train_raw.jsonl \
  --output_jsonl train_with_codes.jsonl
```

### 3. Run Fine-Tuning (SFT)

Run the `sft_12hz.py` script to fine-tune the model.

```bash
python sft_12hz.py \
  --init_model_path Qwen/Qwen3-TTS-12Hz-1.7B-Base \
  --output_model_path output \
  --train_jsonl train_with_codes.jsonl \
  --batch_size 2 \
  --lr 2e-5 \
  --num_epochs 3 \
  --speaker_name my_custom_speaker
```

**Key Parameters:**
*   `--init_model_path`: Base model to start from (`1.7B-Base` or `0.6B-Base`).
*   `--output_model_path`: Directory to save checkpoints.
*   `--batch_size`: Adjust based on GPU memory.
*   `--lr`: Learning rate (default 2e-5).
*   `--num_epochs`: Number of training epochs.

### 4. Inference with Fine-Tuned Model

Load the fine-tuned checkpoint and generate speech.

```python
import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

# Load from the specific epoch checkpoint
model = Qwen3TTSModel.from_pretrained(
    "output/checkpoint-epoch-2",  # Path to checkpoint
    device_map="cuda:0",
    dtype=torch.bfloat16,
    attn_implementation="flash_attention_2",
)

# Generate using the speaker name used during training
wavs, sr = model.generate_custom_voice(
    text="This is my new custom voice speaking.",
    speaker="my_custom_speaker",  # Must match --speaker_name used in training
)
sf.write("output_finetuned.wav", wavs[0], sr)
```
