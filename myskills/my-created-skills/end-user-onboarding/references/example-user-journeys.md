# Example user journeys

Short patterns to align onboarding shape. Adapt commands to the repo.

## 1. CLI tool (PyPI or npm global)

**Path:** Install → verify version → `doctor` (if any) → run primary command with `--help` → one “real” action (e.g. init or check).

**First success:** Primary command exits 0 and prints expected summary.

**Common pitfalls:** Undeclared system deps; wrong Python on PATH; need to distinguish `pip install` vs `pip install -e .` for contributors only.

## 2. Web app + backend

**Path:** Install client deps → set `API_URL` → start backend (or point to hosted URL) → start client → open browser URL → health check.

**First success:** Browser loads UI; health endpoint returns OK.

**Common pitfalls:** CORS; default API URL still `localhost` when user tests from another device; separate ports not listed.

## 3. Editor or host plugin (e.g. OpenClaw)

**Path:** Install plugin via marketplace or documented package → configure host → `doctor` against backend URL → `setup` or equivalent → run one action that proves connectivity.

**First success:** `doctor` PASS and one feature works (e.g. search, sync).

**Common pitfalls:** Host-specific paths; backend URL required but not prompted; mixing **beta user** steps with **operator** full-stack bring-up—split docs.

## Cross-reference

- Packaging gaps: **ship-it** skill.
- Release and deploy automation: **deploy-and-ci** skill in this repo under `skills/deploy-and-ci/`.
