---
name: short-video-tts-script-writer
description: >
  Write high-energy, fast-paced short video scripts optimized for ElevenLabs TTS
  (or similar neural speech synthesis). Combines Fireship-style dense explainer
  pacing with TTS text normalization, pronunciation control, and expressive
  audio tags. Use when generating voiceover scripts for tech explainers,
  tutorials, news briefs, or any short-form video where the narration will be
  AI-generated. Outputs scripts that are structurally tight, humor-dense, and
  acoustically clean — ready to paste into a TTS generator without manual
  cleanup.
license: Complete terms in LICENSE.txt
---

# Short Video TTS Script Writer

Use this skill when the user wants a voiceover script for a short video that
will be narrated with AI text-to-speech (ElevenLabs, etc.). It fuses
**Fireship-style information density and humor** with **TTS engineering best
practices** so the generated audio sounds professional, expressive, and
natural — not robotic or error-prone.

**Golden rule**: Write for the ear first, the eye second, and the algorithm
third. Every line must earn its place. If a sentence doesn't teach, entertain,
or set up a punchline, cut it.

---

## 1. Use When

- User says: "write a script for a short video about X"
- User mentions: "voiceover script", "narration script", "TTS script",
  "ElevenLabs script", "AI voice script"
- Video formats: "X in 100 Seconds", tech explainer, news brief, quick tutorial,
  short-form vertical video (Reels/Shorts/TikTok)
- Any script that will be fed to a TTS engine rather than recorded by a human

---

## 2. Script Structure Templates

### A. "X in 100 Seconds" (95-105s, ~20 visual shots)

| Time | Beat | Script Guidance |
|------|------|-----------------|
| 0:00-0:03 | Cold open hook | One provocative sentence. No intro. |
| 0:03-0:08 | Title card | Narrator pauses; title is visual only. |
| 0:08-0:35 | What it IS + first core concept | Short sentences. One idea per breath. Start code demo immediately. |
| 0:35-0:50 | The gotcha / common mistake | Setup → meme insert. Deadpan delivery. |
| 0:50-1:15 | Second concept / practical example | Quick code snippet. Imperative mood. |
| 1:15-1:35 | Ecosystem mention or analogy | One sentence analogy. Cut if too long. |
| 1:35-1:50 | Wrap + outro in topic syntax | Code-syntax outro. No generic "like and subscribe". |
| 1:50-2:00 | Hard cut | Silence or final meme. |

**Meme target**: 5-8 inserts. **Forbidden words**: "Welcome", "guys", "today
we're going to", "in this video", "let's get started".

### B. Shorts / Reels (30-60s, ~12-18 shots)

| Time | Beat | Script Guidance |
|------|------|-----------------|
| 0:00-0:02 | Text hook (visual only) | No voice yet. Big on-screen text. |
| 0:02-0:05 | Voice enters with provocation | One punchy statement. |
| 0:05-0:55 | Rapid tips / demos | Hard-cut between concepts in script. One sentence per shot. |
| 0:55-1:00 | Meme + outro text | Voice drops out; visual punchline. |

**Meme target**: 3-5 inserts.

### C. The Code Report (4-6 min, ~40-50 visual inserts)

| Time | Beat | Script Guidance |
|------|------|-----------------|
| 0:00-0:05 | Newsreel title | Visual. Narrator silent or low "mm-hmm". |
| 0:05-0:20 | Hook | "In case you missed it, [Company] just [shocking thing]." |
| 0:20-1:30 | Background | Timeline narration. Keep sentences short. |
| 1:30-2:30 | Technical implications | Code examples read as spoken descriptions, not literal syntax. |
| 2:30-3:30 | Community reaction | Read tweets/reddit comments with sarcastic tone tags. |
| 3:30-4:30 | Analysis / honest take | Practical advice. Self-deprecating humor works here. |
| 4:30-5:00 | Outro in relevant syntax | Same as 100 Seconds. |

**Meme target**: 10-15 inserts.

---

## 3. Voice & Tone (Narration Character)

The narrator is a **senior dev who has seen it all** — knowledgeable, slightly
cynical, secretly enthusiastic. Smart, dry, fast. NOT a corporate presenter.

### Delivery Rules for TTS
1. **Short sentences**. One idea per breath. TTS models handle short clauses better than complex compound sentences.
2. **Imperative mood**: "Install it. Import it. Break it."
3. **Deadpan sarcasm**: The funnier the content, the flatter the delivery. Let audio tags carry the emotion.
4. **No verbal filler**: Remove "so", "basically", "you know", "kind of" at the drafting stage.
5. **Contrast for humor**: Serious technical explanation → absurd one-liner.
6. **Forbidden words**: "Welcome", "guys", "today we're going to", "in this video",
   "let's get started", "before we begin", "as you can see".

---

## 4. TTS Text Normalization (Non-Negotiable)

TTS models mispronounce numbers, symbols, dates, and abbreviations. **Normalize
ALL of these in the script before adding audio tags.** Do not leave raw symbols
in the output.

### Normalization Table

| Raw Input | Spoken Form | Example |
|-----------|-------------|---------|
| `$42.50` | forty-two dollars and fifty cents | `$99.99` → ninety-nine dollars and ninety-nine cents |
| `£1,001.32` | one thousand and one pounds and thirty-two pence | |
| `1234` | one thousand two hundred thirty-four | Expand all bare numbers > 20 |
| `3.14` | three point one four | |
| `555-555-5555` | five five five, five five five, five five five five | Phone numbers digit-by-digit |
| `2nd` | second | All ordinals |
| `XIV` | fourteen | Roman numerals ("the fourteenth" if a title) |
| `Dr.` | Doctor | Expand abbreviations |
| `Ave.` | Avenue | |
| `St.` | Street | But saints: "St. Patrick" stays |
| `Ctrl + Z` | control z | Keyboard shortcuts |
| `100km` | one hundred kilometers | Unit abbreviations |
| `100%` | one hundred percent | Percentages |
| `elevenlabs.io/docs` | eleven labs dot io slash docs | URLs: spell out separators |
| `2024-01-01` | January first, two-thousand twenty-four | Dates |
| `14:30` | two thirty PM | Times |
| `01/02/2023` | January second, two-thousand twenty-three | Pick locale-appropriate form |
| `API` | A-P-I or "application programming interface" | Acronyms: spell out if uncommon |
| `HTML` | H-T-M-L or "hypertext markup language" | |
| `npm install react` | N-P-M install react | Package managers as letters |
| `JSON` | J-son or "Jay-sawn" | Choose the pronunciation you want |

### Pronunciation Tricks for Edge Cases

- **Phonetic spelling**: If a word is consistently mispronounced by your chosen
  voice, respell it phonetically in the script (e.g., "trapezIi" for emphasis).
- **Capital letters for stress**: "It was a VERY long day." Capitalization
  increases emphasis in Eleven v3.
- **Ellipses for hesitation**: "It… well, it might work." Adds pause + weight.
- **Dashes for interruption**: "Wait — what's that noise?"

---

## 5. Audio Tags for Expressive TTS

For Eleven v3 (or tag-aware TTS models), inject audio tags to control emotion
and non-verbal delivery. **Tags must describe auditory actions only.** Place
them strategically before or after the segment they modify.

### Tag Categories

**Emotional Directions:**
`[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[annoyed]`,
`[appalled]`, `[thoughtful]`, `[surprised]`, `[sarcastic]`, `[curious]`,
`[mischievously]`, `[professional]`, `[reassuring]`, `[frustrated]`, `[delighted]`

**Non-Verbal Sounds:**
`[laughs]`, `[laughs harder]`, `[starts laughing]`, `[chuckles]`, `[giggles]`,
`[sighs]`, `[exhales]`, `[exhales sharply]`, `[inhales deeply]`, `[clears throat]`,
`[short pause]`, `[long pause]`, `[wheezing]`, `[snorts]`, `[gasps]`, `[muttering]`

**Sound Effects (use sparingly):**
`[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`

### Tag Placement Rules

1. **Before the line** for global mood: `[sarcastic] Oh, you thought CSS was easy?`
2. **After the line** for reaction: `Another build tool. [sighs]`
3. **Inline** for shifts: `It was working [excited] until it wasn't. [sighs]`
4. **Combine** for complex delivery: `[nervously] So… I may have debugged myself. [robotic voice] TENCE.`
5. **Do NOT** turn narrative descriptions into tags. If the text says "He laughed loudly," add a tag instead of replacing: `He laughed loudly [chuckles].`
6. **Do NOT** use non-auditory tags like `[standing]`, `[grinning]`, `[pacing]`, `[music]`.

### Tag Density by Format

| Format | Tag Density | Guidance |
|--------|-------------|----------|
| "100 Seconds" | 4-6 tags | Fast pace; use short tags like `[sighs]` or `[excited]` |
| Shorts | 3-5 tags | Punchy; one tag per major beat |
| Code Report | 8-12 tags | More room for emotional arc |

### Fish Audio S2 / S2.1-Pro Tags

Fish Audio uses `[square bracket]` natural-language emotion cues — **not a fixed list**, any descriptive expression works:

- **Emotions:** `[happy]`, `[sad]`, `[angry]`, `[excited]`, `[calm]`, `[nervous]`, `[confident]`, `[surprised]`, `[scared]`, `[worried]`, `[frustrated]`, `[empathetic]`, `[embarrassed]`, `[curious]`, `[sarcastic]`, `[determined]`, `[bored]`, `[confused]`, `[anxious]`
- **Tones:** `[whispering]`, `[shouting]`, `[screaming]`, `[soft tone]`, `[in a hurry tone]`
- **Sounds:** `[laughing]`, `[chuckling]`, `[sobbing]`, `[sighing]`, `[groaning]`, `[panting]`, `[gasping]`, `[yawning]`, `[snoring]`
- **Pauses:** `[break]` (short), `[long-break]` (extended)
- **No SSML.** Use `[break]`/`[long-break]` for pauses.

### xAI Grok Voice Tags

- **Inline:** `[pause]`, `[long-pause]`, `[hum-tune]`, `[laugh]`, `[chuckle]`, `[giggle]`, `[cry]`, `[tsk]`, `[tongue-click]`, `[lip-smack]`, `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`
- **Wrapping:** `<whisper>text</whisper>`, `<shouting>text</shouting>`, `<sing>text</sing>`, `<hum>text</hum>`, `<narrate>text</narrate>`, `<fast>text</fast>`, `<slow>text</slow>`

---

## 6. Pause & Pacing Control

### For Eleven v2 / v2.5 Models
Use `<break time="x.xs" />` for natural pauses up to 3 seconds.

```
"Hold on, let me think." <break time="1.5s" /> "Alright, I've got it."
```

**Caution**: Too many break tags in one generation causes instability (speedups,
artifacts). Use 1-2 per script maximum. Prefer punctuation pauses instead.

### For Eleven v3 Models
v3 does NOT support `<break>`. Use:
- **Ellipses** for hesitation: `It was... a mistake.`
- **Capitalization** for emphasis: `It was a VERY long day.`
- **Punctuation** for rhythm: commas, periods, dashes
- **Audio tags** for breath/pause: `[short pause]`, `[long pause]`, `[exhales]`

### General Pacing Rules
1. **Record/compress to 1.15-1.25x** in post, OR write sentences that read fast
   naturally.
2. **One idea per sentence** — TTS handles short clauses better.
3. **Aggressive jump-cut style** in writing: separate distinct thoughts with
   line breaks so the editor knows to cut.

---

## 7. Output Format

Deliver the final script in this exact structure:

```markdown
# [Topic] — [Format] Script

## Metadata
- **Target Duration**: [e.g., 95-105s]
- **TTS Model**: [Eleven v3 / Fish S2.1-Pro / xAI Grok / Multilingual v2]
- **Voice**: [Voice name or description]
- **Meme Inserts**: [count]
- **Audio Tags**: [count]

## Visual Shot List (for editor)
1. [0:00-0:03] Cold open: [description]
2. [0:03-0:08] Title card: [description]
3. ...

## Normalized Voiceover Script

[Paste the fully normalized, tag-enhanced script here.]

[Each shot should be on its own line or clearly delimited.]

## Pronunciation Notes
- "React": ree-act (not ray-act)
- "Kubernetes": koo-ber-net-ees
- [Any other words that need explicit direction]
```

---

## 8. Anti-Patterns (NEVER Do)

1. **"Hey guys, welcome back"** — Start with the hook. No intros.
2. **Leaving raw symbols in script** — `$100`, `API`, `npm`, `2024-01-01` must be normalized.
3. **Long compound sentences** — TTS drifts on clauses. Break them up.
4. **No audio tags on v3** — Flat TTS sounds robotic. Tags are the emotion layer.
5. **Non-auditory tags** — `[grinning]`, `[pacing]`, `[music]` will confuse the model.
6. **Over-explaining** — If a frame doesn't entertain, teach, or transition, cut it.
7. **Corporate voice** — "We're excited to announce" is forbidden.
8. **Fade-transition language** — Script should feel like hard cuts: "Next. Install it. Break it."
9. **Ignoring normalization** — TTS will say "dollar sign one zero zero" if you leave `$100`.
10. **Completeness over entertainment** — Cut concepts before you cut jokes.

---

## 9. Quick Reference: Normalized Script Example

**Topic**: TypeScript in 100 Seconds  
**Model**: Eleven v3  
**Voice**: fast, dry, slightly sarcastic

```
[excited] TypeScript is JavaScript that went to college.
[short pause]
It adds static types so your code breaks in the editor instead of in production.
[short pause]

Install it with NPM. npm install typescript.
[sarcastic] Or don't. Enjoy your runtime errors.

Type inference means you don't have to annotate everything.
[introspective] Unless you want to. [mischievously] Or unless your team lead demands it.

Interfaces describe shapes. Types describe shapes.
[appalled] Yes, they're mostly the same. No, we don't talk about it.

Generics let you write reusable components.
T is not a variable name. It's a way of life.

That's TypeScript in one hundred seconds.
[whispers] Now go fix those any types.
```

---

## 10. Quality Checklist

Before delivering the script, verify:

- [ ] Hook in first 3 seconds (no intro)
- [ ] All numbers, symbols, dates, abbreviations normalized for speech
- [ ] Acronyms spelled out or phonetically guided
- [ ] Audio tags are auditory-only (no `[grinning]`, `[music]`)
- [ ] Audio tags placed strategically before/after relevant segments
- [ ] Tag density matches format target
- [ ] Sentences are short (one idea per breath)
- [ ] No forbidden words: "welcome", "guys", "today we're going to", "in this video"
- [ ] At least one sarcastic or self-deprecating moment
- [ ] Meme insert opportunities noted in shot list
- [ ] Pronunciation notes included for ambiguous tech terms
- [ ] Outro uses topic-relevant syntax (not generic CTA)
- [ ] If using v2/v2.5: `<break>` tags used sparingly (max 1-2)
- [ ] If using v3: no `<break>` tags; ellipses + audio tags only
