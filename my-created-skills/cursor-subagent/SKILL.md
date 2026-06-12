---
name: cursor-subagent
description: >-
  Delegate work to stateful Cursor sub-agents (Composer 2.5) via the cursor-subagent
  daemon, NATS event bus, and Rust WebSocket gateway. Supports local runtime (default)
  and Cursor cloud agents via --runtime cloud --repo. Use when spawning sub-agents
  from Codex, Claude Code, or other main agents; orchestrating parallel waves with
  wave-execution; running cursor-subagent spawn/send/watch/close/bus; or when
  CURSOR_API_KEY and multi-turn sub-agent sessions are needed.
disable-model-invocation: true
---

# Cursor Sub-Agent

## Overview

Use the **cursor-subagent stack** to run stateful Composer 2.5 sessions:

1. **NATS bus** — event streaming decoupled from the Python daemon
2. **Rust gateway** — WebSocket bridge for live `watch`
3. **Python daemon** — REST API, session manager, cursor-sdk

Load [`references/daemon-and-cli-reference.md`](references/daemon-and-cli-reference.md) for full command details.

## Prerequisites

1. Install Python package: `pip install -e .`
2. Install NATS: `scripts/install-nats-server.ps1` (Windows) or `.sh` (Unix)
3. Build gateway: `cargo build --release -p subagent-gateway`
4. Configure `CURSOR_API_KEY` (see **Credentials** below)
5. Start stack:
   ```bash
   cursor-subagent bus start
   cursor-subagent daemon start
   ```

## Credentials

Resolve `CURSOR_API_KEY` before spawning. Priority (first match wins):

1. Environment variable already set
2. Repo `.env` — walks up from `--cwd` to the `.git` root
3. `~/.cursor/subagents/.env` — machine default

**Agent rules:**

- Always pass `--cwd` to the **target repository** being automated
- Prefer repo `.env` for project-specific keys; never read, log, or commit it
- Mint keys at https://cursor.com/dashboard/cloud-agents

## When to delegate

- Disjoint implementation tasks with clear write scopes
- Parallel wave tracks (use `wave create` / `wave spawn` — local only today)
- Remote/PR work in Cursor cloud VMs (`spawn --runtime cloud --repo ...`)
- Multi-turn iteration on the **same session** via `send`

Do **not** spawn a new session per message.

## Core workflow (local — default)

```bash
cursor-subagent spawn --task "<precise task with owned paths>" --cwd /path/to/repo --json
cursor-subagent send <sessionId> "<feedback>" --json
cursor-subagent send <sessionId> "<feedback>" --watch --json
cursor-subagent watch <sessionId>              # Rust gateway WebSocket
cursor-subagent events <sessionId> --json      # SQLite replay
cursor-subagent close <sessionId> --json
```

Local runtime edits the live `--cwd` checkout via the cursor-sdk bridge.

On Linux, start `bus` before `daemon` when live watch is needed. The daemon
binds a NATS publisher during startup; if it started while NATS was down, run
`cursor-subagent daemon stop && cursor-subagent daemon start`.

## Cloud agents

Cloud runtime is **already supported** for single `spawn` / `resume` / `send` sessions. No extra code is required — pass `--runtime cloud` and `--repo`.

```bash
cursor-subagent spawn \
  --task "<precise task>" \
  --runtime cloud \
  --repo https://github.com/your-org/your-repo \
  --cwd /path/to/repo \
  --json

cursor-subagent resume \
  --agent-id bc-<uuid> \
  --runtime cloud \
  --repo https://github.com/your-org/your-repo \
  --cwd /path/to/repo \
  --task "Continue" \
  --json
```

**When to use cloud**

- Long-running work that should survive your machine disconnecting
- PR-based workflows against a GitHub/GitLab remote
- Parallel agents that should not depend on a local checkout

**When to use local (default)**

- Uncommitted local changes the agent must see
- Fast iteration on the working tree
- Windows bridge is automatic; local is the best-tested path

**Cloud prerequisites**

- `CURSOR_API_KEY` (same resolution as local — see **Credentials**)
- Paid Cursor plan with GitHub or GitLab connected (read-write on `--repo`)
- `--repo` is **required** — cloud clones from the remote; `--cwd` is still required for env loading and session bookkeeping
- Cloud agent IDs use the `bc-<uuid>` prefix (local uses `agent-<uuid>`)

**Follow-ups:** reuse the same session with `send` — same as local. `runtime` and `repo_url` are persisted in SQLite for daemon recovery.

**Wave limitation:** `wave spawn` does **not** pass `--runtime` or `--repo` yet; wave tasks always spawn **local** agents. Use individual `spawn` commands for cloud waves until that is extended.

See [`references/credentials-and-bridge.md`](references/credentials-and-bridge.md) for local vs cloud comparison.

## Resume and templates

```bash
cursor-subagent resume --agent-id <id> --cwd . --task "Continue" --json
# Cloud resume: add --runtime cloud --repo https://github.com/org/repo
cursor-subagent spawn --from-template <sessionId> --task "Run again" --json
```

Use `--persist` on spawn to keep closed session metadata for templates.

## Wave orchestration

Cross-ref **wave-execution** skill:

```bash
cursor-subagent wave create --wave-id wave-1 --goal "..." --tasks tasks.json --json
cursor-subagent wave spawn wave-1 --cwd . --json
cursor-subagent wave status wave-1 --json
cursor-subagent wave close wave-1 --json
```

## Rules for main agents

- One session per delegated task; reuse via `send`
- Start `bus` before `daemon`/`watch`; REST auto-starts Python daemon but cannot retroactively bind NATS if the daemon started while the bus was down
- Always `close` sessions or `wave close` when finished
- Never log `CURSOR_API_KEY`
- v1 provider: `cursor-composer` only
- On Windows, local runtime bridge bootstrap is automatic
- Always pass an absolute `--cwd`; repo-local `.env` credentials and daemon recovery depend on it
- Use `--persist` only when you need templates or durable event replay after close
- If `/` is full, SQLite WAL and Python tooling can fail; use a cache path on `/data` for `uv run`

See [`references/agent-md-snippet.md`](references/agent-md-snippet.md) for AGENTS.md copy-paste block.