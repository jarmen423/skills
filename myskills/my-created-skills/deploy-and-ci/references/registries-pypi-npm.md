# Registries (thin reference)

This file orients the agent. **Detailed** packaging steps, `pyproject` layouts, `npm pack` debugging, and TestPyPI flows live in the **ship-it** skill:

- `references/python-pypi.md`
- `references/node-npm.md`

Load those when fixing manifest issues, entry points, or publish failures.

## Decision prompts

| Question | Why it matters |
|----------|----------------|
| Public PyPI vs private index? | URL, auth, and CI secrets differ |
| Scoped npm (`@org/pkg`) vs unscoped? | Publish permissions and registry URL |
| TestPyPI / `npm publish --dry-run` first? | Catches tarball mistakes before immutability |

## Typical CI secrets (names only)

- `PYPI_API_TOKEN` — when OIDC is not used
- `NPM_TOKEN` — automation token for npm publish in CI
- `NODE_AUTH_TOKEN` — often used with `registry-url` in `setup-node`

Never echo these in workflow output.

## Version alignment

- **Python:** version in `pyproject.toml` or tag-driven dynamic version — match release workflow.
- **Node:** `package.json` version must match intended publish; use `npm version` or Changesets per team policy.

## Handoff to ship-it

If the failure is “package empty,” “wrong files in sdist,” “imports fail after install,” run the **ship-it** audit phases before changing CI.
