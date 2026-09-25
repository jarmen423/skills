# Sources and people to learn from

The primary material behind these skills, plus where to look for more. "Reverse engineering things like this is a great way to learn. Be curious and inspect lots of animations" (Emil Kowalski).

## Writing that shaped these skills
**Rauno Freiberg** (Staff Design Engineer, Vercel; co-author of cmdk). rauno.me
- *Invisible Details of Interaction Design*: rauno.me/craft/interaction-design. Metaphors, kinetic physics, gestures, frequency and novelty, Fitts's law, implicit input.
- *Novelty*: rauno.me/craft/novelty. 90% familiar / 10% novel, and gating one-time animations.
- *Designing Depth*: rauno.me/craft/depth. Dirtying the frame, choreography, blur as depth.
- *What will you ship?* (the Vercel homepage build) and *Crafting the Next.js Website*: grids, focus rings, performance-first visuals.
- Field Notes: rauno.me/notes/1–5.
- The original Web Interface Guidelines: github.com/raunofreiberg/interfaces.
- *Devouring Details*: devouringdetails.com, an interactive reference manual. The Next.js Dev Tools and Behind Scenes chapters are free.

**Emil Kowalski** (Design Engineer, Linear; formerly Vercel; author of Sonner and Vaul). emilkowal.ski
- *Great Animations*, *Good vs Great Animations*, *You Don't Need Animations*, *7 Practical Animation Tips*, *The Magic of Clip Path*, *CSS Transforms*, *Building a Toast Component*, *Building a Drawer Component*, *Building a Hold to Delete Component*, *Train Your Judgement*, *Agents with Taste*, *Developing Taste*.
- His agent skills: github.com/emilkowalski/skill (animation decision framework, recipes, review format).
- The course: animations.dev.
- Source worth reading: github.com/emilkowalski/sonner and github.com/emilkowalski/vaul.

**Paco Coursey** (Webmaster, Linear; formerly Vercel). paco.me
- Writing: disabling theme transitions, custom underlines, px vs rem, Safari's dark-mode favicon contrast, and craft demos (exclusion tabs, iOS menu, blur, timeline, macOS windows).
- cmdk: github.com/dip/cmdk (formerly pacocoursey/cmdk). Read ARCHITECTURE.md and command-score.ts.
- next-themes: github.com/pacocoursey/next-themes. A no-flash theming script.
- Interview: ui.land/interviews/paco-coursey.

**Linear's design writing**. linear.app/now
- *How we redesigned the Linear UI (part II)*: LCH theme generation from base, accent and contrast. Inter Display.
- *A calmer interface for a product in motion* (2026): "Don't compete for attention you haven't earned", "Structure should be felt not seen".
- *A design reset (part I)*, and *Invisible details* (the context-menu safe triangle).
- linear.app/method.

**Vercel**
- Web Interface Guidelines: vercel.com/design/guidelines, with an agent version at github.com/vercel-labs/web-interface-guidelines (AGENTS.md, command.md).
- The Geist design system: vercel.com/geist (colors, typography, materials, component guidance).
- *Design Engineering at Vercel*: vercel.com/blog/design-engineering-at-vercel.

**Manu Arora / Aceternity UI**
- ui.aceternity.com: effect components. Source is available through `ui.aceternity.com/registry/<name>.json`.
- blog.aceternity.com: bento grid and template build posts.

**Layout references**
- bentogrids.com: ~285 curated bento designs (about 200 from product websites, the rest graphic or keynote work), filterable by web, graphic, animation and dark/light.
- The Frontend FYI "Rebuilding Linear's homepage" series and repo: github.com/frontendfyi/rebuilding-linear.app (Next.js + Tailwind, CSS-only animations).
- iamsteve.me/blog/bento-layout-css-grid: container queries and art-directed images in bento cells.

**Performance and accessibility**
- Motion's web animation performance tier list: motion.dev/blog/web-animation-performance-tier-list.
- Chrome's "Animating a blur": developer.chrome.com/blog/animated-blur.
- WCAG 2.2.2 (Pause, Stop, Hide) and 2.3.3 (Animation from Interactions).
- WAI-ARIA Authoring Practices: w3.org/WAI/ARIA/apg (combobox, menu, dialog, tabs patterns).

## Design engineers worth following
From the Design Engineers hub (design-engineers-x.vercel.app, 89 people):
- **Vercel:** Rauno Freiberg, Shu Ding, John Phamous (prediction cones, optical alignment), James Clements, shadcn
- **Linear:** Paco Coursey, Emil Kowalski, Gavin Nelson, Yann-Edern Gillet
- **Elsewhere:**
  - Jhey Tompkins (jhey.dev, CSS experiments)
  - Maxime Heckel (maximeheckel.com, shaders and springs)
  - Dan Hollick (Tailwind)
  - Mariana Castilho (uilabs.dev)
  - Jakub Krehel (jakub.kr)
  - Max Barvian (barvian.me)
  - Aiden Bai (React Scan, Million)
  - Julien Thibeaut (ibelick.com)
  - Samuel Kraft (Raycast)
  - Manu Arora (Aceternity)

Their personal sites are usually the best documentation of their techniques. Most post breakdowns on X, which you usually can't fetch, so prefer their sites and repos.
