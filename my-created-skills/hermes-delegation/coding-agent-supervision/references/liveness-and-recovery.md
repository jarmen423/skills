# Liveness and Recovery Signatures

## Buffered but progressing

Signals:
- wrapper has no stdout yet;
- process consumes CPU;
- pytest/build child exists;
- source/test mtimes and diff stat advance.

Action: leave it running and report those artifacts. Do not open the TUI merely
to check.

## Plan-only successful exit

Signals:
- exit code 0;
- output says only “I’ll read…”, “I’ll add…”, or restates the plan;
- worktree diff and timestamps are unchanged.

Action: do not call it complete. Resume the same session once with an explicit
“begin with tool calls and execute now” correction. Verify the worktree again.
After a second plan-only exit, switch worker or implement directly.

## Apparently running but stalled

Signals:
- no useful child;
- no file/diff movement for several minutes;
- negligible CPU;
- only spinner/TUI model-stream process remains.

Action: inspect process tree, terminate the stuck wrapper without deleting the
worktree, and resume the same logical session non-interactively when supported.

## Wrong-worktree reviewer

Signals:
- transcript `pwd` or Git branch differs from the requested review target;
- findings describe code already fixed in the target branch.

Action: discard the verdict. Reissue with an absolute path, exact branch/base,
and mandatory `INVALID_PATH` outcome on mismatch.

## Worker side effects outside the requested diff

Signals:
- staged files despite parent-owned commits;
- scratch scripts or virtualenv directories;
- claimed clean diff that omits a new untracked test.

Action: unstage without discarding, identify/remove only generated artifacts,
mark intended new files with `git add -N`, and rerun the complete gates.

## Max-turns exit with narrated completion

Signals:
- exit 1 with `max turns reached` (or exit 0 after the cap silently truncates);
- transcript tail narrates finished work ("the review is written") in future/
  immediate tense;
- the named artifact does not exist on disk;
- child phases gated on that artifact never started.

Action: do not accept the narration. Inventory durable state (git log per
branch, worktree list, uncommitted diffs, `.pytest_cache/v/cache/lastfailed`
with its mtime), stat every claimed file, then resume the SAME session with a
state-grounded continuation prompt that names the exact missing artifacts and
requires read-back proof before any gated step proceeds. Full anatomy:
`max-turns-orchestration-recovery.md`.

## Quota/auth account switch

After the user switches a CLI account, run a one-minute exact-response smoke
prompt before a long edit. A successful smoke proves current auth/quota; a quota
error is transient account state, not a durable claim that the tool is broken.
