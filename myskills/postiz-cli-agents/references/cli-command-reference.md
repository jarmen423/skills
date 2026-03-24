# Postiz CLI — command reference (condensed)

Source alignment: [postiz-agent README](https://github.com/gitroomhq/postiz-agent), Postiz app [`apps/cli/README.md`](https://github.com/gitroomhq/postiz-app/blob/main/apps/cli/README.md).

## Environment

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `POSTIZ_API_KEY` | Yes | — | API token |
| `POSTIZ_API_URL` | No | `https://api.postiz.com` | API base URL (use for self-hosted) |

## Integrations

| Command | Purpose |
|---------|---------|
| `postiz integrations:list` | List connected integrations (ids, identifiers, metadata) |
| `postiz integrations:settings <integration-id>` | Schema: limits, required settings, tool methods |
| `postiz integrations:trigger <integration-id> <method-name>` | Run a provider tool |
| `postiz integrations:trigger <integration-id> <method-name> -d '{"key":"value"}'` | Tool with JSON payload |

Examples:

```bash
postiz integrations:trigger reddit-id getFlairs -d '{"subreddit":"programming"}'
postiz integrations:trigger youtube-id getPlaylists
postiz integrations:trigger linkedin-id getCompanies
```

## Posts

| Command | Purpose |
|---------|---------|
| `postiz posts:create ...` | Create scheduled or draft post |
| `postiz posts:list` | List posts (default window about last 30 days to next 30 days) |
| `postiz posts:list --startDate ... --endDate ...` | Filter by ISO range |
| `postiz posts:list --customer <customer-id>` | Filter by customer |
| `postiz posts:delete <post-id>` | Delete a post |
| `postiz posts:missing <post-id>` | List provider content when release id was not returned |
| `postiz posts:connect <post-id> --release-id "<id>"` | Attach published content id for analytics |

### posts:create common flags

| Flag | Meaning |
|------|---------|
| `-c, --content` | Text; repeat for main + comments / thread segments |
| `-s, --date` | Schedule time, **ISO 8601** (required) |
| `-t, --type` | `schedule` or `draft` (default `schedule`) |
| `-m, --media` | Comma-separated URLs per matching `-c` block |
| `-i, --integrations` | Comma-separated integration ids (required) |
| `-d, --delay` | Delay between comment/thread segments in **milliseconds** (default 5000) |
| `--settings` | JSON string for provider-specific settings |
| `-j, --json` | Path to JSON file for full structure |
| `--shortLink` | Short links (default true) |

Multi-platform: pass multiple ids to `-i` as comma-separated.

## Upload

```bash
postiz upload <file-path>
```

Returns JSON; use the returned hosted URL (often `.path`) in `posts:create -m`. Required for many video/image workflows so platforms receive trusted URLs.

## Analytics

```bash
postiz analytics:platform <integration-id>
postiz analytics:platform <integration-id> -d 30
postiz analytics:post <post-id>
postiz analytics:post <post-id> -d 30
```

`-d` is lookback **days** (defaults vary by command; see `--help`).

If `analytics:post` indicates missing linkage, use `posts:missing` then `posts:connect` before expecting metrics.

## HTTP API mapping (public v1)

| Endpoint | Method | Role |
|----------|--------|------|
| `/public/v1/posts` | POST | Create post |
| `/public/v1/posts` | GET | List posts |
| `/public/v1/posts/:id` | DELETE | Delete post |
| `/public/v1/posts/:id/missing` | GET | Missing provider content |
| `/public/v1/posts/:id/release-id` | PUT | Set release id |
| `/public/v1/integrations` | GET | List integrations |
| `/public/v1/integration-settings/:id` | GET | Settings schema |
| `/public/v1/integration-trigger/:id` | POST | Trigger tool |
| `/public/v1/analytics/:integration` | GET | Platform analytics |
| `/public/v1/analytics/post/:postId` | GET | Post analytics |
| `/public/v1/upload` | POST | Upload media |

## Provider-specific settings

For full per-platform JSON schemas, use `integrations:settings` output and provider docs in the Postiz repo (`apps/cli/PROVIDER_SETTINGS.md` when developing from source).
