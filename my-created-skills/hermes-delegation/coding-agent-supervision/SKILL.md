---
name: coding-agent-supervision
description: "Use when supervising background coding-agent CLI jobs."
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [coding-agent, supervision, liveness, worktree, review]
    related_skills: [antigravity-cli, grok-build-cli, codex, opencode, muse-code-cli, shared-worktree-integration]
---

# Coding-Agent Supervision

Use this class-level workflow when Hermes runs Grok Build, Antigravity, Codex,
OpenCode, Muse Code, or another coding-agent CLI in the background. Tool-specific
flags stay in the vendor skill (`muse-code-cli` for `muse exec`); this skill
governs supervision, evidence, recovery, and integration.

## User-facing operating style

- Give brief evidence-based check-ins: changed files, test/build child activity,
  process state, and verified results.
- A spinner, `running` label, or exit code 0 is not progress.
- If the user avoids opening a TUI because it may pause or rewind work, monitor
  entirely from the parent. Do not ask them to open it.
- Disclose a genuine stall immediately. Do not silently wait through repeated
  empty polls.
- **Never emit a tool-only turn.** Every turn that runs tools must also carry
  prose: what was launched and why, or what the results mean and what comes
  next. A turn containing only tool calls reads as a stall or a crash to the
  user (corrected twice 2026-09-03: "You just executed tool calls but returned
  an empty response"). Narrate before the batch when it needs context, report
  immediately when results land — especially after background-agent polls,
  status checks, and delegation dispatches.

## Orchestration topology must be explicit

Before launching multi-agent work, say which topology is actually being used:

- **One lead process with internal sub-agents**: one top-level CLI/session receives the whole DAG and is instructed to spawn children.
- **Several independently tracked top-level agents**: the parent launches and monitors one separate CLI/session per task or PR.

Never describe the first topology as “five Grok agents are running” until the child sessions/worktrees exist. State the verified facts instead: one lead process, which child worktrees/session IDs exist, and which phases have not started. OS process trees often hide internal agents; use the vendor session list from each worktree plus Git/file movement as proof. This distinction is user-facing, not an implementation detail—the user may be deciding whether work is independently attributable and recoverable.

## Preferred launch

1. Use a dedicated branch/worktree when concurrent code edits could overlap.
   Isolation is a Git safety measure, not a waiting period: non-overlapping live
   operations may continue when separately authorized.
2. Prefer bounded headless/print mode with an outer process timeout and
   completion notification.
3. State exact path/branch, allowed tools, forbidden side effects, test command,
   and parent-owned commit policy in the prompt.
4. For a newly authenticated account, run a tiny exact-response smoke prompt
   before spending a long task attempt.
5. When requesting a child provider/model override, verify the **actual** model
   recorded by dispatch or completion metadata before assigning the expensive
   work package. Treat the requested pin as unconfirmed until runtime evidence
   matches it; on a mismatch, stop after the smoke and switch to an explicit
   vendor CLI/session rather than waiting for a run from the wrong model.
6. In an isolated worktree, require a coherent verified commit before the
   worker exits; the parent owns review, integration, and push. In a genuinely
   shared checkout, let only the designated integrator commit.

## Liveness evidence ladder

Many print-mode CLIs buffer their prose until completion. Empty stdout alone is
not a stall. Check, in order:

1. wrapper state via process poll/log;
2. process CPU/elapsed time and useful children (pytest, compiler, formatter);
3. `git status --short` and `git diff --stat`;
4. changed-file mtimes/sizes;
5. test artifacts or reports moving.

Report the concrete evidence. If none changes for several minutes and no useful
child is active, treat the worker as stalled rather than trusting the label.

## Attribute the right worker first

When several agents share a checkout, do not infer ownership from the working
directory or process name alone. Correlate process lineage/PTY, session title or
ID, latest session events, and target-file hash movement before saying which
worker is testing, editing, or stalled. Persistent IDE/ACP servers may be hours
old and serve unrelated tasks; PID age is not task age. Redact process arguments
before reporting because API keys often appear there.

A 10–20 second mtime/size/hash sample distinguishes active editing from a long
test: a test has a useful child or moving test output, while repeated source
hash changes with no test child means the worker is editing. If production uses
bind-mounted source, fail closed on startup while runtime-sensitive hashes are
moving so different services cannot load different revisions.

See `references/multi-agent-attribution-and-live-code-freeze.md` for the full
attribution ladder, bind-mount freeze gate, and user-facing report examples.

## Completion is artifact-based

Exit code 0 is necessary but insufficient. A worker that replies only “I’ll
start by…” or repeats the plan has not completed the task.

Before accepting success:

- inspect every changed production file;
- inspect every changed regression test and match each claimed scenario to its actual fixture values and assertions; a green test name or a worker's handoff sentence does not prove the provider-shaped case exists;
- inspect staged, unstaged, and untracked state;
- rerun claimed focused and regression tests in the project environment;
- for a Playwright/`check.cjs` harness: read the vite config for `server.port` and
  `strictPort` before exporting a different PORT env — a hardcoded `strictPort` wins and
  a second start dies with "Port N is already in use". `ss -ltnp` that port: if a check
  process is already using a live listener, do not start another server and do not kill
  it out from under the child; if it is leftover, kill that pid, start ONE, wait until
  that host:port returns HTTP 200, run `check.cjs` yourself, then kill the server. A
  child's `PASS` line is not enough; a curl miss in the first second of bind is a startup
  race, not a dead server. After patching locator strings, read them back — inside
  single-quoted JS, `\\"` is a backslash-quote in the CSS selector, not an attribute
  quote; write `'[data-testid="foo"]'`.
- run compile/lint/build gates and `git diff --check`;
- confirm the response satisfies every named acceptance criterion.

**Prove new regression tests can fail.** A worker's green suite may contain vacuous
tests that pass with or without the fix. Before committing, temporarily revert ONLY
the production expression(s) (e.g. `sed` the fix back to the old expression — never
touch the test file), run the new tests, and confirm they go RED; then restore and
re-run the full gate GREEN. Prefer the targeted expression revert over stashing the
whole prod file: a full stash breaks collection when the test file imports the new
helpers, which proves only dependence, not failure. For a brand-new module, `mv`
only the implementation file aside, run the new tests (expect missing-module RED),
then restore — never `git stash` for this, because stash is repo-global and can
hide another worktree's WIP.

If a session exits plan-only, verify zero/partial edits first. Resume the same
session once with an execution-only correction when supported. If it repeats
the failure, stop spending turns and switch worker or implement directly.

**Grok review stdout is not the verdict.** Headless `grok -p` often flushes only
planning sentences to Hermes. The real text is in
`~/.grok/sessions/<urlencoded-cwd>/<SESSION_ID>/updates.jsonl` as
`agent_thought_chunk` / later `sessionUpdate`. A run with `stop_reason:
cancelled` (or User cancelled a tool) is not complete. Thought chunks that
flipped `PASSED: yes` and `PASSED: no` several times are not a mergeable
review — wait for one final PASSED block, a user-pasted verdict, or a short
resume that emits only that shape. Do not merge on a cancelled thought.

A especially common variant at turn caps: the worker narrates completion
("the review is written… I should provide a summary") but the named artifact
was never written. Distinguish narrated completion from materialized completion:
any claimed file must be stat'd and read back before it counts. When the
claimed artifact is missing, treat everything it gated as not done.

A second stop cause to check before resuming: paid-API exhaustion. An exit
transcript ending in `402 Payment Required: Grok Build usage balance
exhausted` is a hard stop, not a retryable failure — do not relaunch (it
burns the freshly topped-up balance on a doomed run) until the vendor auth
check (`grok inspect --json`) confirms the balance is live again, and ask
the user to top up first. Treat 402 exactly like a turn cap for state
inventory purposes, but never as a liveness problem.

## Long orchestrations: turn caps and mid-run recovery

Multi-phase orchestrations (stacked PRs, implement→review→fix loops) reliably
exhaust headless turn caps; review cycles are what consume turns, not coding.
Design for the cap instead of hoping to fit:

- Require an incremental progress/result artifact written after EACH phase
  (branch, commit, tests, review verdict), never only at the end — a cap kill
  at the end loses the entire summary.
- On `max turns reached` / exit 1: do not restart from scratch and do not trust
  the transcript tail. Inventory durable state yourself: `git log` per branch,
  worktree list, uncommitted diffs, and `.pytest_cache/v/cache/lastfailed`
  (empty object `{}` = the last run finished with zero failures; its mtime
  dates the last test pass without rerunning).
- Resume the SAME worker session with a state-grounded continuation prompt:
  enumerate the verified commits/sessions/worktrees as facts, forbid redoing
  completed phases, name the exact missing artifacts, and restate the
  prohibitions. This converts a dead run into a cheap continuation.
- To confirm a lead worker really spawned internal per-phase sub-agents, run
  `grok sessions list` (or the vendor equivalent) from EACH worktree: the lead
  session lives in the control worktree and each child gets a distinct session
  ID scoped to its own workspace. Absence of a child session in a worktree
  means the phase was not actually delegated.
- Termination rule for the operator: several minutes with no file mtime
  movement, no test child, and no new session entries is a stall; a fresh
  mtime within the last minute during a long quiet stretch is progress.
- Stack boundary tests create expected transitions: an earlier PR's guard
  test (e.g. `test_service_package_does_not_ship_checker_or_matcher`) will
  fail once a later PR adds the excluded module. Flag it to the user as an
  intentional PR-N transition, and make sure the resume prompt says so, so
  the worker deletes/updates the guard instead of treating it as a real
  regression.

See `references/max-turns-orchestration-recovery.md` for a worked recovery
(stack state table, resume prompt anatomy, cost/turn accounting, and the
402-balance-exhaustion stop cause).

### Proving delegation and turn budgets (vendor-neutral)

- A lead worker may spawn internal sub-agents per phase. OS process trees do
  not show them (only unrelated helper children); the vendor's session list
  run from EACH worktree is the reliable evidence — each real child gets a
  distinct session ID scoped to its workspace. No child session in a worktree
  = that phase was not actually delegated yet. For Grok specifically:
  `grok sessions list` per worktree.
- Review cycles consume turns roughly 2-3x faster than coding: a five-PR
  stack with two reviews per PR exhausted a 100-turn cap (~547 model calls,
  ~$12). Budget caps from phase count x (implement + reviews + fixes) with
  headroom, or run reviews as separate bounded invocations.

## Long autonomous sessions: degeneration and the compaction blind spot

A long session producing numeric tool output (profilers, SQL counts, throughput
numbers) can **degenerate mid-task into digit-soup gibberish** that looks like
binary or a cipher — the model regurgitating the repetitive numbers dominating
its context. It is not encryption, not injection, not a terminal bug. It often
happens while the model is still correct: the final sane turns usually carry the
root cause and even the in-flight fix. Full recovery playbook lives in
`agent-work-recovery` (`references/degenerated-agent-session-recovery.md`).

Supervision-side checks when taking over a long-running session:

- **Estimate real context size before trusting token counters**: per-call context ≈
  cumulative content+reasoning chars ÷ ~3.5, NOT `input_tokens/api_calls` (that
  ratio is just the non-cached tail). A session showing ~390k/call average can be
  at ~1M at the peak — the average is a ramp average.
- **Compaction may never fire on some providers**: the trigger reads the provider's
  `usage.prompt_tokens`; on OpenAI-compatible endpoints that report only the
  non-cached tail, the compressor's threshold (e.g. 60% of the window) is never
  crossed and there is no char-based backstop. Verify with
  `SELECT COUNT(*) FROM messages WHERE session_id=? AND compacted=1` in
  `~/.hermes/state.db` — zero after a multi-hour session is the red flag.
- **Take-over rule**: read the last sane assistant turns from the state DB (the
  UI scrollback truncates), verify the in-flight work against live git/container
  state, and resume from the verified root cause rather than restarting the task.

## Worker cleanup traps

Workers may ignore prompt boundaries by staging files, creating virtualenvs, or
leaving scratch scripts. Parent cleanup is mandatory:

- unstage worker edits without discarding them;
- remove only verified generated/untracked artifacts;
- never stash a shared worktree;
- isolated feature worktrees are not an exception: a child that stashes for a
  clean tsc baseline still writes the repo-global stash and can displace the
  production clone. After any mentioned stash/pop, diff `git status` against the
  pre-dispatch snapshot and treat stash as a brief violation;
- after a worker that mentioned stash, diff `git stash list` against the
  pre-dispatch snapshot and never pop — stash is repo-global, so a worktree
  stash can displace the production clone's entries;
- use `git add -N` for intended untracked source/tests so `git diff`, diff stat,
  and `git diff --check` include them;
- re-run verification after cleanup.

A clean plain `git diff --check` before intent-to-add does not prove an untracked
new file is clean.

**Agy review “Sound parts” are not live facts.** 2026-09-05 lifecycle review:
agy agreed on missing `purchase_confirmed.market`, no retention purge, and Q2
drift, then claimed hot-poll XADD is fingerprint-gated and empty `sold` is
forced to `[]`. Live Redis contradicted both (`was_hot` XADD, `"sold":{}`,
~1GB untrimmed stream). Parent live-checks every “sound” claim before telling
Josh the architecture is fine. Read the written `review-notes/*.md`, not the
`agy -p` stdout summary.

**Hermes `delegate_task` 401:** Josh 2026-09-05 — “that doesnt make sense test
the subagents again or use /antigravity-cli.” One no-tools smoke; if it still
401s, switch immediately to isolated-worktree `agy -p --new-project` (path-fence
first). Do not keep retrying the same child provider.

### Antigravity (agy) print-run hygiene (2026-09-03)

A one-shot `agy -p` port (742 insertions, ~6 min under `--print-timeout 25m`,
background + poll) produced a CORRECT feature commit that also carried: 4
`@ts-ignore` band-aids on files outside the task — every one masking a
PRE-EXISTING type error (one hid a real updater API mismatch,
`update.relaunch` missing on the type) — a brand-new `bun.lock`, a tsconfig
`"types"` edit added only to make `tsc -b` pass on a repo whose tsc baseline
was never clean, that edit's tsc-emit artifacts (`vite.config.js/.d.ts`,
`*.tsbuildinfo`), and a deleted `@ts-expect-error` in `vite.config.ts`.
Audit every agy commit file-by-file before landing; the full worked audit is
in `references/agy-print-run-audit-2026-09-03.md`.

- Classify each changed file: feature / justified / out-of-scope. `git ls-tree <parent> -- <path>` proves a "modified" file is actually NEW (never tracked) — solid-shell tracking `bun.lock` does not mean its sibling package does.
- Never demand a clean typecheck on a red-baseline repo (vite builds never typecheck). Gate = zero NEW errors mentioning touched files + total `error TS` count equal to the parent baseline + full tests + production build. Use `tsc -b --force`: stale tsbuildinfo makes plain `tsc -b` report 0 errors because it compiles nothing.
- Test a band-aid by deletion: remove the `@ts-ignore`/tsconfig line, run tsc; if the surfaced error also exists on the parent commit, the band-aid hid a pre-existing issue — revert it AND the unrelated file (unrelated changes must not ride a feature commit).
- `git checkout <parent> -- <path>` fixes only the worktree; the INDEX keeps the worker's version. Between amends, verify with `git status --short` (col 1 = staged) plus `git diff --cached <parent> --stat` — a dropped guard re-entered a later amend exactly this way.
- agy commits under the user's git identity with whatever trailers you scripted; confirm with `git show --stat` + `git log --format=%B`.
- Prompt shape that worked: give the worker its OWN worktree branched off the lead's feature branch so the reference implementation is in-tree (never absolute paths into other clones), inline the task file via `"$(cat TASK.md)"`, and PATH-prepend a wrapper blocking `git checkout|switch|reset|restore|stash|clean|rebase` while exec'ing real git otherwise.
- Hermes terminal hardline-blocks giant multi-statement verification one-liners; put the gate in a `verify-*.sh` inside the worktree and `bash` it (delete before commit).
- Delegation tiering (Josh, 2026-09-03): for a two-lane feature where lane 2 is a mechanical port of lane 1, implement lane 1 directly and dispatch ONE agy one-shot for the port — delegate_task fan-out and doing both by hand were both explicitly declined ("subagents sound like overkill", "take one and dispatch an /agy for the other, just for efficiency"). Dispatch lane 2 only after lane 1 is committed so the port targets a real reference.

## Hermes delegation runner

Use `timeboxed-subagent-orchestration` as the canonical procedure for
`delegate_task` budgets, first-write checkpoints, resume chains, anti-recon
briefs, and timeout recovery. The notes below are supplementary supervision
checks; when they overlap, follow the canonical skill rather than maintaining
two slightly different timing rules.

Runner behavior varies by deployment, so use historical timings only as sizing
evidence, never as a guaranteed timeout.

- **Do not assume a runner-enforced wall-clock cap.** A prompt's `MAX` time or tool count is advisory, and a child can continue far beyond it. Record the deadline at dispatch, inspect transcript plus file movement at the first checkpoint, steer once when the exact edit is known, and stop the worker when it exceeds the operator budget without material progress. Size every dispatch to finish well under 10 minutes; split work packages by file boundary into slices when needed. A single hung command can consume the whole budget.
- **Transport failures masquerade as task failures.** `[Errno 32] Broken pipe` and silent multi-minute stalls mid-generation are provider/API-shape problems (e.g. a responses-API endpoint the runner can't drive), not model or task problems. When the user says they fixed the config, the IN-FLIGHT dispatch may predate the fix — check its transcript for fresh activity before assuming the fix failed. A trivial no-tools smoke dispatch (`SUBAGENT_OK`) proves nothing about tool-heavy dispatches.
- **Recon is the clock-killer.** Pre-bake every recon finding into the brief: absolute test-command path, dependency facts, conventions, env facts. State "start editing immediately; exploration budget 5 minutes MAX". When the fix is fully known, specify edits down to file:line and exact replacement code so the agent only applies and iterates. The strongest form: make the file writes the literal first tool calls, drafted from the brief, with code-reading allowed only afterward to fix failures.
- **Untracked plan files are invisible in fresh worktrees** (`.hermes/plans/` is gitignored). Copy plan docs into the worktree BEFORE dispatching, or agents burn minutes hunting them.
- **Fresh worktrees lack gitignored runtime files** some config modules expect
  at import. Never copy live tokens, session contexts, persona contexts, or
  other production runtime state into a worker checkout. Point configuration
  at committed test fixtures through environment variables; for an
  existence-only glob, use a clearly scoped symlink and exclude it from every
  commit. Treat collection failures caused by missing runtime inputs as a
  fixture/setup gap, not evidence of a product regression.
- **A timed-out agent may have finished the work — or 90% of it.** On timeout/broken-pipe, read the live transcript tail (`~/.hermes/cache/delegation/live/<id>/task-*.log`), then verify tree state (`git status`, `ast.parse` on modified files) and run tests yourself before re-dispatching — never cold-retry. Dispatch a RESUME agent: "what is already done (verified), what remains, do not redo recon." Each resume starts from verified filesystem state; the chain converges. Worked costs: WP2 = 3 dispatches (stall pre-write → all core code written → tests+commit); WP3 = 3 (recon stall → all files written → 1 test fix + commit); WP4 = 2 + orchestrator-side test fixes.
- **Several dispatches dying simultaneously with the SAME storage/lock error is an infrastructure burst, not bad briefs** — colocated writers hammering shared state (multiple live agent processes against one state DB). Do not rewrite the briefs. Verify the burst has settled (stable state-DB WAL/mtime across a few samples), then re-dispatch with a one-line retry rule for that error ("if a tool call fails with 'session storage busy', wait 30s and retry once"). A delegation reported as "owner exited before recording a terminal result; outcome unknown" is a checkpoint, not a verdict: inventory the worktree and transcript yourself and resume from verified state.
- **Controller discipline (user preference, 2026-09-02, stated twice)**: the orchestrator verifies, commits, and reviews — it does not implement unless an agent has stalled twice on the same slice. When falling back, disclose it plainly with the scorecard.
- **Two-stage review pays even when tests are green**: a scoped read-only reviewer ("these commits, these spec sections, max N findings with severities") found 4 MAJOR bugs that 43 passing tests had pinned incorrectly or not at all (one was a tuple-unpack bug that returned the wrong field as a stream ID — no test asserted the ID). Hand findings to a fix agent as another surgical brief, with a new test assertion per finding.
- **Tests written without running are drafts.** One agent wrote both test files then timed out before executing them; running them exposed a stale-signature seed helper AND a real implementation bug (string card_id crashing a fail-open path so every observation was silently swallowed). Budget the dispatch so tests run inside the window, or run them controller-side immediately after.
- **When tests fail, classify which side is wrong before fixing.** Three classes seen: (a) implementation bug — fix the code; (b) test contradicts the spec's own semantics (single-auction close legitimately ends hot state; first-ever fingerprint legitimately emits one event) — fix the test and document why; (c) harness reads the wrong shape (scan-helper not parsing JSON blobs inside HASH values; partition-count mismatch between seed helper and module constants) — make the harness use the same module constants the implementation routes by.
- **Anchored multi-site edits go through a substitution script.** When you have exact insert-before/after anchors, apply them via one Python script whose replacements assert `count(old) == 1` per site — the assert refuses stale anchors, the single pass keeps files internally consistent, and preparing the anchors closely enough to script them caught two latent NameErrors that would have crashed at runtime. Keep the script in /tmp; `ast.parse` the target afterward.
- **Verify the centerpiece before dispatching a resume.** Run the one roundtrip that proves the biggest landed artifact works (proto build→serialize→parse, import-and-call), then state that verification as fact in the resume brief so the next agent never re-litigates finished work.


Independent reviewers frequently inherit a different checkout. Every review
prompt must name the exact absolute worktree and branch and require this guard:

1. First verify `pwd`, Git branch, and base/head.
2. If any differ, return `INVALID_PATH` and stop.
3. Never infer the target from another worktree with a similar branch name.

Discard a verdict whose transcript inspected the wrong checkout, even if its
findings sound plausible. Reissue a compact path-fenced review against the final
diff.

## Review and integration gates

1. Specification review: behavior, ordering, failure semantics, and test meaning.
2. Quality/concurrency/privacy review: lifecycle ownership, races, secret
   handling, KISS/DRY, and unnecessary scope.
3. If either review changes code, rerun both for the changed area.
4. Parent independently verifies and commits only after both pass.
5. **A conditional PASS is an open finding.** "PASS, but F1 needs spec-owner
   sign-off" means the reviewer waived a stated requirement; the controller IS
   the spec owner — either fix the finding or explicitly reject it with a
   reason. Never merge on an open waiver, and never let the waiver silently
   disappear in the next review round without an explicit disposition.
6. **Lock shared contracts before dispatching parallel lanes.** When two
   lanes both consume a wire format, protocol, or generated bindings, the
   controller designs, commits, and pushes the contract (regenerating every
   binding: server protos AND client TS/typed stubs) FIRST, then branches
   each implementer worktree from that contract commit. Two lanes each
   inventing "their" version of the message is the classic drift source, and
   reviewing it after both landed means re-doing a lane.

See `references/liveness-and-recovery.md` for concise incident signatures and
recovery decisions. See `references/delegation-runner-limits.md` for the
worked Hermes-delegation playbook: slice sizing, brief template, timeout/
broken-pipe protocol, and controller verification checklist.
