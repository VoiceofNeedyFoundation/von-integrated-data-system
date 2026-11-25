# Voice of Needy Integrated Data System — Detailed Data Model

**Version:** 4.1 review proposal  
**Updated:** 25 November 2026

## 1. Model scope

This document provides the technical detail needed to review the logical model. The accompanying Draw.io file is the authoritative field-level visual. Physical PostgreSQL/Supabase types, migrations, RLS policies and data loading will be prepared only after this model is approved.

## 2. Canonical core tables

| # | Table | Grain | Main content and controls |
|---:|---|---|---|
| 1 | `core.participants` | One canonical person | Name, contact, disability, education, address, support details, identity status; source-recorded and directly confirmed gender are separate |
| 2 | `core.participant_identifiers` | One identifier assigned to one participant | Permanent, candidate, legacy, roster, registration and external IDs; verification and source linkage |
| 3 | `core.projects` | One programme/donor project | Project, donor, financial year, dates, targets and centres |
| 4 | `core.outreach_events` | One sourcing, mobilisation, call or eligibility event | Event date/type, response, outcome, follow-up, owner and source attributes; participant may be unresolved |
| 5 | `core.batches` | One training cohort | Project, centre/location, planned and actual dates, intake, trainers, topics, status and evidence |
| 6 | `core.enrolments` | One participant attempt in one batch | Registration, training dates, completion/dropout, re-entry and placement readiness |
| 7 | `core.sessions` | One planned or delivered session in one batch | Session number, topic, dates, delivery status, facilitator and evidence |
| 8 | `core.attendance` | One enrolment-session attendance result | Present/absent status, date, original register mark and verification |
| 9 | `core.assessments` | One enrolment, assessment point, domain and attempt result | Baseline/midline/endline/weekly/Kredo, score, rubric, completion, evidence and verification status |
| 10 | `core.employers` | One employer organisation | Contact and engagement profile, accessibility, disability hiring needs and verification |
| 11 | `core.job_opportunities` | One role/vacancy at one employer | Role, location, requirements, salary, vacancies, dates and status |
| 12 | `core.placement_attempts` | One enrolment-opportunity attempt | Suitability, pipeline stages, interview/offer/joining, salary, status and evidence |
| 13 | `core.followups` | One employment follow-up attempt | Checkpoint, due/contact dates, employment status, workplace, role, salary, exit reason and evidence |

## 3. Control tables

| Table | Grain and purpose |
|---|---|
| `staging.import_runs` | One repeatable import execution with source, staged, loaded, rejected and unresolved counts |
| `staging.source_records` | One immutable source row with raw payload, standardised payload, validation, identity decision and target lineage |
| `audit.change_log` | One material change to a protected operational record, including actor and before/after values |
| `security.user_access` | One user-role-scope assignment with optional project and centre restrictions |

## 4. Main relationships

| Parent | Relationship | Child |
|---|---|---|
| Participant | one-to-many | Identifiers and outreach events |
| Project | one-to-many | Outreach events and batches |
| Participant + batch | one enrolment attempt | Enrolment |
| Batch | one-to-many | Enrolments and sessions |
| Enrolment + session | one attendance result | Attendance |
| Enrolment | one-to-many | Assessment results and placement attempts |
| Employer | one-to-many | Job opportunities |
| Job opportunity | one-to-many | Placement attempts |
| Placement attempt | one-to-many | Follow-ups |
| Import run | one-to-many | Source records |

## 5. Key field-level decisions

### Participant identity

- `participant_id` is the internal UUID; `participant_code` is the human-readable permanent code.
- Candidate, legacy, attendance-roster and external file numbers are stored as identifiers, not extra participant columns.
- `identity_status` distinguishes confirmed, provisional, unresolved and merged records.
- Source-recorded gender remains separate from directly confirmed gender.
- Gender confirmation includes a controlled status, date and linked source/evidence record.
- Restricted contact, disability, income and address fields require role-based access.

### Training and attendance

- Enrolment uniqueness is participant + batch + attempt number.
- Batch location and official dates are maintained once in `batches` and referenced by enrolments and attendance.
- Planned dates are not treated as actual completion dates.
- Daily register marks are unpivoted into attendance rows; percentages are derived.
- Attendance-source participants may remain provisional until identity confirmation.

### Assessments

- `assessment_type` and `period_code` distinguish baseline, midline, endline, weekly and external/Kredo results.
- Results store score, maximum score, derived percentage, rubric version and attempt number.
- `verification_status`, evidence URL, missing reason and raw source result prevent unverified scores from being treated as confirmed outcomes.

### Placement and follow-up

- Employer, opportunity and candidate attempt are separate records.
- Offer, joining and employment retention require explicit evidence/verification indicators.
- Follow-ups are append-only attempts; an unreachable participant does not silently become unemployed.

## 6. Master Sheet mapping

| Master Sheet area | Canonical destination |
|---|---|
| Participant Registry | `participants`, `participant_identifiers`, `source_records` |
| Sourcing and Mobilization | `outreach_events`; verified profile updates to `participants` |
| Training | `enrolments`; baseline/midline/endline/Kredo results to `assessments` |
| Training Batch and plan references | `projects`, `batches`, `sessions`, `source_records` |
| Session planned vs complete | Session columns unpivoted to `sessions`; summaries derived |
| Daily attendance and source roster | Day columns unpivoted to `attendance`; identity evidence retained in `source_records` |
| Weekly assessments | Week columns unpivoted to `assessments` |
| Employers Data | `employers`, `job_opportunities` |
| Placements | `placement_attempts`, linked employer/opportunity and evidence |
| Follow-ups | `followups` linked to a placement attempt |
| Verification, mapping, dropout and extra-trainee tabs | `source_records`; approved decisions update relevant core records |

## 7. Latest Master Sheet alignment

The model was checked against the 25 November 2026 Master Sheet structure.

- New directly confirmed gender fields required the Version 4.1 participant-field update described above.
- Attendance location and batch columns are represented by the existing `batches`, `enrolments` and `attendance` relationships.
- Midline scores use the existing assessment structure.
- Registration-date, training-date and completion-quality review fields remain source validation evidence until approved.
- Curriculum/assessment source and verification fields map to assessment evidence, verification status and source lineage.

## 8. Reporting views

| View | Purpose |
|---|---|
| `reporting.vw_candidate_funnel` | Sourcing, mobilisation, enrolment and conversion |
| `reporting.vw_training_delivery` | Batch, session completion and attendance |
| `reporting.vw_assessment_progress` | Comparable assessment progress with verification status |
| `reporting.vw_placement_pipeline` | Opportunity matching through verified joining |
| `reporting.vw_retention_income` | Follow-up, retention and income outcomes |

Reporting views are read-only. They must not resolve identities or overwrite operational records.

## 9. Migration and governance rules

- Preserve every original source row and checksum.
- Never auto-merge uncertain identities.
- Load core records only after validation and identity decisions are recorded.
- Reconcile source, staged, loaded, rejected and unresolved counts for every import.
- Apply project/centre-scoped access and protect sensitive fields.
- Record material corrections in the audit log.
- Do not begin production migration until business definitions and the logical model are approved.

## 10. Review checklist

- Confirm each table has one clear grain.
- Confirm controlled statuses and evidence requirements.
- Confirm identity-resolution and non-merge rules.
- Confirm source-to-target mappings preserve all information.
- Confirm KPI denominators and treatment of unresolved/unverified records.
- Confirm privacy and access scopes.

