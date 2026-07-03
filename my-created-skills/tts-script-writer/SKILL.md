---
name: tts-script-writer
description: >
  Write expressive, production-ready voiceover scripts optimized for ElevenLabs
  TTS (or similar neural speech synthesis). Covers text normalization,
  pronunciation control, pause pacing, and audio tag injection for emotional
  delivery. Use when generating narration scripts, explainer voiceovers,
  audiobook passages, podcast intros, or any solo-speaker content that will be
  read by AI text-to-speech. Outputs clean, normalized scripts ready to paste
  into a TTS generator without manual cleanup.
license: Complete terms in LICENSE.txt
---

# TTS Script Writer

Use this skill when the user wants a **solo voiceover script** that will be
narrated by AI text-to-speech (ElevenLabs, etc.). It ensures the script is
**acoustically clean** (no mispronounced numbers or symbols), **expressive**
(via audio tags and punctuation), and **structurally sound** for TTS generation.

**Golden rule**: Write for the ear, not the eye. If it looks fine on paper but
sounds wrong when spoken, it's wrong.

---

## 1. Use When

- User says: "write a voiceover script", "narration script", "TTS script"
- User mentions: "ElevenLabs script", "AI voice script", "text to speech script"
- Content types: explainer videos, tutorials, audiobooks, podcast segments,
  e-learning modules, product demos, guided meditations, announcements
- Any single-speaker script fed to a TTS engine

---

## 2. Script Structure Templates

### A. Explainer / Tutorial (2-5 min)
- **Hook (0:00-0:15)**: One sentence that promises value or provokes curiosity.
- **Context (0:15-0:45)**: Why this matters. One paragraph max.
- **Core Concepts (0:45-3:00)**: 2-4 sections. One idea per section.
  - Concept → Example → Takeaway
- **Practical Application (3:00-4:00)**: Step-by-step or demo narration.
- **Wrap / CTA (4:00-5:00)**: Summary + next step. No generic "thanks for watching."

### B. Audiobook / Long-Form Narration (5+ min)
- **Scene Setting**: Establish mood with descriptive language and audio tags.
- **Pacing Variation**: Alternate between action (fast, short sentences) and
  reflection (slower, longer clauses with ellipses).
- **Character Voices (if applicable)**: Use audio tags to shift delivery:
  `[whispers]` for secrets, `[angry]` for conflict, `[sad]` for loss.
- **Chapter Breaks**: Use `<break time="2.0s" />` (v2/v2.5) or `[long pause]` (v3)
  between scenes.

### C. Podcast Intro / Promo (30-60s)
- **Identity Line (0:00-0:05)**: Show name + host name. Confident, direct.
- **Episode Tease (0:05-0:25)**: What's in this episode. One compelling fact.
- **Value Proposition (0:25-0:45)**: Why the listener should stay.
- **Call to Action (0:45-0:60)**: Subscribe, follow, or visit. Specific, not generic.

### D. Product Demo / Announcement (1-3 min)
- **Problem Statement (0:00-0:20)**: The pain point. Relatable language.
- **Solution Reveal (0:20-0:40)**: Product name + one-sentence value prop.
- **Feature Walkthrough (0:40-2:00)**: 3 features max. Benefits, not specs.
- **Proof / Social (2:00-2:30)**: One testimonial or metric.
- **CTA (2:30-3:00)**: Exact action. "Go to [URL]." (normalized for speech)

---

## 3. TTS Text Normalization (Non-Negotiable)

TTS models mispronounce numbers, symbols, dates, and abbreviations.
**Normalize ALL of these in the script before adding audio tags.**

### Normalization Table

| Raw Input | Spoken Form | Example |
|-----------|-------------|---------|
| `$42.50` | forty-two dollars and fifty cents | `$99.99` → ninety-nine dollars and ninety-nine cents |
| `£1,001.32` | one thousand and one pounds and thirty-two pence | |
| `€100` | one hundred euros | |
| `¥1000` | one thousand yen | |
| `1234` | one thousand two hundred thirty-four | Expand all bare numbers > 20 |
| `3.14` | three point one four | |
| `555-555-5555` | five five five, five five five, five five five five | Phone numbers digit-by-digit |
| `2nd` | second | All ordinals |
| `XIV` | fourteen | Roman numerals ("the fourteenth" if a title) |
| `⅔` | two-thirds | |
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
| `npm` | N-P-M | Package managers as letters |
| `JSON` | J-son or "Jay-sawn" | Choose the pronunciation you want |

### Code & Technical Content
- **Code snippets**: Read as spoken descriptions, not literal syntax.
  - Bad: `const x = useState(0)`
  - Good: "const x equals use state zero"
- **File paths**: Spell separators. `src/components/Button.tsx` → "src slash
  components slash button dot tee-ess-ex"
- **Git commands**: `git commit -m "fix"` → "git commit dash m fix"
- **Regex**: `/^[a-z]+$/i` → "slash caret a through z plus dollar slash i"

---

## 4. Pronunciation Control

### Phonetic Spelling
If a word is consistently mispronounced by your chosen voice, respell it
phonetically in the script.

- Example: "trapezIi" to emphasize the "ii"
- Example: "Kubernetes" → "koo-ber-net-ees" if the voice struggles

### Capitalization for Emphasis (v3)
Capital letters increase emphasis in Eleven v3:
- "It was a VERY long day."
- "This is NOT a drill."

### Phoneme Tags (v2 / Flash v2 only)
For precise pronunciation of specific words, use SSML phoneme tags:
```xml
<phoneme alphabet="cmu-arpabet" ph="P R AH0 N AH0 N S IY EY1 SH AH0 N">
  pronunciation
</phoneme>
```

**Note**: Phoneme tags only work with Eleven Flash v2 and Eleven English v1.
Multilingual v2 and v3 do NOT support phoneme tags.

---

## 5. Pause & Pacing Control

### For Eleven v2 / v2.5 / Flash v2 Models
Use `<break time="x.xs" />` for natural pauses up to 3 seconds.

```
"Hold on, let me think." <break time="1.5s" /> "Alright, I've got it."
```

**Caution**: Too many break tags in one generation causes instability (speedups,
artifacts). Use 1-2 per short script, 2-3 per long script. Prefer punctuation
pauses instead.

### For Eleven v3 Models
v3 does NOT support `<break>`. Use:
- **Ellipses** for hesitation: `It was... a mistake.`
- **Capitalization** for emphasis: `It was a VERY long day.`
- **Punctuation** for rhythm: commas, periods, dashes
- **Audio tags** for breath/pause: `[short pause]`, `[long pause]`, `[exhales]`, `[sighs]`

### General Pacing Guidelines
1. **Short sentences** are more intelligible in TTS than complex compound sentences.
2. **One idea per sentence** — especially important for technical content.
3. **Paragraph breaks** create natural breathing room. Don't cram everything
   into one block.
4. **Vary sentence length** to avoid robotic cadence. Short. Then a bit longer.
   Then short again.

---

## 6. Audio Tags for Expressive Delivery

For Eleven v3 (or tag-aware TTS models), inject audio tags to control emotion
and non-verbal delivery. **Tags must describe auditory actions only.**

### Tag Categories

**Emotional Directions:**
`[happy]`, `[sad]`, `[excited]`, `[angry]`, `[whisper]`, `[annoyed]`,
`[appalled]`, `[thoughtful]`, `[surprised]`, `[sarcastic]`, `[curious]`,
`[mischievously]`, `[professional]`, `[reassuring]`, `[frustrated]`, `[delighted]`,
`[nervously]`, `[cautiously]`, `[cheerfully]`, `[quizzically]`, `[elated]`,
`[deadpan]`, `[dramatically]`, `[dismissive]`, `[impressed]`, `[warmly]`

**Non-Verbal Sounds:**
`[laughs]`, `[laughs harder]`, `[starts laughing]`, `[chuckles]`, `[giggles]`,
`[giggling]`, `[groaning]`, `[sighs]`, `[exhales]`, `[exhales sharply]`,
`[inhales deeply]`, `[clears throat]`, `[short pause]`, `[long pause]`,
`[wheezing]`, `[snorts]`, `[gasps]`, `[muttering]`, `[happy gasp]`

**Sound Effects (use sparingly):**
`[gunshot]`, `[applause]`, `[clapping]`, `[explosion]`, `[swallows]`, `[gulps]`,
`[record scratch]`, `[binary beeping]`

**Overall Direction (scene context):**
`[football]`, `[wrestling match]`, `[auctioneer]`, `[news broadcast]`,
`[podcast studio]`, `[hacker den]`, `[library]`, `[classroom]`

### Tag Placement Rules

1. **Before the line** for global mood: `[sarcastic] Oh, you thought this was easy?`
2. **After the line** for reaction: `Another framework. [sighs]`
3. **Inline** for mid-sentence shifts: `It was working [excited] until it wasn't. [sighs]`
4. **At the start of a scene** for ambient context: `[podcast studio]` or `[library]`
5. **Do NOT** turn narrative descriptions into tags. If the text says "He laughed
   loudly," add a tag: `He laughed loudly [chuckles].`
6. **Do NOT** use non-auditory tags: `[standing]`, `[grinning]`, `[pacing]`, `[music]`

### Tag Density Guidelines

| Content Type | Tag Count | Guidance |
|--------------|-----------|----------|
| Explainer / Tutorial | 4-8 tags | One tag per major section or emotional beat |
| Audiobook / Story | 10-20 tags | Higher density for character emotion and scene shifts |
| Podcast Intro | 2-4 tags | Confidence and energy tags for the hook |
| Product Demo | 3-6 tags | Enthusiasm for features, professionalism for specs |
| Meditation / Calm | 4-6 tags | Soft tags: `[whisper]`, `[softly]`, `[gently]` |

### Fish Audio S2 / S2.1-Pro Tags

Fish Audio uses `[square bracket]` natural-language emotion cues. The tag set is **not fixed** — any descriptive expression like `[whispers sweetly]` or `[laughing nervously]` works.

**Sample emotions:** `[happy]`, `[sad]`, `[angry]`, `[excited]`, `[calm]`, `[nervous]`, `[confident]`, `[surprised]`, `[scared]`, `[worried]`, `[frustrated]`, `[empathetic]`, `[embarrassed]`, `[disgusted]`, `[proud]`, `[curious]`, `[sarcastic]`, `[determined]`, `[bored]`, `[confused]`, `[anxious]`
**Tones:** `[whispering]`, `[shouting]`, `[screaming]`, `[soft tone]`, `[in a hurry tone]`
**Sounds:** `[laughing]`, `[chuckling]`, `[sobbing]`, `[crying loudly]`, `[sighing]`, `[groaning]`, `[panting]`, `[gasping]`, `[yawning]`, `[snoring]`
**Pauses:** `[break]` (short), `[long-break]` (extended)
**No SSML support.** Use `[break]` for pauses instead.

### xAI Grok Voice Tags

Grok supports **inline** `[tag]` at specific points and **wrapping** `<tag>text</tag>` for delivery style.

**Inline tags:** `[pause]`, `[long-pause]`, `[hum-tune]`, `[laugh]`, `[chuckle]`, `[giggle]`, `[cry]`, `[tsk]`, `[tongue-click]`, `[lip-smack]`, `[breath]`, `[inhale]`, `[exhale]`, `[sigh]`
**Wrapping tags:** `<whisper>text</whisper>` · `<shouting>text</shouting>` · `<sing>text</sing>` · `<hum>text</hum>` · `<narrate>text</narrate>` · `<fast>text</fast>` · `<slow>text</slow>`

---

## 7. Model Selection Quick Guide

| Model | Provider | Best For | Audio Tags | Break Tags |
|-------|----------|----------|------------|------------|
| Eleven v3 | ElevenLabs | Expressive narration, character voices | Yes¹ | No |
| Multilingual v2 | ElevenLabs | Natural speech, multiple languages | No | Yes³ |
| S2.1-Pro-Free | Fish Audio | Free TTS (free till Jul 2026) | Yes² | No⁴ |
| S2-Pro | Fish Audio | Premium expressive TTS | Yes² | No⁴ |
| Grok Voice | xAI | Expressive + custom voices | Yes⁵ | Yes⁵ |

¹ v3 uses `[bracket]` tags — no SSML `<break>` support.  
² Fish uses `[bracket]` natural-language cues. `[break]`/`[long-break]` for pauses.  
³ Supports SSML `<break time="x.xs" />`. No bracket audio tags.  
⁴ Fish uses `[break]`/`[long-break]` instead of SSML `<break>`.  
⁵ xAI supports inline `[tag]` + wrapping `<tag>text</tag>`.

**Recommendation**: Use Eleven v3 for character-driven or expressive content.
Use Fish S2.1-Pro-Free for budget-friendly expressive TTS. Use Grok Voice when
inline emotion tags and custom voice cloning are needed.

---

## 8. Output Format

Deliver the final script in this structure:

```markdown
# [Title] — TTS Script

## Metadata
- **Content Type**: [Explainer / Audiobook / Podcast / Demo / etc.]
- **Target Duration**: [e.g., 3-5 minutes]
- **TTS Model**: [Eleven v3 / Fish S2.1-Pro / xAI Grok / Multilingual v2]
- **Voice**: [Voice name or description]
- **Audio Tags**: [count]

## Normalized Voiceover Script

[Paste the fully normalized, tag-enhanced script here.]

[Use paragraph breaks for natural breathing room.]

## Pronunciation Notes
- "React": ree-act (not ray-act)
- "Kubernetes": koo-ber-net-ees
- [Any other words that need explicit direction]

## Post-Production Notes (optional)
- Speed adjustment: [1.0x / 1.15x / 1.25x]
- Background music: [genre / tempo / volume relative to voice]
```

---

## 9. Anti-Patterns (NEVER Do)

1. **Leaving raw symbols in script** — `$100`, `API`, `2024-01-01`, `Ctrl+Z` must
   be normalized.
2. **Long run-on sentences** — TTS drifts on complex clauses. Break them up.
3. **No audio tags on v3** — Flat TTS sounds robotic on expressive models.
4. **Non-auditory tags** — `[grinning]`, `[pacing]`, `[music]` will be spoken or ignored.
5. **Too many `<break>` tags** — Causes instability (speedups, artifacts). Max 2-3.
6. **Using `<break>` with v3** — v3 does not support SSML break tags.
7. **Inconsistent pacing** — Avoid monotone sentence length. Vary short and long.
8. **Generic CTAs** — "Thanks for watching" and "like and subscribe" are lazy.
   Write topic-specific closings.
9. **Ignoring model capabilities** — Don't use phoneme tags with v3 or
   Multilingual v2. They won't work.
10. **Writing for the eye** — Read the script aloud (or imagine it spoken) before
    delivering. If it sounds awkward, rewrite it.

---

## 10. Quality Checklist

Before delivering the script, verify:

- [ ] All numbers, symbols, dates, abbreviations normalized for speech
- [ ] Acronyms spelled out or phonetically guided
- [ ] Audio tags are auditory-only (no `[grinning]`, `[music]`)
- [ ] Audio tags placed strategically before / after / inline
- [ ] Tag density appropriate for content type
- [ ] Sentences vary in length (not all short, not all long)
- [ ] Paragraph breaks create natural breathing room
- [ ] No raw code syntax — all technical content spoken-out
- [ ] Pronunciation notes included for ambiguous terms
- [ ] Model-appropriate pause control (`<break>` for v2, `[break]/[long-break]` for Fish, ellipses/tags for v3)
- [ ] Phoneme tags only used with compatible models (Flash v2, English v1)
- [ ] CTA or closing is specific to the topic (not generic)
- [ ] If using Fish Audio: uses `[break]`/`[long-break]` for pauses, no SSML
- [ ] If using xAI Grok: inline `[pause]`/`[long-pause]` or wrapping tags as appropriate
