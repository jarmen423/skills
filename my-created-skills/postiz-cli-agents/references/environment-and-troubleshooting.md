# Environment and troubleshooting — Postiz CLI

## How environment works

The CLI loads credentials from **environment variables only** (`POSTIZ_API_KEY`, optional `POSTIZ_API_URL`). It does **not** automatically read a project `.env` file.

Having a key in `.env` on disk is not sufficient until those variables are exported into the process that runs `postiz`.

## Loading from a `.env` file (shell)

**Option A — export for current session (bash):**

```bash
set -a
source /path/to/.env
set +a
postiz integrations:list
```

**Option B — one-off export:**

```bash
export POSTIZ_API_KEY="..."
export POSTIZ_API_URL="https://your-instance.example.com"   # if self-hosted
```

**Option C — direnv:** use a `.envrc` that exports the variables so they load when entering the directory.

Avoid echoing or logging the key. Do not commit `.env`.

## Self-hosted Postiz

Set `POSTIZ_API_URL` to the public base URL of the Postiz API for that deployment (no trailing slash unless your CLI docs specify otherwise). Keep HTTPS in production.

## Common issues

| Symptom | What to check |
|---------|----------------|
| `POSTIZ_API_KEY is not set` | Export the variable in the same shell; confirm with a non-printing check (e.g. test length) rather than printing the key. |
| Integration not found | Run `integrations:list` and use the exact `id` string. |
| Invalid date | Use ISO 8601, e.g. `2025-12-31T12:00:00Z`. |
| Upload or post rejected for media URL | Run `postiz upload` first; use returned URL in `-m`. |
| `analytics:post` shows missing linkage | `posts:missing` then `posts:connect` with the correct release id from the provider. |
| Wrong API host | Set `POSTIZ_API_URL` to match your account or self-hosted instance. |

## Documentation links

- [Postiz introduction](https://docs.postiz.com/introduction)
- [Public API](https://docs.postiz.com/public-api/introduction)
- [Configuration reference](https://docs.postiz.com/configuration/reference)
- [postiz-agent (CLI / agent patterns)](https://github.com/gitroomhq/postiz-agent)
