# Requirements register

**Status** — Discovery draft. Confirmed means directly supported by the project brief and reviewed evidence; it does not mean the database design is approved.

## Confirmed functional requirements

| ID | Requirement | Evidence status |
| --- | --- | --- |
| FR-01 | Preserve source records from sourcing through follow-up with traceable provenance. | Confirmed |
| FR-02 | Maintain a stable person identity independent of row numbers, source files and programme events. | Confirmed |
| FR-03 | Allow one person to have multiple source records, contacts, enrolments, batches, assessments, placements and follow-ups. | Confirmed |
| FR-04 | Keep outreach-only leads even when they never register or train. | Confirmed |
| FR-05 | Support consent, registration and document-verification status without fabricating missing historical values. | Confirmed |
| FR-06 | Support programme/donor, financial year, training location, batch and participant roster structures. | Confirmed |
| FR-07 | Track scheduled and completed training sessions at batch level and attendance at participant/session or participant/day level. | Confirmed, detailed fields pending |
| FR-08 | Record assessment evidence appropriate to the approved release scope. | Confirmed need; weekly workflow pending |
| FR-09 | Track employer requirements, candidate preferences, interviews, offers, joining, job changes and placement status. | Confirmed need; definitions pending |
| FR-10 | Track post-placement follow-up and retention at 3, 6 and 12 months or another approved cadence. | Confirmed need; source/owner pending |
| FR-11 | Provide centre, batch, district, donor/project and participant-level monitoring views. | Confirmed |
| FR-12 | Support future frontend creation and updates using approved validation and access rules. | Confirmed |

## Confirmed non-functional requirements

| ID | Requirement |
| --- | --- |
| NFR-01 | Keep participant data and credentials out of Git, issues, pull requests and logs. |
| NFR-02 | Preserve source lineage and every record disposition. |
| NFR-03 | Make migration repeatable, auditable and idempotent. |
| NFR-04 | Separate development/testing from production and use synthetic data in repository tests. |
| NFR-05 | Apply least-privilege authentication, authorisation and audit controls when backend work is authorised. |
| NFR-06 | Version schema and interface changes and coordinate breaking changes with the frontend workstream. |
| NFR-07 | Keep data entry practical for field staff and resilient to incomplete workflows. |
| NFR-08 | Ensure VoN ownership and handover without personal-account dependencies. |

## Inferred requirements needing confirmation

- A lead should have a lifecycle state and can later link to a registered participant without losing the original source identity.
- Registration, enrolment and batch membership should be separate events.
- A person may be enrolled more than once and should not receive a second person identity solely for that reason.
- Training location, participant home location and employer/job location should be distinct.
- A batch should have planned and actual dates, capacity, status and an approved session plan.
- Placement attempts should be recorded even if no offer or joining occurs.
- Retention should be event-based so multiple follow-ups and job transitions can coexist.
- Alerts are needed for upcoming batches, placement activity and overdue workflow steps, but their timing and ownership are not approved.

## Decisions required before modelling approval

1. Historical migration period and phasing.
2. Authoritative source hierarchy per domain.
3. Person-matching evidence and confidence thresholds.
4. Review rules for repeat enrolment and multiple registrations.
5. Canonical programme, donor/project, location, disability and status vocabularies.
6. Weekly assessment scope.
7. Placement and retention definitions and evidence.
8. Frontend forms, user roles and approval steps.
9. Data retention, consent and sensitive-field access rules.
