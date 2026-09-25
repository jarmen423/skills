---
name: interface-guidelines
description: How an interface behaves — the small rules that make web UI feel solid and trustworthy, from Rauno Freiberg's and Vercel's Web Interface Guidelines and Geist's component rules. Covers focus rings, keyboard support, hit targets, forms and validation, loading/empty/error states, toasts, tooltips, menus, dialogs, tabs, UI copy, touch, hydration and accessibility, with an audit mode (scanner script, file:line report). Use when building or reviewing any interactive component, when asked to audit, sand or check accessibility, or when something feels broken or unreliable. Animation belongs to interface-motion; colors and type to devtool-visual-system.
---

# Interface guidelines

"Interfaces succeed because of hundreds of choices" (Vercel). Most of them go unnoticed when right and are felt immediately when wrong: a clipped focus ring, a double-submitted form, a label that jitters on hover, a spinner that flashes for 40ms. This skill is the checklist of those choices and the reasoning behind them, so you can apply them while building and catch them while reviewing.

The rules come from people who ship this work at Vercel and Linear. Rauno Freiberg's framing is the one to hold onto: "If your UI only works 80% of the time, the perception of quality breaks. It's lipstick on a pig. Core interactions — scrolling, text input, navigation — must always work perfectly." Robustness comes before flourish.

## Two modes

**Build mode** (you are writing UI). Apply the rules for the element types you touch. For a component type listed in `references/components.md` (button, tooltip, modal, toast, skeleton, spinner, menu, tabs, segmented control, input, empty state, command menu), read its entry before writing it. Finish with the quick pass at the end of this file.

**Audit mode** (the user asks for a review, audit or polish pass).
1. Scope the files (the diff, a route, or the paths named).
2. Run the scanner for mechanical candidates: `bash <this-skill-dir>/scripts/scan.sh <paths…>` (`<this-skill-dir>` is the base directory this skill was loaded from). It greps for known anti-patterns. Treat every hit as a *candidate*: open the line and confirm it before reporting, because grep can't see context (a global focus style, a wrapper that adds the label, a spread that isn't an ellipsis).
3. Read each file against the relevant categories in `references/rules.md`. The scanner can't find missing things (no empty state, no `aria-live`, no Undo), so this reading step is where most real findings come from.
4. Report in the format below. Offer to fix; don't silently rewrite unless asked.

## The rules that matter most

The full list with MUST/SHOULD/NEVER levels is in `references/rules.md`. These are the ones that most often separate "competent" from "considered".

**Focus and keyboard**
- Every focusable element gets a visible `:focus-visible` ring. `outline: none` / `outline-none` with no replacement is the most common regression. It usually arrives via a component library class and silently beats a global focus style.
- Draw rings with `box-shadow: 0 0 0 2px var(--bg), 0 0 0 4px var(--focus)`: a 2px gap plus a 2px ring. It follows `border-radius` everywhere, and the gap keeps it legible on any surface. Don't transition the ring (`transition: none` on `:focus-visible`), because a fading focus ring reads as lag. On colored or error surfaces, switch to an inset high-contrast ring.
- Full keyboard support per WAI-ARIA APG: trap focus in modals, return it to the trigger on close, arrow keys in lists and menus, Escape closes.
- Sticky headers must never cover focused elements. Use `scroll-margin-top` on anchor targets.

**Targets and touch**
- Hit targets are at least 24px (44px on touch). If the visual is smaller, expand the hit area with padding or a pseudo-element, not the visual. Lists of interactive rows have no dead gaps between items: grow padding instead of adding margin.
- Label and control share one hit target (checkboxes, radios, toggles). Clicking a label focuses its input.
- Gate hover styles behind `@media (hover: hover) and (pointer: fine)` so taps don't leave stuck hover states.
- Mobile `<input>` font-size is at least 16px, or iOS zooms on focus. Never disable zoom (`user-scalable=no`, `maximum-scale=1`).
- `touch-action: manipulation` removes the double-tap-zoom delay. Replace the iOS tap highlight rather than just deleting it.

**Forms**
- Wrap inputs in a `<form>` so Enter submits. In a `<textarea>`, ⌘/Ctrl+Enter submits.
- Keep submit enabled until the request starts, then disable it and show a spinner *next to the original label*. The button shouldn't morph into a gray disabled blob; loading is functionally disabled, not visually. Include an idempotency key for mutations.
- Accept free text and validate after (on blur or submit), never by blocking keystrokes. Allow submitting incomplete forms so validation can speak. On submit, focus the first error. Errors sit inline next to the field and name the fix.
- Correct `type`, `inputmode`, `autocomplete` and a meaningful `name`. Disable spellcheck for emails, codes and usernames. Never block paste. Trim values.
- Placeholders are example values ending in `…` (`sk-0123456789…`), not instructions.
- Warn before discarding unsaved changes.

**Feedback and state**
- Show feedback where the action happened. A copy button swaps its icon to a checkmark for ~1.5s; it doesn't fire a toast.
- Prefer optimistic updates: reconcile on response, roll back with an explanation on failure. Destructive actions get a confirm step or an Undo window (5–10s, with the literal label "Undo").
- Toasts and inline validation announce through `aria-live="polite"`.
- Spinners and skeletons get a show-delay (~150–300ms) and a minimum visible time (~300–500ms), so fast responses don't flicker. React `<Suspense>` does this for you.
- Skeletons mirror the final layout's size and shape. "A 200×20 block becoming an 80×16 string reads as a glitch."
- Design every state: empty, sparse, dense, error, very long content. Empty states prompt the next action with one primary CTA.
- The URL reflects state (tabs, filters, pagination, open panels), and Back/Forward restore scroll position.

**Motion.** The details live in the `interface-motion` skill. The guideline-level rules:
- Animate `transform` and `opacity`. Never `transition: all`, because it animates layout properties you didn't intend.
- Honor `prefers-reduced-motion`.
- Frequent, low-novelty actions don't animate in: context menus, command menus, list add/remove.
- Set `transform-origin` to where the element comes from.

**Typography and content**
- Font weight never changes on hover or selection, because it shifts layout. Change color instead.
- `font-variant-numeric: tabular-nums` for anything that updates or gets compared: timers, prices, tables, counters.
- Use `…` not `...`, curly quotes not straight ones, and a non-breaking space between a number and its unit (`10&nbsp;MB`) and inside shortcuts (`⌘&nbsp;K`).
- Use `text-wrap: balance` on headings and `text-wrap: pretty` on paragraphs to avoid widows.
- Flex children that should truncate need `min-width: 0`. Every text container must survive empty, short and absurdly long content.
- Format dates and numbers with `Intl.*`, never by hand.
- Unset gradient text on `::selection`, or selected text becomes invisible.

**Layout and surfaces**
- Nested radii are concentric: inner radius = outer radius − padding.
- Use layered shadows (a tight contact shadow plus a soft ambient one) and semi-transparent borders, so edges stay crisp on any background.
- `:hover`, `:active` and `:focus` must have *more* contrast than rest.
- Align deliberately to a grid, baseline or edge, and optically adjust by ±1px where geometry lies (play icons, arrows, rounded glyphs).
- Check mobile, laptop and ultra-wide (zoom to 50%). Respect `env(safe-area-inset-*)`. No accidental horizontal scrollbars.

**Performance** (it's a feature of the design)
- Reserve space for media with explicit dimensions or `aspect-ratio` to avoid CLS. Preload above-the-fold images and lazy-load the rest.
- Virtualize lists over ~50 items. Batch layout reads and writes, and never read layout during render.
- Write real-time values (pointer position, scroll progress) straight to the DOM or CSS variables through refs, not through React state.
- Pause looping animations and videos when off-screen.
- Mutations should finish in under 500ms. If they can't, make them optimistic.

## Components

`references/components.md` holds per-component rules for Button, Tooltip, Modal, Toast, Skeleton, Spinner, Menu, Tabs, Segmented control, Input, Empty state and Command menu, plus the copywriting conventions they share. Read the relevant entry before building one of these. The rules are specific (tooltip delay ~150ms, menus cap at ~10 items, destructive modals default focus to Cancel), and specifics are what make components feel native.

## Sanding: finding what the checklist can't

Rauno Freiberg, borrowing Jim Nielsen's term, calls this "sanding": "just click around a lot until you stop finding broken states." When you can run the UI (see the `run` skill, or Playwright if available), do this before calling it done:
- Spam-click every button and toggle. Does anything double-fire, shift or get stuck?
- Tab through the page. Is every stop visible, in DOM order, and never hidden under a sticky header?
- Resize from 320px to ultra-wide. Try empty data, one item, a thousand items and a 200-character name.
- Throttle CPU and network. Does the loading state flicker or stall? Do state transitions play on first page load? They shouldn't. "Often state transitions accidentally play out when the page loads, but this makes the application feel poorly built."
- Turn on reduced motion and check nothing important disappears.
- For complex widgets, add temporary keyboard shortcuts that flip between states (loading, error, empty, expanded) so you can test transitions quickly.

## Audit report format

Group findings by file with one line per finding, clickable, most severe first. State the issue and location; add a fix only when it isn't obvious. No preamble.

```
src/components/ui/button.tsx
  src/components/ui/button.tsx:8 [must] `outline-none` removes the focus ring; global :focus-visible is overridden by the utility → drop `outline-none` so the global outline applies, or add `focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-canvas` (Tailwind rings compose with the variant's `shadow-*`; an arbitrary `shadow-[…]` would replace it)
  src/components/ui/button.tsx:8 [should] loading state missing; add `loading` that keeps label + spinner, pointer-events-none

src/app/pricing/page.tsx
  ✓ pass
```

Severity: `[must]` for accessibility, data-loss or broken-interaction issues; `[should]` for polish. If a rule conflicts with an explicit product decision in the code or comments, mention the conflict instead of flagging it as a bug.

## Quick pass before you finish building
- [ ] Focus ring visible on every interactive element; keyboard can reach and operate everything
- [ ] Hit targets ≥24px (44px touch); no hover styles on touch
- [ ] Loading, empty, error and long-content states exist and don't shift layout
- [ ] Buttons: disabled only while the request runs, label kept, no double submit
- [ ] Only `transform`/`opacity` animate; no `transition: all`; reduced motion respected
- [ ] `…`, curly quotes, `tabular-nums` where numbers change, `Intl` for dates and numbers
- [ ] Icon-only controls have `aria-label`; decorative layers have `aria-hidden` and `pointer-events: none`

## In this repo (agent-memory-labs-frontend)
- The global focus style is `:focus-visible { outline: 2px solid var(--color-accent) }` in `src/app/globals.css` (base layer). Any Tailwind `outline-none` utility overrides it, and shadcn primitives in `src/components/ui/` use that class, so check that each one supplies its own `focus-visible:` ring.
- The global rule also sets `border-radius: 6px` on focus. It's in the base layer, so `rounded-*` utilities and `.card` override it. It only visibly affects focused elements with no radius of their own, like links and images.
- Tokens: `--color-ring` (#8fb3ff) for focus, `--color-canvas` for the ring gap, `.kbd` for keyboard hints. The bottom of `globals.css` has a blanket `prefers-reduced-motion` block that sets every animation and transition to ~0ms, fades included. That's blunter than "gentler, not zero", but it does stop every loop. New decorative loops should still use `motion-safe:`.
