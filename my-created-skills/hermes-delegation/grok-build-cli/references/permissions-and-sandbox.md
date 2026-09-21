# Permissions and Sandbox — Grok Build 1.0.5

## Permission order

1. Pre-tool hooks.
2. Deny rules.
3. Ask rules.
4. Allow rules.
5. Remembered project grants.
6. Built-in read-only approvals.
7. Permission mode.

Deny rules win, including under `--always-approve`.

## Rule syntax

Common prefixes: `Bash(...)`, `Read(...)`, `Edit(...)`, `Write(...)`,
`Grep(...)`, `WebFetch(...)`, and `MCPTool(...)`. Pair narrow allows with
explicit denies. `--tools`/`--disallowed-tools` remove tools in headless mode;
`--allow`/`--deny` gate them.

Review-only runs should explicitly deny `Edit`, `Write`, `Bash`, and network
rather than merely omitting auto-approval.

## Permission modes

- `default`: ask with safe read auto-approval.
- `acceptEdits`: file edits without prompt.
- `plan`: planning compatibility mode.
- `auto`: safety-checked automatic behavior.
- `dontAsk`: only pre-approved operations.
- `bypassPermissions`: always approve except denies/hooks.

## Sandbox profiles

- `off`: unrestricted.
- `workspace`: writes cwd, `$HOME/.grok`, and temporary directories.
- `read-only`: blocks workspace writes and child network on supported Linux.
- `strict`: limits reads/writes to narrower paths and blocks child network.

Sandbox is kernel-enforced at process start and sticky for the session. Resuming
with another sandbox profile is refused. Bubblewrap may fail in restricted
containers (`uid map: Permission denied`); do not claim sandbox enforcement when
that happens. Use isolated worktrees plus explicit permission denies instead.
