---
name: excalidraw-learning-aids
description: create readable excalidraw learning aids and repo architecture or mechanism diagrams from code, notes, mermaid, docs, screenshots, or open-ended prompts. use when the user wants to teach, explain, onboard, or understand complex software systems, codebase internals, request lifecycles, data/control flows, distributed architecture, or any concept that benefits from a polished hand-drawn visual aid using excalidraw api, excalidraw mcp, mermaid-to-excalidraw, or portable .excalidraw files.
---

# Excalidraw Learning Aids

Use this skill to turn complex systems into clear, large, teachable Excalidraw visuals. Prioritize comprehension over diagram density: the result should be more readable than a typical Mermaid diagram and should not require squinting.

## Core workflow

1. Clarify the teaching target only when necessary: audience, repo area, mechanism, and output format.
2. Inspect the source material. For software repositories, map entrypoints, modules, runtime boundaries, data/control flow, and the specific mechanism being taught. Use `scripts/repo_snapshot.py` when a quick repo map would help.
3. Choose the visual format:
   - architecture map: services, packages, layers, dependencies
   - request/mechanism flow: numbered path through handlers, queues, stores, workers
   - lifecycle/state model: phases, triggers, side effects
   - mental model: concepts, analogies, and constraints
   - before/after or comparison: tradeoffs and design alternatives
4. Draft a storyboard before drawing: title, 3-7 key ideas, visual chunks, arrows, callouts, and learner takeaway.
5. Create the Excalidraw output through the best available route:
   - if an Excalidraw MCP tool is available, call its documentation/readme tool first, then create or update the scene with large elements and labels.
   - if a self-hosted or Plus API is available, use the configured endpoint and credentials; do not assume the alpha Plus API is stable.
   - if no live drawing tool is available, generate a portable `.excalidraw` file. Use `scripts/create_excalidraw_scene.py` for structured flow/architecture diagrams.
   - if the input is Mermaid, use it as a rough parseable sketch, then enlarge, regroup, relabel, and add teaching callouts. Do not return plain Mermaid unless explicitly requested.
6. Review the result with the visual quality checklist below before finalizing.

## Visual quality checklist

A good output from this skill must satisfy these rules:

- Use large, readable text: default node labels around 24-32 px; supporting detail around 16-20 px.
- Prefer 5-9 major visual chunks per canvas. Split into multiple panels or frames instead of cramming.
- Use whitespace deliberately. Keep arrows short and mostly horizontal or vertical.
- Put the main learner takeaway in the title or subtitle.
- Label arrows with the verb or payload, not just direction.
- Use callouts for the "why" behind important code paths, not just component names.
- Group related modules into layers or bounded regions: ui, api, domain, infrastructure, storage, external systems.
- For repo diagrams, cite concrete files/functions/classes in small footnote-style labels or callouts.
- Avoid decorative complexity. Every color, icon, and shape should teach something.
- If the scene feels dense, create progressive panels: overview first, then the selected mechanism.

## Repo-to-learning-diagram method

For software repo questions, follow the detailed process in `references/repo-visualization-workflow.md`.

Default extraction questions:

- What starts the flow? cli command, route, event, cron, test, component render, queue message, user action?
- Which files implement the path?
- Where are boundaries crossed? process, package, service, network, database, cache, filesystem, vendor api?
- What data shape moves through the system?
- Where are decisions, retries, validation, state changes, or side effects?
- What should a newcomer remember after seeing the diagram?

## Excalidraw integration notes

Read `references/excalidraw-integration.md` when using MCP, the Excalidraw component API, Mermaid conversion, export utilities, or self-hosted endpoints.

Use the built-in script when a direct drawing API is unavailable:

```bash
python scripts/create_excalidraw_scene.py spec.json output.excalidraw
```

To see the expected spec format:

```bash
python scripts/create_excalidraw_scene.py --example
```

For quick repository reconnaissance:

```bash
python scripts/repo_snapshot.py /path/to/repo --output repo_snapshot.md
```

## Output expectations

When the user asks for an artifact, produce one of these:

- `.excalidraw` scene file for import/opening in Excalidraw
- MCP-created interactive Excalidraw view when the MCP server is connected
- SVG/PNG export when an export-capable API/runtime is available
- concise explanation plus the artifact link or location

When returning a diagram, include a short note naming the intended learner takeaway and the key source files or concepts represented. Do not over-explain the whole diagram in prose; the visual should carry the explanation.
