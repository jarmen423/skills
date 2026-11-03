#!/usr/bin/env bash
# Grep UI source for interface-guideline anti-patterns.
#
# Usage: scan.sh [path ...]        (defaults to ./src, or . if there is no src/)
#
# Every hit is a CANDIDATE, not a verdict: grep can't see a global focus style,
# a wrapper that supplies a label, or a deliberate exception. Open each line and
# confirm before reporting it.

set -uo pipefail

paths=("$@")
if [ ${#paths[@]} -eq 0 ]; then
  if [ -d src ]; then paths=(src); else paths=(.); fi
fi

globs=(-g '*.tsx' -g '*.jsx' -g '*.ts' -g '*.js' -g '*.css' -g '*.scss' -g '*.html' -g '*.vue' -g '*.svelte' -g '*.astro' -g '*.mdx'
       -g '!node_modules' -g '!.next' -g '!dist' -g '!build' -g '!out' -g '!coverage' -g '!*.min.*')

search() { # $1 = regex, rest = paths
  local re=$1; shift
  if command -v rg >/dev/null 2>&1; then
    rg -n --no-heading --color=never "${globs[@]}" -e "$re" "$@" 2>/dev/null
  else
    grep -rnE --include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js' --include='*.css' \
      --include='*.scss' --include='*.html' --include='*.vue' --include='*.svelte' --include='*.astro' --include='*.mdx' \
      --exclude-dir=node_modules --exclude-dir=.next --exclude-dir=dist --exclude-dir=build --exclude-dir=out \
      -e "$re" "$@" 2>/dev/null
  fi
}

# tag | regex | what to verify
checks=(
  "transition-all|transition-all\b|transition:[[:space:]]*all\b|\`transition: all\` animates layout props by accident; list the properties"
  "focus|outline-none|outline:[[:space:]]*(none|0)\b|focus ring removed; confirm a focus-visible replacement on the same element"
  "zoom|user-scalable=no|maximum-scale=1|userScalable:[[:space:]]*false|maximumScale:[[:space:]]*1\b|never disable pinch zoom"
  "paste|onPaste|confirm it doesn't preventDefault; never block paste"
  "semantics|<(div|span|li|img|svg)[^>]*onClick|clickable non-button; use <button> or <a> (keyboard + a11y)"
  "nav|onClick=\{[^}]*(router\.push|location\.href|window\.open)|navigation in onClick; use <a>/<Link> so ⌘-click and prefetch work"
  "ellipsis|[A-Za-z]\.\.\.([\"'<\`[:space:]]|$)|use … (U+2026) in user-facing text, not ..."
  "autofocus|autoFocus|\bautofocus\b|autofocus needs a reason; avoid on touch devices"
  "tabindex|tabIndex=\{?[\"']?[1-9]|positive tabIndex breaks DOM focus order"
  "scale-0|\bscale-0\b|scale\(0\)|scale:[[:space:]]*0[,[:space:]}]|scale:[[:space:]]*\[0[,[:space:]]|never animate from scale(0); start at 0.9–0.97 (by size) with opacity 0"
  "layout-anim|animate=\{\{[^}]*\b(width|height|top|left)\b|transition-\[[^]]*(width|height|top|left)|transition:[^;]*\b(width|height|top|left)\b|animating layout properties; prefer transform/opacity"
  "ease-in|\bease-in([\"'[:space:];,)]|$)|easeIn\b|ease-in on entering/moving UI feels sluggish; use ease-out (a short ≤150ms exit is the only exception)"
  "weight-shift|hover:font-(medium|semibold|bold|black)|group-hover:font-|data-\[state=active\]:font-(medium|semibold|bold)|font weight change on hover/selection shifts layout"
  "pointer-state|on(Pointer|Mouse)Move=\{[^}]*set[A-Z]|setState per pointer move; fine for discrete state (active index), but continuous values (x/y, progress) belong in a ref or CSS variable"
  "random|Math\.random\(\)|Math.random in render causes hydration mismatch; move to effect or seed it"
  "big-blur|(backdrop-)?blur-(2xl|3xl)\b|blur\(([4-9][0-9]|[1-9][0-9]{2})px\)|large blur/backdrop-filter is expensive, especially animated or full-screen"
  "will-change|will-change|permanent will-change wastes memory; set it only while animating"
  "vh|\bh-screen\b|min-h-screen|100vh|100vh jumps with mobile browser chrome; consider dvh/svh"
)

total=0
for entry in "${checks[@]}"; do
  tag=${entry%%|*}
  rest=${entry#*|}
  hint=${rest##*|}
  re=${rest%|*}
  case $tag in
    focus) skip='focus-visible' ;;   # replacement ring on the same line
    *) skip='' ;;
  esac
  while IFS= read -r hit; do
    [ -z "$hit" ] && continue
    if [ -n "$skip" ] && printf '%s' "$hit" | grep -qE "$skip"; then continue; fi
    loc=${hit%%:*}; tmp=${hit#*:}; line=${tmp%%:*}; code=${tmp#*:}
    code=$(printf '%s' "$code" | sed -E 's/^[[:space:]]+//' | cut -c1-120)
    printf '%s:%s [%s] %s\n    %s\n' "$loc" "$line" "$tag" "$hint" "$code"
    total=$((total + 1))
  done < <(search "$re" "${paths[@]}")
done

# <img> without explicit dimensions on the same line (multi-line JSX will false-positive; check manually)
while IFS= read -r hit; do
  [ -z "$hit" ] && continue
  loc=${hit%%:*}; tmp=${hit#*:}; line=${tmp%%:*}
  printf '%s:%s [img-size] <img> without width/height on this line; confirm dimensions or aspect-ratio\n' "$loc" "$line"
  total=$((total + 1))
done < <(search '<img\b' "${paths[@]}" | grep -vE 'width|height|fill' || true)

echo
echo "$total candidate(s). Verify each in context; the scanner can't see missing states, labels or live regions."
