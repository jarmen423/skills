# Single-Speaker Fine-Tuning Guide


Fine-tuning is recommended when you need maximum stability and consistency for a specific voice. This process uses the **Base** models (`Qwen3-TTS-12Hz-1.7B/0.6B-Base`) [8].


## 1. Data Preparation
Prepare a JSONL file (`train_raw.jsonl`) where each line is a JSON object containing:
*   `audio`: Path to the target training audio (wav).
*   `text`: Transcript of the audio.
*   `ref_audio`: Path to the reference audio used for conditioning (recommended to use the *same* file for all samples to ensure stability).


**Example `train_raw.jsonl`:**
```json
{"audio": "/data/1.wav", "text": "Hello world", "ref_audio": "/data/ref.wav"}
{"audio": "/data/2.wav", "text": "Qwen TTS", "ref_audio": "/data/ref.wav"}
8, 17
2. Extract Audio Codes
Convert the raw audio into codes compatible with the 12Hz tokenizer.
python -m qwen_tts.finetuning.prepare_data \
    --input_data /path/to/train_raw.jsonl \
    --output_data /path/to/train_codes.jsonl \
    --model_name_or_path Qwen/Qwen3-TTS-12Hz-1.7B-Base
17
3. Run Fine-Tuning (SFT)
Run the Supervised Fine-Tuning script.
python -m qwen_tts.finetuning.sft_12hz \
    --train_data /path/to/train_codes.jsonl \
    --model_name_or_path Qwen/Qwen3-TTS-12Hz-1.7B-Base \
    --output_dir output/my_finetuned_model \
    --num_train_epochs 5 \
    --batch_size 4 \
    --learning_rate 1e-5
17
Checkpoints will be saved in output/my_finetuned_model.
