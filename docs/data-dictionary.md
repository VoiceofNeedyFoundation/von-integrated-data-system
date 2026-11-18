# Draft logical data dictionary

**Status:** Proposed field-level companion to [data-model.md](data-model.md). Types and required fields are provisional until business review and source-to-target mapping are complete. No database objects have been created.

## Conventions

- Primary keys use immutable UUIDs.
- Every operational table will include `created_at`, `updated_at`, `created_by` and an appropriate audit mechanism.
- Historical fields may be null when not collected. Null is not used to mean not applicable or refused where those meanings matter; explicit status fields are used.
- Original source values are preserved through source lineage and, where needed, an `original_value` alongside the canonical value.
- Personal, disability, document and employment information is sensitive and must be access-controlled.

## 1. Participant identity

### `participant`

Canonical person identity. Existence does not imply registration, training or placement.

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| participant_id | UUID | Yes | Internal immutable key |
| participant_code | Text | After approval | Human-readable VoN ID; format pending |
| given_name | Text | When known | Normalised first/given name |
| middle_name | Text | No | Normalised middle name |
| family_name | Text | No | Normalised surname/family name |
| display_name | Text | Yes | Operational display name |
| date_of_birth | Date | No | Verified or reported DOB |
| birth_year | Integer | No | Used when full DOB was not collected |
| gender_code | Reference | No | Approved controlled value |
| identity_status | Reference | Yes | provisional, verified, disputed, merged, restricted |
| deceased_flag | Boolean | No | Only when operationally required |
| notes | Text | No | Restricted non-source narrative |

### `participant_identifier`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| participant_identifier_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Canonical participant |
| identifier_type | Reference | Yes | master ID, candidate ID, portal ID, legacy ID, etc. |
| identifier_value | Text | Yes | Exact identifier value |
| issuing_system | Text/Reference | Yes | Source system/organisation |
| valid_from / valid_to | Date | No | Validity period |
| verification_status | Reference | Yes | reported, matched, verified, disputed |
| is_primary | Boolean | Yes | Primary identifier for that type |

Unique rule: identifier type + issuing system + value cannot link to two active participants without a recorded conflict.

### `participant_contact`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| participant_contact_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Participant |
| contact_type | Reference | Yes | phone, email, address |
| contact_value | Text | Yes | Protected contact value |
| relationship_to_participant | Reference | No | self, parent, caregiver, other |
| contact_name | Text | No | Contact person where not self |
| is_primary | Boolean | Yes | Preferred contact of type |
| consent_to_contact | Boolean/Unknown | No | Consent state where collected |
| verified_at | Timestamp | No | Verification time |
| valid_from / valid_to | Date | No | History |

### `participant_profile`

Stores operational profile attributes separately from identity.

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| participant_profile_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Participant |
| disability_type_code | Reference | No | Approved category |
| disability_percentage | Decimal | No | Reported/verified percentage |
| disability_verification_status | Reference | No | reported, document verified, disputed |
| education_level_code | Reference | No | Highest known education |
| employment_status_code | Reference | No | Status at observation date |
| household_income_band_code | Reference | No | Band, when required |
| preferred_language_code | Reference | No | Communication/training language |
| accommodation_needs | Text | No | Restricted operational need |
| effective_from / effective_to | Date | No | Version validity |

### `participant_document_check`

Tracks verification state without unnecessarily copying document numbers or files.

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| document_check_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Participant |
| registration_id | UUID/FK | No | Related registration |
| document_type | Reference | Yes | UDID, disability certificate, education, bank, etc. |
| check_status | Reference | Yes | not requested, requested, received, verified, rejected, expired |
| checked_at | Timestamp | No | Verification time |
| checked_by | UUID/FK | No | Responsible user |
| issue_reason | Text | No | Missing/mismatch reason |
| secure_object_reference | Text | No | Reference to approved private storage, if used |

## 2. Sourcing and mobilisation

### `source_lead`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| source_lead_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | No | Null until safely resolved |
| source_channel_code | Reference | No | UDID list, referral, field visit, job fair, partner, social, other |
| source_organisation | Text/Reference | No | Referring organisation |
| sourced_on | Date | No | Observation/receipt date |
| location_id | UUID/FK | No | Source location |
| raw_name | Text | Yes | Source-record name retained through protected staging |
| lead_status | Reference | Yes | new, assigned, contacted, interested, not interested, unreachable, registered, closed, unknown |
| closure_reason_code | Reference | No | Reason for closure |
| source_record_id | UUID/FK | Yes | Provenance |

### `mobilisation_assignment`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| assignment_id | UUID | Yes | Primary key |
| source_lead_id | UUID/FK | Yes | Assigned lead |
| assigned_to_user_id | UUID/FK | Yes | Mobiliser |
| assigned_at | Timestamp | Yes | Assignment time |
| due_at | Timestamp | No | Follow-up deadline |
| assignment_status | Reference | Yes | active, reassigned, completed, cancelled |
| ended_at | Timestamp | No | Closure time |

### `mobilisation_interaction`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| interaction_id | UUID | Yes | Primary key |
| source_lead_id | UUID/FK | No | Related lead |
| participant_id | UUID/FK | No | Canonical participant if resolved |
| interaction_at | Timestamp | Yes for new data | Actual date/time |
| interaction_type | Reference | Yes | call, visit, counselling, awareness, message, other |
| outcome_code | Reference | Yes | connected, no answer, unreachable, interested, declined, callback, registered, other |
| next_action_code | Reference | No | Required follow-up |
| next_action_due_at | Timestamp | No | Due time |
| performed_by | UUID/FK | No | Staff/user |
| notes | Text | No | Restricted notes |
| source_record_id | UUID/FK | No | Required for migrated data |

## 3. Programme and registration

### `programme`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| programme_id | UUID | Yes | Primary key |
| programme_code | Text | Yes | Stable code |
| programme_name | Text | Yes | Approved name |
| description | Text | No | Purpose |
| active_from / active_to | Date | No | Operating period |

### `donor` and `project`

`donor` holds a canonical funding organisation. `project` records a donor-funded/time-bound implementation with programme, dates, approved name and reporting period.

Core project fields: `project_id`, `project_code`, `project_name`, `programme_id`, `donor_id`, `start_date`, `end_date`, `status`.

### `registration`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| registration_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Applicant |
| programme_id | UUID/FK | Yes | Programme |
| project_id | UUID/FK | No | Project if known |
| registered_on | Date | No historically; yes for new data | Registration date |
| registration_status | Reference | Yes | started, submitted, eligible, ineligible, verified, withdrawn, unknown |
| consent_status | Reference | No | not requested, provided, declined, unknown |
| eligibility_status | Reference | No | pending, eligible, ineligible, exception, unknown |
| eligibility_reason | Text | No | Reason/exception |
| registered_at_location_id | UUID/FK | No | Registration location |
| source_record_id | UUID/FK | No | Historical provenance |

### `location` and `training_site`

`location` stores a hierarchy using `location_id`, `parent_location_id`, `location_type`, `canonical_name` and official codes when available.

`training_site` stores `training_site_id`, `site_code`, `site_name`, `location_id`, `site_type`, `active_from` and `active_to`. This avoids assuming every historical label is a permanent centre.

## 4. Training

### `training_batch`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| batch_id | UUID | Yes | Primary key |
| batch_code | Text | Yes | Stable VoN batch code |
| batch_name | Text | No | Display label |
| programme_id | UUID/FK | Yes | Programme |
| project_id | UUID/FK | No | Donor/project |
| training_site_id | UUID/FK | No | Delivery site |
| planned_start_date / planned_end_date | Date | No | Plan |
| actual_start_date / actual_end_date | Date | No | Observed dates |
| target_size | Integer | No | Planned capacity |
| batch_status | Reference | Yes | planned, enrolling, active, completed, cancelled, unknown |
| financial_year | Text/Reference | No | Approved FY representation |

### `enrolment`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| enrolment_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Participant |
| registration_id | UUID/FK | No | Registration, where available |
| batch_id | UUID/FK | Yes | Batch |
| enrolled_on | Date | No historically; yes for new data | Enrolment date |
| enrolment_status | Reference | Yes | enrolled, active, completed, discontinued, transferred, cancelled, unknown |
| exit_date | Date | No | Exit/completion date |
| exit_reason_code | Reference | No | Reason |
| source_record_id | UUID/FK | No | Provenance |

Repeat enrolment is allowed. A separately approved duplicate-detection rule should flag suspicious same-person/same-batch records.

### `session_definition`

Core fields: `session_definition_id`, `session_code`, `session_name`, `module_name`, `default_duration_minutes`, `sequence_hint`, `active_flag`.

### `batch_session`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| batch_session_id | UUID | Yes | Primary key |
| batch_id | UUID/FK | Yes | Batch |
| session_definition_id | UUID/FK | No | Curriculum definition |
| session_title | Text | Yes | Actual title |
| planned_start_at / planned_end_at | Timestamp | No | Planned schedule |
| actual_start_at / actual_end_at | Timestamp | No | Actual delivery |
| trainer_user_id | UUID/FK | No | Lead trainer |
| delivery_status | Reference | Yes | planned, completed, partial, postponed, cancelled, unknown |
| cancellation_reason | Text | No | Reason |
| delivery_notes | Text | No | Operational notes |

### `attendance`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| attendance_id | UUID | Yes | Primary key |
| enrolment_id | UUID/FK | Yes | Participant's batch enrolment |
| batch_session_id | UUID/FK | Yes | Session |
| attendance_status | Reference | Yes | present, absent, excused, not scheduled, unknown/not recorded |
| recorded_at | Timestamp | No | Entry time |
| recorded_by | UUID/FK | No | User |
| verification_status | Reference | Yes | reported, verified, disputed |
| source_record_id | UUID/FK | No | Historical provenance |

Unique rule: one active attendance decision per enrolment and batch session. Corrections are audited.

### `assessment_definition` and `assessment_result`

Definitions store instrument/version, stage (baseline, weekly, midline, endline), domain and scoring rules. Results link to participant/enrolment, assessment definition, date, score/value, evidence status and source record.

These tables remain future-compatible even if the first-release weekly workflow is deferred.

### `training_completion`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| training_completion_id | UUID | Yes | Primary key |
| enrolment_id | UUID/FK | Yes | Enrolment |
| completion_status | Reference | Yes | completed, discontinued, transferred, in progress, unknown |
| decision_date | Date | No | Determination date |
| attendance_summary | Decimal/Integer | No | Derived only from verified attendance |
| evidence_status | Reference | Yes | reported, calculated, verified, unknown |
| reason_code | Reference | No | Discontinuation/exception reason |

## 5. Placement and retention

### `employer`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| employer_id | UUID | Yes | Primary key |
| employer_code | Text | Yes | Stable code |
| legal_name | Text | Yes | Canonical name |
| display_name | Text | No | Common name |
| sector_code | Reference | No | Industry/sector |
| headquarters_location_id | UUID/FK | No | Location |
| verification_status | Reference | Yes | unverified, verified, disputed, inactive |
| active_flag | Boolean | Yes | Current operational status |

### `employer_contact`

Core fields: `employer_contact_id`, `employer_id`, `contact_name`, `role_title`, protected phone/email, `valid_from`, `valid_to`, `verification_status`.

### `job_opportunity`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| job_opportunity_id | UUID | Yes | Primary key |
| employer_id | UUID/FK | Yes | Employer |
| role_title | Text | Yes | Vacancy role |
| job_location_id | UUID/FK | No | Location |
| openings | Integer | No | Number of openings |
| compensation_amount | Decimal | No | Amount |
| compensation_period | Reference | No | monthly, daily, annual, other |
| accessibility_notes | Text | No | Workplace/accessibility information |
| opportunity_status | Reference | Yes | draft, open, paused, filled, closed, unknown |
| opened_on / closed_on | Date | No | Availability period |

### `placement_attempt`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| placement_attempt_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Candidate |
| enrolment_id | UUID/FK | No | Related training enrolment |
| job_opportunity_id | UUID/FK | No | Opportunity |
| employer_id | UUID/FK | No | Employer when opportunity record is absent |
| attempt_date | Date | No historically; yes for new data | Referral/interview date |
| attempt_stage | Reference | Yes | referred, interview scheduled, interviewed, selected, offered, rejected, withdrawn, no-show |
| outcome_date | Date | No | Outcome date |
| outcome_reason | Text/Reference | No | Reason |
| evidence_status | Reference | Yes | reported, document verified, employer verified, unknown |
| source_record_id | UUID/FK | No | Provenance |

### `employment`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| employment_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Employee |
| placement_attempt_id | UUID/FK | No | Originating attempt |
| employer_id | UUID/FK | Yes | Employer |
| job_opportunity_id | UUID/FK | No | Opportunity |
| role_title | Text | No | Joined role |
| work_location_id | UUID/FK | No | Work location |
| offered_on | Date | No | Offer date |
| joined_on | Date | Required for verified placement | Joining date |
| compensation_amount / period | Decimal/Reference | No | Starting compensation |
| employment_status | Reference | Yes | offered, joined, active, left, terminated, unknown |
| ended_on | Date | No | End date |
| exit_reason_code | Reference | No | Exit reason |
| verification_status | Reference | Yes | reported, participant verified, employer verified, document verified |

### `follow_up`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| follow_up_id | UUID | Yes | Primary key |
| participant_id | UUID/FK | Yes | Participant |
| employment_id | UUID/FK | No | Employment episode |
| follow_up_type | Reference | Yes | 3-month, 6-month, 12-month, event-based |
| due_on | Date | No | Scheduled date |
| completed_on | Date | No | Actual interaction date |
| contact_outcome | Reference | No | reached, unreachable, rescheduled, declined |
| employment_status_observed | Reference | No | active, left, changed job, unknown |
| satisfaction_or_progress | Text/Reference | No | Approved measure |
| support_needed | Boolean/Unknown | No | Support flag |
| next_action_due_on | Date | No | Follow-up action |
| performed_by | UUID/FK | No | Staff/user |
| source_record_id | UUID/FK | No | Provenance |

## 6. Provenance, quality and audit

### `source_asset`

Core fields: `source_asset_id`, Drive/file identifier, file name, type, version/checksum, authority class (original, translated, consolidated, portal, master, derived), reporting period, owner, discovered date and active flag.

### `source_record`

Core fields: `source_record_id`, `source_asset_id`, sheet/table name, source row key/fingerprint, extraction run, raw-record secure reference, observed date and import status.

### `record_link`

Links one source record to a destination entity type and ID, with link purpose, transformation version and confidence/review state.

### `identity_match_candidate`

| Field | Logical type | Required | Meaning |
| --- | --- | --- | --- |
| identity_match_candidate_id | UUID | Yes | Primary key |
| left_source_record_id | UUID/FK | Yes | First record |
| right_participant_id or source_record_id | UUID/FK | Yes | Candidate match |
| match_score | Decimal | No | Algorithmic score, not a decision |
| matched_signals | Structured data | No | Phone, DOB, legacy ID, etc.; protected |
| conflicting_signals | Structured data | No | Conflicts |
| review_status | Reference | Yes | pending, confirmed, rejected, insufficient evidence |
| reviewed_by / reviewed_at | UUID/Timestamp | No | Human review |
| decision_reason | Text | No | Evidence-based decision |

### `data_quality_issue`

Core fields: issue ID, source/destination reference, issue type, severity, description, detected rule/version, status, owner, resolution, resolved time and audit link.

### `reference_value`

Stores controlled vocabularies and historical-to-canonical mappings without overwriting the original source text.

## 7. Access and ownership placeholders

The logical model reserves `user_profile`, `role`, and `user_role_assignment` with programme/project/location scope. The detailed permission matrix is intentionally not finalised until VoN confirms:

- who can see participant contact and disability data;
- who can create or edit mobilisation, training, attendance and placement records;
- who can verify identity and documents;
- who can export data;
- who can approve corrections, merges and status changes;
- how former staff access is removed.

## 8. Required next modelling work after business approval

1. Confirm the model review decisions.
2. Map every approved Master Sheet/source column to a destination field.
3. Classify every field as observed, transformed or derived.
4. Define canonical status and reference-value lists.
5. Define future-entry required fields separately from historical migration requirements.
6. Create synthetic examples and validation tests.
7. Convert the approved logical model into version-controlled SQL only when Supabase work is authorised.
