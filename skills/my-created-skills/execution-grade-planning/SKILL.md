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

## Planning stance

Act as the architecture/product planning layer, not the mechanical implementer. The plan should make implementation obvious and reduce agent discretion.

Separate every important behavior into three layers:

1. **Conceptual decision** — the product/architecture rule.
2. **Technical method** — the concrete mechanism that enforces the rule.
3. **Verification oracle** — tests, commands, or report checks proving the method enforces the concept.

If the concept is clear but the implementation is not, pause and compare viable technical methods with the user before choosing. Explain the engineering implications of each option (safety, performance, reviewability, extensibility, failure modes) and explicitly verify that the chosen method actually enforces the conceptual rule.

Do not leave these for implementer agents to invent.

## Execution packet format

Each packet should include:

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

Prefer many precise packets over a few broad PRs when broad PRs hide product decisions. Packets do not have to become separate merged PRs: adjacent tiny packets can be grouped after semantics are nailed down.

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

## Pitfalls

- Do not hand a strategic plan directly to implementers if exact pass/fail semantics are still open.
- Do not let implementation agents decide product concepts inside code.
- Do not confuse “the agent can write the code” with “the diff will be reviewable and product-correct.”
- Do not over-index on PR count; design packets first, then group only after risk is visible.
