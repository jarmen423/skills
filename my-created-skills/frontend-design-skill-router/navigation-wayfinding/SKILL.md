# Navigation, Wayfinding & Information Architecture

> Dedicated content skill for building navigation systems that feel lightweight, predictable, and fast while scaling to complex products.

**Core Mandate**  
Great navigation is invisible architecture made visible. It reduces hunting, maintains user orientation, and makes movement between contexts feel instant. Performance is not separate from IA — slow navigation (full reloads, layout thrashing, repeated network requests) is experienced by the user as friction even if the labels are perfect.

## When to Use This Skill

Use this skill when an agent is:
- Designing or refactoring global navigation, sidebars, command palettes, or tab systems
- Building dense productivity tools where users constantly move between lists, items, and views
- Implementing keyboard-first or command-driven navigation
- Dealing with deep hierarchical content (files, pages, layers, databases)
- Trying to make route transitions feel instant instead of janky

## Core Principles

1. **Recognition over recall.** Make destinations visible or instantly searchable rather than buried in nested menus.
2. **Speed is part of the information architecture.** Prefetching, optimistic updates, client-side caching, and compositor-only transitions are IA decisions.
3. **Progressive disclosure + recency bias.** Show the most relevant destinations first. Command palettes and recent items dramatically reduce cognitive load.
4. **Preserve context.** Good navigation doesn't erase where the user came from. Maintain scroll position, selection state, and soft route descriptors.
5. **Limit depth and choices.** Hick’s Law and Fitts’s Law still apply. Deep nesting and too many top-level items destroy both delight and performance.

## Key Patterns & Techniques

### 1. Command Palette as Primary Navigation Layer
For power users and dense products, a global `⌘K` / `Ctrl+K` command palette (built on primitives like cmdk) often becomes the real navigation surface.

- Search local state first (MobX/Redux/Zustand or derived state) so results appear in <100 ms
- Lazy-load the palette chunk itself
- Bias toward recency and frequency
- Support fuzzy search and direct actions, not just destinations

**Linear & Vercel pattern:** The palette searches an in-memory local data store. Navigation and actions feel instantaneous because there is zero network latency on read.

### 2. Persistent, Collapsible Sidebar + Smart Prefetching
For desktop-heavy SaaS:
- 240–280 px expanded, ~64–72 px collapsed icon-only
- Use `position: sticky` or fixed with proper z-indexing
- Prefetch likely next routes on hover (`next/link` prefetch or service worker)
- Virtualize any long nested trees

**Vercel Dashboard pattern:** Resizable sidebar + floating bottom bar on mobile + universal command menu. Aggressive prefetching and memoization delivered major FMP and Lighthouse wins.

### 3. Bottom Tab Bar for Mobile
For apps with 3–5 primary destinations:
- Place targets in the thumb zone (Fitts’s Law)
- Limit to 3–5 tabs (Hick’s Law)
- Animate only `transform`/`opacity` for active indicators
- Use shared layout animations (`layoutId` in Framer Motion) scoped properly so measurement cost stays bounded

### 4. Virtualization + Derived State for Deep Hierarchies
Deep trees (Figma layers, Notion sidebar, file explorers) must be virtualized.

- Only render visible rows + small overscan
- Compute names/icons/selection state only for visible nodes (two-pass rendering)
- Use derived/cached state so expanding one node doesn't re-render the entire tree

**Figma Layers Panel:** Rebuilt with windowing + derived state → 30–50% faster interactions in large files.

### 5. Optimistic + Context-Preserving Transitions
- Use soft route descriptors instead of bare `href`s (Stripe pattern) so context (test/live mode, active account) survives navigation
- Animate route changes with `transform`/`opacity` only
- Preserve scroll position when going back
- Show skeleton or optimistic state immediately

### 6. Service Worker + Client-Side Caching for Repeated Navigation
GitHub Issues and similar tools use client-side caching + preheating + service worker so repeated list ↔ detail navigation feels near-instant.

## Production Examples (Delight + Performance)

**Linear Command Palette + Optimistic UI**  
Delight: Keyboard-first workflow that feels like a native OS. Creating issues, changing status, and navigating feels instantaneous.  
Performance: Data hydrated into local MobX store from IndexedDB. Zero network on search/filter. Every package code-split and cacheable. Transitions on `transform`/`opacity` under 100 ms.

**Vercel Dashboard Navigation**  
Delight: Clean sidebar + command menu that makes jumping between projects and deployments feel effortless.  
Performance: Aggressive route prefetching, SWR/memoization, and Geist command menu. One redesign improved First Meaningful Paint by >1.2 s and Lighthouse from 51 to 94.

**Figma Layers Panel**  
Delight: Managing tens of thousands of layers without the UI ever feeling heavy.  
Performance: Custom two-pass virtualization + derived state. Only visible rows compute properties. Massive win in large files.

**Arc Browser Sidebar + Command Bar**  
Delight: Spatial model (Favorites, Pinned, Spaces) that replaces tab chaos with calm order.  
Performance: Suspends inactive tabs after 5 minutes. Only recently used pinned tabs stay active. Transitions use hardware-accelerated compositor layers.

**Notion Sidebar Tree + Quick Find**  
Delight: Infinitely nestable workspace that still feels personal and navigable.  
Performance: Lazy-loaded page previews, collapsed branches, and Quick Find (`Ctrl/Cmd+P`) that bypasses the tree entirely.

**GitHub Issues + Projects**  
Delight: Fast movement between list and detail with preserved context.  
Performance: Client-side caching + preheating + service worker. Repeated navigation avoids full network round-trips.

**Raycast Command Palette**  
Delight: Extreme speed — everything reachable in a few keystrokes with rich metadata.  
Performance: Native system APIs, lazy-loaded extensions, debounced search, and very lightweight UI so results render in a single frame.

**Apple iOS/iPadOS Tab Bars & Adaptive Sidebars**  
Delight: Predictable, thumb-reachable navigation that adapts gracefully from iPhone to iPad.  
Performance: Platform-native compositing. The system handles transitions and layer promotion.

## Anti-Patterns to Avoid

- Deep nested menus that force recall instead of recognition
- Navigation drawers or full-screen reveals that erase context
- Animating `left`, `top`, `width`, or `height` on route or panel transitions (causes layout thrashing)
- Command palettes that do synchronous server filtering on every keystroke
- Rendering entire deep trees without virtualization
- Full-page reloads on every navigation in a single-page app
- Parallax or heavy 3D navigation chrome that competes with actual content

## Further Reading & Authoritative Sources

- Linear performance engineering notes and "How is Linear so fast?"
- GitHub Issues navigation performance write-up
- Figma Blog — "Improving Performance in the Layers Panel" and incremental loading
- Vercel Blog — Dashboard redesign and command menu
- cmdk repository (fast command palette primitives)
- web.dev — View Transitions API, transform-based movement, and INP guidance
- Apple Human Interface Guidelines — Tab bars, sidebars, and navigation
- Nielsen Norman Group — Hamburger menus and hidden navigation research
- Laws of UX — Hick’s Law, Fitts’s Law, recognition vs recall

This skill contains the patterns used by Linear, Vercel, Figma, Arc, Notion, GitHub, and Raycast to make navigation feel both delightful and fast. Use it whenever movement between contexts is a core part of the product experience.