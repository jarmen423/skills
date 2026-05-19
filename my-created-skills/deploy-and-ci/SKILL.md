---
name: deploy-and-ci
description: "Take a project from mergeable to reproducibly released and deployed: CI quality gates, GitHub Actions or similar, release workflows, version strategy, registry publishing (PyPI, npm, container registries), environment promotion (staging/production), secrets in CI, test publishes (TestPyPI, npm dry-run), and platform deployment (Cloudflare, Vercel, Netlify, Render, AWS, Kubernetes). Use when setting up CI/CD, release automation, GitHub Actions, deploy pipelines, production deploy, OIDC trusted publishing, container image tagging, or troubleshooting release failures. Delegates deep packaging and manifest work to the ship-it skill; delegates first-run UX and user quickstarts to end-user-onboarding."
---

# Deploy and CI/CD

This skill covers **delivery mechanics**: what runs on every push, what produces artifacts, how versions move to registries, and how deployments reach environments. It does **not** duplicate the full **packaging audit** (use the **ship-it** skill — load `references/python-pypi.md`, `node-npm.md`, `docker-registry.md`, and `doctor-patterns.md` from that skill’s folder; often `~/.claude/skills/ship-it/` or `skills/ship-it/`). It complements **end-user-onboarding** at `skills/end-user-onboarding/` (user-facing install path and doctor UX).

## Phase 0 — Detect delivery signals

Scan the repo root and common paths:

| Signal | Implies |
|--------|---------|
| `.github/workflows/*.yml` | CI/CD on GitHub Actions |
| `.gitlab-ci.yml`, `azure-pipelines.yml` | Other CI (adapt patterns) |
| `pyproject.toml`, `setup.cfg` | Python artifacts (wheel/sdist) |
| `package.json` | Node artifacts; check `workspaces` for monorepos |
| `Dockerfile`, `compose*.yml` | Container images and local stack |
| `wrangler.toml`, `vercel.json`, `netlify.toml` | Platform-specific deploy |

If the task is **primarily** “make `pip install` / `npm install` work from a registry and audit the manifest,” **switch to ship-it** for that workflow, then return here for pipeline wiring.

## Phase 1 — Define the release artifact

Document:

- **What ships:** wheel, npm tarball, Docker image, static `dist/`, Helm chart, etc.
- **Version source:** git tags, `package.json` version, `pyproject` dynamic version, CalVer, etc.
- **Who consumes it:** public registry, private registry, single customer.

Ask when unclear:

> Which **artifact** is the source of truth for production: container image, npm package, Python wheel, or a hosted static bundle? If multiple, which one gates a release?

## Phase 2 — CI plan (quality gates)

Goals:

1. **Fast feedback** on PRs: lint, typecheck, unit tests.
2. **Build** the same artifact users get (reproducible).
3. **Optional** integration tests with services (containers, secrets from CI).

Use [references/ci-github-actions.md](references/ci-github-actions.md) for GitHub Actions patterns (caching, matrices, OIDC).

Classify checks as **required** vs **nightly** so releases are not blocked by flaky optional jobs.

## Phase 3 — Release workflow

Define:

- **Trigger:** tag push (`v*`), manual `workflow_dispatch`, or release branch.
- **Steps:** bump validation (if not tag-driven), build, sign (if applicable), publish to registry.
- **Secrets:** prefer **OIDC / trusted publishing** where supported; otherwise named secrets — never log values.

Thin registry notes: [references/registries-pypi-npm.md](references/registries-pypi-npm.md). Deep packaging steps: **ship-it** references.

Container outline: [references/container-registry.md](references/container-registry.md).

## Phase 4 — CD and environments

For each environment (staging, production):

- **Who deploys:** pipeline only, human approval, or both.
- **Config:** env-specific variables; separate projects or accounts when needed.
- **Rollback:** previous image tag, `npm dist-tag`, or redeploy known git SHA.

Platform-specific high-level notes: [references/platform-notes.md](references/platform-notes.md). Prefer linking to **current** vendor docs for CLI flags; keep the reference minimal so it does not go stale.

## Phase 5 — User intervention (explicit prompts)

**Registry and auth model:**

> Which registry and **scope** apply: npm (public or `@scope`), PyPI, TestPyPI first, GHCR, ECR? Do you use **OIDC trusted publishing** (no long-lived token) or a **stored token** in CI secrets? I will align the workflow to that choice; tell me the organization or repo constraints.

**Deploy target:**

> Production should run on **[platform]**. Is this the **same** account or project as **[existing app]**? If you can **enable the [X] MCP integration**, I can use it with your approval; otherwise add secret **`NAME`** in CI and confirm when set **without pasting the value**.

**Monorepo:**

> Which package’s version **tags** or **changelog** drive the release for this pipeline?

## Phase 6 — Verification gate

Before calling a release “done”:

1. Install or pull the artifact in a **clean** environment (fresh venv, `npm ci` in empty dir, or `docker pull`).
2. Run **ship-it**-style smoke if applicable (import, CLI `--help`).
3. Run **end-user-onboarding** style **doctor** or health check against the deployed URL if the product defines one.

If any step fails, fix forward with a patch version or new build — document the policy.

## Handoff

Provide:

1. Table of workflows and triggers.
2. Required secrets (names only) and OIDC trust configuration summary.
3. Artifact coordinates (package name@version, image:tag).
4. Known gaps (manual steps left intentionally).

## Cross-skill map

| Topic | Use |
|-------|-----|
| pyproject / npm pack / twine / detailed Docker build | **ship-it** skill |
| User quickstart, doctor-first UX, operator vs user docs | **end-user-onboarding** skill (`skills/end-user-onboarding/`) |
