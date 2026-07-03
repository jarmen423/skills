---
name: dialogue-script-writer
description: >
  Write natural, expressive multi-speaker dialogue scripts optimized for
  ElevenLabs Text to Dialogue (v3). Covers speaker dynamics, turn-taking,
  interruptions, emotional audio tags, and API constraints. Use when generating
  conversational scripts, interview formats, podcast episodes, dramatic scenes,
  or any multi-speaker content that will be produced with AI dialogue synthesis.
  Outputs chunked scripts ready for the Text to Dialogue API.
license: Complete terms in LICENSE.txt
---

# Dialogue Script Writer

Use this skill when the user wants a **multi-speaker dialogue script** that will
be generated with ElevenLabs **Text to Dialogue** (v3 model). It ensures the
script sounds **natural and conversational** — with proper turn-taking,
interruptions, emotional variety, and acoustic cleanliness.

**Golden rule**: Dialogue is a tennis match, not a monologue rally. Every line
should provoke a reaction, advance the topic, or reveal character.

---

## 1. Use When

- User says: "dialogue script", "conversation script", "multi-speaker script"
- User mentions: "Text to Dialogue", "two people talking", "interview script",
  "podcast dialogue", "dramatic scene", "character conversation"
- Content types: podcasts, interviews, debates, dramatic scenes, tutorials in
  dialogue format, customer service simulations, audiobook dialogue
- Any script targeting ElevenLabs Text to Dialogue API or similar multi-speaker
  TTS pipeline

---

## 2. Speaker Dynamics

### Defining Characters
Before writing, establish each speaker's voice:

| Attribute | Host A | Host B |
|-----------|--------|--------|
| **Role** | Expert / Guide / Skeptic | Learner / Challenger / Optimist |
| **Tone** | Dry, measured, authoritative | Energetic, curious, reactive |
| **Speech Pattern** | Short, declarative sentences | Questions, exclamations, interruptions |
| **Audio Tag Signature** | `[deadpan]`, `[thoughtful]`, `[sarcastic]` | `[excited]`, `[surprised]`, `[laughing]` |

**For 3+ speakers**: Assign each a distinct role and emotional register so the
listener can tell them apart even without visual cues.

### Chemistry Rules
1. **No monologues longer than 15 seconds.** Cut to another speaker for a
   reaction, question, or punchline.
2. **Reactions are content.** "Wait, WHAT?" is as valuable as the explanation
   that provokes it.
3. **Interruptions create realism.** People don't wait for perfect pauses.
4. **Let speakers disagree.** Conflict is more engaging than consensus.
5. **Shared moments land harder.** Both speakers laughing at the same joke hits
   harder than one person laughing alone.

---

## 3. Dialogue Mechanics

### Interruptions
Use dashes and audio tags to create natural cut-ins.

```
Speaker 1: [starting to speak] So the way it works is—
Speaker 2: [jumping in] —wait, is this the part where you explain callbacks?
Speaker 1: [sighs] Unfortunately, yes.
```

### Call and Response
One speaker drops information; the other reacts. The reaction is the beat.

```
Speaker 1: [deadpan] The database is down.
Speaker 2: [alarmed] AGAIN?!
Speaker 1: [sarcastic] Third time this week. We're calling it "intermittent uptime."
```

### Tag Team Explanation
Split one concept across speakers. Faster and more engaging than a solo lecture.

```
Speaker 1: A closure is when a function remembers the scope it was created in—
Speaker 2: [excited] —even after that scope has finished executing!
Speaker 1: [impressed] Exactly. You've been paying attention.
```

### Devil's Advocate
One speaker raises an objection so the other can demolish it. The viewer learns
through conflict.

```
Speaker 2: [questioning] But do we really need types? JavaScript was fine for years.
Speaker 1: [appalled] Fine? [exhales sharply] You debug undefined at three AM and tell me it was fine.
```

### Trailing Thoughts
Use ellipses to indicate hesitation, trailing off, or unfinished ideas.

```
Speaker 1: [indecisive] So I was thinking maybe we could... uhhh...
Speaker 2: [quizzically] Use a different framework?
Speaker 1: [relieved] Yes! Thank you.
```

### Overlapping Intent
Simulate people talking over each other without actual audio overlap issues.

```
Speaker 1: [starting to speak] If we refactor the—
Speaker 2: [overlapping] —the whole module?
Speaker 1: [pause] I was going to say "the config." But sure, let's burn it all down.
```

---

## 4. Script Structure Templates

### A. Interview Format (5-15 min)
- **Intro (0:00-0:30)**: Host introduces guest + topic. One sentence each.
- **Background (0:30-2:00)**: Guest's origin story. Host asks follow-ups.
- **Core Topic (2:00-8:00)**: 3-5 questions. Each answer provokes a reaction.
- **Hot Take (8:00-10:00)**: Devil's advocate question. Lively debate.
- **Rapid Fire (10:00-12:00)**: Short questions, shorter answers.
- **Wrap (12:00-15:00)**: One lesson + where to find guest.

### B. Podcast Episode (20-40 min)
- **Cold Open (0:00-1:00)**: Best clip from the episode. Hooks the listener.
- **Intro (1:00-2:00)**: Music + show identity. Host energy sets the tone.
- **Segment 1: News / Topic (2:00-10:00)**: Hosts trade takes. No monologues.
- **Segment 2: Deep Dive (10:00-25:00)**: One concept explored through dialogue.
- **Segment 3: Listener Mail / Q&A (25:00-35:00)**: Hosts read questions aloud,
  then debate answers.
- **Outro (35:00-40:00)**: Summary + CTA. Specific, not generic.

### C. Dramatic Scene (2-5 min)
- **Establishment**: Setting + relationship. Audio tags set mood.
- **Inciting Incident**: Something changes. One speaker drops a bombshell.
- **Rising Tension**: Disagreement escalates. Shorter turns, sharper tags.
- **Climax**: Emotional peak. `[angry]`, `[desperately]`, `[shouting]`.
- **Resolution**: One speaker concedes, or they agree to disagree.
- **Button**: Final line that lands the scene. Often ironic or bittersweet.

### D. Tutorial in Dialogue (3-8 min)
- **Problem Setup**: Host B describes the struggle. Host A listens.
- **Concept Introduction**: Host A explains. Host B asks "dumb" questions.
- **Walkthrough**: Step-by-step, alternating speakers.
- **Gotcha Moment**: Host B tries it wrong. Host A corrects with a joke.
- **Wrap**: Both confirm understanding. Shared victory.

---

## 5. TTS Text Normalization for Dialogue

Every speaker's lines must be normalized BEFORE audio tags are applied. TTS
errors in dialogue are especially jarring because they break the conversational
flow.

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
| `npm` | N-P-M |
| `JSON` | J-son or "Jay-sawn" |

### Dialogue-Specific Normalization
- **Code snippets**: Read as spoken descriptions.
  - Bad: `const x = useState(0)`
  - Good: "const x equals use state zero"
- **File paths**: Spell separators. `src/components/Button.tsx` → "src slash
  components slash button dot tee-ess-ex"
- **URLs in conversation**: If hosts joke about a URL, normalize it fully.
  Nothing kills a punchline like a robot saying "h-t-t-p-s colon slash slash."

---

## 6. Audio Tags for Expressive Dialogue

Eleven v3 Text to Dialogue uses square-bracket tags for emotion, delivery,
non-speech audio events, and scene context. **Tags must describe auditory
actions only.**

### Tag Categories

**Emotional Directions:**
`[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[annoyed]`,
`[appalled]`, `[thoughtful]`, `[surprised]`, `[sarcastic]`, `[curious]`,
`[mischievously]`, `[professional]`, `[reassuring]`, `[frustrated]`, `[delighted]`,
`[deadpan]`, `[cautiously]`, `[cheerfully]`, `[quizzically]`, `[elated]`,
`[nervously]`, `[alarmed]`, `[sheepishly]`, `[stifling laughter]`, `[cracking up]`,
`[desperately]`, `[panicking]`, `[warmly]`, `[impressed]`, `[dismissive]`,
`[dramatically]`, `[with genuine belly laugh]`, `[robotic voice]`, `[singing]`

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
`[podcast studio]`, `[hacker den]`, `[classroom]`, `[coffee shop]`

### Tag Placement Rules

1. **Before the line** for mood: `[sarcastic] Oh, you thought this was easy?`
2. **After the line** for reaction: `Another framework. [sighs]`
3. **Inline** for mid-sentence shifts: `It was working [excited] until it wasn't.`
4. **Interrupt tags** for overlapping intent:
   ```
   Speaker 1: [starting to speak] So I was thinking—
   Speaker 2: [jumping in] —that we should rewrite everything?
   ```
5. **Scene context tags** at the start of a chunk: `[podcast studio]` or `[coffee shop]`
6. **Do NOT** use non-auditory tags: `[standing]`, `[grinning]`, `[pacing]`, `[music]`
7. **Do NOT** turn narrative into tags. If text says "He laughed," add a tag:
   `He laughed [chuckles].`

### Tag Density Guidelines

| Content Type | Tags per Speaker | Guidance |
|--------------|-----------------|----------|
| Interview | 4-8 | Professional but expressive |
| Podcast | 6-12 | Higher energy, more reactions |
| Dramatic Scene | 10-20 | Full emotional arc per speaker |
| Tutorial Dialogue | 3-6 | Clear and helpful, occasional humor |
| Customer Simulation | 4-6 | `[professional]`, `[sympathetic]`, `[reassuring]` |

---

## 7. Pacing & Pause Control (v3 Specific)

**Eleven v3 does NOT support `<break>` tags.** Use these instead:

| Technique | Effect | Example |
|-----------|--------|---------|
| Ellipses | Hesitation, trailing thought | `[indecisive] I was thinking maybe... uhhh...` |
| Capitalization | Emphasis, stress | `It was a VERY long day.` |
| Dashes | Interruption, abrupt stop | `Wait — you're telling me it works?` |
| Commas | Brief rhythmic pause | `Okay, so, the way it works is...` |
| Periods | Hard stop, new beat | Short sentences. Clear ideas. |
| Audio tags | Breath, pause, non-verbal | `[short pause]`, `[exhales]`, `[sighs]` |

### Pacing Rules for Dialogue
1. **Average turn length**: 3-8 seconds. Never let one speaker hold the floor
   longer than 10-15 seconds.
2. **Reaction beats**: The other speaker should respond within 1-2 seconds of a
   punchline or key point.
3. **Vary turn length**: Mix short reactions ("Wait, WHAT?") with longer
   explanations to create rhythm.
4. **Silence as a beat**: Dead silence after an absurd statement can be
   comedic — but mark it with `[long pause]` or a scene tag.

---

## 8. API Constraints & Chunking

ElevenLabs Text to Dialogue has specific limits:

| Constraint | Limit |
|------------|-------|
| Model | Eleven v3 ONLY |
| Characters per request | Max 2,000 total across ALL speakers |
| Speakers | Unlimited, but 2-3 recommended for clarity |
| Determinism | Nondeterministic — use `seed` parameter for consistency |
| Free regenerations | 2 per generation (dashboard only, same params) |

### Chunking Strategy
If the full script exceeds 2,000 characters:
1. Split at natural scene boundaries, topic shifts, or hard cuts.
2. End each chunk on a mini-cliffhanger, reaction beat, or emotional peak.
3. Use the same `seed` value if regenerating a chunk for consistency.
4. Concatenate audio in post-production with hard cuts.

**Quick reference**: A 5-minute interview at conversational pace is usually
4-6 chunks.

---

## 9. Output Format

Deliver the final script in this structure:

```markdown
# [Title] — Dialogue Script

## Metadata
- **Content Type**: [Interview / Podcast / Dramatic Scene / Tutorial Dialogue]
- **Target Duration**: [e.g., 5-10 minutes]
- **Model**: Eleven v3 (Text to Dialogue)
- **Speakers**: [count]
- **Chunks**: [1-N]
- **Scene Context**: [podcast studio / coffee shop / classroom / etc.]

## Speaker Definitions
- **Speaker 1 (Alex)**: [Role, tone, tag signature]
- **Speaker 2 (Jordan)**: [Role, tone, tag signature]
- **Speaker 3 (optional)**: [Role, tone, tag signature]

## Dialogue Script

### Chunk 1 (chars: X / 2000)
[Scene context tag if applicable]

Speaker 1: [deadpan] The deployment failed.
Speaker 2: [alarmed] Again?!
Speaker 1: [sarcastic] Third time this week.
...

### Chunk 2 (chars: X / 2000)

Speaker 2: [starting to speak] So what you're saying is—
Speaker 1: [jumping in] —that we should have used Kubernetes?
...

## Pronunciation Notes
- "React": ree-act
- "Kubernetes": koo-ber-net-ees
- [Any ambiguous terms]

## Post-Production Notes
- Compress all voices equally (2:1 ratio, -18dB threshold)
- EQ: slight high-mid boost (+2-3dB at 3-5kHz) for clarity
- Hard cuts between chunks — no crossfade
- Optional: background ambience per scene context
```

---

## 10. Anti-Patterns (NEVER Do)

1. **One-speaker monologues** — If a speaker talks for more than 15 seconds,
   insert a reaction, question, or interruption.
2. **"So, welcome to the show" intros** — Start with conflict, curiosity, or a
   provocative statement.
3. **Leaving raw symbols** — `$100`, `API`, `npm`, `2024-01-01` must be normalized.
4. **No audio tags** — Flat dialogue sounds like robots reading a transcript.
5. **Non-auditory tags** — `[grinning]`, `[pacing]`, `[music]` will be spoken or fail.
6. **Consensus-only dialogue** — Agreement is boring. Let speakers disagree,
   misunderstand, or one-up each other.
7. **Ignoring the 2000-char limit** — The API will reject or truncate. Chunk
   proactively.
8. **Identical voices** — If using the API, assign distinct voices to each
   speaker. Same voice = confusing dialogue.
9. **Fade-transition language** — Script should feel like hard cuts between takes.
10. **Using `<break>` tags** — v3 does not support SSML break tags. Use ellipses
    and audio tags only.

---

## 11. Quality Checklist

Before delivering the script, verify:

- [ ] Hook or conflict in first 3 lines
- [ ] All numbers, symbols, dates, abbreviations normalized for speech
- [ ] Acronyms spelled out or phonetically guided
- [ ] No speaker monologue exceeds 15 seconds uninterrupted
- [ ] Audio tags are auditory-only (no `[grinning]`, `[music]`)
- [ ] At least 2 interruptions or overlapping moments per chunk
- [ ] At least 1 reaction beat per key point
- [ ] Turn ratio is balanced — no single speaker dominates
- [ ] Tag density appropriate for content type
- [ ] Scene context tag used at start of each chunk if applicable
- [ ] Script chunked if total characters exceed 2,000
- [ ] Each chunk ends on a natural beat (not mid-sentence)
- [ ] No `<break>` tags used (v3 does not support them)
- [ ] Pronunciation notes included for ambiguous terms
- [ ] Speaker definitions clearly distinguish voice and personality

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
