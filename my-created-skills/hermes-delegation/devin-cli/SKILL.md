---
name: devin-cli
description: "Delegate coding to Devin CLI (headless, sessions)."
version: 0.1.0
author: Josh Friedman (jarmen423), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Coding-Agent, Devin, Cognition, Headless, Sessions, Worktree]
    related_skills: [coding-agent-supervision, devin-handoff, devin-thread-distillation, muse-code-cli, grok-build-cli, codex, opencode, antigravity-cli]
---

# Devin CLI

Delegate bounded coding work to Cognition's local Devin CLI (`devin`) through
the Hermes `terminal` tool. Prefer non-interactive `-p` (print) mode. The
interactive REPL is only for a human multi-turn session.

Load `coding-agent-supervision` for liveness, recovery, and review gates. This
skill is the Devin-LOCAL surface. Cloud sessions with their own VM, browser,
and CI are `devin-handoff` (the REPL's `/handoff` also transfers there); mining
past local threads is `devin-thread-distillation`. Re-read `devin --help` after
`devin --version` changes; three doc surfaces disagree with the binary.

Verified against `devin 3000.10.31 (b98cc431)`.

## When to Use

- Implement, fix, refactor, or review code with local Devin.
- Resume a retained Devin session without opening the REPL.
- Run Devin in an isolated git worktree.

Do not use for: cloud Devin sessions (VM, browser, CI, PR delivery) — that is
`devin-handoff`; driving the REPL when `devin -p` can finish and exit; any
credit-consuming run before the user confirms it (see Prerequisites 3).

## Prerequisites

1. `terminal(command="command -v devin && devin --version")`. PATH `devin` is a
   symlink into `~/.local/share/devin/cli/_versions/current/bin/devin` (Rust
   ELF). Trust `devin --version`.
2. Auth without printing secrets: `terminal(command="devin auth status")`
   prints login state, the credentials FILE path, endpoints, and the account
   name — never contents. `~/.local/share/devin/credentials.toml` is the secret
   store; never `cat` it and never pass a token as an argument. `devin auth
   login` is a browser flow; `--force-manual-token-flow` is the remote/SSH
   path. `devin auth logout` clears stored credentials.
3. Every `-p` run spends Devin credits/ACU. `devin models list` shows the
   account's model families with per-tier pricing. Obey the paid-API spending
   gate: the user confirms the first paid run of a session, then run one tiny
   exact-response smoke before a long task.
4. Set Hermes `workdir` to the exact repo or worktree. Sessions are
   directory-scoped (`devin list`, `-c`).

Install, if missing: `curl -fsSL https://cli.devin.ai/install.sh | bash`.
`devin update [--force]` self-updates; re-check flags after the version moves.

## Preferred Mode: Bounded Headless Runs

`devin` with no flags starts the REPL, `devin -- <prompt>` starts the REPL with
an initial message, and bare `devin <PATH>` positionals open Devin Desktop —
never pass paths as positionals. Automation always uses `-p`.

Write the brief with `write_file`, then:

```text
terminal(
  command="devin -p --prompt-file /absolute/path/brief.md --permission-mode dangerous --respect-workspace-trust false --export /absolute/path/run.atif.json",
  workdir="/path/to/isolated-worktree",
  background=true,
  notify_on_complete=true,
  timeout=1200,
)
```

`--prompt-file` loads the initial prompt from a file. Verified: the file is
read (a missing one aborts with `Error: Failed to read prompt file
"...": No such file or directory (os error 2)`). Prefer it over `-p "inline"`
for anything beyond a smoke: no shell quoting, no ARG_MAX truncation.

`--permission-mode dangerous` (aliases `yolo`, `bypass`) auto-approves every
tool. It is the headless analog of Muse's `--disable-approval`: in `-p` mode
there is nobody to answer a prompt. Use it ONLY in an isolated worktree with a
fenced brief. Never on a shared or production checkout.

`--respect-workspace-trust false` is mandatory for scripts. Non-interactive
cannot show the trust prompt and fails in an untrusted directory — and a fresh
worktree usually is one.

`--export <PATH>` writes the conversation after each turn (ATIF format). Pass
an explicit path; the flag's value-less default path is unspecified.

There is no `--json` and no `--max-turns` (both verified rejects: `error:
unexpected argument`). `-p` prints prose to stdout and exits. Bound the run
with the prompt contract below plus the outer Hermes `timeout`; write an
incremental result file after each coherent change so a timeout keeps the
findings.

### Prompt contract

The brief is the whole task. Include:

- work only in the current directory; do not follow absolute paths into any
  other checkout, especially a production or deploy clone
- branch name, allowed edits, and the exact test command
- commit policy: Devin does not commit unless the brief asks; the parent still
  reviews the diff before integrating
- no push, no secrets in the transcript, no edits outside this worktree
- if a question would be needed, pick the conservative option and record it
- stop when the named acceptance criteria are met and verified, not when the
  narration feels done

### Permission modes (alias map)

- `{auto|normal}` (default) — read-only auto; writes and shell prompt.
- `accept-edits` — workspace edits auto; shell still prompts.
- `smart` — accept-edits plus a fast model auto-runs actions it judges safe.
- `{dangerous|yolo|bypass}` — everything auto. The headless default.
- `autonomous` — per docs requires `--sandbox` and exists only in sandbox
  sessions.

Under `-p`, assume any needed prompt fails or hangs (unverified) and the outer
timeout is the backstop — so unattended runs get `dangerous` in a worktree.

### Sandbox (Research Preview)

`--sandbox` confines exec-tool processes (macOS Seatbelt; Linux
bubblewrap+seccomp). Linux needs `bwrap` AND `socat`, and resolution failure is
fail-closed: the session refuses to start rather than running unsandboxed.
`devin sandbox setup` prints the prerequisites. On this VM expect a hard fail:
`bwrap` exists but unprivileged user namespaces are denied (`uid map:
Permission denied`) and `socat` is missing.

When the sandbox cannot run, fall back to `dangerous` inside an isolated
worktree — the worktree plus the fenced brief is the boundary. Sandbox config
(`sandbox.allowed_domains`, `denied_domains`, `network_mode`, and
`sandbox.excluded` Exec rules) lives in `~/.config/devin/config.json`; details
in `references/flags.md`.

### Read the result

Exit code `2` is a usage error (verified). The success/failure exit code of
`-p` is not verified here — do not gate on it. `-p` prose is a report, not
proof; there is no JSONL stream to parse. The durable record is the `--export`
ATIF file plus the diff. Verify the diff and rerun the tests yourself.

Session-handle capture and the sessions DB: `references/sessions-and-state.md`.

## Resume Without the REPL

`-r` with no id and bare `devin list` open interactive pickers. Headless:

```text
terminal(command="devin list --format json", workdir="/path/to/worktree")
# ... launch, then diff the list to capture the new session id ...
terminal(
  command="devin -p -r <SESSION_ID> --prompt-file /absolute/path/continue.md --permission-mode dangerous --respect-workspace-trust false",
  workdir="/path/to/same-worktree",
  background=true,
  notify_on_complete=true,
)
```

- Capture the id by diffing `devin list --format json` (or `--format csv`,
  which also carries `short_id`) in the launch directory before and after the
  run. IDs are memorable two-word slugs (e.g. `checkered-desert`), not UUIDs,
  and `-p` stdout does not reliably print one.
- `-c` continues the most recent session in the current directory.
- `--model` combined with `-c`/`-r` switches the resumed conversation's model.
- `devin rm <id|name>` deletes a session irreversibly.
- Resume from the same directory: sessions are directory-scoped.

Export for your own audit, not for chat paste: the ATIF file can contain tool
output and task text.

## Worktree Isolation

Hermes creates the worktree; Devin runs inside it. There is no Devin-owned
worktree flag to lean on.

```text
terminal(command="git worktree add -b fix/topic /absolute/path/topic <base>", workdir="/path/to/repo")
terminal(command="devin -p --prompt-file /absolute/path/brief.md --permission-mode dangerous --respect-workspace-trust false --export /absolute/path/run.atif.json", workdir="/absolute/path/topic", background=true, notify_on_complete=true)
```

Never give Devin absolute paths into a protected checkout. Sessions bind to
the launch directory: confirm `pwd` is the worktree before launching.

## Interactive REPL

Only when a human needs a persistent session. Requires a PTY.

```text
terminal(command="tmux new-session -d -s devin-work -x 140 -y 40")
terminal(command="tmux send-keys -t devin-work 'cd /path/to/repo && devin' Enter")
terminal(command="tmux capture-pane -t devin-work -p -S -100")
```

Slash commands (`/mode`, `/loop`, `/btw`, `/fork`, `/revert`, `/usage`,
`/compact`, `/handoff`) exist only inside that REPL. `/handoff` packages the
conversation plus git branch and transfers to cloud Devin — track that under
`devin-handoff`. `devin setup` is an interactive wizard. Do not drive either
from `terminal`.

## Procedure

1. **Confirm the binary and auth presence.** `devin --version` succeeds and
   `devin auth status` says logged in, without printing secrets.
2. **Fence the checkout.** Isolated worktree for edits. Production clone is
   off limits.
3. **Note existing session ids** in the worktree (`devin list --format json`).
4. **Write a self-contained brief** and launch the incantation above with
   Hermes `timeout` and `notify_on_complete=true`.
5. **Capture the session id** from the list diff while the run is retained.
6. **Judge artifacts, not exit codes.** Read the diff, rerun tests, run
   `git diff --check`. Resume the same session once if the run was plan-only
   or cut short. Then stop spending turns.

Completion means the requested files exist and independent verification passed.

## Pitfalls

- `devin <PATH>` opens Devin Desktop. Prompt positionals need `--` (`devin --
  fix the bug`); automation is `-p` + `--prompt-file`.
- No `--json`, no `--max-turns` (verified rejects). Bound with the brief and
  the outer timeout; `--export` is the record.
- `-p` cannot show the workspace-trust prompt: pass `--respect-workspace-trust
  false` or the run fails in an untrusted directory.
- Mode aliases disagree across surfaces: the invalid-value error lists
  `normal (auto), accept-edits, dangerous (yolo, bypass), autonomous (requires
  --sandbox)` and OMITS `smart` — yet `--permission-mode smart` parses.
  docs.devin.ai lists only `normal, dangerous, bypass`. Trust the alias map
  above.
- `devin shell` is a removed feature kept as a hidden stub: "shell integration
  has been removed" and `devin shell setup` errors `unrecognized subcommand
  'setup'`. Docs still advertise it; the stub text points at `shell remove`
  for stale rc-file hook cleanup.
- What `-p` does when a prompting mode needs approval is unverified — don't
  design around it; use `dangerous` in a worktree.
- `--export` without a path uses an unspecified default; always pass one.
- `devin rm` is irreversible, and hidden sessions (`sessions.hidden`) exist.
- Every run spends credits/ACU (the REPL's `/usage` shows the meter). User
  confirms paid runs; smoke first after fresh auth.
- `~/.local/share/devin/credentials.toml` is the secret store. Never read it.
- Exit 0 and fluent prose are not verified work — apply the artifact gate from
  `coding-agent-supervision`.
- Three doc surfaces (docs.devin.ai, docs.devinenterprise.com, cognitionai
  mintlify) disagree with each other and with the binary;
  `references/flags.md` records the 3000.10.31 truth. `man devin` may be
  absent on minimized systems.
- The sessions DB shows `backend_type='windsurf'` — the Codeium/Windsurf
  heritage stack behind Devin. Not a different tool.

## Verification

Free checks (no credits spent): `devin --version`, `devin auth status`,
`devin doctor`, `devin list --format json`, `devin models list`, and a
parse-level probe with an invalid `--permission-mode` (exits `2` at parse
time, before any file or network access).

Paid smoke (spends credits — user approval first), in a throwaway git dir:

```text
terminal(command="devin -p --permission-mode dangerous --respect-workspace-trust false \"Reply with exactly DEVIN_ECHO_OK and do not use tools.\"", workdir="/absolute/path/throwaway-git-dir")
```

Success for a real delegation:

- `devin --version` matches the help you followed.
- `pwd` was the intended worktree at launch; sessions stayed directory-scoped.
- Session id was captured from the list diff, and resume used `-r <id>` from
  the same directory.
- Permission mode and trust flag matched the side-effect scope actually
  needed.
- Changed files are accounted for; required tests and `git diff --check` pass
  under the parent, not only inside Devin's prose.
- No token, `credentials.toml` content, or raw export landed in the transcript.

## References

- `references/flags.md` — flags and subcommands verified from `devin --help`,
  alias map, doc errata.
- `references/sessions-and-state.md` — sessions DB schema, id capture, config
  and data paths.
- Docs: https://docs.devin.ai/cli/reference/commands (lags the binary)