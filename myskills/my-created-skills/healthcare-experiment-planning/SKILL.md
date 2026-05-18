---
name: healthcare-experiment-planning
description: Plan, critique, or redesign healthcare experiments for Agentic Memory, especially MIMIC-backed benchmarks, publication plans, hospital-intelligence tasks, and retrieval/RAG studies. Use when Codex needs to decide what question matters, isolate the system variable, choose fair baselines, design cohorts and artifacts, reject weak EHR-lookup experiments, or turn healthcare research into a rigorous experiment plan.
---

# Healthcare Experiment Planning

Use this skill to design experiments that test a **memory-native system**, not
preprocessing tricks or capabilities an EHR already provides.

## Workflow

1. **Name the decision-worthy problem first.**
   - State who cares: board, CQO, CMIO, patient-safety lead, researcher, or engineer.
   - State what existing tools fail to do: not what is merely inconvenient.
   - Reject ideas that only prove chart lookup, SQL filtering, or ordinary EHR reporting.

2. **Write the primary question in one sentence.**
   - Prefer: "Can the full stack assemble the right cross-time evidence packet from noisy memory better than narrower baselines?"
   - Avoid: "Can the system retrieve rows we already identified with patient/time filters?"

3. **Define the tested variable.**
   - Keep corpus, task, query, and scoring constant across arms.
   - Let retrieval architecture vary: lexical, vector-only, graph-only, temporal-only, full stack.
   - Treat oracle filters and gold SQL as controls or ceilings, not as main competitors.

4. **Choose a cohort that preserves the real difficulty.**
   - Reduce scale by sampling patients/admissions, not by stripping away the noise the system must handle.
   - Use enough patients to exceed plausible manual review capacity.
   - Preserve patient-level split integrity and time-of-availability rules.

5. **Design outputs people would actually use.**
   - Prefer evidence packets, similar-case sets, drift reports, protocol-compliance trails, or review queues.
   - Require provenance, timestamps, and compact reviewable artifacts.
   - For board-level tasks, measure review burden reduction and actionability, not only retrieval metrics.

6. **Select baselines and metrics that answer the question.**
   - Use gold SQL/manual analytics as a ceiling where appropriate.
   - Use lexical/vector/graph/temporal baselines to isolate architectural contributions.
   - Include evidence completeness, noise rate, temporal validity, review compression, and provenance quality when relevant.

7. **Check publication validity before implementation.**
   - Temporal leakage, label leakage, oracle leakage, cohort leakage, and post-hoc features must be ruled out explicitly.
   - Pre-register or version-lock gold queries and task-generation logic before tuning baselines.
   - Separate automated scoring from claims that require human review.

8. **Return an execution-ready plan.**
   - Problem
   - Claim
   - Stakeholder
   - Dataset slice
   - Cohort
   - Task families
   - Arms
   - Metrics
   - Artifacts
   - Leakage controls
   - What success would mean
   - What failure would mean
   - First runnable smoke

## Fast Rejection Rules

Reject or redesign an experiment if any of these are true:

- It proves something the EHR already does well.
- The benchmark script performs the hard clinical reasoning before the stack runs.
- The "full-stack" arm gets oracle patient/time filters that weaker arms do not.
- The result would still be uninteresting even if the full stack won.
- The gold label is merely "abnormal" when the real product claim is significance, triage, or cross-event synthesis.
- The task can be solved by one exact SQL predicate and no meaningful memory composition.
- The proposed output is not useful to any named stakeholder.

## Reference Loading

- Read [scientific-design-principles.md](references/scientific-design-principles.md)
  when deciding whether an experiment is actually testing the system.
- Read [mimic-benchmark-opportunities.md](references/mimic-benchmark-opportunities.md)
  when choosing MIMIC-backed task families or stakeholder narratives.
- Read [experiment-plan-template.md](references/experiment-plan-template.md)
  when writing a new plan or critiquing an existing one.
- If the task requires deeper source grounding, inspect the raw research corpus in:
  - `D:\code\agentic-memory\artifacts\mimic-deep-research\original_prompt.md`
  - `D:\code\agentic-memory\artifacts\mimic-deep-research\gemini-am-benchmark-design.md`
  - `D:\code\agentic-memory\artifacts\mimic-deep-research\kimi1-am_mimic_benchmark.agent.final.md`
  - `D:\code\agentic-memory\artifacts\mimic-deep-research\kimi2-benchmark_design_plan.md`

## Output Standard

Prefer concise plans that answer:

1. What matters?
2. Why does this matter beyond ordinary EHR functionality?
3. What exactly is the system variable?
4. What would a win prove?
5. What would a loss teach us?

Do not hide a weak experiment under a long taxonomy.
