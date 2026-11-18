# Voice of Needy IDS core relational data model

**Status:** Detailed logical/physical proposal for review. No database schema has been created.

This document defines the canonical operational model and its exact relationships. The complete source-to-dashboard architecture is in [data-architecture.md](data-architecture.md), and dashboard facts/dimensions are in [dashboard-data-model.md](dashboard-data-model.md).

## 1. Modelling standard

- PostgreSQL schemas separate `ref`, `core`, `audit`, `raw`, `stg`, `int`, `mart` and `api`.
- Table names are plural nouns. Foreign-key columns use the referenced entity name, such as `participant_id`, `enrolment_id` and `batch_session_id`.
- Internal primary keys are UUIDs.
- Human-readable and historical identifiers are alternate keys, never primary database keys.
- Transaction/event tables record one observed occurrence per row.
- Current status is derived from status events where history matters.
- Closed status sets use check constraints/enums; business-maintained values use reference tables.
- Dates use `date`; real event times use `timestamptz`.
- Money stores numeric amount and currency/period separately.
- Every mutable operational row includes audit timestamps and actor/request metadata.
- Source lineage is stored separately rather than repeated as free text on operational tables.

## 2. Relationship overview

```mermaid
flowchart TD
    P["Participant identity"] --> S["Sourcing and mobilisation"]
    P --> R["Registration and enrolment"]
    R --> T["Batches, sessions and attendance"]
    T --> A["Assessment and completion"]
    P --> J["Placement attempts"]
    J --> E["Employment episodes"]
    E --> F["Follow-up and support"]
    L["Source lineage and quality"] --> P
    L --> S
    L --> R
    L --> T
    L --> J
    L --> E
```

A participant may enter the system as an unresolved source lead. Registration, enrolment, completion, placement and employment are separate facts.

## 3. Participant identity, sourcing and registration ERD

```mermaid
erDiagram
    PARTICIPANTS {
        uuid participant_id PK
        text participant_code UK
        text display_name
        date date_of_birth
        int birth_year
        text gender_code
        text identity_status
        timestamptz created_at
    }
    PARTICIPANT_IDENTIFIERS {
        uuid participant_identifier_id PK
        uuid participant_id FK
        text identifier_type
        text identifier_value
        text issuing_system
        text verification_status
        boolean is_primary
    }
    PARTICIPANT_CONTACTS {
        uuid participant_contact_id PK
        uuid participant_id FK
        text contact_type
        text contact_value
        text relationship_to_participant
        boolean is_primary
        date valid_from
        date valid_to
    }
    PARTICIPANT_PROFILES {
        uuid participant_profile_id PK
        uuid participant_id FK
        uuid location_id FK
        text disability_type_code
        numeric disability_percentage
        text education_level_code
        text employment_status_code
        date effective_from
        date effective_to
    }
    SOURCE_LEADS {
        uuid source_lead_id PK
        uuid participant_id FK
        uuid source_record_id FK
        text source_channel_code
        date sourced_on
        uuid source_location_id FK
        text lead_status
    }
    MOBILISATION_ASSIGNMENTS {
        uuid assignment_id PK
        uuid source_lead_id FK
        uuid assigned_to_user_id FK
        timestamptz assigned_at
        timestamptz due_at
        text assignment_status
    }
    MOBILISATION_INTERACTIONS {
        uuid interaction_id PK
        uuid source_lead_id FK
        uuid participant_id FK
        timestamptz interaction_at
        text interaction_type
        text outcome_code
        timestamptz next_action_due_at
        uuid performed_by_user_id FK
    }
    REGISTRATIONS {
        uuid registration_id PK
        uuid participant_id FK
        uuid programme_id FK
        uuid project_id FK
        date registered_on
        text registration_status
        text consent_status
        text eligibility_status
    }
    DOCUMENT_CHECKS {
        uuid document_check_id PK
        uuid participant_id FK
        uuid registration_id FK
        text document_type
        text check_status
        timestamptz checked_at
    }

    PARTICIPANTS ||--o{ PARTICIPANT_IDENTIFIERS : has
    PARTICIPANTS ||--o{ PARTICIPANT_CONTACTS : has
    PARTICIPANTS ||--o{ PARTICIPANT_PROFILES : has_versions
    PARTICIPANTS o|--o{ SOURCE_LEADS : resolves_to
    SOURCE_LEADS ||--o{ MOBILISATION_ASSIGNMENTS : assigned
    SOURCE_LEADS ||--o{ MOBILISATION_INTERACTIONS : receives
    PARTICIPANTS o|--o{ MOBILISATION_INTERACTIONS : receives
    PARTICIPANTS ||--o{ REGISTRATIONS : submits
    PARTICIPANTS ||--o{ DOCUMENT_CHECKS : has
    REGISTRATIONS o|--o{ DOCUMENT_CHECKS : requires
```

### Relationship rules

1. `source_leads.participant_id` is nullable until identity is safely resolved.
2. A Master Sheet sourcing row is not automatically a mobilisation interaction.
3. A participant can have multiple contacts and profile versions.
4. Registration requires a participant but does not require an enrolment.
5. Document checks record status; full document data is stored only when approved and necessary.
6. Lead and interaction history remain after a person registers.

## 4. Programme, project and location reference ERD

```mermaid
erDiagram
    PROGRAMMES {
        uuid programme_id PK
        text programme_code UK
        text programme_name
        date active_from
        date active_to
    }
    DONORS {
        uuid donor_id PK
        text donor_code UK
        text donor_name
    }
    PROJECTS {
        uuid project_id PK
        uuid programme_id FK
        uuid donor_id FK
        text project_code UK
        text project_name
        date start_date
        date end_date
        text project_status
    }
    LOCATIONS {
        uuid location_id PK
        uuid parent_location_id FK
        text location_type
        text location_code
        text canonical_name
    }
    TRAINING_SITES {
        uuid training_site_id PK
        uuid location_id FK
        text site_code UK
        text site_name
        text site_type
        date active_from
        date active_to
    }

    PROGRAMMES ||--o{ PROJECTS : contains
    DONORS o|--o{ PROJECTS : funds
    LOCATIONS o|--o{ LOCATIONS : contains
    LOCATIONS ||--o{ TRAINING_SITES : hosts
```

A training site may be temporary. Historical centre text maps to a site/location only after review.

## 5. Training delivery ERD

```mermaid
erDiagram
    TRAINING_BATCHES {
        uuid batch_id PK
        text batch_code UK
        uuid programme_id FK
        uuid project_id FK
        uuid training_site_id FK
        date planned_start_date
        date planned_end_date
        date actual_start_date
        date actual_end_date
        int target_size
        text batch_status
    }
    ENROLMENTS {
        uuid enrolment_id PK
        uuid participant_id FK
        uuid registration_id FK
        uuid batch_id FK
        date enrolled_on
        text enrolment_status
        date exit_date
        text exit_reason_code
    }
    SESSION_DEFINITIONS {
        uuid session_definition_id PK
        text session_code UK
        text session_name
        text module_name
        int default_duration_minutes
        text curriculum_version
    }
    BATCH_SESSIONS {
        uuid batch_session_id PK
        uuid batch_id FK
        uuid session_definition_id FK
        text session_title
        timestamptz planned_start_at
        timestamptz actual_start_at
        timestamptz actual_end_at
        uuid trainer_user_id FK
        text delivery_status
    }
    ATTENDANCE {
        uuid attendance_id PK
        uuid enrolment_id FK
        uuid batch_session_id FK
        text attendance_status
        text verification_status
        timestamptz recorded_at
        uuid recorded_by_user_id FK
    }
    ASSESSMENT_INSTRUMENTS {
        uuid assessment_instrument_id PK
        text instrument_code UK
        text instrument_name
        text instrument_version
        text stage_type
        numeric maximum_score
    }
    ASSESSMENT_EVENTS {
        uuid assessment_event_id PK
        uuid assessment_instrument_id FK
        uuid batch_id FK
        uuid batch_session_id FK
        date assessment_date
        text assessment_stage
    }
    ASSESSMENT_RESULTS {
        uuid assessment_result_id PK
        uuid enrolment_id FK
        uuid assessment_event_id FK
        text domain_code
        text measure_code
        numeric numeric_score
        text categorical_result
        text evidence_status
    }
    TRAINING_COMPLETIONS {
        uuid training_completion_id PK
        uuid enrolment_id FK
        text completion_status
        date decision_date
        text reason_code
        text evidence_status
    }

    TRAINING_BATCHES ||--o{ ENROLMENTS : contains
    PARTICIPANTS ||--o{ ENROLMENTS : undertakes
    REGISTRATIONS o|--o{ ENROLMENTS : leads_to
    SESSION_DEFINITIONS o|--o{ BATCH_SESSIONS : defines
    TRAINING_BATCHES ||--o{ BATCH_SESSIONS : schedules
    ENROLMENTS ||--o{ ATTENDANCE : receives
    BATCH_SESSIONS ||--o{ ATTENDANCE : records
    ASSESSMENT_INSTRUMENTS ||--o{ ASSESSMENT_EVENTS : instantiates
    TRAINING_BATCHES ||--o{ ASSESSMENT_EVENTS : hosts
    BATCH_SESSIONS o|--o{ ASSESSMENT_EVENTS : includes
    ENROLMENTS ||--o{ ASSESSMENT_RESULTS : receives
    ASSESSMENT_EVENTS ||--o{ ASSESSMENT_RESULTS : produces
    ENROLMENTS ||--o| TRAINING_COMPLETIONS : concludes
```

### Training cardinalities and constraints

| Table | Declared grain | Uniqueness/validation |
| --- | --- | --- |
| `training_batches` | One operational batch | Unique approved batch code |
| `enrolments` | One participant membership in one batch | Flag duplicate active participant × batch; repeat batches allowed |
| `batch_sessions` | One scheduled/delivered session occurrence | Batch + planned occurrence key or immutable session ID |
| `attendance` | One enrolment × batch session | Unique active pair; enrolment and session must share batch |
| `assessment_events` | One assessment occurrence | Instrument + batch + date/stage |
| `assessment_results` | One enrolment × assessment event × domain/measure | Unique active combination |
| `training_completions` | One current decision per enrolment | Prior decisions retained in audit history |

### Session status

Use one controlled status, not independent booleans:

- `planned`
- `scheduled`
- `completed`
- `partially_completed`
- `postponed`
- `cancelled`
- `unknown_historical`

The Master Sheet planned-vs-completed view is generated from `batch_sessions`; it is not the storage design.

## 6. Placement, employment and retention ERD

```mermaid
erDiagram
    EMPLOYERS {
        uuid employer_id PK
        text employer_code UK
        text legal_name
        text display_name
        text sector_code
        uuid headquarters_location_id FK
        text verification_status
    }
    EMPLOYER_CONTACTS {
        uuid employer_contact_id PK
        uuid employer_id FK
        text contact_name
        text role_title
        text phone
        text email
        date valid_from
        date valid_to
    }
    JOB_OPPORTUNITIES {
        uuid job_opportunity_id PK
        uuid employer_id FK
        uuid job_location_id FK
        text role_title
        int openings
        numeric compensation_amount
        text compensation_period
        text opportunity_status
    }
    PLACEMENT_ATTEMPTS {
        uuid placement_attempt_id PK
        uuid participant_id FK
        uuid enrolment_id FK
        uuid job_opportunity_id FK
        uuid employer_id FK
        date opened_on
        text current_stage
        text current_outcome
    }
    PLACEMENT_STAGE_EVENTS {
        uuid placement_stage_event_id PK
        uuid placement_attempt_id FK
        text stage_code
        date stage_date
        text outcome_code
        text evidence_status
    }
    EMPLOYMENTS {
        uuid employment_id PK
        uuid participant_id FK
        uuid placement_attempt_id FK
        uuid employer_id FK
        uuid job_opportunity_id FK
        text role_title
        date offered_on
        date joined_on
        date ended_on
        numeric compensation_amount
        text employment_status
        text verification_status
    }
    FOLLOWUP_SCHEDULES {
        uuid followup_schedule_id PK
        uuid employment_id FK
        text checkpoint_type
        date due_on
        text schedule_status
    }
    FOLLOWUPS {
        uuid followup_id PK
        uuid followup_schedule_id FK
        uuid employment_id FK
        uuid participant_id FK
        date completed_on
        text contact_outcome
        text employment_status_observed
        boolean support_needed
    }
    SUPPORT_INTERVENTIONS {
        uuid support_intervention_id PK
        uuid employment_id FK
        uuid followup_id FK
        text intervention_type
        date opened_on
        date closed_on
        text intervention_status
    }

    EMPLOYERS ||--o{ EMPLOYER_CONTACTS : has
    EMPLOYERS ||--o{ JOB_OPPORTUNITIES : offers
    PARTICIPANTS ||--o{ PLACEMENT_ATTEMPTS : undertakes
    ENROLMENTS o|--o{ PLACEMENT_ATTEMPTS : informs
    JOB_OPPORTUNITIES o|--o{ PLACEMENT_ATTEMPTS : targets
    EMPLOYERS o|--o{ PLACEMENT_ATTEMPTS : involves
    PLACEMENT_ATTEMPTS ||--o{ PLACEMENT_STAGE_EVENTS : progresses_through
    PLACEMENT_ATTEMPTS o|--o| EMPLOYMENTS : results_in
    PARTICIPANTS ||--o{ EMPLOYMENTS : holds
    EMPLOYERS ||--o{ EMPLOYMENTS : employs
    EMPLOYMENTS ||--o{ FOLLOWUP_SCHEDULES : requires
    FOLLOWUP_SCHEDULES ||--o{ FOLLOWUPS : fulfilled_by
    EMPLOYMENTS ||--o{ FOLLOWUPS : receives
    FOLLOWUPS o|--o{ SUPPORT_INTERVENTIONS : triggers
    EMPLOYMENTS ||--o{ SUPPORT_INTERVENTIONS : receives
```

### Placement design decisions

- Referral, interview, selection, offer and joining are stage events.
- A Boolean set such as `interviewed`, `selected`, `joined` is not used because contradictory states are possible.
- `placement_attempts.current_stage` is a cached/derived operational value; stage-event history is authoritative.
- An employment row is created only when the approved employment evidence rule is met.
- Multiple placement attempts and multiple employment episodes are allowed.
- Retention is evaluated per employment episode, not only per participant.

## 7. Source lineage, identity resolution and audit ERD

```mermaid
erDiagram
    IMPORT_BATCHES {
        uuid import_batch_id PK
        text pipeline_version
        timestamptz started_at
        timestamptz finished_at
        text run_status
    }
    SOURCE_ASSETS {
        uuid source_asset_id PK
        text provider_file_id
        text file_name
        text authority_class
        text checksum
        timestamptz discovered_at
    }
    SOURCE_TABS {
        uuid source_tab_id PK
        uuid source_asset_id FK
        text tab_name
        int header_row
        int source_row_count
    }
    SOURCE_RECORDS {
        uuid source_record_id PK
        uuid source_tab_id FK
        uuid import_batch_id FK
        text source_row_locator
        text row_fingerprint
        jsonb source_payload
    }
    RECORD_LINEAGE {
        uuid record_lineage_id PK
        uuid source_record_id FK
        text target_schema
        text target_table
        uuid target_record_id
        text transformation_version
        text link_status
    }
    IDENTITY_MATCH_CANDIDATES {
        uuid identity_match_candidate_id PK
        uuid source_record_id FK
        uuid participant_id FK
        numeric match_score
        text review_status
        uuid reviewed_by_user_id FK
        timestamptz reviewed_at
    }
    DATA_QUALITY_ISSUES {
        uuid data_quality_issue_id PK
        uuid source_record_id FK
        text target_table
        uuid target_record_id
        text issue_type
        text severity
        text issue_status
        uuid owner_user_id FK
    }
    PARTICIPANT_MERGE_EVENTS {
        uuid participant_merge_event_id PK
        uuid surviving_participant_id FK
        uuid merged_participant_id FK
        uuid approved_by_user_id FK
        timestamptz merged_at
        text decision_reason
    }
    RECORD_CHANGE_EVENTS {
        uuid record_change_event_id PK
        text target_table
        uuid target_record_id
        text operation
        uuid actor_user_id FK
        jsonb before_value
        jsonb after_value
        timestamptz occurred_at
    }

    SOURCE_ASSETS ||--o{ SOURCE_TABS : contains
    SOURCE_TABS ||--o{ SOURCE_RECORDS : contains
    IMPORT_BATCHES ||--o{ SOURCE_RECORDS : loads
    SOURCE_RECORDS ||--o{ RECORD_LINEAGE : creates_or_supports
    SOURCE_RECORDS ||--o{ IDENTITY_MATCH_CANDIDATES : proposes
    PARTICIPANTS ||--o{ IDENTITY_MATCH_CANDIDATES : candidate
    SOURCE_RECORDS o|--o{ DATA_QUALITY_ISSUES : raises
    PARTICIPANTS ||--o{ PARTICIPANT_MERGE_EVENTS : survives
    PARTICIPANTS ||--o{ PARTICIPANT_MERGE_EVENTS : merged_from
```

### Identity decision states

- `pending`
- `confirmed_match`
- `rejected_match`
- `insufficient_evidence`
- `conflict_requires_von`

Algorithmic scores prioritise review; they do not merge people.

## 8. User, role and scope model

```mermaid
erDiagram
    USER_PROFILES {
        uuid user_id PK
        uuid auth_user_id UK
        text display_name
        text staff_status
    }
    ROLES {
        uuid role_id PK
        text role_code UK
        text role_name
    }
    USER_ROLE_ASSIGNMENTS {
        uuid user_role_assignment_id PK
        uuid user_id FK
        uuid role_id FK
        uuid programme_id FK
        uuid project_id FK
        uuid location_id FK
        date valid_from
        date valid_to
    }
    RECORD_OWNERSHIP {
        uuid record_ownership_id PK
        uuid user_id FK
        text entity_type
        uuid entity_id
        text ownership_type
        timestamptz assigned_at
        timestamptz ended_at
    }

    USER_PROFILES ||--o{ USER_ROLE_ASSIGNMENTS : receives
    ROLES ||--o{ USER_ROLE_ASSIGNMENTS : defines
    USER_PROFILES ||--o{ RECORD_OWNERSHIP : owns
```

Final role scope and RLS policies require VoN approval.

## 9. Master Sheet mapping

| Master Sheet tab | Raw/staging object | Canonical core objects | Dashboard/final output |
| --- | --- | --- | --- |
| Participant Registry | `stg.participant_profiles` | participants, identifiers, contacts, profiles | dim participant reporting |
| Sourcing | `stg.source_leads` | source leads, referrals | participant journey, sourcing funnel |
| Mobilization | `stg.mobilisation_interactions` | assignments, interactions | mobilisation interaction fact |
| Training | `stg.registrations`, `stg.enrolments` | registrations, enrolments, completions | training enrolment fact |
| Training Batch | `stg.training_batches` | training batches | batch dimension |
| Session planned vs complete | `stg.batch_sessions` | session definitions, batch sessions | session delivery fact |
| Daily attendance | `stg.attendance_marks` | attendance | attendance fact |
| Weekly assessments | `stg.assessment_results` | instruments, events, results | assessment-result fact |
| Placements | `stg.placement_events` | attempts, stage events, employment | placement pipeline fact |
| Follow-ups | `stg.followup_interactions` | schedules, follow-ups, support | employment checkpoint fact |
| Employers Data | `stg.employers`, opportunities | employers, contacts, opportunities | employer dimension/fact |
| Attendance Verify | identity/DQ staging | identity queue and quality issues | data-quality fact |
| Outreach Contacts Verify | lead/identity staging | source leads and identity queue | data-quality and sourcing facts |
| ID Mapping & Source Trace | raw and audit objects | identifiers and lineage | reconciliation reports |

## 10. Identifier design

| Entity | Internal key | Business/source identifier |
| --- | --- | --- |
| Participant | UUID `participant_id` | Approved `participant_code`; Master/portal/legacy IDs stored separately |
| Source lead | UUID | Source asset/tab/row fingerprint |
| Registration | UUID | Source registration number where available |
| Batch | UUID | Approved `batch_code`; original Pankh batch IDs preserved |
| Enrolment | UUID | Candidate/enrolment/registration ID as alternate identifier |
| Batch session | UUID | Optional generated human session code |
| Employer | UUID | Approved employer code and canonical legal name |
| Employment | UUID | Optional business employment episode code |
| Source record | UUID | File/version + tab + row locator + fingerprint |

IDs never depend on mutable names or spreadsheet row position alone.

## 11. Physical integrity rules

1. `participant_identifiers(issuing_system, identifier_type, identifier_value)` is unique for active identifiers.
2. `attendance(enrolment_id, batch_session_id)` is unique for the active record.
3. The attendance enrolment and session must belong to the same batch.
4. `assessment_results(enrolment_id, assessment_event_id, domain_code, measure_code)` is unique.
5. `followup_schedules(employment_id, checkpoint_type)` is unique unless an approved reschedule version exists.
6. Joining date cannot precede offer/selection evidence without an exception.
7. Employment end date cannot precede joining date.
8. Batch actual end cannot precede actual start.
9. Profile/contact effective periods cannot overlap when marked primary for the same type.
10. Every migrated core record has at least one lineage record.
11. Rejected/unresolved staging rows cannot be loaded as confirmed core events.
12. Corrections and merges create audit events; destructive deletion is not routine.

## 12. Historical versus future-entry requirements

| Area | Historical migration | Future frontend |
| --- | --- | --- |
| Missing dates | Allowed with explicit evidence status | Required for observed operational events |
| Unknown status | Allowed when source cannot establish value | User must select an approved status |
| Source lineage | Mandatory | Request ID and actor audit are mandatory |
| Participant identity | Can remain unresolved | Duplicate check before creation |
| Batch/session | Incomplete historical relationship can enter review | Valid batch/session relationship required |
| Placement | Historical reported value may remain unverified | Stage and evidence rules enforced |
| Follow-up | No fabricated events | Due schedule and completion workflow enforced |

## 13. Review decisions required

Senior managers and operational owners must approve:

- earliest stage for canonical participant creation;
- repeat enrolment and transfer rules;
- registration, completion, placement and retention definitions;
- session catalogue and adaptable-session rules;
- attendance and completion thresholds;
- assessment instruments and first-release scope;
- employer/job/placement stage vocabulary;
- 3-, 6- and 12-month follow-up rules;
- centre/training-site hierarchy;
- participant business ID format;
- data ownership, privacy and access;
- historical migration period and source authority.

After approval, the model will be converted into version-controlled SQL migrations only when backend implementation is authorised.
