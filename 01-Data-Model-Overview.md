# Voice of Needy Integrated Data System — Data Model Overview

**Version:** 4.1 review proposal  
**Updated:** 25 November 2026  
**Status:** Logical model for review. No production database, Supabase configuration, or historical migration is authorised by this document.

## 1. What this model is for

The model creates one reliable participant journey from first contact through training, assessment, placement and employment follow-up. It replaces spreadsheet-shaped storage with linked records while retaining the original source row, verification status and audit history.

## 2. Participant journey

1. **Sourcing and mobilisation** — a person may have several outreach or call events before joining training.
2. **Identity resolution** — permanent, candidate, roster, legacy and external IDs are linked without automatically merging uncertain matches.
3. **Training enrolment** — a participant may enrol in more than one batch or make more than one attempt.
4. **Delivery and attendance** — batches contain sessions; daily attendance becomes one participant-session result instead of Day 01–46 columns.
5. **Assessment** — baseline, midline, endline, weekly and Kredo results use one consistent assessment structure with evidence and verification status.
6. **Placement** — employer opportunities and candidate placement attempts are tracked separately.
7. **Employment follow-up** — repeated retention, salary and exit follow-ups remain linked to the original placement.

## 3. Model at a glance

| Layer | Contents | Purpose |
|---|---|---|
| Core | 13 tables | Participant journey, programme delivery and employment outcomes |
| Staging | 2 tables | Repeatable imports, source-row preservation, validation and identity review |
| Audit | 1 table | Material record-change history |
| Security | 1 table | User role and project/centre access scope |
| Reporting | 5 read-only views | Funnel, delivery, assessment, placement and retention reporting |

### Core domains

| Domain | Main tables |
|---|---|
| Participant and outreach | `participants`, `participant_identifiers`, `projects`, `outreach_events` |
| Training | `batches`, `enrolments`, `sessions`, `attendance`, `assessments` |
| Employment | `employers`, `job_opportunities`, `placement_attempts`, `followups` |

## 4. Important design decisions

- One canonical participant can hold many source and operational identifiers.
- Uncertain identity matches remain in review; they are not automatically merged.
- Source-recorded gender and gender confirmed directly by the participant are stored separately, with confirmation status, evidence linkage and date.
- Batch location belongs to the batch; attendance records link to the enrolment and session instead of duplicating location text.
- Baseline, midline, endline, weekly and Kredo results use the same assessment table.
- Training dates, completion claims and assessment results retain verification status and evidence.
- Wide spreadsheet columns such as Session 01–45 and Day 01–46 are converted into rows.
- Every imported row retains its original file, tab, row, checksum and raw values.
- Reporting views never perform identity matching or overwrite operational data.

## 5. What reviewers should decide

1. Is the participant journey complete for the first release?
2. Are sourcing, mobilisation, enrolment, dropout, completion and non-join definitions correct?
3. Are batch, session and attendance rules correct for VoN operations?
4. Are assessment points and verification expectations correct?
5. Are placement suitability, joining and retention definitions correct?
6. Is the separation between source-recorded and participant-confirmed information appropriate?
7. Are privacy and project/centre access boundaries sufficient?
8. Which KPI definitions must be agreed before physical schema and migration work begins?

## 6. Review order

1. Read this overview.
2. Review `02-Detailed-Data-Model.md` for table grains, relationships, mappings and controls.
3. Open `03-Data-Model.drawio` for the complete editable visual model and field-level design.

