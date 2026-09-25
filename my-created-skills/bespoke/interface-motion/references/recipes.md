# Motion recipes

Copy-paste implementations. Values come from Emil Kowalski's published skill recipes and blog demos, the Sonner and Vaul source, Geist's production CSS and Devouring Details. CSS first; Motion (`motion/react` / `framer-motion`) where CSS can't do it.

## Contents
1. Tokens
2. Button press
3. Tooltip group (delay once, then instant)
4. Popover / dropdown (origin-aware)
5. Modal / dialog
6. Drawer / bottom sheet
7. Toast stack (Sonner model)
8. Accordion
9. Tab indicator (sliding) and clip-path tabs
10. Icon / label swap with blur
11. List add/remove with reflow
12. Number and timer ticks
13. Stagger (lists) and hierarchical stagger (heroes)
14. Scroll reveal (once)
15. Hold-to-confirm
16. Theme switch without transitions
17. Route / view transitions timing
18. Springs cheat sheet
19. Glow and state changes without repaint

---

## 1. Tokens
```css
:root {
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  --dur-press: 160ms;
  --dur-small: 150ms;   /* tooltip, small popover */
  --dur-menu: 200ms;
  --dur-modal: 250ms;
  --dur-sheet: 500ms;
}
```
Tailwind v4: put them in `@theme` as `--ease-*` and use them as `ease-out-…` utilities. Keep one set, and extend the codebase's tokens rather than forking near-identical beziers.

## 2. Button press
```css
.button { transition: transform 160ms var(--ease-out); }
.button:active { transform: scale(0.97); }
```
Tailwind: `transition-transform duration-150 ease-[cubic-bezier(0.23,1,0.32,1)] active:scale-[0.97]` (or the project's own strong ease-out token; Tailwind's built-in `ease-out` is the weak `(0,0,0.2,1)`). Motion: `whileTap={{ scale: 0.97 }}`. The acceptable range is 0.95–0.98. If you want a hover lift, gate it:
```css
@media (hover: hover) and (pointer: fine) { .button:hover { background: var(--bg-hover); } }
```

## 3. Tooltip group: delay once, then instant
The first tooltip waits ~150–300ms so sweeping the mouse across doesn't flash them. While one is open, neighbors open immediately *and without animation*.
```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition: transform 125ms var(--ease-out), opacity 125ms var(--ease-out);
}
.tooltip[data-starting-style], .tooltip[data-ending-style] { opacity: 0; transform: scale(0.97); }
.tooltip[data-instant] { transition-duration: 0ms; }   /* Base UI sets this for grouped/instant opens */
```
Radix: wrap in `<Tooltip.Provider delayDuration={200} skipDelayDuration={300}>`.

## 4. Popover / dropdown: origin-aware
```css
.popover {
  transform-origin: var(--transform-origin);       /* Radix: var(--radix-popover-content-transform-origin) */
  transition: opacity 200ms var(--ease-out), transform 200ms var(--ease-out);
}
.popover[data-starting-style], .popover[data-ending-style] { opacity: 0; transform: scale(0.95); }
```
Motion version (Emil's demo values):
```jsx
<motion.div
  initial={{ opacity: 0, scale: 0.85 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.85 }}
  transition={{ duration: 0.15, ease: [0.32, 0.72, 0, 1] }}
  style={{ transformOrigin: "top left" }}  /* match the side the trigger is on */
/>
```
For **frequently used menus** (context menus, the account menu), skip the entrance: render instantly, fade out over ~100–150ms, and blink the selected item's background once before closing.

## 5. Modal / dialog
```css
.modal { transform-origin: center; transition: opacity 250ms var(--ease-out), transform 250ms var(--ease-out); }
.modal[data-starting-style], .modal[data-ending-style] { opacity: 0; transform: scale(0.96); }
.backdrop { transition: opacity 250ms var(--ease-out); }
.backdrop[data-starting-style], .backdrop[data-ending-style] { opacity: 0; }
```
Animate the backdrop with the dialog so they read as one surface. Motion version with the blur trick:
```jsx
initial={{ scale: 0.9, opacity: 0, filter: "blur(2px)" }}
animate={{ scale: 1, opacity: 1, filter: "blur(0px)" }}
exit={{ scale: 0.9, opacity: 0, filter: "blur(2px)" }}
transition={{ duration: 0.2, ease: [0.32, 0.72, 0, 1] }}
```
Geist's overlay token is `.3s` from scale `.96` with `cubic-bezier(.175,.885,.32,1.1)` (a slight overshoot). Use that only if the product's personality allows overshoot.

## 6. Drawer / bottom sheet
```css
.drawer { transform: translateY(0); transition: transform 500ms var(--ease-drawer); }
.drawer[data-closed] { transform: translateY(100%); }       /* percentage = works at any height */
.drawer::after { content: ""; position: absolute; inset-inline: 0; top: 100%; height: 200%; background: inherit; } /* no gap when over-dragged */
```
While dragging, set `transition: none` and write `el.style.transform` directly. On release, restore the transition inline so it animates from wherever the finger left it. Thresholds are in `gestures.md`.

The optional "page becomes a sheet" effect (Vaul `shouldScaleBackground`):
```css
[data-drawer-wrapper] { transform-origin: top; border-radius: 8px; overflow: hidden;
  transform: scale(calc((100vw - 26px) / 100vw)) translate3d(0, calc(env(safe-area-inset-top) + 14px), 0);
  transition: transform 500ms var(--ease-drawer), border-radius 500ms var(--ease-drawer); }
```
(Compute the scale in JS as `(innerWidth - 26) / innerWidth`. It's shown in CSS for readability.) While dragging, interpolate by progress `p`: overlay opacity `1 − p`, wrapper scale `s + p(1 − s)`, radius `8 − 8p`, translateY `max(0, 14 − 14p)`.

## 7. Toast stack (Sonner model)
Constants: 3 visible, 14px gap, 356px wide, 4000ms lifetime, 24px viewport offset (16px under 600px), 200ms exit and unmount.
```css
[data-toast] { transition: transform 400ms ease, opacity 400ms ease, height 400ms ease, box-shadow 200ms ease; }
[data-toast][data-mounted="false"] { transform: translateY(100%); opacity: 0; }   /* enter via mounted flag or @starting-style */
/* collapsed: each toast behind the front lifts by the gap and shrinks 5% per step */
[data-toast][data-expanded="false"][data-front="false"] {
  transform: translateY(calc(var(--lift) * var(--toasts-before) * 14px)) scale(calc(1 - var(--toasts-before) * 0.05));
  height: var(--front-toast-height);           /* uneven heights: all match the front toast */
}
[data-toast][data-expanded="false"][data-front="false"] > * { opacity: 0; }  /* only edges peek */
[data-toast][data-visible="false"] { opacity: 0; pointer-events: none; }   /* index ≥ 3 */
[data-toast]::after { content: ""; position: absolute; left: 0; right: 0; top: 100%; height: calc(14px + 1px); } /* keep hover across gaps */
```
The details that make it feel right:
- Expand on hover, where each expanded offset = index × gap + sum of heights before it.
- Pause the timer on hover, on focus, and while `document.hidden`. Resume with the remaining time, not a fresh 4s.
- Enter and exit from the same edge.
- Swipe to dismiss (see `gestures.md`).
- A hotkey (e.g. ⌥T) focuses the region.
- Announce with `aria-live="polite"`.

Sonner deliberately uses 400ms plain `ease` (slower and more elegant than usual), which suits its tone. Personality can override the defaults, as long as it's a deliberate choice.

## 8. Accordion
One of the few acceptable height animations. Keep it short and measure it:
```css
.content { overflow: hidden; height: var(--content-height); transition: height 200ms var(--ease-out), opacity 200ms var(--ease-out); }
.content[data-closed] { height: 0; opacity: 0; }
```
Base UI and Radix expose `--accordion-panel-height` / `--radix-accordion-content-height`. Modern CSS alternative: `interpolate-size: allow-keywords` with `height: auto` (progressive enhancement). Pair height with an opacity fade so the reveal doesn't look like a wipe.

## 9. Tab indicator
**Sliding pill (shared layout):**
```jsx
{active && <motion.span layoutId="tab-pill" className="absolute inset-0 rounded-md bg-white/10"
  transition={{ type: "spring", bounce: 0, duration: 0.3 }} />}
```
Under load (tabs that trigger route changes), Motion layout animations can drop frames. Vercel moved its dashboard tab indicator to CSS for this reason. The CSS version measures the active tab and transitions `transform: translateX(…)` and `width`→`scaleX` on one indicator, over ~220ms with `cubic-bezier(0.5, 0, 0.2, 1)`.

**Clip-path tabs** (text and background change color in perfect sync; credited to Paco Coursey): render the tab list twice. The top copy is styled active (`aria-hidden`, `tabIndex={-1}`, `pointer-events: none`) and absolutely positioned, then clipped to the active tab's rect:
```js
const { offsetLeft: l, offsetWidth: w } = activeTab;
overlay.style.clipPath = `inset(0 ${100 - ((l + w) / list.offsetWidth) * 100}% 0 ${(l / list.offsetWidth) * 100}% round 17px)`;
```
```css
.overlay { position: absolute; inset: 0; transition: clip-path 250ms var(--ease-in-out); }
```

## 10. Icon / label swap with blur
```jsx
<AnimatePresence mode="popLayout" initial={false}>
  <motion.span key={state}
    initial={{ opacity: 0, scale: 0.8, filter: "blur(2px)" }}
    animate={{ opacity: 1, scale: 1, filter: "blur(0px)" }}
    exit={{ opacity: 0, scale: 0.8, filter: "blur(2px)" }}
    transition={{ duration: 0.15 }} />
</AnimatePresence>
```
Use this for copy→check, play→pause and save→saved. The copy checkmark stays ~1.5–2s, then swaps back. `initial={false}` stops it from animating on first render.

## 11. List add/remove with reflow
Remove the leaving item from flow immediately so siblings reflow *in parallel* with its exit:
```jsx
<MotionConfig transition={{ type: "spring", stiffness: 280, damping: 18, mass: 0.3 }}>
  <AnimatePresence mode="popLayout" initial={false}>
    {items.map((it) => <motion.li key={it.id} layout exit={{ opacity: 0, scale: 0.8 }} />)}
  </AnimatePresence>
</MotionConfig>
```
If adding and removing items is a core, frequent action in a productivity view, consider no animation at all (Rauno's bookmarks lesson).

## 12. Number and timer ticks
Each changing digit slides and blurs; unchanged digits stay still. Always use `tabular-nums`:
```jsx
<span className="tabular-nums inline-flex overflow-hidden">
  {digits.map((d, i) => (
    <AnimatePresence key={i} mode="popLayout" initial={false}>
      <motion.span key={d} initial={{ y: 12, opacity: 0, filter: "blur(2px)" }}
        animate={{ y: 0, opacity: 1, filter: "blur(0px)" }} exit={{ y: -12, opacity: 0, filter: "blur(2px)" }}
        transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}>{d}</motion.span>
    </AnimatePresence>
  ))}
</span>
```
For bursty updates (a counter that changes faster than the animation), skip the animation when `Date.now() - lastUpdate < duration`. In production, NumberFlow is the library Emil recommends.

## 13. Stagger
**Lists (occasional views only):** 30–80ms between items, never blocking interaction.
```css
.item { opacity: 0; transform: translateY(8px); animation: fade-up 300ms var(--ease-out) forwards; }
.item:nth-child(2) { animation-delay: 50ms; } .item:nth-child(3) { animation-delay: 100ms; }
@keyframes fade-up { to { opacity: 1; transform: none; } }
```
Or set `style={{ animationDelay: `${i * 50}ms` }}` with `--i`, capped so item 20 doesn't wait a second.

**Hero (marketing):** stagger by importance, with *non-uniform* delays, because uniform delays feel as mechanical as linear easing.

| Element | Motion | Delay |
|---|---|---|
| Headline | opacity 0→1, blur 10px→0, translateY 30%→0, 1s | 0.2s |
| Subhead | same, translateY 20% | 0.5s |
| CTAs | same, translateY 20% | 0.8s |
| Badge / pill | opacity + blur only, no slide | 1.4s |

Play it once per session or first visit, not on every back-navigation (see `choreography.md`).

## 14. Scroll reveal (once)
```css
.reveal { clip-path: inset(0 0 100% 0); }
.reveal[data-visible] { clip-path: inset(0 0 0 0); transition: clip-path 600ms var(--ease-in-out); }
```
```js
const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { el.dataset.visible = ""; io.disconnect(); } },
  { rootMargin: "0px 0px -100px 0px" });
io.observe(el);
```
Motion: `useInView(ref, { once: true, margin: "-100px" })`. Fire it once, because "re-animating on every scroll-by is an interface fighting its reader." Keep reveals to marketing surfaces, never in product UI. Prefer a subtle fade + 8–16px rise, or a clip-path reveal on images; avoid large slides from the sides.

## 15. Hold-to-confirm
```css
.hold { position: relative; transition: transform 160ms var(--ease-out); }
.hold:active { transform: scale(0.97); }
.hold .overlay { position: absolute; inset: 0; clip-path: inset(0 100% 0 0); transition: clip-path 200ms var(--ease-out); } /* release: fast */
.hold:active .overlay { clip-path: inset(0 0 0 0); transition: clip-path 2s linear; }                                     /* press: deliberate, linear = progress */
```
The overlay duplicates the label in the danger colors and is `aria-hidden`. Confirm with `onTransitionEnd` / a 2s timer, and give keyboard users an equivalent (hold Enter, or a confirm step).

## 16. Theme switch without transitions
Switching themes shouldn't animate every element's colors. Disable transitions for one frame:
```js
const css = document.createElement("style");
css.appendChild(document.createTextNode("*,*::before,*::after{transition:none!important}"));
document.head.appendChild(css);
applyTheme(next);
(() => window.getComputedStyle(document.body))(); // force reflow
setTimeout(() => document.head.removeChild(css), 1);
```
next-themes does this with `disableTransitionOnChange`. For a deliberate reveal, the View Transitions API with a clip-path circle from the toggle is the modern route. Make it rare and optional.

## 17. Route / view transitions timing (Vercel recipe)
- Exit 150ms ease-in (the short-exit exception from SKILL.md step 2), then enter 210ms ease-out, delayed by the exit. Move 400ms.
- Slide offset 10px. Scale 0.85↔1 for shared elements.
- Directional slides only for hierarchical or ordered navigation (list → detail, step 1 → 2). Lateral moves (tab to tab) get a fade or nothing, because a slide "falsely implies spatial depth".
- Priority: shared element > Suspense reveal > list identity > state change > route change. "If you can't articulate what it communicates, don't add it."
- Reduced motion sets all view-transition durations to 0.

## 18. Springs cheat sheet
| Use | Config |
|---|---|
| Default UI spring (no overshoot) | `{ type: "spring", bounce: 0, duration: 0.3 }` (0.2–0.5 depending on size) |
| Recommended "alive" spring | `{ type: "spring", duration: 0.5, bounce: 0.2 }` |
| After a flick or drag release | `bounce: 0.15–0.3`, passing the release velocity in |
| Pointer-follow smoothing | `useSpring(value, { stiffness: 100–220, damping: 10–30 })` |
| Snappy list layout | `{ stiffness: 280, damping: 18, mass: 0.3 }` |
| Apple reference | move: damping 1.0 / response 0.4 · sheet: 0.8 / 0.3 |

"No bounce should be your default." Overshoot on a menu that just faded in feels wrong; overshoot on a card you flicked feels right. Match bounce to the object's conceptual mass: a light card bounces less.

## 19. Glow and state changes without repaint
Never animate `box-shadow` or `background-image` on hover. Put the glow on a pseudo-element and fade that:
```css
.card { position: relative; }
.card::after { content: ""; position: absolute; inset: 0; border-radius: inherit; pointer-events: none;
  box-shadow: 0 0 0 1px rgb(50 145 255 / 0.8), 0 0 24px rgb(50 145 255 / 0.25); opacity: 0; transition: opacity 200ms var(--ease-out); }
@media (hover: hover) and (pointer: fine) { .card:hover::after { opacity: 1; } }
```
The same applies to focus rings, except those shouldn't transition at all (`transition: none` on `:focus-visible`).
