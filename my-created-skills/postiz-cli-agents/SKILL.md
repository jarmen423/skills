---
name: postiz-cli-agents
description: This skill should be used when working with the Postiz public API through the postiz CLI, scheduling or drafting social posts, listing or deleting posts, uploading media, running integration discovery (integrations list, settings, trigger), fetching analytics, or fixing missing release IDs after publish. Triggers include Postiz CLI, POSTIZ_API_KEY, AI agent social scheduling, multi-platform posts, and self-hosted Postiz via POSTIZ_API_URL.
---

# Postiz CLI for AI agents

## Overview

Use the global `postiz` command to drive Postiz’s public HTTP API: discover connected channels, create scheduled or draft posts, upload media, and read analytics. Output is JSON-friendly for scripting.

**Documentation:** [Introduction](https://docs.postiz.com/introduction) · [Public API](https://docs.postiz.com/public-api/introduction) · Index: [llms.txt](https://docs.postiz.com/llms.txt) · Agent repo: [gitroomhq/postiz-agent](https://github.com/gitroomhq/postiz-agent)

**Deeper command and provider detail:** load [`references/cli-command-reference.md`](references/cli-command-reference.md) and [`references/environment-and-troubleshooting.md`](references/environment-and-troubleshooting.md) when needed.

## When to use this skill

- Schedule or draft posts, threads, or multi-platform campaigns via CLI.
- List or delete posts; inspect date ranges.
- Upload images, video, or documents before referencing URLs in posts.
- Discover integration IDs, schemas, and trigger provider tools (flairs, playlists, companies, etc.).
- Read platform or post analytics; resolve `missing` provider linkage with `posts:missing` and `posts:connect`.
- Point a CLI at a self-hosted instance using `POSTIZ_API_URL`.

## Prerequisites

- Install the CLI globally (any of): `npm install -g postiz`, `pnpm install -g postiz`, or `bun install -g postiz`.
- Ensure `postiz` is on `PATH` (verify with `postiz --help`).

## Environment (required)

The CLI reads **only** process environment variables, not project `.env` files automatically.

- Set `POSTIZ_API_KEY` before any command.
- Optionally set `POSTIZ_API_URL` (default public API: `https://api.postiz.com`).

If the key lives in a `.env` file, export it for the shell session before calling `postiz`. See [`references/environment-and-troubleshooting.md`](references/environment-and-troubleshooting.md) for patterns (`direnv`, `set -a` / `source`, etc.).

Never commit API keys or paste them into logs or chat output.

## Core agent workflow

Execute steps in order unless the task is read-only (e.g. list posts).

1. **Discover:** `postiz integrations:list` — note each integration `id` and provider identifier.
2. **Schema:** `postiz integrations:settings <integration-id>` — character limits, required settings, available tool methods.
3. **Dynamic data (optional):** `postiz integrations:trigger <id> <method> [-d '{"key":"value"}']` — e.g. Reddit flairs, YouTube playlists, LinkedIn companies.
4. **Media:** For TikTok, Instagram, YouTube, and similar, run `postiz upload <file>` first; use the returned URL in `-m` (comma-separated per content block).
5. **Create:** `postiz posts:create` with ISO 8601 `-s` date, `-i` integration id(s), and optional `-c`, `-m`, `--settings`, `--json`.
6. **Analytics:** `postiz analytics:platform <integration-id>` or `postiz analytics:post <post-id>`. If post analytics indicate missing linkage, run `postiz posts:missing <post-id>` then `postiz posts:connect <post-id> --release-id "..."`.

## Command quick reference

| Area | Commands |
|------|----------|
| Integrations | `integrations:list`, `integrations:settings <id>`, `integrations:trigger <id> <method> [-d json]` |
| Posts | `posts:create` (requires `-s`, `-i`), `posts:list`, `posts:delete <id>`, `posts:missing <id>`, `posts:connect <id> --release-id` |
| Media | `upload <file>` |
| Analytics | `analytics:platform <integration-id> [-d days]`, `analytics:post <post-id> [-d days]` |

**Create post (minimal):**

```bash
postiz posts:create -c "Content" -s "2025-12-31T12:00:00Z" -i "integration-id"
```

**Create from JSON file:**

```bash
postiz posts:create --json post.json
```

**List integrations (JSON):**

```bash
postiz integrations:list
```

Full flags, endpoints table, and platform notes: [`references/cli-command-reference.md`](references/cli-command-reference.md).

## Output and parsing

Treat CLI stdout as JSON where documented. Use `jq` in shell pipelines when selecting fields (e.g. integration id by provider, upload `.path`).

## Related in-repo reference

If working inside the Postiz application monorepo (`postiz-app`), the canonical long-form CLI skill lives at `apps/cli/SKILL.md` with extended provider examples.
