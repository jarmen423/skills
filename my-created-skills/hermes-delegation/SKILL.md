---
name: hermes-delegation
description: "Use when delegating coding to an external CLI agent."
version: 1.0.0
author: Josh Friedman (jarmen423), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Coding-Agent, Delegation, Router, Orchestration]
    related_skills: [coding-agent-supervision, shared-worktree-integration, timeboxed-subagent-orchestration, devin-handoff, devin-thread-distillation]
---

# Hermes Delegation Router

> Progressive-disclosure routing layer for delegating bounded coding work to
> external coding-agent CLIs. The subskills in this directory hold each
> vendor's verified command surface; this file decides which one to load.

Supported subskills: Codex, OpenCode, Grok Build, Antigravity (agy), Meta
Muse Code, and Cognition Devin — plus `coding-agent-supervision` for the
shared background-run workflow.

## Core Mandate

Hermes orchestrates, the external CLI executes. The parent writes the brief,
fences the checkout, and owns verification and integration. Delegate when a
task is well-specified and self-contained; implement directly when the work is
smaller than its brief would be.

All child paths below are relative to this skill's directory.

## How to Use This Router

1. Match the task to the closest routing question below.
2. Read the short synthesis for the governing constraints.
3. Load ONE child `SKILL.md` for the vendor's real flags and pitfalls.
4. For every background run, also load `coding-agent-supervision/SKILL.md`.
5. Load a second child only when the task genuinely crosses vendors.

### Progressive-disclosure rule

Do **not** preload all child skills "just in case." Start with one. Add
another only when the work demonstrably needs it.

### Shared contract (every child CLI)

- Brief written to a file; headless invocation with an outer Hermes timeout.
- Work in an isolated git worktree; production clones are off limits.
- No push, no secrets in the transcript, no edits outside the worktree.
- **Exit 0 means the turn ended, not that the work is correct.** The parent
  re-verifies artifacts before accepting anything.

---

## 0. Supervision, Evidence & Recovery

**Route here when:** the CLI runs in the background (always), or you need
liveness checks, stall detection, turn-cap recovery, worker attribution,
cleanup traps, or the completion checklist.

**Synthesis**  
A spinner and an exit code are not progress. Verify by artifacts: changed
files, rerun tests, compile/lint gates. Prove new regression tests can fail.
Narrate every tool-bearing turn. This class-level workflow governs ALL the
CLIs below; vendor skills carry only tool-specific flags.

**Go to:** `coding-agent-supervision/SKILL.md`

---

## 1. OpenAI Codex

**Route here when:** implementing features or fixes and driving GitHub
branches/PRs is part of the deliverable; the user names Codex or `codex`.

**Synthesis**  
`codex exec` headless. Full PR lifecycle support. Watch the shared
ChatGPT-account rate limit on burst dispatches.

**Go to:** `codex/SKILL.md`

---

## 2. OpenCode

**Route here when:** implementing features or fixes, or running PR review;
the user names OpenCode or `opencode`.

**Synthesis**  
`opencode run` headless. Strong review lane.

**Go to:** `opencode/SKILL.md`

---

## 3. xAI Grok Build

**Route here when:** fast iterative implementation or review on xAI models;
the user names Grok Build or `grok`.

**Synthesis**  
`grok -p` headless. The flushed stdout is often only planning prose — read
the vendor session log for real output and verdicts.

**Go to:** `grok-build-cli/SKILL.md`

---

## 4. Google Antigravity (agy)

**Route here when:** a cheap parallel slice (e.g. a mechanical port of an
already-landed reference implementation), or overflow capacity is needed.

**Synthesis**  
`agy -p --new-project` in an isolated worktree. Quota resets in ~3h — plan
interruptible slices. Path-fence `git` with a wrapper; audit every commit
file-by-file for ride-along changes.

**Go to:** `antigravity-cli/SKILL.md`

---

## 5. Meta Muse Code

**Route here when:** a bounded implementation/fix/refactor with session
resume, or the user names Muse.

**Synthesis**  
`muse exec` is the only headless path (bare `muse` opens the TUI). JSONL
stream gives session id and final answer. Never `--yolo` on a shared checkout.

**Go to:** `muse-code-cli/SKILL.md`

---

## 6. Cognition Devin (local CLI)

**Route here when:** a bounded implementation/fix/refactor or review on
Devin's models; the user names Devin or `devin`.

**Synthesis**  
`devin -p` headless; `--respect-workspace-trust false` is mandatory in
scripts. Every run spends credits/ACU — obey the paid-API gate (user confirms,
one tiny smoke first). Needs a whole VM with browser/CI or a finished PR
back? That is cloud Devin — `devin-handoff`, not this router's child.

**Go to:** `devin-cli/SKILL.md`

---

## Routing Shortcuts

| Task | Start with | Add only if needed |
|---|---|---|
| Any background/long run | Vendor child + `coding-agent-supervision` | `shared-worktree-integration` |
| "Implement this feature with X" | That vendor's child | `coding-agent-supervision` |
| Branch + PR deliverable | `codex` | `coding-agent-supervision` |
| PR review pass | `opencode` or `codex` | — |
| Mechanical port of landed reference | `antigravity-cli` | — |
| Bounded run needing session resume | `muse-code-cli` or `devin-cli` | — |
| Task needs a VM, browser, CI, or cloud PR | `devin-handoff` (cloud, outside this router) | — |
| Several CLIs at once | `timeboxed-subagent-orchestration` | Per-vendor children |

## Adjacent Skills (not subskills here)

- `devin-handoff` — cloud Devin sessions with their own VM, browser, and repo
  access; the REPL's `/handoff` lands there.
- `devin-thread-distillation` — mine past Devin CLI threads into reviews.
- `shared-worktree-integration` — concurrent agents editing one worktree.
- `timeboxed-subagent-orchestration` — Hermes `delegate_task` budgets and
  timeout recovery.

## Final Principle

One child skill per delegation, supervision on every background run, and the
parent trusts its own verification over any exit code, spinner, or summary.
