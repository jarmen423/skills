# Interface rules: full list

This merges Rauno Freiberg's original guidelines (github.com/raunofreiberg/interfaces), Vercel's Web Interface Guidelines (vercel.com/design/guidelines, whose agent version is AGENTS.md in vercel-labs/web-interface-guidelines) and the code-level checks in its audit command. Levels: **MUST** = broken or inaccessible without it, **SHOULD** = polish, **NEVER** = anti-pattern.

## Contents
1. Keyboard and focus
2. Targets, touch and pointer
3. Forms and inputs
4. Feedback, state and navigation
5. Motion
6. Typography
7. Content and copy
8. Content handling (resilience)
9. Accessibility semantics
10. Layout
11. Surfaces and color
12. Dark mode and theming
13. Hydration
14. Performance
15. Anti-pattern list (flag on sight)

---

## 1. Keyboard and focus
- MUST: full keyboard support per the WAI-ARIA Authoring Practices pattern for the widget.
- MUST: visible focus rings on `:focus-visible`, using `:focus-within` for grouped controls. Sticky or fixed elements never cover the focused element.
- MUST: manage focus: trap it inside modals, move it into newly opened surfaces, return it to the trigger on close.
- NEVER: `outline: none` without a visible replacement.
- SHOULD: draw focus rings with `box-shadow` (`0 0 0 2px var(--bg), 0 0 0 4px var(--focus)`) so they follow `border-radius`. Outline ignored radius in Safari before 16.4. Don't transition the ring.
- SHOULD: on colored, destructive or error surfaces, use an inset, high-contrast (often white) ring instead of the brand ring, which disappears there.
- SHOULD: give inline links a little focus padding: `border-radius: 2px; padding-inline: 2px; margin-inline: -2px`.
- SHOULD: arrow keys ↑↓ move through sequential lists, and ⌘⌫ deletes the focused item where deletion exists.
- SHOULD: trigger dropdown menus on `mousedown`/`pointerdown`, not `click`, so they open immediately on press.
- SHOULD: interactive elements handle keyboard events (Enter/Space) if they aren't native buttons or links, and preferably they should be native.
- SHOULD: localize keyboard shortcuts for non-QWERTY layouts and show platform symbols (⌘ on macOS, Ctrl elsewhere).

## 2. Targets, touch and pointer
- MUST: hit targets ≥24px, and ≥44px on mobile. Expand the hit area when the visual is smaller.
- MUST: no dead zones. The label and control of checkboxes and radios share one target, and lists of interactive rows increase padding instead of leaving gaps.
- MUST: if it looks clickable, it is clickable. Every gesture has a tap/click and keyboard alternative unless the gesture is essential.
- MUST: `touch-action: manipulation` on interactive surfaces. Disable `touch-action` on custom pan or zoom components so native scroll and zoom don't fight them.
- MUST: mobile `<input>` font-size ≥16px, or iOS zooms on focus.
- NEVER: disable zoom (`user-scalable=no`, `maximum-scale=1`).
- SHOULD: gate hover styles behind `@media (hover: hover)` (and `(pointer: fine)`) so touch presses don't show sticky hover.
- SHOULD: set `-webkit-tap-highlight-color` to match the design, and replace it with a real pressed state rather than just removing it.
- MUST: `overscroll-behavior: contain` in modals, drawers and sheets.
- MUST: during drag, disable text selection and set `inert` on the dragged element's content.
- SHOULD: keep a drag alive after the pointer leaves a small control (use `setPointerCapture`), because sliders disappear under the thumb.
- SHOULD: render menus and popovers where the finger doesn't cover them.
- SHOULD: don't autofocus inputs on touch devices, because the keyboard covers the screen. On desktop, autofocus when there's a single primary input.
- SHOULD: apply `muted` and `playsinline` to autoplaying `<video>` so it plays on iOS.
- SHOULD: interactive elements disable `user-select` on their inner content, and decorative layers (glows, gradients) set `pointer-events: none` so they don't steal events.
- SHOULD: use a "prediction cone" (safe triangle) for nested menus so moving diagonally toward a submenu doesn't close it.
- SHOULD: delay the first tooltip in a group (~150ms or more), then let adjacent tooltips open instantly while one is already showing.

## 3. Forms and inputs
- MUST: clicking a label focuses its input. Wrap inputs in `<form>` so Enter submits. In a `<textarea>`, ⌘/Ctrl+Enter submits.
- MUST: correct `type` and `inputmode`, `autocomplete` plus a meaningful `name`. Don't trigger password managers on non-auth fields: avoid reserved names and use `autocomplete="off"` or a specific token like `one-time-code`.
- MUST: work with password managers and 2FA, and allow pasting codes.
- NEVER: block paste (`onPaste` + `preventDefault`).
- MUST: accept free text and validate after. Don't block typing. Allow incomplete submission so errors appear.
- MUST: errors appear inline next to the field. On submit, focus the first error. Highlight every invalid field.
- MUST: keep submit enabled until the request starts, then disable it with a spinner while keeping the label. Include an idempotency key.
- MUST: trim values, because text expansion and paste add trailing spaces.
- MUST: warn on unsaved changes (`beforeunload` or a router guard).
- MUST: inputs are hydration-safe (see section 13).
- SHOULD: disable spellcheck (and usually autocorrect/autocomplete) for emails, codes, usernames and technical fields.
- SHOULD: use HTML validation (`required`, `pattern`, `min`) where it fits.
- SHOULD: placeholders show an example value and end with `…` (`+1 (123) 456-7890`, `sk-0123456789…`).
- SHOULD: absolutely position input prefix and suffix decorations (icons, units) over the input with matching padding, and make clicking them focus the input.
- SHOULD: toggles take effect immediately, with no Save or confirm step.
- SHOULD: use "ghost inputs" (borderless until hover or focus) for table-like editable data, and drop the input entirely for read-only fields.

## 4. Feedback, state and navigation
- MUST: the URL reflects state: filters, tabs, pagination, expanded panels, selected item.
- MUST: Back/Forward restores scroll position.
- MUST: links are `<a>`/`<Link>` (so middle-click, ⌘-click and prefetch work). NEVER use `<div onClick>` for navigation.
- MUST: confirm destructive actions or provide an Undo window.
- MUST: polite `aria-live` for toasts and inline validation.
- SHOULD: optimistic UI. Update locally, reconcile on response, and on failure roll back with feedback or offer retry.
- SHOULD: show feedback relative to its trigger: an inline checkmark after copy, not a toast, and highlight the inputs that caused an error.
- SHOULD: loading states get a show-delay (~150–300ms) and a minimum visible time (~300–500ms) to avoid flicker. `<Suspense>` does this.
- SHOULD: `…` on menu items that open a follow-up ("Rename…") and on loading labels ("Saving…").
- SHOULD: redirect for auth on the server before the client loads, to avoid URL jank.
- MUST: no dead ends. Every error and empty state offers a way forward.

## 5. Motion (full guidance in the `interface-motion` skill)
- MUST: honor `prefers-reduced-motion`. Pause decorative loops rather than snapping them (`animation-play-state: paused`). Interactions the user drives directly can stay.
- MUST: animate `transform` and `opacity` only. NEVER animate `top`, `left`, `width` or `height` for interaction feedback.
- NEVER: `transition: all`. List the properties.
- MUST: animations are interruptible and input-driven. Autoplay only muted, non-essential loops, and give anything autoplaying for >5s alongside content a pause, stop or hide control.
- MUST: correct `transform-origin`: popovers grow from their trigger.
- MUST: SVG transforms go on a `<g>` wrapper with `transform-box: fill-box` (Safari origin bugs).
- SHOULD: interaction feedback ≤200ms. Scale in from 0.9–0.97 depending on size (never 0; exact ranges in `interface-motion`). Button press ~0.97.
- SHOULD: frequent, low-novelty actions (context menu open, list add/remove, trivial hovers) skip entrance animation. macOS menus animate out but not in.
- SHOULD: switching themes doesn't trigger transitions (disable them for one frame, as next-themes does).
- SHOULD: pause looping animations when off-screen.
- SHOULD: `scroll-behavior: smooth` for in-page anchors, with a `scroll-margin-top` offset.
- SHOULD: prefer CSS, then the Web Animations API, then JS libraries.

## 6. Typography
- SHOULD: `-webkit-font-smoothing: antialiased` and `text-rendering: optimizeLegibility`. Subset fonts to the needed scripts (`unicode-range`) and limit variable axes.
- MUST: font weight doesn't change on hover or selected state (it causes layout shift).
- SHOULD: no weights below 400 for UI text. Medium headings look best at 500–600.
- SHOULD: fluid display sizes with `clamp()`, e.g. `clamp(48px, 5vw, 72px)`.
- MUST: `font-variant-numeric: tabular-nums` for tables, timers, prices, counters and comparisons.
- SHOULD: `-webkit-text-size-adjust: 100%` to stop iOS landscape text inflation.
- SHOULD: `text-wrap: balance` on headings and `text-wrap: pretty` on body text. Avoid widows and orphans.
- SHOULD: curly quotes. Hang punctuation on pull quotes (`text-indent: -0.4em`).
- SHOULD: scaling text changes its anti-aliasing, so animate a wrapper, not the text node.
- SHOULD: preload critical fonts with `font-display: swap`.

## 7. Content and copy
- MUST: `…` (U+2026), never `...`.
- MUST: non-breaking spaces in `10&nbsp;MB`, `⌘&nbsp;K` and multi-word brand names. Use `&#x2060;` (word joiner) where no space should appear.
- MUST: `<title>` matches the page or context.
- MUST: skeletons mirror final content size and shape.
- MUST: design empty, sparse, dense and error states. Empty states prompt creation, optionally with templates.
- MUST: redundant status cues: not color alone. Icons carry text labels or an accessible name.
- MUST: locale-aware formatting (`Intl.DateTimeFormat`, `Intl.NumberFormat`, `Intl.RelativeTimeFormat`). Detect language from `Accept-Language`/`navigator.languages`, never from IP.
- SHOULD: inline help first. Tooltips are a last resort ("tooltips kinda mean we failed as designers" — Rauno).
- SHOULD: `translate="no"` on brand names, code tokens and identifiers.
- SHOULD (copy conventions):
  - Active voice, second person.
  - Action-oriented, specific labels ("Save API Key", not "Continue").
  - Numerals for counts ("8 deployments").
  - Errors say what happened and how to recover ("Your API key is incorrect or expired. Generate a new key in your account settings.").
  - Keep nouns consistent, one term per concept.
  - Currency uses either 0 or 2 decimals in a given context, never mixed.

## 8. Content handling (resilience)
- MUST: text containers handle long content (`truncate`, `line-clamp-*`, `break-words`/`overflow-wrap: anywhere` for URLs and hashes).
- MUST: flex and grid children that truncate need `min-width: 0`.
- MUST: no broken UI for empty strings or empty arrays.
- MUST: resilient to short, average and very long user-generated content.

## 9. Accessibility semantics
- MUST: native semantics before ARIA (`<button>`, `<a>`, `<dialog>`, `<details>`, `<label>`).
- MUST: icon-only buttons have an `aria-label` naming action and target ("Copy deployment URL"). Don't add `aria-label` to a button that already has visible text.
- MUST: decorative elements are `aria-hidden`. Illustrations built from HTML/SVG get `role="img"` + `aria-label` on the wrapper and `aria-hidden` on the inner tree.
- MUST: hierarchical headings, a skip link and `scroll-margin-top` on anchor targets.
- MUST: media has captions or transcripts, keyboard-operable controls, and decorative media is hidden from assistive tech.
- MUST: disabled buttons don't carry tooltips (they're out of the tab order, so they're never announced). Explain why inline instead.
- MUST: hover-triggered tooltips contain no interactive content.
- SHOULD: images render with `<img>` (screen readers, right-click copy), not CSS backgrounds, when they are content.
- SHOULD: gradient text unsets its gradient in `::selection`.
- SHOULD: style `::selection` deliberately.
- SHOULD: an SVG favicon whose `<style>` responds to `prefers-color-scheme`.
- SHOULD: verify with the browser's full accessibility tree, not just the DOM.
- SHOULD: code blocks announce copies through a visually hidden `role="log" aria-live="polite"` node, and line numbers use `content: counter(line) / ""` so they're not read aloud.

## 10. Layout
- MUST: deliberate alignment to a grid, baseline or edge. SHOULD: optical alignment (±1px) where geometry misleads.
- SHOULD: balance icon and text lockups (icon size and stroke tuned to the cap height; 16px/1.5 stroke standalone, ~18px/1.75 inline with 20px text).
- MUST: verify on mobile, laptop and ultra-wide (zoom out to 50% to simulate).
- MUST: respect safe areas with `env(safe-area-inset-*)`.
- MUST: avoid unwanted scrollbars. Check with macOS "Show scroll bars: Always" to see what Windows users see.
- SHOULD: flex and grid over JS measurement. Use container queries for widgets that live in varying widths.
- SHOULD: keep a layout's structure and grid position consistent across pages, so navigation reads as instant rather than as a reflow.
- SHOULD: when creating an item at the end of a page, temporarily add height so the new input can scroll to center.
- SHOULD: make concentric hit areas: sibling buttons, never nested `<button>`s.

## 11. Surfaces and color
- SHOULD: layered shadows (tight contact + soft ambient). Keep shadow alphas small (2–6%) with negative spread so the blur stays under the element.
- SHOULD: crisp edges with semi-transparent borders or 1px shadow rings (~8% black on light, ~10–15% white on dark).
- SHOULD: nested radii are concentric: child ≤ parent, inner = outer − padding.
- SHOULD: hue consistency: tint borders, shadows and muted text toward the background hue instead of pure gray.
- MUST: meet contrast. Prefer APCA over WCAG 2 for judgments on dark UIs.
- MUST: `:hover`, `:active` and `:focus` have more contrast than rest.
- MUST: charts are color-blind friendly (don't rely on red/green alone).
- SHOULD: large dark gradients band. Add a subtle noise or dither texture, or use a background image. Scaling and blurring filled rectangles also bands, so use radial gradients instead.
- SHOULD: large `blur()` / `backdrop-filter` values are slow. Keep blur radii modest, especially over large or animated areas.

## 12. Dark mode and theming
- MUST: `color-scheme: dark` (or `light dark`) on `<html>` so scrollbars and form controls match.
- SHOULD: `<meta name="theme-color">` matches the page background.
- MUST: native `<select>` gets an explicit `background-color` and `color` (Windows renders it light otherwise).
- SHOULD: no flash of the wrong theme. A blocking script in `<head>` sets the class before paint (next-themes does this).

## 13. Hydration
- MUST: controlled inputs with `value` have `onChange`, or use `defaultValue`.
- SHOULD: guard date and time rendering against server/client mismatch (render on the client, or pass a fixed timestamp).
- SHOULD: `suppressHydrationWarning` only where truly needed (the theme class on `<html>`, timestamps).

## 14. Performance
- MUST: reserve space for media: explicit `width`/`height` or `aspect-ratio`, and placeholders (tiny blurred base64 with `filter: blur(32px); scale: 1.2`).
- MUST: preload above-the-fold images (`priority` / `fetchpriority="high"`) and lazy-load the rest (`loading="lazy"`).
- MUST: virtualize lists >50 items (or use `content-visibility: auto`).
- MUST: batch layout reads and writes. Never read layout (`getBoundingClientRect`, `offsetHeight`, `scrollTop`) during render.
- MUST: track re-renders (React DevTools, React Scan). Profile with CPU and network throttling and with extensions disabled.
- MUST: mutations complete in <500ms, or are optimistic.
- SHOULD: test iOS Low Power Mode and macOS Safari.
- SHOULD: uncontrolled inputs where possible.
- SHOULD: bypass React for real-time values: write to refs, `el.style` or CSS variables in the event handler.
- SHOULD: `will-change` only for the duration of a heavy animation, never pre-emptively everywhere. Use `translateZ(0)` sparingly.
- SHOULD: pause or unmount off-screen videos, since many autoplaying videos choke iOS. Prefer `<video autoplay muted loop playsinline>` over GIF, with a reduced-motion still fallback.
- SHOULD: `preconnect` to CDNs (with `crossorigin` when needed). Move long tasks to Web Workers.
- SHOULD: adapt to device capability (reduced motion, low memory, save-data) before shipping heavy visuals.

## 15. Anti-pattern list (flag on sight)
- `user-scalable=no` or `maximum-scale=1`
- `onPaste` + `preventDefault`
- `transition: all` / Tailwind `transition-all`
- `outline: none` / `outline-none` without a `focus-visible` replacement
- `<div>`/`<span>` with click handlers. Navigation via `onClick` instead of `<a>`
- images without dimensions
- large arrays `.map()`ed without virtualization
- form inputs without labels. Icon buttons without `aria-label`
- hardcoded date or number formats
- `autoFocus` without clear justification
- animated GIF where compressed video fits
- gesture-only actions with no click or keyboard alternative
- `...` in user-facing strings
- font-weight change on `:hover` or selected state
- animating from `scale(0)`
- `setState` on `pointermove`/`scroll` for purely visual values
