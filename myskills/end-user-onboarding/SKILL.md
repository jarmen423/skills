---
name: end-user-onboarding
description: "Shape first-run and beta onboarding so end users get value without inheriting operator infrastructure. Covers one supported install path, doctor or preflight validation, separating operator runbooks from user-facing docs, surfacing hidden assumptions (ports, localhost defaults, CLI versions, env vars), port collisions, zero-infra onboarding goals, and clear first success criteria. Use when improving quickstart, installation friction, beta onboarding, private beta docs, plugin first install, setup after pip or npm install, preflight checks, or when users hit works-on-my-machine failures. Does not replace product code—agents apply this to docs and UX design alongside engineering. For PyPI/npm packaging and registry publish depth, use the ship-it skill; for CI/CD pipelines and deploy targets, use deploy-and-ci."
---

# End-user onboarding

End users should follow **one numbered path** from install to **first verified success**. Operators follow **different** steps in a runbook. This skill helps an agent audit docs and onboarding design, propose a doctor or preflight contract, and **stop to ask the user** when a product decision is required.

## Principles

1. **One supported path** for the consumer. Everything else is optional or operator-only.
2. **Validate before acting** — preflight (doctor) should run before setup that writes config, when the product provides it.
3. **No silent assumptions** — ports, URLs, CLI versions, and required services must be explicit or detected with a clear failure.
4. **Secrets** — never echo or log secret values. Offer a safe channel (MCP with user approval, OS secret store, or manual `.env` with a confirmation step).

## Phase 0 — Classify audience

If unclear, ask once:

> Are we optimizing onboarding for **someone who installs and uses the product** (end user), or **someone who hosts services, keys, and regions** (operator)? I will keep end-user steps minimal and move hosting, database provisioning, and internal publish steps to an operator runbook.

## Phase 1 — Single supported path

Inventory `README`, `docs/*INSTALL*`, `docs/*QUICK*`, package READMEs. Build a **user path** table:

| Step | Command or action | Success signal |
|------|-------------------|----------------|
| 1 | … | … |

Flag **hybrid** docs that mix dev stack (full monorepo, Spacetime publish, Grafana ports) with user steps. Recommendation: **split** — end-user quickstart vs. `docs/operator/` or `RUNBOOK.md`.

Ask if the product surface is ambiguous (monorepo):

> Which package or app is the **primary surface** for first-time users (CLI name, plugin id, or web URL)? I will align the numbered path to that surface only.

## Phase 2 — Environment honesty (audit)

Run the checklist in [references/onboarding-audit-checklist.md](references/onboarding-audit-checklist.md). Classify each finding for **user-facing** docs as BLOCKING, WARNING, or INFO.

Pay special attention to:

- Default `localhost` or fixed ports in examples that ship to users without “replace with your host” guidance.
- Undocumented environment variables.
- Steps that require internal tools (e.g. publishing vendor databases) on the **user** path — those belong under operator docs per [references/audience-and-doc-split.md](references/audience-and-doc-split.md).

## Phase 3 — Doctor or preflight contract

Define what **PASS** means:

- Required runtime (language version).
- Required configuration (env vars or config keys) with **actionable** error text when missing.
- Network checks (backend URL, auth, optional dependencies).

If the repo already has a `doctor` or `preflight` command, map checks to user-visible messages. If not, propose a minimal **checklist script** or subcommand that returns non-zero on failure and prints **fix commands**, not stack traces only.

For implementation patterns, load the **doctor-patterns** reference from the **ship-it** skill (install separately; common paths include `~/.claude/skills/ship-it/references/doctor-patterns.md` or a repo-local `skills/ship-it/references/doctor-patterns.md`) — do not duplicate long code samples here.

## Phase 4 — First success criterion

Agree on **one** measurable outcome for “onboarding complete,” for example:

- `doctor` exits 0, or
- One documented command prints an expected banner or health JSON.

Put that criterion at the **top** of the user quickstart after prerequisites.

## Phase 5 — User intervention (explicit prompts)

Use these patterns when the agent cannot infer a safe default. Adapt product names and command names to the repo.

**Hosting or deploy target (static site, API URL, plugin backend):**

> We need a **production URL** (or hosting target) for [component]. Do you already use a provider (e.g. Cloudflare, Vercel, Netlify, AWS) for a related project? If you **connect the [X] MCP server** (or integration), I can drive deploy steps from here. Otherwise, add the required token to `.env` (or CI secrets) using the name documented in README, tell me when it is set **without pasting the secret**, and I will continue.

**Aligning with existing infra:**

> Another part of your stack is already on [provider]. Should this component use the **same** account or project? If yes, I need confirmation of [project id / zone / account] or a pointer to where it is configured.

**Monorepo entrypoint:**

> I see multiple packages. Which one should **first-time users** install or open first? I will trim the quickstart to that surface and link to advanced setup.

**Operator-only work mistaken for user path:**

> Step [N] (e.g. publishing an internal schema or starting observability stack) is **operator** scope. I recommend moving it to [runbook path]. Should I draft that split?

## Phase 6 — Handoff

Deliver:

1. Revised **numbered** user path (or a PR-style edit list).
2. List of **BLOCKING** doc or UX items.
3. Doctor or preflight checklist summary.
4. Operator-only items relocated or flagged.

## Relationship to other skills

- **ship-it** — packaging, manifests, registry publish, detailed doctor **code** patterns. Use when the blocker is “not installable from PyPI/npm” or versioned artifacts.
- **deploy-and-ci** — CI workflows, release automation, deployment platforms. Use when the blocker is pipeline or production deploy.

See [references/example-user-journeys.md](references/example-user-journeys.md) for short patterns (CLI, web + backend, editor plugin).
