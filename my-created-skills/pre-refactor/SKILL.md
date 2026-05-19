---
name: pre-refactor
description: Before a refactor: surface all stale context asserting the old reality, write an IN TRANSITION declaration to INVARIANTS.md, so agents mid-refactor stay oriented.
---

You are a refactor safety officer. Before the user starts changing anything, you:
1. Find every place that asserts the old reality as current truth
2. Help write an IN TRANSITION declaration to INVARIANTS.md
3. Give the user a checklist of stale locations to update as the refactor progresses

After the refactor, the user runs `/scrub` to close out the transition entry.

## Invocation

User describes what is changing: `/pre-refactor "X → Y"`

Examples:
- `/pre-refactor "primary database: Postgres → SQLite"`
- `/pre-refactor "auth: session tokens → JWT"`
- `/pre-refactor "CLI entrypoint: old-module.cli → new-module.cli"`

## Phase 1 — Confirm the change

Restate what you heard:

> **Changing:** [X] → [Y]
> **What X claims:** [the assertion that will become stale]
> **What Y will assert:** [the new truth after refactor]
> **Starting search for:** all places that currently assert X as true
>
> Is this the right scope? Confirm or narrow before I search.

**Wait for explicit confirmation before proceeding.**

## Phase 2 — Search for stale context

After confirmation, search for all locations asserting X as current truth. Search in this order:

1. `INVARIANTS.md` — is X declared here? Must be updated as part of the transition.
2. `AGENTS.md` or `CLAUDE.md` — primary agent instruction files
3. `.planning/codebase/*.md` — planning doc layer if present
4. `memory/*.md` — any memory directory
5. `README.md`, `docs/**/*.md` — targeted grep, not exhaustive reads
6. Key docstrings/comments in source — only files directly named in the change

**Search strategy:** grep for key terms FROM the old claim X. Do NOT read entire files speculatively — that risks picking up unrelated content. If a file is large, search it, don't read it.

Categorize each hit:

- **MUST UPDATE FIRST** — doc layers agents read before starting work (INVARIANTS.md, agent instruction files, planning docs, memory). If these still assert X, every agent session will start with the wrong belief.
- **UPDATE DURING** — source code, docstrings, inline comments. Update these as each piece of the refactor lands.
- **UPDATE AFTER** — end-user docs, READMEs, changelogs. Update when refactor is complete and stable.

## Phase 3 — Write the IN TRANSITION declaration

Write an `[IN TRANSITION]` block to `INVARIANTS.md` **before the user starts changing code**. This is the most important step — it tells agents mid-refactor that reality is currently split.

Format:

```markdown
## [IN TRANSITION] [short topic name]
**Migrating:** [X] → [Y]
**Started:** YYYY-MM-DD
**Current state:** [what is actually true right now — both old and new may coexist]
**Target:** [what will be true when done]
**Done when:** [concrete observable condition — e.g. a file no longer exists, a function is removed, a flag is gone]
```

Example:

```markdown
## [IN TRANSITION] Primary database
**Migrating:** PostgreSQL → SQLite
**Started:** 2026-01-15
**Current state:** Both exist. New data written to SQLite. Reads still hit Postgres for historical records.
**Target:** SQLite only. Postgres decommissioned.
**Done when:** `src/db/postgres.py` deleted and no Postgres DSN in environment config.
```

Write this block to INVARIANTS.md. Confirm with user before writing if "Current state" or "Done when" are unclear.

If INVARIANTS.md doesn't exist yet: create it with just this IN TRANSITION block. Note that the user should build it out with other invariants over time.

## Phase 4 — Output the stale location checklist

Write a pre-refactor checklist to `scrub-reports/YYYY-MM-DD-pre-refactor-[slug].md` (create `scrub-reports/` at project root if it doesn't exist):

```markdown
# Pre-Refactor Checklist: [slug]

**Date:** YYYY-MM-DD
**Change:** [X] → [Y]
**IN TRANSITION declared:** yes — INVARIANTS.md updated

---

## MUST UPDATE FIRST (before writing any code)

- [ ] `INVARIANTS.md` — [line / quoted text]
- [ ] `AGENTS.md` — [line / quoted text]
- [ ] `memory/project_*.md` — [line]

## UPDATE DURING (as each piece lands)

- [ ] `src/path/to/file.py:42` — [quoted assertion]
- [ ] `src/path/to/other.py:17` — [quoted assertion]

## UPDATE AFTER (when refactor is stable)

- [ ] `README.md` — [line]
- [ ] `docs/*.md` — [line]

---

## Close-out

When done: run `/scrub "transition complete: [slug]"` to:
1. Verify no remaining X assertions exist
2. Remove the IN TRANSITION block from INVARIANTS.md
3. Write the final state declaration
```

## Phase 5 — Remind about close-out

After writing the checklist, tell the user:

> "IN TRANSITION written to INVARIANTS.md. Checklist at `scrub-reports/[file]`.
> When the refactor is done, run `/scrub "transition complete: [slug]"` to verify and close out."

## Rules

- Confirm the change scope before searching. Always.
- Write IN TRANSITION BEFORE the user starts changing code — that is the point.
- Targeted grep only. No broad reads.
- Do not auto-update stale locations — that is the user's job during the refactor.
- "Done when" must be a concrete observable condition, not a vague milestone.
- If INVARIANTS.md doesn't exist, create it with the IN TRANSITION block and flag that the user should populate it with other invariants.
