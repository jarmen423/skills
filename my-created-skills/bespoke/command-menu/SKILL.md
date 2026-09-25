---
name: command-menu
description: How to build or fix a ⌘K command menu the way Linear, Vercel and Raycast do, from cmdk's source and Geist's rules. Covers the combobox accessibility pattern, keyboard map, IME composition guard, pointer-vs-keyboard selection, fuzzy ranking and groups, nested pages, recents, empty states, copy, styling and performance. Use whenever the user mentions a command menu or palette, ⌘K or Ctrl+K, a quick switcher or omnibar, or any list that filters as you type.
---

# Command menu

A command menu is the keyboard-first spine of a devtool. Linear: "You can take almost every action in Linear without lifting your fingers off of the keyboard", and ⌘K is the door. People open it hundreds of times a day, so every rule here serves one goal: **it must feel instant and never get in the way.** Paco Coursey, who wrote cmdk: "What we call a delightful user experience is just delivering a faster path to user goals."

## Build vs. reuse
- **Prefer `cmdk`** (unstyled, accessible, used by Vercel, Linear's site, shadcn's `<Command>`) for new menus. It handles filtering, ranking, grouping, ARIA and keyboard navigation, and performs well up to ~2,000–3,000 items without virtualization. Beyond that, pass `shouldFilter={false}`, filter yourself and virtualize.
- **If the project already has a custom menu,** don't swap libraries unasked. Audit it against the checklist at the bottom and fix the gaps.

## Opening and closing
- **Bind the shortcut yourself** (cmdk deliberately doesn't), on `keydown`, with `(e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k"` and `preventDefault()`. Toggle, don't just open. Show `⌘K` on macOS and `Ctrl K` elsewhere.
- **No entrance animation, at least when opened from the keyboard.** A menu opened 100+ times a day "would be very annoying" if it animated (Emil Kowalski, citing Raycast), and Rauno calls repeated command-menu animation "cognitive burden". Render it instantly. A ≤100ms backdrop fade is the most it should get, and exits may fade. Vercel's Geist ships a subtle `scale(.96)` entrance; if a product keeps one, make it ≤150ms and skip it for keyboard opens.
- **Focus:** the input is focused on open. On close, focus returns to the element that was focused before. Escape closes (or pops a page, see below). Clicking the backdrop closes.
- **Scroll lock** on the page while open, with `scrollbar-gutter: stable` (or compensate for the removed scrollbar's width) so the page doesn't shift sideways.
- Keep `open` false during SSR to avoid a hydration mismatch.

## Structure and accessibility (the combobox pattern)
DOM focus stays in the input the whole time. The highlighted option is communicated through `aria-activedescendant`, not by moving focus (that would be roving tabindex).

| Part | Role and attributes |
|---|---|
| Dialog | `role="dialog"`, `aria-modal="true"`, `aria-label="Command menu"` |
| Label | visually hidden `<label>` bound to the input |
| Input | `role="combobox"`, `aria-expanded="true"`, `aria-controls={listId}`, `aria-activedescendant={activeItemId}`, `aria-autocomplete="list"`, `autoComplete="off"`, `autoCorrect="off"`, `spellCheck={false}` |
| List | `role="listbox"`, `aria-label` |
| Group | wrapper `role="presentation"`; items container `role="group"` + `aria-labelledby` its heading |
| Item | `role="option"`, stable `id`, `aria-selected`, `aria-disabled` |
| Empty | "No results for “{query}”" |
| Loading | `role="progressbar"` (or an `aria-live` "Loading…") |
| Result count | a visually hidden `aria-live="polite"` region: "12 results" |

## Keyboard map
| Keys | Action |
|---|---|
| ↓ / ↑ | next / previous item (optionally `loop`) |
| Ctrl+N / Ctrl+J, Ctrl+P / Ctrl+K | down / up (Emacs and Vim bindings, on by default in cmdk) |
| ⌘↓ / ⌘↑, Home / End | last / first item |
| Alt+↓ / Alt+↑ | first item of the next / previous group |
| Enter | run the selected item |
| Escape | pop a nested page, else close |
| Backspace on an empty input | pop a nested page |

**Guard against IME composition** in every handler. Otherwise, pressing Enter to confirm a Japanese, Chinese or Korean composition runs a command:
```ts
if (e.nativeEvent.isComposing || e.keyCode === 229 || e.defaultPrevented) return;
```

## Selection: keyboard vs. pointer
- Track the selected item **by value (a stable id), not by index**, so the selection survives items mounting and unmounting as results change. After each keystroke, select the first result.
- **Pointer selects on `pointermove`, not `pointerenter`** (cmdk's behavior). The likely reason: the list scrolls and re-filters under a resting cursor, and `pointerenter` would then steal the keyboard's selection.
- **Hover never scrolls the list; the keyboard does.** Only keyboard moves call `scrollIntoView({ block: "nearest" })`. When the selected item is the first in its group, scroll the group heading into view too, so headings aren't clipped. Give the list `scroll-padding-block: 8px`.
- Selection and hover changes are instant (`transition: none`). Only `:active` gets a brief background change.

## Filtering and ranking
- **Fuzzy, abbreviation-friendly scoring** (cmdk's `command-score`). Ranking order:
  1. consecutive character matches
  2. matches at word starts after a space or hyphen (0.9)
  3. matches after `/ \ _ + . # " @ [ ( { &` (0.8)
  4. mid-word jumps (0.17)

  Transpositions still match weakly (0.1). There are tiny penalties for skipped characters (0.999 each), case mismatches (0.9999) and incomplete matches (0.99), so "html" beats "html5" for the query "html". For fuzzy search, copy `command-score.ts` from github.com/dip/cmdk (MIT) rather than reinventing it.
- For small, curated menus (<200 items), a tiered scorer is fine: label prefix > word-start > substring > all query words present in label + keywords.
- **Keywords (aliases)** are part of the searchable text: "theme" should find "Toggle Dark Mode", and "billing" should find "Settings → Plans". Normalize case, spaces and hyphens once, not per comparison.
- **Groups** are ordered by their best item's score, and items are sorted within each group. Ungrouped items go on top. Hide empty groups with the `hidden` attribute and don't leave spacing gaps (`*:not([hidden]) + [group] { margin-top: 8px }`).
- **Items only shown while searching.** Deep actions like "Change theme to Dark" appear once the user types, which keeps the empty state short.

## Content
- **Empty query:** show recents first (last 3–5 actions or pages), then suggested commands in groups. Never show an empty box.
- **Items are Title Case verb phrases that act:** "Create Issue", "Go to Settings", "Copy Install Command". Items that open a sub-page end in "…" ("Change Theme…", "Search Docs…").
- **The placeholder names the scope** and ends in "…": "Search projects and commands…", never a bare "Search…". Inside a sub-page, show the page as a badge above or inside the input (e.g. `Theme ›`).
- Show the item's own shortcut as a right-aligned `<kbd>`, so the menu teaches the keyboard (Linear's context menus do this too). Put icons at 16px in the tertiary color, brightening when selected.
- **No results:** “No results for “{query}”.” plus an escape hatch (search the docs, ask support, clear filters).
- **Split into pages** past ~30 top-level items. Preserve the query when navigating back from a sub-page.

## Nested pages
Keep a stack: `const [pages, setPages] = useState<string[]>([])`. The current page is `pages.at(-1)`. Escape, or Backspace on an empty query, pops it. Reset the query when pushing a page, and restore it when popping. The list height animates between pages (below), and content swaps without a slide.

## Dimensions and styling
- Dialog: `max-width: 640px`, top-anchored (`padding-top: 12–15vh`), radius 8–16px, a 1px border at white 8–10%. The surface is the raised tier, or a nearly invisible gradient (Linear: `linear-gradient(136.61deg, rgb(39 40 43) 13.72%, rgb(45 46 49) 74.3%)`). Shadow `0 16px 70px rgb(0 0 0 / 0.2)` or deeper on dark. Backdrop `rgb(0 0 0 / 0.5–0.6)`, optional 2px blur.
- Input: 17–18px text, 48–56px tall, 20px padding, a bottom hairline, `caret-color` in the accent.
- Rows: 40–48px (36px in dense menus), 14px text, 12px icon gap, 8px radius inset within the list's 8px padding. Selected: a subtle fill (white 5–8%) and optionally a 3px accent bar on the left. Group headings: 12px, tertiary, 8px horizontal padding.
- `<kbd>`: 20px minimum, 4px radius, a surface one step up, 12–13px in the tertiary color.
- **List height transition:** measure the list with a ResizeObserver, write `--list-height`, and use `height: min(400px, var(--list-height)); transition: height 100ms ease`. This is the one animation worth having: it keeps the box from jumping as results filter.
- `overscroll-behavior: contain` on the list, and `content-visibility: auto` on rows for long lists.

## Performance
- Filter and sort synchronously on each keystroke, which is fast enough for thousands of items. Don't debounce the input for local data, because debouncing feels laggy.
- Async results: show a loading row, stream items in as they arrive, and keep filtering them. Cancel stale requests.
- Memoize item lists. Re-render only the list, not the whole dialog, on each keystroke (cmdk exposes `useCommandState(selector)` for this).

## Minimal cmdk example
cmdk's `Command.Dialog` closes on Escape before your `onKeyDown` runs, because Radix's dismiss layer listens on the document first. For nested pages, put a plain `<Command>` inside your own dialog and intercept Escape there:
```tsx
"use client";
import * as React from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { Command } from "cmdk";

export function CommandMenu() {
  const [open, setOpen] = React.useState(false);
  const [pages, setPages] = React.useState<string[]>([]);
  const [search, setSearch] = React.useState("");
  const savedQueries = React.useRef<string[]>([]);
  const page = pages.at(-1);

  const pushPage = (p: string) => { savedQueries.current.push(search); setPages((ps) => [...ps, p]); setSearch(""); };
  const popPage = () => { setPages((ps) => ps.slice(0, -1)); setSearch(savedQueries.current.pop() ?? ""); };

  React.useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.isComposing || e.keyCode === 229) return;
      if (e.key.toLowerCase() === "k" && (e.metaKey || e.ctrlKey)) { e.preventDefault(); setOpen((o) => !o); }
    };
    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <Dialog.Root open={open} onOpenChange={(o) => { setOpen(o); if (!o) { setPages([]); setSearch(""); savedQueries.current = []; } }}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 bg-black/60" />
        <Dialog.Content aria-describedby={undefined}
          className="fixed left-1/2 top-[14vh] w-full max-w-[640px] -translate-x-1/2"
          onEscapeKeyDown={(e) => { if (pages.length) { e.preventDefault(); popPage(); } }}  /* Escape pops a page first */
        >
          <Dialog.Title className="sr-only">Command menu</Dialog.Title>
          <Command label="Command menu"
            onKeyDown={(e) => {
              if (e.nativeEvent.isComposing) return;
              if (e.key === "Backspace" && !search && pages.length) { e.preventDefault(); popPage(); }
            }}>
            <Command.Input value={search} onValueChange={setSearch}
              placeholder={page === "theme" ? "Search themes…" : "Search pages and commands…"} />
            <Command.List>
              <Command.Empty>No results for “{search}”.</Command.Empty>
              {!page && (
                <Command.Group heading="Navigation">
                  <Command.Item keywords={["home"]} onSelect={() => go("/")}>Go to Home</Command.Item>
                  <Command.Item onSelect={() => pushPage("theme")}>Change Theme…</Command.Item>
                </Command.Group>
              )}
              {page === "theme" && ["Light", "Dark", "System"].map((t) => (
                <Command.Item key={t} onSelect={() => setTheme(t)}>{t}</Command.Item>
              ))}
            </Command.List>
          </Command>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```
Style through its data attributes: `[cmdk-item][data-selected="true"]`, `[cmdk-group-heading]`, `[cmdk-list]` with `--cmdk-list-height`. (`go` and `setTheme` stand in for your router and theme setter.)

## Checklist (audit any command menu against this)
- [ ] ⌘K / Ctrl+K toggles. Opening is instant with no scale-in. Focus goes to the input and returns on close.
- [ ] Combobox roles + `aria-activedescendant`, a hidden label, and a live result count
- [ ] ↑↓, Home/End, Enter, Escape, and Ctrl+N/P. **IME composition guard** on every key handler
- [ ] Selection tracked by id. First result auto-selected on each keystroke
- [ ] Pointer selects on move. **Hover doesn't scroll the list**; keyboard moves scroll to `nearest`
- [ ] Fuzzy or tiered ranking with keyword aliases. Groups ranked by best item. No gaps from empty groups
- [ ] Recents when the query is empty. Helpful "No results for “…”" with an escape hatch
- [ ] Verb-phrase items, "…" on items that open pages, a scoped placeholder, `<kbd>` shortcuts
- [ ] Nested pages pop with Escape or Backspace. Query preserved on back
- [ ] List height transitions (~100ms). The page doesn't shift when scroll locks

## In this repo (agent-memory-labs-frontend)
`src/components/command-menu.tsx` is a custom implementation. What it already does well:
- ⌘K toggle, restoring focus via `restoreRef`
- the combobox, listbox and option roles, with `aria-activedescendant`
- a tiered `score()` and ordering that depends on the query
- an `aria-live` region for toasts
- the `OPEN_EVENT` hook so other components can open the menu

Gaps against this checklist:
- The combobox input has no accessible name: there is no `<label>` or `aria-label`, and the placeholder doesn't count. The listbox has no `aria-label` either.
- Selection is tracked by index (`active`), not by item id, so it can jump when results re-rank.
- The key handler has no IME composition guard.
- `onMouseMove → setActive(i)` feeds the same effect that calls `scrollIntoView`, so hovering can scroll the list.
- There are no Home/End or Ctrl+N/P bindings, and no live result count.
- Rows use `transition-colors`, so the highlight fades behind the cursor and the arrow keys. Make selection changes instant.
- The dialog plays `zoom-in-[0.98] slide-in-from-top-2` on every open. Drop it, at least when the menu is opened from the keyboard.
- `document.body.style.overflow = "hidden"` can shift the page sideways when a scrollbar disappears. Consider `scrollbar-gutter: stable` on `html`.
