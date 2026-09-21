# Sessions and JSONL

## Where sessions live

Retained sessions are under `~/.local/share/muse/sessions/YYYY/MM/DD/<uuid>/`.
Each directory has `session.jsonl`. The queryable index is
`~/.local/share/muse/session-index.db`, table `sessions`.

There is no `muse sessions list`. Query the index with the Hermes `terminal`
tool. Never select `first_user_prompt` or `search_text`.

```text
terminal(command="python3 - <<'PY'
import sqlite3, os
path = os.path.expanduser('~/.local/share/muse/session-index.db')
con = sqlite3.connect(path)
ws = '/absolute/path/to/worktree'
rows = con.execute('''
SELECT session_id, status, model_id, workspace_root, git_branch, title, updated_at_us, session_log_path
FROM sessions
WHERE workspace_root = ?
ORDER BY updated_at_us DESC
LIMIT 10
''', (ws,))
for row in rows:
    print(row)
PY")
```

`session_log_path` is the file to pass to `muse trace inspect --session-log`
and to `muse export --session` (an existing file path wins over an id parse).

Resume headless only with `muse exec --session-id <session_id>` from that
same `workspace_root`, unless you intentionally pass `--allow-workspace-switch`.

## JSONL fields that matter

`--json` writes one JSON object per line to stdout. Hermes may merge stderr
into the same log. Ignore lines that do not start with `{`.

| Field | Meaning |
| --- | --- |
| `stream.kind` / `stream.id` | `session` plus the session UUID to resume. Capture it from the first session event. |
| `payload_type` `session.workspace_branch.observed` | `payload.record.workspace_root` must match the worktree before you treat the run as isolated. |
| `payload_type` `run.output.delta` | Incremental assistant text in `payload.text`. |
| `payload_type` `run.terminal.completed` | Turn ended. Read `payload.terminal` and `payload.text`. |
| `payload_type` `task.lifecycle.failed` | A child task failed even if the terminal event says completed. |

Extract the terminal event without loading the whole log into the conversation:

```text
terminal(command="python3 - <<'PY'
import json
path = '/absolute/path/muse-stdout.jsonl'
session = None
terminal = None
failed = 0
with open(path) as fh:
    for line in fh:
        line = line.strip()
        if not line.startswith('{'):
            continue
        ev = json.loads(line)
        stream = ev.get('stream') or {}
        if stream.get('kind') == 'session' and session is None:
            session = stream.get('id')
        kind = ev.get('payload_type')
        if kind == 'task.lifecycle.failed':
            failed += 1
        if kind == 'run.terminal.completed':
            terminal = ev.get('payload') or {}
print('session', session)
print('terminal', None if terminal is None else terminal.get('terminal'))
print('failed_tasks', failed)
text = '' if terminal is None else terminal.get('text') or ''
print(text[:2000])
PY")
```

If the Hermes process log is the only capture, write that filtered extract to
a file first. Do not paste a raw export into chat.

## Export

```text
muse export --session <UUID> --out /absolute/path/run.json --redacted
```

Run it with Hermes `workdir` set to the session's workspace. `--redacted` is
still not safe to quote in chat: encrypted reasoning blobs stay verbatim, and
redaction is pattern-based. Read it locally, then summarize.

## What not to use as progress

- A `muse:` stderr line about skills loading.
- Exit code 0.
- `payload.terminal == completed` when `git status` in the worktree is clean
  and the brief required edits.

Pair this page with `coding-agent-supervision`: process state, child
test/build processes, and file mtimes are the liveness ladder. The session
JSONL advancing is Muse-specific evidence on that ladder.
