---
name: devtool-visual-system
description: How an interface looks in the Linear/Vercel devtool style, measured from their production CSS. Covers dark themes as an OKLCH lightness ladder, low-contrast borders, text tiers, a rationed accent, typography (Inter/Geist, tracking, weights, two-tone headings), elevation without shadows, restrained glow and masks, buttons, headers and landing-page anatomy with the product as the hero, plus a script that generates and contrast-checks palettes. Use when setting up or changing tokens, colors, themes, type or surfaces, when asked for something like Linear or Vercel, or when a UI looks cheap, flat, muddy or generic.
---

# Devtool visual system

The Linear/Vercel look is mostly **restraint made precise**: near-black surfaces separated by 2–3% lightness steps, hairline borders you feel more than see, text in four deliberate tiers, one accent color used rarely, type that's tight and confident rather than loud, and the product itself as the hero image. Linear's 2026 refresh named the two principles: **"Don't compete for attention you haven't earned"** and **"Structure should be felt not seen."**

Paco Coursey (Linear): "Poor design manifests as slowness… What we call a delightful user experience is just delivering a faster path to user goals." The aesthetic serves speed and focus. When a decoration doesn't help someone scan or decide, remove it.

## 1. Color: build a ladder, don't pick swatches

Linear replaced 98 hand-set theme variables with three inputs, **base color, accent color and contrast**, derived in a perceptual color space (LCH). Equal lightness numbers then *look* equally light, so the ladder stays even. Do the same thing in OKLCH:

| Role | Dark value (Linear 2026, measured) | OKLCH L | Rule |
|---|---|---|---|
| Page canvas | `#08090a` | 13.9% | Near-black, never `#000`. Chroma ≤ 0.005 with a faint cool (or, per 2026, slightly warm) hue |
| Deep hero canvas | `#010102` | ~7% | Marketing heroes only |
| Panel / level 1 | `#0f1011` | 17.2% | Each elevation step is **+2–3 L** |
| Level 2 / raised | `#141516` | 19.5% | Popovers, menus |
| Level 3 / overlay | `#191a1b` | 21.7% | Dialogs |
| Hover → active fill | `#1c1c1f` → `#232326` → `#28282c` | 22.8 → 27.8% | Same ladder, continued |
| Border | `#23252a`, or white at 5% / 8% | ~26% | **≈1.3:1 against the page.** Felt, not seen |
| Text primary | `#f7f8f8` | 97.8% | 18.7:1. Not pure white |
| Text secondary | `#d0d6e0` | 87.4% | 13.6:1, slightly cool-tinted |
| Text tertiary | `#8a8f98` | 64.9% | 6.1:1, APCA Lc 42. Short supporting lines at ≥15px, not long paragraphs |
| Text quaternary | `#62666d` | 50.9% | 3.5:1, Lc 23. **Disabled and decorative only.** It's below APCA's Lc 30 floor for any text people need to read |
| Accent | `#7170ff` (brand `#5e6ad2`) | 62% | Primary action, selection, focus, links. Nothing else |

Rules:
- **Elevation is lightness, not shadow.** On dark UIs, shadows barely read. Raise a surface by stepping it up the ladder, and optionally add a 1px top highlight (`inset 0 1px 0 rgb(255 255 255 / 0.04)`) and a dark outer ring (`0 0 0 1px rgb(0 0 0 / 0.6)`).
- **Chrome recedes.** Sidebars and navigation sit a notch *dimmer* than the content area. Use fewer and smaller icons, with no colored icon backgrounds.
- **Keep neutrals nearly achromatic.** Limit how much of the accent's hue bleeds into the grays; that's how Linear's 2024 redesign got its "neutral and timeless appearance". Linear's 2026 grays moved "warmer… crisp, but less saturated". Too warm looks muddy.
- **Mix in a perceptual space:** `color-mix(in oklch, var(--accent) 36%, transparent)` for selection and tints.
- **Ration the accent.** "If every element made repetitive use of a strong accent color, the color would no longer feel as significant" (Rauno, Vercel homepage). The main CTA on dark is usually an *inverted* light pill, not the accent.
- **Prototype in black and white opacities first** (Karri Saarinen's method), then convert to tokens.
- Set `color-scheme: dark` and theme the scrollbar (6px, 10% white thumb, 20% on hover).

**Use the script** rather than eyeballing contrast:
```bash
# derive a full ladder from two colors (30 = standard contrast, 100 = high-contrast theme)  (<this-skill-dir> = the base directory this skill was loaded from)
python3 <this-skill-dir>/scripts/theme.py generate --base '#08090a' --accent '#7170ff' --format tailwind
# check any set of colors against a background (WCAG 2 + APCA, with a usage verdict)
python3 <this-skill-dir>/scripts/theme.py check --bg '#08090a' '#8a8f98' '#62666d' '#ffffff14'
```
Prefer APCA's verdict for dark UIs. WCAG 2 overstates the contrast of mid-gray text on black: Linear's tertiary passes WCAG AA at 6.1:1, but APCA rates it Lc 42, which is supporting text rather than body copy. Linear knowingly runs its lower tiers light. When readability matters more than matching Linear, take the script's verdict: roughly Lc 60+ for paragraphs, 45+ for large text and labels, and 30+ for placeholders and meta.

## 2. Surfaces, borders, radii
- **Borders:** 1px, either the solid border token or translucent white (`rgb(255 255 255 / 0.05–0.08)`; 0.12 only for emphasis). Geist draws them as shadow rings (`box-shadow: 0 0 0 1px`), which layer cleanly with other shadows and never shift layout.
- **Remove separators that don't earn their place.** If every section has a border, none of them separate anything. Use spacing and a heading first.
- **Card recipe (dark):**
  ```css
  .card {
    border-radius: 12px;
    background: linear-gradient(rgb(255 255 255 / 0.03), rgb(255 255 255 / 0.03)), var(--bg-panel); /* 3% lift */
    box-shadow: inset 0 0 0 1px rgb(255 255 255 / 0.06), inset 0 1px 0 rgb(255 255 255 / 0.04);
  }
  ```
  For a raised floating element on dark, add `0 0 0 1px rgb(0 0 0 / 0.6), 0 4px 24px rgb(0 0 0 / 0.2)`. In light mode, shadows do work: use layered, tiny-alpha stacks (`0 1px 1px #00000005, 0 4px 8px -4px #0000000a, 0 16px 24px -8px #0000000f`) with negative spread.
- **Radii:** 6px for controls, 8px for small cards, 12px for menus, dialogs and cards, 16px+ for large marketing surfaces, pills for primary marketing buttons. Nested radii are concentric: inner = outer − padding.
- **Specular edge highlight** (Linear's signature detail): a duplicate 1px border masked by a radial ellipse, so only one corner catches light. See `references/tokens.md`.

## 3. Typography
- **Family:** Inter Variable (v4) with `font-feature-settings: "cv01", "ss03"`, or Geist Sans. Inter 4 has an optical-size axis, and `font-optical-sizing: auto` (the browser default) applies it from the font size, so large headings get the Inter Display cut with no second family. Linear's CSS also declares `font-variation-settings: "opsz" auto`, which is invalid CSS that browsers ignore, so don't copy it. Pin `"opsz" 32` only if you need a fixed cut. A mono (Geist Mono, Berkeley Mono, SF Mono) for code, IDs and keyboard hints; add `"zero"` for slashed zeros in IDs.
- **Weights:** 400 body, **510 for headings** (Linear's "confident, not loud"), 590 for emphasis and titles, 680 at most. Geist uses 600 for headings. Avoid 700+ on display type, and never go below 400 in UI.
- **Tracking tightens with size:**

  | Size | Letter-spacing | Line-height |
  |---|---|---|
  | ≥ 40px display | −0.022em (Linear) to −0.06em (Geist's tighter headings) | 1.0–1.1 |
  | 24–32px | −0.012em to −0.04em | 1.125–1.33 |
  | 17–20px | −0.012em | 1.33–1.4 |
  | 13–15px UI and body | −0.01em to 0 | 1.5–1.6 |
  | 12px and uppercase labels | 0 to +0.02em (loosen uppercase) | 1.4 |

- **Sizes:** body 15px on marketing and 13–14px in dense product UI. Heading steps 17 / 20 / 24 / 32 / 40 / 48 / 56 / 64 / 72, stepping down by token at breakpoints (hero 64 → 56 → 40, and about 38px on phones).
- **Hierarchy through lightness, not size.** The two-tone heading: `<h2 class="text-tertiary"><strong class="text-primary font-[510]">A new species of product tool.</strong> Purpose-built for modern teams…</h2>`. Vercel and Linear both use this lockup.
- **Measure and wrap:** cap headings in `ch` (16–18ch), use `text-wrap: balance` on headings and `pretty` on paragraphs. Use `text-box: trim-both cap alphabetic` for optical alignment where supported. Nudge big display type left by 1–2px so its side bearing lines up with body text.
- **Numbers:** `tabular-nums` wherever values change or align.
- **Gradient text** only as a whisper (white → ~70% white, top to bottom), never rainbow. Check contrast at the darkest stop, set a solid fallback `color`, and unset it in `::selection`.

## 4. Light, gradients, glow (use almost none)
Linear's live site has 227 mask usages, and most of its "gradients" are **alpha masks fading content at the edges**, not color.
- **Masks first:** fade screenshots, marquees, code blocks and grids into the surface (`mask-image: linear-gradient(to bottom, #000 60%, transparent)`) instead of hard-cropping them.
- **Glows are 3–8% white**, built from eased multi-stop radial gradients so no ring or band shows. Colored glows, when used, sit at ≤0.15 alpha and come from the brand hue.
- **Surface gradients should be almost invisible.** Linear's command-menu panel goes from `rgb(39,40,43)` to `rgb(45,46,49)` at 136.61°, about 6 RGB units.
- **Large dark gradients band.** Add static grain (opacity 0.05–0.1) or dither.
- **Dated tells to avoid:** saturated purple radial blobs, rainbow gradient headlines, glassmorphism everywhere, and neon borders on every card. That's the 2021–23 "Linear clone" look, which Linear itself has moved past.
- For signature effects (spotlights, beams, lamps, border glows), use the `signature-effects` skill and its one-effect-per-viewport budget.

## 5. Components that set the tone
- **Buttons (marketing, dark):** pill radius, weight 510, heights 32 / 40 / 44px.
  - *Primary*: an inverted light pill (`#e5e5e6` → `#fff` on hover, text in the canvas color).
  - *Secondary*: dark glass (`rgb(255 255 255 / 0.05)` with `backdrop-filter: blur(4px)` and `box-shadow: inset 0 0 0 1px #ffffff08, inset 0 1px #ffffff0a, 0 0 0 1px #0009, 0 4px 4px #0000001a`).
  - *Brand*: the accent fill with `filter: brightness(1.15)` on hover.
  - All of them press to `scale(.97)` over ~160ms.
- **Header:** transparent at the top. After scroll it becomes `rgb(11 11 11 / 0.8)` with `backdrop-filter: blur(20px)` and a `1px rgb(255 255 255 / 0.08)` bottom hairline. Compensate for scrollbar removal when modals lock scroll (`scrollbar-gutter: stable`).
- **Hover highlights appear instantly and fade out over ~150ms.** In lists and menus, the hover has no fade-in.
- **Logos:** monochrome (`filter: grayscale(1) brightness(4)` on dark) at ~50–60% opacity.
- **Keyboard hints:** `<kbd>` at 18–20px square, 4–5px radius, mono or 0.8em, in a tertiary color, right-aligned in rows.

## 6. Marketing page anatomy
Read `references/marketing-anatomy.md` before building or restyling a landing page. The short version:
- **Hero:** a short, concrete headline (≤ ~8 words), a one-line subhead, one primary and one secondary CTA, an optional "New · Feature →" pill, then **the product UI, built in HTML or a crisp crop, as the hero image**. Not an illustration, and not a stock gradient.
- **One idea per section,** in a single vertical flow. No zig-zag. Big gaps (128–256px) between acts.
- **Feature sections** use a bento (`bento-grids` skill) or alternating product crops with two-tone headings.
- **Proof** (logos, a stat, a quote) comes early and stays quiet.
- **"Dirty the frame":** depth comes from blurred background layers, bottom-edge fades and offset duplicate frames that reinforce the message, not from decorations.

## 7. Anti-patterns
- Pure `#000` canvas with pure `#fff` body text: too harsh, and it breaks the elevation ladder.
- Hand-picked hex values that drift (five nearly identical grays). Derive them instead.
- Borders, separators and icons on everything. Chrome as bright as the content.
- Heading weight 700–800 with default tracking on a 64px headline.
- Using the accent for decoration, or more than one saturated color per viewport.
- Body copy in the quaternary tier, or mid-gray gradient text under 4.5:1.
- `* { transition: all }` to smooth theme switches.
- A hero with an abstract blob instead of the product.

## References
- `references/tokens.md`: full measured token sets for Linear (dark and light, type scale, radii, z-layers, motion, buttons, shadows, edge highlight) and Vercel Geist (10-step color roles, type scale, materials, shadows, focus ring, spacing, control heights). Read it when you need exact values or want to match either system closely.
- `references/marketing-anatomy.md`: section-by-section anatomy of a devtool landing page (header, hero, product mock, logos, features, bento, CTA, footer) with concrete values from linear.app and the Vercel homepage write-ups.
- `scripts/theme.py`: palette generator and contrast checker (no dependencies).

## In this repo (agent-memory-labs-frontend)
The tokens already follow this system. Extend them rather than replacing them (`src/app/globals.css`, `@theme inline`):
- Canvas `#060708` (L 12.8%) and surfaces `#0b0c0e` / `#111214` / `#18191c`.
- Borders `--color-line` (white 8%) and `--color-line-strong` (14%).
- Text tiers, as measured by `theme.py check --bg '#060708'`:
  - `fg` `#f5f6f7`: 18.6:1, Lc −102.
  - `fg-muted` `#9a9ea6`: 7.5:1, Lc −50. Good for one- or two-line descriptions. For paragraphs people must read, APCA wants about Lc 60 (`#aeb2ba`).
  - `fg-subtle` `#6a6e76`: 3.9:1, Lc −26. Below APCA's Lc 30 text floor, so use it for disabled or decorative text only. Readable meta text needs at least `#7a7e86` (Lc 34).
- Accents `accent` `#8fb3ff` and `time` `#f2b560`.
- Existing utilities: `.card`, `.spotlight`, `.text-sheen` (the whisper gradient), `.bg-grid`, `.glow-ambient`, `.hairline-x`, `.mask-fade-y`, `.kbd`, `.eyebrow`. The `SectionHeader` in `src/components/primitives.tsx` sets 34/44px headings at `tracking-[-0.035em]`.

Run `theme.py check --bg '#060708' …` on any new color before adding it.
