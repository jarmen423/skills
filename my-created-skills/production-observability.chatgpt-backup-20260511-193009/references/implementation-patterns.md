# Implementation Patterns

Use these patterns when translating an observability contract into code or review comments.

## Step Wrapper Pattern

For multi-step workflows, centralize step instrumentation instead of writing ad hoc logs in every branch.

Pseudo-code:

```text
run_step(step_name, context, fn):
  start_time = now()
  emit event workflow.step.started with context + step_name
  start span "[workflow] [step_name]"
  try:
    result = fn(context)
    emit event workflow.step.completed with duration and result summary
    record duration histogram with labels workflow, step, result=success
    return result
  catch error:
    failure = classify(error)
    emit event workflow.step.failed with failure.code, failure.class, retryable, duration
    increment failure counter with labels workflow, step, failure_class
    mark span error with predictable error.type
    create or update operator diagnostic report
    raise typed workflow error
```

The wrapper should ensure every step emits consistent fields, even when the step fails before reaching business logic.

## Boundary Patterns

### HTTP/API Boundary

- Accept or create `request_id` at the edge.
- Accept and forward W3C `traceparent` and `tracestate` when present.
- Start or continue a root span for the request.
- Return `request_id` or safe `diagnostic_id` in error responses.
- Record route templates, not raw URLs with query strings.

### Queue/Worker Boundary

- Store `traceparent`, `tracestate`, `workflow.run_id`, `attempt_id`, and `request_id` in durable job metadata.
- Emit enqueue, dequeue, start, retry, completion, and terminal failure events.
- Track queue lag as a histogram or gauge suitable for alerting.
- Use span links if the worker starts a new trace rather than continuing a parent span.
- Make retries visible: attempt number, next delay, max attempts, and last failure code.

### Shell Script or Child Process Boundary

- Pass correlation context through environment variables or explicit arguments.
- Require structured stdout/stderr lines or a machine-readable result file.
- Convert script exit codes into typed failure codes.
- Capture duration, exit code, sanitized stderr summary, and resource usage if relevant.
- Never pass secrets solely to make logs easier; redact before emission.

Example environment contract:

```text
TRACEPARENT
TRACESTATE
REQUEST_ID
WORKFLOW_RUN_ID
ATTEMPT_ID
STEP_NAME
DEPLOYMENT_ENVIRONMENT
```

### External API Boundary

- Create a client span for every dependency call that matters to the workflow.
- Record dependency name, operation, timeout, retry count, result, normalized status, and external request ID.
- Use idempotency keys for side-effecting calls when the provider supports them.
- Classify dependency failures into timeout, rate limit, quota, auth, conflict, 4xx validation, 5xx, and unknown.
- Do not log raw provider payloads unless explicitly sanitized and retention is acceptable.

### Database or Durable State Boundary

- Persist workflow state transitions and terminal outcomes.
- Make state updates idempotent and include expected previous state when possible.
- Record last successful step, current state, failure code, and updated timestamp.
- Add a stuck-workflow query based on `current_state`, `updated_at`, and workflow timeout.

## Cost and Performance Defaults

Use these defaults unless the user gives stronger requirements.

### Tracing

- Keep all failed traces and important slow traces.
- Sample successful high-volume traces, but preserve enough success data for latency baseline and canary comparison.
- Use low-cardinality span names; store IDs as attributes.
- Avoid huge span attributes and raw payloads.

Tradeoff: lower sampling reduces cost and overhead, but can hide rare success-path regressions or make before/after comparisons weaker.

### Structured Events and Logs

- Emit one structured event per state transition and one terminal result event.
- Avoid duplicating the same error across multiple layers unless each layer adds distinct context.
- Batch and export asynchronously for non-audit telemetry.
- Include high-cardinality diagnostic fields in events when they materially reduce incident time.

Tradeoff: wide events improve root-cause analysis, but ingestion and retention costs grow with event volume and field size.

### Metrics

- Use metrics for aggregate health and alerting, not per-user debugging.
- Keep label sets bounded and predictable.
- Use histograms for durations and queue lag.
- Record failure counters by workflow, step, and broad failure class.

Tradeoff: metrics are cheap and alert-friendly when labels are bounded; unbounded labels can create extreme storage and query costs.

### Synchronous vs Asynchronous Telemetry

- Normal diagnostic telemetry should not block the hot path.
- Security/audit-critical records may need durable synchronous writes.
- If the telemetry sink is slow or down, the application should degrade safely rather than cascade failure.

Tradeoff: synchronous writes provide stronger guarantees, but increase latency and couple product availability to the telemetry path.

### Retention

- Keep aggregate metrics long enough for trends and SLO reviews.
- Keep high-detail traces/events long enough for incident investigation and deploy comparison.
- Keep audit logs according to security/compliance needs.
- Reduce or redact payload details before extending retention.

Tradeoff: longer retention improves forensic analysis but increases cost and privacy exposure.

## Alerting Patterns

Prefer alerts that are actionable and tied to user impact.

Page-worthy examples:

```text
slo burn rate indicates user-visible failures will exhaust budget quickly
critical workflow terminal failures exceed threshold for active users
workflow stuck age exceeds business-critical timeout
queue lag threatens user-visible freshness/latency
external dependency failure causes elevated user-visible errors
```

Ticket/dashboard examples:

```text
single retryable dependency timeout recovered automatically
low-volume flaky step below user-impact threshold
non-critical workflow p95 latency regression without budget risk
one-off validation failures caused by user input
```

Avoid alerts on raw log counts, unclassified exceptions, or every individual failed attempt unless each event requires immediate human action.

## Verification Patterns

Before declaring work production-ready, require evidence.

```text
trace evidence: choose one workflow_run_id and show all step spans in order
log/event evidence: query by attempt_id and see every state transition
metric evidence: attempts, failures, durations, queue lag, and stuck age populate correctly
failure evidence: injected dependency timeout yields typed failure code and safe user diagnostic
redaction evidence: tokens/newlines/raw payloads are absent or sanitized
alert evidence: synthetic or replayed failure hits intended page/ticket path only
cost evidence: estimated event rate, label cardinality, sampling, and retention are acceptable
```
