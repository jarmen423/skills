---
name: knowledge_graph_hero_exhibit
version: 0.1
description: |
  Generates interactive knowledge-graph hero sections with science-exhibit aesthetics. This
  skill constructs circular or specimen-like graph layouts with a loose outer rim of
  peripheral nodes, multiple interior clusters and clean negative space for typography. It
  outputs a structured SceneSpec containing nodes, edges, layers, camera information and
  styling tokens, plus a Three.js module for rendering, preview images, and diagnostics.
  The skill supports iterative refinement of the layout and export of packaged assets.
license: MIT
authors:
  - chatgpt
inputs:
  intent:
    type: string
    description: "Operation to perform: `generate_hero_graph`, `iterate`, or `export`."
    required: true
  aspect_ratio:
    type: string
    description: "Desired aspect ratio of the hero section, for example `16:9`."
    default: "16:9"
  pixel_ratio:
    type: number
    description: "Target device pixel ratio for rendering."
    default: 1.0
  node_count:
    type: integer
    description: "Approximate number of nodes in the graph."
    default: 400
  cluster_count:
    type: integer
    description: "Number of clusters of nodes."
    default: 5
  rim_density:
    type: number
    description: "Proportion of nodes placed on the outer rim, from 0 to 0.5."
    default: 0.1
  palette:
    type: string
    description: "Palette preset name, such as `cool`, `ivory`, `monochrome`, or `burgundy`."
    default: "cool"
  accent_colors:
    type: array
    description: "Optional list of hex codes for custom accent colors."
    items:
      type: string
  safe_area:
    type: object
    description: "Normalized rectangle reserved for headlines or CTAs; coordinates in [0,1]."
    properties:
      x:
        type: number
      y:
        type: number
      w:
        type: number
      h:
        type: number
    default:
      x: 0.06
      y: 0.10
      w: 0.44
      h: 0.32
outputs:
  scenespec_json:
    description: "JSON structure describing nodes, edges, layer assignments, camera settings, and styling tokens."
  threejs_module:
    description: "ES module that renders the SceneSpec using Three.js, including parallax and bloom."
  previews:
    description: "PNG or GIF preview images, with optional short MP4 or GIF animation for quick review."
  diagnostics:
    description: "Metrics report containing draw calls, GPU memory use, performance proxy stats, and background or safe-area compliance checks."
functions:
  generate_hero_graph:
    description: "Generate a new SceneSpec and associated assets from the provided parameters."
    parameters:
      node_count: integer
      cluster_count: integer
      rim_density: number
      palette: string
      accent_colors: array
      safe_area: object
    returns:
      - scenespec_json
      - threejs_module
      - previews
      - diagnostics
  iterate:
    description: "Modify an existing SceneSpec according to a change request such as `reduce clutter` or `increase negative space`."
    parameters:
      scenespec_json: string
      change_request: string
    returns:
      - scenespec_json
      - previews
      - diagnostics
  export:
    description: "Package the SceneSpec and assets into a zip archive for deployment."
    parameters:
      scenespec_json: string
    returns:
      - file
---

# Knowledge Graph Hero Exhibit

This skill creates immersive hero-section graphics that resemble scientific exhibits or
planetarium installations. It is intended for interactive web experiences built with
Three.js and WebGL, with a pure black background, restrained glow, layered parallax depth,
and a circular knowledge-graph silhouette made of clusters, bridges, and scattered rim nodes.

## Purpose

Use this skill when the user wants to:

- Generate a science-exhibit style knowledge-graph hero section
- Create a circular or specimen-like network composition for a website hero
- Iterate on node density, palette, negative space, or cluster structure
- Export a SceneSpec plus implementation-ready Three.js assets
- Build an interactive, high-performance WebGL network experience with visual restraint

## Core Design Principles

The skill should optimize for:

- A nearly circular overall silhouette
- A loose outer rim of scattered peripheral nodes
- Multiple distinct interior clusters with varied density
- Clear negative space for typography and CTA overlays
- Layered depth for parallax and subtle camera drift
- A pure black background with no gradients
- A calm, awe-inspiring science-exhibit aesthetic
- Strong silhouette readability without visual overload

## Skill Workflow

### 1. Graph generation

Create a base graph either procedurally or from user-provided data.

For procedural generation, use graph families that produce believable topology:

- Stochastic Block Models for explicit communities
- Barabási-Albert for hub-heavy structures
- Watts-Strogatz for clustered small-world behavior
- Erdős-Rényi for controlled randomness

If the input is data-driven, optionally compute:

- node importance
- community structure with Louvain or Leiden
- embeddings for semantic clustering

### 2. Cluster placement

Treat each cluster as a supernode and place cluster centers inside a disk while:

- preserving minimum separation
- respecting a typography-safe area
- maintaining a circular specimen-like silhouette
- reserving room for a loose outer rim

### 3. Intra-cluster layout

Inside each cluster, run a localized organic layout such as:

- Fruchterman-Reingold
- ForceAtlas2-like refinement

Normalize each cluster to its local radius so clusters remain distinct and visually legible.

### 4. Rim node placement

Place peripheral nodes near the outer boundary with jitter so the result feels organic,
not like a perfect ring.

Rim nodes should:

- lightly orbit the structure
- connect sparingly to nearby clusters
- reinforce the circular silhouette
- avoid cluttering the center

### 5. Global refinement

Run a final graph-wide refinement pass with:

- mild collision avoidance
- attractive and repulsive balancing
- center gravity to keep the graph inside the disk
- repulsion from the safe area
- optional depth-layer assignment for parallax

Depth layers should generally be:

- foreground
- midground
- background

### 6. Styling and palette

Apply a restrained visual system.

Rules:

- use 2 to 4 dominant hues max
- zone color by cluster, not random node noise
- reserve accent colors for high-importance regions
- keep bloom restrained and museum-like
- preserve contrast on pure black
- maintain visual calm over maximal complexity

### 7. Rendering and preview generation

Render via a Three.js/WebGL pipeline.

Recommended runtime strategy:

- `Points` or instanced billboards for most nodes
- `InstancedMesh` for premium foreground hubs if needed
- `LineSegments` for most edges
- selective bloom using `EffectComposer` and `UnrealBloomPass`
- subtle pointer-driven parallax
- optional slow idle drift
- diagnostics via renderer stats

Generate:

- preview PNGs
- optional short animated previews
- diagnostics for draw calls, memory, and compliance checks

## Supported Intents

### `generate_hero_graph`

Create a new hero graph from high-level parameters.

Example requests:

- "Generate a science-exhibit circular hero graph with 5 clusters and cool tones."
- "Create a sparse circular network with ember-red accents and lots of negative space."
- "Make a monumental hero graph for a Three.js landing page."

### `iterate`

Modify an existing SceneSpec using natural-language edits.

Example requests:

- "Reduce clutter in the center."
- "Make the clusters more distinct."
- "Add more breathing room top-left."
- "Keep the circular silhouette but scatter the outer rim more."
- "Shift to a museum-like ivory palette."

### `export`

Bundle the SceneSpec and runtime assets for deployment.

Expected exports may include:

- SceneSpec JSON
- Three.js module
- palette tokens
- texture assets
- preview images
- diagnostics

## SceneSpec Expectations

The output SceneSpec should contain:

- stable node IDs
- stable edge definitions
- cluster IDs
- importance values
- 3D coordinates
- layer assignments
- palette and styling tokens
- camera defaults
- parallax settings
- interaction affordances
- safe-area definition

## Recommended Palette Presets

### cool
- Base: `#EAF2FF`, `#CFE7FF`
- Accent: `#A0D8EF`

### ivory
- Base: `#F4F1E8`, `#E8DED0`
- Accent: `#C2975A`

### monochrome
- Base: `#FFFFFF`, `#BFBFBF`
- Accent: `#737373`

### burgundy
- Base: `#EAE6F2`, `#DDD5E8`
- Accent: `#A42E5C`, `#C33A4C`

Custom `accent_colors` may override or supplement preset accents.

## Visual Constraints

Always enforce the following:

- background must be exactly `#000000`
- no gradients
- no UI chrome unless explicitly requested
- no labels baked into the graph unless explicitly requested
- preserve silhouette readability at small sizes
- preserve a typography-safe area
- avoid hairball-like density
- avoid rainbow palettes unless explicitly requested
- avoid excessive bloom or glow fog
- avoid chaotic sci-fi clutter

## Accessibility and UX

The hero should feel alive, but never distracting.

Requirements:

- support `prefers-reduced-motion`
- reduce or disable drift and parallax when motion reduction is preferred
- keep hover interactions subtle
- avoid large sudden movements
- maintain enough contrast for visibility
- ensure the graph behaves as a background/hero element first, interactive system second

## Performance Priorities

Optimize for browser delivery.

Target strategies:

- minimize draw calls
- batch repeated geometry
- use instancing where possible
- keep postprocessing passes minimal
- use semantic LOD for large graphs
- expose diagnostics for draw calls and memory
- support mobile-safe reductions in density and motion

## Suggested Implementation Notes

A good MVP should include:

1. SceneSpec generator with safe-area enforcement
2. Hybrid layout engine for cluster + rim composition
3. Three.js renderer template
4. Basic hover and parallax
5. Reduced-motion support
6. Preview rendering
7. Performance and compliance checks
8. Export packaging

## Example Usage

### Example 1: create

User request:

`Generate a science-exhibit hero graph with 5 clusters, cool white and cyan palette, subtle ember accents, and headline-safe space on the left.`

Expected behavior:

- create a circular or near-circular SceneSpec
- reserve left-side negative space
- generate interior clusters plus scattered rim nodes
- return previews and runtime bundle

### Example 2: iterate

User request:

`Keep the reds but reduce clutter and make the outer rim feel more scattered.`

Expected behavior:

- preserve palette
- lower edge density or node overlap
- widen outer-node jitter distribution
- update previews and diagnostics

### Example 3: export

User request:

`Export the current graph for implementation in my Three.js hero section.`

Expected behavior:

- package SceneSpec
- include rendering module
- include assets and previews
- return deployable bundle

## Notes

This skill is intended as a reusable production blueprint for building interactive
knowledge-graph hero sections. It is most effective when paired with a deterministic layout
pipeline and optional AI assistance for:

- style extraction from reference images
- prompt-to-style parameter generation
- sprite and texture synthesis
- iterative creative direction

The geometry and runtime behavior should remain deterministic and testable even when AI is
used to guide style decisions.
