# Inference Workflows with `qwen-tts`


First, ensure the environment is set up:
```bash
pip install qwen-tts
# Optional: FlashAttention 2 for performance
14, 15
1. Custom Voice Generation (Standard TTS)
Use this for applications requiring specific emotions or styles using the preset speakers.
from qwen_tts.model import Qwen3TTSModel


# Load the CustomVoice model
model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice")


# Generate speech with instruction
output = model.generate_custom_voice(
    text="Welcome to the future of speech synthesis.",
    language="English",
    speaker="Aiden",  # Select from supported speakers
    instruct="Speak with a warm and encouraging voice." # Natural language instruction
)
13, 16
2. Voice Cloning (Zero-Shot)
Use the Base model to clone a voice from a reference audio file.
from qwen_tts.model import Qwen3TTSModel


model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base")


# Clone from a local file
output = model.generate_voice_clone(
    text="I am now speaking with your voice.",
    ref_audio="path/to/reference_audio.wav",
    ref_text="The transcript of the reference audio." # Optional but recommended for quality
)
Tip for Reusability:To avoid re-processing the reference audio for every request, create a prompt first:
# Create a reusable prompt
clone_prompt = model.create_voice_clone_prompt(
    ref_audio="path/to/ref.wav", 
    ref_text="Transcript here"
)


# Use the prompt for generation
output = model.generate_voice_clone(
    text="New text to speak.",
    voice_clone_prompt=clone_prompt
)
3, 6
3. "Voice Design then Clone" Workflow
This pattern allows you to "invent" a character voice using text descriptions and then use it consistently.
Design: Use the VoiceDesign model to generate a sample.
Clone: Use the generated sample as ref_audio for the Base model.
# 1. Design the voice
design_model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign")
design_output = design_model.generate_voice_design(
    text="This is the voice you requested.",
    instruct="An epic and trustworthy voice for a documentary trailer."
)
# Save design_output['audio'] to file or memory


# 2. Clone the designed voice (Load Base model)
base_model = Qwen3TTSModel.from_pretrained("Qwen/Qwen3-TTS-12Hz-1.7B-Base")
output = base_model.generate_voice_clone(
    text="Now I can read the full script with this epic voice.",
    ref_audio=design_output['audio'], # Use the designed audio as reference
    ref_text="This is the voice you requested."
)
6
