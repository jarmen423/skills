---
name: checklist-ledger
description: Collaborate on a hosted checklist/to-do list with your user through the `checklist` CLI. Use when the user mentions their "checklist", "to-do list", "ledger", items to add/finish/move, or asks for help tracking tasks. The CLI is the only supported way to mutate the data — do not edit D1 or call the Worker API directly.
---

# checklist-ledger

The user has a single-user hosted checklist app (Cloudflare Worker + D1 + Vite
React UI). It is designed to be driven by agents. You and the user share the
same list — when you add, finish, or move items, the user sees them in the
browser, and vice versa.

The supported way to mutate the list is the `checklist` CLI. The CLI talks
to the Worker's token-protected API; both the browser UI and the CLI go
through the same auth, so you and the user are operating on one source of
truth.

## When to use this skill

- The user mentions "my checklist", "to-do list", "ledger", or any task they
  want tracked across sessions.
- The user asks "what's on my list?" or "what did we finish?".
- The user says "add X to the list", "mark Y done", "move Z up", "remind me
  to ...".
- You are starting a multi-step task and want to leave breadcrumbs the user
  can see, or you want to check whether the user already has an item for what
  you are about to do.
- You are doing work on the user's behalf that maps to discrete deliverables
  — file an item, do the work, mark it done.

When NOT to use this skill:

- The user is asking about a one-off task that doesn't need to persist across
  sessions. Use your normal scratchpad.
- The user is asking how to use the CLI themselves. Point them at
  `docs/CLI.md` in the repo.
- You need to inspect raw database rows. That's outside the supported
  contract; use the CLI.

## First-run: discover the user's setup

Before any `checklist` command, find out whether the CLI is installed and
where the user's config lives. Do NOT assume any specific path, URL, or
ledger name.

### 1. Is the CLI installed?

```
command -v checklist || which checklist
```

If it returns a path, you're good — skip to step 3.

If it's missing, tell the user:

> The `checklist` CLI isn't installed on this machine. To install it, you
> need to either publish the package from the repo
> (`npm version patch && npm publish`) and then run
> `npm install -g checklist-ledger`, or install from a local checkout with
> `npm install -g <path-to-repo>`. The full setup is in `docs/CLI.md`.

Stop here. Do not try to run checklist commands without the binary.

### 2. Has the user configured it?

The CLI looks for config in two places (env vars first, then a JSON file):

- `CHECKLIST_API_URL`, `CHECKLIST_ADMIN_TOKEN`, `CHECKLIST_LEDGER_ID`
  environment variables.
- `~/.checklist-ledger.json` (resolves via `os.homedir()` — on Windows that
  is `%USERPROFILE%\.checklist-ledger.json`).

Check both. For the env vars, in your shell:

```
echo "URL=${CHECKLIST_API_URL:-unset}"
echo "TOKEN=${CHECKLIST_ADMIN_TOKEN:+set}${CHECKLIST_ADMIN_TOKEN:-unset}"
echo "LEDGER=${CHECKLIST_LEDGER_ID:-unset}"
```

For the file, read it:

```
cat ~/.checklist-ledger.json
```

If `apiUrl` and `adminToken` are set in either place, you're authenticated
and can proceed.

If they're missing entirely, you have two jobs:

1. Ask the user for their token (and the API URL if they don't use the
   public deployment).
2. Persist it for them:

```
checklist login --api-key <token> [--api-url <url>] [--ledger-id <id>]
```

`checklist login` is bootstrap-safe — it does NOT require an existing
config to run. It writes `~/.checklist-ledger.json` (mode 0600 on POSIX,
best-effort on Windows). Re-running with a new token merges with the
existing file and preserves `defaultLedgerId` if you don't pass
`--ledger-id`.

After login, verify with step 3.

### 3. Verify auth actually works

The config file may be stale (the user rotated the Worker secret and forgot
to update their local config). The only way to know is to call the API:

```
checklist ledgers
```

- If you get a list of ledgers → you're authenticated, proceed.
- If you get `Missing or invalid checklist admin token.` (401) → the
  Worker's `ADMIN_TOKEN` secret rotated and your local config is stale. Tell
  the user; do NOT guess or retry with old values. The fix is
  `wrangler secret put ADMIN_TOKEN` on a machine with wrangler
  authenticated, then `checklist login --api-key <new-token>` on every
  client (including this one).
- If you get `Set CHECKLIST_API_URL and CHECKLIST_ADMIN_TOKEN, or create
  ~/.checklist-ledger.json.` → config is missing entirely, go back to
  step 2.

## Discover the user's ledgers

Do not hardcode ledger names or ids. Find them:

```
checklist ledgers
checklist ledgers --all    # include archived
```

The output shows id, name, and status (active/archived). The CLI also
accepts ledger names anywhere it accepts ids — but ids are unambiguous and
faster, so prefer them once you've discovered them. Cache the mapping for
the rest of the session; you can re-run `checklist ledgers` if you suspect
it changed.

If the user mentions a ledger by name ("the Work ledger", "add to Today")
and you don't see it in `checklist ledgers`, ask before creating a new one
— creating a duplicate ledger is annoying for the user to clean up.

## The four operations agents actually use

You will spend 95% of your checklist work in these commands. The full
reference is `checklist help`.

### 1. See what's there

```
checklist list                          # active items in default ledger
checklist list --ledger "<name-or-id>"
checklist list full                     # include details and timestamps
checklist list 1-10                     # a positional range by display order
checklist finished                      # recently finished items
checklist find "auth bug"               # substring search over titles
```

`checklist list` is the first thing to run when a session starts and the
user has mentioned prior work — it tells you what's already in flight and
what they've been thinking about. Run it before adding new items so you
don't duplicate.

### 2. Add items

```
checklist add "Write deployment notes" \
  --details "Add D1 setup and custom domain steps." \
  --ledger "<name-or-id>"
checklist child <parent-id-or-title> "Create the production D1 database"
```

`checklist add` always creates a top-level item at the bottom of the
ledger. `checklist child <parent> "<title>"` adds a sub-item under an
existing item, matched by id or title substring. Use `--details` for
anything longer than a sentence; the user's UI shows details in an
expandable panel.

Decision rule for "is this a child or a new top-level item?":

- If it is a sub-step of an item already on the list → child.
- If it is its own deliverable the user will look at independently →
  top-level.
- When in doubt, ask. Duplicates are easy to merge with `checklist move`
  and `done`, but the user gets grumpy when their list fills with junk.

### 3. Update / mark done / reopen

```
checklist update <id-or-title> --title "..." --details "..."
checklist done <id-or-title>
checklist reopen <id-or-title>
checklist move <id-or-title> --before <other-id-or-title>
checklist move <id-or-title> --after <other-id-or-title>
```

`checklist done` is the only way to "complete" an item. Don't delete items
unless the user explicitly asks — `checklist list` is more useful when
the finished history is preserved.

### 4. Inspect

```
checklist details <id-or-title>
```

`checklist details` returns the children list, which is how you discover
sub-tasks you didn't know existed.

## Coordination protocol — how to act well with the user

This is the part the README doesn't say and you have to internalize:

1. **Pull before you push.** Before adding anything, run `checklist list`
   (or `checklist find`) to see if the user already has an item for what
   you are about to do. If a match exists within ~80% title similarity,
   reuse it (update the details / add a child) instead of creating a
   duplicate. Duplicates are how you lose the user's trust in this tool.

2. **Match the user's granularity.** If their existing items are
   coarse-grained ("Ship the deploy script"), yours should be too. If
   theirs are fine-grained ("Add D1 binding", "Add custom domain", "Add
   deploy workflow"), match that. Look at 3-5 existing items in the same
   ledger before adding yours.

3. **Stay in the same ledger.** When the user names a ledger explicitly,
   use that one. When they say nothing, use the default ledger (whatever
   `--ledger-id` or `CHECKLIST_LEDGER_ID` resolves to). Don't create new
   ledgers without asking.

4. **Update, don't re-add.** When scope changes on an item you previously
   added, prefer `checklist update --title / --details` over creating a
   new item and finishing the old one. Position in the list conveys
   "this is still the same work".

5. **Mark done as soon as the work is done.** Don't let items pile up in
   `active` after you've finished them — that breaks the user's mental
   model of "active = I need to look at this".

6. **Never edit D1 or call the Worker API directly.** This is the single
   biggest invariant of the project. Mutations must go through the CLI so
   the auth, ordering, and timestamp logic all run through one path. If
   the CLI can't do what you need, that's a CLI bug — fix it in the repo,
   don't work around it by writing SQL.

7. **When the user is mid-conversation and asks for a small thing** ("add
   'review PR' to my list"), do it in one command without ceremony. No
   need to dump the full list first unless you're unsure whether the
   item exists.

## Failure modes you must handle

- **401 invalid token** — the Worker secret rotated and your config is
  stale. Stop, tell the user, do not retry. They need to run
  `wrangler secret put ADMIN_TOKEN` and then `checklist login` on every
  machine.
- **Item-not-found** — your id or title substring didn't match anything
  in the chosen ledger. Run `checklist list --ledger <name>` to see what's
  there and pick the right ref. Don't guess ids.
- **Wrong ledger** — you added something to one ledger when the user
  meant another. There is no cross-ledger move. Finish the wrong item and
  re-add to the right ledger. If the user wants cross-ledger moves,
  that's a feature request for the repo.
- **Env var overriding the file** — if `CHECKLIST_ADMIN_TOKEN` is set in
  the shell, it persists across commands and will mask the file's value
  even after you update the file. Unset it (`unset CHECKLIST_ADMIN_TOKEN`
  or `Remove-Item Env:\CHECKLIST_ADMIN_TOKEN`) before relying on the file.
- **Wrong default ledger** — `CHECKLIST_LEDGER_ID` or the
  `defaultLedgerId` in the config file may point at a ledger you don't
  expect. If `checklist list` returns items the user didn't mention, run
  `checklist ledgers` and pass `--ledger <id>` explicitly on every command
  until the user fixes the default.

## Verification

After writing any item, verify with:

```
checklist details <id-or-title>
```

That returns the item with its children, details, and timestamps — enough
to confirm the write landed.

## See also

- `docs/CLI.md` — full command reference for humans.
- `README.md` — setup and deployment (D1, Cloudflare, GitHub Actions).
- `src/worker/http.ts` — auth check (bearer-token string equality).
- `src/cli/index.ts` — config loader (env var → file fallback) and
  `handleLogin` (bootstrap-safe writer).