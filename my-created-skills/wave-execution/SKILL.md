---
name: wave-execution
description: Use when planning or executing multi-wave parallel work on any project. Covers the execution framework, task registry, write-scope ownership, handoff rules, merge gates, and how to split safe parallel subagent work without collisions.
---

# Wave Execution

Use this skill when work should be organized as wave-based parallel execution instead of ad hoc tasking.

## Start Here

Before doing anything else, orient yourself to the project by reading:

1. The project's root `README.md` or equivalent overview doc
2. Any roadmap or target-state document
3. The execution plan directory (e.g., `.planning/execution/README.md`)
4. The wave roadmap (e.g., `.planning/execution/ROADMAP.md`)
5. The task registry (e.g., `.planning/execution/tasks.json`)

Use domain-specific research or design docs when the current phase touches a specialized layer (e.g., data modeling, API contracts, UI systems).

Use these companion references when drafting or reviewing execution artifacts:

- `references/task-template.md`
- `references/handoff-template.md`
- `references/ownership-examples.md`

## Core Rule

Parallelize by **disjoint write scope**, not by vague topic.

Safe:

- two agents each owning a separate package, module, or directory
- research/docs vs implementation code
- UI vs data layer (when shared schema is already stable)

Unsafe:

- two threads editing the same file
- two threads editing the same narrow module boundary
- starting downstream work before the upstream contract or schema is stable

## The Workflow

### 1. Lock the wave

Before launching subagents:

- define the wave goal
- define task ids
- define dependencies
- define write ownership
- define verification commands
- define handoff paths

Record this in your project's execution plan and task registry before any work starts.

### 2. Split only non-overlapping work

Good split examples:

- research/docs vs implementation
- module A vs module B (when no shared file)
- UI/reporting vs data layer (when schema is stable)
- configuration/calibration vs validation logic

Bad split examples:

- two agents both touching a shared types or contracts file
- two agents both touching the same service or repository module
- two agents editing the same data or config files

Use `references/ownership-examples.md` when deciding whether a split is actually safe.

### 3. Make each task self-contained

Each task should include:

- precise goal
- owned files or directories
- dependencies
- what not to touch
- required verification
- required handoff file

Use `references/task-template.md` for the worker prompt shape.

### 4. Require a handoff before closure

Every task writes a handoff under your project's designated handoffs directory (e.g., `.planning/execution/handoffs/<wave-id>/`).

The handoff must state:

- what changed
- what was verified
- blockers or residual risks
- what the next thread should know

Use `references/handoff-template.md` when drafting or reviewing handoffs.

### 5. Merge only through gates

Do not consider a wave done until:

- all required task handoffs exist
- integration review is complete
- verification passes

Define gate commands appropriate to your project's toolchain. Common examples:

- `npm run typecheck` / `tsc --noEmit`
- `npm test` / `pytest` / `cargo test`
- `npm run build` / `make build`

## Subagent Rules

Use subagents when:

- there are 2 or more independent tracks
- the write scopes do not overlap
- waiting on one result is not required for the next local step

Keep work local when:

- the task is on the critical path
- the schema or contract is still moving
- file ownership is shared or ambiguous

When spawning a worker, always specify:

- exact owned paths
- exact deliverable
- instruction not to revert unrelated changes
- instruction to write or update the expected handoff artifact

## Recommended Wave Shape

For most phases in any project:

1. Research or contract lock
2. Parallel implementation threads
3. Integration thread
4. Verification gate
5. Status update in task registry

Do not skip the contract-lock step for phases that widen shared types, schemas, or interface boundaries.

## Orchestrator Read-Only Mode (Optional)

Enable this mode when the orchestrating agent should act purely as a coordinator and never touch code or artifacts directly.

### When to use

- Large waves where the orchestrator managing work is a different concern from doing work
- Projects where all edits must be traceable to a specific worker subagent
- Any context where you want a clean audit trail of who changed what

### Rules when active

**No direct edits.** The orchestrator must not write, edit, or delete any project file. All changes are delegated to worker subagents with explicit owned paths.

**No direct reviews.** The orchestrator must not perform code review itself. Reviews are delegated to review subagents. The orchestrator reads only the summary report those review subagents produce.

**Verification exception.** Before delegating to a corrective subagent, the orchestrator is allowed to read files to confirm that a regression or error reported in a review actually exists. This is a read-only check — it does not authorize edits.

### Delegation flow

```
Orchestrator
  └─ spawns worker subagents (edits)
  └─ spawns review subagents (reviews)
       └─ review subagent writes summary report
  └─ orchestrator reads report
  └─ orchestrator optionally reads code to verify reported issue exists
  └─ orchestrator spawns corrective subagent (edits)
```

### Handoff implication

Review subagents must write their own handoff or summary report (e.g., `.planning/execution/handoffs/<wave-id>/review-<task-id>.md`). The orchestrator uses that file as its sole input for deciding whether to dispatch corrections.

## Common Failure Modes

- launching parallel work before the contract is stable
- allowing two threads to touch the same shared file
- treating existing artifacts as sufficient research when a real research phase is needed
- marking a task complete without a handoff
- claiming a wave is done before the project-level gate passes

## Output Style

When using this skill, prefer:

- wave ids
- task ids
- explicit dependencies
- explicit write scopes
- short merge gates

Do not produce fuzzy plans like "frontend/backend/data in parallel" without file ownership.
