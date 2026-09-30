# Layout, Composition, Visual Hierarchy & Spacing Systems

> Dedicated content skill for building interfaces that feel premium, calm, and trustworthy through disciplined layout systems that also stay fast and resilient.

**Core Mandate**  
Great layout is invisible architecture. It makes users feel smart because they can predict where things are, while the browser stays fast because the rules are declarative and compositor-friendly. Visual hierarchy should emerge from the layout system itself (Grid, subgrid, spacing tokens, typographic scale) rather than being repeatedly painted on with custom CSS or JavaScript measurement.

## When to Use This Skill

Use this skill when an agent is:
- Establishing spacing systems, grids, or visual hierarchy for a new product or design system
- Building dense productivity interfaces (dashboards, tables, editors) that must feel calm
- Creating marketing pages or brand storytelling with asymmetric but disciplined composition
- Fighting Cumulative Layout Shift (CLS) or layout thrashing
- Trying to make an interface look premium without heavy JavaScript-driven measurement or reflow

## Core Principles

1. **Hierarchy emerges from the system, not decoration.** Use a strict spacing scale, typographic modular scale, and tokenized surfaces so visual weight comes from position, size, and contrast — not from adding more effects.
2. **Reserve space aggressively.** Images, media, and dynamic content must have explicit dimensions or aspect-ratio boxes. CLS is a trust and performance problem, not just a metric.
3. **Prefer declarative CSS over JavaScript measurement.** Container queries, subgrid, CSS Grid, and `content-visibility` solve many problems that teams used to reach for ResizeObserver or `getBoundingClientRect` for.
4. **One compositional grammar across contexts.** Marketing pages and dense application surfaces should share the same underlying spacing, grid, and hierarchy system so brand expression doesn't become a parallel styling universe.
5. **Calm over loud.** Great layout feels quiet because only a few things are truly loud. Most elements should support the primary content, not compete with it.

## Key Patterns & Techniques

### 1. Strict Spacing & Typographic Scales
Use a 4-point or 8-point spacing scale and a clear modular type scale (major-third or perfect-fourth). Map these to design tokens / CSS variables so they are consistent and cheap to change.

**Linear pattern:** Very tight 4 pt base spacing because the UI is scanned, not read. Consistent vertical rhythm makes high-density interfaces feel calm.

**Shopify Polaris / GitHub Primer:** Generous but predictable padding inside cards, clear separation between data-dense areas and action areas.

### 2. CSS Grid + Subgrid + Container Queries (Modern Baseline)
- Use CSS Grid for two-dimensional control with fractional units (`fr`) instead of calculating pixel widths in JavaScript.
- Subgrid lets nested regions inherit track logic so alignment comes from layout primitives.
- Container queries let individual components respond to their parent’s width instead of the viewport. This is both a performance and maintainability win.

**Netflix container queries case study:** Framed as a performance and maintainability improvement, not just responsive design convenience.

### 3. Preventing Cumulative Layout Shift (CLS)
- Always reserve space for images and media with explicit `width`/`height` or `aspect-ratio`.
- Use `next/image` or equivalent with proper `sizes` and priority on LCP images.
- Self-host fonts or use `font-display: swap` + preload critical fonts.
- Never inject dynamic content (ads, CTAs, notifications) above already-rendered text without reserving space.

### 4. Asymmetric but Disciplined Composition (Marketing Surfaces)
Marketing pages can use overlapping cards, angled containers, and high-contrast sections, but they must still be pinned to a rigid underlying grid. The delight comes from intentionality, not chaos.

**Vercel marketing pages:** Overlapping elements and editorial feel achieved while keeping everything on a disciplined grid system. Asymmetric heroes are static or GPU-parallax only.

### 5. Layered Contexts Without Visual Chaos
Complex tools (Figma, Linear, Notion) layer multiple contexts (toolbar, properties panel, canvas, layers panel). Each panel should be a self-contained layer with consistent internal spacing. The canvas or primary content area should feel like the focal point.

**Figma UI:** Floating panels over WebGL canvas with strict 8 pt spacing tokens. Each panel is isolated so edits inside the canvas don’t invalidate outer UI layout.

### 6. Content-Visibility & Stable Layout for Dense Interfaces
Use `content-visibility: auto` on off-screen panels, long lists, and below-the-fold sections. Combine with stable row heights in lists so the browser can skip layout work for content the user hasn’t reached yet.

## Production Examples (Delight + Performance)

**Linear Interface Density**  
Delight: High information density that still feels calm and scannable. Every list row is the same height; hover states are composited.  
Performance: Strict 4 pt spacing scale + CSS Grid/Flexbox. Only `transform`/`opacity` animate. No DOM measurement during interactions. Lists are virtualized where needed.

**Vercel Marketing & Dashboard Composition**  
Delight: Editorial, asymmetric marketing pages that still feel premium and intentional. Dashboard feels airy and clear.  
Performance: Asymmetric elements pinned to rigid grid. `will-change` used sparingly on focused elements only. WebP/AVIF images served at exact display sizes. No layout shifts from fonts or images.

**Stripe Dashboard & Connect Pages**  
Delight: Sophisticated but light and simple. Strong visual hierarchy through spacing and color rather than heavy effects.  
Performance: CSS Grid for layout. Gradient surfaces and depth created with CSS gradients and pseudo-elements instead of continuous JavaScript canvas work. Fixed sidebar + readable prose column with `scroll-margin-top`.

**Notion Block-Based Layout**  
Delight: Minimalist canvas where user-generated content remains the absolute focal point. Visual hierarchy comes almost entirely from whitespace, indentation, and typography.  
Performance: Every block is an isolated React component using efficient flexbox. Predictable padding/height math enables virtualization and cheap re-renders.

**Figma Canvas + Panels**  
Delight: Multiple contexts (toolbar, properties, layers, infinite canvas) layered without visual chaos.  
Performance: UI layer floats deterministically over WebGL canvas. Layout calculations are highly decoupled from the heavy rendering surface.

**Apple Product Pages**  
Delight: Cinematic storytelling through massive imagery and precisely choreographed scroll reveals.  
Performance: Heavy pre-production asset pipeline. Videos are short and compressed. Scroll handlers are throttled and drive only `transform`/`opacity`. Excellent `prefers-reduced-motion` fallbacks.

**Airbnb Card Grids**  
Delight: Consistent rhythm and scanability across search results.  
Performance: Strict aspect-ratio containers on images prevent CLS. Each card can be composited independently.

**GitHub Primer Design System**  
Delight: Clear, reusable product language for hierarchy and spacing across the entire platform.  
Performance: Spacing and typography tokens map directly to utility classes. No runtime computation of layout values.

## Anti-Patterns to Avoid

- JavaScript-driven measurement and animation of `width`, `height`, `top`, or `margin` for things CSS Grid, Flexbox, or container queries can already solve
- Font strategies that create FOIT or CLS (especially variable fonts without proper fallbacks)
- Decorative translucency or heavy backdrop filters that muddy hierarchy and cost GPU/battery
- Card-heavy interfaces where every block tries to be primary
- Asymmetric composition without an underlying rigid grid (feels chaotic rather than intentional)
- Injecting dynamic content above the fold without reserving space
- Using many different component idioms and spacing systems on the same surface

## Further Reading & Authoritative Sources

- **Refactoring UI** by Adam Wathan & Steve Schoger (especially chapters on hierarchy, spacing, and layout)
- web.dev — Optimize Cumulative Layout Shift (CLS), Optimize INP
- MDN — Subgrid, Container Queries, and CSS Grid guides
- Netflix container queries case study
- Stripe Connect and accessible color system engineering posts
- Apple Human Interface Guidelines — Layout and Materials
- Material Design 3 — Applying layout and spacing tokens
- Josh Comeau — Interactive Guide to CSS Transitions and CSS Variables
- Patterns.dev — Virtualize long lists and avoid layout thrashing
- Vercel Geist design system (live reference for asymmetric marketing + tight dashboard spacing)
- Linear design system (live reference for dense productivity UI)

This skill contains the layout and composition patterns used by Linear, Vercel, Stripe, Figma, Notion, Apple, and Airbnb to create interfaces that feel both premium and fast. Use it when establishing the foundational visual structure of a product or design system.