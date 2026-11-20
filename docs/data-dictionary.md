# Voice of Needy IDS logical data dictionary

**Version:** 4 field-level proposal  
**Status:** For analyst, frontend and senior-management review. Types and constraints are logical until SQL migrations are approved.

The editable diagram and this dictionary are generated from the same entity specification. All operational tables also carry `created_at`, `updated_at`, `created_by` and `updated_by` where applicable.

## 1. core.participants

One canonical person; current identity, profile, contact and support details.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `participant_id` | uuid NOT NULL |
| UQ | `participant_code` | text NOT NULL |
| — | `first_name` | text NOT NULL |
| — | `middle_name` | text NULL |
| — | `last_name` | text NULL |
| — | `gender_code` | text NULL |
| — | `date_of_birth` | date NULL |
| — | `primary_mobile` | text NULL, restricted |
| — | `primary_email` | text NULL, restricted |
| — | `mobile_verified` | boolean NOT NULL |
| — | `email_verified` | boolean NOT NULL |
| — | `disability_type` | text NULL, restricted |
| — | `disability_percent` | numeric(5,2) NULL |
| — | `education_level` | text NULL |
| — | `address` | text NULL, restricted |
| — | `district` | text NULL |
| — | `state` | text NULL |
| — | `pin_code` | text NULL |
| — | `family_income` | numeric NULL, restricted |
| — | `parent_guardian` | jsonb NULL, validated |
| — | `support_preferences` | jsonb NULL, validated |
| — | `external_file_number` | text NULL |
| — | `identity_status` | text NOT NULL, check |
| — | `record_status` | text NOT NULL, check |

## 2. core.participant_identifiers

Multiple VoN, legacy, candidate, roster and external identifiers per participant.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `participant_identifier_id` | uuid NOT NULL |
| FK | `participant_id` | uuid NOT NULL |
| — | `identifier_type` | text NOT NULL, check |
| — | `identifier_value` | text NOT NULL, restricted |
| — | `normalised_hash` | text NULL |
| — | `is_primary` | boolean NOT NULL |
| — | `is_verified` | boolean NOT NULL |
| — | `verified_at` | timestamptz NULL |
| — | `source_record_id` | uuid NULL |
| UQ | `type + value/hash` | partial uniqueness |

## 3. core.projects

Programme/donor project context used across mobilisation, delivery and outcomes.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `project_id` | uuid NOT NULL |
| UQ | `project_code` | text NOT NULL |
| — | `project_name` | text NOT NULL |
| — | `donor_name` | text NULL |
| — | `financial_year` | text NULL |
| — | `start_date` | date NULL |
| — | `end_date` | date NULL |
| — | `target_participants` | integer NULL >= 0 |
| — | `centre_codes` | text[] NULL |
| — | `is_active` | boolean NOT NULL |

## 4. core.outreach_events

One sourcing, mobilisation, call or eligibility event; may precede identity resolution.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `outreach_event_id` | uuid NOT NULL |
| FK | `participant_id` | uuid NULL |
| FK | `project_id` | uuid NULL |
| — | `event_type` | text NOT NULL, check |
| — | `event_date` | date NULL |
| — | `source_channel` | text NULL |
| — | `source_name` | text NULL |
| — | `call_response` | text NULL |
| — | `eligibility_status` | text NULL, check |
| — | `outcome_status` | text NULL, check |
| — | `outcome_reason` | text NULL |
| — | `next_followup_date` | date NULL |
| — | `owner_user_id` | uuid NULL |
| — | `record_classification` | text NULL |
| — | `source_attributes` | jsonb NULL, validated |

## 5. core.batches

One training cohort with planned and actual delivery context.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `batch_id` | uuid NOT NULL |
| UQ | `batch_code` | text NOT NULL |
| FK | `project_id` | uuid NOT NULL |
| — | `original_batch_ids` | jsonb NULL, validated |
| — | `financial_year` | text NULL |
| — | `centre_code` | text NULL |
| — | `centre_name` | text NULL |
| — | `planned_intake` | integer NULL >= 0 |
| — | `planned_start_date` | date NULL |
| — | `planned_end_date` | date NULL |
| — | `actual_start_date` | date NULL |
| — | `actual_end_date` | date NULL |
| — | `planned_session_count` | integer NULL >= 0 |
| — | `trainer_details` | jsonb NULL, validated |
| — | `planned_topics` | jsonb NULL, validated |
| — | `batch_status` | text NOT NULL, check |
| — | `plan_evidence_url` | text NULL |
| — | `completion_evidence_url` | text NULL |

## 6. core.enrolments

One participant attempt in one batch; training, completion, dropout and readiness.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `enrolment_id` | uuid NOT NULL |
| FK | `participant_id` | uuid NOT NULL |
| FK | `batch_id` | uuid NOT NULL |
| UQ | `participant + batch + attempt` | unique |
| — | `candidate_enrolment_code` | text NULL |
| — | `attempt_number` | integer NOT NULL |
| — | `registration_date` | date NULL |
| — | `training_start_date` | date NULL |
| — | `training_end_date` | date NULL |
| — | `status` | text NOT NULL, check |
| — | `completion_status` | text NULL, check |
| — | `completion_date` | date NULL |
| — | `dropout_stage` | text NULL |
| — | `dropout_reason_category` | text NULL |
| — | `dropout_reason_detail` | text NULL |
| — | `reentry_date` | date NULL |
| — | `profile_complete` | boolean NULL |
| — | `documents_verified` | boolean NULL |
| — | `resume_current` | boolean NULL |
| — | `interview_ready` | boolean NULL |
| — | `readiness_review_date` | date NULL |
| — | `readiness_notes` | text NULL |

## 7. core.sessions

One planned/delivered session for one batch; normalises Session 01–45 columns.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `session_id` | uuid NOT NULL |
| FK | `batch_id` | uuid NOT NULL |
| UQ | `batch + session_number` | unique |
| — | `session_number` | integer NOT NULL > 0 |
| — | `module_code` | text NULL |
| — | `topic` | text NULL |
| — | `planned_date` | date NULL |
| — | `actual_date` | date NULL |
| — | `delivery_status` | text NOT NULL, check |
| — | `status_reason` | text NULL |
| — | `facilitator_details` | jsonb NULL, validated |
| — | `evidence_url` | text NULL |
| — | `session_notes` | text NULL |

## 8. core.attendance

One enrolment-session result; normalises Day 01–46 marks and source rosters.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `attendance_id` | uuid NOT NULL |
| FK | `enrolment_id` | uuid NOT NULL |
| FK | `session_id` | uuid NOT NULL |
| UQ | `enrolment + session` | unique |
| — | `attendance_date` | date NULL |
| — | `attendance_status` | text NOT NULL, check |
| — | `reason` | text NULL |
| — | `source_register_id` | text NULL |
| — | `source_mark` | text NULL |
| — | `verified` | boolean NOT NULL |
| — | `verification_notes` | text NULL |

## 9. core.assessments

One enrolment, assessment point/week and domain result.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `assessment_id` | uuid NOT NULL |
| FK | `enrolment_id` | uuid NOT NULL |
| UQ | `enrolment + type + period + domain + attempt` | unique |
| — | `assessment_type` | text NOT NULL, check |
| — | `period_code` | text NULL |
| — | `domain_code` | text NULL |
| — | `domain_label` | text NULL |
| — | `attempt_number` | integer NOT NULL |
| — | `assessment_date` | date NULL |
| — | `rubric_version` | text NULL |
| — | `score_value` | numeric NULL |
| — | `maximum_score` | numeric NULL > 0 |
| — | `score_percent` | numeric generated/derived |
| — | `completion_status` | text NOT NULL, check |
| — | `missing_reason` | text NULL |
| — | `source_result` | jsonb NULL, validated |

## 10. core.employers

One employer organisation and its current engagement profile.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `employer_id` | uuid NOT NULL |
| UQ | `employer_code` | text NOT NULL |
| — | `employer_name` | text NOT NULL |
| — | `location_address` | text NULL |
| — | `contact_name` | text NULL, restricted |
| — | `contact_designation` | text NULL |
| — | `contact_number` | text NULL, restricted |
| — | `contact_email` | text NULL, restricted |
| — | `sector` | text NULL |
| — | `disability_types_considered` | text[] NULL |
| — | `accessibility_notes` | text NULL |
| — | `existing_staff_with_disability` | integer NULL >= 0 |
| — | `required_staff_with_disability` | integer NULL >= 0 |
| — | `last_contact_date` | date NULL |
| — | `verification_status` | text NOT NULL, check |

## 11. core.job_opportunities

One role/vacancy at one employer; supports open-vacancy and matching questions.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `job_opportunity_id` | uuid NOT NULL |
| FK | `employer_id` | uuid NOT NULL |
| FK | `project_id` | uuid NULL |
| — | `role_title` | text NOT NULL |
| — | `work_type` | text NULL |
| — | `location` | text NULL |
| — | `education_required` | text NULL |
| — | `skills_required` | jsonb NULL, validated |
| — | `accessibility_requirements` | text NULL |
| — | `salary_amount` | numeric NULL >= 0 |
| — | `salary_period` | text NULL, check |
| — | `vacancies_count` | integer NULL >= 0 |
| — | `open_date` | date NULL |
| — | `close_date` | date NULL |
| — | `status` | text NOT NULL, check |

## 12. core.placement_attempts

One candidate-opportunity attempt from mapping through verified joining/exit.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `placement_attempt_id` | uuid NOT NULL |
| FK | `enrolment_id` | uuid NOT NULL |
| FK | `job_opportunity_id` | uuid NULL |
| UQ | `enrolment + opportunity + attempt` | unique when linked |
| — | `attempt_number` | integer NOT NULL |
| — | `skills_fit` | boolean NULL |
| — | `preference_fit` | boolean NULL |
| — | `location_fit` | boolean NULL |
| — | `accessibility_fit` | boolean NULL |
| — | `suitability_status` | text NULL, check |
| — | `suitability_reason` | text NULL |
| — | `pipeline_stage` | text NOT NULL, check |
| — | `referral_date` | date NULL |
| — | `interview_date` | date NULL |
| — | `offer_date` | date NULL |
| — | `joining_date` | date NULL |
| — | `actual_employer_name` | text NULL |
| — | `actual_job_role` | text NULL |
| — | `joining_salary` | numeric NULL >= 0 |
| — | `salary_period` | text NULL, check |
| — | `offer_letter_available` | boolean NOT NULL |
| — | `joining_verified` | boolean NOT NULL |
| — | `placement_status` | text NOT NULL, check |
| — | `rejection_or_exit_reason` | text NULL |
| — | `status_date` | date NULL |
| — | `evidence_url` | text NULL |

## 13. core.followups

One employment follow-up/checkpoint attempt after placement.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `followup_id` | uuid NOT NULL |
| FK | `placement_attempt_id` | uuid NOT NULL |
| UQ | `placement + checkpoint + attempt` | unique |
| — | `checkpoint_month` | integer NULL |
| — | `attempt_number` | integer NOT NULL |
| — | `due_date` | date NULL |
| — | `followup_date` | date NULL |
| — | `employment_status` | text NULL, check |
| — | `current_workplace` | text NULL |
| — | `previous_workplace` | text NULL |
| — | `current_job_role` | text NULL |
| — | `monthly_salary` | numeric NULL >= 0 |
| — | `salary_period` | text NULL, check |
| — | `reason_for_leaving` | text NULL |
| — | `verification_status` | text NOT NULL, check |
| — | `evidence_url` | text NULL |
| — | `notes` | text NULL |

## 14. staging.import_runs

One repeatable import execution with reconciliation counts.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `import_run_id` | uuid NOT NULL |
| — | `source_asset_name` | text NOT NULL |
| — | `source_asset_id` | text NULL |
| — | `source_version` | text NULL |
| — | `pipeline_version` | text NOT NULL |
| — | `started_at` | timestamptz NOT NULL |
| — | `completed_at` | timestamptz NULL |
| — | `status` | text NOT NULL, check |
| — | `source_count` | integer NOT NULL >= 0 |
| — | `staged_count` | integer NOT NULL >= 0 |
| — | `loaded_count` | integer NOT NULL >= 0 |
| — | `rejected_count` | integer NOT NULL >= 0 |
| — | `unresolved_count` | integer NOT NULL >= 0 |
| — | `error_summary` | text NULL |

## 15. staging.source_records

One immutable source row plus validation, identity decision and target lineage.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `source_record_id` | uuid NOT NULL |
| FK | `import_run_id` | uuid NOT NULL |
| — | `source_file_id` | text NULL |
| — | `source_file_name` | text NOT NULL |
| — | `source_sheet_name` | text NULL |
| — | `source_row_number` | integer NULL |
| — | `source_record_key` | text NOT NULL |
| — | `source_checksum` | text NOT NULL |
| — | `raw_payload` | jsonb NOT NULL, restricted |
| — | `standardised_payload` | jsonb NULL |
| — | `validation_status` | text NOT NULL, check |
| — | `validation_issues` | jsonb NULL |
| — | `identity_match_status` | text NULL, check |
| — | `match_confidence` | numeric NULL |
| — | `review_decision` | text NULL, check |
| — | `reviewed_by` | uuid NULL |
| — | `reviewed_at` | timestamptz NULL |
| — | `target_table` | text NULL |
| — | `target_record_id` | uuid NULL |
| — | `disposition` | text NOT NULL, check |

## 16. audit.change_log

Material change history for protected operational records.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `change_log_id` | uuid NOT NULL |
| — | `target_table` | text NOT NULL |
| — | `target_record_id` | uuid NOT NULL |
| — | `operation` | text NOT NULL, check |
| — | `changed_fields` | text[] NULL |
| — | `before_values` | jsonb NULL, restricted |
| — | `after_values` | jsonb NULL, restricted |
| — | `actor_user_id` | uuid NULL |
| — | `changed_at` | timestamptz NOT NULL |
| — | `request_id` | text NULL |

## 17. security.user_access

Role and optional project/centre access scope for an authenticated user.

| Key | Field | Type / constraint |
|---|---|---|
| PK | `user_access_id` | uuid NOT NULL |
| FK | `auth_user_id` | uuid NOT NULL -> auth.users |
| — | `role_code` | text NOT NULL, check |
| FK | `project_id` | uuid NULL |
| — | `centre_code` | text NULL |
| — | `valid_from` | date NULL |
| — | `valid_to` | date NULL |
| — | `is_active` | boolean NOT NULL |
| — | `granted_by` | uuid NULL |
| — | `granted_at` | timestamptz NOT NULL |

## Controlled values

Stable status fields use PostgreSQL check constraints or enum/domain types defined in version-controlled migrations. A separate lookup table is introduced only when VoN needs users to administer the values at runtime.

Minimum controlled lists include outreach event/outcome/eligibility, batch/enrolment/session/attendance/assessment status, placement pipeline/status, follow-up employment/verification status, identifier type, salary period, user role and import disposition.

## Privacy

Phone, email, address, government/external identifiers, disability/support information, income and raw source payloads are restricted. Reporting views exclude direct identifiers unless an authorised operational use requires them.
