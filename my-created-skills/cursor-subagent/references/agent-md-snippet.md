## Cursor sub-agents

Delegate implementation work to stateful Composer 2.5 sessions via the local stack:

```bash
cursor-subagent bus start
cursor-subagent spawn --task "<task with owned file paths>" --cwd <repo> --json
cursor-subagent send <sessionId> "<follow-up>" --json
cursor-subagent close <sessionId> --json
```

**Cloud agents (optional):** add `--runtime cloud --repo https://github.com/org/repo` to `spawn` or `resume` when work should run in a Cursor cloud VM against the remote repo. Requires paid plan + GitHub/GitLab access. `wave spawn` is local-only.

**Credentials:** set `CURSOR_API_KEY` in `<repo>/.env` or `~/.cursor/subagents/.env`. Always pass `--cwd` to the target repo. Never log the key.

**Rules:** one session per task; reuse via `send`; start `bus` before `watch`; always `close` when done.
