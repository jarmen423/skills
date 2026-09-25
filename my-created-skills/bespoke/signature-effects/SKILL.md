---
name: signature-effects
description: How to build and budget decorative effects on marketing pages — spotlights, masked grid and dot backgrounds, light beams and lamps, border glows, pointer-tracked card lights, SVG beam pulses, grain, edge fades, tilt and glare, blur-in text, orbs and canvas fields — without effect soup, jank or accessibility failures, distilled from Aceternity UI's source and the Linear, Vercel and Cursor effects it recreates. Use when asked for a hero background, glow, beam, shimmer, sparkles, aurora or animated border, when adapting an Aceternity or Magic UI component, or when a page has heavy decorative animation. Product-UI transitions belong to interface-motion.
---

# Signature effects

Effects are the most visible and least important part of a devtool page. Linear, Vercel and Cursor each have one or two signatures (a lamp, a glare card, a border glow) and use them sparingly against calm, dark surfaces. Aceternity UI rebuilt those signatures as copy-paste components. Its creator, Manu Arora, is clear about how to use them: **"good animation should support the interface, not become the interface"** and "the best animation usually isn't the one you notice." He also criticizes AI-generated landing pages for their uniform visual weight, vague copy and excessive animation (paraphrased from his posts).

The job is to pick the right effect, build it cheaply, and make it removable.

## 1. The effect budget (decide before building)
1. **One hero effect per viewport.** Choose a single light source or motion signature (spotlight, beams, lamp, aurora *or* orbs). Everything else is static texture (grid, dots, grain) plus local hover micro-interactions. Aceternity's demos show each effect alone; "effect soup" comes from stacking the demos.
2. **Ambient loops are slow and faint.** Periods of 7s or more (beams 10–20s, orbs 20–40s, aurora 60s), light alphas ≤0.2, strokes ≤0.4, and random phase offsets so nothing pulses in sync.
3. **Interaction effects stay local.** Spotlights and glows appear only on the hovered card, only for fine pointers (`@media (hover: hover) and (pointer: fine)`), and ease in (~300ms).
4. **Decoration never carries information.** The page must read fully with every effect removed, because that's what reduced-motion and low-power users get.
5. **Match the effect to the product and re-tint it.** Copied verbatim (cyan `#18CCFC` → indigo `#6344F5` → violet `#AE48FF`, `from-neutral-200 to-neutral-500` headlines, `bg-black/[0.96]`), these read as "Aceternity template". Re-tint to the brand's palette and re-time to its motion personality.
6. **The restraint test:** if you removed the effect, would anyone notice anything but less noise? If not, remove it.

## 2. Choose a primitive
Nearly every effect is one of these. Code for each is in `references/primitives.md`.

| Primitive | Looks like | Cost | Notes |
|---|---|---|---|
| **Masked pattern** (grid / dots) | Fine grid or dot field fading to the edges | Free (static) | Lines `#171717`–`#262626` on black, 20–64px cells. Mask the pattern itself with a radial gradient |
| **Static light source** (blurred ellipse, soft cone, conic lamp) | A spotlight beam or lamp from above | Cheap if static | Blur once, animate only transform and opacity. Peak alpha ≤0.2 |
| **Pointer spotlight** (radial mask or background at the cursor) | A card lights up under the pointer | Paint per move | CSS vars on the element (not `:root`), coalesced with rAF, never React state |
| **Border glow ring** (conic arc isolated to the 1px border) | A light arc on the card edge that faces the pointer or rotates | Paint per frame while animating | `mask-composite: exclude` ring and `@property --angle`. Few cards only |
| **Path-following blob** | A glow circling a button's border | JS per frame | Prefer the conic ring or `offset-path` |
| **SVG beam / traveling pulse** | Hairlines with light pulses running along them | Moderate | A faint static rail plus a `pathLength="1"` dash pulse. 0.5–1.25px strokes |
| **Grain** | Film texture, anti-banding | Free (static) | Opacity 0.05–0.1, overlay blend. Never animated |
| **Edge-fade masks** | Content dissolving at the edges | Free | Use them everywhere decorative layers meet containers |
| **Tilt / parallax / glare** | Cards tilting toward the pointer | Transform per move | Direct `style.transform` writes, subtle angles, ease in then track 1:1 |
| **Blur-in text** | Headline materializing word by word | Filter on few spans | Hero only, once. Total ≤1s. Keep the real text for screen readers |
| **Distance ripple** | A wave across a tile grid from the click | Pure CSS | Per-cell `--delay: distance × 55ms` |
| **Canvas field** (dots, stars, particles) | A living background | rAF loop | DPR ≤2, pause off-screen and in hidden tabs, one static frame under reduced motion |
| **Orbs / aurora** | Drifting colored clouds | The most expensive | Blur the container once, animate only blob transforms, consider a static image |

## 3. Engineering hygiene (every effect, every time)
Aceternity's source is a catalog of good ideas with production gaps: only 1 of ~45 components handles reduced motion. When you adopt or write any effect, fix these:
- [ ] **Reduced motion:** loops stop or become static, and pointer effects are disabled or static. `MotionConfig reducedMotion="user"` doesn't stop CSS keyframes, rAF or canvas loops, or motion values you set by hand, so gate those yourself.
- [ ] **No React state on high-frequency events.** Pointer and scroll values go to Motion values (`useMotionValue` + `useMotionTemplate`) or direct `el.style` writes, coalesced to one per frame.
- [ ] **No layout properties animated** (`width` in a lamp → `scaleX`). No `background-position` on big blurred layers. No blur *tweens* on large areas (crossfade a pre-blurred copy instead).
- [ ] **No layout reads in loops** (`getBoundingClientRect` polling, `getTotalLength` per frame). Cache and refresh with ResizeObserver.
- [ ] **No `Math.random()` in render.** It causes a Next.js hydration mismatch. Generate after mount, or use a seeded PRNG.
- [ ] **Unique SVG ids per instance** via `useId()` (`id="gradient"` / `id="filter"` collide across instances).
- [ ] **Offscreen and hidden-tab pause** for loops and canvases (IntersectionObserver + `visibilitychange`). Cancel rAF, don't spin it.
- [ ] **Decorative layers:** `aria-hidden="true"` and `pointer-events: none`. Marquee clones get `aria-hidden` + `inert`.
- [ ] **Contrast:** gradient text is checked at its darkest stop and has a solid fallback `color`. Text over animated backgrounds gets a scrim or halo. Glow doesn't count toward contrast. Body copy uses neutral-400-ish, not neutral-500, on near-black: `#737373` on `#0a0a0a` is only 4.18:1.
- [ ] **At most one WebGL context per page.** No 600KB three.js dependency for a hover sparkle.
- [ ] **Keyframes shipped with the component** (in Tailwind v4, `@theme inline { --animate-x: …; @keyframes x {…} }`). Copying TSX without its keyframes renders nothing, silently.
- [ ] **WCAG 2.2.2 (Pause, Stop, Hide, level A):** anything that starts moving on its own, lasts more than 5s, and sits alongside other content needs a visible way to pause, stop or hide it, or must stop by itself within 5s. Honoring `prefers-reduced-motion` is also required (it's the technique for 2.3.3), but it doesn't satisfy 2.2.2 on its own. Marquees also pause on hover and focus.

## 4. Adapting an Aceternity (or similar) component
1. Fetch the source from the registry (`https://ui.aceternity.com/registry/<name>.json` → `files[].content`) and copy its keyframes from the docs page's Tailwind v4 tab.
2. Fix imports to match the project (`motion/react` ↔ `framer-motion`; the v12 APIs are identical).
3. Run the hygiene checklist above. Most components need reduced-motion handling, `useId`, and state → motion-value fixes.
4. Re-tint to the design tokens, calm the alphas down, and slow the loops.
5. Check it at 320px wide, in Safari, and with reduced motion on.

## 5. Where effects belong on a page
- **Hero:** one light source + one static texture (grid or dots, masked) + the product UI. Optionally blur-in the headline once.
- **Feature cards:** a pointer spotlight or border glow on hover, for fine pointers. Nothing ambient.
- **Section dividers:** a gradient hairline (`linear-gradient(to right, transparent, rgb(255 255 255 / 0.1) 50%, transparent)`), or a sunrise horizon (a giant ellipse with a 1px top border in the brand color at 40% over a radial glow).
- **CTA band:** a masked grid plus a faint glow is plenty.
- **Never:** effects in product UI (dashboards, settings, forms). The devtool look inside the app is calm surfaces and instant feedback.

## References
- `references/primitives.md`: minimal, dependency-light implementations of every primitive above (CSS-first, with React/Motion variants), plus the values Aceternity ships for each (durations, alphas, blur sizes, palettes), and the Glare Card "ease in then track" trick.

## In this repo (agent-memory-labs-frontend)
The effects already present, all in `src/app/globals.css`:
- `.spotlight`: a pointer-tracked border and fill light, driven by `--mx` and `--my`, which `SpotlightCard` writes on the element
- `.bg-grid`: a 64px grid at 4.5% white
- `.bg-dots`, `.mask-radial`, `.mask-fade-y`
- `.glow-ambient`: a radial glow tinted by the local hour through `--ambient`
- `.text-sheen`, `.shimmer-text`
- the `animate-beam` SVG pulse (used with `motion-safe:` in `home/bento.tsx`)

The hero already stacks three soft glows plus the masked grid: the `glow-ambient` layer in `src/app/page.tsx`, and in `home/hero-preview.tsx` a blurred hour-tinted glow and an amber one. Together they read as one ambient light, which is already the budget. Don't add another. If you touch the hero, consider consolidating them. `SpotlightCard` writes `--mx`/`--my` straight from `pointermove` without rAF coalescing. It's fine at this scale, but add rAF coalescing if many cards animate at once.
