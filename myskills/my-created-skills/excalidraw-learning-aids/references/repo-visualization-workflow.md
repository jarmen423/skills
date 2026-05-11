# Repo Visualization Workflow

Use this reference when the input is a software repository, code snippets, stack traces, docs, or a question about how part of a codebase works.

## 1. Build a repo mental model

Collect only enough evidence to draw accurately:

1. Identify language and framework from manifests and config files.
2. Find entrypoints: routes, cli commands, event handlers, jobs, components, package exports, tests.
3. Trace the requested path through imports, function calls, types, configs, and side effects.
4. Distinguish runtime boundaries from source-code boundaries. A folder is not necessarily a service.
5. Record concrete anchors: file paths, function/class names, request names, event names, table/collection names.

Use `scripts/repo_snapshot.py` to produce a compact tree, language counts, manifest list, and simple import map. Treat its output as a starting map, not a substitute for reading important files.

## 2. Choose the teaching frame

Pick one primary frame. Do not try to draw every repo detail.

### Architecture map

Best for onboarding, system overview, package boundaries, or service dependencies.

Include:
- actors/external systems
- layers or bounded contexts
- major modules/services
- storage and queues
- key dependency arrows
- a legend explaining colors and arrow types

### Mechanism flow

Best for "how does X work?" questions.

Include:
- trigger
- numbered steps
- files/functions responsible for each step
- branching decisions
- state changes and side effects
- failure/retry paths if they are essential to understanding

### Request lifecycle

Best for web backends, api handlers, frontend data loading, auth, middleware, or async jobs.

Include:
- request/event input
- handler chain
- validation/auth
- domain logic
- data access
- response or emitted event

### Concept map

Best for explaining abstractions, domain models, plugin systems, or unfamiliar architecture styles.

Include:
- central concept
- supporting concepts
- examples from code
- common misconceptions or pitfalls

## 3. Storyboard before drawing

Create a tiny storyboard in text before creating elements:

- Title: one sentence learner takeaway.
- Audience: beginner, intermediate maintainer, reviewer, architect.
- Panels: overview, deep dive, edge cases, takeaway.
- Diagram chunks: 5-9 major nodes per panel.
- Source anchors: 3-8 files/functions/classes to show as small labels.

If more than nine chunks are needed, split into multiple canvases or create a wide progressive diagram with clear section headings.

## 4. Design repo diagrams for readability

Recommended layout patterns:

- Left to right for request/data flow.
- Top to bottom for lifecycle phases.
- Concentric or nested boxes for ownership/boundaries.
- Swimlanes for layers: client, edge/api, domain, infra, storage, external.
- Side callouts for code evidence and gotchas.

Use labels like:
- `1. parse config`
- `2. build dependency graph`
- `3. cache resolved result`

Avoid labels like:
- `manager`
- `service`
- `processor`

Every ambiguous noun should get a verb or purpose.

## 5. Represent code evidence without clutter

Use small code-anchor labels inside or below nodes:

- `src/server/routes/chat.ts`
- `AuthMiddleware.validate()`
- `packages/core/src/graph/resolve.ts`

Show only the best anchors. If every node has five file paths, create a separate "source map" panel instead.

## 6. Verification pass

Before final output, check:

- Does every arrow mean something specific?
- Can a newcomer explain the flow after one minute?
- Are file/function labels accurate and tied to inspected code?
- Did the diagram distinguish actual runtime calls from static imports?
- Are hidden mechanisms surfaced: caching, retries, batching, config, feature flags, auth, queues?
- Is there enough whitespace to read at normal zoom?
