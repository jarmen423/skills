# Gestures: drag, swipe, flick

Physics and thresholds for anything the user drags. Sources: Rauno Freiberg's "Invisible Details of Interaction Design" and Devouring Details (Next.js Dev Tools chapter), Emil Kowalski's toast and drawer write-ups, the Sonner and Vaul source, and Apple's WWDC 2018 "Designing Fluid Interfaces" (via Emil's apple-design skill).

## Principles
1. **Respond on pointer-down and track 1:1.** Apply the finger's delta immediately and keep the grab offset (where on the element they grabbed it). "A threshold doesn't mean a 0→1 animation after the threshold": a pinch that does nothing until 20px, then zooms, feels broken. Apply the delta right away and animate the *commit* past the threshold.
2. **Never lock input during a transition.** Every animation is interruptible, so the user can catch a flying element mid-air. Always animate from the current (presentation) value, never from the previous target.
3. **Lightweight actions can commit mid-gesture; destructive ones only on release.** Revealing search or an overlay can fire once the elements reach their logical final position, and reverse in the same gesture. Dismissing, deleting or closing waits for release: "What if I were to change my mind half-way through?" Let users peek, then back out.
4. **Decide by velocity as well as distance.** A short, fast flick should work as well as a long, slow drag. Decide commit vs cancel by the release velocity's *sign and size*, not position alone.
5. **Dampen, don't block.** Dragging in a disallowed direction or past a boundary moves the element with increasing resistance instead of stopping dead. "Things in real life don't suddenly stop, they slow down first."
6. **Preserve momentum and angle.** A thrown element keeps its release velocity and direction; iOS's Dynamic Island dismissal "is never perfectly centered or consistent in timing." Pass the release velocity into the settling spring.
7. **Tune bounce to conceptual mass.** Light objects (cards, toasts) bounce less. Only momentum-carrying gestures earn overshoot.
8. **Every gesture has a click and keyboard alternative** (close button, Escape, arrow keys), unless the gesture itself is essential.

## Mechanics checklist
- `el.setPointerCapture(e.pointerId)` on pointerdown, so the drag survives the pointer leaving the element. This matters for sliders that vanish under the thumb.
- Ignore right-click (`e.button === 2`) and bail out when text is selected (`window.getSelection()?.toString()`).
- **Drag start threshold (hysteresis):** 10px for touch and 2px for mouse (Vaul) before committing to a drag, so taps and scrolls aren't hijacked.
- **Axis lock:** after >1px of movement, lock to the dominant axis: `Math.abs(dx) > Math.abs(dy) ? "x" : "y"`.
- While dragging:
  - set `transition: none`, `user-select: none`, and `inert` on the dragged content
  - write `el.style.transform` directly, not a CSS variable on a parent (that recalculates styles for all children) and not React state
- On release, restore the transition inline so the element animates from where it was dropped, or hand off to a spring with the release velocity.
- `touch-action: none` (or `pan-y` for horizontal-only drags) on the drag surface so the browser doesn't fight you. Use `overscroll-behavior: contain` on scrollable sheets.
- Ignore extra touches mid-drag (`if (isDragging) return`).
- After a drag release, suppress the click and focus that would otherwise fire. Vaul sets `justReleased` for 200ms when velocity > 0.05, so releasing over an input doesn't focus it.
- Extend the hit area during drag (a `::before` with `inset: -100%`) so fast moves don't lose the element.

## Velocity
Keep a short history of (position, time) samples, e.g. the last 100ms, and compute velocity at release:
```js
const velocity = Math.abs(distance) / (performance.now() - startTime); // px/ms
```
Sonner uses the whole gesture (distance ÷ total time). For long drags, a recent-samples window is more accurate.

## Momentum projection (where a flick would land)
Apple's UIScrollView deceleration, used in Rauno's snapping dev-tools badge:
```js
function project(velocityPxPerS, decelerationRate = 0.998) {
  return ((velocityPxPerS / 1000) * decelerationRate) / (1 - decelerationRate);
}
// on release, per axis:
const projected = { x: pos.x + project(vx), y: pos.y + project(vy) };
const target = nearest(snapPoints, projected);
animate(el, target, { type: "spring", bounce: 0.2, velocity: v }); // hand off velocity
```
"Projection enhances drag gestures to swipe gestures, enabling short flicks to move the element." Use `0.99` for a snappier, shorter projection.

## Rubber-banding
Two proven curves. Apple's feels like iOS scroll overscroll; Vaul's log curve starts with a dead zone.
```js
// Apple: grows ~c·overshoot at first, approaches `dimension` asymptotically
const rubberband = (overshoot, dimension, c = 0.55) =>
  (overshoot * dimension * c) / (dimension + c * Math.abs(overshoot));

// Sonner (disallowed direction): approaches ~20px
const dampen = (d) => d * (1 / (1.5 + Math.abs(d) / 20));
// switch to the dampened value only once it's smaller than the raw delta, to avoid a jump

// Vaul (dragging a drawer past fully-open): logarithmic
const dampenValue = (v) => 8 * (Math.log(v + 1) - 2);
```
Fill the space revealed by over-dragging (a `::after` extending the background 200%) so no gap appears.

## Constants that ship
| | Sonner (toast swipe) | Vaul (drawer) |
|---|---|---|
| Distance to dismiss | 45px | 25% of drawer height |
| Velocity to dismiss | > 0.11 px/ms | > 0.4 px/ms |
| Settle / reset | 400ms `ease` via transition | 500ms `cubic-bezier(0.32, 0.72, 0, 1)` |
| Exit | 200ms ease-out to ±100%, unmount at 200ms | same curve, translate 100% |
| Wrong-direction drag | dampened (≈20px ceiling) | rubber-band (log) |
| Drag start threshold | 1px axis lock | 10px touch / 2px mouse |

**Snap points (Vaul):**
- velocity > 2 px/ms: jump to the last snap point (flick up) or close / go to the first (flick down)
- velocity > 0.4 and the drag is < 40% of the viewport: move exactly one snap point in the drag direction
- otherwise: snap to the nearest point

"If you flick hard enough, the drawer will skip some points or even close completely."

## Scroll vs drag arbitration (sheets with scrollable content)
- Don't start a drag if a scrollable ancestor's `scrollTop !== 0`. The user is scrolling content.
- After content scrolls back to the top, keep drag locked for ~100ms, so a fast upward scroll that hits the top doesn't turn into a close.
- Don't allow a drag for ~500ms after opening, while the open animation runs.
- Never drag from `<select>`, from marked no-drag zones, or while text is selected.
- Once a drag has started, never cancel it mid-gesture.
- On iOS, listen for `touchend`, because Safari doesn't fire `mouseup` after scrolling.
- For the on-screen keyboard, use `visualViewport` resize to lift the sheet above it.

## Drag-driven interpolation
Map drag progress `p` (0 → 1) onto the surrounding UI so the whole scene responds to the finger, not just the dragged element:
- overlay opacity `1 − p`
- background scale and radius interpolate back toward rest
- a nested parent drawer interpolates its offset (−16px) and scale back to 1

Compute these per frame in the pointer handler and write them directly to the DOM.

## Touch ergonomics
- Fingers hide content. Show feedback *above* the finger (the iOS loupe), render menus where the thumb isn't, and keep slider values visible off to the side.
- Screen edges and corners are the easiest targets (Fitts's law). Radial menus put every option equidistant from the pointer.
- Test on a real phone: Safari remote devtools over USB, hitting the dev server by LAN IP. Simulators lie about touch and momentum.
