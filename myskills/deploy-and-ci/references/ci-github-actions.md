# CI patterns (GitHub Actions)

## Goals

- **PR workflow:** lint, test, build — must be fast and reliable.
- **Release workflow:** publish artifacts only when criteria are met (tag, manual approval, or `release` event).

## Structure

- `ci.yml` — on `pull_request` and `push` to main: install deps, cache, matrix if needed, run tests.
- `release.yml` — on `push` tags `v*` or `workflow_dispatch`: build, attest (optional), publish.

Keep **secrets** out of logs; use `if: github.event_name == 'push' && startsWith(github.ref, 'refs/tags/')` for publish jobs so forks do not accidentally run them without secrets.

## Caching

- **Node:** `actions/setup-node` with `cache: npm` or `cache: pnpm`.
- **Python:** `actions/setup-python` with `cache: pip` or cache keyed on lock files.

## Matrices

Use for OS × Python version or Node version when the product supports multiple; cap combinations to avoid queue time explosion.

## OIDC for publishing

For PyPI **trusted publishing** and similar:

- No long-lived API token in repo secrets when OIDC is available.
- Configure the **issuer**, **repository**, and **workflow** on the registry side; workflow needs `permissions: id-token: write` and the official publish action.

Exact YAML varies by year — follow current **PyPI** and **GitHub** docs when implementing.

## Artifacts between jobs

Use `actions/upload-artifact` and `download-artifact` to pass built wheels or `dist/` to a signing or publish job on the same workflow run.

## Reusable workflows

`workflow_call` is useful for monorepos: one callable workflow per package with inputs for package path and registry target.

## Failure hygiene

- Surface **test names** and **file:line** in annotations when possible.
- Do not mark flaky network calls as required unless retries and timeouts are explicit.
