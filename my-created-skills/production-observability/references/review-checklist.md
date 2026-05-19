# Production Observability Review Checklist

Use this checklist for PR reviews, design reviews, incident hardening, and launch readiness. Mark an item as not applicable only when the workflow truly does not cross that concern.

## Merge or Launch Gates

### Workflow and State

- [ ] The workflow has named states, terminal outcomes, retries, timeouts, and partial-success behavior.
- [ ] Each irreversible side effect has a state transition or event before/after it.
- [ ] The system can report the current state and last successful step for a workflow run.
- [ ] Stuck workflows can be found by query without reading raw logs manually.

### Correlation

- [ ] `request_id` or equivalent is created at the entrypoint and returned or exposed safely.
- [ ] `workflow.run_id` and `attempt_id` exist for multi-step or retryable work.
- [ ] `trace_id` and `span_id` are present in logs/events emitted inside traced work.
- [ ] W3C `traceparent` and `tracestate` or equivalent context crosses service boundaries.
- [ ] Async work preserves context through job metadata, message headers, or span links.
- [ ] External provider request IDs are captured where available.

### Traces and Spans

- [ ] There is a root span for the workflow/request.
- [ ] Each meaningful step has a child span or linked span.
- [ ] Span names are low-cardinality and do not contain IDs.
- [ ] Failed spans include predictable `error.type` or equivalent failure class.
- [ ] Retries and important state transitions are visible on the span or as correlated events.

### Structured Events and Logs

- [ ] State transitions emit structured events with stable `event_name` values.
- [ ] Terminal success and terminal failure are both emitted.
- [ ] Events include workflow, state, step, duration, correlation IDs, and failure classification.
- [ ] High-cardinality diagnostic fields are placed in events/traces, not metric labels.
- [ ] Logs are not only prose strings; they are queryable by ID, state, step, and failure class.

### Metrics and SLOs

- [ ] Attempts, failures, per-step duration, queue lag/backlog, and stuck age are measurable where relevant.
- [ ] Duration metrics use histograms with appropriate buckets.
- [ ] Metric labels are bounded and reviewed for cardinality risk.
- [ ] User-impact SLIs/SLOs are defined or explicitly deferred with a reason.
- [ ] Alerts are tied to SLO burn, user-visible failure, stuck work, queue lag, or actionable dependency failures.
- [ ] Non-actionable anomalies are dashboards or tickets, not pages.

### Failure Classification

- [ ] Failures have typed codes and broad classes.
- [ ] Retryable vs terminal failures are explicit.
- [ ] User-correctable failures are separated from system/operator failures.
- [ ] Dependency failures capture provider, operation, status, timeout, retry count, and provider request ID if available.
- [ ] Unknown failures are allowed only as a fallback and create follow-up work to classify them.

### User and Operator Diagnostics

- [ ] User-facing errors include a safe stable error code and diagnostic/support identifier.
- [ ] User-facing errors do not expose secrets, stack traces, raw provider payloads, or sensitive PII.
- [ ] Operators can retrieve a diagnostic report by request/workflow/attempt ID.
- [ ] Operator diagnostics include current state, failed step, failure code, trace link, timing, attempts, and external request IDs.
- [ ] The report distinguishes what is safe for users from what is operator-only.

### Security and Redaction

- [ ] Tokens, passwords, api keys, auth headers, private keys, connection strings, and raw secrets are never logged.
- [ ] Sensitive identifiers are hashed/tokenized when direct values are not required.
- [ ] User-controlled strings are sanitized to reduce log injection risk.
- [ ] Audit logs and debug logs have distinct purposes, schemas, and retention.
- [ ] Retention matches data sensitivity and business need.

### Cost and Performance

- [ ] Trace sampling policy is stated, including how failed/slow traces are retained.
- [ ] Event/log volume is estimated for the workflow's expected traffic.
- [ ] Metric cardinality has been reviewed and high-cardinality labels removed.
- [ ] Telemetry export is non-blocking unless durability is required for audit/security.
- [ ] Backpressure behavior is defined if telemetry sinks are slow or unavailable.
- [ ] Payload size and retention tradeoffs are documented.

### Proof and Verification

- [ ] A single workflow run can be followed from request to terminal state by ID.
- [ ] A synthetic failure produces the expected span status, event, metric, failure code, and user diagnostic.
- [ ] A redaction test verifies secrets and log-injection strings are sanitized.
- [ ] A launch/fix dashboard or query exists before rollout.
- [ ] The team can state exactly what telemetry would prove the fix worked.

## Review Verdict Language

Use strong language when production diagnosability is missing:

```text
needs changes: this can fail in production without telling us which step failed. add a workflow_run_id, attempt_id, per-step spans/events, typed failure codes, and a user-safe diagnostic id before shipping.
```

```text
acceptable with tradeoff: success traces are sampled to control cost, but failed and slow traces are retained, and aggregate metrics cover attempts, failures, duration, queue lag, and stuck workflows.
```

```text
blocker: account_id/request_id is used as a metric label. move it to structured events/traces and keep metric labels bounded.
```
