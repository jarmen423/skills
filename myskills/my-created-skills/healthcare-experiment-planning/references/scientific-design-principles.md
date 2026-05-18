# Scientific Design Principles

## Core Rule

The benchmark should test the **memory architecture** as the independent
variable. It should not test how much task logic the benchmark author embedded
in preprocessing.

## What Good Looks Like

- Same corpus, same query, same gold target, same scoring for every real arm.
- Different retrieval architecture per arm:
  - lexical
  - vector-only
  - graph-only
  - temporal-only
  - full temporal + graph + vector composition
- Gold SQL/manual analytics used as a ceiling or label generator, not confused
  with the product.
- Debug controls labeled honestly:
  - `oracle_patient_filtered`
  - `oracle_time_filtered`
  - `gold_sql_ceiling`
- Success tied to a real decision, workflow, or review burden.

## Anti-Patterns

### 1. Oracle filtering disguised as a baseline

If the benchmark gives a retriever the exact patient and exact evidence window,
then the hard part may already be solved. That can be useful for wiring checks,
but it is not the scientific answer.

### 2. EHR lookup as a product claim

"Find this patient's lab near this timestamp" is not enough. Existing EHRs can
already surface patient-specific rows. Prefer tasks requiring:

- cross-admission continuity
- trajectory reconstruction
- evidence-packet assembly
- similar-case retrieval
- protocol drift
- cross-event contradiction detection

### 3. Preprocessing does the cognition

If the script decides which events are clinically significant and hands only
those to the system, the benchmark measures preprocessing quality. Preserve the
noise the memory system is supposed to rank through.

### 4. Labels stronger than the evidence supports

If the data only provides proxy labels, call them silver labels. Do not claim
clinical truth without adjudication.

### 5. Metrics that do not match the claim

If the claim is "reduce expert review burden," report only Recall@k is
insufficient. Add metrics such as:

- evidence completeness
- noise rate
- events reviewed per true case
- review compression
- future-leakage rate
- provenance completeness

## Question Ladder

Use this ladder to test whether the experiment is worth doing:

1. What existing workflow is failing?
2. Why do Epic/SQL/vector search fail on it?
3. What part of the failure requires memory composition?
4. What output would a real stakeholder use?
5. What is the smallest experiment that isolates that advantage?

If you cannot answer all five, the experiment is not ready.

## Validity Checklist

- Gold logic defined before baseline tuning.
- Patient leakage prevented across splits.
- Temporal availability defined at query time.
- Future information excluded where the task is prospective.
- Cohort sampling rationale stated.
- Oracle/debug controls separated from reportable baselines.
- Stakeholder utility and methodological novelty both stated.
