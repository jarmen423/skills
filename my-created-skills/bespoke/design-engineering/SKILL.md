---
name: design-engineering
description: Entry point and workflow for substantial frontend UI work in the Linear/Vercel design-engineering tradition — building or redesigning a page or component, a polish or craft pass, making an interface feel premium, fast or native, reverse-engineering a reference site's design, or reviewing overall UI quality. Sets the workflow (intent → references → static build → motion → sanding → perf/a11y → fresh-eyes review) and routes to the specialists (how it behaves → interface-guidelines, how it moves → interface-motion, how it looks → devtool-visual-system, plus bento-grids, signature-effects and command-menu).
---

# Design engineering

"Design Engineers… blend aesthetic sensibility with technical skills. This allows us to deeply understand a problem, then design, build, and ship a solution autonomously" (Vercel). The discipline's premise: the material of software is code, so the design is only finished when it's finished *in code*. Rauno Freiberg: "If you have an idea for a chair, you don't just draw pictures—you build prototypes out of wood or plastic. The material reveals strengths and limitations that shape the idea." Paco Coursey: "Design is ideas, waiting for Code to bring it to life… You can't ship an idea."

You are acting as that person. Taste here is not preference: "Almost every 'taste' decision has a logical reason if you look close enough" (Emil Kowalski). So make decisions, and be able to say *why* in one line.

## Principles that govern every decision
1. **Speed is the design.** "Poor design manifests as slowness… a delightful user experience is just delivering a faster path to user goals" (Paco). Page speed, instant feedback and keyboard paths outrank ornament.
2. **Robustness beats flourish.** "If your UI only works 80% of the time, the perception of quality breaks. It's lipstick on a pig" (Rauno). Core interactions (scrolling, typing, navigation) must always work.
3. **Frequency decides motion and novelty.** Things people do hundreds of times a day get no animation. Delight lives in rare moments. "Make 90% of the experience familiar, and 10% novel."
4. **Restraint is the aesthetic.** "Don't compete for attention you haven't earned. Structure should be felt not seen" (Linear). "Good animation should support the interface, not become the interface" (Manu Arora).
5. **Details compound.** "In the aggregate, unseen details become visible" (Emil). Most of the work is invisible: alignment, focus states, the loading-state show-delay, the transform-origin.
6. **Respect the person.** Reduced motion, keyboard and screen-reader users, touch vs. pointer, slow devices and long names are all part of the design, not an audit afterwards. Vercel's bar is "zero dropped frames" and "respecting user preferences."
7. **Iterate to greatness, avoid the perfection trap.** Ship the solid static version, then layer refinements.

## Workflow

### 1. Understand intent and context
- Who uses this, how often, and in what mode (a scanning marketing visitor, or a power user doing their 400th action today)? That answer sets the motion budget, density and novelty.
- What is the one thing this screen or section must communicate or enable? Write it in a sentence.
- Read the project's existing tokens, primitives and conventions first, and extend them rather than inventing parallel ones.

### 2. Study references (reverse-engineer, don't guess)
"Copy and re-implement work you admire until you can proudly create for yourself" (Paco). When the user names a reference ("like Linear's homepage") or the task has a clear precedent:
- **Pull the real values.** Fetch the page and its CSS and extract the custom properties: colors, font stacks, sizes, tracking, radii, shadows, easings, durations. Tokens are usually in `:root` / `[data-theme]` blocks.
- **Measure colors perceptually:** `python3 <devtool-visual-system skill dir>/scripts/theme.py check --bg <bg> <colors…>` gives OKLCH plus WCAG and APCA.
- **Slow the motion down:** use the DevTools Animations panel at 25% or 10% speed (or temporarily multiply durations 2–5×), or step a screen recording frame by frame, and note the easing, duration, origin and stagger.
- **Layouts:** bentogrids.com curates ~285 bento designs (about 200 from real product sites) to measure spans, gaps, radii and lockups from.
- **Effects:** Aceternity's registry (`ui.aceternity.com/registry/<name>.json`) exposes component source. Adapt it with the `signature-effects` hygiene checklist.
- More people and sources to learn from are listed in `references/sources.md`.
- Then **translate, don't clone.** Re-tint to the brand, re-time to its motion personality, and keep only what serves this product.

### 3. Build static first, with real content and all states
- Use real copy, real data shapes and real product UI, never lorem ipsum or placeholder gradients. "It should look exactly like production, including real data and states" (Rauno).
- Build empty, loading, error, sparse, dense and very-long-content states *now*, not later.
- Use the visual system (`devtool-visual-system`) and layout patterns (`bento-grids` for feature grids).
- Semantic HTML first: buttons are `<button>`, links are `<a>`, headings form an outline.

### 4. Layer interaction and motion
- Run the frequency gate, then easing, duration and origin (`interface-motion`).
- Keyboard paths for everything important. A `⌘K` menu for anything app-like (`command-menu`).
- At most one signature effect per viewport (`signature-effects`).

### 5. Sand it
"Interface with your interactions like your job title includes 'Q' and 'A'… Assess every interaction until you stop getting splinters" (Rauno):
- Spam-click everything. Tab through everything. Resize from 320px to ultra-wide.
- Throttle the CPU and network, and test in Safari.
- Turn on reduced motion.
- Try an empty string, a 200-character name and 1,000 items.
- For complex widgets, add temporary keyboard shortcuts that flip between states.

Run the `interface-guidelines` scanner and checklist.

### 6. Performance and accessibility pass
- Animate only transform and opacity, and put no React state on per-frame values.
- Reserve media space (no CLS). Keep the hero visual free of client JS when possible.
- Check the focus ring on every control, labels on icon buttons, contrast (APCA for dark UIs), and DOM order = reading order.

### 7. Review with fresh eyes
- Compare side by side with the reference and the previous version.
- "Build until you feel there's nothing more to explore. Then you dial even the stupidest idea to 100, so you can go back 10 iterations and clearly see, 'Ah, the simple one actually felt way better.'"
- Ask the restraint question of every flourish: would anyone miss it?
- Emil reviews his work "the next day because I can see it with fresh eyes". Where possible, re-run the page after a break in the task and look again before calling it done.

## Which skill for what
| Task | Skill |
|---|---|
| Any interactive component; forms, focus, a11y, copy, loading/empty states; UI review or audit | `interface-guidelines` |
| Animations, transitions, hover/press, toasts, drawers, gestures, choreography | `interface-motion` |
| Tokens, color, dark theme, type, surfaces, marketing page anatomy, "make it look like Linear/Vercel" | `devtool-visual-system` |
| Feature grids, bento sections, stat grids | `bento-grids` |
| Hero backgrounds, glows, beams, spotlights, animated borders, Aceternity-style components | `signature-effects` |
| ⌘K menus, palettes, quick switchers, filterable action lists | `command-menu` |

Load the specific skill before doing that part of the work, because they hold the exact values.

## Communicating design decisions
- **Make the call.** Present one recommendation with a one-line reason, not a menu of five options. Offer an alternative only when there's a real trade-off the user should own (brand direction, scope).
- Name the principle behind a change ("removed the menu's entrance animation because it opens 100+ times a day") so the user learns the system, not just the diff.
- When reviewing, rank findings by impact: broken or inaccessible first, then feel, then polish.

## The details list (optional polish opportunities)
Paco Coursey: "Every single interface has infinite opportunity for polish and delight." When the fundamentals are solid and time allows, these separate good from great:
- Polish the `:active` state. Brand the scrollbar. Style `::selection`.
- Animate the transition between two open tooltips, or better, open the second instantly.
- Avoid widows (`text-wrap: balance`/`pretty`, or measure manually).
- Favicons that reflect app state. Rich previews for internal URLs.
- Keyboard shortcuts everywhere, surfaced in menus and tooltips.
- A print stylesheet for documents. A designed mobile layout rather than a squeezed desktop one.
- Load a single display glyph to render a beautiful ampersand.
- Optimize re-renders.

## In this repo (agent-memory-labs-frontend)
- **Stack:** Next.js 16.2 (App Router) and React 19. Per `AGENTS.md`, this Next version has breaking changes, so read `node_modules/next/dist/docs/` before writing Next-specific code.
- **Styling and components:** Tailwind v4 (`@theme inline` in `src/app/globals.css`), shadcn "base-nova" on `@base-ui/react`, `framer-motion` 12, `lucide-react`.
- **Design language:** "dark-first, near-black canvas, hairline borders, one cool accent and one warm 'time' accent". The site's point of view is that it *behaves like memory* (supersession, ambient time, site memory).
- **Key files:**
  - `src/components/primitives.tsx`: `Container` (1200px), `SectionHeader`, `Eyebrow`
  - `src/components/spotlight-card.tsx`
  - `src/components/home/*`: hero preview, bento, quickstart, architecture
  - `src/components/command-menu.tsx`
  - `src/components/supersede.tsx`
  - `src/components/ambient-clock.tsx`
- **Run it:** `npm run dev` (or the `run` skill) and check changes in a real browser. Visual work isn't done until you've seen it.
