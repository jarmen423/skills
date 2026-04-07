# Wave Task Prompt Template

Use this shape when launching a worker on any project.

## Required Fields

- task id
- wave id
- goal
- owned paths
- dependencies
- forbidden paths or boundaries
- deliverable
- verification commands
- handoff path

## Prompt Skeleton

```md
Task: <task-id> (<wave-id>)

Goal
- <one-sentence outcome>

Ownership
- <owned path 1>
- <owned path 2>

Do not touch
- <shared file or module boundary 1>
- <shared file or module boundary 2>

Dependencies
- <dependency or "none">

Deliverable
- <what the worker must finish>

Verification
- <command 1>
- <command 2>

Handoff
- Write/update: <handoff path>

Rules
- You are not alone in the codebase.
- Do not revert unrelated changes.
- Stay inside the owned write scope.
- If the task cannot be completed safely inside scope, stop and report the blocker in the handoff.
```

## Good Example

```md
Task: W3B-2 (wave-3-data-layer-refactor)

Goal
- Extract repository logic into a dedicated service layer with a stable interface.

Ownership
- src/services/user-repository.ts
- src/services/order-repository.ts
- src/services/index.ts
- src/services/__tests__/repository.test.ts

Do not touch
- src/types/index.ts
- src/api/routes.ts
- src/ui/**

Dependencies
- W3B-1 shared type definitions must be finalized before this task starts.

Deliverable
- Repository service layer is extracted, typed, and test-covered.

Verification
- npm run typecheck
- npm test

Handoff
- Write/update: .planning/execution/handoffs/wave-3-data-layer-refactor/w3b-2-repository-service.md
```
