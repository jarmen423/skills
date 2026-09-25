---
name: bento-grids
description: How to design and build bento grid sections — the asymmetric feature-card grids on Apple, Linear, Vercel and Raycast pages — so they tell one product story and stay scannable. Covers content-first hierarchy, cell count and ratio limits, cell anatomy and headline lockups, dark surfaces, CSS Grid templates with per-breakpoint areas, gap and radius math, container queries, responsive collapse and accessibility. Use whenever building or critiquing a features section, bento, card grid, USP or stats grid, even if the user just says feature cards or asks to make a section more interesting.
---

# Bento grids

A bento grid is a *hierarchy you already have*, drawn with area. "The pattern doesn't generate priority on its own—it expresses a priority you already have" (Deck.gallery on Apple's keynotes). So the work starts with the content, not the grid. Apple's iPhone slide makes the camera largest, then titanium, then A17, and "a reader scanning the slide for two seconds takes away 'camera, titanium, A17'." Your grid should pass the same two-second test.

## 1. Decide the story first
Write the cells as a list before touching CSS:
1. **Thesis (the hero cell):** the one capability you want remembered, shown with real product UI or a live demo. There's exactly one; two is the limit, and "three hero tiles cancel each other out."
2. **Proof (medium cells):** 2–4 supporting claims: speed, integrations, a stat, collaboration.
3. **Close (small or accent cell):** a CTA, a trust signal or "read the release notes".

Then apply the limits:
- **5–9 cells** for a feature section. Going to ~12 only works if the extras are single-token stat cells (Axiom).
- **At most 3 footprint ratios** (1×1, 2×1, 1×2, 2×2; occasionally 3×1). More reads as chaos.
- **Size encodes importance, not word count.** Never size a cell to fit its copy.
- **One idea per cell.** Content density shrinks with the cell: "Small tiles = one idea only. Cut copy if it doesn't fit; don't shrink font."
- **0–2 saturated cells**, placed first or diagonally. Everything else is a neutral surface. Every cell in a different color is the "primary school classroom" effect.
- **Don't use a bento** for sequential steps, long-form text, catalogs or data tables.

## 2. Pick a proven layout
| Template | Shape | Use when |
|---|---|---|
| **Mirrored brick** | 7+5 / 5+7 (or 8+4 / 4+8) on 12 columns | The default for devtools (Copilot, Attio, Linear). Four cells, diagonal tension |
| **Hero + trio** | 12 / 4+4+4 | One feature clearly dominates (Raycast). The hero may break its top edge |
| **Textbook 2×2 hero** | `hero hero a` / `hero hero b` / `c d e` on 3 columns | 5–6 cells with a clear #1 |
| **Two over three** | 6+6 / 4+4+4 (or 3+3 / 2+2+2 on 6 columns) | Five peers with a light hierarchy (Mintlify) |
| **Tall sides** | `a b c` / `a d c` | Content that bleeds off the bottom (phone, editor) |
| **Staggered tall** | 3×4 with tall cells offset per column | 8–9 small monochrome features (Clerk). No row line crosses all columns |
| **Drawn grid** | 2×2 with 1px rules and `+` crosshairs, no card surfaces | A Vercel-style editorial feel |
| **Bento-as-hero** | A center CTA cell ringed by stat cells | A pricing or one-number story (Axiom) |

Full CSS for each (plus the Linear areas-as-data component) is in `references/templates.md`. Read it before implementing.

## 3. Cell anatomy
```
┌ cell ── surface · 1px border · radius R · overflow: clip · container-type: inline-size
│  ├ media slot  (≈60–70% of height): product UI crop / live demo / stat / illustration,
│  │              usually absolute, bleeding off 1–2 edges, faded with a mask
│  └ text slot   anchored bottom (default) or top: [eyebrow] title + 1–2 line body [+ link]
```
- **Title:** 1–6 words, 15–26px (devtool cells run smaller and lighter than generic guides suggest: Linear used 26px regular, Clerk ~15px medium).
- **Body:** 1–2 lines, 14–16px, in the muted text tier. Cap it at ~310px (the Linear rebuild's `max-w-[31rem]` was on a 62.5% root, where 1rem is 10px) or `max-w-prose`.
- **Padding:** 1×1 ≈ 20px, 2×1 ≈ 24px, hero 32–56px. Visual→title gap 12–16px, title→body 8px.
- **Product UI crops, never whole screenshots.** Crop to one interaction. Make the image *larger than the cell* and position it absolutely (`width: 200%`, `top: 40%`) so it can't resize the track, then fade it: `mask-image: linear-gradient(black, transparent 70%)`.
- **Align what repeats:** anchor text slots consistently per row (all bottom or all top). Put `flex: 1` on the text block (iamsteve's trick) so the media lines up across cells whose copy differs in length, or use subgrid when titles themselves must align.

**Headline lockups.** Pick one per grid and don't mix three:
1. **Title + muted body**, stacked (Linear, Supabase, Raycast).
2. **Bright lead + muted continuation** in one paragraph: `<p><strong class="text-primary">Best practices, built in.</strong> <span class="text-tertiary">Static analysis that…</span></p>` (Vercel, Attio, Neon).
3. **Muted setup → bright payoff:** "Empower your team to solve bigger problems with **Copilot for Business**."
4. **Eyebrow + headline:** an accent 13px label above a white headline (Linear Asks).
5. **Stat:** an optional small setup, a *huge* numeral (unit at 40–60% size, or in another color), and a small muted caption. "The loudest type isn't a headline. It's a number."

## 4. Surfaces (dark devtool)
- The cell is **barely there**: one step above the page, with the border doing the separating. Linear's rebuild: `border: 1px solid rgb(255 255 255 / 0.08); background: linear-gradient(rgb(255 255 255 / 0), rgb(255 255 255 / 0.05))`, invisible at the top and lifted at the bottom where the text sits.
- **Frame-in-frame bezel:** an outer frame (`p-2`/`p-3`, radius R) holding an inner card (radius R − padding). The concentric radii read as machined.
- **Grouped outer radius** (Mintlify, Tailwind UI): only the corners on the grid's outer edge get the big radius (~32–40px), and inner corners stay small (~8–16px), so the whole grid reads as one object. Recompute the corners at each breakpoint.
- **Gradient 1px border:** a `::before` with `padding: 1px`, a top-to-bottom white gradient, and `mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); mask-composite: exclude`.

## 5. Geometry that holds together
- **Columns:** `repeat(12, minmax(0, 1fr))`. The `minmax(0, …)` matters: plain `1fr` means `minmax(auto, 1fr)`, so a long URL or code block can blow the track open. Put `min-width: 0` on flex children in cells too. (Tailwind's `grid-cols-*` already uses `minmax(0,1fr)`.)
- **Gap:** identical everywhere, between ½ and 1× the cell radius (24px radius → 12–24px gap). Desktop 16–32px, tablet 12–16px, mobile 12px.
- **Radius:** 16–24px is standard; marketing heroes go to 32–48px. **Nested radius = outer − padding**, floored at about 4px. When padding ≥ radius, adjust by eye.
- **Rows:** either fixed row heights (`grid-auto-rows: minmax(280px, auto)`) *or* `aspect-ratio` on cells, never both. Release fixed heights below desktop.
- **Placement:** use `grid-template-areas`, not nth-child line numbers (they're brittle), and not `grid-auto-flow: dense` for anything with a reading order (it breaks DOM↔visual order for screen readers and keyboard users). Keep `dense` for decorative, order-free sets only.
- **Declare each breakpoint's layout as data with a fixed DOM order.** This is Linear's production pattern:
  ```css
  .bento { display: grid; gap: var(--gap, 24px);
    grid-template-columns: repeat(var(--cols, 12), minmax(0, 1fr));
    grid-template-areas: var(--areas); }
  @media (max-width: 1024px) { .bento { grid-template-areas: var(--areas-md, var(--areas)); } }
  @media (max-width: 640px)  { .bento { --cols: 4; grid-template-areas: var(--areas-sm, var(--areas)); } }
  ```
  ```html
  <div class="bento" style="--areas:'a a a a a a a b b b b b' 'c c c c c d d d d d d d';
                            --areas-sm:'a a a a' 'b b b b' 'c c c c' 'd d d d'">
  ```
- **Container queries inside cells** make each cell adapt to its *own* width, not the viewport:
  ```css
  .cell { container: cell / inline-size; }
  .cell h3 { font-size: clamp(1rem, 0.9rem + 1.2cqi, 1.625rem); }
  @container cell (min-width: 32rem) { .cell-body { flex-direction: row; } }
  @container cell (max-width: 20rem) { .cell p { display: none; } }   /* 1×1: drop the body line */
  ```
  Art-direct media per container size (`object-fit: none` + `object-position`, and a different `aspect-ratio`) rather than scaling a screenshot down until it's illegible.
- **Subgrid** (`grid-template-rows: subgrid; grid-row: span 3`) aligns visual, title and body across cells that share row tracks, e.g. a uniform bottom row. Don't force it onto mixed-height cells.

## 6. Responsive collapse
1. **Write the DOM in mobile reading order**, hero first, and re-map areas per breakpoint. Never use `order` to move the hero.
2. Columns go 12 → 8 (≤768px) → 4 or 1 (≤640px). The hero stays full width. Pairs of 1×1s stay paired on tablet, and a 7/5 brick becomes 12/12.
3. Release fixed row heights, but **vary the stacked heights** (important cells taller) so a single column doesn't read as a list.
4. Hide purely decorative cells, or turn a row into a **horizontal scroll-snap carousel** (Linear's rebuild): `display:flex; overflow-x:auto; scroll-snap-type:x mandatory` with cells `flex: 0 0 85%; scroll-snap-align: center`, the scrollbar hidden by a clipping parent, and edge padding so the first and last cells can center.
5. Recompute grouped outer radii for the stacked order.

## 7. Motion and interaction
- **Hover:** at most 1–2 properties, 200–300ms ease-out, gated by `@media (hover: hover) and (pointer: fine)`. Good options:
  - a border brighten
  - a pointer spotlight (see `signature-effects`)
  - a hidden secondary link rising in from `translateY(30%) scale(.8); opacity: 0`
  - text nudging `translateX(8px)`

  Don't lift, scale, glow and tilt all at once.
- **Entrance:** a short stagger (50–80ms per cell) on first view only (`once: true`), 8–16px rise plus fade. Or none at all: a bento that's simply there is fine.
- **Live cells** (auto-cycling shortcuts, a looping demo) run only while in view, pause on hover and focus, stop under reduced motion, and never carry information that's only available while animating.

## 8. Accessibility
- The section is a `<section aria-labelledby>` with a real heading. Each standalone cell is an `<article>` (or `<li>` in a `<ul>`) with its own heading level.
- DOM order = reading order = mobile order. Decorative art and icons get `aria-hidden="true"`. UI built in HTML inside a cell gets `role="img"` + an `aria-label` describing what it shows, with `aria-hidden` inside.
- Interactive cells have a visible focus ring, and if the whole cell is a link, use one `<a>` with the heading as its accessible name (not nested links).
- Text on colored or image cells meets contrast (check the darkest gradient stop).

## Checklist
- [ ] One hero cell, first in the DOM. 5–9 cells. ≤3 footprint ratios on a shared column grid
- [ ] Each cell carries one idea. 1×1 cells: title ≤6 words, body ≤2 lines
- [ ] Media is a cropped, masked product UI or a real demo, taken out of flow so it can't resize tracks
- [ ] `minmax(0,1fr)` tracks. Equal gaps (½–1× radius). Nested radius = outer − padding
- [ ] Areas declared per breakpoint. Explicit mobile order (or carousel). Container queries inside cells
- [ ] 0–2 saturated cells. The rest are neutral surfaces one step up with an 8–10% white border
- [ ] One lockup style across the grid. Text slots anchored consistently
- [ ] Hover ≤2 properties, gated. Entrance once. Live demos pause off-screen and under reduced motion
- [ ] `<section>` + `<article>`s, DOM = reading order, decorative `aria-hidden`, focus visible

## In this repo (agent-memory-labs-frontend): current state, context not constraints
`src/components/home/bento.tsx` is a 7-cell bento on `lg:grid-cols-6` (`md:grid-cols-2`):
- rows run 4+2 / 2+2+2 / 3+3
- every cell is a `SpotlightCard` with `p-6`
- the cells use live demos (the time-travel scrubber, the hover-able knowledge graph, a code-intel popover) and the `CardText` title + muted-body lockup

This is the starting point, not a template to preserve. A redesign can replace it with a different layout or a different story, or drop the bento entirely if another format tells the product story better. Whatever you build, the rules above apply to the new version (one hero, at most three footprints, one lockup style), and decorative animation goes behind `motion-safe:`.
