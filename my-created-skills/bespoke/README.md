# Bespoke: design engineering skills

One router skill (`bespoke`) with six sub-skills for building interfaces in the Linear / Vercel "devtool" school, where visual design, motion and front-end engineering are one job. Each one is distilled from primary sources: production CSS, library source code and the designers' own writing. They are not generic advice.

**Stance:** the skills are meant to **elevate a project, not maintain it**. An agent using them treats the project's current design as material to critique, and breaks out of its patterns to give it a distinct, bespoke point of view. It has full authority to say a design isn't working and replace it outright, and it stays within the existing look only when explicitly told to. The "restraint" in the sources (Rauno's 90% familiar / 10% novel, Linear's "don't compete for attention you haven't earned") is a taste principle about where attention goes: keep the frequent paths calm so the bold, signature moments land. It is never a reason to preserve something generic.

| Skill | Use it for | Distilled from |
|---|---|---|
| `bespoke` (`SKILL.md`) | Router: the mandate, the workflow (intent → references → static build → motion → sanding → perf/a11y → review) and routing | Vercel's design-engineering team, Rauno Freiberg, Emil Kowalski, Paco Coursey, Manu Arora |
| `interface-guidelines` | Focus, keyboard, targets, forms, states, copy, a11y, performance, and a UI audit mode with `scripts/scan.sh` | Rauno's and Vercel's Web Interface Guidelines, Geist component rules, Devouring Details |
| `interface-motion` | Whether to animate, easing, durations, origin, springs, interruptibility, gestures, choreography | Emil Kowalski (animations.dev, Sonner, Vaul source), Rauno's interaction essays, Geist motion tokens |
| `devtool-visual-system` | Dark themes as an OKLCH lightness ladder, borders, text tiers, type, restrained light, marketing anatomy, plus `scripts/theme.py` | linear.app production CSS, Linear's redesign posts, Vercel Geist |
| `bento-grids` | Feature grids: story-first hierarchy, cell anatomy, CSS templates, responsive collapse | bentogrids.com teardowns, linear.app's grid component, Frontend FYI's Linear rebuild |
| `signature-effects` | Spotlights, beams, lamps, border glows, grain and masks, with an effect budget and hygiene checklist | Aceternity UI component source, Motion's performance tier list, WCAG 2.2.2 / 2.3.3 |
| `command-menu` | ⌘K palettes: a11y pattern, keyboard map, IME guard, ranking, pages, styling | cmdk source and architecture notes, Geist CommandMenu rules |

`bespoke/SKILL.md` is the only skill an agent sees at startup. The six sub-skills keep their own `SKILL.md` files in nested folders; installers and Claude Code only register the top-level one, and the router tells the agent which sub-skill to read and when.

## Scripts
- `interface-guidelines/scripts/scan.sh [paths…]` greps UI source for anti-patterns and prints `file:line` candidates to verify: `transition-all`, `outline-none` with no ring, disabled zoom, clickable divs, `scale(0)`, ease-in, layout animations, state on pointermove, `Math.random` in render, large blurs and more.
- `devtool-visual-system/scripts/theme.py check --bg <hex> <hex…>` prints OKLCH, WCAG 2 and APCA contrast for each color, with a usage verdict.
- `devtool-visual-system/scripts/theme.py generate --base <hex> --accent <hex> [--contrast 30] [--format css|tailwind|json]` derives a full dark token ladder. At contrast 30 its output reproduces Linear's measured values. It needs no dependencies.

## Install
```sh
bunx skills add jarmen423/skills/my-created-skills --skill bespoke
```
This installs the whole `bespoke/` folder, sub-skills included, as a single skill. To install by hand, copy or symlink `bespoke/` into `.claude/skills/` (per project) or `~/.claude/skills/` (global).

For uploads that take one zip (for example claude.ai), run `python build_bundle.py`. It writes `dist/bespoke.zip` with the sub-skills renamed to `GUIDE.md`, so the uploader sees one skill.

The router and each sub-skill end with an "In this repo" section written for the `agent-memory-labs-frontend` site where they were first used. If you use them elsewhere, remove or rewrite that section.
