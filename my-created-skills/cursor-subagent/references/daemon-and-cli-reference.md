# Daemon, Bus, and CLI Reference

## Stack startup

```bash
cursor-subagent bus start       # nats-server + subagent-gateway
cursor-subagent daemon start    # Python REST daemon
cursor-subagent bus status --json
cursor-subagent daemon status --json
```

## Session commands

| Command | Description |
| ------- | ----------- |
| `spawn --task TEXT [--cwd .] [--provider cursor-composer] [--persist] [--from-template ID] [--runtime local\|cloud] [--repo URL] [--json]` | Create session + first task |
| `resume --agent-id ID [--cwd .] [--task TEXT] [--json]` | Re-register session from Cursor agent ID |
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
| `wave spawn <waveId> [--task-ids T1,T2] [--json]` | Spawn parallel sessions |
| `wave status <waveId> [--json]` | Wave + sessions |
| `wave close <waveId> [--json]` | Close all wave sessions |

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

## Python REST API (unchanged)

| Method | Path |
| ------ | ---- |
| POST | `/sessions`, `/sessions/resume` |
| GET | `/sessions`, `/sessions/{id}`, `/sessions/{id}/events` |
| POST | `/sessions/{id}/messages`, `/sessions/{id}/cancel`, `/shutdown` |
| DELETE | `/sessions/{id}` |
| POST/GET | `/waves`, `/waves/{id}`, `/waves/{id}/spawn`, `/waves/{id}/close` |

Streaming moved off FastAPI WebSocket — use gateway instead.
