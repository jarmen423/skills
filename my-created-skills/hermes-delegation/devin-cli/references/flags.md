# Devin CLI — verified flag surface (3000.10.31, b98cc431)

Verified from the installed binary's own `--help` output, 2026-09-22. Re-read
`devin --help` after any version change; this is a record, not a dump of every
flag, and the docs lag the binary (see errata at the bottom).

## Invocation

```
devin [OPTIONS] [PATH]... [-- <PROMPT>...] [COMMAND]
```

- `[PATH]...` positionals open **Devin Desktop** on those paths.
- `[-- <PROMPT>...]` after `--` is the initial message (REPL).
- `-p` is the non-interactive print mode — the delegation path.

## Global flags (verified accepts)

| Flag | Env | Notes |
| --- | --- | --- |
| `--prompt-file <FILE>` | | Load the initial prompt from a file. Read verified: missing file → `Error: Failed to read prompt file "...": No such file or directory (os error 2)` |
| `--config <PATH>` | | Override the default user config file (`~/.config/devin/config.json`) |
| `--permission-mode <MODE>` | `DEVIN_PERMISSION_MODE` | Default `auto`. Alias map below |
| `--sandbox` | `DEVIN_SANDBOX` | Research Preview. Linux needs `bwrap` + `socat`; fail-closed |
| `--model <MODEL>` | `DEVIN_MODEL` | E.g. `opus`, `codex`, full family names. With `-c`/`-r` switches the resumed conversation's model |
| `-p, --print [PROMPT]` | | Print response and exit (non-interactive) |
| `--export [PATH]` | | Export conversation after each turn (ATIF format). Value-less form uses an unspecified default path |
| `-c, --continue` | | Resume the most recent session in the current directory |
| `-r, --resume [SESSION_ID]` | | Resume a specific session; omit = interactive picker |
| `--respect-workspace-trust [true\|false]` | | Default `true`. `false` required in scripts: non-interactive cannot show the trust prompt and fails in an untrusted directory |
| `-h, --help` / `-V, --version` | | `devin version` ≡ `--version` |

Verified REJECTS (exit `2`, `error: unexpected argument`): `--json`,
`--max-turns`. There is no machine-readable output mode and no turn/step cap
flag. Usage errors exit `2` (verified).

## Permission-mode alias map

| Value | Aliases | Behavior (from `--help`) |
| --- | --- | --- |
| `auto` | `normal` (default) | Read-only auto; writes and shell prompt |
| `accept-edits` | | Workspace edits auto; shell still prompts |
| `smart` | | accept-edits + a fast model auto-runs actions it judges safe |
| `dangerous` | `yolo`, `bypass` | Everything auto. The headless choice |
| `autonomous` | | Per docs requires `--sandbox`, sandbox sessions only |

Parse-verified: `smart` and `autonomous` are both accepted by the parser. The
invalid-value error's own list omits `smart` — see errata.

## Subcommands (from `devin --help`)

| Command | Notes |
| --- | --- |
| `auth` | `login [--force-manual-token-flow]`, `logout`, `status` |
| `mcp` | `add [-t stdio\|http] [-s local\|project\|user] [--url\|--command] [-e K=V] [-H header] [--scopes] [--oauth-resource]`, `list`, `get`, `remove`, `login`, `logout`, `enable`, `disable` |
| `models list` | Account model families, aliases, per-tier pricing (49 families on this account: claude-opus-5, claude-fable-5.1, claude-sonnet-5, ...) |
| `doctor` | Config diagnostic (reported 3 custom subagent profiles: `swe17-coder`, `swe17-general`, `swe17-researcher`) |
| `rules` | `list [--provider cursor\|windsurf]`, `show <name>`, `paths` — always-on context blobs |
| `skills` | `list [--trigger user\|model]`, `show`, `paths` — slash commands + context blobs; reads `~/.agents/skills` and `~/.hermes/skills` |
| `plugins` | `install`, `list`, `info`, `update`, `remove`, `prune` |
| `cloud drs` | Declarative Repo Setup: environment blueprints, sandbox sessions, builds |
| `desktop` | Open Devin Desktop |
| `list` / `ls` | Sessions in the current directory. `--format json` / `--format csv` for scripts; bare = interactive picker |
| `rm <id\|name>` | Delete a session irreversibly |
| `ssh` | SSH into a cloud Devin session's box |
| `forward` | Forward ports from a cloud Devin session's box |
| `update [--force]` | Self-update |
| `version` | Same as `--version` |
| `migrate` | Migrate configuration from other tools |
| `sandbox setup` | Print sandbox prerequisites (the only `sandbox` subcommand) |
| `setup [--force-manual-token-flow]` | Interactive setup wizard |
| `uninstall [--clean --force]` | Uninstall; `--clean` removes all data |
| `acp` | ACP server over stdio. `--agent-type summarizer\|review`, `--model`, `--refusal-fallback <MODELS>` |
| `shell` | DEPRECATED hidden stub — see errata |

ACP notes: `devin` and `devin -p` run their agent in a spawned `devin acp`
child; `DEVIN_REFUSAL_FALLBACK` (comma-separated models) is the env that
reaches that child for `devin` and `devin -p`. The `summarizer` agent type
persists its output to `~/.local/share/devin/summaries/<session_id>.md`.

## Interactive-only (no headless equivalent)

REPL slash commands: `/mode`, `/normal`, `/accept-edits`, `/smart`, `/plan`,
`/ask <q>`, `/bypass` (`/yolo`, `/dangerous`), `/autonomous`, `/model`,
`/fast`, `/theme`, `/clear` (`/new`), `/continue`, `/fork`, `/steps`,
`/revert`, `/resume`, `/ls`, `/rename-session`, `/title`, `/rm-session`,
`/export`, `/workspace`, `/add-dir`, `/undo-add-dir`, `/loop`, `/btw <q>`,
`/hooks`, `/help`, `/shortcuts`, `/bug`, `/update`, `/upgrade`, `/login`,
`/logout`, `/context`, `/usage`, `/compact`, `/cloud-sessions`, `/handoff`.
Also interactive-only: `-r` with no id, bare `devin list`, `devin setup`.
`/handoff` transfers the local session to cloud Devin (→ `devin-handoff`).

## Doc errata (three doc surfaces vs the binary)

1. **Permission modes**: docs.devin.ai says `normal, dangerous, bypass`. The
   binary's invalid-value error says `normal (auto), accept-edits, dangerous
   (yolo, bypass), autonomous (requires --sandbox)` and omits `smart` — while
   the long help omits `autonomous` and includes `smart`. The alias map above
   is the working union.
2. **`devin shell setup`** is documented as [Feature Preview]; in 3000.10.31
   shell integration is REMOVED. `devin shell` is a hidden stub: "shell
   integration has been removed; kept as a hidden compatibility stub so stale
   rc-file hooks stay silent and can be cleaned up via `shell remove`".
   `devin shell setup` errors `unrecognized subcommand 'setup'`.
3. **Undocumented subcommands** on the docs.devin.ai commands page, all
   verified present: `models`, `doctor`, `plugins`, `cloud`, `desktop`, `rm`,
   `ssh`, `forward`, `migrate`.
4. **`--respect-workspace-trust`** takes an optional `true|false` value; docs
   show it valueless.
5. **Env vars** in the binary's help (`DEVIN_PERMISSION_MODE`, `DEVIN_SANDBOX`,
   `DEVIN_MODEL`, `DEVIN_REFUSAL_FALLBACK`) are missing from the docs flag
   table.
6. **`man devin`** is referenced by docs but absent on minimized Ubuntu
   systems.
