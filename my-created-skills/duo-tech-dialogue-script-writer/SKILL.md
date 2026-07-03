---
name: duo-tech-dialogue-script-writer
description: >
  Write fast-paced, comedic two-host dialogue scripts for short tech explainer
  videos, optimized for ElevenLabs Text to Dialogue (v3). Fuses Fireship-style
  information density and meme-aware pacing with conversational banter,
  interruptions, call-and-response, and TTS normalization. Outputs chunked
  dialogue scripts ready for the ElevenLabs Text to Dialogue API with speaker
  labels, audio tags, and voice assignment notes. Use when the user wants a
  two-person co-host script, duo banter format, or conversational explainer
  that will be generated with multi-speaker TTS.
license: Complete terms in LICENSE.txt
---

# Duo Tech Dialogue Script Writer

Use this skill when the user wants a **two-person dialogue script** for a short
video that will be narrated with AI text-to-speech — specifically ElevenLabs
**Text to Dialogue** (v3 model). It fuses **Fireship-style density and humor**
with **natural conversational dynamics**: interruptions, call-and-response,
devil's advocacy, and shared disbelief.

**Golden rule**: Two voices should feel like one brain with two mouths — fast,
finishing each other's thoughts, and roasting technology together.

---

## 1. Use When

- User says: "two person script", "co-host script", "dialogue script",
  "banter format", "duo explainer"
- User mentions: "Text to Dialogue", "multi-speaker TTS", "two voices",
  "conversation script", "podcast style video"
- Video formats: dual-host explainers, interview-style tutorials, debate format,
  "two devs react" shorts, conversational news briefs
- Any script targeting ElevenLabs Text to Dialogue API or similar multi-speaker
  TTS pipeline

---

## 2. The Two-Host Dynamic

### Host A — The Cynic (Voice: dry, fast, deadpan)
- Role: Senior dev who has seen every hype cycle. Delivers facts with sarcasm.
- Speaks in short, imperative sentences. "Install it. Import it. Break it."
- Gets quietly excited about genuinely clever tech, then immediately masks it.
- Often starts explanations, then lets Host B finish the joke.

### Host B — The Hype Man (Voice: energetic, reactive, incredulous)
- Role: The curious challenger. Asks the "dumb" questions viewers are thinking.
- Reacts loudly to absurdity. "Wait, WHAT?" "You're kidding."
- Plays devil's advocate so Host A can demolish the counter-argument.
- Gets genuinely excited about features, then immediately roasted by Host A.

### Chemistry Rules
1. **No solo monologues longer than 15 seconds.** Cut away to the other host for
   a reaction, interruption, or punchline.
2. **Finish each other's sentences.** Host A starts a technical point; Host B
   lands the joke.
3. **Shared disbelief.** Both hosts react to tech absurdity — layered reactions
   are funnier than solo ones.
4. **Contrast drives comedy.** Host A is dry; Host B is animated. The gap
   between them is the humor.
5. **No corporate podcast energy.** This is not a "panel discussion." It's two
   devs arguing at a hackathon.

---

## 3. Dialogue Mechanics

### Interruptions
Use dashes and audio tags to create natural cut-ins. Eleven v3 handles
overlapping intent well when scripted clearly.

```
Speaker 1: [starting to speak] So I was thinking we could—
Speaker 2: [jumping in] —test our new timing features?
Speaker 1: [surprised] Exactly! How did you—
Speaker 2: [overlapping] —know what you were thinking? Lucky guess!
```

### Call and Response
Host A drops knowledge; Host B reacts. The reaction IS the beat.

```
Speaker 1: [deadpan] TypeScript is just JavaScript that went to college.
Speaker 2: [laughing] Okay, okay. But does it actually get a job after?
Speaker 1: [sarcastic] Only if it stops using any.
```

### Tag Team Explanation
Split one concept across two speakers. Faster than one person explaining.

```
Speaker 1: Generics let you write reusable components—
Speaker 2: [excited] —where T is not a variable name—
Speaker 1: [mischievously] —it's a way of life.
```

### Devil's Advocate
Host B raises an objection so Host A can crush it. Viewer learns through
conflict.

```
Speaker 2: [questioning] But do you REALLY need types? JavaScript was fine.
Speaker 1: [appalled] Fine? FINE? [exhales sharply] You debug undefined at three AM and tell me it was fine.
```

### Trailing Sentences
Use ellipses to indicate hesitation or trailing thoughts. Natural in dialogue.

```
Speaker 1: [indecisive] Hi, can I get uhhh...
Speaker 2: [quizzically] The usual?
Speaker 1: [elated] Yes! [laughs] I'm so glad you knew!
```

---

## 4. Script Structure Templates

### A. "X in 100 Seconds — Duo Edition" (95-105s, ~20 shots)

| Time | Beat | Dialogue Pattern |
|------|------|------------------|
| 0:00-0:03 | Cold open hook | Host A drops provocation. Host B reacts immediately. |
| 0:03-0:08 | Title card | Visual only. Brief host reactions off-camera or low. |
| 0:08-0:35 | What it IS | Host A explains. Host B interrupts with questions. Tag-team the core concept. |
| 0:35-0:50 | The gotcha | Host B states the common mistake. Host A corrects with sarcasm. Meme insert. |
| 0:50-1:15 | Second concept | Host A demos. Host B narrates the visual reaction. |
| 1:15-1:35 | Ecosystem / analogy | Both hosts rapid-fire one-sentence takes. |
| 1:35-1:50 | Wrap + outro | Host A delivers closing line. Host B adds deadpan tag. |
| 1:50-2:00 | Hard cut | Shared silence or final reaction meme. |

**Turn ratio target**: ~55% Host A, ~45% Host B. Neither should dominate.

### B. "Two Devs React" Short (30-60s, ~12-18 shots)

| Time | Beat | Dialogue Pattern |
|------|------|------------------|
| 0:00-0:02 | Text hook (visual) | Big on-screen text. Hosts silent. |
| 0:02-0:05 | Voice enters | Host A states the absurd fact. Host B gasps. |
| 0:05-0:55 | Rapid-fire takes | Alternate hosts every 3-5 seconds. No monologues. |
| 0:55-1:00 | Meme + outro | Both hosts react to the meme. Hard cut. |

### C. "The Code Report — Duo Desk" (4-6 min, ~40-50 inserts)

| Time | Beat | Dialogue Pattern |
|------|------|------------------|
| 0:00-0:05 | Newsreel title | Visual. Hosts do low "mm-hmm" or paper rustling. |
| 0:05-0:20 | Hook | Host A drops the headline. Host B reacts with shock. |
| 0:20-1:30 | Background | Host A narrates timeline. Host B interjects with disbelief. |
| 1:30-2:30 | Technical implications | Host A explains architecture. Host B asks clarifying questions. |
| 2:30-3:30 | Community reaction | Both hosts read tweets aloud, roasting each one. |
| 3:30-4:30 | Analysis / honest take | Host A gives practical advice. Host B plays skeptic. |
| 4:30-5:00 | Outro | Host A delivers code-syntax sign-off. Host B adds one-liner. |

---

## 5. TTS Text Normalization (Critical for Dialogue)

Every speaker's lines must be normalized BEFORE audio tags are applied. TTS
models mispronounce raw symbols, and in dialogue those errors destroy the
natural flow.

### Normalization Table

| Raw Input | Spoken Form |
|-----------|-------------|
| `$42.50` | forty-two dollars and fifty cents |
| `£1,001.32` | one thousand and one pounds and thirty-two pence |
| `1234` | one thousand two hundred thirty-four |
| `3.14` | three point one four |
| `555-555-5555` | five five five, five five five, five five five five |
| `2nd` | second |
| `XIV` | fourteen (or "the fourteenth" if a title) |
| `Dr.` | Doctor (but saints: "St. Patrick" stays) |
| `Ave.` | Avenue |
| `St.` | Street |
| `Ctrl + Z` | control z |
| `100km` | one hundred kilometers |
| `100%` | one hundred percent |
| `elevenlabs.io/docs` | eleven labs dot io slash docs |
| `2024-01-01` | January first, two-thousand twenty-four |
| `14:30` | two thirty PM |
| `API` | A-P-I or "application programming interface" |
| `HTML` | H-T-M-L |
| `npm install react` | N-P-M install react |
| `JSON` | J-son or "Jay-sawn" |

### Dialogue-Specific Normalization
- **Code snippets**: Read as spoken descriptions, not literal syntax.
  - Bad: `const x = useState(0)`
  - Good: "const x equals use state zero"
- **File paths**: Spell separators. `src/components/Button.tsx` → "src slash components slash button dot tee-ess-ex"
- **Git commands**: `git commit -m "fix"` → "git commit dash m fix"
- **URLs in banter**: If hosts are joking about a URL, normalize it fully so
the joke lands. Nothing kills a punchline like a TTS robot saying "h-t-t-p-s".

---

## 6. Audio Tags for Expressive Dialogue

Eleven v3 (Text to Dialogue) uses square-bracket tags for emotion, delivery,
and non-speech audio events. **Tags must describe auditory actions only.**

### Tag Categories

**Emotional Directions:**
`[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[annoyed]`,
`[appalled]`, `[thoughtful]`, `[surprised]`, `[sarcastic]`, `[curious]`,
`[mischievously]`, `[professional]`, `[reassuring]`, `[frustrated]`, `[delighted]`,
`[deadpan]`, `[cautiously]`, `[cheerfully]`, `[quizzically]`, `[elated]`,
`[nervously]`, `[alarmed]`, `[sheepishly]`, `[stifling laughter]`, `[cracking up]`,
`[desperately]`, `[panicking]`, `[mischievously]`, `[warmly]`, `[impressed]`,
`[dismissive]`, `[dramatically]`, `[with genuine belly laugh]`, `[robotic voice]`

**Non-Verbal Sounds:**
`[laughs]`, `[laughs harder]`, `[starts laughing]`, `[chuckles]`, `[giggles]`,
`[giggling]`, `[groaning]`, `[sighs]`, `[exhales]`, `[exhales sharply]`,
`[inhales deeply]`, `[clears throat]`, `[short pause]`, `[long pause]`,
`[wheezing]`, `[snorts]`, `[gasps]`, `[muttering]`, `[happy gasp]`

**Audio Events / Environment:**
`[leaves rustling]`, `[gentle footsteps]`, `[applause]`, `[clapping]`,
`[gunshot]`, `[explosion]`, `[swallows]`, `[gulps]`, `[record scratch]`,
`[binary beeping]`

**Overall Direction (scene context):**
`[football]`, `[wrestling match]`, `[auctioneer]`, `[news broadcast]`,
`[podcast studio]`, `[hacker den]`

### Tag Placement Rules

1. **Before the line** for mood: `[sarcastic] Oh, you thought CSS was easy?`
2. **After the line** for reaction: `Another build tool. [sighs]`
3. **Inline** for mid-sentence shifts: `It was working [excited] until it wasn't.`
4. **Interrupt tags** for overlapping intent:
   ```
   Speaker 1: [starting to speak] So I was thinking we could—
   Speaker 2: [jumping in] —test our new timing features?
   ```
5. **Scene context tags** can be placed at the start of a chunk to set ambient
   tone: `[podcast studio]` or `[hacker den]`
6. **Do NOT** use non-auditory tags: `[standing]`, `[grinning]`, `[pacing]`, `[music]`
7. **Do NOT** turn narrative into tags. If text says "He laughed," add a tag:
   `He laughed [chuckles].`

### Tag Density by Format

| Format | Tags per Speaker | Guidance |
|--------|-----------------|----------|
| "100 Seconds Duo" | 3-5 each | Fast pace; short tags like `[sighs]`, `[excited]` |
| "Two Devs React" | 2-4 each | Punchy; one tag per major beat |
| "Code Report Duo" | 6-10 each | More room for emotional arcs and reactions |

---

## 7. Pacing & Pause Control (v3 Specific)

**Eleven v3 does NOT support `<break>` tags.** Use these instead:

| Technique | Effect | Example |
|-----------|--------|---------|
| Ellipses | Hesitation, trailing thought | `[indecisive] Hi, can I get uhhh...` |
| Capitalization | Emphasis, stress | `It was a VERY long day.` |
| Dashes | Interruption, abrupt stop | `Wait — what's that noise?` |
| Commas | Brief rhythmic pause | `Install it, import it, break it.` |
| Periods | Hard stop, new beat | Short sentences. One idea. Next. |
| Audio tags | Breath, pause, non-verbal | `[short pause]`, `[exhales]`, `[sighs]` |

### Pacing Rules for Dialogue
1. **Average turn length**: 3-8 seconds. Never let one speaker hold the floor
   longer than 10 seconds.
2. **Reaction beats**: Host B should react within 1-2 seconds of Host A's
   punchline. Silence is death in duo format.
3. **Speed**: Script to be read at 1.15-1.25x natural pace. Write short
   sentences that feel fast even at normal speed.
4. **No dead air**: If there's a visual insert (meme, code demo), one host
   should narrate it or both should react to it. Never leave both silent.

---

## 8. API Constraints & Chunking

ElevenLabs Text to Dialogue has specific limits:

| Constraint | Limit |
|------------|-------|
| Model | Eleven v3 ONLY |
| Characters per request | Max 2,000 total across ALL speakers |
| Speakers | Unlimited, but 2 is recommended for clarity |
| Determinism | Nondeterministic — use `seed` parameter for consistency |
| Free regenerations | 2 per generation (dashboard only, same params) |

### Chunking Strategy
If the full script exceeds 2,000 characters:
1. Split at natural scene boundaries or hard cuts.
2. End each chunk on a mini-cliffhanger or reaction beat.
3. Regenerate with the same `seed` if you need to re-render a chunk.
4. Concatenate audio in post-production.

**Quick check**: A 100-second duo script with fast banter is usually 2-3 chunks.

---

## 9. Output Format

Deliver the final script in this structure:

```markdown
# [Topic] — Duo Dialogue Script

## Metadata
- **Format**: [100 Seconds Duo / Two Devs React / Code Report Duo]
- **Target Duration**: [e.g., 95-105s]
- **Model**: Eleven v3 (Text to Dialogue)
- **Host A Voice**: [Voice name / description — dry, fast, deadpan]
- **Host B Voice**: [Voice name / description — energetic, reactive]
- **Chunks**: [1-3]
- **Meme Inserts**: [count]
- **Total Tags**: [count]

## Voice Assignment
- **Speaker 1** = Host A (The Cynic)
- **Speaker 2** = Host B (The Hype Man)

## Visual Shot List (for editor)
1. [0:00-0:03] Cold open: [description]
2. [0:03-0:08] Title card: [description]
3. ...

## Dialogue Script

### Chunk 1 (chars: X / 2000)

Speaker 1: [deadpan] TypeScript is JavaScript that went to college.
Speaker 2: [laughing] Okay, okay. But does it actually get a job after?
Speaker 1: [sarcastic] Only if it stops using any.
...

### Chunk 2 (chars: X / 2000)

Speaker 1: [starting to speak] So I was thinking we could—
Speaker 2: [jumping in] —test our new timing features?
...

## Pronunciation Notes
- "React": ree-act
- "Kubernetes": koo-ber-net-ees
- [Any ambiguous terms]

## Post-Production Notes
- Compress both voices equally (2:1 ratio, -18dB threshold)
- EQ: slight high-mid boost (+2-3dB at 3-5kHz) for clarity
- Speed: 1.15-1.25x if narration feels slow
- Hard cuts between chunks — no crossfade
```

---

## 10. Anti-Patterns (NEVER Do)

1. **One-host monologues** — If a speaker talks for more than 15 seconds,
   insert an interruption or reaction.
2. **"Welcome to the show" intros** — Start with conflict or provocation.
3. **Leaving raw symbols** — `$100`, `API`, `npm`, `2024-01-01` must be normalized.
4. **No audio tags** — Flat dialogue sounds like two robots reading. Tags carry
   the personality.
5. **Non-auditory tags** — `[grinning]`, `[pacing]`, `[music]` will confuse v3.
6. **Corporate podcast tone** — This is not a "panel discussion." It's argument
   as entertainment.
7. **Ignoring the 2000-char limit** — The API will reject or truncate. Chunk
   proactively.
8. **Balanced expertise** — Host B should NOT be as expert as Host A. The gap
   creates teaching moments.
9. **Fade-transition language** — Script should feel like hard cuts.
10. **Completeness over chemistry** — Cut a fact before you cut a reaction beat.
    The duo dynamic is the product.

---

## 11. Quick Reference: Full Dialogue Example

**Topic**: TypeScript in 100 Seconds — Duo  
**Model**: Eleven v3 Text to Dialogue  
**Host A**: dry, fast, deadpan  
**Host B**: energetic, reactive, incredulous

```
Speaker 1: [deadpan] TypeScript is JavaScript that went to college.
Speaker 2: [laughing] Okay, okay. But does it actually get a job after?
Speaker 1: [sarcastic] Only if it stops using any.
Speaker 2: [appalled] Hey! any is a valid type!
Speaker 1: [sighs] So is drinking straight from the milk carton.
Speaker 2: [thoughtful] Fair.
Speaker 1: [starting to explain] It adds static types so your code breaks in the editor—
Speaker 2: [jumping in] —instead of in production at three AM!
Speaker 1: [impressed] Exactly. You're learning.
Speaker 2: [excited] Type inference means you don't annotate everything!
Speaker 1: [mischievously] Unless your team lead demands it.
Speaker 2: [groaning] Don't remind me.
Speaker 1: [deadpan] Interfaces describe shapes. Types describe shapes.
Speaker 2: [quizzically] So they're the same thing?
Speaker 1: [long pause] ...We don't talk about it.
Speaker 2: [stifling laughter] Got it.
Speaker 1: [wrapping up] That's TypeScript in one hundred seconds.
Speaker 2: [whispers] Now go fix those any types.
Speaker 1: [deadpan] I'm not whispering. I'm just disappointed.
```

---

## 12. Quality Checklist

Before delivering the script, verify:

- [ ] Hook in first 3 seconds; Host B reacts within 2 seconds
- [ ] All numbers, symbols, dates, abbreviations normalized for speech
- [ ] Acronyms spelled out or phonetically guided
- [ ] No speaker monologue exceeds 15 seconds uninterrupted
- [ ] Audio tags are auditory-only (no `[grinning]`, `[music]`)
- [ ] Turn ratio is roughly 55/45 — neither host dominates
- [ ] Tag density matches format target per speaker
- [ ] At least 2 interruptions or overlapping moments
- [ ] At least 1 devil's advocate exchange
- [ ] At least 1 shared disbelief / layered reaction moment
- [ ] No forbidden words: "welcome", "guys", "today we're going to", "in this video"
- [ ] Meme insert opportunities noted in shot list
- [ ] Pronunciation notes included for ambiguous tech terms
- [ ] Script chunked if total characters exceed 2,000
- [ ] Each chunk ends on a natural beat (not mid-sentence)
- [ ] No `<break>` tags used (v3 does not support them)

---

## 11. Multi-Provider Tag Reference

When using **Fish Audio S2/S2.1-Pro** instead of ElevenLabs (e.g., for budget-friendly single-speaker narration):

- `[happy]`, `[sad]`, `[angry]`, `[excited]`, `[calm]`, `[nervous]`, `[confident]`, `[surprised]`, `[scared]`, `[worried]`, `[frustrated]`, `[empathetic]`, `[embarrassed]`, `[curious]`, `[sarcastic]`, `[determined]`, `[bored]`, `[confused]`, `[anxious]`
- `[whispering]`, `[shouting]`, `[screaming]`, `[soft tone]`, `[in a hurry tone]`
- `[laughing]`, `[chuckling]`, `[sobbing]`, `[crying loudly]`, `[sighing]`, `[groaning]`, `[panting]`, `[gasping]`, `[yawning]`, `[snoring]`
- `[break]` (short pause), `[long-break]` (extended pause)

When using **xAI Grok Voice**:

- Inline: `[pause]`, `[long-pause]`, `[hum-tune]`, `[laugh]`, `[chuckle]`, `[giggle]`, `[cry]`, `[tsk]`, `[tongue-click]`, `[lip-smack]`, `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`
- Wrapping: `<whisper>text</whisper>`, `<shouting>text</shouting>`, `<sing>text</sing>`, `<hum>text</hum>`, `<narrate>text</narrate>`, `<fast>text</fast>`, `<slow>text</slow>`
