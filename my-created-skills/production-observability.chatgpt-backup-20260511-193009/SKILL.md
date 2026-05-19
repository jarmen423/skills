---
name: production-observability
description: >-
  design, review, and debug production observability for multi-step systems before or during implementation. use when planning or changing workflows with background jobs, workers, queues, scripts, external apis, provisioning, deployment pipelines, or cross-service boundaries; when reviewing pull requests for observability gaps; or when diagnosing incidents where traces, structured events, metrics, correlation ids, redaction, slo alerts, cost, or performance tradeoffs matter.
---

# Production Observability

## Overview

Use this skill to make observability a required part of production system design, implementation, review, and incident hardening. Prefer an actionable observability contract over vague advice: identify what telemetry proves where work is, what failed, who is affected, what is safe to show users, what operators can inspect, and whether a fix worked.

## Operating Principle

Do not treat telemetry as an after-the-fact patch for surprises. For any multi-step production workflow, first make the workflow observable enough that a future failure is diagnosable without guessing.

If the user is asking for a code change, design review, debugging help, or incident response and observability is missing, explicitly call out the gap before or alongside the implementation advice. Make reasonable assumptions rather than blocking on questions unless a missing detail materially changes safety, cost, or correctness.

## Workflow

1. **Choose the operating mode.**
   - New feature or system design: produce an observability contract before implementation details.
   - Implementation or PR review: identify missing instrumentation, risky gaps, and minimal changes required before merge.
   - Incident/debugging: identify the fastest diagnostic path with current telemetry, then specify what must be added to prevent repeat ambiguity.
   - Postmortem/hardening: turn detection gaps into concrete telemetry, alerts, runbooks, and prevention tasks.

2. **Map the workflow as a state machine.**
   Name every meaningful state and terminal outcome. Include retries, timeouts, compensation/rollback, idempotency behavior, and partial-success states. Avoid advising a patch until the exact failing step would be knowable from telemetry.

3. **Define correlation and propagation.**
   Require stable identifiers across boundaries: `trace_id`, `span_id`, `request_id`, `workflow_run_id`, `attempt_id`, `job_id`, `message_id`, `idempotency_key`, and relevant domain IDs. Require W3C `traceparent` and `tracestate` propagation for HTTP-like boundaries, and equivalent serialized context for queues, workers, shell scripts, scheduled jobs, and external APIs.

4. **Design the telemetry contract.**
   Cover traces/spans, structured events/logs, metrics, and audit records separately. Use OpenTelemetry-style semantic attributes where possible. Use wide, queryable events for high-cardinality diagnostic fields. Keep metric labels low-cardinality.

5. **Classify failures.**
   Require typed failure codes and failure classes. Distinguish retryable, permanent, user-correctable, dependency, rate-limit, quota, timeout, conflict, invariant, and unknown failures. For every failure class, specify what is shown to the user and what is reserved for operators.

6. **Design diagnostics.**
   Require a user-facing diagnostic response containing a safe error code plus a supportable identifier. Require an operator diagnostic report or endpoint that can answer: current state, last successful step, failed step, failure code, trace link, attempt history, timings, retries, external request IDs, and redacted error details.

7. **Discuss cost and performance tradeoffs.**
   Every implementation recommendation must mention relevant tradeoffs: trace sampling, event volume, metric cardinality, payload size, synchronous vs asynchronous telemetry writes, retention, egress/storage costs, hot-path latency, and backpressure behavior if telemetry sinks are slow.

8. **Define alerting and proof.**
   Tie alerts to user impact, SLO burn, stuck workflows, queue lag, or actionable dependency failures. Avoid paging on noisy internals. Define the exact metric, trace query, log query, or diagnostic check that proves the system is healthy and proves a fix worked.

## Required Output Gates

For substantive answers, include these gates either as sections or clearly marked bullets:

- **state machine:** states, transitions, terminal outcomes, retries, and timeouts.
- **correlation:** which IDs exist, where they are created, and how they cross boundaries.
- **telemetry:** traces/spans, structured events/logs, metrics, and audit logs.
- **failure taxonomy:** typed failure codes/classes and retryability.
- **user diagnostics:** safe user-facing error code/message and support identifier.
- **operator diagnostics:** report/endpoint fields or query path.
- **alerts/slos:** what should page a human, what should create a ticket, and what should only be dashboarded.
- **cost/performance:** explicit tradeoffs and a recommended default.
- **proof:** what telemetry would show the fix or launch is working.

If the user asks for a shorter answer, compress these gates but do not silently omit correlation, failure taxonomy, redaction, cost/performance, or proof.

## Default Output Patterns

### Observability Contract

Use this for new systems, new workflows, design docs, and larger refactors. Load `references/observability-contract-template.md` when a structured contract is useful.

Recommended shape:

```text
# Observability Contract: [workflow]

## Assumptions
## Workflow state machine
## Correlation and propagation
## Trace/span design
## Structured events and logs
## Metrics and SLOs
## Failure taxonomy
## User-facing diagnostics
## Operator diagnostics
## Security and redaction
## Cost/performance tradeoffs
## Verification plan
```

### PR or Implementation Review

Use this when reviewing code, patches, architecture notes, or implementation plans. Load `references/review-checklist.md` for the review rubric.

Recommended shape:

```text
## Observability review verdict
## Must fix before production
## Should fix soon
## Acceptable tradeoffs
## Suggested instrumentation patch
## Verification queries/checks
```

### Incident Diagnostic Ladder

Use this when the user is debugging an active or recent production issue.

Recommended shape:

```text
## What to identify first
## Current likely blind spots
## Fastest diagnostic path with existing telemetry
## Telemetry that should have existed
## Hardening changes
## Proof the incident class is fixed
```

## Resource Guide

- Use `references/observability-contract-template.md` for a fillable design template.
- Use `references/field-catalog.md` for standard fields, cardinality guidance, and event naming.
- Use `references/implementation-patterns.md` for boundary-specific patterns, step wrappers, sampling, and cost/performance defaults.
- Use `references/review-checklist.md` for PR/design/incident hardening gates.
- Use `references/standards-map.md` to ground advice in the bundled standards and source set.
