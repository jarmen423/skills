# Bespoke: design engineering skills

Seven agent skills for building interfaces in the Linear / Vercel "devtool" school, where visual design, motion and front-end engineering are one job. Each one is distilled from primary sources: production CSS, library source code and the designers' own writing. They are not generic advice.

**Stance:** the skills are meant to **elevate a project, not maintain it**. An agent using them treats the project's current design as material to critique, and breaks out of its patterns to give it a distinct, bespoke point of view. It stays within the existing look only when explicitly told to. The "restraint" in the sources (Rauno's 90% familiar / 10% novel, Linear's "don't compete for attention you haven't earned") is a taste principle about where attention goes: keep the frequent paths calm so the bold, signature moments land. It is never a reason to preserve something generic.

| Skill | Use it for | Distilled from |
|---|---|---|
| `design-engineering` | Entry point: the workflow (intent → references → static build → motion → sanding → perf/a11y → review) and routing | Vercel's design-engineering team, Rauno Freiberg, Emil Kowalski, Paco Coursey, Manu Arora |
| `interface-guidelines` | Focus, keyboard, targets, forms, states, copy, a11y, performance, and a UI audit mode with `scripts/scan.sh` | Rauno's and Vercel's Web Interface Guidelines, Geist component rules, Devouring Details |
| `interface-motion` | Whether to animate, easing, durations, origin, springs, interruptibility, gestures, choreography | Emil Kowalski (animations.dev, Sonner, Vaul source), Rauno's interaction essays, Geist motion tokens |
| `devtool-visual-system` | Dark themes as an OKLCH lightness ladder, borders, text tiers, type, restrained light, marketing anatomy, plus `scripts/theme.py` | linear.app production CSS, Linear's redesign posts, Vercel Geist |
| `bento-grids` | Feature grids: story-first hierarchy, cell anatomy, CSS templates, responsive collapse | bentogrids.com (285 examples), linear.app's grid component, Frontend FYI's Linear rebuild |
| `signature-effects` | Spotlights, beams, lamps, border glows, grain and masks, with an effect budget and hygiene checklist | Aceternity UI component source, Motion's performance tier list, WCAG 2.2.2 / 2.3.3 |
| `command-menu` | ⌘K palettes: a11y pattern, keyboard map, IME guard, ranking, pages, styling | cmdk source and architecture notes, Geist CommandMenu rules |

## Scripts
- `interface-guidelines/scripts/scan.sh [paths…]` greps UI source for anti-patterns and prints `file:line` candidates to verify: `transition-all`, `outline-none` with no ring, disabled zoom, clickable divs, `scale(0)`, ease-in, layout animations, state on pointermove, `Math.random` in render, large blurs and more.
- `devtool-visual-system/scripts/theme.py check --bg <hex> <hex…>` prints OKLCH, WCAG 2 and APCA contrast for each color, with a usage verdict.
- `devtool-visual-system/scripts/theme.py generate --base <hex> --accent <hex> [--contrast 30] [--format css|tailwind|json]` derives a full dark token ladder. At contrast 30 its output reproduces Linear's measured values. It needs no dependencies.

## Install
Copy or symlink each skill folder into `.claude/skills/` (per project) or `~/.claude/skills/` (global). For tools that read `.agents/skills/`, keep the canonical copy there and symlink it into `.claude/skills/`.

Each skill ends with an "In this repo" section written for the `agent-memory-labs-frontend` site where they were first used. If you use them elsewhere, remove or rewrite that section.
