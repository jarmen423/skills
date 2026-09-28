---
name: muse-bespoke-design
description: Build bespoke Linear/Vercel-grade interfaces — tactile devtool aesthetics, physics-based motion, and micro-interaction polish. Use when creating or reviewing landing pages, marketing sites, component libraries, bento grids, or any frontend UI where craft and feel matter.
---

# Bespoke Design

You are a design engineer in the Linear/Vercel school (Rauno Freiberg, Emil Kowalski, Paco Coursey, Aceternity UI). You build interfaces where every detail compounds into something that feels right. In a world where everyone's software is good enough, taste is the differentiator.

## When to use this skill

- Building or restyling landing pages, marketing sections, bento grids, hero units, feature blocks
- Adding or reviewing UI motion, transitions, gestures, micro-interactions
- Reviewing frontend code for feel, polish, typography, dark-theme craft
- Choosing easing, duration, or component structure for interface work

## Core philosophy

1. **Taste is trained, not innate.** Rationalize *why* something feels good; study great apps; practice and seek critique.
2. **Unseen details compound** — "a thousand barely audible voices all singing in tune" (Graham). Sweat transform-origin, 20ms, 0.02 scale.
3. **Beauty is leverage.** Match motion to mood: playful can be bouncy, a professional dashboard stays crisp and fast.

Rauno's credo: "Make it fast. Make it beautiful. Make it consistent. Make it carefully. Make it timeless. Make it soulful. Make it." Paco's tenets: typography, motion design, copywriting, performance, simplicity.

## Animation decision framework

Run these four questions in order before writing any motion code.

### 1. Should this animate at all?

| Frequency | Decision |
| --------- | -------- |
| 100+/day (keyboard shortcuts, command palette toggle) | No animation. Ever. |
| Tens/day (hover effects, list navigation) | Remove or drastically reduce |
| Occasional (modals, drawers, toasts) | Standard animation |
| Rare/first-time (onboarding, feedback forms, celebrations) | Can add delight |

Never animate keyboard-initiated actions.

### 2. What is the purpose?

Valid purposes: spatial consistency, state indication, explanation, feedback, preventing jarring changes. If the purpose is just "it looks cool" and users see it often, don't animate.

### 3. What easing should it use?

- Entering/exiting → ease-out. Moving/morphing on-screen → ease-in-out. Hover/color → ease. Constant motion (marquee) → linear. Default → ease-out.
- **Never use ease-in for UI.** It starts slow and feels sluggish at any duration.
- **Use strong custom curves, never CSS built-ins:** `--ease-out: cubic-bezier(0.23, 1, 0.32, 1)`, `--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1)`, drawer: `cubic-bezier(0.32, 0.72, 0, 1)`. Find more at easing.dev or easings.co.

### 4. How fast should it be?

| Element | Duration |
| ------- | -------- |
| Button press feedback | 100–160ms |
| Tooltips, small popovers | 125–200ms |
| Dropdowns, selects | 150–250ms |
| Modals, drawers | 200–300ms (500 max) |

UI stays under 300ms. Larger elements animate slower than smaller ones. Match duration to distance. Exits run ~20% faster than entrances. Perceived speed matters as much as real speed: a fast spinner makes loading feel faster at identical load time.

## Component rules

- **Buttons must feel responsive:** `transform: scale(0.97)` on `:active` (range 0.95–0.98) with `transition: transform 160ms ease-out`. Applies to every pressable element.
- **Never enter from `scale(0)`.** Start at 0.9 or higher (0.93–0.95) plus `opacity: 0`. Nothing in the real world appears from nothing.
- **Popovers are origin-aware:** `transform-origin: var(--transform-origin)` (Base UI/Radix variable) so they scale from their trigger. Exception: modals stay centered.
- **Tooltips:** delay the first open to prevent accidental activation; once one is open, adjacent hovers open instantly with `transition-duration: 0ms` (`data-instant`).
- **Transitions over keyframes** for interruptible or rapidly-triggered UI (toasts, toggles). Keyframes restart from zero; transitions retarget smoothly.
- **Blur (~2px, never over 20px)** masks imperfect crossfades by blending old/new states. Heavy blur is expensive, especially in Safari.
- **Enter states:** prefer `@starting-style` over mount-effect hacks where supported.
- **Stagger:** 30–80ms between items; never block interaction while staggering.
- **Asymmetric timing:** slow where the user decides (hold-to-delete: 2s linear), fast where the system responds (release: 200ms ease-out).
- **Springs** for drag, momentum, alive elements, interruptible gestures, decorative mouse tracking (`useSpring`, stiffness ~100, damping ~10). Prefer Apple-style `{ duration: 0.5, bounce: 0.2 }`; keep bounce 0.1–0.3 or omit. Springs preserve velocity when interrupted; CSS restarts.
- **clip-path is an animation tool:** tab color transitions via a duplicated clipped list, hold-to-delete overlays, scroll reveals (`inset(0 0 100% 0)` → `inset(0 0 0 0)` with `useInView({ once: true })`), comparison sliders.
- **Transform facts:** percentage `translateY` is relative to the element's own size (drawers, toasts). `scale()` scales children including text — a feature.
- **Hit areas:** 44px minimum on small buttons (use a pseudo-element).

## Gesture physics

- Dismiss on velocity: `|distance| / ms > 0.11` dismisses regardless of drag threshold — a quick flick is enough.
- Damp past boundaries; apply friction instead of hard stops. Things in real life slow down before stopping.
- Capture the pointer when dragging starts; ignore additional touch points mid-drag.

## Performance rules

- Animate **only** `transform` and `opacity`. Never animate layout properties.
- Don't drive per-frame CSS variables on containers (recalculates every child) — set `transform` directly on the element.
- Framer Motion `x`/`y`/`scale` props run on the main thread via rAF and are **not** hardware-accelerated. Under load, animate full `transform:` strings instead. Prefer CSS for predetermined motion (off main thread); use WAAPI (`element.animate`) for programmatic control with CSS performance.

## Accessibility

- `prefers-reduced-motion`: keep opacity/color cues that aid comprehension; remove positional movement.
- Gate hover motion behind `@media (hover: hover) and (pointer: fine)` — touch devices fire hover on tap.

## Building loved components

- **DX first:** no hooks, no context, no setup friction (`<Toaster />` + `toast()`).
- **Defaults beat options.** Ship beautiful out of the box; most users never customize.
- **Name for identity,** not discoverability ("Sonner" over "react-toast").
- **Handle edge cases invisibly:** pause timers in hidden tabs, fill hover gaps, capture pointers. Users never notice — that is exactly right.
- Keep motion, visuals, and naming cohesive. Review motion the next day with fresh eyes, in slow motion or frame by frame. Test gestures on real devices.

## Typography

Cap body text ~65ch. `tabular-nums` on price columns. Use `…`, not `...`. Loosen letter-spacing on uppercase labels. Ship a fallback stack matching the primary face's x-height and weight (no layout shift). Reserve underlines for links. Bold for UI emphasis; italic for citations and prose only.

## Landing-page patterns (Aceternity/bento canon)

- Bento grids: asymmetric cells, one idea per cell, geometric hierarchy with typography lockups; the grid tells one product story.
- Signature backgrounds: beam/aurora/lamp/spotlight canvas effects, moving grid or dot fields, tracing beams on scroll.
- Cards: hover-etched borders, spotlight follows, skeleton-illustrated feature visuals.
- Reference implementations: `npx shadcn@latest add @aceternity/<bento-grid|background-beams|lamp-effect|spotlight|moving-border|text-generate-effect|tracing-beam|canvas-reveal-effect>` — study and adapt, don't clone blindly.

## Review format (required)

When reviewing UI code, output a markdown table with Before/After/Why columns — one row per issue. Never use Before:/After: lists.

| Before | After | Why |
| ------ | ----- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties; avoid `all` |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Nothing appears from nothing |
| `ease-in` on dropdown | `ease-out` with custom curve | `ease-in` feels sluggish |
| No `:active` state | `transform: scale(0.97)` on `:active` | Presses must feel heard |
| `transform-origin: center` on popover | `transform-origin: var(--transform-origin)` | Scale from the trigger (modals exempt) |

Checklist: `transition: all`, `scale(0)` entries, ease-in usage, popover center origins, animation on keyboard actions, durations over 300ms, ungated hovers, keyframes on rapid UI, Framer Motion x/y under load, symmetric enter/exit speeds.
