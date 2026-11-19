# Project status

**Current stage:** Discovery and data-model review (Checkpoints 1–3 preparation)

**Last updated:** 19 November 2026, India time

## Completed in the current iteration

- Reviewed the VoN key-question spreadsheet: 13 high-priority questions covering mobilisation, training, assessments, readiness, placement, suitability, retention and income.
- Reviewed the supplied external detailed data-model diagram and extracted its entity/relationship design pattern.
- Rebuilt the VoN model around verified VoN needs rather than copying the reference project.
- Reduced the canonical business design to 22 tables, with staff/access and audit structures shown separately, and documented which earlier concepts were combined, removed or deferred.
- Added direct traceability from every key question to core tables, mart facts and identified collection gaps.
- Added a revised Mermaid ERD and senior-management review pack.

## Current outputs

- `docs/data-architecture.md`
- `docs/data-model.md`
- `docs/data-dictionary.md`
- `docs/dashboard-data-model.md`
- `docs/key-question-to-data-model.md`
- `docs/senior-manager-data-model-review.md`

## Pending approvals

- Business definitions for denominators, conversion, attendance/completion, assessment timing, readiness, verified joining, retention and income.
- Canonical model approval (Checkpoint 3).
- Source-to-target mappings and unresolved identity rules.

## Blockers

- KQ12 income at 24 months is not currently available.
- Several key-question datasets are only partially available and need standard future collection.
- Supabase/VoN production access is intentionally out of scope at this stage.

## Next actions after review

1. Record manager decisions and update controlled lists/business rules.
2. Complete field-level source-to-target mapping and historical profiling.
3. Obtain formal model approval.
4. Only then create version-controlled SQL migrations, synthetic tests and frontend contracts.

No production migration, Supabase configuration or Vercel change has been made.
