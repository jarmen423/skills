## cursor-subagent orchestration

Use `cursor-subagent` for stateful Cursor Composer 2.5 sub-agents when a task
has a clear owned path, can run independently, or needs multi-turn follow-up.

```bash
cursor-subagent bus start
cursor-subagent daemon start
cursor-subagent bus status --json
cursor-subagent daemon status --json

cursor-subagent spawn --task "<precise task and owned paths>" --cwd "$(pwd)" --json
cursor-subagent send <sessionId> "<feedback>" --watch --json
cursor-subagent events <sessionId> --json
cursor-subagent close <sessionId> --json
```

Rules:

- Start `bus` before `daemon` when live `watch` is needed.
- Always pass an absolute `--cwd`; repo `.env` and recovery depend on it.
- Reuse one session with `send`; do not spawn one session per message.
- Use `--persist` only for templates or replay that must survive `close`.
- Always close sessions or waves when finished.
