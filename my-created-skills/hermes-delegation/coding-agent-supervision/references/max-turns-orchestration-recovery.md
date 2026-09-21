# Max-Turns Orchestration Recovery — Deal-Capture Stack (2026-08-28)

Worked example of recovering a five-PR Grok Build stack after the lead
orchestrator hit its 100-turn cap, then again after an API balance
exhaustion. Numbers are from those runs; the shape is reusable.

## What the runs looked like

- Launch: one bounded headless Grok lead (`grok -p ... --max-turns 100
  --output-format json --always-approve`) in a control worktree, prompt
  requiring a fresh worktree-isolated agent per PR plus two reviews each.
- Exit 1 #1: `Error: max turns reached` after ~100 turns, 547 model calls,
  ~$12.19, ~7M input / ~797K output tokens. Review cycles consumed the
  turns, not the coding. Transcript tail NARRATED a review document
  ("Ready to write it") that was never written; nothing it gated (PR 3
  commit) happened.
- Exit 1 #2 (after a successful resume that committed PR 3 and PR 4):
  `402 Payment Required: Grok Build usage balance exhausted` after 59
  turns, ~$8.66, ~58.8M total tokens. Hard stop, not retryable — resume
  only after the user tops up, and confirm `grok inspect --json` passes
  before relaunching.
- Run #3 resumed once more to fix PR 5's FAIL reviews and commit.

## Durable-state inventory (what to check, in order)

| Check | Command | What it proved in this run |
|---|---|---|
| Worktrees | `git worktree list` | control + pr1 + pr2 + pr3 existed; pr4/pr5 absent |
| Branch state | `git -C <wt> status --short --branch` + `git log` | PR1 `af5d5222`, PR2 `fc9de88e`, later PR3 `74b77674`, PR4 `f190fdfb` correctly stacked |
| Last test outcome | `.pytest_cache/v/cache/lastfailed` + mtime | `{}` = zero failures; mtime dated the pass minutes before the stop |
| Real delegation | `grok sessions list` run from EACH worktree | lead session in control wt; distinct child session in pr1/pr3 wts; none where a phase hadn't started |
| Claimed artifacts | `stat` / read back every file the transcript claimed | `/tmp/grok-josh/spec-review-pr3.md` did not exist at cap #1; existed with PASS after recovery |
| Result artifact | the end-of-run JSON path | absent at cap, present after final resume |

Key discipline: the transcript tail is a CLAIM. Git, pytest cache, worktree
list, and session lists are EVIDENCE. Rebuild the true state from evidence
before writing the resume prompt.

## Resume prompt anatomy (what worked — twice)

Resume the SAME worker session (`grok -p <prompt> --resume <lead-session-id>`
from the SAME control workdir) with a prompt that has exactly these parts:

1. **Verified current state** — enumerate commits (full SHAs), parentage,
   worktrees, child session IDs, uncommitted files, lastfailed content, and
   the missing artifacts as facts. "Do not redo PR 1 or PR 2."
2. **Immediate task** — the narrow next actions only: materialize missing
   review files, verify they exist by reading them back, fix named findings,
   run gates, commit, continue to remaining phases.
3. **DO NOT block** — all original prohibitions restated (no push, no
   production checkout, no docker/migrations/deploy, no wholesale prototype
   commits) plus the materialization rule: "Do not claim a review exists
   until the file exists and has been read back."
4. **Output contract** — write the result artifact when finished OR a
   partial truthful result at the turn cap, so the next recovery is cheaper.

The first continuation restarted mid-PR-3 instead of paying PR 1–2 again;
the second converted a 402 death into a bounded PR-5-fix-and-commit run.

## Stack boundary-test transitions (expected, not regressions)

An earlier PR's guard test (e.g. `test_service_package_does_not_ship_
checker_or_matcher` in PR 3) legitimately fails once a later PR adds the
excluded module. Name this in the resume prompt so the worker updates the
guard as an intentional transition instead of chasing a phantom regression.

## Operator-facing status reporting pattern

The user asked twice for plain status ("is he actually doing that though",
"see if we're progressing"). What landed as answers:

- Per-PR table: branch, commit SHA, clean/dirty, insertions/deletions, tests.
- Evidence delegation is real: distinct child session ID per worktree — and
  honestly flagging which phases had NO child session yet (not started,
  correctly gated on the parent).
- Liveness: file mtimes sampled to the minute ("PR 3 files changed about one
  minute before the check") beats any spinner claim.
- Cost/turn accounting at each stop (turns, model calls, dollars) so the
  user can judge whether to continue resuming.

## Anti-stall design notes for the NEXT orchestration

- Have the lead write/append an incremental progress artifact after EACH
  phase, not only at the end.
- Budget reviews separately: two reviewers per PR roughly doubles turns; set
  `--max-turns` from phase count × (implement + 2 reviews + fixes) with
  headroom, or run reviews as separate bounded invocations.
- The narrated-but-unwritten artifact failure mode is the reason the resume
  prompt demands read-back proof for every claimed file.
- Check the exit transcript for 402/balance errors before assuming turns ran
  out, and never relaunch on a paid API until the balance check passes.

## Skill-library note

The Grok-specific turn-cap/delegation guidance was ALSO wanted in the
`grok-build-cli` skill, but that skill is user-owned (created_by=None) and
autonomous writes to it are refused — the correct move was recording the
vendor-neutral version here in the curator-managed supervision umbrella and
recommending `hermes curator adopt grok-build-cli` if the user wants it
mirrored into the vendor skill.
