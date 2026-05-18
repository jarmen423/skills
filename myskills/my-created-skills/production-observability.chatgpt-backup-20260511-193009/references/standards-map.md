# Standards and Source Map

This skill uses the following standards and field-tested guidance as source material. Prefer official standards for normative behavior and use practitioner material for debugging posture and tradeoff framing.

## OpenTelemetry

Use for the core telemetry model: traces, spans, logs, metrics, resources, semantic conventions, context propagation, and log/trace correlation.

Relevant source areas:

- https://opentelemetry.io/docs/concepts/semantic-conventions/
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/semconv/general/trace/
- https://opentelemetry.io/docs/specs/semconv/general/metrics/
- https://opentelemetry.io/docs/specs/semconv/messaging/messaging-spans/
- https://opentelemetry.io/docs/specs/semconv/cicd/

Skill interpretation:

- Use spans for meaningful operations and cross-service causality.
- Use semantic attributes where applicable instead of inventing one-off names.
- Use predictable low-cardinality span names and failure types.
- Correlate logs/events with `trace_id` and `span_id`.
- Treat provisioning and deployment-style workflows as pipeline-like where CI/CD conventions are a useful fit.

## W3C Trace Context

Use for cross-boundary trace propagation.

Relevant source:

- https://www.w3.org/TR/trace-context/

Skill interpretation:

- Preserve `traceparent` and `tracestate` across HTTP/service boundaries.
- For queues, workers, shell scripts, and scheduled jobs, serialize equivalent trace context into job metadata or process environment.
- Do not invent incompatible propagation if standard trace context can be used.

## Google SRE

Use for SLOs, SLIs, paging discipline, error budgets, and burn-rate alerting.

Relevant source:

- https://sre.google/workbook/alerting-on-slos/

Skill interpretation:

- Alert on user-impacting symptoms and SLO burn, not every internal anomaly.
- Pages should be urgent, actionable, and tied to customer impact or imminent risk.
- Low-traffic systems need careful alert design because single failures can create misleading burn-rate signals.

## Prometheus

Use for metrics naming, labels, histograms, counters, and alerting rule discipline.

Relevant sources:

- https://prometheus.io/docs/practices/naming/
- https://prometheus.io/docs/practices/histograms/
- https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/

Skill interpretation:

- Metric names should use a relevant prefix, one unit, and one measured quantity.
- Use `_total` counters and duration histograms in seconds when appropriate.
- Keep labels bounded and avoid high-cardinality IDs in metric labels.
- Use metrics for aggregate health and alerting, not individual incident archaeology.

## OWASP Logging Cheat Sheet

Use for logging security boundaries.

Relevant source:

- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html

Skill interpretation:

- Do not log secrets, access tokens, credentials, raw auth headers, private keys, or sensitive PII.
- Sanitize user-controlled data to reduce log injection risk.
- Separate audit logging from debug/diagnostic logging.
- Treat logs as sensitive production data with retention and access controls.

## Honeycomb Observability Engineering Material

Use for modern debugging posture: wide events, high-cardinality fields, and queryability.

Relevant sources:

- https://docs.honeycomb.io/get-started/basics/observability/
- https://docs.honeycomb.io/get-started/basics/observability/concepts/high-cardinality/

Skill interpretation:

- High-cardinality diagnostic fields such as `account_id`, `request_id`, `attempt_id`, `workflow.run_id`, `job_id`, and `external.request_id` are often essential for root-cause analysis.
- Put high-cardinality details in traces/events/logs designed for queryability, not in metric labels that explode time-series cardinality.
- Prefer wide, structured events over prose-only logs.

## USE Method

Use for infrastructure and resource bottleneck checks.

Relevant source:

- https://www.brendangregg.com/usemethod.html

Skill interpretation:

- For each relevant resource, check utilization, saturation, and errors.
- Apply to CPUs, memory, network, storage, thread pools, queues, file descriptors, workers, and other constrained resources.
- Useful during performance incidents and capacity design.

## RED Method

Use for service endpoint health.

Representative source:

- https://grafana.com/docs/grafana/latest/visualizations/simplified-exploration/traces/investigate/choose-red-metric/

Skill interpretation:

- For request-like services, track rate, errors, and duration.
- Use RED alongside traces, structured events, SLOs, and dependency instrumentation.
- RED is a useful starting point, not a complete observability contract for multi-step workflows.

## Incident Postmortem Patterns

Use for turning surprises into prevention tasks.

Representative sources:

- https://www.pagerduty.com/resources/learn/incident-postmortem/
- https://response.pagerduty.com/after/post_mortem_template/

Skill interpretation:

- Capture timeline, impact, contributing factors, detection gaps, response gaps, and prevention tasks.
- Convert detection gaps into telemetry contracts, not just documentation.
- Keep reviews blameless and system-focused.
