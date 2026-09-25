# Component rules

Per-component conventions from the Geist design system docs (vercel.com/geist), Devouring Details' DD System, Rauno's field notes and cmdk. Read the entry for the component you're building. Copy rules follow Vercel's: Title Case for buttons and headings in product UI, sentence case on marketing pages.

## Contents
Button · Tooltip · Modal / Dialog · Sheet / Drawer · Toast · Skeleton · Spinner and loading dots · Menu / Dropdown / Context menu · Tabs · Segmented control · Input · Empty state · Command menu · Cards and lists

---

## Button
- Use a `<button>` for mutations and a link for navigation (render prop or `asChild` onto `<a>`/`<Link>`). Never make a `<div>` clickable.
- **Loading ≠ disabled.** Pass `loading`: show a spinner beside the label, keep the label, keep the button's color, and make it functionally inert (`pointer-events: none`, `aria-busy`, and `aria-disabled` for the request's duration). "Buttons do not need to become visually disabled when loading, only functionally… reduces cognitive load because the button no longer jarringly transitions from an accent color to gray." Mount the spinner only when loading starts.
- Disable only when the action is impossible, and say why next to it. Disabled buttons can't take tooltips because they aren't focusable.
- Labels are "Verb + Noun" in Title Case: `Deploy Project`, `Save API Key`. Never bare `Submit`, `OK` or `Confirm`. Mode switches append "Instead" (`Use Password Instead`).
- A destructive button pairs 1:1 with its toast: `Delete Project` → "Project deleted".
- Icon-only buttons need an `aria-label` naming the action *and* target: "Copy deployment URL", not "Copy". Don't add `aria-label` when there's visible text.
- Press feedback: `scale(0.97)` on `:active` with a ~100–160ms transition. In light mode the button darkens on press; on inverted or dark variants it lightens. Hover changes background color only, never weight or size.
- Separate `variant` (solid, soft, ghost, outline) from `color` (accent, red, amber…), because "variant… couples color and appearance" otherwise.
- Sizes follow control heights: ~24 / 28–32 / 36 / 40px, with 16px icons. The hit area stays ≥24px even for "tiny" buttons.
- Never nest buttons. For a compound control (badge with a count and a close ×), make the pieces sibling buttons with concentric hit areas.

## Tooltip
- A tooltip explains *why* something exists or what a cryptic control does. It doesn't repeat the visible label or describe the interaction ("Click to override").
- ~150ms entry delay, so it doesn't flicker as the mouse sweeps past. Once one tooltip in a group is open, neighbors open instantly with no delay and no animation.
- Opens on hover *and* keyboard focus. Escape closes it. No interactive content inside. Never wrap a labeled input in a tooltip.
- One sentence, sentence case, no trailing period for a fragment. Tooltips are the only floating element with an arrow or stem.
- Treat them as a last resort. Inline help or a better label is usually the real fix.

## Modal / Dialog
- Only for decisions that block the page. For context or detail, use a sheet, drawer or inline expansion. Destructive confirmations belong in a modal, because sheets "read as too soft".
- Trap focus, return it to the trigger on close, close on Escape and backdrop click (except when there are unsaved edits).
- The title is a Title Case statement, never a question ("Delete Project", not "Are you sure?"). The body is 1–3 sentences, consequence first. The primary button repeats the title's verb. `Cancel` stays literal. Use `Done` for acknowledgments. End destructive bodies with "This cannot be undone."
- Default focus goes to Cancel on destructive modals. Enter never triggers a destructive action without typed confirmation. For high-stakes actions, require typing the resource name.
- Motion: fade and scale from ~0.96 over 200–300ms with ease-out, from the center (modals are the one popover-like surface that isn't anchored to a trigger). Backdrop fades to ~0.8 opacity. `overscroll-behavior: contain` on the scroll region.

## Sheet / Drawer
- For contextual detail that keeps the page visible. Bottom sheets on mobile: max-height 75–80dvh, a drag handle, and swipe-down to dismiss (velocity- and distance-based; see `interface-motion`).
- Transition `transform 0.5s cubic-bezier(0.32, 0.72, 0, 1)` (the iOS sheet curve). Backdrop `rgb(0 0 0 / 0.7)`.
- How the page behind reacts signals what's still interactive. Blurred or dimmed means inert. Content that slides away at full opacity stays reachable.

## Toast
- Only for non-blocking acknowledgment of something the user did, or background events they need to know about. Never narrate a flow with a stack of toasts.
- Copy: `{Noun} {past-participle}` ("Domain added"). Never "successfully". Errors are two short sentences ending in a recovery step ("Couldn't verify domain. Try again."). Use `Couldn't` for problems caused by the user's own state and `Failed to` for system errors.
- Failures the user must triage get a short toast *plus* a persistent inline record. A toast alone vanishes.
- Undo toasts stay 5–10s with the literal label `Undo`. Default auto-dismiss ~4s, paused while hovered and while the tab is hidden.
- `aria-live="polite"`. Use `assertive` only for blocking errors.
- Prefer inline feedback when there's an obvious trigger (copy → checkmark on the button).
- Stacking and swipe-to-dismiss values (Sonner) are in `interface-motion`.

## Skeleton
- Only when the layout is known. Otherwise use a spinner, loading dots or a progress bar.
- Match the final content's size and shape: pill for avatars, rounded for buttons, square for images, text-line heights for copy. A mismatch reads as a glitch when content arrives.
- Set `aria-busy="true"` on the region. No shimmer under reduced motion or on low-power devices. A static tint is fine.
- Pair with a show-delay (~150–300ms) so fast loads never flash a skeleton.

## Spinner and loading dots
- A spinner is for 1–3s waits on a single action. Waits over ~1s get copy naming the work ("Deploying…").
- Mount it when the action starts, not pre-rendered and toggled, or a half-rotation shows at idle.
- Size it to the surrounding type or icon.
- Loading dots sit inline in copy (`Saving<LoadingDots/>`), and never after a verb that has already completed.

## Menu / Dropdown / Context menu
- Opens on press (`pointerdown`), not hover. Close on activation, Escape or outside click, never on hover-out.
- Opening is instant with no entrance animation, because menus are high-frequency. A short fade-out on close is fine, and a brief accent blink on the chosen item confirms the choice (the macOS pattern).
- Cap at ~10 items and group with dividers. Destructive items go last, after a divider, in red.
- `…` only on items that open a follow-up dialog ("Rename…").
- Keyboard: arrows, Home/End, typeahead, Enter/Space to activate. Return focus to the trigger.
- Nested submenus need a safe triangle (prediction cone) so diagonal pointer paths don't close them.
- Row: ~32–36px tall, 6px radius, 8px horizontal padding, inside a container with ~4–6px padding (so row radius = container radius − padding).
- Context menus beat a repeated `···` button on every card, since they work from anywhere on the surface. Also expose the same actions in a visible dropdown for discoverability.

## Tabs
- 5–7 tabs on desktop, 3–4 on mobile. Titles are 1–2 word nouns.
- Switching is instant. The active tab lives in the URL.
- Counts go in a badge next to the title, not in the title, and the badge disappears at zero.
- The active indicator may slide (transform-based, ~200–250ms), but panel content swaps without a directional slide (tabs are lateral, not hierarchical).

## Segmented control (switch)
- 2–3 options with radio semantics (`role="radiogroup"`, arrow keys move selection).
- Pad every segment so the widest label fits. The active pill must not resize when selection changes.
- Labels are parallel, 1–2 words.

## Input
- Labels are Title Case nouns, always present (visually hidden if the design omits them). Placeholders are example values, not instructions.
- Helper text is one sentence, connected with `aria-describedby`.
- Validate on blur, or on submit for the first pass. The message names the field and the constraint ("Project name must be 1–100 characters"), without "please".
- Heights: 32 / 36 / 40px. Font ≥16px on mobile.
- Focus: border shifts plus a soft 3–4px halo (e.g., `0 0 0 1px <alpha-600>, 0 0 0 4px rgb(255 255 255 / 0.24)` on dark).
- Prefix and suffix adornments are absolutely positioned over the input's padding, and clicking them focuses the input.

## Empty state
- One primary CTA, plus a secondary only when there are two legitimate paths ("three CTAs is a smell"). Offer templates when creation is the goal.
- For no-results states, quote the query in curly quotes ("No results for “auth token”") and offer to clear filters.
- The error variant includes a copyable request ID and "Try Again".
- Never "Get Started", "Continue" or "OK" as the CTA. Name the action ("Create Project").

## Command menu (⌘K)
The `command-menu` skill has the full pattern (cmdk architecture, ranking, keyboard map, ARIA roles, styling). Key rules:
- Open with ⌘K / Ctrl+K globally. Open instantly, with no scale-in (see `command-menu` for the reasoning, and for Geist's .96 exception).
- Items are Title Case verb phrases that *act* ("Create Issue", "Go to Settings"). The placeholder names the scope and ends in "…" ("Search projects…", never bare "Search…").
- Show recents when the query is empty. Preserve the query when navigating back from a sub-page. Backspace on an empty input pops a page. Split into pages past ~30 items.
- Announce the result count in `aria-live`. Show shortcuts as `<kbd>`.

## Cards and lists
- Don't border everything: if every section is bordered, sections blend. Remove the outer container and promote the key label to a section header instead.
- Drop data that's always identical across items (it wastes a row and teaches users to ignore the area).
- Give widgets distinct visual "characters" so they're scannable at a glance.
- Interactive list rows have no gaps between hit areas. Selection is shown by background, never by weight change.
