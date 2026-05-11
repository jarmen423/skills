# Visual Design Rubric

Use this rubric when a diagram needs quality review or redesign.

## Readability thresholds

- Title: 36-48 px.
- Section heading: 28-36 px.
- Main node label: 24-32 px.
- Node detail: 16-20 px.
- Code anchor or footnote: 14-16 px.

Avoid tiny text even if the canvas gets large. Excalidraw canvases can be spacious; use that advantage.

## Information density

A single panel should usually contain:

- 1 main takeaway
- 3-7 major nodes
- 3-8 arrows
- 1-4 callouts
- 0-1 legend

For larger systems, make multiple panels:

1. System overview
2. One critical path
3. Data/state model
4. Failure or edge-case path

## Visual grammar

Use consistent semantics:

- Blue-ish nodes: interfaces, api, network boundary.
- Green-ish nodes: domain logic, transformations, core mechanisms.
- Yellow-ish nodes: data stores, caches, config, state.
- Purple-ish nodes: async workers, queues, schedulers, background processing.
- Gray nodes: external actors/systems.
- Red/pink callouts: hazards, failure paths, security-sensitive points.

Do not rely only on color. Pair color with labels, grouping, and shape/position.

## Better than Mermaid checklist

The diagram should improve on Mermaid by adding at least three of these:

- larger typography
- whitespace and grouping
- learner-focused title/subtitle
- code source anchors
- callouts explaining why steps matter
- progressive panels
- legend for semantics
- simplified but accurate runtime boundaries
- explicit failure/edge path where relevant

## Common fixes

- Too many arrows: split into phases or show only primary flow, then add a secondary panel for side effects.
- Too much text in nodes: move details to callouts or source anchors.
- Too many components: collapse internal helpers into one mechanism node.
- Ambiguous arrows: label each arrow with action, protocol, event, or payload.
- Folder diagram masquerading as architecture: replace folders with runtime responsibilities and boundaries.
