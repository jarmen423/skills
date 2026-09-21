# Headless and Sessions — Grok Build 1.0.5

## Headless flags

`-p`/`--single` triggers headless. `-s`/`--session-id` creates a **new**
unused UUID; `-r`/`--resume` and `-c`/`--continue` resume. `-s` with
`-r`/`-c` requires `--fork-session`.

Headless-only: `--tools`, `--disallowed-tools`, `--max-turns`, `--agents`.
Both modes: `--allow`, `--deny`, `--permission-mode`,
`--reasoning-effort`/`--effort`.

## Output formats

- `plain`: text.
- `json`: one object with `text`, `stopReason`, `sessionId`, `requestId`,
  `num_turns`, `usage`, `modelUsage`, and reported cost fields.
- `streaming-json`: newline-delimited ACP updates ending with `end`.
- `streaming-messages-json`: newline-delimited Messages API format.

Cost absent means unreported, not free. `sessionId` is persistent Grok context;
`requestId` identifies one prompt.

## Session storage

```text
$HOME/.grok/sessions/<url-encoded-cwd>/<session-id>/
  summary.json
  updates.jsonl
  chat_history.jsonl
  plan.json
  rewind_points.jsonl
  signals.json
  compaction_checkpoints/
  subagents/
```

- `grok sessions list` and search are scoped to cwd.
- `grok export <ID> [OUTPUT]` exports Markdown.
- `grok trace <ID> --local -o <path>` exports a local trace.
- `grok inspect --json` reports cwd, project, permissions, skills, hooks, and
  models.
- Use IDs in scripts; title matching is cwd-scoped and ambiguous on duplicates.
- Sandbox profile is persisted with the session and cannot change on resume.
