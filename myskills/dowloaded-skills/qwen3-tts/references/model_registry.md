# Qwen3-TTS Model Registry


Qwen3-TTS models are generally available in 0.6B and 1.7B parameter sizes. The 12Hz tokenizer variants are the primary release for general usage [5].


## Released Models (12Hz Series)


| Model Name | Primary Use Case | Features |
| :--- | :--- | :--- |
| **Qwen3-TTS-12Hz-1.7B-Base** | **Voice Cloning** & **Fine-Tuning** | Supports 3-second rapid cloning from audio; used as the base for SFT (Supervised Fine-Tuning). |
| **Qwen3-TTS-12Hz-0.6B-Base** | **Voice Cloning** & **Fine-Tuning** | Lightweight version of the Base model. Lower latency (93ms start time) [12]. |
| **Qwen3-TTS-12Hz-1.7B-CustomVoice** | **Controllable TTS** (Presets) | Supports 9 premium timbres. Allows style/emotion control via instructions (e.g., "Speak warmly"). |
| **Qwen3-TTS-12Hz-0.6B-CustomVoice** | **Controllable TTS** (Presets) | Lightweight version of CustomVoice. |
| **Qwen3-TTS-12Hz-1.7B-VoiceDesign** | **Voice Creation** | Generates speech from a text description of a voice (e.g., "An epic movie trailer voice"). |


## Supported Languages
All models support: Chinese, English, Japanese, Korean, German, French, Russian, Portuguese, Spanish, Italian [5].


## Preset Speakers (CustomVoice Models)
These models do not support arbitrary cloning but offer high controllability over these specific identities [13]:


*   **Chinese**: Vivian (Young Female), Serena (Gentle Female), Uncle_Fu (Seasoned Male), Dylan (Beijing Male), Eric (Chengdu Male).
*   **English**: Ryan (Dynamic Male), Aiden (Sunny American Male).
*   **Japanese**: Ono_Anna (Playful Female).
*   **Korean**: Sohee (Warm Female).
