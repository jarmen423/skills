# Devin CLI — sessions and local state (verified 2026-09-22, 3000.10.31)

## Session index

`~/.local/share/devin/cli/sessions.db` — SQLite; open read-only
(`file:...?mode=ro`). Timestamps are **epoch SECONDS**, not milliseconds.
Session ids are memorable two-word slugs (e.g. `checkered-desert`), not UUIDs;
`devin list --format csv` also emits a `short_id` column.

Schema (from `sqlite_master`):

- `sessions(id TEXT PRIMARY KEY, working_directory TEXT NOT NULL, backend_type
  TEXT NOT NULL, model TEXT NOT NULL, agent_mode TEXT NOT NULL, created_at
  INTEGER NOT NULL, last_activity_at INTEGER NOT NULL, title TEXT,
  main_chain_id INTEGER, shell_last_seen_index INTEGER DEFAULT 0, cogs_json
  TEXT, workspace_dirs TEXT, hidden INTEGER NOT NULL DEFAULT 0, metadata TEXT)`
- `message_nodes(row_id INTEGER PRIMARY KEY AUTOINCREMENT, session_id TEXT
  NOT NULL, node_id INTEGER NOT NULL, parent_node_id INTEGER, chat_message
  TEXT NOT NULL, created_at INTEGER NOT NULL, metadata TEXT, UNIQUE(session_id,
  node_id), FOREIGN KEY session_id → sessions(id))` — a forest:
  `parent_node_id NULL` marks roots; `/fork` branches here. `chat_message` is
  JSON with `role`, `content`, `metadata.is_user_input`; real user turns =
  `role='user' AND json_extract(metadata,'$.is_user_input')=1`.
- `prompt_history(id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT NOT NULL,
  timestamp INTEGER NOT NULL, session_id TEXT NOT NULL, is_shell INTEGER NOT
  NULL DEFAULT 0)`
- `refinery_schema_history` (migration bookkeeping)

Notes:

- `backend_type` is `windsurf` on this account — the Codeium/Windsurf heritage
  stack behind Devin (API server `server.codeium.com`). Not a different tool.
- `agent_mode` records the mode in effect (e.g. `bypass`); `model` the pinned
  model (e.g. `swe-2-max`).
- `hidden` marks sidebar-hidden sessions. `devin rm` deletes rows
  irreversibly — there is no soft delete.
- Never print `prompt_history.content` or raw `chat_message` (task text and
  secrets live there). Select metadata columns only.

## Listing and id capture

- `devin list` = interactive picker for the current directory.
- `devin list --format json` — verified shape for an empty directory: `[]`.
- `devin list --format csv` — header `id,short_id,working_directory,last_activity_at,last_activity_ago,title`.
- `-p` stdout does not reliably carry the session id. Capture it by listing in
  the launch directory BEFORE the run and diffing after: the new row's `id` is
  the resume handle. Do this while the run is retained, not after cleanup.
- `-c` continues the most recent session in the current directory; `-r <id>`
  resumes a specific session from any launch directory.

## Export

`--export [PATH]` exports the conversation after each turn in **ATIF** format.
Always pass an explicit path (the value-less default is unspecified). Exports
can contain tool output and task text — audit files, never chat paste.

## Config and data map

- `~/.config/devin/config.json` — observed key paths (values withheld):
  `hooks.{SessionStart,UserPromptSubmit,Stop,PostCompaction,SessionEnd,PreToolUse,PostToolUse,PermissionRequest}`,
  `version`, `devin.org_id`, `shell.setup_complete`, `theme_mode`,
  `agent.model`, `agent.preferred_family_models.swe-2`, `permissions.allow`.
  The `sandbox.*` section (docs: `allowed_domains`, `denied_domains`,
  `network_mode`, `excluded`) also lives here and is ignored unless
  `--sandbox` is active. `--config <PATH>` overrides this file.
- `~/.config/devin/mcp_config.json` — MCP server registrations.
- `~/.config/devin/agents/` — custom subagent profiles (`devin doctor` counts
  these; 3 loaded here: `swe17-coder`, `swe17-general`, `swe17-researcher`).
- `~/.config/devin/cli/`, `~/.config/devin/skills/` — CLI state and
  user-scoped skills.
- `~/.local/share/devin/credentials.toml` — **SECRET STORE**. Never read,
  never print, never copy into a worktree. `devin auth status` shows only the
  path plus endpoints and account name.
- `~/.local/share/devin/summaries/<session_id>.md` — ACP summarizer output.
- `~/.local/share/devin/cli/sessions.db` — the session index above.
- `~/.local/share/devin/cli/_versions/` — versioned binaries;
  `~/.local/bin/devin` symlinks to `_versions/current/bin/devin`.
- `~/.devin/plans/`, `~/.cache/devin/cli/`, `~/.cache/devin/telemetry_state.json`.

## Cross-agent visibility

`devin skills list` reads `~/.agents/skills` and `~/.hermes/skills`, so the
shared skill symlink fan-out shows up in Devin as `/slash` commands with
`[user,model]` triggers. `devin rules list` shows always-on context blobs
(e.g. `global_rules [Windsurf] always-on`). This is how a Hermes-authored
skill becomes Devin context without any Devin-specific install step.
