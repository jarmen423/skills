# Field Catalog and Naming Guidance

Use these fields as a starting point. Adapt names to the codebase, but keep the concepts consistent across services.

## Field Classes

| field | purpose | cardinality | metrics label? | notes |
| --- | --- | --- | --- | --- |
| `timestamp` | event time | high | no | use structured timestamp, not message text |
| `level` | log severity | low | maybe | keep severity meanings consistent |
| `event_name` | event type | low | maybe | use stable names, not sentences |
| `service.name` | emitting service | low | yes | align with OpenTelemetry resource naming |
| `service.version` | deployed version | medium | maybe | useful during deploys/canaries |
| `deployment.environment` | prod/staging/dev | low | yes | never infer from hostname only |
| `workflow.name` | logical workflow | low | yes | e.g. `signup_provisioning` |
| `workflow.version` | workflow schema/version | low/medium | maybe | useful during migrations |
| `workflow.run_id` | one workflow execution | high | no | store in events/traces, not metric labels |
| `workflow.state` | current state | low | yes | state-machine state |
| `request_id` | user/API request | high | no | safe support identifier if designed that way |
| `trace_id` | distributed trace | high | no | correlate logs/events/spans |
| `span_id` | span correlation | high | no | include in logs emitted inside spans |
| `parent_span_id` | span parent | high | no | optional if trace backend handles it |
| `attempt_id` | execution attempt | high | no | required for retries/replays |
| `idempotency_key_hash` | replay correlation | high | no | hash if original key is sensitive |
| `job_id` | queue job | high | no | async workflows |
| `message_id` | broker message | high | no | async workflows |
| `queue.name` | queue/topic | low | yes | keep bounded |
| `worker.name` | worker type | low/medium | maybe | avoid per-pod if unbounded |
| `step.name` | workflow step | low | yes | keep stable and bounded |
| `step.status` | started/completed/failed | low | yes | use consistent enum |
| `duration_ms` | step/event duration | high | no | metric should use histogram seconds |
| `retry.count` | attempt number | low | maybe | bucket if needed |
| `retry.next_delay_ms` | next backoff delay | high | no | event/debug field |
| `failure.code` | typed failure code | medium | maybe | prefer bounded codes |
| `failure.class` | broad class | low | yes | alert on this, not raw message |
| `failure.retryable` | retry decision | low | yes | boolean |
| `error.type` | predictable error type | low/medium | maybe | align with OpenTelemetry when possible |
| `error.message_redacted` | safe summary | high | no | never raw secrets/payloads |
| `http.method` | http method | low | yes | standard semantic field |
| `http.status_code` | response status | low | yes | standard semantic field |
| `url.path_template` | route template | low/medium | maybe | use `/accounts/{id}`, not raw URL |
| `url.full` | full URL | high/sensitive | no | avoid unless explicitly sanitized |
| `external.system` | dependency name | low | yes | e.g. `cloudflare`, `stripe` |
| `external.operation` | dependency operation | low | yes | e.g. `route_publish` |
| `external.request_id` | provider request id | high | no | essential for support/escalation |
| `external.status_code` | provider status | low | maybe | normalize where possible |
| `account_id` | domain account | high | no | useful in events/traces if allowed |
| `tenant_id` | tenant/org | high | no | use carefully; never secret |
| `user_id` | user identity | high/sensitive | no | hash/tokenize if needed |
| `user_error_code` | safe user error | low/medium | maybe | stable and documented |
| `operator_diagnostic_id` | operator report id | high | no | return to user only if safe |
| `redaction.version` | redaction policy version | low | no | helps verify sanitization changes |

## Event Naming

Prefer stable, machine-queryable names:

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

Avoid names that include IDs, raw error messages, or one-off prose:

```text
bad: account_123_provisioning_failed_because_token_expired
bad: oh no cloudflare timed out again
bad: route publish for foo.example.com failed with 500
```

Use fields for details:

```json
{
  "event_name": "runtime_provision.step.failed",
  "workflow.name": "runtime_provision",
  "workflow.run_id": "wf_123",
  "step.name": "route_publish",
  "failure.class": "dependency_timeout",
  "failure.code": "runtime_provision.route_publish.dependency_timeout.cloudflare_api",
  "trace_id": "...",
  "attempt_id": "attempt_2"
}
```

## Cardinality Rules

Use high-cardinality fields where they are valuable for debugging, but put them in the right telemetry type.

- Good in traces/events/logs: `request_id`, `trace_id`, `attempt_id`, `workflow.run_id`, `account_id`, `job_id`, `external.request_id`.
- Usually bad in metric labels: `request_id`, `trace_id`, `attempt_id`, `workflow.run_id`, `account_id`, `user_id`, raw URL, raw error message.
- Good metric labels: `service`, `env`, `workflow`, `step`, `result`, `failure_class`, `dependency`, bounded `region`.

When a high-cardinality field is needed for analysis, prefer a structured event or trace attribute over a Prometheus-style metric label.

## Severity Guidance

| level | use for | avoid |
| --- | --- | --- |
| `debug` | local/development or short-lived deep diagnostics | always-on noisy production paths |
| `info` | normal state transitions and terminal success | per-loop spam without business value |
| `warn` | retryable degradation, slow dependency, unusual but handled condition | user-visible failures that should be errors |
| `error` | failed workflow attempt, terminal failure, data invariant violation | expected validation failures unless they indicate system misuse |
| `fatal` | process/service cannot continue | routine request failures |

## Audit vs Debug Logs

Audit logs and debug logs are not interchangeable.

Audit logs should answer:

```text
who initiated the action?
what action was attempted?
what resource was affected?
when did it happen?
was it allowed or denied?
what durable state changed?
```

Debug/diagnostic logs should answer:

```text
where is the workflow now?
what step ran?
what dependency was called?
how long did it take?
what failure code/class occurred?
what trace/report links connect the evidence?
```
