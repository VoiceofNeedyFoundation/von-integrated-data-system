# Senior-management review: reduced VoN data model

## Decision requested

Review and approve the reduced first-release model: **12 business tables, 3 audit tables, 1 access table and 5 reporting views**.

## Reduction achieved

| Version | Business/core | Audit/access | Stored dashboard tables | Total physical tables |
|---|---:|---:|---:|---:|
| Previous proposal | 22 | 7 | 0 | 29 |
| Revised version 3 | 12 | 4 | 0 | 16 |

This is a reduction of 13 physical tables (approximately 45%) without deleting source attributes.

## What was combined

- identifiers, contacts and support needs into participant;
- sourcing and mobilisation contacts into outreach records;
- assessment event, domain result and rubric metadata into assessment;
- readiness flags into enrolment;
- candidate match and verified employment into placement;
- identity review and data-quality exceptions into source-record audit;
- dashboard facts/dimensions into SQL views.

## Why the remaining tables cannot be safely combined

- Participant and enrolment differ because one person can join more than one batch.
- Batch, session and attendance have different one-to-many grains.
- Employer, opportunity and placement represent organisation, vacancy and candidate attempt.
- Follow-ups repeat after joining and must preserve history.

## Review decisions

1. Approve the 12-table business boundary.
2. Approve structured JSON for alternative identifiers/contacts and low-volume supporting attributes.
3. Approve outreach records as the common sourcing/mobilisation event table.
4. Approve placement as both pipeline attempt and joined-employment record.
5. Approve five dashboard views rather than stored fact/dimension tables for release 1.
6. Confirm conversion, completion, readiness, verified joining, retention and income definitions.

## Recommendation

Approve version 3 as the first-release logical model, subject to field-level source mapping and KPI-definition corrections. Do not create production schema or migrate data until Checkpoint 3 is formally recorded.
