---
name: execution-grade-planning
description: Use when converting broad product/architecture plans into implementation-agent-ready execution packets with minimal inference risk. Especially useful for evals, safety boundaries, product gates, multi-PR stacks, and users who want conceptual decisions made before coding.
---

# Execution-Grade Planning

Use this skill when a user wants to plan work deeply enough that implementer agents do not have to infer product context or make hidden product decisions.

## Core principle

A strategic plan is not automatically implementer-proof. For product-critical work, convert broad plans into execution-grade packets before dispatching implementation agents. The planning agent and user should decide concepts, contracts, pass/fail semantics, safety rules, and verification oracles up front; implementer agents should primarily edit files, run gates, and report outcomes.

## Trigger signals

Use this when:

- The user is worried implementers will infer the wrong context.
- The user says they are newer to coding and need conceptual/product correctness nailed down before code review.
- The task defines evals, product metrics, quality gates, safety boundaries, or product truth meters.
- A child plan or architecture doc is strong strategically but leaves schema, matching, failure precedence, setup safety, or report shape undecided.
- Multiple agents will execute sequentially from prompts.
- A one-PR plan hides several independent decisions.
- **The user mentions existing repos or codebases that might overlap with what needs building.** This is a signal to run Phase 0 audit before any planning — don't plan from scratch when pre-built components may already exist.

## Planning stance

Act as the architecture/product planning layer, not the mechanical implementer. The plan should make implementation obvious and reduce agent discretion.

Separate every important behavior into three layers:

1. **Conceptual decision** — the product/architecture rule.
2. **Technical method** — the concrete mechanism that enforces the rule.
3. **Verification oracle** — tests, commands, or report checks proving the method enforces the concept.

If the concept is clear but the implementation is not, pause and compare viable technical methods with the user before choosing. Start concisely: name the gap, why capable engineers could disagree, then list 2-3 plausible engineering approaches in one sentence each ("Engineer 1 might... Engineer 2 might..."). Only expand tradeoffs after the user picks the contested area to examine. Then explain engineering implications (safety, performance, reviewability, extensibility, failure modes) and explicitly verify that the chosen method enforces the conceptual rule.

Do not leave these for implementer agents to invent.

## Phase 0: Codebase Audit

Before writing a single execution packet, check whether existing code already solves parts of the problem. This is especially important when the user mentions other repos or projects they own.

### Process

1. **Discover** — Ask the user if they have other repos/projects that might overlap. If they name one, clone/fetch it.
2. **Map** — Read the full file tree, README, and key sources of each candidate repo. Build a functional checklist of what it provides.
3. **Compare** — Side-by-side table of capabilities between what's needed and what exists. Classify each capability as: **already exists**, **partially exists**, **missing**.
4. **Classify the relationship** between the repos:
   - **Overlapping** — same language, same area, same function. Candidate for dedup or replace.
   - **Complementary** — different layer of the same stack (e.g. one is the comms bus, the other is the execution engine). Candidate for absorb as dependency.
   - **Unrelated** — different domain entirely. No reuse possible.
5. **Decide** — Three paths to present to the user:
   - **Overwrite** — one repo replaces the other entirely (only when truly overlapping).
   - **Absorb** — add the other repo as a dependency/submodule and extend it.
   - **Build fresh** — nothing reusable, start new.

### Comparison table template

```markdown
| Capability | Repo A | Repo B | Status |
|---|---|---|---|
| Bidirectional NATS pub/sub | Full (HubClient) | One-directional only | Repo A provides |
| Provider abstraction | Nothing | Protocol + 2 impls | Repo B provides |
| Structured envelope protocol | Yes (Envelope) | Raw JSON | Repo A provides |
| ... | ... | ... | ... |
```

### Pitfalls

- Do not overwrite codebases in different languages unless you plan a full rewrite.
- Do not assume "has NATS code" means "solves the NATS problem" — check directionality (pub only? sub only? bidirectional?).
- Do not skip reading the actual source — README descriptions are aspirational.
- Present the decision to the user before acting — "should we overwrite, absorb, or build fresh?" is their call.

## Execution packet format

Each packet should include:

- cite parent plans at the top but ensure they are accurate first
- Packet ID and goal.
- Conceptual rules decided up front.
- Exact technical contract: JSON shapes, field names, semantics, precedence, defaults.
- Source-state facts already verified.
- Owned files and likely functions/modules.
- Forbidden files and non-goals.
- Tests to add and existing tests to preserve.
- Verification commands and expected outcomes.
- Safety/privacy rules.
- Handoff checklist.

## Splitting rule

Prefer many precise packets over a few broad PRs when broad PRs hide product decisions. Here, “PR” may mean a trusted implementation unit, not necessarily a final merged GitHub PR. Packets do not have to become separate merged PRs: after concepts and technical methods are clarified, adjacent packets can be grouped if cognitive load is low and the remaining work is mostly mechanical/stamina rather than judgment.

Split whenever a packet mixes distinct risk types:

- schema/contract design
- live side effects
- scoring/gating semantics
- report/user experience
- safety/privacy policy
- already-large shared files
- failures that would be hard to localize

## References

- `references/execution-grade-packet-planning.md` — detailed session-derived guidance and examples for turning broad plans into no-inference implementation packets.
- `references/codebase-audit-methodology.md` — structured approach for comparing existing repos before planning: discovery, capability mapping, classification, decision fork.

## Pitfalls

- Do not hand a strategic plan directly to implementers if exact pass/fail semantics are still open.
- Do not let implementation agents decide product concepts inside code.
- Do not confuse “the agent can write the code” with “the diff will be reviewable and product-correct.”
- Do not over-index on PR count; design packets first, then group only after risk is visible.
