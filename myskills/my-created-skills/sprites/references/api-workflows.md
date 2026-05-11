# Sprite API Workflows

## Table of Contents

- [Deploy Code](#deploy-code)
- [Restart a Service](#restart-a-service)
- [Read Logs](#read-logs)
- [Run a Command](#run-a-command)
- [Check Service Status](#check-service-status)

---

## Deploy Code

### Option A: Filesystem API (write files directly)

Use `PUT /v1/sprites/{name}/fs/{path}` to write individual files.

```bash
curl -X PUT \
  -H "Authorization: Bearer $SPRITE_TOKEN" \
  -H "Content-Type: application/octet-stream" \
  --data-binary @local_file.py \
  "https://api.sprites.dev/v1/sprites/my-sprite/fs/app/local_file.py"
```

### Option B: Exec API (git pull)

Open a WebSocket to `/v1/sprites/{name}/exec` and run:

```bash
cd /srv/agentic-memory-ladybug-mcp && git pull
```

### Option C: Git bundle + exec

For private repos that the sprite cannot reach directly:

1. Create a git bundle locally: `git bundle create /tmp/bundle main`
2. Upload the bundle via Filesystem API
3. Exec: `git fetch /tmp/bundle +main:refs/remotes/origin/main && git switch -C main refs/remotes/origin/main`

---

## Restart a Service

Use the Exec API to restart the service. For systemd:

```bash
systemctl restart am-server
# or
systemctl restart healthcare-dashboard
```

For direct process restart:

```bash
pkill -f "am_server.server"
# then start again (e.g. via systemd or nohup)
```

Or use the Services API:

```bash
curl -X POST \
  -H "Authorization: Bearer $SPRITE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"command": "restart"}' \
  "https://api.sprites.dev/v1/sprites/my-sprite/services/am-server"
```

---

## Read Logs

### Read a log file

```bash
curl -H "Authorization: Bearer $SPRITE_TOKEN" \
  "https://api.sprites.dev/v1/sprites/my-sprite/fs/var/log/am-server.log"
```

### Tail logs via exec

Open a WebSocket exec session and run:

```bash
tail -f /var/log/am-server.log
# or
tail -f /srv/agentic-memory-ladybug-mcp/logs/server.log
```

---

## Run a Command

Exec API uses WebSocket. Connect to:

```
wss://api.sprites.dev/v1/sprites/{name}/exec
```

With headers:
- `Authorization: Bearer $SPRITE_TOKEN`

Send JSON messages for stdin. Receive stdout/stderr over the socket.

Python SDK example:

```python
from sprites_sdk import SpriteClient

client = SpriteClient(token=os.environ["SPRITE_TOKEN"])
sprite = client.sprite("ladybug-binjk")

# Run a command and get output
result = sprite.exec("cd /srv/agentic-memory-ladybug-mcp && git status")
print(result.stdout)
```

---

## Check Service Status

### Check systemd service

```bash
systemctl is-active am-server
systemctl status am-server
```

### Check HTTP health endpoint

```bash
curl https://ladybug-binjk.sprites.app/health
curl https://ladybug-binjk.sprites.app/health/onboarding
```

### Check running processes

```bash
ps aux | grep am_server
```
