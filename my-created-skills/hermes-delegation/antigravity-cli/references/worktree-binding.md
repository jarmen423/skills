# Isolated worktree binding for Antigravity

Verified 2026-09-02 with Antigravity CLI 1.1.24.

## Fresh worktree rule

`--project` accepts an existing Antigravity project ID or name. It does not accept a filesystem path. Passing `--project .` reused unrelated saved project state: one path-fence run selected the protected deploy clone and another selected `~/.gemini/antigravity-cli/scratch`.

For a newly created isolated Git worktree:

1. Copy any untracked plan files into the worktree and never include absolute protected-clone paths in the prompt, even in a negative instruction.
2. Run a no-edit smoke with the intended `workdir` and `--new-project`.
3. Require exact `pwd`, Git branch, and HEAD in the response.
4. Only after that passes, launch the edit run from the same worktree with `--new-project`.
5. Inspect the edit conversation's first `run_command` Cwd and verify the protected clone branch/HEAD after launch.

Example:

```text
agy -p 'Run pwd, git branch --show-current, and git rev-parse HEAD. Return only those values. Do not edit.' \
  --new-project --mode plan --print-timeout 2m
```

## Model flag compatibility

`Gemini 3.1 Pro (High)` rejects a separate `--effort` flag with:

```text
--effort is not supported for model "Gemini 3.1 Pro (High)"
```

Remove `--effort`; do not treat this as task failure or silently switch models.
