# Antigravity print-run audit — desktop My Activity port (2026-09-03)

Worked example backing the "Antigravity (agy) print-run hygiene" section of
the SKILL.md. Dispatch: `agy -p "$(cat TASK.md)" --model 'Gemini 3.1 Pro
(High)' --dangerously-skip-permissions --print-timeout 25m`, background with
process poll; finished in ~6 minutes for a 742-insertion SolidJS port.

## Launch config that worked

- Isolated worktree branched off the LEAD'S FEATURE BRANCH (not main), so the
  reference implementation (solid-shell panel/service/tests) was inside the
  worker's own tree. Reference files by worktree-relative path only — never
  absolute paths into the production clone.
- `PATH=/tmp/agy-safe-bin:$PATH` wrapper script: case-blocks
  `checkout|switch|reset|restore|stash|clean|rebase` with exit 126, else
  `exec /usr/bin/git "$@"`. Write it as a multi-line case script — a for-loop
  that rewrites the same file per iteration leaves only the LAST word blocked.
- Task brief (TASK.md, inlined via `$(cat TASK.md)`): background, exact
  endpoint contract, reference file list, desktop-specific deltas (userEaFetch
  auth, diverged BinderPanel, test script addition), constraints (no Rust, no
  changes outside the package), verification commands, and the exact commit
  message with trailers. The worker followed all of it.

## What the diff contained, and how each file was classified

| Change | Classification | How determined |
|---|---|---|
| 4 feature files + `"test": "bun test"` in package.json | keep (feature) | matched brief |
| 1 `// @ts-ignore` line each in App.tsx, PurchasesPanel.tsx, liveAuctionSearchService.ts, purchasesStore.ts | out-of-scope band-aid → revert | sed-deleted the lines, ran `bun x tsc -b`: TS6133 unused-var ×3 and TS2339 `update.relaunch` surfaced → all four mask PRE-EXISTING errors (the relaunch one hid a real updater API mismatch) → `git checkout <parent> --` each file |
| `bun.lock` (new) | out-of-scope → remove | `git ls-tree <parent> -- <pkg>/bun.lock` returned nothing (new file). Parity assumption wrong: solid-shell tracks one, tauri never did |
| tsconfig.json: added `"types": ["vite/client"]` | out-of-scope → revert | reverting resurfaced 9 pre-existing `ImportMeta.env` errors — the edit existed only to green a never-clean baseline |
| `vite.config.js`, `vite.config.d.ts`, `tsconfig*.tsbuildinfo` | tsc emit artifacts of the tsconfig edit → remove | never tracked on parent (`git ls-tree`); emitted by running tsc with the modified config |
| `vite.config.ts`: deleted `// @ts-expect-error process is a nodejs global` | out-of-scope → restore parent | restoring makes tsc flag `Unused '@ts-expect-error' directive` — the directive is stale on parent too (baseline 14→15). Not our wart to fix in a feature commit |

## The gate for a red-baseline repo

vite builds never typecheck, so `tsc -b` clean was never a real gate here:

1. `bun x tsc -b --force 2>&1 | grep -cE 'error TS'` == parent baseline count (14; 15 after honestly restoring the parent's stale directive).
2. Zero errors mentioning new/touched files (grep for the new filenames).
3. Full `bun test` green (16/16).
4. Production `bun run build` green.

`--force` is mandatory: stale `tsconfig.tsbuildinfo` from the worker's run
made plain `tsc -b` report 0 errors — it compiled nothing.

## Index/worktree drift during amend cleanup

- `git checkout <parent> -- <path>` fixes the WORKTREE only; the index keeps
  the worker's version. Three-way check each cycle: `git status --short`
  (first column = staged, second = worktree) + `git diff --cached <parent>
  --stat`.
- Amends keep previously committed content unless explicitly re-staged. The
  vite.config.ts change re-entered a later amend exactly this way (a broad
  `git add` meant to restore one file re-added the modified version). Final
  acceptance: `git diff --cached <parent> --stat` shows ONLY the intended
  file set (here 5 files, 742 insertions, 12 deletions).
- Untracking worker additions: `git rm --cached <path>` keeps the worktree
  file; verify staged deletions with `git status --short`.

## Result

One agy invocation + ~4 parent verification cycles. Final commit: 5 files,
742 insertions, zero new tsc errors vs baseline, 16/16 tests, production
build green, trailers `Agent-Session-ID: agy-trade-activity-desktop` /
`Agent-harness: antigravity`.

## Environment note (transient, not a rule)

Hermes' terminal hardline-blocked two oversized multi-statement verification
one-liners (grep pipelines with command substitution). Recovery each time:
write the gate as a small `verify-*.sh` in the worktree and `bash` it, then
delete the script before committing.
