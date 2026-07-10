---
name: nats-hub
description: Coordinate with other AI agents via the nats-hub messaging bus. Use this skill when you need to send messages to other agents, delegate tasks, manage sessions, or orchestrate parallel work across multiple agents.
---

# NATS Hub Multi-Agent Coordination

You have access to a set of MCP tools that connect to the **nats-hub** bus —
a NATS-based messaging layer for agent-to-agent and human-to-agent communication.

## Available MCP Tools

### Agent Discovery
- **list_agents** — See who's online. Filter by `capability` or `alive_within_secs`.
- **get_agent** — Get details for one agent by identity.

### Messaging
- **send_message** — Broadcast to a channel (all subscribers see it).
- **send_direct** — DM a specific agent (private, inbox-routed).
- **send_status** — Post a status update ("working", "idle", "ready", "error").

### Session Management
- **start_session** — Start a multi-turn session with a worker agent. Returns a session_id.
- **send_to_session** — Send a follow-up message on an existing session.
- **close_session** — Close a session when done.
- **list_sessions** — List active/closed sessions.
- **get_session** — Get details for one session.

### Task Delegation
- **delegate_task** — One-shot: send a task to a worker, wait for the reply.
  Use for quick assignments that need a response.

### Wave Orchestration
- **create_wave** — Create a group of parallel tasks with disjoint write scopes.
  Provide a goal and a list of {worker, goal} tasks.
- **list_waves** — List waves (optionally filter by status).
- **get_wave** — Get a wave by ID.
- **list_wave_tasks** — List tasks in a wave.
- **get_wave_task** — Get one task in a wave.

### History & Threading
- **get_history** — Query message history (filter by channel, sender, kind, time).
- **get_thread** — Get a conversation thread by root message ID.
- **list_pending** — List unanswered messages for an agent.

### Analytics
- **get_analytics** — Get stats: message_rate, latency, agent_activity, channel_hotspots, error_rate.

## Communication Patterns

### Broadcast to a channel
```
send_message(channel="agents.broadcast", message="Hello everyone", from="codex")
```

### Direct message
```
send_direct(to="worker-1", message="Can you review my PR?", from="codex")
```

### Delegate a task and get the result
```
delegate_task(to="worker-1", prompt="Fix the failing test in auth module", from="codex", timeout=120)
```

### Start a multi-turn session
```
start_session(worker="hermes-worker", from="codex", prompt="Help me debug this issue")
→ returns session_id

send_to_session(session_id="abc123", message="Here's the error log...", from="codex")

close_session(session_id="abc123", from="codex")
```

### Create a parallel wave
```
create_wave(
  goal="Refactor auth module across 3 services",
  orchestrator="codex",
  tasks=[
    {worker: "worker-a", goal: "Refactor auth-rs"},
    {worker: "worker-b", goal: "Update auth-api"},
    {worker: "worker-c", goal: "Fix auth tests"}
  ]
)
```

## When to Use This Skill

Use nats-hub tools when you need to:
- **Coordinate** with other AI agents or human operators on the bus
- **Delegate** work to specialized worker agents
- **Check status** of running agents before assigning tasks
- **Orchestrate** parallel work across multiple agents (waves)
- **Review** message history or conversation threads
- **Monitor** bus activity with analytics

## Prerequisites

The nats-hub bus must be running:
1. NATS server: `nats-server -c config/nats-server.conf`
2. Hub server: `cargo run --bin hub-server` (in the nats-hub repo)

If the bus is down, MCP tools will return errors. The SessionStart hook
will warn you if it can't connect.
