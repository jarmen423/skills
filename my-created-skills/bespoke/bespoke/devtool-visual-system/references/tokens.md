# Measured tokens: Linear and Vercel Geist

Values read from production CSS on 2026-09-25 (linear.app's 49 stylesheets, Vercel's Geist CSS) and from both teams' design posts. Use them to match either system closely, or as calibrated defaults.

## Contents
1. Linear: dark theme
2. Linear: light theme
3. Linear: typography
4. Linear: layout, radii, z-layers
5. Linear: motion
6. Linear: buttons, shadows, highlights
7. Linear: theme generation (LCH)
8. Geist: color roles and scales
9. Geist: typography
10. Geist: materials, shadows, focus, spacing

---

## 1. Linear: dark theme
```css
[data-theme=dark] {
  color-scheme: dark;
  --color-bg-marketing: #010102;   --color-bg-primary: #08090a;   --color-bg-panel: #0f1011;
  --color-bg-level-0: #08090a; --color-bg-level-1: #0f1011; --color-bg-level-2: #141516; --color-bg-level-3: #191a1b;
  --color-bg-secondary: #1c1c1f; --color-bg-tertiary: #232326; --color-bg-quaternary: #28282c;
  --color-bg-translucent: #ffffff0d;                                   /* 5% white */
  --color-border-primary: #23252a; --color-border-secondary: #34343a; --color-border-tertiary: #3e3e44;
  --color-border-translucent: #ffffff0d; --color-border-translucent-strong: #ffffff14;  /* 5% / 8% */
  --color-line-primary: #37393a; --color-line-secondary: #202122; --color-line-tertiary: #18191a;
  --color-text-primary: #f7f8f8; --color-text-secondary: #d0d6e0; --color-text-tertiary: #8a8f98; --color-text-quaternary: #62666d;
  --color-link-primary: #828fff; --color-link-hover: #fff;
  --color-brand-bg: #5e6ad2; --color-accent: #7170ff; --color-accent-hover: #828fff; --color-accent-tint: #18182f;
  --color-button-invert-bg: #e5e5e6; --color-button-invert-bg-hover: #fff;
  --color-selection-bg: color-mix(in lch, var(--color-brand-bg), black 10%);
  --color-overlay-primary: #000000d9;                                  /* 85% scrim */
  --header-bg: #0b0b0bcc; --header-border: #ffffff14;
  --shadow-low: 0px 2px 4px #0000001a; --shadow-medium: 0px 4px 24px #0003; --shadow-high: 0px 7px 32px #00000059;
  --icon-grayscale-image-filter: grayscale(100%) brightness(400%);
}
```
OKLCH ladder: page 13.9 → panel 17.2 → level-2 19.5 → level-3 21.7 → secondary 22.8 → tertiary 25.7 → quaternary 27.8. Chroma is 0.002–0.011. Borders sit at L≈26 (1.3:1). Text tiers are 97.8 / 87.4 / 64.9 / 50.9 L, which gives contrast 18.7 / 13.6 / 6.1 / 3.5:1. Shadows are `0 0 0 transparent` at the root and exist only where a theme opts in.

The legacy "glass" marketing theme (the 2021–23 look, still in the CSS) uses page `#000212`, surfaces and borders all as white alphas (`#ffffff08`, `#ffffff12`, `#ffffff26`), and text `#b4bcd0` with 60% and 40% alpha variants.

## 2. Linear: light theme
- Backgrounds `#fff` / `#f9f8f9` / `#f4f2f4` / `#eeedef` / `#e9e8ea`. Levels `#fff` `#f8f8f8` `#f4f4f4` `#f0f0f0`.
- Borders `#e9e8ea` / `#e4e2e4` / `#dcdbdd`, translucent `#0000000d` / `#00000014`.
- Text `#282a30` (14.3:1), `#3c4149` (10.3:1), `#6f6e77` (5.0:1), `#86848d` (3.7:1). Never pure black. Slight warm-violet hue (~308–326°).
- Shadows exist in light mode: tiny `0 1px 1px #00000017`, low `0 1px 4px -1px #00000017`, medium `0 3px 12px #00000017`, high `0 7px 24px #0000000f`.
- Focus ring 2px, offset 2px. Scrollbar thumb `#0000001a` → `#0003` → `#0000004d` (dark: `#ffffff1a` → `#fff3` → `#fff6`), 6px wide (10px when active).

## 3. Linear: typography
```css
--font-regular: "Inter Variable", "SF Pro Display", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-monospace: "Berkeley Mono", ui-monospace, "SF Mono", Menlo, monospace;
--font-serif-display: "Tiempos Headline", ui-serif, Georgia, serif;
font-feature-settings: "cv01", "ss03";      /* alternate 1, round quotes & commas */
font-optical-sizing: auto;                  /* default; Inter 4's opsz axis → Display cut at large sizes.
                                               (Linear also ships `font-variation-settings: "opsz" auto`, which is invalid and ignored) */
--font-weight-normal: 400; --font-weight-medium: 510; --font-weight-semibold: 590; --font-weight-bold: 680;
```
| Token | Size | Line-height | Tracking |
|---|---|---|---|
| title-9 | 72px | 1 | −0.022em |
| title-8 | 64px | 1.06 | −0.022em |
| title-7 | 56px | 1.1 | −0.022em |
| title-6 | 48px | 1 | −0.022em |
| title-5 | 40px | 1.1 | −0.022em |
| title-4 | 32px | 1.125 | −0.022em |
| title-3 | 24px | 1.33 | −0.012em |
| title-2 | 20px | 1.33 | −0.012em |
| title-1 | 17px | 1.4 | −0.012em |
| text-large | 17px | 1.6 | 0 |
| text-regular | 15px | 1.6 | −0.011em |
| text-small | 14px | 1.5 | −0.013em |
| text-mini | 13px | 1.5 | −0.01em |
| text-micro | 12px | 1.4 | 0 |

The homepage H1 is title-8 at weight 510 (line-height forced to 1), stepping to title-7 at ≤1024px and title-5 at ≤640px, or 38px with a 360px max-width on phones. Section h2s are capped at 16–18ch with `text-wrap: balance`. Underlines use `text-decoration-thickness: 1.5px; text-underline-offset: 2.5px` in the quaternary color.

## 4. Linear: layout, radii, z-layers
- Page max 1024px (homepage up to 1344px + 46px outer padding), prose 624px, inline padding 24px, block padding 64px, header 57–72px, header blur 20px, minimum tap size 44px.
- Grid: 12 → 8 (≤768px) → 4 (≤640px) columns, 32px gap. Areas are declared per breakpoint as CSS variables (see the `bento-grids` skill).
- Radii: 4, 6, 8, 12, 16, 24, 32, 9999px.
- Z-index: header 100 · overlay 500 · popover 600 · command menu 650 · dialog 700 · toasts 800 · tooltip 1100 · context menu 1200 · skip-nav 5000.
- Hero product mock: 1320×720, app radius 12px, frame padding 8px, sidebar 232px. Built in HTML/SVG with its own surface tokens (`#0f1011`, `#191d20`, borders `#2a2e33` / `#24282c` / `#191d21`).

## 5. Linear: motion
- `--speed-highlightFadeIn: 0s; --speed-highlightFadeOut: .15s`: hover is instant on, and fades out over 150ms.
- The default transition is `.16s cubic-bezier(.25,.46,.45,.94)` (ease-out-quad) on background, color, filter and transform. Quick is .1s and regular .25s.
- Dialogs scale in from .96 (+ fade) over .175s. There's also a `.15s` `dialogBounce` to `scale(.98)`, likely the "can't dismiss" feedback when you click outside a blocking dialog. Context menus scale from .9 over .1s, entering with ease-out and exiting with ease-in. Nav dropdowns scale from .98 over .18s. Drawers use `.5s cubic-bezier(.32,.72,0,1)`.
- Buttons press to `scale(.97)`, with `will-change: transform` only while active. Primary hover is `filter: brightness(115%)`.
- Hero: each title line starts at `opacity: 0; filter: blur(10px); transform: translateY(20%)` and reveals line by line. The line boxes carry `margin: -30px; padding: 30px` so the blur isn't clipped.
- Decorative motion and smooth scroll run only under `prefers-reduced-motion: no-preference`.
- Easing tokens: the full Penner set, e.g. `--ease-out-quint: cubic-bezier(.23,1,.32,1)`, `--ease-out-expo: cubic-bezier(.19,1,.22,1)`, `--ease-in-out-cubic: cubic-bezier(.645,.045,.355,1)`.

## 6. Linear: buttons, shadows, highlights
| Size | Height | Font | Padding | Icon |
|---|---|---|---|---|
| mini | 24 | 12 | 0 10 | 12 |
| small | 32 | 13 | 0 12 | 16 |
| medium | 40 | 13 | 0 14 | 16 |
| default | 40 | 15 | 0 16 | 18 |
| large | 44 | 16 | 0 20 | 18 |

Buttons are pill-shaped at weight 510.
- **Secondary (dark glass):** `background: #ffffff0d; backdrop-filter: blur(4px); box-shadow: inset 0 0 0 1px #ffffff08, inset 0 1px #ffffff0a, 0 0 0 1px #0009, 0 4px 4px #0000001a`. That's a 3% inner ring, a 4% top-edge highlight, a 60% black outer ring and a soft drop.
- **Invert (main CTA):** `#e5e5e6` → `#fff` on hover, with text in the canvas color.
- **Ghost:** tertiary text, `bg-quaternary` on hover.
- **Inline link-button:** `margin-left: -8px; padding-inline: 8px`, so the hit area is padded while the text stays aligned.

Common shadows on dark: `0 1px #0006` (a dark under-edge), `inset 0 0 0 1px var(--color-border-primary), 0 0 32px 0 #08090acc` (a panel sinking into the page). Focus is `0 0 0 2px var(--color-bg-primary), 0 0 0 4px var(--color-brand-bg)`.

**Edge highlight** (a specular light on part of a border):
```css
.edge-highlight { position: relative; }
.edge-highlight::after {
  content: ""; position: absolute; inset: -1px; pointer-events: none;   /* -1px: sit ON the host's 1px border */
  border: inherit; border-radius: inherit; border-color: var(--edge-highlight-color, #ffffff0f); /* 6%; 8–12% variants */
  mask: radial-gradient(ellipse var(--w, 17%) var(--h, 29%) at var(--x, 0) var(--y, 0), #000 0%, transparent 90%);
}
```
**Eased glow** (no visible ring): radial stops at 100% / 94% / 78% / 58% / 35% / 16% / 3% / 0 of a 3%-white tint, at positions 0 / 15 / 30 / 45 / 60 / 75 / 90 / 100%. Write them with `color-mix(in srgb, var(--tint) N%, transparent)`.

Dashed hairlines: `linear-gradient(to right, var(--line) 0 2px, transparent 2px 6px)` (2px dash, 4px gap).

## 7. Linear: theme generation (LCH)
- Every theme is `{ base: [L, C, H, a], accent: [L, C, H, a], contrast: 30 }`, with an optional separate sidebar base that is slightly darker (L 11.9 → 8.7 in one theme). Contrast 30 is standard and 100 is high contrast.
- "LCH… a red and a yellow color with lightness 50 will appear roughly equally light."
- "Limiting how much chrome (blue in our case) was used in the calculations" keeps the neutrals timeless.
- The 2026 color tool exposes hue, chroma and lightness sliders per token in a dev toolbar, and exports JSON to Figma.
- `scripts/theme.py generate` reproduces the measured dark ladder from base + accent at contrast 30.

## 8. Geist: color roles and scales
Ten 10-step scales (gray, gray-alpha, blue, red, amber, green, teal, purple, pink) with fixed roles per step:

| Steps | Role |
|---|---|
| 100 / 200 / 300 | Component backgrounds: default / hover / active (badges use 200–300) |
| 400 / 500 / 600 | Borders: default / hover / active |
| 700 / 800 | High-contrast fills (solid buttons, badges): default / hover |
| 900 / 1000 | Text and icons: secondary / primary |

Backgrounds: `bg-100` (the default, especially under color) and `bg-200` (a subtle secondary; use sparingly). Dark `#000`/`#0a0a0a`, light `#fff`/`#fafafa`.

| Scale | Theme | 100 → 1000 |
|---|---|---|
| gray | dark | #1a1a1a #1f1f1f #292929 #2e2e2e #454545 #878787 #8f8f8f #7d7d7d #a0a0a0 #ededed |
| gray-alpha | dark | #ffffff12 #ffffff17 #ffffff21 #ffffff24 #ffffff3d #ffffff82 #ffffff8a #ffffff78 #ffffff9c #ffffffeb |
| gray | light | #f2f2f2 #ebebeb #e6e6e6 #eaeaea #c9c9c9 #a8a8a8 #8f8f8f #7d7d7d #4d4d4d #171717 |
| blue | dark | #06193a #022248 #002f62 #003771 #004287 #0090ff #0071f6 #005fd8 #50a8ff #ebf6ff |
| red | dark | #330a11 #440d13 #5d0e17 #6f101b #88151f #f32e40 #f13242 #e2162a #ff5e63 #ffeaed |
| amber | dark | #291800 #331b00 #4f2900 #573200 #6c4100 #e99c00 #ffb200 #ff9900 #ff9900 #fff3d9 |
| green | dark | #00250a #003110 #003814 #004616 #00661d #009431 #00ab3e #009335 #00ca52 #daffe5 |

On P3 displays Geist swaps in `oklch()` values (e.g. blue-700 `oklch(57.61% .2321 258.23)`). Focus color is blue-700 (light) / blue-900 (dark). Selection is inverted (gray-1000 background, gray-100 text).

## 9. Geist: typography
Geist Sans and Geist Mono, at weights 400 / 500 / 600 (550 for strong in body copy).

| Class | Size / LH | Tracking | Weight |
|---|---|---|---|
| heading-72 / 64 / 56 | 72/72, 64/64, 56/56 | −0.06em | 600 |
| heading-48 / 40 | 48/56, 40/48 | −0.06em | 600 |
| heading-32 / 24 | 32/40, 24/32 | −0.04em | 600 |
| heading-20 / 16 / 14 | 20/26, 16/24, 14/20 | −0.02em | 600 |
| button-16 / 14 / 12 | 16/20, 14/20, 12/16 | 0 | 500 |
| label-14 (most common UI text) | 14/20 | 0 | 400 |
| label-13 (secondary line, tabular for numbers) | 13/16 | 0 | 400 |
| copy-16 (modals) / copy-14 (default) / copy-13 (dense) | 16/24, 14/20, 13/18 | 0 | 400 |
| copy-20 / 24 (marketing hero) | 20/36, 24/36 | 0 | 400 |

Heading `<strong>` = "Subtle" (500 + gray-900). Body `<strong>` = 550 + gray-1000.

## 10. Geist: materials, shadows, focus, spacing
| Material | Radius | Use |
|---|---|---|
| base / small | 6px | Everyday surfaces, slightly raised |
| medium / large | 12px | Further raised |
| tooltip | 6px | The only floating element with a stem |
| menu / modal | 12px | Lift from the page |
| fullscreen | 16px | Biggest lift |

"Favor the lowest elevation that still reads as elevated… over-elevating is a common source of visual noise." Don't stack two materials on one element.

```css
--ds-shadow-border: 0 0 0 1px #00000014;                    /* dark: #ffffff25 */
--ds-shadow-small: 0px 2px 2px #0000000a;
--ds-shadow-medium: 0px 2px 2px #0000000a, 0px 8px 8px -8px #0000000a;
--ds-shadow-menu: 0 0 0 1px #00000014, 0px 1px 1px #00000005, 0px 4px 8px -4px #0000000a, 0px 16px 24px -8px #0000000f;
--ds-shadow-modal: 0 0 0 1px #00000014, 0px 1px 1px #00000005, 0px 8px 16px -4px #0000000a, 0px 24px 32px -8px #0000000f;
--ds-focus-ring: 0 0 0 2px var(--ds-background-100), 0 0 0 4px var(--ds-focus-color);
--ds-focus-border (inputs): 0 0 0 1px var(--ds-gray-alpha-600), 0 0 0 4px #00000029;   /* dark: #ffffff3d */
```
- Spacing is a 4px base (8, 12, 16, 24, 32, 40, 64, 96, 128). Gap 24px, page margin 24px.
- Control heights 32 / 36 / 40px, form text 14/20.
- Menu rows 36px tall, 6px radius, `0 8px` padding, popover padding 6px.
- Page width 1200–1400px.
- Motion: popovers .2s, overlays .3s from scale .96 with `cubic-bezier(.175,.885,.32,1.1)`, sheets .5s `cubic-bezier(.32,.72,0,1)`, backdrop opacity .8.
