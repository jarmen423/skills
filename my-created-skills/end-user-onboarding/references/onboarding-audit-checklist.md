# Onboarding audit checklist

Use this when reviewing a repo for first-run quality. Record each item as **BLOCKING**, **WARNING**, or **INFO** for **user-facing** documentation and defaults.

## A. Single path

- [ ] There is exactly **one** primary quickstart for the intended product surface (CLI, app, plugin).
- [ ] Steps are **ordered**; no “choose your own adventure” without a default recommendation.
- [ ] Advanced paths link out instead of inline branching in step 1–3.

## B. Prerequisites

- [ ] Minimum language/runtime versions are stated and **match** `engines`, `pyproject`, or CI.
- [ ] Required external tools (Docker, a vendor CLI) are justified; optional tools are labeled optional.

## C. Hidden assumptions

- [ ] No undocumented **ports**; if defaults exist, document collision behavior or how to change them.
- [ ] No **hardcoded** `localhost` in user-facing examples without explaining production replacement.
- [ ] **Environment variables**: every required var is listed with purpose; secrets are never defaulted to real values.
- [ ] **CLI version drift**: if a specific minor version is required, state it or pin in docs.

## D. Doctor and failure UX

- [ ] A preflight or `doctor` exists, or a minimal substitute is proposed.
- [ ] Failures print **what failed**, **why it matters**, and **one** next command or doc link.
- [ ] Exit codes: non-zero on blocking failure (for scripts and CI).

## E. Security

- [ ] No steps ask users to **paste secrets into chat**; prefer env files or secret managers.
- [ ] Example `.env` files use placeholders only (`YOUR_API_KEY`).

## F. Operator leakage

- [ ] Internal-only steps (publish schema, seed observability) are **not** in the default user path.
- [ ] If full stack is optional, the quickstart states what works **without** it.

## G. First success

- [ ] A **single** success criterion is stated early (command output, HTTP 200, exit 0).
- [ ] Troubleshooting section maps common errors to fixes (port in use, wrong URL, auth).
