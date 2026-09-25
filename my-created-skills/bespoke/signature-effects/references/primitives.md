# Effect primitives

Minimal implementations, CSS-first. Each primitive lists the Aceternity components built on it and the values those components ship with, so you can match the look without importing the component and its problems. The code is written to pass the hygiene checklist in SKILL.md.

## Contents
P1 Masked pattern background · P2 Pointer spotlight · P3 Static light sources · P4 Border glow ring · P5 Path-following blob · P6 SVG beams and pulses · P7 Grain · P8 Edge fades · P9 Tilt, parallax, glare · P10 Blur-in text · P11 Distance ripple · P12 Canvas field · P13 Orbs and aurora · P14 Bezel surfaces · P15 Gradient hairlines and horizons

---

## P1. Masked pattern background (grid / dots)
Aceternity: Grid and Dot Backgrounds, the Spotlight hero, Hero Highlight. Lines `#e4e4e7` (light) / `#262626` (dark), 40px (20px "small"). The Spotlight hero goes quieter, at `#171717` on `bg-black/[0.96]`.
```css
.grid-bg { position: absolute; inset: 0; pointer-events: none;
  background-image:
    linear-gradient(to right, var(--grid-line, rgb(255 255 255 / 0.05)) 1px, transparent 1px),
    linear-gradient(to bottom, var(--grid-line, rgb(255 255 255 / 0.05)) 1px, transparent 1px);
  background-size: 40px 40px;
  background-position: -1px -1px;                       /* align lines to the container edge */
  mask-image: radial-gradient(ellipse 60% 50% at 50% 0%, #000 30%, transparent 100%); }
.dot-bg { background-image: radial-gradient(var(--dot, rgb(255 255 255 / 0.12)) 1px, transparent 1px); background-size: 20px 20px; }
```
Mask the pattern layer itself rather than painting an opaque overlay, so it works over any background. Snap the grid to the layout's columns where you can. Hover reveal (Hero Highlight): a second copy of the pattern in the accent color, revealed with a 200px radial mask at the pointer (P2).

## P2. Pointer spotlight
Aceternity: Card Spotlight (`#262626` reveal, 350px radius, transparent at 80%), Evervault (250px), Hero Highlight (200px).
```css
.spot { position: relative; isolation: isolate; }
.spot::before { content: ""; position: absolute; inset: -1px; border-radius: inherit; pointer-events: none; z-index: -1;
  background: radial-gradient(350px circle at var(--x, 50%) var(--y, 50%), rgb(255 255 255 / 0.06), transparent 80%);
  opacity: 0; transition: opacity 300ms cubic-bezier(0.23, 1, 0.32, 1); }
@media (hover: hover) and (pointer: fine) { .spot:hover::before { opacity: 1; } }
```
```ts
export function trackPointer(el: HTMLElement) {
  let raf = 0, x = 0, y = 0;
  const onMove = (e: PointerEvent) => {
    x = e.clientX; y = e.clientY;
    if (raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      const r = el.getBoundingClientRect();
      el.style.setProperty("--x", `${x - r.left}px`);   // on the element, never :root (inheritance = F-tier)
      el.style.setProperty("--y", `${y - r.top}px`);
    });
  };
  el.addEventListener("pointermove", onMove, { passive: true });
  return () => { el.removeEventListener("pointermove", onMove); cancelAnimationFrame(raf); };
}
```
React with Motion: `const mx = useMotionValue(0)` → `style={{ maskImage: useMotionTemplate\`radial-gradient(350px circle at ${mx}px ${my}px, white, transparent 80%)\` }}`. It reconciles zero times per move. **Border-only variant:** apply the gradient to a `::before` that has `padding: 1px` and the ring mask from P4, so only the border lights up. Keep the revealed color close to the base. It should read as light, not paint.

## P3. Static light sources
**Blurred ellipse beam** (Aceternity Spotlight): an SVG ellipse at `fill-opacity .21`, `feGaussianBlur stdDeviation 151`, rotated with a matrix, entering once over `2s ease .75s`:
```html
<svg class="beam" viewBox="0 0 3787 2842" fill="none" aria-hidden="true">
  <g filter="url(#beam-blur-UNIQUE)"><ellipse cx="1924.71" cy="273.5" rx="1924.71" ry="273.5" fill="#fff" fill-opacity=".21"
    transform="matrix(-0.822 -0.569 -0.569 0.822 3631.88 2291.09)"/></g>
  <defs><filter id="beam-blur-UNIQUE" x="0" y="0" width="3787" height="2842" filterUnits="userSpaceOnUse">
    <feGaussianBlur stdDeviation="151"/></filter></defs>
</svg>
```
```css
.beam { position: absolute; top: -10rem; left: 0; width: 138%; height: 169%; pointer-events: none; opacity: 0;
  animation: beam-in 2s ease .75s forwards; }
@keyframes beam-in { from { opacity: 0; transform: translate(-72%, -62%) scale(.5); } to { opacity: 1; transform: translate(-50%, -40%) scale(1); } }
@media (prefers-reduced-motion: reduce) { .beam { animation: none; opacity: 1; transform: translate(-50%, -40%); } }
```
**Blur-free cone** (Spotlight New): low-alpha radial falloff on a rotated div, with no filter at all:
```css
.cone { position: absolute; width: 560px; height: 1380px; transform: translateY(-350px) rotate(-45deg); pointer-events: none;
  background: radial-gradient(68.54% 68.72% at 55.02% 31.46%, hsl(210 100% 85% / .08) 0, hsl(210 100% 55% / .02) 50%, transparent 80%); }
```
Its drift is `x: [0, 100, 0]` over 7s easeInOut, reversing. Keep it static under reduced motion.

**Conic lamp** (Linear-style, Aceternity Lamp): two mirrored conic gradients meeting at the top center, with a bright 2px bar and a blurred orb:
```css
.lamp-l { background: conic-gradient(from 70deg at center top, var(--lamp), transparent, transparent); }
.lamp-r { background: conic-gradient(from 290deg at center top, transparent, transparent, var(--lamp)); }
.lamp-bar { height: 2px; background: var(--lamp); transform: scaleX(.5); transition: transform .8s cubic-bezier(.77,0,.175,1); } /* scaleX, not width */
.lamp.in-view .lamp-bar { transform: scaleX(1); }
```
Trim the cones' outer edges with masks (`linear-gradient(to top, #000, transparent)`) so no hard edge shows.

## P4. Border glow ring
Aceternity Glowing Effect ("as seen on Cursor"): a multicolor `repeating-conic-gradient`, isolated to the border, with an arc carved out by a conic mask that turns to face the pointer.
```css
@property --angle { syntax: "<angle>"; initial-value: 0deg; inherits: false; }
.ring { position: relative; border-radius: 16px; }
.ring::after { content: ""; position: absolute; inset: -1px; border-radius: inherit; padding: 1px; pointer-events: none;
  background: conic-gradient(from var(--angle), transparent 0 70%, var(--glow-a, #60a5fa) 85%, var(--glow-b, #a78bfa) 92%, transparent);
  -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
  -webkit-mask-composite: xor; mask-composite: exclude; }
.ring.spin::after { animation: ring-spin 4s linear infinite; }
@keyframes ring-spin { to { --angle: 360deg; } }
@media (prefers-reduced-motion: reduce) { .ring.spin::after { animation-play-state: paused; } }
```
**Pointer-aimed** (the Cursor feel):
- `target = atan2(dy, dx) * 180/π + 90` from the card center.
- Take the shortest path: `delta = ((((target - current) % 360) + 540) % 360) - 180`. (Aceternity's `((d + 180) % 360) - 180` is wrong in JS for d < −180, because `%` keeps the sign.)
- Tween `--angle` over **~2s with `cubic-bezier(0.16, 1, 0.3, 1)`**. The slow, heavily eased catch-up is what makes it read as physical light rather than a cursor follower.
- Deactivate inside a central "inactive zone" (~70% of the half-size), and activate within a `proximity` of ~64px outside the card.
- Use one shared pointer listener, coalesced with rAF.

Avoid `background-attachment: fixed` on the ring, because it repaints on scroll.

## P5. Path-following blob (Moving Border)
Aceternity traces an invisible `<rect rx="30%">` with `getPointAtLength` every frame, drawing an 80px `radial-gradient(#0ea5e9 40%, transparent 60%)` blob at opacity .8 (3s per lap) inside a `padding: 1px; overflow: hidden` wrapper. The inner surface radius is the outer radius × 0.96. Cheaper options:
- P4's rotating conic ring
- CSS `offset-path: inset(0 round 999px); offset-distance: 0 → 100%` on the blob, with no JS. Basic-shape offset paths are recent, so check support and keep P4 as the fallback.
- If you keep JS: cache `getTotalLength()`, refresh it with ResizeObserver, and pause off-screen

## P6. SVG beams and traveling pulses
Two mechanisms:
1. **Animate the gradient coordinates.** Aceternity Beams move `x1/x2/y1/y2` of a `linearGradient` from 0% to 100% over 10–20s. Tracing Beam drives `y1/y2` in `userSpaceOnUse` from scroll through springs (`stiffness 500, damping 90`). Best for near-straight paths.
2. **Animate a dash.** This follows curves exactly:
```html
<svg viewBox="0 0 700 320" aria-hidden="true" class="beams">
  <path d="M0 40 C200 40 300 280 700 280" stroke="rgb(255 255 255 / .06)" fill="none"/>                 <!-- static rail -->
  <path class="pulse" pathLength="1" d="M0 40 C200 40 300 280 700 280" stroke="url(#g-UNIQUE)" fill="none"
        stroke-width="1.25" stroke-linecap="round"/>
  <defs><linearGradient id="g-UNIQUE" x1="0" x2="1">
    <stop stop-color="var(--beam-a)" stop-opacity="0"/><stop offset=".3" stop-color="var(--beam-a)"/>
    <stop offset=".6" stop-color="var(--beam-b)"/><stop offset="1" stop-color="var(--beam-b)" stop-opacity="0"/>
  </linearGradient></defs>
</svg>
```
```css
.pulse { stroke-dasharray: .15 1; animation: travel 3.6s linear infinite; }
@keyframes travel { from { stroke-dashoffset: .15; } to { stroke-dashoffset: -1; } }
@media (prefers-reduced-motion: reduce) { .pulse { display: none; } }
```
Rules:
- Draw the faint static rail (0.05–0.16 opacity) so the structure reads even when paused.
- Strokes are 0.5–1.25px, and pulse gradients start and end at opacity 0.
- Jitter each pulse with a delay and duration generated after mount (hydration), or with a deterministic formula like `delay = i * 0.45s` (as this repo's bento graph does).
- Fade line ends with a mask, not opacity. "The line would then feel like it came to a full stop all at once" (Rauno).

Background Lines (height.app) variant: `strokeDasharray "50 800" → "20 800"` and `strokeDashoffset 800 → 0` with opacity `[0,1,1,0]` over 10s, 2.3px, round caps.

## P7. Grain
```css
.grain::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: .07; mix-blend-mode: overlay;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"); }
```
Use opacity 0.05–0.1 for plain grain (up to 0.2 with `mix-blend-mode: overlay`, which softens it), and never animate it (static grain is free after the first paint). It also hides banding in large dark gradients. Aceternity uses a `noise.webp` at 0.1–0.2 with `mix-blend-mode: overlay`.

## P8. Edge fades
```css
.marquee     { mask-image: linear-gradient(to right, transparent, #000 20%, #000 80%, transparent); }
.fade-bottom { mask-image: linear-gradient(to bottom, #000 60%, transparent); }
.vignette    { mask-image: radial-gradient(50% 50% at 50% 50%, #000 0%, transparent 100%); }
.edges-x     { mask-image: linear-gradient(90deg, transparent 0, #000 12px calc(100% - 12px), transparent 100%); } /* Linear nav */
```
The most common tell of copy-pasted effects is a hard edge on a glow, grid or beam, so fade every decorative layer into the page.

## P9. Tilt, parallax, glare
- **Tilt** (3D Card): the parent has `perspective: 1000px` and the card has `transform-style: preserve-3d`. Rotation is `(pointer − center)/25` degrees, written straight to `style.transform`. Children lift with `translateZ(50–100px)` on hover. Negate `rotateX` so the surface *faces* the pointer.
- **Glare** (Glare Card, "as seen on Linear"): the tilt is subtle (`Δ% / 3.5 × 0.4` deg), with a `radial-gradient(farthest-corner circle at var(--m-x) var(--m-y), rgb(255 255 255 / .8) 10%, rgb(255 255 255 / .65) 20%, transparent 90%)` in `mix-blend-mode: soft-light`. **The ease-in-then-track trick:** on pointer enter, keep `transition-duration: 300ms` for 300ms, then set it to 0 for 1:1 tracking. On leave, restore it so the card eases home.
- **Wobble** (parallax): the outer layer translates `offset/20` px, and the inner translates the opposite way with `scale(1.03)`, over `transition: transform .1s ease-out`.
- **Scroll tilt** (Container Scroll): `rotateX 20→0`, `scale 1.05→1` (0.7→0.9 on mobile), title `translateY 0→−100` across the section's scroll progress, with `perspective: 1000px`.
- All of them: fine pointers only, and no tilt under reduced motion.

## P10. Blur-in text
- Aceternity Text Generate: words go from `opacity: 0; filter: blur(10px)` to visible over 0.5s with a 0.2s stagger. That's too slow past ~5 words.
- Design Engineers hub: characters go from `{opacity: 0, y: 10, blur(4px)}` over 0.4s, with a 15ms stagger per character and ease `[.33, 1, .68, 1]`.
- Linear: whole lines go from `blur(10px) + translateY(20%)`, with the line boxes padded (`margin: -30px; padding: 30px`) so the blur isn't clipped.

Rules:
- Keep the total under ~1s.
- Put the real string in `aria-label` on the wrapper and mark the spans `aria-hidden`.
- Hero only, and once.
- Blur ≤10px on few elements.

## P11. Distance ripple
Background Ripple: on click, each cell gets `--delay: distance * 55ms` and `--duration: 200 + distance * 80ms` (`distance = hypot(dRow, dCol)`), and one keyframe pulses opacity 0.4 → 0.8 → 0.4. It's pure CSS after setting the variables. Mask the grid (`radial-gradient` from the top).

## P12. Canvas field
The model to copy is Aceternity's Dotted Glow Background:
- cap `devicePixelRatio` at 2 and call `ctx.setTransform(dpr, 0, 0, dpr, 0, 0)`
- size the canvas with ResizeObserver
- pause with IntersectionObserver
- clean up every listener
- resolve colors from CSS variables and watch theme changes
- add `shadowBlur` only to the few brightest dots

Add what it lacks:
- **cancel** the rAF when off-screen rather than skipping draws
- stop when `document.hidden`
- render a single static frame under reduced motion

Density example (Stars): 0.00015 stars/px², radius 0.5–0.55, 70% twinkling.

## P13. Orbs and aurora (most expensive, so use last)
- Orbs (Background Gradient Animation): five 80%-size radial blobs in `mix-blend-mode: hard-light` orbit on 20–40s loops through offset `transform-origin`s. The blur sits on the **container** (`blur(40px)` plus an SVG goo matrix), not on each blob.
- Aurora: repeating 100° gradients at 300%/200% size, `blur(10px)`, `mix-blend-difference`, animating `background-position` over 60s. That repaints a viewport-sized blurred layer every frame.

Cheaper paths:
- animate only blob `transform`s under one static blur
- drop the goo filter
- ship a static image or a short muted `<video>` poster for reduced motion and low-power devices

## P14. Bezel surfaces
- **Stacked shadow card** (Design Engineers hub): `shadow-[0_1px_2px_rgba(0,0,0,.3),0_2px_4px_rgba(0,0,0,.3),0_4px_8px_rgba(0,0,0,.3),0_8px_16px_rgba(0,0,0,.3),inset_0_0_0_1px_rgba(255,255,255,.03),inset_0_1px_0_rgba(255,255,255,.06)]` on `from-zinc-900 to-zinc-950`, radius 24px. The doubling offsets (1/2/4/8/16) give a physical falloff, and the top inset highlight is the "lit from above" edge.
- **Frame-in-frame** (Glowing Effect demo): the outer `rounded-3xl border p-3` holds an inner `rounded-xl` card (24 − 12 = 12, concentric).
- **Avatar ring:** `0 0 0 2px #000, 0 0 0 3px rgb(255 255 255 / .1)`, a dark gap plus a faint outer hairline.

## P15. Gradient hairlines and horizons
```css
.hairline { height: 1px; background: linear-gradient(to right, transparent, rgb(255 255 255 / .1) 50%, transparent); }
.sparkle-line { height: 1px; background: linear-gradient(to right, transparent, var(--accent) 50%, transparent); box-shadow: 0 0 12px var(--accent); }
/* "sunrise" horizon (Linear 2022 rebuild): giant ellipse edge over a radial glow, masked */
.horizon { position: relative; height: 600px; overflow: hidden; pointer-events: none;
  mask-image: radial-gradient(circle at center, #000, transparent 80%); }
.horizon::before { content: ""; position: absolute; inset: 0; opacity: .4;
  background: radial-gradient(circle at bottom center, var(--accent), transparent 70%); }
.horizon::after { content: ""; position: absolute; top: 50%; left: -50%; width: 200%; height: 142.8%; border-radius: 50%;
  border-top: 1px solid color-mix(in oklch, var(--accent) 40%, transparent); background: var(--bg-canvas); }
```
