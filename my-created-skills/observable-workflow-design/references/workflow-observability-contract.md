# Workflow Observability Contract

This reference gives copyable shapes for stateful, retryable workflows.

## Attempt Table

Use a database table, durable object, KV record, queue result table, or job store.
The storage backend is less important than preserving a per-attempt history.

```sql
create table workflow_attempts (
  attempt_id text primary key,
  workflow_name text not null,
  resource_id text not null,
  account_id text,
  status text not null,
  current_step text,
  failed_step text,
  failure_code text,
  failure_message_safe text,
  trace_id text,
  request_id text,
  retry_count integer not null default 0,
  started_at timestamptz not null default now(),
  finished_at timestamptz,
  updated_at timestamptz not null default now(),
  log_excerpt text,
  metadata jsonb not null default '{}'::jsonb
);

create index workflow_attempts_resource_idx
  on workflow_attempts (workflow_name, resource_id, updated_at desc);

create index workflow_attempts_failure_idx
  on workflow_attempts (workflow_name, failed_step, failure_code, updated_at desc);
```

If the project already has a final resource table, keep it. The attempt table is
for history and diagnosis; the final table is for the current desired state.

## Step Event Shape

```json
{
  "event": "workflow.step_started",
  "workflow": "account_runtime_provisioning",
  "attempt_id": "prov_01...",
  "resource_id": "rt_...",
  "step": "bootstrap_started",
  "status": "started",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "request_id": "req_...",
  "account_id": "acct_...",
  "timestamp": "2026-05-10T18:39:33Z",
  "metadata": {
    "provider": "sprites",
    "artifact_ref": "git-sha"
  }
}
```

Failure:

```json
{
  "event": "workflow.step_failed",
  "workflow": "account_runtime_provisioning",
  "attempt_id": "prov_01...",
  "resource_id": "rt_...",
  "step": "bootstrap_validated",
  "status": "failed",
  "duration_ms": 812,
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "error": {
    "code": "BOOTSTRAP_VALIDATION_FAILED",
    "message_safe": "Runtime bootstrap validation failed.",
    "retryable": false,
    "exception_type": "ValueError"
  },
  "log_excerpt": "Validation profile seeded_fixture expected search results but returned 0."
}
```

## Diagnostics Endpoint

Operator endpoint shape:

```json
{
  "workflow": "account_runtime_provisioning",
  "resource_id": "rt_...",
  "current_status": "failed",
  "latest_attempt": {
    "attempt_id": "prov_01...",
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "status": "failed",
    "failed_step": "bootstrap_validated",
    "failure_code": "BOOTSTRAP_VALIDATION_FAILED",
    "failure_message_safe": "Runtime bootstrap validation failed.",
    "retryable": false,
    "started_at": "2026-05-10T18:39:00Z",
    "finished_at": "2026-05-10T18:40:23Z"
  },
  "steps": [
    {"step": "auth_checked", "status": "ok", "duration_ms": 12},
    {"step": "provider_created", "status": "ok", "duration_ms": 4402},
    {"step": "bootstrap_validated", "status": "failed", "duration_ms": 812}
  ],
  "external_resources": {
    "provider_resource_id": "provider-id-redacted-or-safe",
    "public_route_published": false
  },
  "next_actions": [
    "Fix validation profile or bootstrap configuration.",
    "Retry sync for the same resource after deploy."
  ]
}
```

User-facing response shape:

```json
{
  "status": "failed",
  "resource_id": "rt_...",
  "failed_step": "bootstrap_validated",
  "error": {
    "code": "BOOTSTRAP_VALIDATION_FAILED",
    "message": "Runtime setup failed during validation."
  },
  "support_id": "req_...",
  "retryable": false
}
```

## Metrics

```text
workflow_attempts_total{workflow,status,failure_code}
workflow_step_duration_seconds{workflow,step,status}
workflow_step_failures_total{workflow,step,failure_code}
workflow_inflight{workflow}
workflow_retry_total{workflow,step,failure_code}
```

Avoid `account_id`, `email`, `request_id`, `attempt_id`, or provider resource IDs
as metric labels.

## Validation Profiles

Name validation profiles explicitly:

- `fresh_empty_runtime`: service starts, config exists, DB exists, auth configured,
  health endpoint responds.
- `seeded_demo_runtime`: seeded fixture records exist and known searches return
  results.
- `migration_runtime`: source and destination counts match, checksums or sample
  records match, migration marker written.
- `edge_route_runtime`: private origin reachable through proxy, auth split works,
  public health responds.

A validation profile mismatch should fail with `CONFIG_MISMATCH` or
`BOOTSTRAP_VALIDATION_FAILED` and include the expected profile in diagnostics.

