# Security And Cost Guardrails

Observability systems often become secondary data stores. Treat them as part of
the security boundary.

## Redaction Defaults

Never log or emit:

- access tokens, refresh tokens, API keys, bearer headers, session IDs
- passwords, private keys, signing secrets, encryption keys
- database connection strings and cloud credentials
- raw payment data or Stripe secrets
- raw health, legal, financial, or other sensitive personal data
- raw request/response bodies unless a route-specific review says it is safe

Prefer:

- stable internal IDs over emails
- salted hashes for user-facing identifiers if analysts need grouping
- typed `error.code` over raw provider exception strings
- `message_safe` for user/support display and `message_debug` only in restricted
  operator logs when justified

## Log Injection Defense

Sanitize untrusted text before writing logs:

- strip or escape carriage returns and line feeds
- avoid delimiter-sensitive plain-text logs for user-controlled fields
- prefer JSON encoders over string concatenation
- bound field lengths for provider messages, paths, command output, and payload
  excerpts

## Cardinality And Cost Rules

High-cardinality fields are essential for debugging, but they belong in the
right signal.

- Metrics: low-cardinality labels only.
- Logs/events: rich high-cardinality fields are acceptable when retention,
  access control, and cost are understood.
- Traces: include enough domain IDs to find one operation, route, account, or
  provider call.
- Sampling: never sample away rare failure classes without a deliberate policy.
- Retention: keep raw verbose telemetry short-lived; keep durable failure
  summaries longer.

## Access Control

Split visibility:

- User-facing errors: safe status, step, typed reason, next action.
- Support/operator diagnostics: trace ID, attempt ID, provider status, redacted
  command excerpts, and retry state.
- Restricted security logs: authentication and authorization events, credential
  lifecycle, secret rotation, and suspicious access.

## Shell And External Process Output

Shell scripts and provider CLIs are common leak points.

- Pass secrets via files or environment variables only when needed.
- Redact command echoes, `set -x`, stdout, and stderr before storing them.
- Capture bounded excerpts with explicit truncation markers.
- Record exit code, timed-out/killed status, and safe failure code separately
  from raw output.

