---
name: fireship-video-style
description: >
  Creative direction skill for producing video shorts in the signature style of
  the YouTube channel Fireship (https://youtube.com/@Fireship). Use this skill
  when the user wants to create fast-paced, high-energy, intentionally-edited
  tech explainer videos, code tutorials, or tech news briefs that feel natural
  and binge-worthy — NOT dry or corporate. This skill provides creative
  direction for scripts, visual design, pacing, editing rhythms, tone of voice,
  and thumbnail strategy. Applicable for any topic that would benefit from
  dense information delivery with deadpan humor, meme inserts, and rapid visual
  cuts. Covers "X in 100 Seconds" explainers, "The Code Report" news briefs,
  and general Fireship-style shorts.
license: Complete terms in LICENSE.txt
---

# Fireship-Style Video Creative Direction

Use this skill when generating creative briefs, video scripts, storyboards,
editing directions, or thumbnail concepts for short-form tech explainer videos.
The goal is to replicate the **intentional, natural, high-density** style of
Fireship — not to create generic tutorial content.

## Core Philosophy

Fireship's style is **"respect the viewer's time by entertaining them first"** —
information sticks because it's delivered with humor, speed, and perfectly-timed
visual punches. Entertainment is not a garnish; it is the delivery mechanism.
The videos feel fast because they ARE fast, not because they were sped up in
post. Meme density is high. Information density is sky-high. Deadpan sarcasm
and programmer-humor are non-negotiable. The result is content that educates
because it entertains — not despite it.

**Golden rule**: If a frame doesn't entertain, teach, or transition — cut it.
Entertainment beats completeness. A 90-second video with 8 memes and 3 core
concepts beats a 120-second video with 12 concepts and 2 memes.

---

## Visual Identity System

### Color Palette
| Role | Value | Usage |
|------|-------|-------|
| Background | `#0a0a0a` or `#111111` | Primary video background, thumbnails |
| Surface | `#1a1a1a` or `#222222` | Cards, panels, code blocks |
| Primary Text | `#ffffff` | Headlines, main body |
| Secondary Text | `#a1a1aa` | Captions, metadata, asides |
| Accent | `#ff6b35` (flame orange) | CTAs, highlights, brand moments |
| Code Accent | `#58d68d` (mint) | Syntax highlights, success states |
| Alert | `#ef4444` (red) | Errors, warnings, dramatic moments |
| Tech Blue | `#3b82f6` | Links, tech logos, secondary accents |

### Typography
- **Headlines/Titles**: Bold, blocky, all-caps or pixel-art aesthetic. Heavy
  weight (800+). Think "100 SECONDS OF CSS" — chunky, slightly retro.
- **Body/Explanation**: Clean sans-serif (Inter, Roboto, or system). White on
  dark. Readable at speed.
- **Code**: Monospace, syntax-highlighted (typically Dracula or One Dark
  theme). Cursor movement visible.
- **Meme Text**: Impact font or standard meme caption style (white text, black
  outline, centered).

### Background Rules
- **Default**: Solid near-black (`#0a0a0a`). Never use gradients as primary
  background.
- **Code demos**: Full-screen terminal/editor with dark theme. Cursor should be
  visible and active.
- **News/title cards**: Can use subtle texture or colored band at top
  (Fireship uses a bright blue bar for "100 SECONDS OF" series).
- **Meme inserts**: Full-screen image/GIF with text overlay, no background
  treatment needed.

---

## Video Structure & Pacing

### Duration Targets
| Format | Length | Use Case |
|--------|--------|----------|
| "X in 100 Seconds" | 95-105s | Technology/language explainer |
| Shorts/Reels | 30-60s | Quick tip, one concept, meme moment |
| The Code Report | 4-6 min | News story, tech event breakdown |
| Deep Dive | 8-12 min | Tutorial with multiple sections |

**"100 Seconds" is a promise, not a suggestion.** Script to ~95s, leaving 10s
buffer. If content doesn't fit, cut concepts — do not exceed 105s. The brand
is the constraint.

### Beat Sheets by Format

#### "X in 100 Seconds" (95-105s, ~20 shots)
- **0:00-0:03**: Cold open — immediate hook. Provocative definition.
- **0:03-0:08**: Title card. Blue bar: "100 SECONDS OF". Below: blocky topic
  name + tech logo.
- **0:08-0:35**: What it IS + first core concept. Code demo starts immediately.
- **0:35-0:50**: The gotcha / common mistake. Meme insert.
- **0:50-1:15**: Second concept / practical example. Quick code snippet.
- **1:15-1:35**: Ecosystem mention or one-sentence analogy.
- **1:35-1:50**: "That's [Topic] in 100 seconds" + wrap.
- **1:50-2:00**: Outro in topic syntax.

#### "The Code Report" (4-6 min, ~40-50 inserts)
- **0:00-0:05**: Newsreel title: "THE CODE REPORT" + date stamp.
- **0:05-0:20**: Hook. "In case you missed it, [Company] just [shocking thing]."
- **0:20-1:30**: Background + what happened. Screenshots, timeline.
- **1:30-2:30**: Technical implications. Code examples, architecture.
- **2:30-3:30**: Community reaction. Tweet screenshots, Reddit threads, memes.
- **3:30-4:30**: Analysis / honest take. Practical advice.
- **4:30-5:00**: Outro in relevant syntax.

#### Shorts (30-60s, ~12-18 shots)
- **0:00-0:02**: Text hook on screen. Big text, no voice yet.
- **0:02-0:05**: Voice enters with provocative statement.
- **0:05-0:55**: Rapid tips/demos. Hard cut between each.
- **0:55-1:00**: Meme + outro text.

### Pacing Rules
1. **Average shot length**: 2-4 seconds. Never hold a static frame longer than
   5 seconds unless it's a dramatic beat.
2. **Jump cuts**: Aggressive but invisible. Cut out every breath, every pause,
   every "um". The narrator should sound slightly breathless in a good way.
3. **Speed ramps**: Narration can be recorded at normal pace and compressed
   to ~1.15-1.25x in post. OR recorded intentionally fast. Either way, the
   result is urgent but still intelligible.
4. **Transitions**: Hard cuts 90% of the time. Occasional quick zoom (push
   in) for emphasis. No dissolves, no fancy transitions.
5. **Information density**: Every sentence should contain a fact, a joke, or
   a transition. No filler.

---

## Narration Voice & Tone

### Character
The narrator is the **senior dev who has seen it all** — knowledgeable,
slightly cynical, secretly enthusiastic. Speaks like you're pair-programming
at 2am. Not a corporate presenter. Not a hype beast. Smart, dry, fast.

### Humor Types (use liberally)
1. **Niche/insider jokes**: Reference the actual framework that dropped last
   week, the bug everyone is complaining about on GitHub, or the deprecated
   API that broke production. Specificity > generality. "There's a new
   JavaScript framework this week" only works if it's actually true.
2. **Self-deprecating**: "I have the personality of a carrot" (actual Fireship
   quote). Acknowledge absurdity of tech culture. "I spent 3 hours debugging
   this. It was a semicolon."
3. **Meme references**: Reaction images, GIFs, viral clips at punchline moments.
   Use memes from the last 6-12 months for maximum recognition.
4. **Sarcastic asides**: "Oh, you thought CSS was easy? That's adorable."
   "Another year, another build tool that will definitely solve everything."
5. **Programming-language puns**: Outros in code syntax. Variable names as
   jokes. Function names that are too honest (`function probablyBreaks()`).
6. **Tech culture commentary**: Mock the absurdity of tech marketing,
   vaporware announcements, or "we're so back / it's joever" cycles.

**Test for humor quality**: If the joke could appear in a corporate deck,
rewrite it. If only 10% of viewers get it, it's probably perfect.

### Delivery Notes
- Speak in **short sentences**. One idea per breath.
- Use **imperative mood**: "Install it. Import it. Break it."
- **Contrast for humor**: Serious technical explanation → absurd meme.
- **Deadpan**: The funnier the content, the more serious the delivery.
- No verbal filler: "so", "basically", "you know", "kind of" — all removed in edit.
- **Forbidden words**: "Welcome", "guys", "today we're going to", "in this video",
  "let's get started", "before we begin", "as you can see".

---

## Visual Insert Types

| Insert | Timing | Purpose |
|--------|--------|---------|
| **Title Card** | 0:03-0:08 | Establish topic with bold typography + tech logo |
| **Code Recording** | 15-20s bursts | Show actual implementation, cursor movement, live typing |
| **Terminal Output** | 3-5s | Show command results, error messages, success confirmations |
| **Meme/GIF** | 1.5-4s at punchline | Comedic relief, emotional reaction, audience proxy |
| **Flash Insert** | 0.5-1.5s | Sub-2-second meme flash. Barely registers, rewards rewatching. |
| **Screenshot/Web** | 5-8s | Show real websites, documentation, GitHub repos |
| **Diagram/Graphic** | 5-10s | Explain architecture, data flow, comparisons |
| **Face Cam** | Optional, corner | Small overlay during explanation; disappear for code demos |
| **"Like & Subscribe"** | Outro 5s | Written in topic-relevant code syntax on dark background |

### Meme Insert Rules
- **Density by format**:
  - "100 Seconds": 5-8 memes or reaction inserts
  - Shorts: 3-5 memes
  - Code Report: 10-15 memes
- Memes should feel **earned** — not random. They punctuate a technical point.
- **Variety rule**: Never use the same meme format more than twice per video.
  Mix reaction memes, tech-specific memes, and pop culture GIFs.
- **Stacking**: Back-to-back meme cuts (2-3 memes in 4 seconds) work for
  rapid-fire reactions or "mood progression" sequences.
- Reaction images (confused face, shocked face, crying face) work best.
- Tech-specific memes ("it works on my machine", "javascript fatigue",
  "recursion meme") get the best engagement.
- **Flash inserts**: Sub-2-second meme flashes that barely register on first
  watch but reward rewinding. Use for subtle comedic layering.
- Duration: 1.5-3 seconds for standard; 0.5-1.5s for flash.

---

## Motion & Animation Specs

Fireship motion is **snappy, not smooth**. Avoid ease-in-out or linear
movement for UI elements. Everything should feel like it snaps into place.

| Animation | Duration | Easing | Notes |
|-----------|----------|--------|-------|
| Hard cut | 0 frames | none | Default. 90% of transitions. |
| Quick zoom (push in) | 8-12 frames | `cubic-bezier(0.22, 1, 0.36, 1)` | For emphasis on code/error. Scale 1.0 → 1.15 |
| Quick zoom (pull out) | 8-12 frames | `cubic-bezier(0.22, 1, 0.36, 1)` | For reveals. Scale 1.15 → 1.0 |
| Horizontal swipe | 6-8 frames | `cubic-bezier(0.33, 1, 0.68, 1)` | Topic changes only. Rare. |
| Flash beat | 1-2 frames | none | White/accent flash for major reveals. |
| Text pop-in | 4-6 frames | `cubic-bezier(0.34, 1.56, 0.64, 1)` | Title cards, stat reveals. Slight overshoot. |
| Cursor blink | 530ms cycle | step | Visible, natural cursor in code recordings. |

**Rules**:
- No fade transitions. No dissolve. No crossfade.
- No motion blur on UI elements.
- No smooth/linear camera moves. Jerky is better than floaty.
- Zooms should feel punchy — arrive fast, settle with a tiny overshoot.

---

## Thumbnail Design

### Composition
- **Background**: Near-black or very dark gradient.
- **Subject**: Dramatic face/expression OR large tech logo (center or right).
- **Text**: 3-6 words max. Huge, bold, high contrast (white or orange on dark).
  Slightly tilted or with subtle shadow for depth.
- **Accent**: Fireship orange (`#ff6b35`) for emphasis words.
- **Branding**: Small Fireship-style flame icon or no logo (the style IS the brand).

### Text Formulas
- "[Topic] just changed everything"
- "[Technology] in 100 Seconds"
- "[Number] [Topic] tips"
- "[Shocking statement]..."
- "You don't know [Topic]"

### Mood
Urgent, slightly alarmist, curiosity-gap. NOT clickbait-lies. The video
actually delivers what the thumbnail promises.

---

## Series Format Templates

### "X in 100 Seconds"
- Title: "[Topic] in 100 Seconds"
- Length: 95-105 seconds (hard cap)
- Structure: Definition → Core concept → Code snippet → One gotcha → Outro in
  topic syntax
- Visual: Blue title bar + bold topic name + tech logo
- Tone: Fastest, most compressed. No time for deep jokes — just quick wit.
- Meme target: 5-8 inserts

### "The Code Report"
- Title: "[News event] // The Code Report"
- Length: 4-6 minutes
- Structure: Hook → Background → The news → Technical implications → Community
  reaction → Takeaway → Outro
- Visual: Newsreel title card with date. More screenshots and web content.
- Tone: Journalistic but sarcastic. Like a hacker's evening news.
- Meme target: 10-15 inserts

### General Explainer / Short
- Length: 30-90 seconds
- Structure: Problem → Solution → Demo → Meme → CTA
- Visual: Code-heavy, fast cuts, meme inserts
- Tone: Helpful but roasted. "Here's why you're doing it wrong."
- Meme target: 3-5 inserts

---

## Audio & Music

### Music
- Upbeat, electronic, slightly tense background track.
- Volume: -20dB to -25dB relative to voice. Audible but not competing.
- Tempo: 120-140 BPM. Driving rhythm that matches the fast cuts.
- Style: Synthwave, lo-fi electronic, or modern chiptune. No corporate
  elevator music.

### Sound Design
- **Keyboard clicks**: Subtle, during typing sequences.
- **Notification sounds**: For "success" moments, compiles, deployments.
- **Error buzz**: For bugs, failures, deprecated features.
- **Whoosh/Swoosh**: Very rare — only for major scene transitions.
- **Silence**: Used as a comedic beat. Dead silence after a bad take or
  absurd statement.
- **Record scratch**: For abrupt "nope" moments or when a take goes wrong.

### Voice Treatment Chain
1. Remove breaths, ums, dead space
2. Compress (2:1 ratio, -18dB threshold)
3. EQ: slight high-mid boost (+2-3dB at 3-5kHz) for clarity
4. Optional: speed to 1.15-1.25x if narration feels slow
5. Limit to -3dB peak
6. No reverb — dry, direct, intimate

---

## Editing Rhythm Patterns

### Standard Pattern (use most often)
```
[Voice starts] → [Code appears] → [Voice explains] → [Result shows] →
[Meme insert] → [Hard cut] → [Next concept]
```

### Punchline Pattern
```
[Setup: serious explanation] → [Pause 0.5s] → [Meme: reaction face] →
[Voice continues dryly]
```

### Reveal Pattern
```
[Problem stated] → [Quick zoom in on code] → [Typing animation] →
[Success output] → [Voice: "That's it."]
```

### News Pattern (Code Report)
```
[Title card with date] → [Screenshot of source] → [Voice summarizes] →
[Code context] → [Tweet/reaction screenshot] → [Meme reaction] →
[Analysis] → [Outro]
```

### Meme Stack Pattern
```
[Setup] → [Meme A: 1s] → [Hard cut] → [Meme B: 1s] → [Hard cut] →
[Meme C: 1.5s] → [Voice: "Anyway..."]
```

---

## Anti-Patterns (NEVER Do)

1. **"Hey guys, welcome back" intros** — Fireship has no intro. Start immediately.
2. **Slow, measured explanations** — If it feels relaxed, it's wrong.
3. **No memes or humor** — Pure technical content feels like a lecture.
4. **Light/white backgrounds** — Dark mode only. This is non-negotiable.
5. **Gradient backgrounds** — Solid dark. Gradients feel dated.
6. **Corporate voice** — No "we're excited to announce". Be real.
7. **Long static screenshots** — If it's not moving or being narrated actively,
   cut it.
8. **Generic thumbnails** — Must have bold text, emotion, or strong visual hook.
9. **Fade transitions** — Hard cuts only. Fades feel slow.
10. **Over-produced graphics** — Code is the star. Don't add motion graphics
    that don't serve the explanation.
11. **Prioritizing completeness over entertainment** — A complete but boring
    video fails. Cut concepts before you cut jokes.
12. **Running long to fit everything** — The format is the constraint. Edit
    ruthlessly. If it doesn't fit, it doesn't belong.

---

## Topic Adaptation Guide

This style works for ANY topic that benefits from dense explanation:

| Topic Type | Adaptation |
|------------|------------|
| Programming language/framework | "X in 100 Seconds" format |
| Tech news / product launch | "The Code Report" format |
| Tutorial / how-to | Compressed tutorial with meme beats |
| Comparison / vs | Side-by-side code, snarky commentary |
| Concept explanation | Analogies + code + reaction meme |
| Tool review | Quick demo, honest verdict, one-liner outro |

The style is **not** limited to programming. Any technical, analytical, or
knowledge-work topic can use this rhythm: fast facts, dry humor, visual
punchlines, respect for the viewer's intelligence.

---

## Quality Checklist

### Production Rigor
- [ ] Hook happens in the first 3 seconds (no logo intro)
- [ ] Average shot length under 4 seconds
- [ ] Background is dark (`#0a0a0a` or similar)
- [ ] Code/demo content is at least 40% of the runtime
- [ ] Outro uses topic-relevant syntax (not generic "like and subscribe")
- [ ] Thumbnail has bold text + emotional/visual hook + dark background
- [ ] No filler words or dead air in the script
- [ ] Information density: every sentence teaches or entertains

### Entertainment Value (mandatory — do not skip)
- [ ] Meme density meets format target (100s: 5-8, Shorts: 3-5, Code Report: 10-15)
- [ ] At least one sarcastic or self-deprecating moment
- [ ] No joke could appear in a corporate deck (test: "Would I send this to a dev friend?")
- [ ] At least one flash insert (sub-2s meme) for rewatch value
- [ ] No "forbidden words" (welcome, guys, today we're going to, in this video)
- [ ] Narrator delivery notes include deadpan / sarcastic tone markers
- [ ] If the script feels "complete" but not funny, cut concepts and add memes

---

## Resources

- `references/fireship-style-deep-dive.md` — Extended analysis with frame-by-frame
  breakdowns of iconic Fireship videos and common editing patterns.
- `references/color-typography-cheatsheet.md` — Quick-reference for visual specs.
