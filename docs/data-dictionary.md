# Voice of Needy IDS data dictionary

**Status:** Version 2 logical dictionary. Types are PostgreSQL-oriented and remain provisional until Checkpoint 3 approval.

Common fields on operational tables: `created_at timestamptz not null`, `updated_at timestamptz not null`, `created_by uuid null`, `updated_by uuid null`. Primary keys are UUIDs unless stated otherwise.

## Reference tables

### `ref.reference_values`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `reference_value_id` | uuid PK | No | Immutable |
| `list_name` | text | No | Controlled list, e.g. attendance_status |
| `code` | text | No | Stable machine code |
| `label` | text | No | User-facing label |
| `sort_order` | integer | No | Default 0 |
| `is_active` | boolean | No | Retire, never delete used values |

Unique: `(list_name, code)`.

### `ref.projects`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `project_id` | uuid PK | No | Immutable |
| `project_code` | text | No | Unique business code |
| `project_name` | text | No | Programme/project name |
| `donor_name` | text | Yes | Separate donor table only if later justified |
| `start_date`, `end_date` | date | Yes | End not before start |
| `target_participants` | integer | Yes | Non-negative |
| `is_active` | boolean | No | Default true |

### `ref.locations`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `location_id` | uuid PK | No | Immutable |
| `location_code` | text | No | Unique |
| `location_name` | text | No | Standard display name |
| `location_type` | text | No | Centre/city/district/state/other |
| `parent_location_id` | uuid FK | Yes | Self-reference; no cycles |
| `is_training_centre` | boolean | No | Default false |
| `is_active` | boolean | No | Default true |

### `ref.assessment_rubrics`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `rubric_item_id` | uuid PK | No | Immutable |
| `rubric_version` | text | No | Versioned, not overwritten |
| `assessment_point` | text | No | Baseline/midline/endline or approved value |
| `domain_code` | text | No | Stable domain |
| `domain_label` | text | No | Display label |
| `maximum_score` | numeric | No | Greater than 0 |
| `effective_from`, `effective_to` | date | Yes | Preserve old definitions |

Unique: `(rubric_version, assessment_point, domain_code)`.

## Participant and mobilisation

### `core.participants`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `participant_id` | uuid PK | No | System generated; never derived from name/phone |
| `participant_code` | text | No | Unique human-readable VoN code |
| `first_name` | text | No | Trimmed; original retained in lineage |
| `middle_name`, `last_name` | text | Yes | No fabricated components |
| `date_of_birth` | date | Yes | Age is derived, not stored |
| `gender_code` | text | Yes | Controlled value |
| `record_status` | text | No | active/inactive/deceased/duplicate_pending_review |

### `core.participant_identifiers`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `participant_identifier_id` | uuid PK | No | Immutable |
| `participant_id` | uuid FK | No | Parent participant |
| `identifier_type` | text | No | UDID, source ID, legacy ID, other |
| `identifier_value_encrypted` | text | No | Restricted; encrypted where required |
| `normalised_hash` | text | Yes | Matching without exposing value |
| `is_verified` | boolean | No | Default false |
| `verified_at` | timestamptz | Yes | Required when verified |

Verified identifiers enforce uniqueness by type and normalised hash where business rules permit.

### `core.participant_contacts`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `participant_contact_id` | uuid PK | No | Immutable |
| `participant_id` | uuid FK | No | Parent participant |
| `contact_type` | text | No | mobile/email/caregiver/other |
| `contact_name` | text | Yes | For caregiver/alternate contact |
| `relationship_code` | text | Yes | Controlled |
| `contact_value_encrypted` | text | No | Restricted PII |
| `normalised_hash` | text | Yes | Matching/search helper |
| `is_primary`, `is_verified` | boolean | No | Defaults false |

### `core.participant_support_profiles`

One restricted current profile per participant.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `participant_id` | uuid PK/FK | No | One-to-one |
| `disability_category_code` | text | Yes | Controlled; no diagnosis inference |
| `support_needs` | text | Yes | Free text with access restriction |
| `accessibility_requirements` | text | Yes | Operational accommodations |
| `preferred_job_sectors` | text[] | Yes | Controlled codes when approved |
| `preferred_work_locations` | text[] | Yes | Controlled/location IDs where possible |
| `career_goal` | text | Yes | Participant-stated |
| `profile_verified_at` | timestamptz | Yes | Verification timestamp |

### `core.mobilisation_cases`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `mobilisation_case_id` | uuid PK | No | One opportunity/cycle |
| `participant_id` | uuid FK | Yes | Null while unresolved |
| `project_id` | uuid FK | Yes | Intended project/programme |
| `source_channel_code` | text | Yes | Controlled |
| `source_name` | text | Yes | Partner/camp/referral detail |
| `first_contact_date` | date | Yes | Historical data may be incomplete |
| `current_stage_code` | text | No | lead/contacted/eligible/ineligible/enrolled/not_joined/etc. |
| `stage_reason_code` | text | Yes | Required for terminal non-enrolment stages |
| `owner_staff_id` | uuid FK | Yes | Current owner |
| `converted_enrolment_id` | uuid FK | Yes | Set only after enrolment exists |

### `core.mobilisation_interactions`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `interaction_id` | uuid PK | No | One event |
| `mobilisation_case_id` | uuid FK | No | Parent case |
| `interaction_at` | timestamptz | No | Event time/date |
| `channel_code` | text | No | call/visit/camp/message/other |
| `outcome_code` | text | Yes | Controlled |
| `notes` | text | Yes | No unnecessary sensitive detail |
| `next_action_at` | timestamptz | Yes | Follow-up due |
| `staff_id` | uuid FK | Yes | Actor/owner |

## Training

### `core.batches`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `batch_id` | uuid PK | No | Immutable |
| `batch_code` | text | No | Unique business code |
| `project_id` | uuid FK | No | Donor/programme context |
| `location_id` | uuid FK | No | Centre |
| `planned_intake` | integer | Yes | Non-negative |
| `planned_start_date`, `planned_end_date` | date | Yes | Separate from actual |
| `actual_start_date`, `actual_end_date` | date | Yes | Evidence-based |
| `batch_status_code` | text | No | planned/active/completed/cancelled |

### `core.enrolments`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `enrolment_id` | uuid PK | No | Immutable |
| `participant_id` | uuid FK | No | Participant |
| `batch_id` | uuid FK | No | Batch |
| `attempt_number` | integer | No | Default 1 |
| `registration_date`, `enrolment_date` | date | Yes | Keep distinct only where source supports |
| `status_code` | text | No | enrolled/active/completed/dropped/reentered/withdrawn |
| `completion_date` | date | Yes | Required for completed |
| `exit_date` | date | Yes | Required for terminal exits where known |
| `exit_reason_code` | text | Yes | Required for dropout/withdrawal |
| `reentry_date` | date | Yes | For approved re-entry |

Unique: `(participant_id, batch_id, attempt_number)`.

### `core.sessions`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `session_id` | uuid PK | No | Immutable |
| `batch_id` | uuid FK | No | Parent batch |
| `session_sequence` | integer | No | Unique within batch |
| `module_code` | text | No | Retail/digital/communication/financial_literacy/life_skills/approved other |
| `topic` | text | Yes | Session topic |
| `planned_date`, `actual_date` | date | Yes | Never overwrite planned with actual |
| `delivery_status_code` | text | No | planned/delivered/rescheduled/cancelled |
| `status_reason_code` | text | Yes | Required for cancelled/rescheduled |
| `facilitator_staff_id` | uuid FK | Yes | Staff |

### `core.attendance`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `attendance_id` | uuid PK | No | Immutable |
| `enrolment_id` | uuid FK | No | Enrolment |
| `session_id` | uuid FK | No | Same batch as enrolment |
| `attendance_status_code` | text | No | Approved values |
| `attendance_reason_code` | text | Yes | Required where policy says |
| `recorded_at` | timestamptz | No | Audit time |

Unique: `(enrolment_id, session_id)`.

### `core.assessment_events` and `core.assessment_results`

| Table/field | Type | Null | Rule |
|---|---|---:|---|
| `assessment_events.assessment_event_id` | uuid PK | No | One sitting |
| `assessment_events.enrolment_id` | uuid FK | No | Enrolment |
| `assessment_events.assessment_point` | text | No | baseline/midline/endline |
| `assessment_events.attempt_number` | integer | No | Default 1 |
| `assessment_events.assessment_date` | date | Yes | Null only when planned/missing record |
| `assessment_events.completion_status` | text | No | complete/partial/missing/not_due |
| `assessment_events.missing_reason_code` | text | Yes | Required when missing |
| `assessment_results.assessment_result_id` | uuid PK | No | One domain result |
| `assessment_results.assessment_event_id` | uuid FK | No | Parent event |
| `assessment_results.rubric_item_id` | uuid FK | No | Versioned domain definition |
| `assessment_results.score_value` | numeric | Yes | Between 0 and maximum |
| `assessment_results.score_percent` | numeric | Yes | Derived, not manually entered |

### `core.readiness_reviews`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `readiness_review_id` | uuid PK | No | Dated review |
| `enrolment_id` | uuid FK | No | Enrolment |
| `review_date` | date | No | Review date |
| `profile_complete` | boolean | No | Evidence rule required |
| `documents_verified` | boolean | No | No document files in this table |
| `resume_current` | boolean | No | Current as of review |
| `interview_ready` | boolean | No | Approved assessment rule |
| `overall_ready` | boolean | No | Derived from approved rule |
| `gap_notes` | text | Yes | Outstanding actions |

## Placement and outcomes

### `core.employers` and `core.vacancies`

| Table/field | Type | Null | Rule |
|---|---|---:|---|
| `employers.employer_id` | uuid PK | No | One organisation |
| `employers.employer_name` | text | No | Normalised; aliases handled in lineage |
| `employers.sector_code` | text | Yes | Controlled |
| `employers.relationship_status_code` | text | No | prospect/active/inactive |
| `employers.last_verified_date` | date | Yes | Activity freshness |
| `employers.accessibility_notes` | text | Yes | Operational information |
| `vacancies.vacancy_id` | uuid PK | No | One opportunity |
| `vacancies.employer_id` | uuid FK | No | Employer |
| `vacancies.role_title` | text | No | Job title |
| `vacancies.location_id` | uuid FK | Yes | Work location |
| `vacancies.openings_count` | integer | Yes | Non-negative |
| `vacancies.status_code` | text | No | open/on_hold/closed/filled |
| `vacancies.open_date`, `vacancies.close_date` | date | Yes | Valid interval |
| `vacancies.requirements`, `vacancies.accessibility_notes` | text | Yes | Matching inputs |

### `core.candidate_vacancy_matches`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `candidate_vacancy_match_id` | uuid PK | No | One attempt |
| `enrolment_id` | uuid FK | No | Candidate programme stay |
| `vacancy_id` | uuid FK | No | Opportunity |
| `match_attempt` | integer | No | Default 1 |
| `skills_fit`, `preference_fit`, `location_fit`, `accessibility_fit` | boolean | Yes | Unknown is distinct from false |
| `suitability_status_code` | text | No | suitable/partly_suitable/not_suitable/not_assessed |
| `suitability_reason` | text | Yes | Required for non-suitable decisions |
| `pipeline_stage_code` | text | No | mapped/referred/interviewed/selected/offered/rejected/withdrawn/joined |
| `referred_at`, `interviewed_at`, `offered_at` | date | Yes | Milestone dates |
| `stage_reason_code` | text | Yes | Rejection/withdrawal reason |

### `core.employments`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `employment_id` | uuid PK | No | One employment episode |
| `candidate_vacancy_match_id` | uuid FK | Yes | May be null for verified historical placements |
| `participant_id` | uuid FK | No | Person |
| `employer_id` | uuid FK | No | Employer |
| `role_title` | text | No | Actual joined role |
| `join_date` | date | No | Verified actual joining |
| `employment_status_code` | text | No | active/ended/unknown |
| `end_date`, `end_reason_code` | date/text | Yes | Required as applicable |
| `joining_income_amount` | numeric | Yes | Non-negative |
| `income_currency`, `income_period_code` | text | Yes | Required with amount |
| `joining_verified`, `joining_verified_at` | boolean/timestamptz | No/Yes | Evidence status |

### `core.employment_followups`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `employment_followup_id` | uuid PK | No | One attempt/checkpoint |
| `employment_id` | uuid FK | No | Employment episode |
| `checkpoint_month` | integer | No | Normally 12 or 24; extensible |
| `attempt_number` | integer | No | Follow-up attempts preserved |
| `due_date`, `completed_date` | date | No/Yes | Completed may be null while pending |
| `verification_status_code` | text | No | pending/verified/unverified/unreachable |
| `retention_status_code` | text | Yes | same_employer/different_employer/exited/unknown |
| `current_employer_id` | uuid FK | Yes | Allows change of employer |
| `current_role_title` | text | Yes | Current role |
| `current_income_amount` | numeric | Yes | Comparable amount |
| `income_currency`, `income_period_code` | text | Yes | Required with amount |
| `exit_reason_code` | text | Yes | If not employed |

Unique: `(employment_id, checkpoint_month, attempt_number)`.

## Staff and security

`core.staff` stores `staff_id`, name, work email, title, active flag and optional auth user ID. `security.user_roles` stores `auth_user_id`, role code, optional project/location scope, valid dates and active flag. Permission enforcement is implemented with RLS after approval.

## Audit dictionary

`audit.import_runs`, `audit.source_records`, `audit.identity_reviews`, `audit.data_quality_issues` and `audit.change_log` are defined in the architecture document. Source records include source asset ID, sheet/table, row key, raw hash, import run, target entity/table/ID and disposition.
