# Master Sheet to canonical model mapping

**Purpose:** Demonstrate that every current Master Sheet tab and column group has a defined destination. Verification tabs do not become operational tables; they remain review evidence until approved.

| Master Sheet tab | Source column groups | Canonical destination / transformation |
|---|---|---|
| Participant Registry | Participant ID; name; gender; DOB; mobile; email; disability; address; district/state/pin; education; income; guardian; first stage/source; registration metadata | `participants`; all ID lists/candidate/batch/external numbers to `participant_identifiers`; source locators to `source_records` |
| Sourcing | Participant/candidate IDs; name; project/donor; year; centre; channel; source file/tab/row/URL; demographic/profile source values; identity/review fields | One `outreach_events` source event; verified profile fields update `participants`; IDs to `participant_identifiers`; provenance/review to `source_records` |
| Mobilization | Event ID; participant/name; contact date; response/channel; source; mobilizer; profile values; eligibility/age/disability/verification review | One row per contact in `outreach_events`; verified participant attributes update `participants`; review evidence stays in `source_records` |
| Training | Participant/candidate/name; registration/start/end; year/status/days; batch IDs/registration no.; dropout/readiness/source fields | `enrolments`; batch/registration IDs to `participant_identifiers`; dropout fields stay on enrolment; source evidence to `source_records` |
| Training | Baseline/endline; Kredo mid/final score/status/completion date | Separate rows in `assessments` with type, period, score and completion status |
| Training Batch | Batch/original batch; project/donor; year; centre; planned/actual dates; participant count; status; trainers/topics; plan/completion evidence | `projects` and `batches`; evidence references in `source_records` and batch evidence fields |
| Training - session planned vs complete | Batch context; planned/completed/pending counts; completion percent; facilitator/evidence/review | Batch summary is derived; batch fields update `batches` |
| Training - session planned vs complete | Session 01–Session 45 | Unpivot to one `sessions` row per batch/session number; planned/actual/status/topic retained from source content/evidence |
| Training - Daily attendance | Participant/candidate/name; year/batch/start/status; aggregate present/absent/marked/percent; source register/link | Resolve `enrolments`; aggregates are calculated from `attendance`; source references go to `source_records` |
| Training - Daily attendance | Day 1–Day 46 | Unpivot to one `attendance` row per enrolment/session/day |
| Training - Weekly assessments | Participant/candidate/name; year/batch/start/status | Resolve `enrolments` |
| Training - Weekly assessments | Week 1–Week 6 | Unpivot to `assessments` with weekly type and period code |
| Employers Data | Employer/company; location; contact; email/phone/designation; disability/education requirements; pay; vacancies; roles; notes; verification/source; existing/required staff | Organisation/contact/engagement fields to `employers`; each verified role/vacancy to `job_opportunities`; source lineage to `source_records` |
| Placements | Participant/candidate/name; employer; role; salary; status; join date; rejection; offer letter; batch; placement exit/reason/evidence | `placement_attempts`; resolve/create verified employer/opportunity; join/offer/exit fields remain on attempt |
| Follow-ups | Participant/candidate/name; current/previous workplace; date; status; salary; leaving reason; evidence/verification | Resolve placement; append one `followups` row per dated attempt/checkpoint |
| 2026 Attendance - Verify | Source tab/row; register name/project/centre/period/start/marks; possible IDs; verification/review | `source_records` identity/validation review only; approved match loads `attendance` |
| Outreach Contacts - Verify | Source/profile/contact/demographic fields; possible permanent ID; eligibility/review/classification | `source_records`; approved event loads `outreach_events`; approved profile update loads `participants` |
| ID Mapping & Source Trace | Legacy/permanent/candidate/batch/session IDs; source workbook/row/link; age/disability review; batch evidence; external number/method | `participant_identifiers`, batch source identifiers and `source_records`; never a new participant solely from a name match |
| 2026 Attendance - Source Roster | Source record/register/PDF/period/batch; matched/possible IDs; totals; Day 01–46; verification/notes | Raw/staging evidence in `source_records`; verified day marks unpivot to `attendance` |
| 2026-27 Extra Trainees - Verify | Source roster/file/row; project/batch/centre/year; profile/contact; dates; proposed/matched IDs; review/action | `source_records`; after identity/batch approval load/update `participants`, `participant_identifiers` and `enrolments` |
| Training and Placement Dropouts | Evidence ID; participant/name; stage/status; reason; dates/file/location/match/source/review | `source_records`; approved training dropout updates `enrolments`; approved placement exit updates `placement_attempts` |
| Training Plans - Source References | Plan/source/type/period/centre/trainers/topics; confirmed batch; completion evidence/review/link | `source_records`; approved plan updates `batches` and creates/updates `sessions` |

## Preservation rule

Even when a source column is transformed or becomes a derived value, its original row and value remain in `staging.source_records.raw_payload` with file, tab, row and checksum. This prevents information loss while keeping the canonical model clean.
