# Forms, Inputs, Validation, Onboarding & Empty States

> Dedicated content skill for building flows where trust, completion rate, and first-user momentum matter more than ornamental cleverness.

**Core Mandate**  
The most lovable forms are the ones users barely feel. Beauty in forms comes from confidence, pace, and legibility — not decoration layered on top of friction. Reduce cognitive load, validate at meaningful checkpoints, preserve user work, and use platform capabilities aggressively so the user types less, not more.

## When to Use This Skill

Use this skill when an agent is:
- Building checkout, signup, settings, or complex data-entry flows
- Designing validation, error handling, or empty states
- Creating onboarding experiences
- Optimizing form completion rates or reducing abandonment

## Core Principles

1. **Reduce fields and choices.** Every extra field increases abandonment. Use progressive disclosure — only show what is needed at that moment.
2. **Validate at meaningful checkpoints**, not on every keystroke. Blur or short debounce (150–250 ms) is usually the right trigger.
3. **Preserve work.** Never lose user input. Error states should keep the data they already entered.
4. **Use native and browser capabilities aggressively.** Autofill, inputmode, passkeys, and platform keyboards reduce friction more than custom UI ever will.
5. **Empty states are opportunities**, not dead ends. They should explain value and present one clear next action.
6. **Onboarding should be treated skeptically.** Most onboarding is disruptive and forgotten. Contextual, pull-based help usually beats mandatory tutorials.

## Key Patterns & Techniques

### 1. Progressive Disclosure in Forms
Break long forms into logical steps or conditional fields. Billing fields should only appear when payment is actually selected. Advanced options should be collapsed by default.

**Stripe Checkout pattern:** Fields appear only when relevant. Autocomplete is orchestrated through rich `autocomplete` attributes. The form feels short even when it collects a lot of information.

### 2. Validation Timing & Error Handling
- Use native HTML constraints (`required`, `type`, `pattern`, `minlength`) as the first line of defense.
- For richer rules, run validation on blur or short debounce, never on every keystroke.
- Show field-level errors next to the problem. Use an error summary at the top for screen readers and keyboard users (GOV.UK pattern).
- Preserve all entered data when showing errors. Move focus to the first error.

### 3. Leveraging Platform Capabilities
- Use correct `autocomplete`, `inputmode`, `enterkeyhint`, and `autocapitalize` values.
- On mobile, dynamic numeric keypads and card scanning dramatically reduce friction.
- Passkey autofill and platform biometric prompts remove typing entirely where possible.
- `contain: layout style paint` on field groups can help isolate expensive validation or formatting work.

### 4. Empty States as First-Success Moments
Treat blank screens as landing pages for the feature. Show a lightweight illustration (SVG or dotLottie), a clear headline naming the value, and one primary action. Use `content-visibility: auto` if the empty state is below the fold.

**Shopify empty state pattern:** Explains what will appear here and gives a clear, single next step. Much more effective than generic "No items yet" messages.

### 5. Onboarding Philosophy
Most users want to get value immediately, not sit through a tour. 
- Lead with a quick win instead of a feature walkthrough.
- Use contextual coaching that appears when the user actually reaches the relevant surface.
- Always provide a "Skip for now" escape.
- If onboarding is necessary, keep it short, skippable, and tied to real setup or first value.

Rive is increasingly used for state-driven, contextual guidance (Figma FigJam mobile, Duolingo) instead of heavy exported animations or full-screen carousels.

### 6. Optimistic & Local-First Form Behavior
For reversible or low-risk actions, apply changes locally first and treat server confirmation as background. This dramatically improves perceived speed and reduces the feeling of "waiting for the form."

## Production Examples (Delight + Performance)

**Stripe Checkout & Elements**  
Delight: Feels effortless. Autocomplete, real-time card validation, descriptive errors, one-click saved payment, and wallet support turn a potentially painful flow into something fast and trustworthy.  
Performance: iFrame isolation for cryptographic work. Field groups use containment. Animations are S-Tier CSS only. Validation and formatting are isolated so they don't block the main thread.

**GOV.UK Design System Validation**  
Delight: Clear, calm error handling that tells users exactly what went wrong and how to fix it without making them feel stupid.  
Performance: Error summary + field-level messages. Focus management. All entered data is preserved. No premature validation while typing.

**Shopify Empty States**  
Delight: Blank screens become helpful moments that explain value and give a clear path forward.  
Performance: Lightweight illustrations + single primary CTA. `content-visibility` when appropriate.

**Linear Create Issue / Command Palette Forms**  
Delight: Instantly summoned via keyboard, rich text input that never drops frames, templates via `/`.  
Performance: Optimistic submission to local state + IndexedDB. Virtualization for long select lists. CSS-only focus rings.

**Vercel Auth & Project Creation**  
Delight: Frictionless GitHub SSO and clean empty states that guide users to their first deploy.  
Performance: Edge redirects + middleware. Skeleton states that match final layout. No layout shift on auth completion.

**Notion Onboarding via Interactive Templates**  
Delight: Users learn by actually doing rather than watching a tutorial. Immediate value delivery.  
Performance: Async duplication of template databases in the background while the UI stays responsive.

**Arc Browser Conversational Onboarding**  
Delight: Short, personality-driven, one question per screen with large tap targets.  
Performance: Preloads the next view while the user reads the current one. Compositor-only slide transitions.

## Anti-Patterns to Avoid

- Placeholder-only labels (especially on mobile)
- Validation that fires on every keystroke or blur before the user is done
- Inputs that reject harmless formatting (forcing users to match your exact expectation)
- Cute empty states with no clear call to action
- Mandatory onboarding carousels or tutorials that front-load memory work instead of reducing it
- Losing user-entered data on validation errors or page transitions
- Animating the height or position of error messages (causes layout thrashing)
- Overly clever multi-step forms that feel longer than a single long form

## Further Reading & Authoritative Sources

- Stripe Checkout and Elements documentation + front-end experience engineering posts
- GOV.UK Design System validation and error summary patterns
- Baymard Institute checkout research
- web.dev payment/address forms and passkey guidance
- Nielsen Norman Group onboarding research
- Shopify Polaris empty state patterns
- Rive usage in Figma FigJam mobile and Duolingo for contextual guidance

This skill focuses on making forms and empty states feel confident and low-friction rather than decorated. The patterns here directly impact completion rates and user trust.