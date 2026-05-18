# Provisioning Case Study: Hidden Validation Mismatch

This case study is intentionally generic, but it comes from a real failure mode:
a production account runtime started empty, while the bootstrap script reused a
demo/reviewer validation that expected seeded search results.

## What Went Wrong

The final route record said provisioning failed, but the important clue was
buried in a script log excerpt:

```text
Ladybug hosted code search returned no results
```

That was not actually a runtime health failure. It was a validation profile
mismatch:

- Production fresh account runtime should validate that the service starts, the
  database file exists, auth is configured, and health responds.
- Demo/reviewer runtime validation can require seeded fixture records and known
  search results.

The wrong validator prevented the edge route from being published, so external
health checks looked like routing or proxy failures.

## What Would Have Made It Immediate

A workflow diagnostic response like this:

```json
{
  "status": "failed",
  "resource_id": "rt_...",
  "attempt_id": "prov_...",
  "failed_step": "bootstrap_validated",
  "failure_code": "BOOTSTRAP_VALIDATION_FAILED",
  "validation_profile": "seeded_demo_runtime",
  "expected_profile": "fresh_empty_runtime",
  "error": "Seeded search validation returned 0 results.",
  "edge_route_published": false
}
```

## Prevention Pattern

Before patching any provisioning workflow:

1. List the exact step timeline.
2. Confirm the failed step from durable attempt state.
3. Check whether the validation profile matches the account/resource type.
4. Publish route records only after the correct validation profile passes.
5. Return `failed_step`, `failure_code`, and safe `log_excerpt` from any
   synchronous `wait=true` API.

## General Lesson

Do not use "fixture/demo validation" as production bootstrap validation.
Validation profiles are product contracts and should be named in code, logs,
metrics, and diagnostics.

