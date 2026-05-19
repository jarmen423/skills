# Wave Handoff Template

Use this format for task completion or pause handoffs.

## Template

```md
# <task-id> Handoff

## Status

- `done` | `blocked` | `paused`

## What Changed

- <high-signal change 1>
- <high-signal change 2>

## Files

- <path 1>
- <path 2>

## Verification

- <command>: pass | fail | not run
- <command>: pass | fail | not run

## Blockers Or Risks

- <blocker or residual risk>

## Next Thread Should Know

- <important context 1>
- <important context 2>
```

## Rules

- Keep it short and operational.
- Do not paste large diffs.
- Call out any assumption that the next thread could trip over.
- If verification was skipped, say exactly why.

## Good Example

```md
# W3B-2 Handoff

## Status

- `done`

## What Changed

- Extracted user and order repository logic into dedicated service modules.
- Added typed interfaces so consumers no longer import raw DB internals.

## Files

- src/services/user-repository.ts
- src/services/order-repository.ts
- src/services/index.ts
- src/services/__tests__/repository.test.ts

## Verification

- npm run typecheck: pass
- npm test: pass

## Blockers Or Risks

- The order repository does not yet handle soft-delete; deferred to a later wave.

## Next Thread Should Know

- The service index exports are stable and safe for the API route layer to consume.
- Do not add new fields to the shared User type until W3C-1 type audit is done.
```
