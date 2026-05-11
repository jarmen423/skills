---
name: sprites
description: >
  Work with Sprites (sprites.dev) — persistent hardware-isolated microVMs for running
  arbitrary code and long-lived services. Use when the user mentions sprites, sprites.dev,
  ladybug sprite, sprite deployment, or any task involving a Sprite microVM. NEVER assume
  SSH access to a Sprite — they are managed exclusively via the Sprites HTTP/WebSocket API.
  Use for: deploying code to sprites, managing sprite services, reading sprite logs/files,
  restarting sprite processes, or debugging issues with a sprite-hosted backend.
---

# Sprites (sprites.dev)

## Critical Rule: No SSH

**Sprites are NOT accessed via SSH.** They are microVMs from [sprites.dev](https://sprites.dev) managed through an HTTP/WebSocket API. If you find yourself thinking "I'll SSH into the sprite," stop — use the API instead.

## What Is a Sprite?

- Persistent, hardware-isolated Linux microVM (not a container)
- Full ext4 filesystem that persists between runs
- Wakes from hibernation on request; idle = no compute cost
- Exposed via a unique URL (e.g. `https://ladybug-binjk.sprites.app`)
- Ideal for long-lived services, AI agent execution, isolated dev environments

## Authentication

All API requests require a Bearer token:

```bash
curl -H "Authorization: Bearer $SPRITE_TOKEN" \
  https://api.sprites.dev/v1/sprites
```

## Core APIs

Base URL: `https://api.sprites.dev/v1`

### Sprites (lifecycle)
- `GET /sprites` — list sprites
- `POST /sprites` — create a sprite
- `GET /sprites/{name}` — get sprite details
- `PATCH /sprites/{name}` — update sprite
- `DELETE /sprites/{name}` — delete sprite

### Exec (command execution)
- WebSocket-based stdin/stdout streaming
- Run commands inside the sprite remotely
- Use this instead of SSH for all shell operations

### Filesystem (file I/O)
- Read, write, and manage files within sprites
- Use this to deploy code, edit configs, read logs

### Services (background processes)
- Manage persistent background services
- Start, stop, restart services (e.g. `am_server`)

### Checkpoints (snapshots)
- Create point-in-time snapshots
- Restore sprite to previous state

### Proxy (networking)
- Tunnel TCP connections to ports inside sprites
- Expose internal ports externally

## Project Context

**Our Sprite:** `https://ladybug-binjk.sprites.app`
- Hosts the `am_server` backend on port 8080
- Runs `LadybugNativeConversationPipeline` and `LadybugNativeResearchPipeline`
- LadybugDB lives inside the sprite at `/srv/agentic-memory-ladybug-mcp/data/`
- Checkout: `/srv/agentic-memory-ladybug-mcp`
- Process: `am_server.server` on port 8080 (PID 43 at last check)
- Auth: `shared_api_key` via `AM_SERVER_API_KEYS`
- Real API key: `7a4b2ef1a7b209016ce2670b6b01fc3066a3553bfae0b0745aaf44266dba724c`

## Common Workflows

### Deploy code to a sprite
Use the **Filesystem API** to write files, or the **Exec API** to run `git pull` / `git fetch` commands. See `references/api-workflows.md` for detailed patterns.

### Restart a service
Use the **Services API** or **Exec API** to run `systemctl restart <service>` or restart the process directly.

### Read logs
Use the **Filesystem API** to read log files (e.g. `/var/log/...` or app-specific logs), or the **Exec API** to tail them.

### Check if a sprite is healthy
HTTP GET to the sprite's URL (e.g. `https://ladybug-binjk.sprites.app/health`).

## Docs & SDKs

- Main docs: https://docs.sprites.dev/
- API reference: https://sprites.dev/api
- SDKs: Go, JavaScript, Python, Elixir
- API version: `0.0.1-dev`
