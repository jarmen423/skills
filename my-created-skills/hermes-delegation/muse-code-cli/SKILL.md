---
name: muse-code-cli
description: "Delegate coding to Muse Code CLI (headless, sessions)."
version: 0.1.0
author: Josh Friedman (jarmen423), Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Coding-Agent, Muse, Meta, Headless, Sessions, Worktree]
    related_skills: [grok-build-cli, codex, opencode, antigravity-cli, coding-agent-supervision]
---

# Muse Code CLI

Delegate bounded coding work to Meta Muse Code (`muse`) through the Hermes
`terminal` tool. Prefer `muse exec` for automation. The interactive TUI is only
for a human multi-turn session.

Load `coding-agent-supervision` for liveness, recovery, and review gates. This
skill is the Muse-specific surface. Re-read `muse exec --help` after
`muse --version` changes; the public docs lag the binary.

## When to Use

- Implement, fix, refactor, or review code with Muse Code.
- Resume a retained Muse session without opening the TUI.
- Run Muse in an isolated git worktree.

Do not use for: driving the TUI when `muse exec` can finish and exit; Muse's
internal workflows as a Hermes orchestration layer; spending a paid model call
before the user confirms a paid-API run.

## Prerequisites

1. `terminal(command="command -v muse && muse --version")`. PATH `muse` may be
   the bash launcher in `~/.local/bin/muse`, not the versioned `muse-bin-*`.
   Trust `muse --version`.
2. Auth without printing secrets. `META_API_KEY`, if set, beats a stored
   browser login. Check presence only:
   `terminal(command="[ -n \"${META_API_KEY:-}\" ] && echo env_key=yes || echo env_key=no; [ -s \"${XDG_CONFIG_HOME:-$HOME/.config}/muse/auth.json\" ] && echo stored_auth=yes || echo stored_auth=no")`.
   Never `cat` `auth.json` or pass a key as an argument. Store a key with
   `muse auth set --api-key-stdin`. `muse login` is a browser device flow and
   is not a headless auth path.
3. Read `~/.config/muse/settings.json` keys `model` and `reasoning_effort`
   with `read_file` before a paid run. Pass `--model` when the task must not
   inherit that pin. A missing settings file is fine; a present file must
   contain `"schema_version": 1` or every command fails at startup.
4. Set Hermes `workdir` to the exact repo or worktree. Sessions are
   workspace-scoped.

Install, if missing, is the upstream launcher:
`curl -fsSL https://dev.meta.ai/install.sh | sh`
(macOS and Linux only; the launcher rejects other platforms).

## Preferred Mode: Bounded Headless Runs

`muse "prompt"` without `exec` starts the TUI. Automation always uses `exec`.

Write the brief with `write_file`, then:

```text
terminal(
  command="muse exec --trust-workspace --disable-approval --user-input-auto-resolve --json --max-model-steps 40 --prompt-file /absolute/path/brief.md",
  workdir="/path/to/isolated-worktree",
  background=true,
  notify_on_complete=true,
  timeout=1200,
)
```

`--trust-workspace` loads this checkout's `AGENTS.md`, skills, and rules for
this run only. It does not save trust. An untrusted workspace disables Muse's
internal agent delegation and ignores project instructions.

`--disable-approval` skips approval prompts but keeps the sandbox. A headless
run has no UI, so the default `on-request` mode can hang forever on a held
shell stage or a new network host.

`--user-input-auto-resolve` auto-cancels clarifying questions. The brief must
say: decide and record assumptions; do not ask.

`--max-model-steps` is the turn cap. There is no `--max-turns`. Hitting the
cap exits 1. Resume the same session; do not start over.

`--json` emits JSONL on stdout. Diagnostics (`muse: ...`) go to stderr. In a
merged Hermes log, keep only lines that start with `{`.

Do not pass `--no-session-log` if you may need to resume. That flag disables
retained resume, export, and peer messaging.

Do not pass `--provider echo` for real work. Echo is a free harness smoke only.

### Prompt contract

The brief is the whole task. Include:

- work only in the current directory; do not follow absolute paths into any
  other checkout, especially a production or deploy clone
- branch name, allowed edits, and the exact test command
- commit policy: Muse does not commit unless the brief asks; the parent still
  reviews the diff before integrating
- no push, no secrets in the transcript, no edits outside this worktree
- if a question would be needed, pick the conservative option and write it down
- if the step cap may hit, write a short result file after each coherent change

### Sandbox fallback

Approval and the OS sandbox are on by default. Linux uses bubblewrap user
namespaces. If stderr says the sandbox needs user namespaces, or
`bwrap --unshare-user` fails with `setting up uid map: Permission denied`,
the sandbox cannot enforce. Shell commands then fail closed.

Only then, and only inside an isolated worktree, add `--disable-sandbox`.
That flag also removes file-tool confinement and forces full network egress.
The worktree plus the prompt fence is the safety boundary. Never use `--yolo`
on a shared or production checkout: it disables approval and the sandbox and
trusts the workspace, which loads that checkout's instructions.

If the sandbox works and the task needs outbound network, pass
`--sandbox-network enabled` inside the isolated worktree. The default
`proxy-only` holds on the first new host, and headless cannot approve it.

### Read the result

Exit 0 means the turn ended, not that the work is correct. Docs: `0`
completed, `1` failed, cancelled, or step-capped, `2` usage error, `130`/`143`
on SIGINT/SIGTERM.

From the JSONL, the session id is `stream.id` on events whose `stream.kind`
is `session`. The final answer is the event with
`payload_type` `run.terminal.completed`: `payload.terminal` and `payload.text`.
A completed terminal can still contain a failed child task. Verify the diff
and rerun the tests yourself. Parser and session queries:
`references/sessions-and-jsonl.md`.

## Resume Without the TUI

`muse resume` and `muse resume --last` open the interactive picker. They are
not headless.

Continue a retained run from the same workspace:

```text
terminal(
  command="muse exec --session-id <UUID> --trust-workspace --disable-approval --user-input-auto-resolve --json --max-model-steps 20 --prompt-file /absolute/path/continue.md",
  workdir="/path/to/same-worktree",
  background=true,
  notify_on_complete=true,
)
```

A workspace mismatch is refused unless you pass `--allow-workspace-switch`.
There is no `muse sessions list`. Query the local index; do not print
`first_user_prompt` or `search_text` (they can hold task text and secrets).

Export for your own audit, not for chat paste:

```text
terminal(command="muse export --session <UUID> --out /absolute/path/run.json --redacted", workdir="/path/to/same-worktree")
```

`--redacted` scrubs secret-shaped strings. Encrypted reasoning stays verbatim.
Default export is raw. `muse trace inspect --session-log <session.jsonl> --render-mode compact` is the readable trace.

## Worktree Isolation

Hermes creates the worktree; Muse runs inside it. Do not use bare `-w` as the
isolation plan: that creates a Muse-owned worktree whose path the parent does
not choose.

```text
terminal(command="git worktree add -b fix/topic /absolute/path/topic <base>", workdir="/path/to/repo")
terminal(command="muse exec --trust-workspace --disable-approval --user-input-auto-resolve --json --max-model-steps 40 --prompt-file /absolute/path/brief.md", workdir="/absolute/path/topic", background=true, notify_on_complete=true)
```

Never give Muse absolute paths into a protected checkout. After launch, confirm
the first JSONL `workspace_root` matches the worktree before letting it continue.

## Interactive TUI

Only when a human needs a persistent session. Requires a PTY.

```text
terminal(command="tmux new-session -d -s muse-work -x 140 -y 40")
terminal(command="tmux send-keys -t muse-work 'cd /path/to/repo && muse' Enter")
terminal(command="tmux capture-pane -t muse-work -p -S -100")
```

Slash commands (`/resume`, `/goal`, `/compact`, `/plan`) exist only inside that
TUI. `muse help` does not list them. Do not send `/exit`; interrupt with Esc
or kill the process.

## Procedure

1. **Confirm the binary and auth presence.** `muse --version` succeeds, and a
   key or stored auth exists, without printing either.
2. **Fence the checkout.** Isolated worktree for edits. Production clone is
   off limits.
3. **Probe the sandbox** if stderr warns about user namespaces. Fall back to
   `--disable-sandbox` only inside that worktree.
4. **Write a self-contained brief** and launch `muse exec` with the flags above,
   Hermes `timeout`, and `notify_on_complete=true`.
5. **Capture the session id** from the first session-stream JSONL event before
   the run ends.
6. **Judge artifacts, not the exit code.** Read the diff, rerun tests, run
   `git diff --check`. Resume the same `--session-id` once if the run was
   plan-only or step-capped. Then stop spending turns.

Completion means the requested files exist and independent verification passed.

## Pitfalls

- `muse PROMPT` and `muse resume` are TUI entry points. Headless is `muse exec`.
- Docs disagree with 1.3.0 help: `exec` accepts `--approval-mode` and
  `--no-session-log`; reasoning values include `none` through `ultra` (binary
  default `high`, overridable in settings). Trust `muse exec --help`.
- `muse sandbox` on Linux is not a health check. Only `muse sandbox windows
  check|setup` exists. Linux failure is the bubblewrap warning or a shell
  environment error.
- `muse workflows` is omitted from `muse --help`. `workflows run` and
  `recover` are a QA lane, not the delegation path.
- `muse init --force` overwrites `AGENTS.md`. Never run it in a repo that
  already has one.
- Default export is raw and can contain tool output. Use `--redacted`, and
  still do not paste it into chat.
- Peer messaging (`muse session-message`) reaches live interactive sessions
  only. It cannot approve tools or steer a headless exec. Continue with
  `--session-id` instead.
- A trimmed `skills_catalog` warning means Muse did not see every skill id.
  Malformed names under `~/.agents/skills` warn and do not fail the run.
  `--no-foreign-personal-context` drops foreign personal rules and skills for
  that run; confirm project skills still load with
  `muse skills list --source project --workspace <path> --trust-workspace --json`.
- The launcher self-updates from the `muse-stable` channel (default interval
  3600s). Re-check flags after the version changes.
- Exit 0 with a plan and no diff is not done.

## Verification

Free harness smoke (no model spend):

```text
terminal(command="muse exec --provider echo --json --no-session-log --max-model-steps 1 --disable-approval 'Reply with exactly MUSE_ECHO_OK'", workdir="/path/to/git-repo")
```

Success for a real delegation:

- `muse --version` matches the help you followed.
- JSONL `workspace_root` is the intended worktree.
- Session id was captured, and resume used that id from the same workspace.
- Approval and sandbox flags match the side-effect scope you actually needed.
- Changed files are accounted for; required tests and `git diff --check` pass
  under the parent, not only inside Muse's summary.
- No API key, `auth.json` contents, or raw export landed in the transcript.

## References

- `references/sessions-and-jsonl.md` — session index query, JSONL fields, export.
- `references/flags.md` — flags verified from `muse --help` / `muse exec --help`.
- Docs: https://dev.meta.ai/docs/muse-code.md
