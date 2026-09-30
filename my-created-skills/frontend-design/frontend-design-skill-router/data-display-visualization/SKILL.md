# Data Display, Tables, Lists, Charts & Complex Visualization

> Dedicated content skill for making large or complex data feel calm, controllable, fast, and scannable.

**Core Mandate**  
The goal is to render the *decision*, not the raw dataset. Users should be able to scan, compare, filter, and act without the interface fighting them. Performance and delight come from the same architectural decisions: virtualization, stable identity, compositor-friendly updates, and selective rendering technology based on data volume and interaction density.

## When to Use This Skill

Use this skill when an agent is:
- Building dense data tables, lists, or grids that users scan for extended periods
- Implementing dashboards with charts, sparklines, or real-time metrics
- Creating interactive visualizations (filtering, brushing, zooming, direct manipulation)
- Dealing with large datasets that cause jank, high memory use, or slow interactions
- Choosing between SVG, Canvas, or WebGL for data rendering

## Core Principles

1. **Render only what is visible (or about to be).** Virtualization (windowing) is non-negotiable for anything beyond a few hundred rows or complex marks.
2. **Decouple interaction from rendering.** Capture pointer events on a transparent overlay and render visuals to Canvas/WebGL when DOM overhead becomes the bottleneck.
3. **Stable identity + atomic updates.** Every row, cell, or mark should have a stable key. Updates should re-render only what changed.
4. **Choose the right rendering primitive for the job.** SVG for declarative, accessible, interactive charts under ~1,000 points. Canvas or WebGL for larger datasets or many moving marks.
5. **Animation must serve comprehension.** If animating a chart makes panning, hovering, brushing, or selecting feel sluggish, the animation lost the argument.
6. **Perceived performance matters as much as raw speed.** Skeletons, deferred rendering, and progressive disclosure reduce cognitive load even when data is still loading.

## Key Patterns & Techniques

### 1. Virtualization / Windowing for Lists and Tables
Never render more DOM nodes than the user can see + a small overscan buffer.

- Use `react-window`, `react-virtuoso`, or TanStack Virtual
- Give items stable keys and either fixed or well-estimated heights
- Use placeholder skeletons or deferred rich content (avatars, charts in cells) until rows are visible
- For tables: combine row virtualization + column virtualization + sticky headers

**Figma Layers Panel pattern:** Two-pass rendering — first determine visible rows, then compute only the properties needed for those rows. Delivered 30–50% faster interactions in large files.

### 2. Atomic / Derived State for High-Frequency Updates
In dense, real-time, or collaborative surfaces, a single changed cell or row should not cause the entire table to re-render.

- Use observable state pools (MobX, Signals) or fine-grained reactivity
- Memoize row/cell components aggressively
- Update only the changed parts of the data model

**Linear issue lists:** Atomic updates mean changing one issue’s status only re-renders that specific cell/row, not the whole list.

### 3. Choosing Rendering Technology for Charts & Visualizations
- **SVG**: Best for declarative, accessible, interactive charts with moderate data volume (< ~1,000 points). Easy hit-testing and styling.
- **Canvas 2D**: Excellent for many simple moving marks, particles, or high-volume time-series. Use libraries like uPlot for extreme performance (150k+ points in ~25 ms).
- **WebGL / Three.js or deck.gl**: When you need 3D perspective, complex lighting, or true spatial indexing for very large point clouds or networks.

**Rule:** If panning/zooming/hovering feels laggy, you are probably using the wrong primitive or not virtualizing/downsampling properly.

### 4. Real-Time / Streaming Data
- Batch incoming updates and synchronize rendering to `requestAnimationFrame`
- Downsample data to the pixel width of the chart when possible
- Use Web Workers for aggregation and parsing
- Consider Canvas or WebGL backends for high-frequency updates

### 5. Progressive Disclosure & Deferred Rich Content
In tables with expandable rows or cells containing charts/editors:
- Don’t mount heavy components during scroll
- Use intersection observers or virtualization to defer rich content until the row is actually visible and stable
- Show lightweight skeletons or summaries first

### 6. Interaction Techniques for Complex Viz
- Decouple pointer events from rendering (transparent DOM overlay + Canvas/WebGL underneath)
- Use spatial indexing (R-tree, quadtree) for fast hit testing
- Throttle or debounce expensive computations (brushing, filtering)
- Provide immediate local feedback even if the full dataset update is async

## Production Examples (Delight + Performance)

**Figma Layers Panel**  
Delight: Managing tens of thousands of layers without the UI ever feeling heavy or laggy.  
Performance: Custom virtualization + derived state. Only visible rows compute names, icons, and selection state. Massive win for large design files.

**Linear Issue Lists & Tables**  
Delight: Snappy, keyboard-navigable, information-dense lists that still feel calm. Instant filtering, grouping, and reordering.  
Performance: Virtualized lists + atomic MobX updates. Only changed cells re-render. Optimistic local state before server confirmation.

**Notion Databases**  
Delight: Highly customizable views (table, board, calendar, list) with tactile drag-and-drop. Same underlying data moves fluidly between representations.  
Performance: Strict limits on properties per view + virtualization of long lists. Lazy loading of embedded databases.

**Vercel Analytics & Deployment Dashboard**  
Delight: Beautiful, instantly responsive sparklines and status indicators that make infrastructure feel legible.  
Performance: Canvas-based rendering for high-volume telemetry. Route-based code splitting and deferred chart rendering after critical path.

**Stripe Transactions & Reporting Tables**  
Delight: Clean, scannable rows with strong information hierarchy and progressive disclosure in expandable rows.  
Performance: Server-side pagination for large sets + column virtualization on wide reports. Sticky headers with `contain: paint layout`.

**Airtable Editable Grid**  
Delight: Spreadsheet-like editing across thousands of cells that still feels responsive.  
Performance: Virtualized grid (row + column) + cell-level memoization + optimistic mutations.

**Superhuman Email List**  
Delight: Instant triage feel with rich metadata and keyboard navigation.  
Performance: Virtualized rows + lazy-loaded avatars with blur-up placeholders. Local-first updates.

**Datadog / Grafana Dashboards**  
Delight: Hundreds of time-series rendered simultaneously with anomaly highlighting and correlated brushing.  
Performance: Downsampling to pixel width, aggregations in workers, Canvas/WebGL rendering path, tooltips in separate DOM overlay.

**uPlot Streaming Charts**  
Delight: Visually sharp high-volume time-series with zero interaction latency.  
Performance: Canvas 2D with zero React overhead in the hot path. Properly accounts for device pixel density.

**Observable Plot**  
Delight: Opinionated, decision-oriented statistical charts that are fast to build and responsive by default.  
Performance: Grammar-of-graphics approach with automatic binning and responsive sizing. Good default for product dashboards.

## Anti-Patterns to Avoid

- Rendering 5,000–10,000+ row tables directly into the DOM
- Mounting charts, rich editors, or heavy components inside table cells during scroll
- Default chart animations on large or streaming datasets
- Non-virtualized infinite scrolls without height estimation or placeholders
- Driving visualization updates from React state on every frame
- Using SVG for datasets with thousands of points without downsampling
- Table cells that trigger layout thrashing when expanding or loading content
- Dashboards that prioritize ornamental gradients and heavy effects over actual comparison and decision-making

## Further Reading & Authoritative Sources

**Virtualization & Tables**
- TanStack Virtual and react-window documentation
- AG Grid virtualization and lazy loading guides
- Figma Blog — "Improving Performance in the Layers Panel"
- Patterns.dev — Virtualize large lists

**Charts & Visualization**
- uPlot GitHub repo and performance characteristics
- Observable Plot documentation
- visx by Airbnb (low-level React visualization primitives with Canvas/SVG/WebGL choice)
- ECharts large dataset and streaming modes
- D3 for bespoke explanatory graphics (use sparingly in product UIs)

**General Data UI Performance**
- web.dev — Rendering performance, INP, and content-visibility
- "Designing Data-Intensive Applications" by Martin Kleppmann (data modeling and stream processing concepts that apply to frontend)
- Linear and Notion engineering notes on scaling data surfaces

This skill covers the core patterns for making data feel calm and fast. It has solid coverage of virtualization, rendering primitive choice, and atomic updates, but is flagged for future expansion on advanced real-time streaming, complex brushing/linking across multiple views, and more specialized chart interaction patterns. 

Use it as the primary reference when building tables, lists, or visualization surfaces that users will spend significant time scanning or manipulating.