# Choreography, depth and novelty

How to sequence several moving parts, and how to budget motion across a page. Sources: Rauno Freiberg's "Designing Depth", "Novelty" and "What will you ship?" (Vercel homepage), Emil Kowalski's "Train Your Judgement" demos, and Vercel's view-transition recipes.

## Choreography: things don't all move at once
"You rarely see all the leaves of a tree moving in a jarring concert all at once." Choreography is deciding *when* each part moves.

- **Start nearest the trigger.** Feedback begins where the user acted, "to promptly communicate that the interface understood you." iOS search pulled down from the top blurs the home screen first, then suggestions appear, then the input morphs and the keyboard peeks. Opened from the bottom button, the same overlay runs in reverse order: the input first, suggestions after "a very slight delay."
- **Follow-through and overlapping action** (the Disney principles Rauno cites most): the main element leads and secondary parts trail it slightly. A panel settles, then its accent line finishes. Keep the trail short so it reads as one motion, not two animations.
- **Stagger siblings like a flock.** A group of similar items appears in quick sequence, which tells the user how many things changed and in what order. It doesn't make the interface feel slower when kept to 30–80ms per item. Cap the total so the last item isn't waiting.
- **Stagger by importance on heroes** (see recipes §13), with non-uniform delays.
- **Choose one entrance per surface.** If the container animates, its content arrives with it. Two nested entrances make the user wait twice.

## Depth
- **Blur and dim what's behind an overlay.** It lowers the background on the z-axis and says "only the overlay is interactive now" (tapping the backdrop dismisses).
- **How something exits tells the user whether it's still reachable.** The iPadOS dock slides off at full opacity when Today View opens, because it's still one swipe away. When Control Center opens, it blurs with the home screen instead, because it's inert until you return.
- **Dirty the frame** (marketing visuals). A product shot floating alone "fell flat… placed as a seemingly sloppy afterthought". The fixes, in order:
  1. blur the inner background to push it back
  2. fade the bottom edge so the boundary feels infinite
  3. add offset duplicate frames or out-of-focus objects that reinforce the message (many preview deployments), not "gimmicky decorations"
- **Scroll-edge fades** instead of hard clipping. Use a sticky fade (gradient plus ~4px blur, ~48px tall) whose opacity follows scroll, `opacity = clamp(scrollTop / 15, 0, 1)`, written straight to `el.style`.

## Novelty budget
- "The more commonly an user interface action is performed, the less rewarding… any novel visual or motion treatment on it becomes." Novelty is "the equivalent of an exclamation mark", like seasoning. Aim for **90% familiar, 10% novel**.
- **Spend it on one-time moments:** first load, first login, onboarding, the first item created. Gate them so they don't replay. Rauno's pattern (written for Next.js middleware, which Next 16 renamed `proxy`, so check `node_modules/next/dist/docs/` for the current API before using it):
  ```ts
  if (request.nextUrl.pathname === "/introduction" && request.cookies.get(COOKIE_ANIMATE_INTRO)?.value === "true") {
    const res = NextResponse.rewrite(new URL("/introduction-animate", request.nextUrl));
    res.cookies.set(COOKIE_ANIMATE_INTRO, "false");
    return res;
  }
  ```
  Lighter alternatives: read the cookie in a Server Component and pass an `animate` prop, or check a `sessionStorage` flag on the client before running the entrance (render the static state first so nothing flashes). Paco Coursey's site staggers the first load but not back-navigation, and iOS staggers home-screen icons after unlock but not when returning from an app.
- **Map the page's rhythm.** On the Vercel homepage, every animated section was tagged high-novelty (a long-distance graph tooltip, pixelating icons) or low-novelty (floating cursors, icon scale on hover). "High novelty animations never appear consecutively between sections, but may be paired with lower novelty animations," with a calm interlude after each animated segment. The same applies to visual motifs: if every section uses the accent color or the grid-and-cross motif, none of them feel significant.
- **Contrast invites curiosity; too much becomes noise.** One rotated, hand-drawn or off-palette element creates intrigue. Five create chaos. That belongs to first impressions and marketing, not productivity screens.
- **The product's intent sets tolerance.** A game or microsite can carry experimental transitions. A tool people use all day pays a "novelty tax" for each one.

## Process
- **Ship the static version first**, then layer animations in follow-up changes. If an animation "didn't perform well, felt pompous, or out of rhythm relative to the page, we didn't build it."
- **Dial ideas to 100 before judging them.** "Build until you feel there's nothing more to explore. Then you dial even the stupidest idea to 100, so you can go back 10 iterations and clearly see, 'Ah, the simple one actually felt way better.'"
- **Sand the edges.** Spam-click, scroll fast, test on low battery and in Safari, and toggle states with temporary keyboard shortcuts until you stop finding splinters.
