# Delegation runner limits — Hermes delegate_task slicing, briefs, failure protocol

This historical scorecard records one runner configuration while orchestrating a multi-package plan via `delegate_task`. Use it for task-sizing evidence, not as a promise of a 600-second cutoff: current runners may continue until the parent explicitly steers or stops them. Companion to the SKILL.md section; this file carries the worked detail.

## Failure tally that produced this reference

| Dispatch | Outcome |
|---|---|
| Full-size WP1 (unbounded) | timeout, 600s, 20 API calls, ZERO edits — entire budget on exploration |
| WP1 slice 1 (pre-baked brief) | ✅ clean success, committed, 25/25 green |
| WP1 slice 2 attempt 1 | broken pipe ~5min, 4 calls, zero edits |
| WP1 slice 2 attempt 2 | timeout, 600s — wrote ~80% of Lua + partial wrappers before dying |
| Slice-2 finish attempt 3 | timeout, 600s — but had FIXED all 4 diagnosed failures; work real, report lost |
| Review-fix agent attempt 4 | timeout, 600s, 12 calls, zero edits — 300s hung grep + hunting untracked spec files |
| WP5a proto+regen (post-transport-fix, tight brief) | ✅ clean first attempt, 6.5 min, zero stalls |
| WP5b attempt 1 | timeout, 26 calls, zero writes — pure recon (recon findings still reused) |
| WP5b resume 1 | timeout — landed 3 of 4 files (171 insertions, verified) |
| WP5b resume 2 | timeout — landed all module functions + partial loop wiring (wire script written to /tmp) |
| WP5b final | (test file + commit slice — the reliable single-artifact shape) |

The scoped read-only review (attempt that DID complete) found 4 MAJOR + 4 MINOR bugs that 43 passing tests missed. Review stages pay even when the suite is green.

## Sizing rule

Right-sized = a competent dev finishes in **under ~7 minutes** with the brief in hand. Split when the task touches >2 files or needs >2 exploratory decisions. Worked split for a shared-contracts WP:

- Slice 1: pure module + golden vectors + tests (one file each).
- Slice 2: Lua scripts + thin wrappers + integration tests (one file each).
- "Write ONE test file + run suite + commit" is the most reliable single-window slice shape observed (4/4 landings).

Phase-level parallelism (three client surfaces in three codebases) is safe; file-level parallelism on one service is not.

## Brief template (in order)

1. **Where**: worktree path, branch, HEAD sha, tree-clean confirmation.
2. **What**: exact files; task text IN the brief; plan files copied into the worktree (untracked plans are invisible to worktrees).
3. **Recon, pre-baked**: test command with absolute interpreter path (`/path/.venv/bin/pytest`), dependency facts ("no fakeredis — scratch redis db15"), test conventions (pytest_asyncio.fixture, strict markers), env facts.
4. **Edits, surgical when known**: file:line + exact replacement code, including ARGV renumbering when Lua signatures change.
5. **Guardrails**: exploration budget 5min MAX; never touch prod db0; no merge/push/deploy; do not weaken tests except where the brief documents the expectation as wrong.
6. **Deliverable contract**: WHY commit message + `Agent-Session-ID`/`Agent-harness` trailers; return sha + pytest tail + per-finding confirmation.

The strongest brief form (verified WP5b final): make the file writes the literal first tool calls, drafted complete from the brief, with code-reading allowed only afterward to fix failures.

## The wire-script technique (anchored multi-site edits)

When the controller has extracted exact patch anchors (insert-before/after context from reading the target file), have the agent — or write controller-side — a **substitution script** instead of N sequential patches:

```python
def sub1(old, new, tag):
    global src
    n = src.count(old)
    assert n == 1, f"{tag}: expected 1 occurrence, found {n}"
    src = src.replace(old, new)
```

Benefits verified live (WP5b): one pass applies every wiring atomically; the
occurrence-count assert refuses to fire on drifted context (catches stale
anchors BEFORE corrupting the file); and preparing the anchors forced reading
the actual code closely enough to catch two latent NameErrors
(`normalize_market(...)` used where only `_normalize_market(market).value`
exists) that would have crashed both new helpers at runtime — found by the
agent while writing the script, fixed in the same pass. Keep the script in
`/tmp`, never in the repo; re-run `ast.parse` on the target after applying.

## Timeout / broken-pipe protocol (resume-chain, verified to convergence)

1. Read transcript tail `~/.hermes/cache/delegation/live/<id>/task-0.log` — `tool ->`/`assistant |` lines show where the clock went.
2. Verify tree before re-dispatch: `git log`, `git status`, `ast.parse` modified files, run tests yourself. Commit verified-green work with proper trailers rather than re-running agents over finished work. **Verify the centerpiece first**: run the one roundtrip/compile check that proves the biggest landed artifact actually works (e.g. build a proto message through the new mapping, serialize, parse back) — then state that verification as fact in the resume brief so the next agent never re-litigates it.
3. Diagnose clock sink: recon → pre-bake brief + forbid exploration; hung command → forbid that class; genuine size → split. Transport stall (silent 5+ min mid-generation, broken pipe) → user-fixed provider config may not reach an IN-FLIGHT dispatch; check transcript freshness, not just the failure label. A zero-write recon window is still harvestable: name its findings in the resume brief so the next agent starts at the writing step.
4. Dispatch a RESUME agent: name the verified on-disk state ("7 files written, parse-checked, 16/17 passing — only X remains"), forbid redoing completed phases, and make file writes the first tool calls where files remain.
5. Retry chains converge. Full-run costs: WP2 = 3 dispatches (stall pre-write → core code + backfill → tests+commit); WP3 = 3 (recon stall → all files → 1 test fix+commit); WP4 = 2 + controller-side test fixes; WP5b = 4 (recon-only → 3/4 files → module fns+wire script → final wiring). Nothing was ever redone from scratch; per-attempt cost is one transcript read + one git status.

## Controller verification (never skip)

- Re-run the slice's tests in the worktree; agent-reported green is a claim.
- "Tests written but never run" are drafts: one agent wrote both test files and died before executing them — running them exposed a stale-signature seed helper AND a real bug (string card_id crashing inside a fail-open catch, silently disabling the whole feature). Budget dispatches so tests run in-window, or run them controller-side immediately.
- Classify failures before fixing: (a) implementation bug → fix code; (b) test contradicts the spec's own semantics → fix test, document why (single-auction close legitimately ends hot state; first-ever fingerprint legitimately emits one event); (c) harness shape mismatch → make the harness use the module constants the implementation routes by (partition_count from SALES_WORKER_PARTITIONS, not a hardcoded 10).
- Grep the diff for contract points (constants, key shapes, precedence rules).
- Check commit trailers before treating a commit as landed.
- **Audit every call site when a worker moves a function.** A moved function
  carries new assumptions about input shape; untouched call sites may now feed
  it a different shape. Worked case (WP5b realtime): `_reconcile_snapshot_rows`
  moved routes→enrich assuming pipeline observations, but the unchanged
  post-filter call site fed it converted snapshot rows whose `observed_at` was
  a build-time stamp — expiry silently neutered there, 50 green tests missed
  it. Read each surviving call site and ask what shape its arguments are NOW.
- **RED-proof every new regression test.** Revert only the fix (e.g. sed-swap
  the two changed call sites back), confirm the new tests fail, restore,
  confirm green. A test that passes both ways is not a regression test.
- **Fix the producer, not the consumer, when tests pin semantics.** Existing
  tests pinned observation-wins expiry; the first controller fix attempt
  (min-over-all-timestamps in the consumer) broke a pinned test. The correct
  fix preserved the genuine pipeline observation through the converter so both
  reconcile passes share one honest clock — consumer semantics untouched.

## Review under time pressure

Cap reviewer scope ("read-only, these commits, these spec sections, max 10 findings with severities"). Route findings to a fix agent as a surgical brief. Add one test assertion per finding so the bug class cannot silently return — the review's MAJOR #1 (a tuple-unpack bug swallowing a return value) survived precisely because no test asserted the returned stream ID.
