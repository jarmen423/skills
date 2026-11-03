# Bento templates

Copy-ready layouts. Every template uses the shared base below, `grid-template-areas`, and a DOM order that already matches the mobile reading order. The measurements come from the bentogrids.com teardowns (approximate, from screenshots) and from linear.app's CSS.

## Contents
- Base
- React + Tailwind v4 component (areas as data)
- T1 Mirrored brick
- T2 Hero + trio / pair
- T3 Textbook 2×2 hero
- T4 Four-column mirrored (wide cells text-left, visual-right)
- T5 Two over three with a grouped outer radius
- T6 Tall sides
- T7 Staggered tall cells
- T8 Drawn grid (Vercel)
- T9 Bento as hero (stat ring)
- T10 Masonry columns
- Mobile reset (put last)
- Mobile carousel
- Cell recipes

---

## Base
```css
.bento {
  --gap: 24px; --r: 24px;
  display: grid; gap: var(--gap);
  grid-template-columns: repeat(12, minmax(0, 1fr));
}
.bento > * { min-width: 0; border-radius: var(--r); overflow: clip; container-type: inline-size; position: relative; }
@media (max-width: 1024px) { .bento { --gap: 16px; } }
```
Templates below add a second class (`<div class="bento t1">`). Put the **mobile reset at the end of the stylesheet, after every template** (see "Mobile reset"). Otherwise the templates, which have the same specificity and come later, silently restore their desktop areas on phones.

## React + Tailwind v4 component (areas as data, Linear's pattern)
```tsx
type Areas = { base: string; md?: string; sm?: string };

export function Bento({ areas, className, children }: { areas: Areas; className?: string; children: React.ReactNode }) {
  return (
    <div
      className={cn(
        "grid gap-4 md:gap-6 grid-cols-4 md:grid-cols-12",
        "[grid-template-areas:var(--areas-sm,var(--areas))] md:[grid-template-areas:var(--areas-md,var(--areas))] lg:[grid-template-areas:var(--areas)]",
        className,
      )}
      style={{ "--areas": areas.base, "--areas-md": areas.md, "--areas-sm": areas.sm } as React.CSSProperties}
    >
      {children}
    </div>
  );
}

export function Cell({ area, className, ...props }: React.ComponentProps<"article"> & { area: string }) {
  return <article style={{ gridArea: area }} className={cn("@container relative min-w-0 overflow-clip rounded-3xl", className)} {...props} />;
}

// usage: mirrored brick
<Bento areas={{
  base: `"a a a a a a a b b b b b" "c c c c c d d d d d d d"`,
  md:   `"a a a a a a a a a a a a" "b b b b b b c c c c c c" "d d d d d d d d d d d d"`,
  sm:   `"a a a a" "b b b b" "c c c c" "d d d d"`,
}}>
  <Cell area="a">…</Cell><Cell area="b">…</Cell><Cell area="c">…</Cell><Cell area="d">…</Cell>
</Bento>
```
(Tailwind v4 has no `grid-template-areas` utility, so use the arbitrary property as above, or plain CSS.)

## T1. Mirrored brick: 7/5 then 5/7 (Copilot, Attio, Linear Asks), or 8/4 then 4/8 (Linear 2022)
```css
.t1 { grid-template-areas: "a a a a a a a b b b b b" "c c c c c d d d d d d d"; grid-auto-rows: minmax(360px, auto); }
@media (max-width: 1024px) { .t1 { grid-template-areas: "a a a a a a a a a a a a" "b b b b b b c c c c c c" "d d d d d d d d d d d d"; } }
```
Copilot measured about a 32px gap and a 24px radius, with 2 gradient cells placed diagonally. The Linear rebuild used a 24px gap, a 48px radius, 32→56px padding and a 480px min-height.

## T2. Full-width hero + trio (Raycast) / + pair (Neon)
```css
.t2 { grid-template-areas: "h h h h h h h h h h h h" "a a a a b b b b c c c c"; }
.t2 .h { aspect-ratio: 16 / 7; overflow: visible; } /* let UI break the top edge */
@media (max-width: 1024px) { .t2 { grid-template-areas: "h h h h h h h h h h h h" "a a a a a a b b b b b b" "c c c c c c c c c c c c"; } }
```

## T3. Textbook 3-column with a 2×2 hero
```css
.t3 { grid-template-columns: repeat(3, minmax(0,1fr)); grid-auto-rows: 220px;
      grid-template-areas: "hero hero a" "hero hero b" "c d e"; }
@media (max-width: 1024px) { .t3 { grid-template-columns: repeat(2, minmax(0,1fr));
      grid-template-areas: "hero hero" "hero hero" "a b" "c d" "e e"; } }
@media (max-width: 640px) { .t3 { grid-template-columns: 1fr; grid-auto-rows: auto;
      grid-template-areas: "hero" "a" "b" "c" "d" "e"; } }
```

## T4. Four-column mirrored (Supabase)
```css
.t4 { grid-template-columns: repeat(4, minmax(0,1fr)); grid-auto-rows: 400px;
      grid-template-areas: "db db auth edge" "store rt vec vec"; }
@media (max-width: 1024px) { .t4 { grid-template-columns: repeat(2, minmax(0,1fr));
      grid-template-areas: "db db" "auth edge" "store rt" "vec vec"; } }
```
The wide cells put text on the left and the visual on the right (`@container (min-width: 36rem) { flex-direction: row }`). The narrow cells center their text with the visual below, bleeding off the edge. A consistent square icon tile in every cell creates the rhythm. Measured about a 12px radius, 24px gap and 10% white borders.

## T5. Two over three, grouped outer radius (Mintlify, Tailwind UI)
```css
.t5 { grid-template-columns: repeat(6, minmax(0,1fr)); --R: 40px; --r: 12px; gap: 8px; }
.t5 > :nth-child(1), .t5 > :nth-child(2) { grid-column: span 3; }
.t5 > :nth-child(n+3) { grid-column: span 2; }
.t5 > * { border-radius: var(--r); }
.t5 > :nth-child(1) { border-top-left-radius: var(--R); }
.t5 > :nth-child(2) { border-top-right-radius: var(--R); }
.t5 > :nth-child(3) { border-bottom-left-radius: var(--R); }
.t5 > :nth-child(5) { border-bottom-right-radius: var(--R); }
@media (max-width: 640px) { .t5 > * { grid-column: 1 / -1; border-radius: var(--r); }
  .t5 > :first-child { border-radius: var(--R) var(--R) var(--r) var(--r); }
  .t5 > :last-child  { border-radius: var(--r) var(--r) var(--R) var(--R); } }
```
The tight gap (≤ the inner radius) makes the grid read as one object. Text sits centered *below* the visual.

## T6. Tall sides (Tailwind UI)
```css
.t6 { grid-template-columns: repeat(3, minmax(0,1fr)); grid-template-rows: repeat(2, minmax(280px, auto));
      grid-template-areas: "a b c" "a d c"; }
```
Put a phone mockup or code editor in the tall cells and let it bleed off the bottom edge.

## T7. Staggered tall cells (Clerk)
```css
.t7 { grid-template-columns: repeat(3, minmax(0,1fr)); grid-auto-rows: 280px; gap: 8px;
      grid-template-areas: "mfa sess otp" "sec sess pw" "magic sso hook" "magic bot hook"; }
```
No horizontal break line crosses all three columns. Keep it monochrome, with small titles (~15px medium) and a mini product illustration per cell.

## T8. Drawn grid, no surfaces (Vercel)
```css
.t8 { display: grid; grid-template-columns: 1fr 1fr; gap: 0; border-top: 1px solid var(--line); }
.t8 > * { padding: 64px; border-radius: 0; overflow: visible; background: none;
          border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); }
.t8 > :nth-child(2n) { border-right: 0; }
.t8 .cross { position: absolute; width: 15px; height: 15px; transform: translate(-50%, -50%); pointer-events: none; }
.t8 .cross::before, .t8 .cross::after { content: ""; position: absolute; background: var(--line-strong); }
.t8 .cross::before { left: 7px; top: 0; width: 1px; height: 100%; }
.t8 .cross::after  { top: 7px; left: 0; height: 1px; width: 100%; }
```
Use the bright-lead + muted-continuation lockup at ~24–28px. Rauno's grid-guide technique renders guides even for empty cells: `.grid-guides { display: contents }`, with each guide `position: absolute; grid-column-start: var(--x); grid-row-start: var(--y)` and borders only on the right and bottom.

## T9. Bento as hero (Axiom)
```css
.t9 { grid-template-columns: repeat(4, minmax(0,1fr)); grid-auto-rows: 120px; gap: 12px;
      grid-template-areas: "s1 s2 s3 s4" "s5 hero hero s6" "s7 hero hero s8" "s9 hero hero s10" "s11 s12 s13 s14"; }
```
This only works when every ring cell is a single-token stat ("5 TB / Ingest included") in one accent color.

## T10. Masonry columns (Apple AirPods, Framer)
```css
.t10 { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 20px; align-items: start; }
.t10 > .col { display: flex; flex-direction: column; gap: 20px; }
```
Each column is independent, and cell heights come from content or explicit `aspect-ratio`, so row lines never align. Hierarchy is carried by column position.

## Mobile reset (put last)
```css
/* Must come AFTER all templates: same-specificity template rules declared later would win otherwise. */
@media (max-width: 640px) {
  .bento { --gap: 12px; grid-template-columns: 1fr; grid-template-areas: none; }
  .bento > :nth-child(n) { grid-area: auto; grid-column: auto; grid-row: auto; }  /* :nth-child(n) matches T5's specificity */
}
```
This works only because the DOM is already in mobile reading order. If a template needs a different phone order, give it its own `@media` block with explicit areas instead of the reset.

## Mobile carousel (Linear rebuild)
```html
<div class="h-[480px] overflow-hidden md:h-auto md:overflow-visible">          <!-- clips the scrollbar -->
  <div class="flex snap-x snap-mandatory gap-4 overflow-x-auto px-6 pb-12 md:grid md:grid-cols-12 md:gap-6 md:overflow-visible md:p-0">
    <article class="w-[85%] shrink-0 snap-center md:col-span-8 md:w-auto">…</article>
    <article class="w-[85%] shrink-0 snap-center md:col-span-4 md:w-auto">…</article>
  </div>
</div>
```
Add `scroll-padding-inline` equal to the side padding. Consider dots or a count ("1 / 4") for orientation, and make sure every card can be reached by keyboard (tab order follows the DOM).

## Cell recipes

**Product-crop cell (text bottom):**
```tsx
<article className="group relative flex min-h-[420px] flex-col justify-end overflow-clip rounded-3xl border border-white/[0.08] bg-[linear-gradient(rgb(255_255_255/0),rgb(255_255_255/0.04))] p-8">
  <img src="/crops/triage.png" alt="" aria-hidden width={1200} height={800}
       className="pointer-events-none absolute left-8 top-8 w-[160%] max-w-none rounded-xl border border-white/10 [mask-image:linear-gradient(black,transparent_75%)]" />
  <h3 className="relative text-[22px] font-medium tracking-[-0.012em] text-fg">Triage in seconds</h3>
  <p className="relative mt-2 max-w-[310px] text-[15px] text-fg-muted">Route incoming work to the right team automatically.</p>
</article>
```

**Stat cell:**
```tsx
<article className="@container flex flex-col justify-between rounded-3xl border border-white/[0.08] p-6">
  <p className="text-sm text-fg-muted">Median recall latency</p>
  <p className="font-semibold tracking-[-0.04em] text-[clamp(48px,14cqi,88px)] leading-none tabular-nums">
    38<span className="text-[0.45em] text-fg-muted">ms</span>
  </p>
  <p className="text-sm text-fg-subtle">p50 across 1.2M queries</p>
</article>
```

**Icon + one-liner cell:**
```tsx
<article className="rounded-2xl border border-white/[0.08] p-5">
  <span className="flex size-8 items-center justify-center rounded-lg bg-white/[0.05] ring-1 ring-inset ring-white/[0.08]"><Icon aria-hidden className="size-4" /></span>
  <p className="mt-4 text-[15px]"><strong className="font-medium text-fg">Self-hosted.</strong> <span className="text-fg-muted">Your data never leaves your VPC.</span></p>
</article>
```
