---
name: MaxBlade parody prompt
description: >-
  use this when writing or directing MaxBlade-style parody agent prompts
  (vibe-coding streamer energy, list accretion, alien delivery scale) — meme
  imitation of structure and tone, not claiming to be him or chasing his results
---
# MaxBlade parody prompt

Write **meme-imitation** prompts and delivery direction in MaxBlade’s streamer-prompt style: soft open → agent handoff → absurd list/detail accretion → AAA/perfection close → optional pep nuke → optional post-nuke grin.

Not for: claiming to *be* MaxBlade, cloning his voice without consent context, or “get the same results he gets.” Personality, verbosity, and phrasing only.

**Companion files (read when needed):**
- `references/alien-scale.md` — full 1–10 scale + seed notes
- `references/fingerprints.md` — how to detect a prompt dump vs chat fluff
- `references/seed-scan-summary.json` — dump windows + top pattern counts
- `references/CORPUS.md` — where the heavy transcript research lives
- `examples/lawnmower-dump-annotated.md` — gold dump with level tags
- `examples/ad-escalation-beat.md` — $5M marketer escalation beat

## Inputs to gather (if missing)
- Target product ask (sim, game, ad, tool)
- Alien delivery level **1–10** (default **8.5** for a full dump; **4–5** for chat bumpers; **1–2** for ops-only)
- Whether TTS will speak it (if yes, keep fillers; tip to 9 only on the last pep line)

## Pattern rules (do these — don’t paste fixed catchphrases)

1. **Soft open → agent handoff → dump** — polite UI please, then “tell/spawn [agent]…”, then the rant.
2. **List / detail accretion** — keep stacking “I want / I need / and…” until absurd. Prefer concrete nouns and micro-detail (materials, SKUs, barcodes, sections) over vague adjectives alone.
3. **Triple-A / photoreal as a grade** — AAA / photorealistic / beyond-AAA is a quality ceiling, not a genre label.
4. **Sensory first, controls late** — hands, sweat, smoke, fabric ripple, grass cut; WASD / Q / E as afterthoughts.
5. **Intensity close** — “do not stop until…” perfect / playable / brilliant; rare triple “beyond, beyond, beyond.”
6. **Pep nuke (short)** — wake / lock in / creatinated·caffeinated / psychotic coach energy / come on / baby / let’s go — burst, not a paragraph.
7. **Post-nuke meta grin** — sorry / ahead of myself / a little out of control / not gonna lie.
8. **Fillers are load-bearing** — um / uh / okay / like / repeated “I want.” Cleaning them flattens the bit.
9. **Praise sandwich** — “you’re incredible/amazing” only as a bridge into the next ask.
10. **Ambition framing** — world’s-first vibe-coded X, overnight N sub-agents, alien technology, AI-psychosis rabbit hole (use sparingly).
11. **Marketer escalation** (when relevant) — features → emotional pain-point ad that “looks like a $5M director team.”

## Alien delivery scale (TTS / read-aloud)

| Level | Register | When |
|------|----------|------|
| 1–2 | Flat ops / soft please | Canvas, open agent, short UI |
| 3 | Warm affirm bridge | Praise → next ask |
| 4–5 | House DJ / lock-in coach | Chat pep, cold open, “lock in / wake” |
| 6–7 | Spec stack → cinematic/SKU fetish | Main dump body |
| 8 | AAA / beyond / don’t-stop climax | End of dump before pep |
| 9 | Pep nuke | Last 1–2 sentences only |
| 10 | Post-nuke grin | After the dump lands |

**Default full parody prompt:** arc **3 → 6 → 8 → tip 9 → optional 10**.  
**Anti-patterns:** calm narrator at 8–9; sad/calm emotion tags on hype text; summarizing accretion into tidy bullets; level-9 for the whole body.

Details and seed evidence: `references/alien-scale.md`.

## Output shape

Produce, in order:

1. **Ops prelude** (1–3 short lines, level 1–3) — optional if user only wants the dump.
2. **Agent handoff line** — tell/spawn named agent to build…
3. **Accretion dump** (level 6–8) — one spoken paragraph (or few), stacked wants, fillers kept.
4. **Close** — don’t-stop / perfect / AAA grade.
5. **Pep nuke** (level 9, short) — optional.
6. **Meta grin** (level 10) — optional one-liner.

If the user asked for **TTS steering**, also give:
- target level number
- engine-agnostic notes (speed ~1.15–1.25 at 8–9; CAPS only on close; no freeform director essay unless the engine supports it)

Before shipping a dump, skim `examples/lawnmower-dump-annotated.md` as a structure check (do not copy it verbatim).

## Quick quality check
- ≥3 stacked “I want/I need/and” clauses OR dense sensory nouns
- Controls (if any) appear after vibe, not before
- Pep is a burst at the end, not the thesis
- Sounds spoken aloud, not a Jira ticket
