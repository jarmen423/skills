# Authoritative Source Map

Use this reference to anchor decisions in standards and mature operational
practice. Prefer current primary docs when the exact API, SDK, or vendor behavior
matters.

## OpenTelemetry

- Source: https://opentelemetry.io/docs/
- Use for: traces, spans, metrics, logs, context propagation, resources, semantic
  conventions, collectors, exporters, and language SDK setup.
- Project rule: OpenTelemetry is the default instrumentation model unless the
  project already has an equivalent standard. Treat traces, metrics, and logs as
  correlated signals, not separate debugging silos.

Key pages:

- Observability primer: https://opentelemetry.io/docs/concepts/observability-primer/
- Signals: https://opentelemetry.io/docs/concepts/signals/
- Baggage: https://opentelemetry.io/docs/concepts/signals/baggage/
- Specification overview: https://opentelemetry.io/docs/reference/specification/overview/

## W3C Trace Context

- Source: https://www.w3.org/TR/trace-context/
- Use for: cross-service trace propagation through `traceparent` and `tracestate`.
- Project rule: every HTTP boundary, worker boundary, queue message, CLI handoff,
  or shell-script handoff should either propagate trace context or record why it
  cannot.

## Prometheus

- Source: https://prometheus.io/docs/practices/instrumentation/
- Use for: metric naming, labels, counters, histograms, and alertable aggregate
  signals.
- Project rule: metrics must be low-cardinality enough to keep the monitoring
  system healthy. Put high-cardinality diagnosis in traces and structured events,
  not unbounded metric labels.

## Google SRE

- Sources:
  - SRE Book: https://sre.google/sre-book/table-of-contents/
  - SRE Workbook: https://sre.google/workbook/table-of-contents/
  - Alerting on SLOs: https://sre.google/workbook/alerting-on-slos/
- Use for: SLIs, SLOs, error budgets, burn-rate alerting, incident response,
  runbooks, and postmortems.
- Project rule: alert humans on user-impacting, actionable conditions. Prefer
  burn-rate and critical-journey alerts over raw CPU, memory, or isolated 500s.

## OWASP Logging Cheat Sheet

- Source: https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
- Use for: security logging, safe event data, log injection prevention, sensitive
  data exclusions, and audit-vs-debug boundaries.
- Project rule: never log access tokens, session IDs, passwords, connection
  strings, encryption keys, raw secrets, or raw sensitive personal data. Sanitize
  CR/LF and delimiter characters in untrusted log fields.

## Honeycomb Observability Engineering Material

- Sources:
  - High cardinality concepts: https://docs.honeycomb.io/get-started/basics/observability/concepts/high-cardinality
  - Structured events: https://www.honeycomb.io/blog/structured-events-basis-observability
- Use for: wide events, high-cardinality debugging, and designing events that can
  isolate one customer, route, job, or provider call.
- Project rule: this is applied industry guidance, not a neutral standard. Use it
  to justify rich structured events, while still managing cost and sensitivity.

## USE And RED Methods

- Brendan Gregg USE method: https://www.brendangregg.com/usemethod.html
- Use for: infrastructure resource checks by utilization, saturation, and errors.
- RED method common practice: request rate, error rate, and duration for services.
- Project rule: use USE for resource bottlenecks and RED for request-facing
  services, but do not let either replace workflow-level diagnosis.

