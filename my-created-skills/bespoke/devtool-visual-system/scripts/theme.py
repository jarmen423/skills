#!/usr/bin/env python3
"""Derive and check dark-UI palettes the way Linear does it: from a few inputs, in a perceptual space.

Two commands, no dependencies:

  theme.py check  --bg '#08090a' '#f7f8f8' '#8a8f98' ...
      For each color: OKLCH, WCAG 2 contrast vs --bg, APCA Lc vs --bg, and a usage verdict.

  theme.py generate --base '#08090a' --accent '#7170ff' [--contrast 30] [--format css|tailwind|json]
      Emits a full token ladder (surfaces, borders, text tiers, accent states) as CSS custom properties.

The ladder offsets come from measuring Linear's 2026 production CSS (page L≈14, surfaces +3/+5.6/+7.8,
hover/active fills, borders ≈+12 L, text ≈98/87/65/51 L). `--contrast` is this script's own knob, not
Linear's algorithm: 30 reproduces the measured ladder, and 100 spreads it for a high-contrast theme.
"""
from __future__ import annotations

import argparse
import json
import math
import sys

# ---------- color math (sRGB <-> OKLab/OKLCH, WCAG, APCA) ----------

def hex_to_rgb(h: str) -> tuple[float, float, float, float]:
    raw, h = h, h.strip().lstrip("#")
    if len(h) not in (3, 4, 6, 8) or any(c not in "0123456789abcdefABCDEF" for c in h):
        raise ValueError(f"not a hex color: {raw!r}")
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h)
    if len(h) not in (6, 8):
        raise ValueError(f"bad hex color: #{h}")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
    return r, g, b, a


def rgb_to_hex(r: float, g: float, b: float) -> str:
    return "#" + "".join(f"{round(max(0, min(1, c)) * 255):02x}" for c in (r, g, b))


def to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def from_linear(c: float) -> float:
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def rgb_to_oklch(r: float, g: float, b: float) -> tuple[float, float, float]:
    r, g, b = to_linear(r), to_linear(g), to_linear(b)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(x) ** (1 / 3), x) for x in (l, m, s))
    L = 0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_
    A = 1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_
    B = 0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_
    C = math.hypot(A, B)
    H = math.degrees(math.atan2(B, A)) % 360
    return L, C, H


def oklch_to_rgb(L: float, C: float, H: float) -> tuple[float, float, float]:
    A, B = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = L + 0.3963377774 * A + 0.2158037573 * B
    m_ = L - 0.1055613458 * A - 0.0638541728 * B
    s_ = L - 0.0894841775 * A - 1.2914855480 * B
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    b = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return from_linear(r), from_linear(g), from_linear(b)


def oklch_in_gamut(L: float, C: float, H: float) -> tuple[float, float, float]:
    """Reduce chroma until the color fits sRGB (keeps L and H)."""
    lo, hi = 0.0, C
    rgb = oklch_to_rgb(L, C, H)
    if all(-1e-4 <= c <= 1 + 1e-4 for c in rgb):
        return rgb
    for _ in range(30):
        mid = (lo + hi) / 2
        if all(-1e-4 <= c <= 1 + 1e-4 for c in oklch_to_rgb(L, mid, H)):
            lo = mid
        else:
            hi = mid
    return oklch_to_rgb(L, lo, H)


def luminance(r: float, g: float, b: float) -> float:
    return 0.2126 * to_linear(r) + 0.7152 * to_linear(g) + 0.0722 * to_linear(b)


def wcag_ratio(fg: tuple[float, float, float], bg: tuple[float, float, float]) -> float:
    a, b = luminance(*fg), luminance(*bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


def apca_lc(txt: tuple[float, float, float], bg: tuple[float, float, float]) -> float:
    """APCA-W3 0.0.98G contrast (Lc). Positive = dark text on light, negative = light text on dark."""
    def y(rgb):
        r, g, b = (c ** 2.4 for c in rgb)
        return 0.2126729 * r + 0.7151522 * g + 0.0721750 * b

    def clamp(v):
        return v + (0.022 - v) ** 1.414 if v < 0.022 else v

    yt, yb = clamp(y(txt)), clamp(y(bg))
    if abs(yb - yt) < 0.0005:
        return 0.0
    if yb > yt:
        s = (yb ** 0.56 - yt ** 0.57) * 1.14
        return 0.0 if s < 0.1 else (s - 0.027) * 100
    s = (yb ** 0.65 - yt ** 0.62) * 1.14
    return 0.0 if s > -0.1 else (s + 0.027) * 100


def over(fg_hex: str, bg_rgb: tuple[float, float, float]) -> tuple[float, float, float]:
    """Composite a possibly-translucent color over an opaque background."""
    r, g, b, a = hex_to_rgb(fg_hex)
    return tuple(a * f + (1 - a) * k for f, k in zip((r, g, b), bg_rgb))  # type: ignore[return-value]


def wcag_use(ratio: float) -> str:
    if ratio >= 7:
        return "AAA"
    if ratio >= 4.5:
        return "AA"
    if ratio >= 3:
        return "AA-large"
    return "fail"


def apca_use(lc: float) -> str:
    """APCA bronze-level guidance by |Lc| (use APCA over WCAG 2 for dark UIs)."""
    x = abs(lc)
    if x >= 75:
        return "body text, any size"
    if x >= 60:
        return "body text ≥16px"
    if x >= 45:
        return "large/bold text ≥24px, UI labels"
    if x >= 30:
        return "placeholder, disabled, meta, icons"
    if x >= 15:
        return "dividers, borders, non-text"
    return "surface step only"


# ---------- commands ----------

def cmd_check(args: argparse.Namespace) -> None:
    bg = hex_to_rgb(args.bg)[:3]
    Lb, Cb, Hb = rgb_to_oklch(*bg)
    print(f"background {args.bg}  oklch({Lb*100:.1f}% {Cb:.3f} {Hb:.0f})\n")
    print(f"{'color':<11}{'OKLCH L/C/H':<22}{'WCAG 2':>16}{'APCA Lc':>9}  APCA use")
    for c in args.colors:
        rgb = over(c, bg)
        L, C, H = rgb_to_oklch(*rgb)
        ratio, lc = wcag_ratio(rgb, bg), apca_lc(rgb, bg)
        print(f"{c:<11}{f'{L*100:5.1f}% {C:.3f} {H:5.0f}':<22}{ratio:6.2f}:1 {wcag_use(ratio):<8}{lc:9.1f}  {apca_use(lc)}")


def ladder(base: str, accent: str, contrast: float) -> dict[str, str]:
    bL, bC, bH = rgb_to_oklch(*hex_to_rgb(base)[:3])
    aL, aC, aH = rgb_to_oklch(*hex_to_rgb(accent)[:3])
    k = 1 + (contrast - 30) / 70 * 0.6          # 30 → 1.0 (measured), 100 → 1.6
    nC = min(bC, 0.012)                          # neutrals stay nearly achromatic
    t = lambda base_l, hi: min(0.99, hi + (base_l - hi) / k)  # push text tiers toward white

    def n(dl: float, c: float = nC) -> str:
        return rgb_to_hex(*oklch_in_gamut(max(0, min(1, bL + dl * k)), c, bH))

    def text(l: float) -> str:
        return rgb_to_hex(*oklch_in_gamut(t(l, 0.99) if k > 1 else l, min(nC, 0.015), bH))

    def acc(dl: float, c_scale: float = 1.0) -> str:
        return rgb_to_hex(*oklch_in_gamut(max(0, min(1, aL + dl)), aC * c_scale, aH))

    white = lambda a: f"rgb(255 255 255 / {a:.2f})"
    return {
        # surfaces: elevation is lightness, not shadow
        "--bg-canvas": rgb_to_hex(*oklch_in_gamut(bL, bC, bH)),
        "--bg-deep": n(-0.07),               # hero/marketing canvas (Linear #010102)
        "--bg-panel": n(0.033),              # sidebars, cards
        "--bg-raised": n(0.056),             # popovers, menus
        "--bg-overlay": n(0.078),            # dialogs
        "--bg-hover": n(0.089, nC * 1.5),
        "--bg-active": n(0.118, nC * 1.5),
        "--bg-selected": n(0.139, nC * 1.5),
        # borders: low contrast (≈1.3:1), or translucent white
        "--border-subtle": white(0.05),
        "--border": n(0.125, nC * 2),
        "--border-strong": n(0.188, nC * 2),
        "--border-alpha": white(0.08),
        "--highlight-top": white(0.04),       # inset 0 1px top-edge highlight
        # text tiers ≈ 98 / 87 / 65 / 51 L (quaternary is NOT body text)
        "--text-primary": text(0.978),
        "--text-secondary": text(0.874),
        "--text-tertiary": text(0.649),
        "--text-quaternary": text(0.509),
        # one accent, used for primary action, selection, focus, links
        "--accent": rgb_to_hex(*oklch_in_gamut(aL, aC, aH)),
        "--accent-hover": acc(0.068, 0.8),
        "--accent-tint": rgb_to_hex(*oklch_in_gamut(min(bL + 0.09, 0.3), aC * 0.3, aH)),
        "--ring": acc(0.068, 0.8),
        "--selection": f"color-mix(in oklch, {accent} 36%, transparent)",
        "--scrim": "rgb(0 0 0 / 0.85)",
    }


def cmd_generate(args: argparse.Namespace) -> None:
    tokens = ladder(args.base, args.accent, args.contrast)
    if args.format == "json":
        print(json.dumps(tokens, indent=2))
        return
    if args.format == "tailwind":
        # utility-friendly names: bg-panel, border-line, text-fg-muted, ring-ring …
        rename = {"--bg-": "--color-", "--border-subtle": "--color-line-subtle", "--border-strong": "--color-line-strong",
                  "--border-alpha": "--color-line-alpha", "--border": "--color-line", "--text-primary": "--color-fg",
                  "--text-secondary": "--color-fg-secondary", "--text-tertiary": "--color-fg-muted",
                  "--text-quaternary": "--color-fg-subtle", "--highlight-top": "--color-highlight"}
        print("@theme {")
        for k, v in tokens.items():
            name = next((k.replace(a, b, 1) for a, b in rename.items() if k.startswith(a)), "--color-" + k[2:])
            print(f"  {name}: {v};")
        print("}")
    else:
        print(":root {\n  color-scheme: dark;")
        for k, v in tokens.items():
            print(f"  {k}: {v};")
        print("}")
    bg = hex_to_rgb(tokens["--bg-canvas"])[:3]
    print("\n/* contrast vs --bg-canvas */", file=sys.stderr)
    for k in ("--text-primary", "--text-secondary", "--text-tertiary", "--text-quaternary", "--accent", "--border"):
        rgb = hex_to_rgb(tokens[k])[:3]
        r, lc = wcag_ratio(rgb, bg), apca_lc(rgb, bg)
        print(f"/* {k:<18} {r:5.2f}:1 {wcag_use(r):<8} Lc {lc:6.1f}  {apca_use(lc)} */", file=sys.stderr)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="contrast + OKLCH for colors against a background")
    c.add_argument("--bg", required=True)
    c.add_argument("colors", nargs="+", help="hex colors; #rrggbbaa is composited over --bg")
    c.set_defaults(func=cmd_check)
    g = sub.add_parser("generate", help="derive a dark token ladder from base + accent")
    g.add_argument("--base", default="#08090a")
    g.add_argument("--accent", default="#7170ff")
    g.add_argument("--contrast", type=float, default=30, help="30 = standard, 100 = high contrast")
    g.add_argument("--format", choices=["css", "tailwind", "json"], default="css")
    g.set_defaults(func=cmd_generate)
    args = p.parse_args()
    try:
        args.func(args)
    except ValueError as e:
        p.error(f"{e} (colors must be hex: #rgb, #rrggbb or #rrggbbaa)")


if __name__ == "__main__":
    main()
