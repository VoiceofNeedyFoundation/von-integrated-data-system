# Senior-management review: Voice of Needy IDS version 4

## Decision requested

Approve or amend the professional first-release logical model shown in the editable diagrams.net file.

| Layer | Count |
|---|---:|
| Canonical core tables | 13 |
| Staging/migration tables | 2 |
| Audit tables | 1 |
| Security tables | 1 |
| Physical tables total | 17 |
| Reporting SQL views | 5 |

This model is intentionally smaller than the earlier 29-table proposal while retaining professional normalization. `participant_identifiers` remains separate because VoN has multiple candidate, legacy, roster, external and permanent identifiers that require uniqueness, verification and source lineage.

## What managers should validate

1. Participant journey and first-release scope.
2. Mobilisation eligibility, conversion and non-join definitions.
3. Planned intake, session delivery and 45-day completion rules.
4. Assessment points/domains and rubric comparability.
5. Placement-readiness checklist.
6. Suitability and verified-joining rules.
7. Retention denominators and treatment of unreachable/unverified records.
8. Income collection, periodicity, verification and privacy.
9. Donor/project, centre and batch reporting ownership.

## Technical review

The analyst/engineer should validate table grains, fields, types, PK/FK/UQ constraints, controlled values, source-to-target mappings, JSON structures and privacy/RLS boundaries.

Do not approve production migration merely by approving this logical model. Physical SQL and migration reconciliation are later checkpoints.
