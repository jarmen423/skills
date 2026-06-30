# Execution-Grade Packet Planning

This reference captures a planning pattern from an Agent Memory Labs WS6 eval-planning discussion.

## Why this pattern exists

The user wanted to avoid a common failure mode: broad plans handed to implementer agents leave them to infer product context, schema choices, failure semantics, and safety rules. If the user is not deeply reviewing code, those hidden choices can become product behavior without explicit approval.

The solution is to use the planning session to make conceptual decisions and technical contracts explicit before implementation.

## Strategic plan vs implementer-proof plan

A strategic plan is good when it names:

- product goals
- major non-goals
- high-level architecture
- rough PR stack
- broad acceptance criteria

An implementer-proof plan additionally pins:

- exact JSON/schema shapes
- identity/matching precedence
- negative-query semantics
- temporal/assertion semantics
- failure-class precedence
- setup safety behavior
- report output contract
- owned/forbidden files per packet
- exact tests and verification commands

## Three-layer decision model

For every product-critical behavior, decide:

1. **Conceptual decision** — what the product must mean.
   - Example: Raw trajectory-only tool logs must never be eligible for ordinary memory retrieval at all, not merely caught after leaking.
2. **Technical method** — how the code should enforce it.
   - Example options might include excluding raw-only trajectory records at ingest/index time, adding retrieval-lane filters, adding eval `negative_identity` assertions, or combining all three. Discuss tradeoffs before choosing.
3. **Verification oracle** — how we prove it.
   - Example: A query with `expected: []` and forbidden `source_turn_id=t3` passes only when no hit resolves to that turn, while a lower-level storage/index test proves raw-only records are never placed in the ordinary retrieval lane.

When several technical methods could satisfy the concept, compare them with the user before writing an implementation prompt. Start with an **engineer divergence scan** before deep explanation:

```text
Gap: exact schema shape.
Why it is a gap: multiple reasonable implementations encode the same concept but create different matcher/reporting contracts.
Engineer 1 might use `{kind, value}` objects for a uniform identity enum.
Engineer 2 might use single-key objects like `{source_turn_id: "t4"}` for concise hand-authored JSON.
Engineer 3 might use `{field, equals, required}` as a generic assertion DSL.
Recommendation to examine first: whether this needs a simple identity primitive or a mini assertion language.
```

Keep this first pass concise. Only expand tradeoffs after the user identifies which contested choice to examine. Then cover safety, performance, observability, UI/report implications, extensibility, and failure modes. The chosen method must be explicitly tied back to the conceptual rule.

## Split-pressure checklist

Start splitting into more packets when two or more of these appear:

1. Shared schema or public contract change.
2. New CLI command.
3. Live side effects.
4. Scoring/gating semantics.
5. Report/UI/UX behavior.
6. New fixtures.
7. Safety/privacy policy.
8. Already-large shared files.
9. Multiple independent acceptance criteria.
10. Failures that would be hard to localize.

## Packet vs PR

Plan as many packets as needed to remove ambiguity. In this workflow, “PR” is often shorthand for a trusted implementation unit, not necessarily a final merged GitHub PR. Do not assume each packet must be separate. After semantics and technical methods are stable, adjacent packets can be grouped when cognitive load is low and the work is mostly mechanical/stamina rather than product judgment. The purpose of packets is to reduce inference risk, not to maximize GitHub PR count.

## Good packet prompt shape

```text
Implement WSX.Y: Negative Identity Semantics.

Conceptual rule:
A forbidden identity in the inspected hit window means the query fails. This is true even if expected identities are also present. For expected-empty leakage queries, absence of forbidden identities is success.

Technical method:
Add `NegativeIdentityAssertion` parsed from `negative_identity` and legacy `negative_paths`. Inspect top 20 hybrid hits by default. Reuse `EvalHitIdentity`.

Owned files:
- crates/am-cli/src/commands/eval_identity.rs
- crates/am-cli/src/commands/eval_retrieval_metrics.rs

Do not touch:
- fixture setup runner
- temporal request construction
- server routes

Tests:
- expected-empty query passes when no forbidden identity appears
- expected-empty query fails when forbidden path appears
- positive expected hit still fails if forbidden identity also appears
- old suites without negative identity still pass
```

## Output recommendation

When reviewing a plan, be candid if it is strong strategically but not implementer-proof. Recommend a planning refresh and list the exact decisions still open. Frame the work as protecting product correctness, not as bureaucracy.