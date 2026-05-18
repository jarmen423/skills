---
name: light-production-observability
description: "Lightweight version of production-observability. Use when you need a concise production observability checklist for services, APIs, workers, background jobs, queues, or integrations, but do not need the full production-observability review framework or the multi-step workflow depth of observable-workflow-design."
---

# Light Production Observability

Use this skill when a system needs to be debuggable in production without guesswork.
It is intentionally broader than dashboards: the output should make an operator able
to answer "what failed, where, why, for whom, and how do we know the fix worked?"

For multi-step provisioning, ingestion, migration, sync, CI/CD, or external API
orchestration, use `observable-workflow-design` instead of relying on this lighter
checklist alone. For formal design reviews, PR reviews, or launch gates, prefer
`production-observability`.

## Default Stance

- Treat telemetry as part of the product contract, not as optional logging.
- Design for unknown failure modes: traces and structured events must carry enough
  context to answer questions that were not known when the code shipped.
- Prefer correlated signals over isolated dashboards: a useful error response
  should point to a trace ID, attempt ID, job ID, or diagnostic record.
- Make user-facing diagnostics safe and concise; keep secrets, tokens, raw PII,
  and sensitive payloads out of logs and responses.
- Use metrics for aggregate trends and alerting. Use traces and structured events
  for high-cardinality diagnosis such as `account_id`, `route_id`, `job_id`, or
  `provider_request_id`.

## Workflow

1. **Map the critical journey**
   - Name the user-visible operation, success condition, and failure boundary.
   - List every component crossed: frontend, API, queue, worker, database,
     third-party API, edge proxy, CLI, script, or hosted runtime.
   - Identify where control changes hands and where retries or async work begin.

2. **Create the observability contract**
   - Required IDs: `trace_id`, `span_id`, `request_id`, and any domain attempt ID
     such as `job_id`, `provision_attempt_id`, `sync_id`, or `import_id`.
   - Required event fields: `event`, `operation`, `service`, `environment`,
     `version`, `status`, `duration_ms`, `error.code`, `error.message_safe`,
     and the domain IDs needed to find one user/workflow.
   - Required spans: one parent span for the operation, child spans for each
     boundary or expensive dependency call.
   - Required metrics: request/job totals, failures by typed reason, latency or
     duration histograms, active work gauges where useful, and retry counts.

3. **Instrument the code path**
   - Add structured logs/events at start, finish, and failure for each boundary.
   - Propagate W3C `traceparent` where HTTP or message boundaries support it.
   - Add manual spans around external providers, shell scripts, workers, queues,
     database writes, and validation gates.
   - Preserve a safe failure summary in durable state when async work fails.

4. **Define SLOs and alert policy**
   - Choose SLIs that match user-visible behavior: availability, latency,
     correctness, freshness, or workflow completion time.
   - Alert on actionable SLO burn or broken critical journeys, not raw noise.
   - Add dashboards only after the instrumentation can already answer the core
     debugging questions.

5. **Verify with evidence**
   - Run a real happy-path check and a forced-failure check.
   - Confirm the same operation can be followed through response, logs, trace,
     metrics, and durable diagnostic state using its IDs.
   - Do not mark the work complete until a future operator can find the failed
     step from one API response, trace ID, or diagnostic endpoint.

## Minimum Acceptance Checklist

- A single operation has a stable `request_id` and `trace_id`.
- Cross-boundary calls preserve trace context or record the break explicitly.
- Every failure has a typed `error.code`, safe message, and component/step name.
- Logs/events can be filtered by the domain ID that a user or operator has.
- Metrics distinguish success, failure class, latency/duration, and retry volume.
- SLO or release-gate checks exist for the critical journey.
- Secrets, tokens, passwords, connection strings, and raw sensitive payloads are
  not logged.
- Tests or smoke checks prove the observability contract on at least one failure.

## What To Produce

For implementation work, produce the smallest useful set of artifacts:

- Observability contract: IDs, events, spans, metrics, dashboards, and alerts.
- Code changes that emit the contract.
- A diagnostic response or operator command showing how to find one failed run.
- Verification output proving a real success and a real failure are traceable.

## Navigation

Load only what the task needs:

- `references/authoritative-sources.md` for the source map and when each source
  should govern the decision.
- `references/instrumentation-contract.md` for concrete event, metric, and trace
  templates.
- `references/security-and-cost-guardrails.md` for redaction, PII, sampling, and
  cardinality control.
