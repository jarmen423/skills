# Frontend Design Excellence Router

> A high-signal routing layer and knowledge base for AI agents building production UIs for Mobile Apps and SaaS/Web Apps.

**Core Mandate**  
Every recommendation must achieve **both visual/emotional delight and high performance at the same time**. Beauty and performance are not a tradeoff. The techniques that make interfaces users fall in love with are the same techniques that keep them fast: compositor-only motion, progressive enhancement, asset optimization, proper layering, device capability detection, and local-first state.

If a pattern looks incredible but tanks real-world performance, this router either shows how the best teams make it work or explicitly flags it as high-risk.

## How to Use This Router

When building or reviewing UI:

1. **Match your task** to the closest routing question in the sections below.
2. **Read the short synthesis** for the governing principles and key patterns.
3. **Go to the dedicated content skill** linked in that section for the full set of production examples, detailed techniques, code patterns, and anti-patterns.
4. **Use the Further Reading** as your on-ramp when you need deeper implementation details, framework docs, or engineering case studies.

This router is deliberately slim. The heavy examples, full analysis, and implementation depth live in the individual content skills so agents only load what they actually need.

## Success Criteria for Lovable Frontends

A frontend is "lovable" when it creates:

- **Emotional delight** — users want to interact with the UI itself.
- **Speed / performance** — 60 fps wherever motion exists, excellent Core Web Vitals, INP under 200 ms, perceived-instant response.
- **Ease of use** — the interface shortens the path from intent to action.
- **Conversion impact** — the UI itself increases desire to complete the task.

The goal is interfaces where the UI creates desire independent of (or in addition to) the underlying functionality.

---

## Navigation, Wayfinding & Information Architecture

**Key Routing Questions**

- Are you building navigation for a dense product where users bounce constantly between lists, items, views, and actions?
- Are you building a mobile app with a small set of top-level destinations?
- Is keyboard speed the primary delight lever for power users?
- Do you have deep hierarchical content (pages, files, layers, wikis)?
- Are you tempted by dramatic full-screen menu reveals, 3D transitions, or parallax nav bars?
- Does navigation feel slow because every click triggers a full-page reload?

**Synthesis**  
Lovable navigation is invisible architecture made visible. It shortens the path from intent to action, keeps users oriented with persistent landmarks, and uses motion only to explain relationships. Performance is part of IA: prefetch likely routes, preserve scroll position, use optimistic updates, and animate only compositor-friendly properties (`transform`/`opacity`). Hidden navigation and layout-triggering animations destroy both delight and speed.

**Go to the dedicated content skill:** `navigation-wayfinding.skill.md`

**Further reading & authoritative sources**  
- Linear performance engineering notes
- GitHub Issues navigation performance write-up
- web.dev guidance on view transitions and transform-based movement
- Apple HIG on tab bars and sidebars
- Figma Layers Panel performance case study

---

## Layout, Composition, Visual Hierarchy & Spacing Systems

**Key Routing Questions**

- Are you building a UI that must look premium immediately while staying resilient, responsive, and cheap to render?
- Are you building a dense productivity tool (dashboard, email, issue tracker)?
- Are you building a marketing page or brand story with scroll-driven composition?
- Are you building a native-feeling mobile app?
- Is motion central to the experience?

**Synthesis**  
Great layout is invisible architecture. A disciplined spacing system and clear hierarchy let users feel smart because they can predict where things are, while the browser stays fast because the rules are declarative and compositor-friendly. Use CSS Grid, subgrid, container queries, and tokenized spacing before reaching for JavaScript measurement. Reserve space for images and media to avoid CLS. Animate only `transform` and `opacity`.

**Go to the dedicated content skill:** `layout-composition.skill.md`

**Further reading & authoritative sources**  
- Stripe Connect and accessible color system posts
- Netflix container queries case study
- MDN subgrid and container query guides
- Refactoring UI (spacing and hierarchy chapters)
- Apple HIG layout and materials guidance

---

## Data Display, Tables, Lists, Charts & Complex Visualization

**Key Routing Questions**

- Are you building an interface that must make large or complex data feel calm, controllable, and fast?
- Are you building dense data tables that users scan for minutes at a time?
- Are you rendering long scrollable lists of cards, messages, or feed items?
- Are you designing dashboards with charts and real-time metrics?
- Are you building interactive visualizations users manipulate directly?

**Synthesis**  
The durable rule is to render the decision, not the dataset. Use virtualization for long surfaces, skeleton or deferred rendering during scroll, and selective rendering technology (SVG vs Canvas vs WebGL) based on mark count and interactivity needs. Decouple interaction from rendering. If chart animation makes panning, hovering, or selecting feel sluggish, the animation lost the argument.

**Go to the dedicated content skill:** `data-display-visualization.skill.md`

**Further reading & authoritative sources**  
- Figma Layers Panel performance rebuild
- TanStack Virtual and AG Grid documentation
- web.dev virtualization guides
- Observable Plot and visx guidance
- uPlot performance characteristics

---

## Forms, Inputs, Validation, Onboarding & Empty States

**Key Routing Questions**

- Are you building a flow where trust, completion rate, and first-user momentum matter more than ornamental cleverness?
- Are you building a long checkout, signup, or data-entry flow?
- Are you adding real-time validation?
- Are you designing an empty state or onboarding flow?

**Synthesis**  
The most lovable forms are the ones users barely feel. Reduce fields, accept multiple sensible input formats, validate at meaningful checkpoints, preserve work, and use native/browser autofill aggressively. Turn empty states into first-success states with one obvious action. Onboarding should be short, skippable, contextual, and tied to real value — not mandatory tutorials.

**Go to the dedicated content skill:** `forms-inputs-validation.skill.md`

**Further reading & authoritative sources**  
- Stripe Checkout and Elements documentation
- GOV.UK Design System validation patterns
- Baymard checkout research
- web.dev payment/address and passkey guidance
- NN/g onboarding research

---

## Microinteractions, Feedback, Loading States, Skeletons & Transitions

**Key Routing Questions**

- Are you building the layer of "aliveness" that turns competent UI into something users enjoy touching?
- Are you managing asynchronous data fetches and route transitions?
- How do you prevent jarring visual flashes when data loads too quickly?
- Are you adding motion or microinteractions to create a "lovable" interface?

**Synthesis**  
Use microinteractions to answer user questions instantly: "Did it register?", "What changed?", "Where did that go?". Prefer skeletons when layout is known, determinate progress when time can be estimated, and local spinners for short indeterminate actions. Keep motion brief, context-reinforcing, and strictly on compositor-friendly properties. Replace nonessential motion when the user requests reduced motion or the page is already heavy.

**Go to the dedicated content skill:** `microinteractions-loading-transitions.skill.md`

**Further reading & authoritative sources**  
- Apple HIG motion guidance
- Shopify Polaris loading components
- Ele.me skeleton screen case study
- React Suspense + Next.js `loading.js`
- NN/g on microinteractions and distracting animation

---

## High-End Visual Experiences (3D, WebGL, Three.js, Canvas, Video & Images)

**Key Routing Questions**

- Are you building a hero, product demo, visualizer, 3D experience, or motion-heavy surface that must feel premium without wrecking runtime performance?
- Are you reaching for 3D, WebGL, or a heavy canvas?
- Are you building a product configurator?
- Are you integrating video, image sequences, or high-fidelity media?

**Synthesis**  
Use CSS, SVG, Motion, and View Transitions for most UI state changes and "premium feel" work. Reach for Canvas when you need many simple moving marks. Use WebGL/Three.js only when real 3D perspective, lighting, or immersive storytelling is central to understanding the product. When you do, progressively enhance: gate on capability signals, ship a poster or 2D fallback, cap DPR, reuse geometry/textures, and render on demand (`frameloop="demand"`). The decision ladder and asset pipeline matter more than the rendering engine.

**Go to the dedicated content skill:** `high-end-visuals-3d-webgl.skill.md`

**Further reading & authoritative sources**  
- React Three Fiber performance docs (`frameloop="demand"`, instancing, LOD)
- Stripe globe engineering case study
- Vercel Ship hero and WebGL experience write-ups
- Three.js manual and best practices
- web.dev high-performance CSS animations and media guidance

---

## Theming, Personalization, Dark Mode & Brand Expression

**Key Routing Questions**

- Are you designing a brand-expressive interface that also needs cross-cutting architectural rules for staying fast as the product grows?
- Are you implementing light/dark mode?
- Do you want motion to feel "branded"?
- Are users expecting heavy personalization (custom accents, covers, avatars)?

**Synthesis**  
Coherent theming creates emotional ownership. Build on semantic tokens and CSS variables so theme changes are instant and cheap. Eliminate FOUC with a blocking script in `<head>` that reads preference and applies the class before hydration. Treat personalized assets as performance assets (optimize, lazy-load, reserve space). Keep heavy effects gated behind capability detection.

**Go to the dedicated content skill:** `theming-personalization.skill.md`

**Further reading & authoritative sources**  
- Stripe accessible color system work
- MDN `prefers-color-scheme`, `light-dark()`, forced-colors guidance
- next-themes and Radix Themes documentation
- Tailwind dark mode and CSS variables patterns
- Apple HIG materials and dark mode guidance

---

## Performance Architecture Patterns for Beautiful Interfaces

**Key Routing Questions**

- Are you trying to make a slow app *feel* fast?
- Are you shipping native-like transitions on mobile web?
- How do you architect a frontend that feels instantly responsive at massive scale?
- How do you eliminate rendering bottlenecks, waterfalls, and main-thread blocking?

**Synthesis**  
True performance architecture treats network latency as a product defect. Use local-first patterns: hydrate from IndexedDB into observable state, apply optimistic updates immediately, and treat the server as background confirmation. On the rendering layer, use Server Components, streaming, selective hydration, and islands. Keep animation on compositor-friendly properties. Measure real-user CWV + conversion, not just Lighthouse scores. Capability detection and reduced-motion support are non-negotiable.

**Go to the dedicated content skill:** `performance-architecture.skill.md`

**Further reading & authoritative sources**  
- Linear Sync Engine engineering notes
- web.dev rendering performance, INP, CLS, and content-visibility guides
- Next.js Server Components + streaming patterns
- Vercel Fluid Compute and edge rendering benchmarks
- Patterns.dev rendering and performance patterns

---

## Final Principle

Lovable frontends are built on a paradox: they feel effortless because the team was ruthless about what to remove, optimize, and contain. The best agents treat every visual decision as a performance decision and every performance decision as a user-experience decision.

**When in doubt:** reduce motion, reduce spacing variety, reduce the number of layout systems in play, and render less by default. Then add back only what genuinely increases emotional pull or clarity while staying inside the frame budget.