# Muse Code flags

Re-read `muse exec --help` after any version change. This page records the
surface that mattered for Hermes delegation. It is not a dump of every flag.

## Launcher vs binary

`command -v muse` may be a bash updater. It execs a versioned `muse-bin-*`
beside itself and can self-update from the `muse-stable` channel
(`MUSE_UPDATE_INTERVAL_SECONDS`, default 3600). Invoke `muse`, not `muse-bin-*`,
unless you are debugging the launcher. Supported platforms in the launcher:
macOS arm64/x86_64 and Linux arm64/x86_64.

## Headless command

```text
muse exec [OPTIONS] [PROMPT]
muse exec --prompt-file <PATH> [OPTIONS]
```

Use `--prompt-file` when the brief contains quotes. Write that file with the
Hermes `write_file` tool.

Delegation flags:

| Flag | Use |
| --- | --- |
| `--trust-workspace` | Load this checkout's skills and rules for this run. Does not save trust. |
| `--disable-approval` | No approval prompts. Sandbox stays on. |
| `--approval-mode untrusted\|on-request\|never` | `on-request` is the default and can hang headless. `never` skips prompts and keeps the sandbox. |
| `--disable-sandbox` | Last resort when bubblewrap user namespaces fail. Also unconfines file tools and forces full network. Isolated worktree only. |
| `--sandbox-network restricted\|enabled\|proxy-only` | Default `proxy-only` holds on a new host. Headless cannot approve that hold. |
| `--yolo` | Disables approval and sandbox and trusts the workspace. Not for a shared or production checkout. |
| `--user-input-auto-resolve` | Auto-cancel clarifying questions. Required for unattended runs. |
| `--json` | JSONL events on stdout. |
| `--max-model-steps <N>` | Step cap. Exit 1 when hit. |
| `--session-id <UUID>` | Continue that retained session. Not a substitute for `muse resume`. |
| `--allow-workspace-switch` | Only when you intentionally continue a session from another workspace. |
| `--model <ID>` | Override settings.json. |
| `--reasoning-effort none\|minimal\|low\|medium\|high\|xhigh\|max\|ultra` | Binary default `high`. Settings can override. |
| `--output-schema <FILE>` | Shape the final answer (meta provider). |
| `--no-foreign-personal-context` | Drop foreign personal rules and skills for this run. |
| `--no-session-log` | No retained resume or export. Do not use for work you may continue. |
| `--image <PATH>` | Attach a local image. Repeatable. |
| `--workspace <PATH>` | Root policy-gated workspace tools at PATH. Prefer Hermes `workdir`. |
| `-w` / `--worktree off\|create\|existing` | Muse-owned worktree. Prefer a Hermes `git worktree add`. |

`--provider echo` is a free harness smoke. Real work uses the default `meta`
provider. Do not set `--base-url` unless the user named an endpoint.

## Interactive-only

`muse` with no subcommand, `muse resume`, and `muse resume --last` open the
TUI. Root flags such as `--model` and `--workspace` may sit on either side of
`resume`. Slash commands are not shell commands.

## Commands that are easy to misuse

- `muse export --session <id|path> --out <file> --redacted` — offline, local
  files only. Without `--out` or `--session`, a non-interactive export writes
  the most recent session for the current workspace and prints the path.
- `muse trace inspect --session-log <jsonl> --render-mode compact|default|verbose --format text|json`
- `muse session-message list --json` and `muse session-message send --target <uuid-or-name>`
  with the body on stdin. Live interactive peers only.
- `muse skills list --source project --workspace <path> --trust-workspace --json`
- `muse auth set --api-key-stdin` — key on stdin, never on the command line.
- `muse logout` clears stored credentials. It does not unset `META_API_KEY`.
- `muse init` writes `AGENTS.md` and stops if it exists. `--force` overwrites
  it completely. `--dry-run` changes nothing.
- `muse workflows` is real but omitted from `muse --help`. Do not use
  `workflows run` or `workflows recover` as the Hermes delegation path; the
  help text marks them as a QA lane.

## Docs that were stale against the binary

When docs and `muse exec --help` disagree, follow the help:

- `--approval-mode` and `--no-session-log` exist on `muse exec`, not only on
  the TUI.
- Reasoning effort values on the binary include `none` and `max`. The binary
  default is `high`.
- `muse sandbox` does not check the Linux bubblewrap sandbox.
