# Daemon, Bus, and CLI Reference

## Stack startup

```bash
cursor-subagent bus start       # nats-server + subagent-gateway
cursor-subagent daemon start    # Python REST daemon
cursor-subagent bus status --json
cursor-subagent daemon status --json
```

Linux notes:

- `bus start` launches detached `nats-server` and `subagent-gateway` processes.
- `daemon start` launches a detached REST daemon.
- Start or restart the daemon after the bus is running when `watch` matters,
  because the daemon creates its NATS publisher at startup.
- If root disk is full, SQLite WAL mode may raise `sqlite3.OperationalError:
  disk I/O error`; free `/` space or move rebuildable caches to `/data`.

## Credentials

Loaded at spawn/resume time from `--cwd`:

| Priority | Source |
| -------- | ------ |
| 1 | `CURSOR_API_KEY` in process environment |
| 2 | `<repo>/.env` (walk up from `--cwd` to `.git` root) |
| 3 | `~/.cursor/subagents/.env` |

Agents must pass an absolute `--cwd` to the repository under automation.

## Session commands

| Command | Description |
| ------- | ----------- |
| `spawn --task TEXT [--cwd .] [--provider cursor-composer] [--persist] [--from-template ID] [--runtime local\|cloud] [--repo URL] [--json]` | Create session + first task |
| `resume --agent-id ID [--cwd .] [--runtime local\|cloud] [--repo URL] [--task TEXT] [--json]` | Re-register session from Cursor agent ID |
| `send <sessionId> "message" [--json] [--watch]` | Follow-up message |
| `watch <sessionId> [--json]` | Gateway WebSocket stream |
| `status <sessionId> [--json]` | Session metadata |
| `events <sessionId> [--since RUN] [--json]` | SQLite event replay |
| `cancel <sessionId> [--json]` | Cancel active run |
| `close <sessionId> [--json]` | Close session |
| `list [--cwd .] [--wave ID] [--json]` | List sessions |

## Bus commands

| Command | Description |
| ------- | ----------- |
| `bus start` | Start NATS + Rust gateway |
| `bus stop` | Stop NATS + gateway |
| `bus status [--json]` | Health check |

## Wave commands

| Command | Description |
| ------- | ----------- |
| `wave create --wave-id ID --goal TEXT --tasks FILE [--json]` | Register wave |
| `wave spawn <waveId> [--task-ids T1,T2] [--cwd .] [--json]` | Spawn parallel sessions |
| `wave status <waveId> [--json]` | Wave + sessions |
| `wave close <waveId> [--json]` | Close all wave sessions |

## Automation commands

Project-local automations are stored in SQLite and run through the local daemon.
Every trigger creates a fresh persisted session. Cross-run continuity comes from
the automation memory summary and recent run history injected into each prompt.

| Command | Description |
| ------- | ----------- |
| `automation create --name NAME --task TEXT --cwd DIR [--cron EXPR] [--webhook] [--json]` | Create a local cron and/or webhook automation |
| `automation list [--status enabled\|paused] [--json]` | List automations |
| `automation show <automationId> [--json]` | Show definition, webhook URL, schedule, and memory |
| `automation trigger <automationId> [--payload JSON] [--json]` | Run immediately |
| `automation runs <automationId> [--limit N] [--json]` | List run ledger rows |
| `automation history <automationId> [--full] [--json]` | Show rolling memory, optionally full history |
| `automation pause|resume <automationId> [--json]` | Disable or enable triggers |
| `automation rotate-secret <automationId> [--json]` | Generate a new one-time webhook secret |
| `automation delete <automationId> [--json]` | Delete definition and local run history |

Webhook POSTs go to `/automations/{id}/webhook` with
`Authorization: Bearer <secret>` and JSON body `{"payload": {...}}`.

### Automation creation recipe

When a user asks an agent to create an automation, use these patterns:

```bash
# Scheduled automation. Use an absolute --cwd and standard five-field cron.
cursor-subagent automation create \
  --name "Daily repo digest" \
  --task "Summarize important repo changes. Read Automation History first and do not repeat completed work. End with an Automation Memory Update section." \
  --cwd /path/to/repo \
  --cron "0 9 * * *" \
  --json

# Webhook automation. The returned webhook_secret is shown only once.
cursor-subagent automation create \
  --name "Deploy review" \
  --task "Review the webhook payload, inspect the repo as needed, identify follow-up work, and end with an Automation Memory Update section." \
  --cwd /path/to/repo \
  --webhook \
  --json

# Smoke run and history check.
cursor-subagent automation trigger <automationId> --payload '{"reason":"smoke"}' --json
cursor-subagent automation history <automationId> --full --json
```

Creation checklist for agents:

- Start `bus` and `daemon` first if status commands show they are not running.
- Report the automation id, schedule or webhook URL, next run time, and where to
  inspect history.
- Do not log `CURSOR_API_KEY`; avoid repeating webhook secrets after creation.
- Use `rotate-secret` if a webhook secret is lost.

## NATS subjects

| Subject | Publisher | Purpose |
| ------- | --------- | ------- |
| `subagent.v1.session.{id}.events` | Python daemon | Stream events |
| `subagent.v1.session.{id}.lifecycle` | Python daemon | run_complete, session_closed |
| `subagent.v1.wave.{id}.events` | Python daemon | Wave-level updates |

## Gateway WebSocket

| URL | Purpose |
| --- | ------- |
| `ws://127.0.0.1:17341/sessions/{sessionId}/stream` | Session events |
| `ws://127.0.0.1:17341/waves/{waveId}/stream` | Wave events |

## Python REST API

| Method | Path |
| ------ | ---- |
| POST | `/sessions`, `/sessions/resume` |
| GET | `/sessions`, `/sessions/{id}`, `/sessions/{id}/events` |
| POST | `/sessions/{id}/messages`, `/sessions/{id}/cancel`, `/shutdown` |
| DELETE | `/sessions/{id}` |
| POST/GET | `/waves`, `/waves/{id}`, `/waves/{id}/spawn`, `/waves/{id}/close` |
| POST/GET/PATCH/DELETE | `/automations`, `/automations/{id}` |
| POST/GET | `/automations/{id}/trigger`, `/automations/{id}/webhook`, `/automations/{id}/runs`, `/automations/{id}/history` |

Streaming moved off FastAPI WebSocket — use gateway instead.

## Cloud agents

Single-session cloud agents are supported end-to-end. Pass `--runtime cloud` and `--repo`:

```bash
cursor-subagent spawn \
  --task "Implement feature X in owned paths" \
  --runtime cloud \
  --repo https://github.com/org/repo \
  --cwd /abs/path/to/repo \
  --json
```

Requirements: `CURSOR_API_KEY`, paid Cursor plan, GitHub/GitLab connected with read-write on `--repo`. Cloud agent IDs are `bc-<uuid>`.

`wave spawn` does **not** forward runtime/repo — wave tasks are local-only today.

## Windows / cursor-sdk bridge

**Local runtime only.** Cloud agents run in Cursor's VM and do not use the bridge for file work.

Local runtime requires the `cursor-sdk` bridge. On Windows the provider pre-launches the bridge and sets `CURSOR_SDK_BRIDGE_URL` / `CURSOR_SDK_BRIDGE_TOKEN` (workaround for SDK `WinError 10038`).

To attach to an existing bridge manually, export those variables before spawning.

## Operational rules

- Always pass an absolute `--cwd`; repo-local `.env` lookup and recovery both
  depend on the stored cwd.
- Reuse the same `sessionId` with `send`; do not spawn a fresh session for each
  follow-up.
- Use `send --watch --json` when the orchestrator should both send feedback and
  stream the resulting run.
- Use `--persist` when event replay or templates must survive `close`.
- Close sessions and waves when finished so live Cursor handles are released.
- Automation cron schedules use daemon-local time and do not backfill downtime.
- Set `SUBAGENT_DISABLE_AUTOMATION_SCHEDULER=1` only for tests or manual daemon debugging.