# Devtool landing page anatomy

Section-by-section structure for a Linear/Vercel-style marketing page. Sources:
- linear.app's 2026 production HTML and CSS
- Rauno Freiberg's write-ups of the Vercel homepage ("What will you ship?") and the Next.js site
- the Frontend FYI "Rebuilding Linear's homepage" series (the 2022-era site)
- LogRocket's "Linear design" analysis
- Manu Arora's landing-page reviews

## The governing idea
"A landing page isn't supposed to show how much you can design. It's supposed to help someone make a decision" (Manu Arora). The strongest pages he reviewed had "a clear headline, product visible early, good spacing, proof where it mattered, and one obvious action." He faults AI-generated pages for centered layouts, uniform visual weight, vague copy and excessive animation (paraphrased). Those are exactly the defaults to resist.

The Linear-style layout (LogRocket) is **sequential and one-dimensional**: one column of acts, with no zig-zagging content, consistently aligned text, minimal CTAs and minimal subject matter.

## Page skeleton
```
Header (sticky, transparent → hairline + blur on scroll)
Hero: pill link · H1 · subhead · CTA pair · product UI
Proof: logo strip (monochrome) or one stat
Act 1…n: section header (two-tone) + product crop / bento / demo
Quiet interlude (text-only statement, changelog, quote)
Final CTA
Footer
```
Vertical rhythm: 128–256px between acts, 64px inside them. Parents own spacing; components carry no outer margin.

## Header
- 56–72px tall, max-width matching the page (1024–1200px), logo left, 4–6 links, CTAs right ("Log in" ghost + "Sign up" invert pill, small size).
- It starts transparent over the hero. After scrolling (toggle `html[data-scrolled]` from a scroll listener or an IntersectionObserver sentinel), it becomes `background: rgb(11 11 11 / 0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgb(255 255 255 / 0.08)`, over a ~160ms transition.
- Dropdowns: bridge the gap between trigger and panel with an invisible pseudo-element, so the panel doesn't close in transit. On first open, animate only opacity (no size morph from stale values), then morph between panels.
- Mobile: a full-screen sheet. Links rise in with a short stagger. Lock scroll.

## Hero
- **Pill link** above the H1: "New · Feature name →", 28px tall, secondary glass style, with an 8%-white inner "highlight" pill for the arrow.
- **H1:** 5–8 concrete words. Weight 500–510 (Linear) or 600 (Geist), tracking −0.022em to −0.04em, line-height 1.0–1.1, size `clamp(40px, 6vw, 72px)`, max ~16ch, `text-wrap: balance`. A whisper gradient (white → ~70% white) at most. Linear's 2026 hero is plain primary text with a line-by-line blur-in.
- **Subhead:** one or two sentences in the secondary/tertiary tier, 17–20px, max ~40ch. Say what it is and who it's for ("Purpose-built for planning and building products").
- **CTAs:** one primary (inverted light pill, or the brand fill) and one secondary (ghost or glass, often "Docs" or a copyable install command). Never three.
- **Product UI as the hero image.** Linear builds a 1320×720 app replica in HTML/SVG (12px radius, 8px frame padding, 232px sidebar) instead of a screenshot: it's crisp at any DPR, themable, and can animate. Otherwise use a real, current screenshot at 2× in a frame:
  - `rounded-[12px]`, a 1px border at 8% white, and a subtle top sheen
  - a mask fading the bottom edge into the page
  - optionally a gradient 1px border via mask-composite
  - optionally a `perspective: 2000px` tilt from `rotateX(25deg)` that flattens when 40% in view (the 2022 Linear hero)
- **Light:** one soft source behind the product (a radial glow at ≤0.15 alpha of the brand hue, or 3–8% white), faded with an eased gradient. The rebuild's version: a conic multi-blue glow at `blur(120px)` flaring to full then settling at 20% opacity over 4s. Pick one light source, not three.
- **Entrance:** stagger pill → H1 → subhead → CTAs → product at ~0.2s steps with 10–20% `translateY`, opacity and (for the H1) blur 10px → 0 over ~1s. It plays once per session, and not on back-navigation.
- Performance: no client JS required for the core hero visual. Shaders and canvas effects fade in after load and are skipped on low-power devices. The product image is `fetchpriority="high"` with fixed dimensions.

## Proof
- Logo strip: 5–8 monochrome logos (`filter: grayscale(1) brightness(4)` on dark, ~50–60% opacity), 2 per row on mobile (hide half), with even optical sizes (normalize by height *and* visual weight).
- A two-tone lead-in above them: "Powering the world's best product teams." (muted) + "From next-gen startups to established enterprises." (bright).
- An infinite marquee is fine only if it's slow (40s+), masked at the edges, pauses on hover, and marks its duplicated clones `aria-hidden` and `inert`.

## Feature acts
- **Section header:** an eyebrow (13px, accent or mono), a two-tone H2 (bright lead sentence + muted continuation), max 16–18ch, then optionally one supporting line.
- **Formats that work:**
  - **Product crop + text:** crop one interaction from the real UI, let it bleed off one or two edges, and fade it with a mask.
  - **Bento** (see `bento-grids`): 4–7 cells, one hero cell, one idea per cell.
  - **Live demo:** a working widget (command menu, keyboard shortcut cycler, scrubber) inside the page. Nothing sells a devtool like touching it.
  - **Feature grid:** 2 columns on mobile, 3 on desktop, icon + "**Title.** muted description" lockups, 14–16px.
- **Per-section color pairs** (from the 2022 Linear rebuild): each act gets `--feature-color` and `--feature-color-dark` RGB triplets used at 0.1–0.15 alpha for its glow and card washes. This keeps one hue per act instead of rainbow everywhere.
- **Rhythm:** alternate high-novelty sections (a big animated demo) with calm ones (text and a static crop). Never put two high-novelty sections back to back. Ration signature motifs (grid lines, crosshairs, glows) so each appearance means something.

## Grid and guides (Vercel)
- A 1080px grid of 360px columns (3 × 360) gives "a readable line-length for 14–16px text". Crosshair `+` marks at intersections echo print registration marks.
- Keep the grid in the same position across pages so navigation feels like the content swapped rather than the page reloaded.
- Build guides with `display: contents` so they render even for empty cells and survive auto-placement (see `bento-grids` → drawn grids).
- Dashed rules: an absolutely positioned 1px element with `linear-gradient(to right, var(--line) 50%, transparent 0)` at `background-size: 5px 1px`, bleeding past the container and masked at both ends.

## Depth and framing ("dirty the frame")
A product shot floating alone reads as "a seemingly sloppy afterthought" (Rauno). In order:
1. Blur or dim the inner background to push it back.
2. Fade the bottom edge so the boundary feels infinite.
3. Add offset duplicate frames or out-of-focus objects that *reinforce the message* (many preview deployments, many issues), never generic decoration.

## Final CTA and footer
- The final CTA repeats the hero's primary action with a short, confident line ("Plan the present. Build the future."). One button, maybe a secondary.
- Footer: a 1px top hairline, 56px of vertical padding, 4–5 link columns (titles 13–14px medium, links in the tertiary color, turning primary on hover), a small status indicator (a green dot and "All systems normal") and a theme switcher.

## Copy
- Concrete nouns and verbs, no jargon. "Clarity is a competitive advantage."
- Headlines state the outcome. Subheads state the mechanism.
- Numerals for stats (`55% faster`), non-breaking spaces in `10 MB` and `⌘ K`, `…` not `...`.
- Buttons are verb + noun. Vercel uses sentence case on marketing pages ("Start building", "Read the docs") and Title Case in product UI. Pick one convention per product and keep it.
