# Troubleshooting

## Quick diagnostics

```bash
cursor-subagent bus status --json
cursor-subagent daemon status --json
```

Both should show running before live spawns.

---

## Auth / credentials

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `CURSOR_API_KEY is not set` | No key in env, repo `.env`, or global file | Add key to `<repo>/.env`; use `--cwd` pointing at that repo |
| Key set but still fails | Wrong repo `--cwd` | Pass absolute path to repo containing `.env` |
| `AuthenticationError` / 401 | Invalid or expired key | Mint new key at dashboard; update `.env` |
| Daemon started before `.env` existed | Old process env | `cursor-subagent daemon stop && cursor-subagent daemon start` |

Agents: never log the key. Confirm `.env` exists without printing it (`Test-Path .env` on Windows).

---

## Windows bridge

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `[WinError 10038] An operation was attempted on something that is not a socket` | cursor-sdk `Bridge.launch()` broken on Windows pipes | Use latest cursor-subagent (includes `bridge_bootstrap`) |
| Still fails after update | Stale daemon | Reinstall package, restart daemon |
| Bridge timeout | Antivirus / missing bridge binary | Reinstall `cursor-sdk`; check package includes bridge |

---

## Stack / streaming

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `watch` connects but no events | NATS or gateway down | `cursor-subagent bus start` |
| Connection refused on 17340 | Daemon not running | `cursor-subagent daemon start` or run any spawn (auto-starts) |
| Connection refused on 17341 | Gateway not running | `cursor-subagent bus start` |
| Events in DB but not watch | Gateway not subscribed | Restart bus; check NATS on 4222 |

---

## Cloud agents

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `repo_url is required for cloud runtime` | `--runtime cloud` without `--repo` | Pass `--repo https://github.com/org/repo` |
| Agent starts but no repo access | GitHub/GitLab not connected or read-only | Connect account in Cursor; grant read-write on target repo |
| Wrong agent on resume | Mixed local/cloud flags | Cloud IDs are `bc-*`; pass `--runtime cloud --repo` on resume |
| Expected cloud but got local edits | Omitted `--runtime cloud` | Re-spawn with `--runtime cloud --repo` |
| `wave spawn` not using cloud | Wave path has no runtime/repo passthrough | Use individual `spawn --runtime cloud` per task |

---

## Sessions

| Symptom | Cause | Fix |
| ------- | ----- | --- |
| `Session not found` | Closed or wrong id | `cursor-subagent list --json` |
| Spawn hangs long time | Normal for agent work | Wait; use `watch` in parallel if needed |
| `result.status === error` (in result text) | Agent ran but task failed | Read `result` field; `send` correction or respawn |
| Zombie sessions after crash | Daemon killed mid-run | `cursor-subagent daemon stop`; restart; `close` stale sessions |

---

## After upgrading cursor-subagent

```bash
pip install -e .
cursor-subagent daemon stop
cursor-subagent bus stop
cursor-subagent bus start
cursor-subagent daemon start
```
