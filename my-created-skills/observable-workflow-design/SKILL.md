---
name: observable-workflow-design
description: Use when designing, implementing, or debugging multi-step workflows such as provisioning, imports, migrations, sync jobs, billing handoffs, CI/CD deploys, queues, workers, external API orchestration, or any async/background process. Forces a state machine, attempt records, step logs, typed failures, correlation IDs, diagnostics endpoint, retry model, and end-to-end verification before patching.
---

# Observable Workflow Design

Use this skill for workflows where "the request succeeded" is not the same as
"the work finished." Typical examples: account provisioning, runtime setup,
data import, repo indexing, payment-to-entitlement activation, migration jobs,
deployment pipelines, webhook handling, and cross-service sync.

This skill complements `production-observability`. That broader skill covers the
general telemetry stack; this one turns one workflow into a debuggable state
machine.

## Iron Rule

Do not patch a failing multi-step workflow until you can name the failed step and
show the evidence. If two patch-test cycles fail, stop and add/read workflow
diagnostics before changing behavior again.

## Workflow Contract

Create or verify these pieces before implementation is considered complete:

1. **State machine**
   - Explicit states such as `queued`, `started`, `dependency_ready`,
     `service_started`, `validated`, `published`, `active`, `failed`.
   - State transitions are append-only or auditable.
   - Terminal states are clear: `active`, `failed`, `cancelled`, `expired`.

2. **Attempt record**
   - One durable record per try, not only a final status row.
   - Required fields: `attempt_id`, `workflow_name`, `resource_id`,
     `actor_id` or `account_id`, `status`, `current_step`, `failed_step`,
     `failure_code`, `failure_message_safe`, `started_at`, `finished_at`,
     `retry_count`, `trace_id`, and bounded `log_excerpt`.

3. **Structured step events**
   - Emit `step_started`, `step_finished`, and `step_failed` events.
   - Every event includes `attempt_id`, `trace_id`, `resource_id`, `step`,
     `status`, `duration_ms`, and typed error fields when failed.

4. **Correlation propagation**
   - Create a `trace_id` and `attempt_id` at the first request.
   - Propagate them through queues, workers, shell scripts, provider calls,
     webhooks, edge workers, and validation scripts.

5. **Diagnostics surface**
   - Provide an operator report, endpoint, CLI command, or log query that returns
     the latest attempt, step timeline, failed step, provider IDs, and publish
     status.
   - User-facing responses should expose a safe subset and a support/debug ID.

6. **Retry and idempotency model**
   - Define which steps are idempotent, retryable, compensatable, or manual-only.
   - Record provider-created resource IDs before moving to the next step.
   - Retrying must reuse or repair existing resources where safe.

7. **End-to-end verification**
   - Test happy path, forced failure, retry/repair, and partial state cleanup.
   - Verify the diagnostic surface is correct before and after the fix.

## Step Taxonomy

Adapt this to the project:

| Step | Evidence to capture |
|---|---|
| `auth_checked` | principal/account, auth method, safe failure code |
| `entitlement_checked` | entitlement source, plan/trial state, billing status |
| `resource_reserved` | route ID, job ID, idempotency key |
| `provider_created` | provider name, provider resource ID, provider request ID |
| `credentials_written` | destination name only, never secret values |
| `source_uploaded` | artifact name, version/ref, checksum if available |
| `bootstrap_started` | command/script name, version/ref, environment profile |
| `bootstrap_validated` | validation profile and result |
| `service_started` | service name, pid or provider service ID |
| `internal_health_ok` | local health status and latency |
| `edge_published` | route/key ID, publish target, version |
| `public_health_ok` | public URL status and latency |
| `active` | activation timestamp, route version |

## Failure Code Defaults

Use typed codes that can be counted and searched:

- `AUTH_INVALID`
- `ENTITLEMENT_MISSING`
- `IDEMPOTENCY_CONFLICT`
- `PROVIDER_CREATE_FAILED`
- `PROVIDER_AUTH_FAILED`
- `ARTIFACT_UPLOAD_FAILED`
- `BOOTSTRAP_FAILED`
- `BOOTSTRAP_VALIDATION_FAILED`
- `SERVICE_START_FAILED`
- `SERVICE_HEALTH_TIMEOUT`
- `EDGE_PUBLISH_FAILED`
- `PUBLIC_HEALTH_FAILED`
- `CONFIG_MISMATCH`
- `SECRET_MISSING`
- `UNKNOWN_UNCLASSIFIED`

`UNKNOWN_UNCLASSIFIED` is allowed only as a temporary catch-all. Convert repeat
unknowns into specific codes.

## What To Produce

For a new or repaired workflow, produce:

- State machine and step list.
- Attempt storage schema or durable record shape.
- Structured event schema.
- Diagnostic endpoint/CLI/report shape.
- Retry/idempotency rules.
- Metrics and alerts for completion, failure class, and step duration.
- Tests or smoke checks proving one success and one failure are observable.

## Navigation

Load these only as needed:

- `references/workflow-observability-contract.md` for copyable schemas,
  event examples, and endpoint response shapes.
- `references/provisioning-case-study.md` for a concrete case where a hidden
  validation mismatch caused hours of patch-test thrashing.

