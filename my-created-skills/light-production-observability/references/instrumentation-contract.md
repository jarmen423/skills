# Instrumentation Contract Templates

Use these templates as a starting point. Rename fields to match the project, but
preserve the intent: every important operation must be traceable, measurable, and
safe to diagnose.

## Required Operation IDs

| ID | Purpose | Where it should appear |
|---|---|---|
| `trace_id` | End-to-end distributed trace identity | traces, logs, responses, diagnostics |
| `span_id` | Current operation segment | logs emitted inside a span |
| `request_id` | Human-facing request lookup | HTTP responses, logs, support tickets |
| `operation_id` | Domain operation identity | durable records, async workers, logs |
| `attempt_id` | Specific try of a retryable operation | attempt table, step logs, metrics |
| `idempotency_key` | Safe retry/deduplication identity | writes, external provider calls |

Use a domain-specific name when helpful, such as `import_id`, `sync_id`,
`provision_attempt_id`, `workflow_run_id`, or `deployment_id`.

## Structured Event Shape

```json
{
  "timestamp": "2026-05-10T18:40:23.123Z",
  "level": "info",
  "event": "runtime_provision.step_finished",
  "service": "control-plane",
  "environment": "production",
  "version": "git-sha-or-release",
  "operation": "runtime_provision",
  "step": "edge_route_publish",
  "status": "ok",
  "duration_ms": 421,
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "request_id": "req_...",
  "attempt_id": "attempt_...",
  "account_id_hash": "acct_hash_or_internal_id",
  "error": null
}
```

Failure events should keep the same shape and add typed error data:

```json
{
  "event": "runtime_provision.step_failed",
  "step": "bootstrap_validation",
  "status": "failed",
  "error": {
    "code": "BOOTSTRAP_VALIDATION_FAILED",
    "message_safe": "Fresh runtime validation failed.",
    "exception_type": "ValueError",
    "retryable": false
  }
}
```

## Trace Span Plan

Create one parent span for the whole user-visible operation:

- `runtime_provision.sync`
- `memory_import.run`
- `billing_checkout.complete`
- `repo_index.run`

Create child spans for each boundary:

- `db.account.lookup`
- `provider.sprite.create`
- `provider.sprite.service.upsert`
- `edge.kv.publish_route`
- `validator.health_check`
- `webhook.stripe.handle`
- `worker.queue.enqueue`
- `worker.queue.process`

Each span should include:

- `operation.name`
- `component`
- `step`
- `status`
- `duration_ms`
- domain IDs needed for debugging
- provider IDs, request IDs, or response status codes
- safe error code/message on failure

## Metrics

Metric names should be stable and low-cardinality.

| Metric | Type | Labels |
|---|---|---|
| `<operation>_attempts_total` | counter | `environment`, `status`, `failure_code` |
| `<operation>_step_duration_seconds` | histogram | `environment`, `step`, `status` |
| `<operation>_step_failures_total` | counter | `environment`, `step`, `failure_code` |
| `<operation>_inflight` | gauge | `environment` |
| `<dependency>_requests_total` | counter | `environment`, `dependency`, `status_code`, `failure_code` |
| `<dependency>_request_duration_seconds` | histogram | `environment`, `dependency` |

Do not use unbounded metric labels such as raw `account_id`, `email`,
`route_id`, `request_id`, or raw exception messages. Put those in structured
events and traces.

## Diagnostic Response Shape

For `wait=true`, operator, CLI, or setup flows, return enough information to stop
guessing:

```json
{
  "status": "failed",
  "operation": "runtime_provision",
  "attempt_id": "attempt_...",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "failed_step": "bootstrap_validation",
  "error": {
    "code": "BOOTSTRAP_VALIDATION_FAILED",
    "message": "Fresh runtime validation failed.",
    "retryable": false
  },
  "operator_diagnostics_url": "/operator/runtime-routes/rt_.../diagnostics"
}
```

Only expose `operator_diagnostics_url` to users who are authorized to use it.

