---
name: agentic-memory-adapter
description: Use when running Agentic Memory with repeatable shell workflows and deciding between quick CLI checks versus deeper MCP dependency and impact analysis.
---

# Agentic Memory Adapter

## Overview

This skill provides a safe shell-first adapter for Agentic Memory operations.
Use it to run deterministic CLI commands with retries/timeouts, then escalate
to MCP tools for multi-step dependency and impact analysis.

## Decision Tree

```text
Start
|
+-- Need fast local action/check?
|   (status, index, search, quick health)
|   -> Use scripts/run_codememory.sh
|
+-- Need dependency graph reasoning or blast-radius analysis?
    (deps, impact, chained analysis)
    -> Start codememory MCP server
    -> Use MCP tools:
       1) search_codebase
       2) get_file_dependencies
       3) identify_impact
```

## Quick Path (CLI Adapter)

```bash
REPO="/abs/path/to/target-repo"
./skills/agentic-memory-adapter/scripts/run_codememory.sh --repo "$REPO" -- status
./skills/agentic-memory-adapter/scripts/run_codememory.sh --repo "$REPO" -- index
./skills/agentic-memory-adapter/scripts/run_codememory.sh --repo "$REPO" -- search "where is neo4j setup?" --limit 5
```

Default behavior:
- Retries failed commands (`--retries`, default `2`)
- Applies a timeout (`--timeout`, default `45s`)
- Emits normalized adapter metadata before raw command output
- Prints concrete recovery steps on hard failure

## Deep Path (MCP Adapter)

1. Start server for a specific repo:

```bash
REPO="/abs/path/to/target-repo"
codememory serve --repo "$REPO" --env-file "$REPO/.env" --port 8000
```

2. In your MCP client, run tools in this order:
- `search_codebase(query, limit)`
- `get_file_dependencies(file_path)`
- `identify_impact(file_path, max_depth)`

Use repo-relative file paths for dependency/impact tools (for example:
`src/codememory/cli.py`).

## Health Check

```bash
REPO="/abs/path/to/target-repo"
./skills/agentic-memory-adapter/scripts/health_check.sh --repo "$REPO"
```

Optional semantic health check:

```bash
./skills/agentic-memory-adapter/scripts/health_check.sh --repo "$REPO" \
  --search-query "authentication flow"
```

## Failure Recovery

`run_codememory.sh` maps common failures to specific fixes:
- Repository not initialized -> run `codememory init` in target repo
- Neo4j unavailable/auth failure -> check `NEO4J_URI`, username/password, and service status
- Missing OpenAI key -> set `OPENAI_API_KEY` in shell or repo `.env`
- Timeout -> increase `--timeout` and retry count, then rerun

Use this adapter for repeatable operations; switch to native MCP tool calls when
you need multi-hop graph analysis in one session.
