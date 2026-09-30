# High-End Visual Experiences: 3D, WebGL, Three.js, Canvas, Video & Images

> Dedicated content skill for building premium visual surfaces (heroes, product configurators, data visualizers, cinematic marketing moments) while ruthlessly protecting runtime performance.

**Core Mandate**  
Visual impact and performance are not opposing forces. The best teams achieve both by treating visual richness as a progressive enhancement layered on top of a fast baseline, with strict frame budgets, capability detection, and asset discipline. This skill focuses on the real techniques used in production by teams that ship interfaces people emotionally respond to without tanking Core Web Vitals, INP, or battery life.

## When to Use This Skill

Use this skill when an agent is:
- Building marketing heroes, product pages, or landing experiences with rich motion or 3D
- Implementing product configurators, 3D viewers, or interactive visualizers
- Adding advanced video/image sequences, scroll-synced storytelling, or particle effects
- Evaluating whether to reach for Three.js / React Three Fiber vs Canvas vs pure CSS/SVG
- Optimizing an existing heavy visual surface that is causing jank, high INP, or poor mobile experience

## Core Principles

1. **Start cheap, enhance progressively.** Most "premium" feel can be achieved with CSS transforms, SVG, Framer Motion/GSAP, and View Transitions. Only reach for Canvas or WebGL when the effect genuinely cannot be done cheaper.
2. **Set explicit frame budgets before designing the effect.** 60 fps = ~16.7 ms per frame. Budget 8–10 ms for JavaScript; let the GPU handle the rest.
3. **Capability detection is non-negotiable.** Gate heavy experiences behind `prefers-reduced-motion`, `navigator.deviceMemory`, `hardwareConcurrency`, and network quality. Always ship a high-quality static or 2D fallback.
4. **Asset pipeline > rendering engine.** Draco compression, KTX2 textures, proper LOD, instancing, and geometry merging usually deliver bigger wins than swapping renderers.
5. **Render on demand, not continuously.** Use `frameloop="demand"` + manual invalidation in React Three Fiber. Never burn frames just because a canvas exists.
6. **The decision ladder matters more than the tech choice.** CSS/SVG → Canvas (many simple marks) → WebGL/Three.js (real 3D perspective, lighting, complex interaction).

## Decision Framework: When to Use What

| Technology       | Best For                                      | Performance Reality                          | When to Avoid |
|------------------|-----------------------------------------------|----------------------------------------------|-------------|
| **CSS + SVG + Motion** | Most UI microinteractions, hero reveals, scroll storytelling, shared-element transitions | Extremely cheap if limited to `transform`/`opacity` | When you need real 3D perspective or thousands of independent moving marks |
| **Canvas 2D**    | Many simple moving marks, particles, custom charts, image sequence scrubbing | Good when you control draw calls; bad if you fight the DOM | When you need lighting, shadows, or complex 3D math |
| **WebGL / Three.js / R3F** | Product configurators, 3D model viewers, immersive data viz, cinematic brand moments | Expensive by default. Wins only with strict discipline (instancing, LOD, on-demand rendering, asset compression) | Decorative heroes on marketing sites that can be done with CSS/SVG + video |

**Rule of thumb:** If the visual is primarily decorative or storytelling, prefer CSS/SVG/Motion + optimized video/image. If the visual is the core product interaction (configurator, 3D inspection, complex data manipulation), then WebGL becomes justifiable — but only with the full performance contract.

## Production Examples (Delight + Performance Analysis)

**Vercel Ship / basement.studio hero**  
Delight: Rich ferrofluid-inspired 3D particles + GLSL shader that feels premium and memorable.  
Performance: Layered progressive enhancement — SVG + CSS first, shader fades in asynchronously. Code-split, disabled on low-power devices via capability detection. Mobile gets reduced or no effect. This is the correct pattern for marketing heroes.

**Stripe interactive globe**  
Delight: High-tech, physically responsive 3D branding that reinforces sophistication.  
Performance: Hard 60 fps budget enforced before design. Antialiasing disabled (edges softened by textures), animation paused during scroll, scroll input debounced. Falls back to static image below threshold. Classic example of setting performance constraints first.

**Figma canvas + layers panel**  
Delight: Infinite zoom/pan canvas with thousands of objects that still feels instant.  
Performance: Custom WebGL renderer + aggressive incremental frame loading + virtualization in the layers panel (only compute visible rows). They treat the canvas like a game engine, not a web page.

**Apple product pages (scroll-synced sequences + WebGL reveals)**  
Delight: Cinematic "product comes alive" feeling through precisely timed image sequences and WebGL.  
Performance: Heavy pre-production asset optimization, short compressed videos triggered by Intersection Observer, `prefers-reduced-motion` fallback to static hero. Scroll handlers throttled and drive only `transform`/`opacity`.

**Linear release page starfield / 3D moments**  
Delight: Immersive, hype-building 3D that makes releases feel special.  
Performance: Code-split via React Suspense, careful `useFrame` discipline (no allocations inside render loop), `frameloop="demand"`.

**Polestar / BMW / Cartier / Nike configurators**  
Delight: Real ownership feeling through material swaps, lighting, and smooth interaction.  
Performance: Single GLB base mesh + named material slots + runtime swaps. Draco + KTX2 compression. PMREM IBL. DPR-aware rendering. Never reload the model on variant change.

**McLaren / Fender configurators**  
Delight: High-fidelity product visualization that drives conversion.  
Performance: Asset pipeline is the real work — decimate to <100k polygons, normal maps for detail, precise material zones, compressed textures. Rendering engine is secondary.

**Ray-Ban commerce pages**  
Delight: Visually rich e-commerce that still converts.  
Performance: Speculation Rules API prerendering + `next/image` responsive pipeline. Doubled conversion while reducing exit rate.

## Key Techniques & Patterns

### 1. Progressive Enhancement + Capability Detection (Most Important)
```tsx
const lowPower =
  window.matchMedia("(prefers-reduced-motion: reduce)").matches ||
  (navigator.deviceMemory ?? 8) <= 4 ||
  (navigator.hardwareConcurrency ?? 8) <= 4;

const Scene = dynamic(() => import("./HeroScene"), { ssr: false });

return lowPower 
  ? <HeroPosterImage /> 
  : <Scene frameloop="demand" dpr={[1, 1.5]} />;
```

### 2. React Three Fiber Production Discipline
- Use `frameloop="demand"` + `invalidate()` for static or lightly interactive scenes.
- Share geometries and materials. Use instancing (`<Instances>`) for repeated objects.
- Never allocate vectors/matrices inside `useFrame`.
- Implement LOD with `drei`'s `<Detailed>`.
- Cap `dpr` (especially on mobile).
- Manually call `.dispose()` on geometries/materials when unmounting.
- Keep draw calls under ~100 per frame for comfortable 60 fps.

### 3. Asset Pipeline (Often Bigger Wins Than Code)
- Geometry: Draco compression
- Textures: KTX2 + Basis (with fallback)
- Models: Proper decimation + normal maps instead of high-poly
- HDR/IBL: PMREMGenerator, precomputed
- Loading: Progressive + poster images

### 4. Motion & Interaction
- UI transitions around the 3D layer should stay on `transform`/`opacity`.
- For scroll-driven stories, prefer native CSS ScrollTimeline or throttled `requestAnimationFrame` over continuous listeners.
- For configurators, keep material/geometry swaps under 16 ms.

### 5. Mobile & Low-Power Reality
Mobile GPUs are memory-bandwidth constrained and thermally throttled. 
- Cap DPR at 1.5–2.0
- Disable post-processing and antialiasing on lower tiers
- Use `frameloop="demand"`
- Always provide excellent 2D/static fallback

## Anti-Patterns to Avoid

- Shipping WebGL to every user on first route without capability detection or fallback
- Autoplaying heavy background video on slow devices or as LCP element
- Layering DOM parallax or heavy CSS effects over an already expensive scene
- Using full-resolution textures everywhere
- Driving animation through React state updates every frame
- Allocating memory inside render loops
- Never calling `.dispose()` (leads to WebGL context lost crashes)
- Treating decorative heroes the same as core product configurators

## Further Reading & Authoritative Sources

**React Three Fiber / Three.js**
- React Three Fiber Scaling Performance docs
- "Why your React Three Fiber gallery drops to 5 FPS and how to fix it" (Alan West)
- Three.js Best Practices (100+ tips)
- drei and react-postprocessing documentation

**Real Production Case Studies**
- Stripe Engineering — "To design and develop an interactive globe"
- Vercel — "Building an interactive WebGL experience in Next.js"
- Rauno Freiberg — Vercel homepage craft writeup (layered CSS/SVG/shader approach)
- Figma Blog — Incremental frame loading and layers panel performance

**General Performance**
- web.dev — High-performance CSS animations, INP, media optimization
- Val Head — *Designing Interface Animation* (psychology + technical constraints)
- Apple WWDC sessions on Safari/WebKit animation and spatial web

**Asset & Pipeline**
- Draco + KTX2 compression guides
- glTF best practices for the web

This skill contains the highest-signal patterns from Linear, Vercel, Stripe, Figma, Apple, and multiple high-end configurator implementations. Use it as the primary reference when the visual layer is central to the experience.