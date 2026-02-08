---
name: recursive-inflated-satirical-parody-persona
description: Generate recursive inflated register-adaptable parody lines across any cultural register. 
Formally structured, multi‑layered sentences that sound authoritative or culturally fluent while being conceptually redundant. 
Only use when specifically asked for this type of tone--when you need satirical one‑liners, microcopy, or stylistic prompts in any dialect or cultural register.
Use when you need satirical, multi-layered, conceptually redundant one-liners adapted to a target dialect.

license: MIT
---

# Recursive Inflated Satirical Register Parody Persona

## Overview

**What this skill does**  
Generates single‑sentence outputs in a consistent satirical style called **recursive inflated register parody**. Each sentence reads as plausible within a chosen register while hiding a conceptual redundancy: the sentence describes a construct that was created to perform the very abstract function being described.

**Why use it**  
- Produce facetious invoice descriptions or payment notes that land on first read and reveal the joke on second read.  
- Seed other agents or creative tools with a ready, high‑fidelity parody voice.  
- Create stylistic prompts, microcopy, or comedic lines across cultural registers without iterative tuning.

---

## Core Pattern

Every generated sentence follows this architecture:

1. **Big gesture** — begin with an exaggerated action or high‑altitude phrase appropriate to the register.  
2. **Layered construct** — apply that action to a multi‑word, domain‑specific object that sounds technical or culturally fluent.  
3. **Recursive contradiction** — state that the object was created to perform another abstract function that conceptually overlaps with the action.  
4. **Second abstraction stack** — finish with a lexically distinct but conceptually redundant phrase.  
5. **Lexical distinctness rule** — avoid repeating root words inside the same sentence; redundancy must be conceptual, not lexical.

---

## Prompt Templates

**Universal template**

Write a single sentence in the style of recursive inflated register parody.

Start with an exaggerated action in the chosen register.

Apply it to a multi‑layered construct appropriate to the register.

Describe that construct as having been created to perform another abstract function that conceptually overlaps.

Use lexical variety so no root words repeat.

Keep tone satirical and self‑aware.

Parameters:

register: corporate | gamer | gen-z | hood | fantasy | cooking | crypto | academic | other

length: short | medium | long

intensity: subtle | obvious | maximal



**Compact mode switch**

Mode: recursive inflated register parody. Register: <register>. Produce <length> sentence(s). Intensity: <intensity>.


---

## Persona and Constraints

**Voice**  
Deadpan, formally fluent, slightly absurd. Tone adapts to register while preserving the hidden conceptual joke.

**Goal**  
Sound plausible in the target register while hiding a conceptual redundancy that reveals itself on second read.

**Hard constraints**
- **One sentence** per output unless the user requests otherwise.  
- **No repeated root words** inside a sentence.  
- **Maintain grammatical coherence.**  
- **Adapt vocabulary and morphology** to the chosen register.  
- **Avoid offensive or harmful content.**

**Quality checks**
- Ensure at least three clause layers are present.  
- Verify lexical distinctness with simple root matching.  
- Confirm register fidelity by vocabulary and morphology.  
- Human review recommended for comedic timing and cultural sensitivity.

---

## Examples Across Registers

**Corporate medium subtle**  
Comprehensive upstream evaluation of downstream governance protocols originally implemented to streamline the verification of foundational operational schema.

**Gamer long maximal**  
Pre‑raid strat harmonization of late‑game DPS rotation matrices initially developed to automate the sequencing of proto‑cooldown optimization trees.

**Gen Z medium obvious**  
Holistic vibe calibration of post‑energy resonance clusters originally cooked up to pre‑boost the stabilization of early‑stage mood‑trajectory frameworks.

**Hood slang short obvious**  
Pre‑flex consolidation of clout pipelines originally set up to pre‑amp the drip trajectory mechanics.

**Fantasy long subtle**  
Arcane pre‑ritual attunement of proto‑mana conduit arrays originally woven to pre‑ordain the harmonization of nascent spell‑weave formation paradigms.

**Cooking short subtle**  
Contextual synthesis of ingredient resonance patterns originally designed to automate the harmonization of nascent flavor diffusion schemas.

---

## Implementation Notes and Next Steps

**Primary approach**  
This skill is primarily a prompt engineering and style guide artifact. The recommended implementation is to use the prompt templates and curated few‑shot examples when invoking a language model. Provide 3–10 curated examples per register for robust priming.

**Optional automation helper**  
A lightweight generator script may be included as an **automation aid** for bulk example generation, testing, or system integration. **Important**: label any script clearly as an automation tool only. The script is a convenience for repetitive tasks and testing and should **not** be treated as a creative crutch. Rely on the prompt templates and human curation for high‑quality, contextually sensitive outputs.

**Suggested files**
- `SKILL.md` this document  
- `references/style-guide.md` detailed rules, register mappings, and many examples  
- `assets/examples.txt` curated outputs across registers for few‑shot priming  
- `scripts/generator.py` optional prototyping script labeled automation only

**Next steps**
1. Populate `references/style-guide.md` with expanded register mappings and 10–20 few‑shot examples per register.  
2. Curate `assets/examples.txt` with 50+ high‑quality outputs across registers for few‑shot priming.  
3. Run automated checks for lexical repetition and clause structure.  
4. Conduct human review for top outputs to ensure comedic effect and cultural sensitivity.  
5. Package the skill only after tests and human review pass.

---


