# MIMIC Benchmark Opportunities

This reference distills the recurring useful ideas from the deep-research corpus
under `artifacts/mimic-deep-research/`. Treat the raw research as a hypothesis
generator; verify drift-prone claims and source details before publication.

## Problems Worth Testing

### 1. Temporal-structural disconnect

Hospitals have data, but the relevant facts are fragmented across time,
encounters, and modules. The useful question is not "can we retrieve a row?" but
"can we reconstruct the clinically relevant story with timestamps and
provenance?"

### 2. Manual evidence assembly burden

Quality committees, mortality review, protocol audits, and root-cause analyses
require evidence packets assembled from many tables. This is where temporal +
graph + vector composition has a plausible advantage.

### 3. Cross-boundary continuity failures

Readmissions, handoffs, medication reconciliation, and repeated admissions are
hard because they cross encounters and departments. These are better targets
than single-admission chart lookup.

### 4. Auditability gap

Hospitals need not only a prediction but an evidence trail. Evidence packets
with source events, timestamps, and provenance are a stronger product shape than
opaque risk scores.

### 5. Protocol adherence and drift

Bundles such as sepsis compliance require exact temporal relationships among
labs, orders, meds, fluids, and interventions. This is a natural place to test
temporal validity and multi-hop composition.

## Strong Candidate Task Families

### Evidence-packet assembly

Question shape:

> Given a critical event or review target, assemble the minimal complete evidence
> packet needed for a quality reviewer to understand what happened.

Useful for:

- deterioration review
- ICU transfer review
- mortality review
- handoff preparation

### Prior similar-case retrieval

Question shape:

> Given an index case, retrieve prior clinically similar cases and the evidence
> that explains both similarity and key differences.

Useful for:

- RCA support
- consult support
- institutional learning

### Protocol adherence / bundle compliance

Question shape:

> For a defined cohort, reconstruct whether required events occurred in the
> allowed temporal order and window.

Useful for:

- sepsis bundle timing
- medication reconciliation
- discharge process compliance

### Cohort outcome drift

Question shape:

> Detect when outcomes or care patterns drift across time, and assemble the
> evidence explaining the change.

Useful for:

- board-level quality oversight
- department performance review
- temporal trend investigations

## MIMIC Table Families Often Needed

- `patients`, `admissions`, `transfers`
- `labevents`, `d_labitems`
- `chartevents`, `d_items`
- `inputevents`, `procedureevents`
- `prescriptions`, `pharmacy`, `emar`, `emar_detail`
- `diagnoses_icd`, `procedures_icd`
- `microbiologyevents`
- later: notes/discharge artifacts when access and scope permit

## Stakeholder Narratives

- **Board:** We do not need another dashboard; we need to understand the chain
  from fragmented events to preventable outcomes before penalties arrive.
- **Reviewer:** The benchmark matters only if it enforces temporal validity,
  reproducibility, and provenance better than prior MIMIC work.
- **Engineer:** The question is not graph versus vector in isolation; the
  question is whether composition of temporal + graph + vector solves tasks no
  single modality handles cleanly.

## Claims To Avoid

- "clinically significant" when only proxy labels exist
- "hospital intelligence" from a single simple lookup task
- "better than EHR" when the task is something EHRs already do
- "autonomous clinical reasoning" from pure retrieval metrics
- board-level value without a review burden, auditability, or drift outcome
