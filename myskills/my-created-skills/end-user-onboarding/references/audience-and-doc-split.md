# Audience and documentation split

## Two audiences

| Audience | Goal | Typical artifacts |
|----------|------|-------------------|
| **End user** | Install, configure minimally, reach first success | Quickstart, `doctor`, env template, FAQ |
| **Operator** | Host, scale, observe, rotate keys, multi-env | Runbooks, infra-as-code, internal CI, disaster recovery |

## What belongs in end-user docs

- Prerequisites (OS, runtime versions) with **how to verify** (`python --version`, `node -v`).
- **Exact** install commands (`pip install`, `npm install -g`, marketplace install).
- **One** happy path: order of commands from clean machine to first success.
- How to set **non-secret** config (URLs, feature flags) and where secrets go **by name** (never values).
- What `doctor` or health checks mean and **what to do** on FAIL (copy-paste fix commands when possible).

## What belongs in operator docs (not the quickstart)

- Publishing vendor-specific artifacts (databases, WASM modules, internal registries) unless the product **explicitly** ships that as the user’s job.
- Full observability stack (Grafana, Prometheus ports) unless users self-host that edition.
- Multi-node clustering, backup/restore, regional failover.
- CI job definitions, release signing, internal package promotion.

## Splitting a hybrid document

1. Copy the current doc to `docs/operator/` (or `runbooks/`) as the **full** stack guide.
2. Replace the user-facing README quickstart with: prerequisites → install → doctor → setup → first check → **link** “Advanced / self-hosted / full stack”.
3. Add a one-line banner at the top of operator docs: “Not required for hosted or default beta users.”

## Naming consistency

Use the same verbs everywhere: if the product says `doctor` in CLI, do not call it “health check” in README without mapping the terms once.
