# Microinteractions, Feedback, Loading States, Skeletons & Transitions

> Dedicated content skill for adding the layer of "aliveness" that turns competent interfaces into ones users enjoy touching — without destroying performance.

**Core Mandate**  
Motion and loading states should answer user questions instantly: "Did it register?", "What changed?", "Where did that go?", "Is this still working?". Delight comes from useful, predictable feedback first. Performance comes from keeping all motion on compositor-friendly properties and replacing heavy spinners with structure-preserving skeletons wherever possible.

## When to Use This Skill

Use this skill when an agent is:
- Adding microinteractions, hover states, button feedback, or status changes
- Designing loading states, skeletons, or empty/loading transitions
- Implementing route changes, page transitions, or shared-element animations
- Choosing between CSS, Framer Motion, GSAP, Rive, Lottie, or Canvas for motion
- Trying to improve perceived performance or reduce jank in interactive surfaces

## Core Principles

1. **Motion must be useful before it is beautiful.** Acknowledge, orient, confirm, or celebrate — don't just move things for the sake of movement.
2. **Keep everything on the compositor.** `transform`, `opacity`, and `filter` only. Never animate `width`, `height`, `top`, `left`, or `margin` in response to user input.
3. **Skeletons over spinners.** Skeletons preserve layout and reduce cognitive load. They make latency feel intentional rather than broken.
4. **Respect reduced motion and device capability.** Heavy or continuous animation should be gated or replaced with lighter alternatives.
5. **Perceived performance is real performance.** Instant local feedback + structure-preserving placeholders often matters more to users than raw request speed.
6. **Choose the right runtime for the job.** CSS for simple discrete states. Framer Motion/GSAP for physics, gestures, and complex sequencing. Rive or dotLottie for state-driven UI graphics that need to stay lightweight.

## Key Patterns & Techniques

### 1. Skeletons Instead of Spinners
Show a lightweight structural placeholder that mirrors the final layout as soon as possible. Only show a spinner for short indeterminate actions where the shape is unknown.

**Ele.me PWA pattern (still relevant):** Skeletons were actual SSR components so navigation responded immediately, then content filled in as data arrived. This is what strong SaaS apps do today.

**Shopify Polaris:** IndexTable skeletons replicate exact row height, column widths, and action buttons so merchants can scan the predicted layout before data arrives.

### 2. Optimistic UI + Local Feedback
Apply reversible or low-risk actions locally first. Show immediate visual confirmation (checkmarks, color changes, added rows) while the server sync happens in the background. This is one of the highest-leverage perceived performance techniques.

### 3. Compositor-Only Motion
All UI transitions and microinteractions should use only `transform` and `opacity`. Use FLIP technique (Framer Motion `layout` / `layoutId`, GSAP Flip) for layout changes so the browser does the interpolation on the GPU.

**Linear pattern:** Status changes and list reordering use spring physics via Framer Motion but stay strictly on transform/opacity. Exits are often slower than entrances for better perceived causality.

### 4. Choosing Animation Runtimes
- **CSS transitions/animations**: Best for simple, discrete state changes (hover, focus, toggle). Near-zero overhead and respects `prefers-reduced-motion` automatically.
- **Framer Motion / Motion**: Best for React-driven, physics-based, gesture-driven, or shared-element transitions. Uses WAAPI under the hood so it can still offload to the compositor.
- **Rive + dotLottie-web**: Excellent for state-driven UI graphics and complex micro-animations that need to stay lightweight across many instances. Newer WebGL/WebGPU backends help when many animations share a page.
- **Lottie**: Still useful but can be heavy if overused. Prefer lighter alternatives for list views or busy surfaces.

### 5. Route & View Transitions
- Use Next.js `loading.js` + React Suspense for streaming skeletons during navigation.
- For cross-document transitions, explore the View Transitions API.
- For intra-page shared-element transitions, use Framer Motion `layoutId` scoped inside `LayoutGroup` so measurement cost stays bounded.

### 6. Reduced Motion & Capability Handling
Respect `prefers-reduced-motion` at the system level. For heavy visual moments (marketing heroes, 3D), use the same capability detection patterns from the High-End Visuals skill (device memory, core count, reduced motion preference).

## Production Examples (Delight + Performance)

**Stripe Checkout Micro-animations**  
Delight: Even the smallest state changes feel polished and reassuring. Card validation, button loading states, and success feedback all feel intentional.  
Performance: Strictly S-Tier CSS properties. Animations are short and purposeful. Cryptographic work is isolated in iframes.

**Linear Transitions & Status Changes**  
Delight: Status changes and list updates feel physical and satisfying. Spring physics make interactions feel alive.  
Performance: Framer Motion tied to React state with interruptible springs. Everything stays on transform/opacity. Optimistic local updates before server round-trip.

**Vercel Skeletons + Optimistic Inputs**  
Delight: Creating a project or editing a setting shows an immediate skeleton that matches final layout. No layout shift.  
Performance: React 18 Transitions + `useOptimistic`. Shimmer effects implemented with `transform: translateX()` on pseudo-elements, not background-position.

**Shopify Polaris Loading Components**  
Delight: Skeletons that actually help merchants understand what is coming.  
Performance: Exact structural replication so users can scan before data arrives. No unnecessary shimmer on dense tables.

**Next.js App Router + Suspense**  
Delight: Route changes feel smooth because meaningful fallback UI appears instantly.  
Performance: Streaming HTML + selective hydration. The most important interactive regions hydrate first.

**Rive in Figma FigJam Mobile & Duolingo**  
Delight: State-driven, contextual micro-animations that feel alive without being heavy.  
Performance: Much lighter than legacy Lottie exports in many cases. Newer dotLottie-web WebGL/WebGPU backends help when many animations coexist.

**GitHub Reactions & Status Indicators**  
Delight: Playful, celebratory feedback that still feels lightweight.  
Performance: Declarative CSS `@keyframes` on pseudo-elements. Zero main-thread JavaScript after the initial trigger.

## Anti-Patterns to Avoid

- Full-page spinners between known app states
- Looping attention-grabbing motion that competes with the user's actual task
- Animating layout-triggering properties (`width`, `height`, `top`, `left`, `margin`)
- Multiple CPU-rasterized animation players (heavy Lottie) running inside scrollers or lists
- Showing skeletons for responses that resolve faster than ~150–200 ms (causes flicker)
- Continuous scroll listeners driving animation
- Ignoring `prefers-reduced-motion`
- Heavy particle or canvas effects as permanent UI chrome instead of short-lived moments

## Further Reading & Authoritative Sources

- Apple Human Interface Guidelines — Motion and Loading
- Shopify Polaris loading and skeleton components
- Ele.me PWA skeleton screen case study
- React Suspense + Next.js `loading.js` documentation
- Framer Motion / Motion docs — Layout animations, AnimatePresence, reduced motion
- GSAP performance and FLIP guidance
- Rive and dotLottie-web documentation
- NN/g on microinteractions and distracting animation
- Val Head — *Designing Interface Animation*

This skill focuses on making interfaces feel alive and responsive while protecting the frame budget and respecting user preferences. The patterns here are some of the highest-leverage ways to improve both emotional delight and perceived performance.