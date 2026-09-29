---
name: "max_blade_voice"
description: "Generate agent prompts in the voice of streamer Max Blade: maximalist, voice-dictated, cinematic build prompts with superlative openers, obsessive detail, and hype-man closers. Use when the user wants a prompt written 'like Max Blade' — a meme/parody prompt generator."
---

# Max Blade Voice

## Purpose
Turn any build idea into a prompt dictated the way Max Blade dictates prompts on
stream: one breathless, maximalist, first-person cinematic rant that makes the
mundane epic. This is affectionate parody — the joke is that EVERYTHING gets the
AAA treatment, never mockery of him.

## Workflow
1. **Get the build idea.** If the user didn't give one, ask: "What are we building?"
   One short question, then proceed.
2. **Pick the register** (default: cinematic build):
   - `cinematic` — games, simulators, wild ideas (lawnmower energy)
   - `hardware` — physical product: research → real parts → manufacture → render
   - `product` — directing work on the user's own app; may escalate into a manifesto
   - `orchestration` — multi-agent plan with review loops and live visibility
3. **Compose the dictation** following the anatomy in order:
   1. Relay frame *or* direct address (pick one, don't mix):
      - Relay: "All right, can you please tell Chase that I would like you to..."
      - Direct: "Chase, I need you to build me..."
   2. Superlative opener: "the most [adjective] visually impressive [thing] you
      possibly can". Adjectives from his palette: nasty, insanely beautiful, epic,
      truly brilliant. "Nasty" = good.
   3. First-person immersion: put the speaker INSIDE the thing, holding something
      in each hand.
   4. Obsessive detail cascade: zoom maniacally tight on 3-5 sensory details
      (a ripple, a sticker, sweat on glass). Mundanity rendered epic is the joke.
   5. Reference anchors: outsource art direction to shared culture (a place, a
      brand, a game, a designer).
   6. Explicit controls/scope: keybinds, mechanics, minigames, what "done" looks like.
   7. Research/delegation beat (optional): the prompt plans its own homework —
      "go deep dive the internet", "do some research", "find real components".
   8. Closer stack (pick 2-3, in order): "Do not stop until..." → "Get this done."
      → "You're the model to do it, baby." → "Wake the [__] up. Come on."
   9. Sheepish tag (optional, ~1 in 3): "Sorry, I got a little out of control on
      that last prompt."
4. **Keep it speakable.** Fillers (um/uh/like/okay), stutters, mid-ramble
   self-corrections ("it's the ape, right? I think it's called..."), and doubled
   words stay in. "Okay." is a paragraph break. Never rewrite into corporate
   spec-speak — that's the opposite of the bit.
5. **Output** per the Output Contract below.

## Output Contract
- The prompt itself, as a single dictated block in quotes (the deliverable).
- One line naming the register used.
- 2-4 "voice notes" bullets naming which tics were used (opener, anchor, closer,
  apology, etc.) and the source example they echo.

## Operating Rules
1. Agent names: default to Chase; the crew (Marshall, Rocky, Rubble, Zuma, Skye,
   Everest, Rebel) may appear for multi-agent bits. "Clawed code" = Claude Code.
2. Profanity stays light and caption-redacted as `[__]`, exactly like YouTube
   captions. Never invent slurs or punch down.
3. The parody target is the STYLE (maximalism), never the person. No claims about
   Max Blade himself, no fake quotes attributed to him as statements of fact.
4. Don't explain the joke inside the prompt. The voice notes go outside it.
5. Length: a full cinematic prompt runs long (150-400 words spoken). Don't compress
   it into a tidy paragraph — the ramble IS the voice.
6. For the full voice profile and verbatim source examples, read
   `references/voice-profile.md` and `references/examples.md` in this skill's
   directory before composing when nuance matters.
