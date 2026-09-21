# Multi-agent attribution and live-code freeze

Use this when several local/remote coding agents share one checkout and the user asks which worker is slow, whether it is testing, or whether production can safely start.

## Attribute the worker before judging liveness

A process name or working directory is not enough when multiple agents share a repository. Before reporting status, correlate at least three signals:

1. Process lineage: PID, parent, terminal/PTY, working directory, elapsed time, and descendants.
2. Session identity: current session title/ID and the latest session event or transcript update.
3. Artifact ownership: recent tool log mentioning the path, or repeated content-hash/mtime movement on the worker's target files.

Persistent app servers and ACP/IDE workers can be hours old while servicing many unrelated tasks. Their PID age is not the task age. A newly launched worker in the same checkout may be an unrelated operator loop; do not attribute its activity to the older implementation task.

Redact command-line secrets before showing process output. API keys and tokens commonly appear in long process arguments.

## Distinguish testing, editing, reasoning, and a stall

Sample rather than infer:

- **Long test/build:** a pytest/compiler/linter child exists, or its output/artifacts advance.
- **Active editing:** relevant file size, mtime, or content hash changes across a 10–20 second sample, even with no test child.
- **Model/tool reasoning:** session JSONL advances and CPU/I/O moves, but source artifacts do not.
- **Likely stall:** no useful child, no session-event movement, near-idle CPU/I/O, and no artifact movement for several minutes.

Reading a file does not normally change its mtime. Hash movement is stronger proof than a spinner or wrapper status. Repeated tiny edits to a very large file can be real but inefficient progress; report that distinction plainly.

When a worker is actively editing tests but has not run them, say exactly that. Do not call it a long test, do not call it done, and do not estimate completion from file count alone.

## Shared bind-mounted production checkout

If running containers import code through a bind mount, concurrent edits are operationally significant:

1. Define the runtime-sensitive path set (services, shared modules, compose/config).
2. Hash it before a canary/startup phase and again before each service start.
3. Require a stable interval and no active writer before startup.
4. If hashes change during a staged rollout, stop further starts and fail closed; otherwise different services can load different revisions.
5. Never reset, stash, or clean another worker's uncommitted work to obtain stability.

An emergency monitoring loop may continue read-only checks while code changes, but it must not start bind-mounted production services until the source is frozen.

## User-facing report shape

Lead with the direct classification:

- "No long test is running; the worker is actively editing regression tests."
- "A focused pytest child is running; output last advanced at …"
- "The worker appears stalled: no child/session/file/CPU movement for …"

Then provide 2–4 concrete evidence points and the next intervention threshold. If active but inefficient, give a bounded steering prompt such as: stop expanding coverage, run the focused suite now, fix only observed failures, then run final verification.
