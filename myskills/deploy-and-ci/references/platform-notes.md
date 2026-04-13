# Platform notes (high level)

These stubs avoid copying vendor CLI flags that change frequently. Prefer the official docs for each platform when implementing.

## Cloudflare (Workers, Pages)

- **Workers:** `wrangler deploy`; secrets via `wrangler secret` or dashboard; often tied to git via CI or Wrangler integrations.
- **Pages:** static frontend; build output directory; preview deployments per branch common.

**Intervention prompt:** *“Same Cloudflare account as [other project]? Account id / zone optional for DNS.”*

## Vercel / Netlify

- Git-connected projects; **preview** vs **production** branch mapping.
- Build command and output directory must match the framework.

**Intervention prompt:** *“Production deploy from `main` only, or also from tags?”*

## Render / Fly.io / Railway

- Container or native buildpack; **region** selection matters for latency and compliance.

**Intervention prompt:** *“Target region and whether the database is co-located.”*

## AWS (ECS, Lambda, S3+CloudFront)

- Larger surface: IAM roles, VPC, secrets manager — split into operator runbook sections.

**Intervention prompt:** *“Existing AWS org/OIDC to GitHub, or long-lived keys in CI?”*

## Kubernetes

- Image digest, namespace, Helm values per env; secrets from external store.

**Intervention prompt:** *“Cluster access model: CI deploy key, Argo CD, or human `kubectl`?”*

---

For **npm/PyPI publish** mechanics, use **ship-it**. For **user-facing install** docs after release, use **end-user-onboarding**.
