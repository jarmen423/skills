---
name: interface-motion
description: How an interface moves — whether to animate at all (the frequency gate) and how to make motion feel fast and physical, from Emil Kowalski's and Rauno Freiberg's work. Covers easing curves, durations, scale and transform-origin, springs, interruptibility, stagger and choreography, drag and swipe gestures (velocity, rubber-banding, snap points), clip-path and blur tricks, performance and reduced motion, with CSS and framer-motion recipes. Use when prototyping interactions or motion for new designs and redesigns, and for any animation, transition, hover or press effect, enter/exit, toast, drawer, popover, tab indicator, scroll reveal or gesture, and whenever an interaction feels slow, janky, floaty or off.
---

# Interface motion

Motion is a tool for explaining change, and it has a cost: every animation delays the user a little and competes for attention. The people who do this best (Emil Kowalski at Linear, Rauno Freiberg at Vercel) spend most of their judgment deciding *what not to animate*. Whatever survives is then tuned until it feels like a physical object responding to the user, not a video playing at them.

Emil's framing: "Easing… is the most important part of any animation. It can make a bad animation look great, and a great animation look bad." Rauno's: "Truly fluid gestures are immediately responsive." Everything below serves those two ideas.

## Work through these steps in order

### 1. Should this animate at all? (the frequency gate)

| How often the user sees it | Decision |
|---|---|
| 100+ times a day: keyboard shortcuts, command palette open, arrow-key list navigation | **No animation.** A keyboard-initiated action never animates in. |
| Tens of times a day: hover on list rows and menu items, toggles, tab switches | Remove it, or make it near-imperceptible (fast, color or opacity only). For tabs, the panel swaps instantly and only the indicator may slide (~200–250ms) |
| Occasionally: modals, drawers, toasts, popovers | Standard animation (below) |
| Rarely or once: onboarding, first load after login, empty-to-first-item, celebrations | This is where delight is allowed to live |

Then name the purpose in one phrase: *feedback* (press), *spatial continuity* (where did it come from or go), *state change* (what changed), *preventing a jarring jump*, *explanation* (marketing only), or *delight* (rare tier only). If the only reason is "it looks nice" on something frequent, don't animate it. Rauno animated the list interactions in his bookmarks app, and "after a couple of days they began to feel sluggish… I removed motion from core interactions and suddenly felt like I was moving much faster."

Useful middle grounds:
- **Animate out, not in.** macOS context menus appear instantly and fade out, and the chosen item blinks the accent color once. Frequent surfaces can follow the same pattern.
- **Novelty is seasoning.** Aim for about 90% familiar and 10% novel. Spend novelty on one-time moments, gated with a cookie or flag so it doesn't replay on every visit (see `references/choreography.md`).
- **Don't layer entrances.** If the panel slides in, its content is simply there. A panel slide plus a staggered list is two entrances, and the second one costs the user time.
- **Animate state changes, never first render.** "Often state transitions accidentally play out when the page loads, but this makes the application feel poorly built." Use `initial={false}` on `AnimatePresence`, or defer measured values until content is stable.

### 2. Pick the easing

```
Entering or exiting the screen?        → ease-out (strong, custom)
Already on screen, moving A → B?       → ease-in-out
Simple hover color/background change?  → ease
Constant motion or progress?           → linear
Unsure?                                → ease-out
```

Never use `ease-in` for anything entering or moving on screen. It holds back the start, which is exactly the moment the user is watching, so a 200ms ease-in feels slower than a 300ms ease-out. The one sourced exception is a **short exit** (≤150ms). Linear's context menus and Vercel's view-transition recipe exit with ease-in, but ease-out exits are never wrong. The built-in CSS `ease-out` is too weak. Use these tokens and copy them exactly rather than approximating:

```css
--ease-out:    cubic-bezier(0.23, 1, 0.32, 1);   /* UI enters/exits: strong, fast start */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* on-screen movement, clip-path reveals */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* iOS sheet curve (Ionic/Vaul); also great for popovers & dialogs */
```

Motion (framer-motion) arrays: `[0.23, 1, 0.32, 1]`, `[0.77, 0, 0.175, 1]`, `[0.32, 0.72, 0, 1]`. Match the product's personality: a crisp tool gets no bounce, and a playful consumer surface can take a little.

### 3. Pick the duration

| Element | Duration |
|---|---|
| Press feedback, small state flips | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects, menus (if animated) | 150–250ms |
| Modals, dialogs | 200–300ms |
| Drawers, sheets, full-screen panels | 400–500ms |
| Marketing reveals and hero entrances | 600ms–1s (never over 1s unless illustrative) |

The rules behind the table:
- Keep UI under 300ms.
- Larger surfaces and longer travel get longer durations, the way a truck takes longer to stop than a bicycle.
- Exits run about 20% faster than entrances.
- Be slow where the user is deciding and fast where the system responds. Hold-to-delete fills over 2s linear, then releases in 200ms ease-out.

### 4. Make it physical: origin, scale, distance
- **Never animate from `scale(0)`.** Nothing real appears from nothing. Emil's rule is to start at 0.90–0.95, "like it was always almost there", always paired with `opacity: 0`. By size:
  - Large surfaces (dialogs, sheets): 0.95–0.97. Geist and Linear dialogs use .96.
  - Anchored popovers and menus: 0.9–0.95. Linear's context menu uses .9, and Emil's popover demo goes to .85 at 150ms.
  - Small swaps (icons, chips, labels): as low as 0.8, with opacity and a 2px blur.

  This list is the canonical range. The other skills defer to it.
- **Press feedback** is `transform: scale(0.97)` on `:active`, with a ~160ms ease-out transition. If you can clearly see the button shrink, the scale is too aggressive.
- **Popovers grow from their trigger.** Set `transform-origin` to the anchor: `var(--transform-origin)` in Base UI, or `var(--radix-popover-content-transform-origin)` in Radix. Modals are the exception and stay centered.
- **Exit the way you came in.** A toast that enters from the bottom leaves toward the bottom, which also makes swipe-to-dismiss obvious.
- **Translate by percentage** (`translateY(100%)`) so the motion fits the element's own size.
- **Blur hides a crossfade that won't settle.** If two states double-expose mid-transition, add `filter: blur(2px)` at the midpoint (keep blur under ~20px; it's expensive in Safari). This is the standard treatment for icon and label swaps: `opacity 0→1, scale 0.8→1, blur(2px)→0` over 150ms.

### 5. Make it interruptible
- Anything that can be toggled quickly (menus, accordions, drawers, toasts, tabs) uses **CSS transitions or springs, not keyframes**. Keyframes restart from zero when retriggered. Transitions and springs retarget from wherever the element currently is.
- For entrances without keyframes, use `@starting-style` (or Base UI's `[data-starting-style]` / `[data-ending-style]`), or set a mounted flag one frame after mount.
- Never lock input during a transition. The user must be able to reverse mid-flight.
- In Motion, animating to a target (not a keyframe array) retargets smoothly. Springs keep velocity when interrupted.

### 6. Use the cheapest tool that works
1. CSS transition: hover, press, toggles
2. `@starting-style` / data-attribute states: mount and unmount
3. CSS `@keyframes`: predetermined loops and one-shots that must stay smooth while the main thread is busy
4. Web Animations API (`el.animate`): programmatic control without a library
5. Motion (`motion/react` or `framer-motion`): springs, layout animations, exit animations, gestures, scroll-linked values

Performance rules that decide whether the animation is smooth or janky:
- **Animate only `transform` and `opacity`** (plus `clip-path` and small `filter`s). Height is acceptable only for accordions: keep them short and never animate to `auto` without measuring.
- Never `transition: all`. List the properties.
- Motion's `x`/`y`/`scale` shorthands animate CSS variables and aren't hardware-accelerated. Under load (route changes, heavy pages), animate `transform: "translateX(…)"` directly, or use CSS.
- Drive continuous values (pointer position, drag offset, scroll progress) through refs, `el.style.transform` or Motion values, never React state. Setting a CSS variable on a parent triggers style recalculation for every descendant, so write `transform` on the moving element itself.
- Add `will-change: transform` only when you see a 1px shift or jitter at the start of an animation, not everywhere.
- Pause loops that are off-screen (IntersectionObserver) or in background tabs.

### 7. Respect people and devices
- **Reduced motion means gentler, not zero.** Remove movement, scaling and parallax, and keep opacity and color changes that help comprehension. Decorative loops pause (`animation-play-state: paused`, which avoids the snap `animation: none` causes) or are hidden entirely when they add nothing static. One-shot entrances jump to their end state. Movement the user drives directly (a drag) stays. In Motion, use `useReducedMotion()` to swap `x: "-100%"` for `x: 0` while keeping the fade.
- **Gate hover effects** with `@media (hover: hover) and (pointer: fine)`. Taps trigger hover on touch devices and leave it stuck. `:active` needs no gating.
- **Hover flicker → animate a child, not the hovered element** (Emil's rule). The likely cause is that scaling or moving the hovered element moves its hit area, so hover toggles at the edges.

### 8. Review by slowing it down
Slow it down: use the Chrome DevTools Animations panel at 25% or 10% speed, temporarily multiply durations 2–5×, or record it and step frame by frame. Check:
- Does anything double-expose?
- Does the easing stop abruptly?
- Is the origin right?
- Do coordinated properties stay in sync?
- Spam the trigger: does it retarget smoothly or restart?
- Look again the next day with fresh eyes.

## Reference files
- `references/recipes.md`: copy-paste implementations (CSS and Motion) for button press, tooltip groups, popover, dropdown, modal, drawer, toast stack, accordion, tab indicators (including clip-path tabs), icon and label swap, list add/remove, number ticker, stagger, scroll reveal, hold-to-delete, theme switch, view-transition timing. Read it before implementing any of these.
- `references/gestures.md`: drag, swipe and flick physics: 1:1 tracking, drag thresholds, velocity, momentum projection, rubber-banding, snap points, scroll-vs-drag arbitration, commit-on-release rules, with the exact constants Sonner and Vaul ship. Read it for anything draggable or swipeable.
- `references/choreography.md`: sequencing multiple elements (stagger, follow-through, trigger-first ordering, depth and blur), novelty budgets for marketing pages, and one-time "first visit" moments. Read it for hero sections, page entrances and multi-part transitions.

## Reviewing motion code
When asked to review animations, reply with one markdown table (`| Before | After | Why |`), one row per issue, most important first. Make the call and give the reasoning in one line rather than offering a menu of options. Common rows:

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 200ms var(--ease-out), opacity 200ms var(--ease-out)` | `all` animates layout properties by accident |
| `initial={{ scale: 0 }}` | `initial={{ scale: 0.95, opacity: 0 }}` | nothing real appears from nothing |
| `ease-in` on a dropdown | `var(--ease-out)` | ease-in delays the moment the user is watching |
| popover `transform-origin: center` | `var(--transform-origin)` | it should grow from its trigger |
| animated ⌘K open | no animation | opened 100+ times a day |
| `@keyframes` on a toggle | CSS transition | keyframes restart; transitions retarget |
| hover scale with no media query | wrap in `@media (hover: hover) and (pointer: fine)` | stuck hover on touch |
| same enter and exit duration | exit ~20% faster | leaving should get out of the way |

## In this repo (agent-memory-labs-frontend): current state, context not constraints
- The library is `framer-motion` 12 (import from `"framer-motion"`). Code copied from sources that import `motion/react` needs the import changed; the API is the same.
- `--ease-out-soft: cubic-bezier(0.16, 1, 0.3, 1)` in `src/app/globals.css` is the current strong ease-out (Tailwind `ease-out-soft`). Whether you extend the current motion values or define a new motion language, keep curves and durations as tokens in `@theme` rather than inline beziers.
- The global `prefers-reduced-motion` block at the bottom of `globals.css` zeroes every animation and transition, fades included. Decorative loops in this codebase already use `motion-safe:` (e.g. `motion-safe:animate-beam`), so gate new loops the same way.
- `src/components/home/bento.tsx` drives the time-travel scrubber with `useSpring(…, { stiffness: 220, damping: 30 })`, and `useTransform` moves the cursor line without re-rendering. It also mirrors the spring into React state (`useMotionValueEvent(x, "change", setPos)`) to recompute which claims are valid, which re-renders every frame. That's acceptable for a handful of rows, but if the scrubbed content grows, quantize it (only `setPos` when the derived state actually changes).
