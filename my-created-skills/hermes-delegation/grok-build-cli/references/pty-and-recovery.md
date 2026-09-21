# PTY and Recovery — Grok Build 1.0.5

## PTY requirements

Headless `-p` needs no PTY. Interactive `grok` needs a PTY; use Hermes
`pty=true` or tmux. `--no-alt-screen` helps when captured alternate-screen
output is garbled.

## Typed-but-unsent prompts

If captured TUI output shows draft text plus `Enter: send`, it was not
submitted. Send Enter again or raw carriage return (`C-m` in tmux,
`process(action="write", data="\r")` for a Hermes PTY process).

## Detecting a wedged spinner

Do not infer progress from the spinner. Require several signals for several
minutes:

1. `updates.jsonl` or relevant worktree files stop advancing.
2. No useful child process is building/testing/editing.
3. CPU stays near idle.
4. No new tool/result event appears.

A single slow model turn is not enough evidence.

## Kill and resume safely

- Kill the Hermes wrapper process only after confirming it is wedged.
- Resume the same Grok `sessionId` with a bounded `grok -p ... --resume <ID>`.
- Do not start a new Grok session; persisted history and edits belong to the old
  ID.
- Use `background=true, notify_on_complete=true` for bounded headless work.
- Exit code 0 is not proof of task completion; intention-only output is
  incomplete until artifacts/tests verify it.
