---
name: grok-build-cli
description: "Operate Grok Build CLI via Hermes: headless, TUI, sessions."
version: 0.1.0
author: Josh Friedman (jarmen423), Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Coding-Agent, Grok, xAI, Headless, TUI, Sessions, Worktree]
    related_skills: [codex, opencode, hermes-agent]
---

# Grok Build CLI

Operate xAI Grok Build (`grok`) through Hermes `terminal` and `process`.
Prefer bounded headless runs for automation; use the interactive TUI only when
a human needs a persistent multi-turn surface.

## When to Use

- Delegate a feature, bug fix, refactor, or code review to Grok Build.
- Resume/export a prior Grok session without losing its context.
- Run independent work in an isolated git worktree.
- Diagnose typed-but-unsent prompts, stuck spinners, or stalled sessions.

Do not use the TUI for a bounded task that `grok -p` can finish and exit.

## Prerequisites

1. Verify the binary through Hermes:
   `terminal(command="command -v grok && grok --version")`.
2. Verify authentication with `grok inspect --json` or `grok doctor`.
3. Set the exact repository with Hermes `workdir`; sessions are workspace-scoped.
4. Read the repository's `AGENTS.md` before delegating edits.

Authentication is managed by `grok login` (subscription OAuth) or
`XAI_API_KEY`. Hermes `x_search` authentication does not authenticate this CLI.

## Preferred Mode: Bounded Headless Runs

Use `-p` for scriptable work. It needs no PTY and exits when the turn completes.

```text
terminal(
  command="grok -p '<self-contained task>' --model grok-4.6 --max-turns 30 --output-format json",
  workdir="/path/to/repo",
  background=true,
  notify_on_complete=true,
  timeout=1200,
)
```

Useful flags verified on Grok Build 1.0.5:

- `-p` / `--single`: one headless prompt.
- `-r` / `--resume <ID>`: resume a persisted session.
- `-c` / `--continue`: resume the most recent session in this workspace.
- `--output-format plain|json|streaming-json|streaming-messages-json`.
- `--max-turns <N>`: bound headless agent turns.
- `--model`, `--reasoning-effort`, `--cwd`.
- `--allow`, `--deny`, `--permission-mode`, `--always-approve`.
- `--tools`, `--disallowed-tools`: headless tool filtering.
- `--disable-web-search`: prevent built-in web search.

Use `process(action="log"|"poll"|"kill", session_id="<Hermes process id>")`
for a background run. Do not poll tightly; `notify_on_complete=true` provides the
completion signal.

**Exit code 0 is not task completion.** If Grok only says what it plans to do,
verify that no artifact changed, then resume the same Grok session with a direct
execution instruction or finish the narrow task yourself.

## Interactive TUI

Interactive Grok requires a PTY. Prefer tmux for reliable capture and input.

```text
terminal(command="tmux new-session -d -s grok-work -x 140 -y 40")
terminal(command="tmux send-keys -t grok-work 'cd /path/to/repo && grok --no-alt-screen' Enter")
terminal(command="tmux capture-pane -t grok-work -p -S -100")
```

`--no-alt-screen` avoids alternate-screen capture problems. Use the TUI only
for persistent multi-turn collaboration; bounded automation belongs in `-p`.

### Typed-but-unsent prompts

If captured output still shows the draft plus `Enter: send`, the prompt was not
submitted. Send another Enter; if needed send a raw carriage return:

```text
terminal(command="tmux send-keys -t grok-work Enter")
terminal(command="tmux send-keys -t grok-work C-m")
```

With a Hermes PTY process, `process(action="submit", data="...")` may require a
second submit; `process(action="write", data="\r")` sends raw carriage return.

## Sessions and Workspaces

Grok sessions are keyed by working directory. Always list/resume/export from the
same `workdir` used to create the session.

```text
terminal(command="grok sessions list --limit 20", workdir="/path/to/repo")
terminal(command="grok sessions search 'keyword' --limit 20", workdir="/path/to/repo")
terminal(command="grok export <SESSION_ID> /tmp/grok-session.md", workdir="/path/to/repo")
terminal(command="grok -p '<continue task>' --resume <SESSION_ID> --max-turns 20 --output-format plain", workdir="/path/to/repo")
```

Use session IDs in automation. `--session-id` creates a new session; it does not
resume one. Sandbox profile is fixed at session creation: resuming under a
different `--sandbox` profile is refused.

## Worktree Isolation

For parallel or risky edits, Hermes creates the git worktree; headless Grok runs
inside it. Grok's `--worktree` flag is TUI-oriented and should not replace
explicit headless isolation.

```text
terminal(command="git worktree add -b fix/topic /tmp/project-topic main", workdir="/path/to/repo")
terminal(command="grok -p '<task; do not commit>' --max-turns 30 --always-approve", workdir="/tmp/project-topic", background=true, notify_on_complete=true)
```

Before integrating, verify every changed file, focused/full tests, and
`git diff --check`. Never mix a timed-out worker's partial edits into another
worktree without an explicit diff review.

## Review-Only Runs

A prose instruction is not a security boundary. Deny mutation and network tools
explicitly:

```text
terminal(
  command="grok -p '<review brief; return findings only>' --permission-mode dontAsk --deny 'Edit(*)' --deny 'Write(*)' --deny 'Bash(*)' --deny 'WebFetch(*)' --disable-web-search --max-turns 20 --output-format plain",
  workdir="/path/to/repo",
  background=true,
  notify_on_complete=true,
)
```

Where kernel sandboxing works, `--sandbox read-only` adds enforcement. In some
containers bubblewrap fails with a user-namespace permission error; use an
isolated worktree plus explicit deny rules rather than pretending that sandbox
succeeded.

## Stopping `/loop` and Scheduler Tasks

A Grok `/loop` is an internal scheduler task, not a Hermes cron job. Killing the
Grok process stops a non-durable task immediately, but the task can remain in the
session's `resources_state.json` and revive when that session is resumed.

For an explicitly requested permanent stop:

1. Attribute the live Grok PID to the exact session (`lsof -p <pid>` shows the
   open session `events.jsonl`; confirm the session title/task before killing).
2. Stop that Grok process group and verify all of its tool/subagent children are
   gone.
3. Prefer `scheduler_list` + `scheduler_delete(task_id)` while the session is
   live. If Grok is already stopped and no scheduler CLI exists, back up the
   session's `resources_state.json`, atomically remove only the exact task under
   `state.grok_build.Scheduler.tasks`, and parse/read it back.
4. Verify: no matching Grok/auth process, no scheduler entry, no detached child,
   and no external service/container the loop could have started.

Do not delete the whole Grok session merely to stop one loop; its transcript and
edits are useful recovery evidence.

## Detecting a Stuck Run

A spinner alone is not progress. Treat a run as wedged only when several signals
agree for several minutes:

1. Grok session files stop advancing.
2. No useful child build/test/file process exists.
3. CPU remains near idle.
4. No new tool/result line appears.

Check through Hermes without opening the TUI:

```text
terminal(command="stat $HOME/.grok/sessions/<encoded-cwd>/<SESSION_ID>/updates.jsonl")
terminal(command="ps -p <PID> -o pid,stat,etime,pcpu,time,cmd; ps --ppid <PID> -o pid,stat,etime,pcpu,time,cmd")
process(action="log", session_id="<Hermes process id>")
```

If wedged, kill the Hermes process and resume the **same Grok session ID** as a
bounded headless job. Persisted edits/session history survive; starting a new
session discards useful context.

## Procedure

1. **Choose mode.** Headless for bounded work; TUI only for persistent dialogue.
2. **Set scope.** Use the exact repo/worktree and a self-contained brief with
   forbidden side effects and required tests.
3. **Bound execution.** Set `--max-turns`, Hermes `timeout`, and
   `notify_on_complete=true`.
4. **Monitor evidence.** Trust file/test/process evidence, not a spinner or an
   intention-only response.
5. **Recover safely.** Detect unsent/stuck sessions, kill only when wedged, and
   resume the same Grok session.
6. **Verify independently.** Re-read the diff, execute tests, run
   `git diff --check`, and use a separate reviewer before committing.

Completion means the requested artifact exists and independent verification
passes—not that Grok exited successfully.

## Pitfalls

- Wrong `workdir` makes sessions appear missing.
- `--session-id` creates; `--resume` continues.
- TUI without PTY/tmux can hang or misrender.
- `Enter: send` means the prompt is still a draft.
- `--tools` removes tools; `--deny` gates them.
- Deny rules and hooks still apply under `--always-approve`.
- Sandbox is sticky and may fail under restricted bubblewrap environments.
- Headless `--worktree` does not replace explicit git worktree isolation.
- A clean exit can contain only a plan; verify external state.
- Never report progress from a spinner alone.

## Verification

- `grok --version` and `grok inspect --json` succeed.
- The run uses the intended workspace and Grok session ID.
- Permission boundaries match the requested side-effect scope.
- Changed files are exactly accounted for.
- Required tests and `git diff --check` pass independently.
- No raw credentials, tickets, cookies, or private URLs appear in prompts/logs.

## References

- `references/headless-and-sessions.md`
- `references/pty-and-recovery.md`
- `references/permissions-and-sandbox.md`
