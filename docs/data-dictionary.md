# Voice of Needy IDS reduced logical data dictionary

**Version:** 3  
**Status:** Logical proposal; PostgreSQL types are provisional.

All business tables use UUID primary keys and include `created_at`, `updated_at`, `created_by` and `updated_by` where applicable. `created_by`/`updated_by` reference the authenticated user identity, so a separate staff table is unnecessary in release 1.

## 1. `core.participants`

One real person. Primary identity/profile/contact/support values are stored as columns; alternative values are retained in validated JSON arrays.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `participant_id` | uuid PK | No | Immutable system key |
| `participant_code` | text unique | No | Human-readable VoN ID |
| `first_name`, `middle_name`, `last_name` | text | Mixed | Do not fabricate missing name components |
| `gender_code` | text | Yes | Controlled constraint |
| `date_of_birth` | date | Yes | Age is calculated, not stored |
| `primary_mobile`, `primary_email` | text | Yes | Restricted/masked; verification flags separate |
| `mobile_verified`, `email_verified` | boolean | No | Default false |
| `disability_type`, `disability_percent` | text/numeric | Yes | Restricted; percent 0–100 |
| `education_level` | text | Yes | Controlled/standardised where possible |
| `address`, `district`, `state`, `pin_code` | text | Yes | Pin code remains text |
| `family_income` | numeric | Yes | Restricted; non-negative |
| `parent_guardian_details` | jsonb | Yes | Validated name/relationship/contact structure |
| `accessibility_and_support` | jsonb | Yes | Requirements, preferences and career goals |
| `alternate_identifiers` | jsonb | Yes | Type/value/verified/source array |
| `alternate_contacts` | jsonb | Yes | Type/value/relationship/verified array |
| `external_file_number` | text | Yes | Historical VoN reference |
| `identity_status` | text | No | verified/pending_review/unresolved |
| `record_status` | text | No | active/inactive/deceased |

## 2. `core.outreach_records`

One sourcing, mobilisation or follow-up contact event. It can exist before participant identity is resolved.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `outreach_record_id` | uuid PK | No | Immutable |
| `participant_id` | uuid FK | Yes | Null until identity is resolved |
| `project_id` | uuid FK | Yes | Interested/associated project |
| `event_type` | text | No | sourced/contacted/follow_up/eligibility_review |
| `event_date` | date | Yes | Historical value may be unavailable |
| `source_channel` | text | Yes | Camp/referral/list/call/other |
| `source_name` | text | Yes | Partner/list/camp detail |
| `call_response` | text | Yes | Controlled value |
| `eligibility_status` | text | Yes | eligible/ineligible/pending/not_assessed |
| `outcome_status` | text | Yes | interested/not_interested/enrolled/unreachable/etc. |
| `outcome_reason` | text | Yes | Required for approved terminal statuses |
| `next_followup_date` | date | Yes | Future action |
| `owner_user_id` | uuid | Yes | Auth user |
| `source_attributes` | jsonb | Yes | Non-core source-only attributes |

## 3. `core.projects`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `project_id` | uuid PK | No | Immutable |
| `project_code` | text unique | No | Stable business code |
| `project_name`, `donor_name` | text | No/Yes | Approved display values |
| `financial_year` | text | Yes | Standard format |
| `start_date`, `end_date` | date | Yes | Valid interval |
| `target_participants` | integer | Yes | Non-negative |
| `centre_codes` | text[] | Yes | Approved centres |
| `is_active` | boolean | No | Default true |

## 4. `core.batches`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `batch_id` | uuid PK | No | Immutable |
| `batch_code` | text unique | No | Canonical batch ID |
| `project_id` | uuid FK | No | Project/donor context |
| `original_batch_ids` | jsonb | Yes | Source batch labels and files |
| `financial_year`, `centre_code`, `centre_name` | text | Yes | Standardised reporting context |
| `planned_intake` | integer | Yes | Non-negative |
| `planned_start_date`, `planned_end_date` | date | Yes | Planned dates |
| `actual_start_date`, `actual_end_date` | date | Yes | Evidence-based actuals |
| `planned_session_count` | integer | Yes | Non-negative |
| `trainer_details`, `planned_topics` | jsonb | Yes | Low-volume structured arrays |
| `batch_status` | text | No | planned/active/completed/cancelled |
| `plan_evidence_url`, `completion_evidence_url` | text | Yes | Restricted as required |

## 5. `core.enrolments`

One participant attempt in one batch.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `enrolment_id` | uuid PK | No | Immutable |
| `participant_id`, `batch_id` | uuid FK | No | Parent participant and batch |
| `candidate_enrolment_code` | text | Yes | Historical/frontend business code |
| `attempt_number` | integer | No | Default 1 |
| `registration_date`, `training_start_date`, `training_end_date` | date | Yes | Source-evidenced |
| `status` | text | No | registered/enrolled/active/completed/dropped/withdrawn/reentered |
| `days_attended` | integer | Yes | Derived from attendance when detailed data exists |
| `completion_status`, `completion_date` | text/date | Yes | Approved completion rule |
| `dropout_stage`, `dropout_reason_category`, `dropout_reason_detail` | text | Yes | Required as applicable |
| `reentry_date` | date | Yes | Approved re-entry |
| `profile_complete`, `documents_verified`, `resume_current`, `interview_ready` | boolean | Yes | Null means not assessed, not false |
| `readiness_review_date`, `readiness_notes` | date/text | Yes | Latest approved review |
| `original_registration_numbers` | jsonb | Yes | Source identifiers |

Unique: `(participant_id, batch_id, attempt_number)`.

## 6. `core.sessions`

One planned/delivered batch session. The 45 Master Sheet session columns become rows.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `session_id` | uuid PK | No | Immutable |
| `batch_id` | uuid FK | No | Parent batch |
| `session_number` | integer | No | Positive; unique within batch |
| `module_code`, `topic` | text | Yes | Approved module/description |
| `planned_date`, `actual_date` | date | Yes | Keep separate |
| `delivery_status` | text | No | planned/delivered/rescheduled/cancelled |
| `status_reason` | text | Yes | Required for rescheduled/cancelled |
| `facilitator_details` | jsonb | Yes | One or more facilitator references |
| `evidence_url`, `session_notes` | text | Yes | Supporting evidence |

Unique: `(batch_id, session_number)`.

## 7. `core.attendance`

One enrolment in one session. The Day 1–46 columns become rows.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `attendance_id` | uuid PK | No | Immutable |
| `enrolment_id`, `session_id` | uuid FK | No | Must belong to same batch |
| `attendance_date` | date | Yes | Session actual/planned date where known |
| `attendance_status` | text | No | present/absent/late/leave/not_marked |
| `reason` | text | Yes | Approved reason where required |
| `source_register_id`, `source_mark` | text | Yes | Original attendance evidence |
| `verified` | boolean | No | Default false |
| `verification_notes` | text | Yes | Review outcome |

Unique: `(enrolment_id, session_id)`.

## 8. `core.assessments`

One assessment result for one enrolment, point/week and domain. Assessment event/result/rubric metadata are combined.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `assessment_id` | uuid PK | No | Immutable |
| `enrolment_id` | uuid FK | No | Parent enrolment |
| `assessment_type` | text | No | baseline/midline/endline/weekly/kredo_mid/kredo_final |
| `period_code` | text | Yes | Week number or assessment point |
| `domain_code`, `domain_label` | text | Yes | Technical/behavioural/approved domain |
| `attempt_number` | integer | No | Default 1 |
| `assessment_date` | date | Yes | Actual date |
| `rubric_version` | text | Yes | Preserves comparability |
| `score_value`, `maximum_score` | numeric | Yes | Valid range |
| `score_percent` | numeric | Yes | Derived |
| `completion_status` | text | No | complete/partial/missing/not_due |
| `missing_reason` | text | Yes | Required when missing |
| `source_result` | jsonb | Yes | Source-specific non-core detail |

## 9. `core.employers`

| Field | Type | Null | Rule |
|---|---|---:|---|
| `employer_id` | uuid PK | No | Immutable |
| `employer_code` | text unique | No | Stable code |
| `employer_name` | text | No | Normalised name |
| `location_address` | text | Yes | Work/office location |
| `contact_name`, `contact_designation`, `contact_number`, `contact_email` | text | Yes | Restricted contact data |
| `sector`, `accessibility_notes` | text | Yes | Matching/reporting |
| `disability_types_considered` | text[] | Yes | Approved values |
| `existing_staff_with_disability`, `required_staff_with_disability` | integer | Yes | Non-negative |
| `last_contact_date` | date | Yes | Engagement freshness |
| `verification_status` | text | No | pending/verified/inactive |

## 10. `core.job_opportunities`

One role/vacancy at an employer. Rows may be created by splitting multi-role employer source cells during reviewed migration.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `job_opportunity_id` | uuid PK | No | Immutable |
| `employer_id` | uuid FK | No | Parent employer |
| `project_id` | uuid FK | Yes | Project engagement context |
| `role_title`, `work_type` | text | No/Yes | Opportunity |
| `location` | text | Yes | Standardised where possible |
| `education_required`, `skills_required` | text/jsonb | Yes | Matching inputs |
| `accessibility_requirements` | text | Yes | Matching input |
| `salary_amount`, `salary_period` | numeric/text | Yes | Comparable units |
| `vacancies_count` | integer | Yes | Non-negative |
| `open_date`, `close_date` | date | Yes | Valid interval |
| `status` | text | No | open/on_hold/filled/closed |

## 11. `core.placements`

One enrolment-opportunity attempt. It covers mapping through verified joining.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `placement_id` | uuid PK | No | Immutable |
| `enrolment_id`, `job_opportunity_id` | uuid FK | No | Candidate and opportunity |
| `attempt_number` | integer | No | Default 1 |
| `skills_fit`, `preference_fit`, `location_fit`, `accessibility_fit` | boolean | Yes | Null means not assessed |
| `suitability_status`, `suitability_reason` | text | Yes | Approved rule |
| `pipeline_stage` | text | No | mapped/referred/interviewed/selected/offered/joined/rejected/withdrawn |
| `referral_date`, `interview_date`, `offer_date`, `joining_date` | date | Yes | Milestones |
| `actual_employer_name`, `actual_job_role` | text | Yes | Preserves historical placement if opportunity incomplete |
| `joining_salary`, `salary_period` | numeric/text | Yes | Comparable units |
| `offer_letter_available`, `joining_verified` | boolean | No | Defaults false |
| `placement_status` | text | No | pending/active/ended/not_joined |
| `rejection_reason`, `exit_reason`, `status_date` | text/date | Yes | Required as applicable |
| `evidence_url` | text | Yes | Controlled access |

Unique: `(enrolment_id, job_opportunity_id, attempt_number)`.

## 12. `core.followups`

One follow-up attempt/checkpoint after placement.

| Field | Type | Null | Rule |
|---|---|---:|---|
| `followup_id` | uuid PK | No | Immutable |
| `placement_id` | uuid FK | No | Parent placement |
| `checkpoint_month` | integer | Yes | 3/6/12/24 or approved value |
| `attempt_number` | integer | No | Default 1 |
| `due_date`, `followup_date` | date | Yes | Due/actual separate |
| `employment_status` | text | Yes | same_employer/different_employer/exited/unreachable/unverified |
| `current_workplace`, `previous_workplace`, `current_job_role` | text | Yes | Current state |
| `monthly_salary`, `salary_period` | numeric/text | Yes | Comparable units |
| `reason_for_leaving` | text | Yes | If exited |
| `verification_status` | text | No | pending/verified/unverified/unreachable |
| `evidence_url`, `notes` | text | Yes | Evidence and interpretation |

## Audit and security

### `audit.import_runs`

Source asset, started/completed times, status, source/staged/loaded/rejected/unresolved counts, pipeline version and error summary.

### `audit.source_records`

Import run, source file/tab/row, source record ID, checksum/raw reference, proposed/matched participant and batch IDs, match confidence/status, reviewer decision, quality issues JSON, resolution notes, target table/ID and disposition. This replaces separate lineage, identity-review and exception tables without losing their fields.

### `audit.change_log`

Target table/ID, operation, changed fields, before/after snapshots subject to privacy controls, actor and timestamp.

### `security.user_access`

Auth user ID, role, optional project/centre scope, valid dates and active flag. Authentication identities remain in the platform auth schema.
