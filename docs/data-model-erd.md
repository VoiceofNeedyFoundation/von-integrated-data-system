# Voice of Needy IDS Mermaid diagrams

**Version:** 3 reduced-table model

## Business model

```mermaid
erDiagram
    PARTICIPANTS ||--o{ OUTREACH_RECORDS : has
    PROJECTS ||--o{ OUTREACH_RECORDS : supports
    PROJECTS ||--o{ BATCHES : funds
    PARTICIPANTS ||--o{ ENROLMENTS : undertakes
    BATCHES ||--o{ ENROLMENTS : contains
    BATCHES ||--o{ SESSIONS : schedules
    ENROLMENTS ||--o{ ATTENDANCE : receives
    SESSIONS ||--o{ ATTENDANCE : records
    ENROLMENTS ||--o{ ASSESSMENTS : has
    EMPLOYERS ||--o{ JOB_OPPORTUNITIES : offers
    ENROLMENTS ||--o{ PLACEMENTS : attempts
    JOB_OPPORTUNITIES ||--o{ PLACEMENTS : receives
    PLACEMENTS ||--o{ FOLLOWUPS : monitored_by
```

## Source-to-dashboard flow

```mermaid
flowchart TD
    A["Master Sheet and historical sources"] --> B["Raw and staging evidence"]
    B --> C["Identity and quality review"]
    C --> D["12-table canonical model"]
    D --> E["Five reporting views"]
    E --> F["VoN dashboard"]
```

## Participant journey

```mermaid
flowchart TD
    A["Sourced or mobilised"] --> B["Enrolled in batch"]
    B --> C["Sessions and attendance"]
    C --> D["Assessments and readiness"]
    D --> E["Matched to opportunity"]
    E --> F["Offer and verified joining"]
    F --> G["Retention and income follow-up"]
```

GitHub renders these fenced Mermaid diagrams directly. The same relationships can later be exported to diagrams.net after business approval; maintaining an editable draw.io file before approval would create two competing design sources.
