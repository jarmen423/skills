## Cursor sub-agents

Delegate implementation work to stateful Composer 2.5 sessions via the local stack:

```bash
cursor-subagent bus start
cursor-subagent daemon start
cursor-subagent bus status --json
cursor-subagent daemon status --json

cursor-subagent spawn --task "<task with owned file paths>" --cwd "$(pwd)" --json
cursor-subagent send <sessionId> "<follow-up>" --watch --json
cursor-subagent events <sessionId> --json
cursor-subagent close <sessionId> --json
```

**Cloud agents (optional):** add `--runtime cloud --repo https://github.com/org/repo` to `spawn` or `resume` when work should run in a Cursor cloud VM against the remote repo. Requires paid plan + GitHub/GitLab access. `wave spawn` is local-only.

**Credentials:** set `CURSOR_API_KEY` in `<repo>/.env` or `~/.cursor/subagents/.env`. Always pass an absolute `--cwd` to the target repo. Never log the key.

**Rules:** one session per task; reuse via `send`; start `bus` before `daemon` when live `watch` is needed; use `--persist` only for templates or replay that must survive `close`; always `close` when done.