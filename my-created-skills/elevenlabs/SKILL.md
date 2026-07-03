# ElevenLabs Integration Skill

## Overview
This skill covers ElevenLabs text-to-speech with **v3 audio tags**, voice cloning, and multi-provider context for the TTS Voice Studio. ElevenLabs v3 uses `[square bracket]` audio tags — NOT SSML-style angle brackets. v3 does NOT support `<break>`, `<emphasis>`, or any XML/SSML tags. Use ellipses (...) for pauses.

Also includes reference tables for **Fish Audio S2/S2.1-Pro** and **xAI Grok Voice** tag syntax, since TTS Voice Studio supports all three natively.

## Audio Tags (ElevenLabs v3)

v3 supports `[bracket]` tags for emotion, delivery, and sound effects. Place them before, after, or inline.

### Emotional Directions
`[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[whispers]`, `[annoyed]`, `[appalled]`, `[thoughtful]`, `[surprised]`, `[nervous]`, `[nervously]`, `[sarcastic]`, `[curious]`, `[mischievously]`, `[professional]`, `[sympathetic]`, `[reassuring]`, `[questioning]`, `[frustrated]`, `[deadpan]`, `[calm]`, `[delighted]`, `[alarmed]`, `[dramatic]`, `[dismissive]`, `[impressed]`, `[warmly]`, `[cheerfully]`, `[quizzically]`, `[elated]`, `[cautiously]`, `[sheepishly]`, `[desperately]`, `[panicking]`, `[cracking up]`, `[stifling laughter]`, `[with genuine belly laugh]`, `[robotic voice]`, `[singing]`, `[strong French accent]`, `[strong Russian accent]` (or any accent)

### Non-Verbal Sounds
`[laughs]`, `[laughs harder]`, `[starts laughing]`, `[chuckles]`, `[giggles]`, `[giggling]`, `[wheezing]`, `[snorts]`, `[sighs]`, `[exhales]`, `[exhales sharply]`, `[inhales deeply]`, `[gasps]`, `[happy gasp]`, `[groaning]`, `[clears throat]`, `[swallows]`, `[gulps]`, `[muttering]`, `[yawning]`, `[snoring]`, `[sings]`, `[woo]`

### Sound Effects (use sparingly)
`[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[record scratch]`, `[binary beeping]`, `[leaves rustling]`, `[gentle footsteps]`

### Overall Direction / Scene Context
`[football]`, `[wrestling match]`, `[auctioneer]`, `[news broadcast]`, `[podcast studio]`, `[hacker den]`, `[library]`, `[classroom]`, `[coffee shop]`

### Best Practices
1. **No SSML**: Never use `<break>`, `<emphasis>`, `<phoneme>` — v3 ignores or chokes on them.
2. **Punctuation for pause**: Ellipses `...` for hesitation, period for hard stop, dash for interruption.
3. **Capitalization for stress**: "It was a VERY long day."
4. **Combine tags**: `[sad][whispering] I miss you so much.`
5. **3-8 tags per page** — over-tagging causes instability.
6. **Match to voice**: A serious professional voice may not respond to `[giggles]`.
7. **Do NOT use non-auditory tags**: `[standing]`, `[grinning]`, `[pacing]`, `[music]` will be spoken aloud or ignored.

## Audio Tags (Fish Audio S2 / S2.1-Pro)

Fish Audio uses [square bracket] natural-language cues. S2 supports **64+ expressions** and is NOT limited to a fixed set — any descriptive expression like `[whispers sweetly]` or `[laughing nervously]` works.

- **Sample basic**: `[happy]`, `[sad]`, `[angry]`, `[excited]`, `[calm]`, `[nervous]`, `[confident]`, `[surprised]`, `[scared]`, `[worried]`, `[frustrated]`, `[satisfied]`, `[delighted]`, `[empathetic]`, `[embarrassed]`, `[disgusted]`, `[proud]`, `[relaxed]`, `[grateful]`, `[curious]`, `[sarcastic]`, `[determined]`, `[hopeful]`, `[nostalgic]`, `[bored]`, `[confused]`, `[disappointed]`, `[regretful]`, `[anxious]`, `[resigned]`
- **Tone**: `[whispering]`, `[shouting]`, `[screaming]`, `[soft tone]`, `[in a hurry tone]`
- **Audio effects**: `[laughing]`, `[chuckling]`, `[sobbing]`, `[crying loudly]`, `[sighing]`, `[groaning]`, `[panting]`, `[gasping]`, `[yawning]`, `[snoring]`
- **Pauses**: `[break]` (short), `[long-break]` (extended)
- **Special**: `[audience laughing]`, `[background laughter]`, `[crowd laughing]`

Place cues at beginning of sentences for sentence-level emotion, or inline for word-level.

## Audio Tags (xAI Grok Voice)

Grok supports two types: **inline** `[tag]` at specific points, and **wrapping** `<tag>text</tag>` for delivery style changes.

### Inline Tags
- **Pauses**: `[pause]`, `[long-pause]`
- **Laughter & crying**: `[laugh]`, `[chuckle]`, `[giggle]`, `[cry]`
- **Mouth sounds**: `[tsk]`, `[tongue-click]`, `[lip-smack]`
- **Breathing**: `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`
- **Other**: `[hum-tune]`

### Wrapping Tags
- `<whisper>text</whisper>` — whispered
- `<shouting>text</shouting>` — shouted
- `<sing>text</sing>` — singing
- `<hum>text</hum>` — humming
- `<narrate>text</narrate>` — narration style
- `<fast>text</fast>` — faster delivery
- `<slow>text</slow>` — slower delivery

## API Endpoints

### Text-to-Speech (ElevenLabs)
```
POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}
```

### Text-to-Speech (Fish Audio)
```
POST https://api.fish.audio/v1/tts
```
Model in header (`model: s2.1-pro-free`), voice as `reference_id` (empty = default built-in).

### Text-to-Speech (xAI Grok Voice)
```
POST https://api.x.ai/v1/tts
```
Requires `language` (BCP-47 or `"auto"`). Supports custom voices.

### Voice Cloning (ElevenLabs)
```
POST https://api.elevenlabs.io/v1/voices/add
```

### Audio Isolation
```
POST https://api.elevenlabs.io/v1/audio-isolation
```

## Models

| Model ID | Provider | Best For | Audio Tags | Break Tags |
|----------|----------|----------|------------|------------|
| `eleven_multilingual_v3` | ElevenLabs | Expressive narration, character voices | Yes¹ | No |
| `eleven_turbo_v2_5` | ElevenLabs | Fast, lower latency | Yes¹ | No |
| `eleven_multilingual_v2` | ElevenLabs | Natural speech, multiple languages | No | Yes² |
| `s2.1-pro-free` | Fish Audio | Free expressive TTS (free till Jul 2026) | Yes³ | No⁴ |
| `s2-pro` | Fish Audio | Premium expressive TTS | Yes³ | No⁴ |
| Grok Voice (built-in) | xAI | Expressive + streaming | Yes⁵ | Yes⁵ |

¹ v3 uses `[square bracket]` tags only — no SSML `<break>` support.  
² Supports SSML `<break time="x.xs" />`. No bracket audio tags.  
³ Fish uses `[square bracket]` natural-language emotion cues.  
⁴ Fish uses `[break]` and `[long-break]` for pauses instead of SSML.  
⁵ xAI supports inline `[tag]` + wrapping `<tag>text</tag>`.
