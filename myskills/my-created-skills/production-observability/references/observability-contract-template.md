# Observability Contract Template

Use this template when designing, reviewing, or hardening a multi-step production workflow. Keep the final contract concise enough that engineers will actually use it, but specific enough that an on-call operator can diagnose failures without guessing.

## 1. Contract Header

```text
workflow_name:
owner:
services/components:
entrypoints:
external_dependencies:
critical_user_journey:
slo_or_business_impact:
```

## 2. Assumptions and Constraints

Document assumptions that affect observability design.

```text
traffic volume:
latency budget:
data sensitivity:
retention requirement:
expected failure modes:
allowed observability tools:
cost sensitivity:
```

## 3. Workflow State Machine

Every production workflow should be explainable as a state machine. Include success, failure, cancellation, timeout, retry, and partial-success states.

| state | entered when | actor/component | timeout | retry/idempotency behavior | emitted event | terminal? |
| --- | --- | --- | --- | --- | --- | --- |
| `received` | request accepted | api/backend | n/a | idempotency key checked | `workflow.received` | no |
| `validated` | input and permissions pass | api/backend | n/a | validation failures are terminal | `workflow.validated` | no |
| `queued` | durable work item created | api/backend | queue sla | enqueue retry with backoff | `workflow.queued` | no |
| `step_running` | worker starts step | worker | step budget | attempt counter increments | `workflow.step.started` | no |
| `step_succeeded` | step completes | worker | n/a | next step starts | `workflow.step.completed` | no |
| `step_failed` | step throws or returns failure | worker | n/a | classify retryability | `workflow.step.failed` | maybe |
| `completed` | all required steps complete | worker/backend | n/a | idempotent replay returns result | `workflow.completed` | yes |
| `failed_terminal` | unrecoverable failure | worker/backend | n/a | user/operator diagnostics created | `workflow.failed` | yes |

Adapt the state names to the real workflow. Do not leave a multi-component workflow with only `success` and `error`.

## 4. Correlation and Propagation

Define where each identifier is created, where it is stored, and how it crosses boundaries.

| identifier | created by | scope | propagated through | visible to user? | required? |
| --- | --- | --- | --- | --- | --- |
| `trace_id` | tracing SDK | distributed trace | W3C `traceparent`; serialized context in jobs | no | yes |
| `span_id` | tracing SDK | operation/span | span context | no | yes |
| `request_id` | edge/api | user request | response header, logs, events | yes | yes |
| `workflow_run_id` | workflow owner | full workflow run | database row, events, spans | maybe | yes |
| `attempt_id` | worker/orchestrator | one execution attempt | job payload, events, spans | yes for support | yes |
| `job_id` | queue/orchestrator | queued work item | queue metadata, spans, logs | no | if async |
| `message_id` | queue/broker | queue message | queue metadata, spans, logs | no | if async |
| `idempotency_key` | client/api | logical operation | database, spans, audit logs | no | if retries/replays possible |
| `external_request_id` | dependency/client | external call | dependency response/header | no | if dependency supports it |

Boundary rules:

- HTTP/service calls: forward W3C `traceparent` and `tracestate` and preserve `request_id` or map it to the downstream request context.
- Queues/background jobs: serialize trace context and workflow IDs into durable job metadata. Use span links when a new trace must begin from a queued message.
- Shell scripts/processes: pass trace context and workflow IDs through environment variables or explicit arguments, then include them in structured output.
- External APIs: record provider name, endpoint/operation, external status, retry count, timeout, and provider request ID when available.

## 5. Trace and Span Design

Use one trace for the user-visible workflow when possible. Use child spans for meaningful steps and external calls. Use links for async work that cannot share a direct parent-child span relationship.

```text
root span: [workflow_name]
  attributes:
    workflow.name:
    workflow.run_id:
    request_id:
    attempt_id:
    account_id/tenant_id if safe:
    idempotency_key_hash if needed:

child spans:
  - validate input
  - create durable workflow record
  - enqueue job
  - run step: [step_name]
  - call external api: [dependency.operation]
  - publish route/config
  - health check
  - finalize workflow
```

Span rules:

- Use low-cardinality span names. Put IDs in attributes, not span names.
- Record `error.type` or equivalent predictable failure class on failed spans.
- Add events to spans for important state transitions, retries, and irreversible side effects.
- Avoid putting secrets, raw tokens, credentials, unredacted payloads, or sensitive PII into span attributes.

## 6. Structured Events and Logs

Emit structured events for state transitions and terminal outcomes. Prefer a small number of consistent event shapes over many ad hoc strings.

Required event families:

```text
[workflow].received
[workflow].validated
[workflow].queued
[workflow].step.started
[workflow].step.completed
[workflow].step.failed
[workflow].retry_scheduled
[workflow].completed
[workflow].failed
[workflow].diagnostic_report_created
```

Minimum fields for workflow events:

```text
timestamp
level
event_name
service.name
service.version
deployment.environment
workflow.name
workflow.run_id
workflow.state
step.name
step.status
trace_id
span_id
request_id
attempt_id
duration_ms
retry.count
failure.code
failure.class
failure.retryable
user_error_code
operator_diagnostic_id
```

Add relevant domain fields such as `account_id`, `tenant_id`, `route_id`, `resource_id`, `sprite_name`, or `plugin_id` only when they are safe, useful, and governed by redaction rules.

## 7. Metrics and SLOs

Use metrics for aggregate health, alerting, and trends. Do not use metrics as the only debugging surface for individual failures.

Example metric families:

```text
[domain]_[workflow]_attempts_total{env, service, workflow, result}
[domain]_[workflow]_failures_total{env, service, workflow, step, failure_class}
[domain]_[workflow]_step_duration_seconds{env, service, workflow, step, result}
[domain]_[workflow]_inflight{env, service, workflow, state}
[domain]_[workflow]_queue_lag_seconds{env, service, workflow, queue}
[domain]_[workflow]_external_dependency_duration_seconds{env, service, dependency, operation, result}
```

Metric label rules:

- Good labels: `env`, `service`, `workflow`, `step`, `result`, `failure_class`, `dependency`, `operation`, bounded `region`.
- Avoid labels: `request_id`, `trace_id`, `attempt_id`, `account_id`, `user_id`, `email`, `raw_error`, `url_with_query`, unbounded resource names.
- Use counters for attempts/failures, histograms for durations, and gauges only for current in-flight/backlog state.
- Prefer SLO-aligned alerts: user-visible error rate, latency, stuck workflow age, queue lag, and error budget burn.

## 8. Failure Taxonomy

Every failure should have a predictable code and class.

| failure class | examples | retryable? | user-facing posture | operator posture |
| --- | --- | --- | --- | --- |
| `validation` | missing field, invalid config | no | ask user to correct input | include field name if safe |
| `authz` | forbidden, missing permission | no | generic permission failure | include principal/role if safe |
| `dependency_timeout` | upstream timeout | yes/maybe | temporary failure | include dependency, timeout, attempt |
| `dependency_5xx` | upstream server error | yes/maybe | temporary failure | include provider status/request id |
| `rate_limited` | dependency 429/quota | yes later | retry later | include quota bucket/reset time |
| `conflict` | resource exists, version mismatch | maybe | retry or refresh guidance | include conflict target if safe |
| `invariant` | impossible state, data mismatch | no | generic failure | high-priority operator detail |
| `worker_crash` | process killed, OOM | yes after recovery | temporary failure | include host/container/job id |
| `unknown` | unclassified exception | maybe | generic failure | require follow-up classification |

Failure code pattern:

```text
[workflow].[step].[class].[specific_reason]
```

Example:

```text
runtime_provision.route_publish.dependency_timeout.cloudflare_api
```

## 9. User-Facing Diagnostics

User-facing diagnostics must be safe, stable, and supportable.

```json
{
  "ok": false,
  "error_code": "provisioning_temporary_failure",
  "message": "We could not finish setup yet. Please retry or contact support with the diagnostic ID.",
  "diagnostic_id": "attempt_123",
  "request_id": "req_abc"
}
```

Rules:

- Show a stable error code and support identifier.
- Do not show stack traces, tokens, raw dependency payloads, credentials, internal hostnames, or sensitive PII.
- Where possible, tell users whether the operation is safe to retry.

## 10. Operator Diagnostics

Provide an operator report, endpoint, or runbook query that can answer the incident questions without code archaeology.

Required fields:

```text
workflow.name
workflow.run_id
current_state
terminal_state
last_successful_step
failed_step
failure.code
failure.class
failure.retryable
trace_id
request_id
attempt_id
job_id/message_id
retry_history
per_step_duration_ms
external_dependencies_called
external_request_ids
redacted_error_summary
user_error_code
created_at/updated_at
owner/service/team
```

The report should make these questions answerable:

```text
what is the request id?
what is the attempt id?
what step are we in?
what exact step failed?
what was the typed failure code?
what is safe to show the user?
what is available only to operators?
what metric/log/trace would prove the fix worked?
```

## 11. Security, Privacy, and Redaction

Set the boundary before defining fields.

- Never log access tokens, refresh tokens, api keys, passwords, private keys, database connection strings, session identifiers, raw authorization headers, or unredacted secrets.
- Hash or tokenize identifiers when direct values are unnecessary.
- Sanitize strings that can contain newlines or control characters to reduce log injection risk.
- Separate audit logs from debug logs. Audit logs should answer who did what, when, and from where; debug logs should explain system behavior.
- Define retention by data class. Do not keep high-detail diagnostic payloads longer than needed.

## 12. Cost and Performance Tradeoffs

Fill this section for every substantial recommendation.

| decision | default recommendation | tradeoff to discuss |
| --- | --- | --- |
| trace sampling | keep all errors; sample successes by traffic and criticality | lower cost can reduce visibility into rare success-path latency |
| structured events | one event per state transition plus terminal result | too many duplicate logs increase ingestion cost and noise |
| metrics labels | low-cardinality labels only | high-cardinality labels can explode series count and cost |
| hot-path telemetry | non-blocking/batched export for normal telemetry | synchronous writes add latency and can fail the request if sink is slow |
| audit records | durable write for security/audit-critical events | stronger guarantees can add latency and operational coupling |
| payload details | record summaries and IDs, not full payloads | less context requires follow-up queries, but reduces privacy and cost risk |
| retention | metrics longer; detailed traces/events shorter unless compliance requires otherwise | longer retention costs more but helps investigate slow-burn issues |

## 13. Verification Plan

Define proof before implementation is considered done.

```text
success query:
  show completed workflows by version over time

failure query:
  group failures by workflow, step, failure_class, and version

trace proof:
  find a single workflow_run_id and show every step span in order

metric proof:
  attempts, failures, duration histogram, queue lag, and stuck workflow age are populated

redaction proof:
  test payload with token/newline/pii and verify logs contain redacted/sanitized fields only

alert proof:
  synthetic failure or replayed event triggers ticket/page at the intended severity
```
