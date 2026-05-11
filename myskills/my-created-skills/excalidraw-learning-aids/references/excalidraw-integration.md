# Excalidraw Integration Notes

Use this reference when deciding how to create or export an Excalidraw learning aid.

## Preferred output routes

1. MCP-connected Excalidraw app: best for interactive diagrams in chat. If an MCP tool exposes a readme/reference tool, call it before creating the view. The current public Excalidraw MCP app advertises tools named `read_me` and `create_view`, but tool names may differ in a user's environment.
2. Self-hosted Excalidraw or custom API: use the endpoint and authentication supplied by the user or environment. Do not invent credentials or assume the hosted Plus API contract is stable.
3. Portable `.excalidraw` file: safest fallback. Generate an Excalidraw JSON scene that the user can import into Excalidraw.
4. SVG/PNG export: use when an export-capable runtime or API is available.

## Excalidraw component API facts

The `@excalidraw/excalidraw` package exposes utilities for serialization, loading, restoring, exporting, and programmatic element creation. For programmatic creation, the skeleton element API can be converted to full elements with `convertToExcalidrawElements` before passing to `initialData` or `updateScene`.

Important design implication: generate high-level skeletons or portable scenes first, then let the API/runtime normalize if available.

## Mermaid-to-Excalidraw guidance

Use Mermaid only as an input accelerator, not as the final design format.

Mermaid conversion works in two steps:

1. parse Mermaid syntax into Excalidraw skeleton elements.
2. convert skeleton elements into full Excalidraw elements.

Current limitations to account for:

- Flowcharts are the main supported diagram type.
- Subgraphs are supported as grouped diagrams.
- Several Mermaid shapes fall back to rectangles.
- Unsupported diagram types may render as images instead of editable Excalidraw shapes.

Therefore, after conversion, enlarge text, regroup components, add callouts, split dense flows into panels, and add source anchors.

## Portable `.excalidraw` scene basics

A portable scene is JSON with this rough shape:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "excalidraw-learning-aids",
  "elements": [],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

When hand-generating elements:

- Use stable ids for nodes and matching arrows when possible.
- Prefer separate text elements for titles, subtitles, callouts, and code anchors.
- Keep node rectangles large enough for 24 px labels.
- Use group ids for a node's rectangle, title, and detail text.
- Use labelled arrows with a text element near the midpoint if arrow labels are not supported by the target route.

## Self-hosting posture

If the user self-hosts Excalidraw or an MCP app:

- Ask for or discover the local endpoint only when actually needed.
- Keep API configuration outside the skill package; do not bake keys into the skill.
- Make diagrams portable so they are not locked to one host.
- Prefer exportable `.excalidraw` plus optional SVG/PNG for sharing.
