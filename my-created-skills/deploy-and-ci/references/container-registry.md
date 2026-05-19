# Container registry (thin reference)

Image build and Dockerfile best practices are covered in depth in the **ship-it** skill: `references/docker-registry.md`. Use that for multi-stage builds, non-root users, and layer hygiene.

## CI/CD angle

- **Tag strategy:** semver (`1.2.3`), `latest` only if policy is explicit, often **git short SHA** for traceability.
- **Registries:** Docker Hub, `ghcr.io`, AWS ECR, GCP Artifact Registry — each has login actions and credential helpers.
- **Promotion:** build once in CI, scan (optional), push to staging registry, then promote the **same digest** to production (re-tag or manifest copy) when possible.

## Secrets

- Prefer **OIDC** or short-lived tokens from cloud providers over long-lived passwords in GitHub secrets.
- Never bake secrets into image layers; use runtime env or secret mounts.

## Compose vs Kubernetes

- **Compose** on a VM: document env file and pull policy.
- **Kubernetes:** image digest in manifests; avoid `:latest` in production without automation.

## When to open ship-it

If the problem is **Dockerfile correctness** or image size, use **ship-it**’s Docker reference first; return here to wire **push** and **deploy** steps.
