# Codex Security Port (agent-agnostic security skills)

A port of the security-research skills from OpenAI's `codex-security` plugin
(https://github.com/openai/codex-security) to a form any coding agent can use —
no Codex Security plugin server, desktop workbench, or MCP tools required.

- **Source:** upstream tree at commit `9abe68c` (2026-09-27), directory
  `plugins/codex-security/`.
- **License:** Apache-2.0 (upstream `LICENSE`).
- **What changed:** all plugin machinery was removed and replaced with plain
  file outputs and generic subagent wording; see "What was changed" below.

## What's inside

Eight skills plus a shared `references/` directory. Each subdirectory is a
self-contained skill in the standard `SKILL.md` + frontmatter format.

| Skill | Purpose |
|---|---|
| `finding-discovery` | Discover candidate vulnerabilities in a repo, scoped path, or diff. Carries the upstream discovery checklist (sink/control enumeration discipline, advisory-seeded rows, instance preservation). |
| `validation` | Prove or refute candidate findings with the strongest feasible method: crashing PoC → valgrind/ASan → debugger trace → focused test → interface reproduction → static trace. |
| `triage-finding` | Verdict findings the user already has (SARIF, CVE/advisory, scanner tickets, bug-bounty reports) against the current code: `confirmed` / `not_actionable` / `needs_review`, plus exploitability stack ranking. |
| `fix-finding` | Turn a validated finding into a minimal, verified code fix with a bypass/regression review pass and ordered verification gates. |
| `verify-fix` | Read-only check that a reported vulnerability is actually fixed in the current checkout. |
| `vulnerability-writeup` | Evidence-first, anti-fabrication disclosure reports (release-history tracing, Alice/Bob/Mallory/Eve actors, no invented excerpts or versions). |
| `propose-security-hardening` | Architectural hardening proposals clustered by violated invariant, with real options, tradeoffs, and before/after views. |
| `assess-patch-risk` | Read-only risk assessment of a patch/PR diff: impact, likelihood, regression protection, recoverability, and a `merge`/`revise`/`no_op`/`block`/`hold_for_evidence` recommendation. |

### Shared references (`references/`)

| File | Used by |
|---|---|
| `security-methodology.md` | Full audit workflow (Part 1) + static source/control/sink assessment method (Part 2). Merged from upstream `core-scan.md` + `static-finding-assessment.md`. |
| `security-guidance.md` | How to resolve `SECURITY.md` policy chains (triage, discovery, any scan). |
| `severity-policy.md` | Severity calibration + mechanical policy-adjustment matrix (verbatim from upstream). |
| `validation-guidance.md` | Instance-preserving validation rules, class-specific proof tuples, confidence calibration. |

## Installation / use

- **Keep the whole `codex-security-port/` folder together.** Skills reference
  `../references/...` (shared) and their own `references/` subdirectories.
- Each subdirectory is independently installable in the usual way for your
  agent (copy or symlink the skill directory into your skills path; the shared
  `references/` directory must stay a sibling of the skill directories).
- The skills are mostly independent. A natural pipeline is:
  `finding-discovery` → `validation` → `fix-finding` → `verify-fix`, with
  `triage-finding` for existing backlog findings, and
  `vulnerability-writeup` / `propose-security-hardening` / `assess-patch-risk`
  as standalone deliverables.
- Skills assume an agent with file/search/execution tools. On a restricted
  agent (no shell, read-only), `validation` and `fix-finding` degrade to the
  static-tracing paths, which they explicitly support.

## What was changed from upstream

- **Removed all Codex Security plugin machinery:** MCP tools
  (`record_codex_security_*`, `start_codex_security_*`, workbench candidates,
  drafts, completion/sealing), the desktop workbench, the Daybreak advisory,
  scan handoff tokens, and progress markers. Phase outputs are plain files in
  a review working directory (`.security-review/` by default): a
  `candidates.jsonl` ledger for discovery, per-candidate validation artifacts,
  and report files.
- **Delegation genericized:** upstream's `fork_turns` subagent calls became
  "launch a fresh read-only subagent if your agent supports them, otherwise
  run the same perspective as a separate pass."
- **Dropped host-locked skills:** `security-scan`, `deep-security-scan`,
  `security-diff-scan`, `track-findings`, and the standalone `threat-model`
  wrapper (its substance lives in Part 1 of `security-methodology.md`). The
  Jira/Linear/GitHub connector how-tos in `triage-finding` were replaced with
  an agent-agnostic intake section — wire those to your agent's own
  connectors/REST access if you need them.
- **References relocated:** merged `core-scan.md` +
  `static-finding-assessment.md` into `references/security-methodology.md`;
  moved `security-guidance.md`, `severity-policy.md`, and
  `validation-guidance.md` to the shared `references/` directory; fixed all
  relative paths.
- **assess-patch-risk:** keeps its JSON schema
  (`schemas/patch-risk-assessment.schema.json`) but not upstream's validator
  script, which depended on plugin internals; validate the JSON against the
  schema yourself or with any JSON-Schema tool.
- **Extracted checklists:** the discovery checklist from upstream
  `finding-discovery` and the validation ladder/rules from upstream
  `validation` are now standalone skills with the ledger/receipt machinery
  stripped.

Everything else — the discovery checklist, verdict rules, severity calibration
and policy-adjustment matrix, validation proof tuples, anti-fabrication rules,
and the report/proposal/risk formats — is carried over essentially verbatim.
