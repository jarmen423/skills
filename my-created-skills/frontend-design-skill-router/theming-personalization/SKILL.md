# Theming, Personalization, Dark Mode & Brand Expression

> Dedicated content skill for building coherent, brand-expressive interfaces that feel personal without sacrificing performance, accessibility, or maintainability.

**Core Mandate**  
Theming and personalization create emotional ownership. When done well, the interface feels like *their* space rather than generic software. This must be achieved with the smallest possible runtime cost (CSS variables, class toggles, minimal JS) and must never break accessibility, performance, or coherence across light/dark/high-contrast modes.

## When to Use This Skill

Use this skill when an agent is:
- Implementing light/dark mode or system preference syncing
- Building multi-brand or heavily customizable interfaces
- Designing token systems or design system theming
- Adding user-controlled personalization (accents, covers, avatars)
- Trying to eliminate FOUC (Flash of Unstyled Content) or theme flickering

## Core Principles

1. **Semantic tokens over raw values.** Use intent-based tokens (`bg-primary`, `text-muted`, `border-default`) mapped to brand primitives. This allows theme, state, density, and contrast changes without rewriting components.
2. **Eliminate FOUC at the source.** A blocking `<script>` in `<head>` that reads preference from `localStorage` or `matchMedia` and applies the class/data-attribute *before* the browser paints is non-negotiable for SSR apps.
3. **CSS variables are the runtime win.** Updating CSS custom properties at the `:root` or `<html>` level lets the browser's native engine repaint instantly with zero React re-renders or layout thrashing.
4. **Dark mode should be first-class**, not a bolted-on variant. Many modern products (Linear especially) design dark-first and derive light mode second to avoid washed-out grays.
5. **Personalization assets are performance assets.** User-uploaded covers, avatars, or accent colors must go through optimization pipelines and respect `content-visibility` / lazy loading.
6. **Accessibility is non-negotiable in theming.** Contrast ratios, forced-colors support, and high-contrast modes must be systemic, not manually fixed per screen.

## Key Patterns & Techniques

### 1. Blocking Script for FOUC Elimination (Critical)
```html
<script>
  (function() {
    const theme = localStorage.getItem('theme') || 
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    document.documentElement.classList.add(theme);
  })();
</script>
```
This must run synchronously in `<head>` before any body content or React hydration. Libraries like `next-themes` handle this safely.

### 2. CSS Variables + Semantic Tokens
Define a compact set of semantic tokens. Changing theme becomes a matter of swapping variable values or toggling a class on `<html>`.

**Linear pattern:** Dark-first palette with clean derivation of light mode. The entire surface is a flat layer of CSS variables + composited opacity transitions. No heavy backdrop blurs or shadow stacks in the core UI.

**Vercel + Geist + next-themes:** Tiny theme provider + blocking inline script. Zero JS runtime weight after hydration. Theme changes are instant.

### 3. System Preference + User Override
Default to `prefers-color-scheme`. Allow users to override and persist only the *intent* (`"dark" | "light" | "system"`), not derived state. This avoids hydration mismatches in SSR.

Use `prefers-color-scheme`, `color-scheme`, `light-dark()`, `forced-colors`, and `prefers-contrast` media features.

### 4. Branded Motion Grammar
If motion should feel "on-brand," define a consistent set of durations, easings, and entrance choreography tied to brand personality. Still keep everything on `transform`/`opacity` and compositor-friendly.

**Stripe pattern:** Recognizable easing family (short snappy ease-out entrances, elastic feedback on success). Driven through CSS custom properties updated via `requestAnimationFrame`.

### 5. User Personalization (Accents, Covers, Avatars)
- Sample user-provided colors server-side or in a worker to derive accessible palettes.
- Aggressively optimize uploaded images (WebP/AVIF, responsive `srcset`, blur-up placeholders).
- Apply accents via a small set of CSS variables so changes are cheap.
- Use `content-visibility` and lazy loading for cover images and avatar grids.

**Arc Browser:** Derives subtle accent from the active tab’s favicon/site color and applies it via CSS variables. Sampled in a Web Worker and cached per origin.

**Notion:** User-controlled accent + cover images feel personal while staying fast because the accent is one CSS variable and covers are aggressively optimized + lazy-loaded.

### 6. Separation of Concerns (UI Chrome vs Content)
In tools like Figma, keep UI chrome theming separate from canvas/document colors. Dark mode can repaint chrome layers while the canvas preserves document fidelity. Heavy color work happens on WebGL worker threads.

## Production Examples (Delight + Performance)

**Linear Dark-First Theming**  
Delight: Beautiful, community-driven custom themes that feel native and personal. Clean dark mode that avoids the usual washed-out grays.  
Performance: Entire UI is CSS variables + composited transitions. Theme changes are instant with zero component re-renders.

**Vercel + Geist + next-themes**  
Delight: Consistent, airy palette with subtle hover/active states. Theme switching feels instant and flicker-free.  
Performance: Blocking inline script eliminates FOUC. CSS variables + minimal JS. Theme changes have zero runtime cost after hydration.

**Stripe Dashboard & Appearance API**  
Delight: Unobtrusive, highly readable theming across payment surfaces that still carries brand character.  
Performance: Custom Appearance API powered by CSS variables. Strict WCAG contrast enforced systemically.

**Arc Browser Dynamic Accents**  
Delight: The browser chrome feels contextually alive based on the current site without being distracting.  
Performance: Dominant color sampled in Web Worker, cached per origin, applied as a small set of CSS variables.

**Notion User Personalization**  
Delight: Accent colors and cover images make shared workspaces feel personal and owned.  
Performance: Accent is a single CSS variable. Cover images are optimized and lazy-loaded. Page shell renders before assets arrive.

**Figma Dark Mode + Canvas Separation**  
Delight: Significantly reduces eye strain for long design sessions while preserving document colors.  
Performance: UI chrome tokens are separate from canvas tokens. Heavy color sampling happens on WebGL worker threads.

**GitHub Primer Theming**  
Delight: Coherent theming at massive scale with excellent high-contrast and colorblind support.  
Performance: Compact variable set. No runtime JS theme switching beyond class toggling. Complex contrast requirements handled through CSS cascading.

**Tailwind Dark Mode + CSS Variables**  
Delight: Instant theme toggling with clean utility classes.  
Performance: `class` strategy + CSS variable integration. Very low runtime cost.

## Anti-Patterns to Avoid

- Flash of Unstyled Content / theme flickering on initial load (especially in SSR apps)
- Storing derived theme state instead of user intent
- Using JavaScript-based theming libraries that force full component tree re-renders on theme change
- Hard-coding raw hex values instead of semantic tokens
- Low-contrast user-generated accents that break readability
- Heavy backdrop blurs or complex shadow stacks as permanent UI chrome (especially in dark mode)
- Treating dark mode as a simple inversion of a light-first system

## Further Reading & Authoritative Sources

- Refactoring UI (color, hierarchy, and theming heuristics)
- Google Material Design 3 Color System + dynamic color
- web.dev — Accessible color and contrast ratios
- MDN — `prefers-color-scheme`, `light-dark()`, `forced-colors`, `prefers-contrast`
- Radix UI Themes documentation
- Tailwind CSS dark mode docs
- next-themes documentation and FOUC prevention patterns
- Vercel — "Introducing Geist" design system writeup
- Linear engineering notes on dark-first UI
- Apple Human Interface Guidelines — Materials and Dark Mode
- Stripe Appearance API documentation

This skill covers the architectural patterns for coherent, performant, and accessible theming and personalization. The biggest wins usually come from semantic tokens + CSS variables + proper FOUC prevention.