# Project understanding and requirements

**Review status** — Evidence-based draft for Checkpoint 1. It is not an approved canonical model.

## Programme context

Voice of Needy Foundation supports persons with disabilities in Karnataka to pursue dignified and sustainable livelihoods. The livelihood pathway combines identification and mobilisation, participant and family counselling, document verification, residential training, assessment and placement readiness, employer engagement, placement support and post-placement follow-up.

The verified programme aspiration is that persons with disabilities obtain work suited to their skills, preferences and access needs; gain greater economic choice; and remain employed with suitable support. Employer willingness, family support, accessible work and accommodation, funding, staff capability and local labour-market conditions are enabling factors, not outcomes that VoN controls alone.

## Verified operating journey

1. **Identification and sourcing** — Potential candidates come from government or UDID records, community and school visits, job fairs, referrals, WhatsApp or social media and other partner lists. Source data can contain the wider eligible population rather than enrolled participants.
2. **Mobilisation** — Mobilisers allocate lists, telephone candidates and families, conduct awareness activity, record responses and follow up. Current records contain repeated and incomplete contacts, and source channel is usually absent.
3. **Consent and registration** — Candidate and family counselling, consent, document collection and verification lead to registration. Name, date-of-birth and identity-document mismatches often surface here. Registration and training enrolment are not the same event.
4. **Batch formation** — Batches are arranged by programme/donor, period and training location. A typical target is about 25–30 participants, but the number and timing of batches are demand-dependent.
5. **Training** — The programme is normally a 45-day residential course. Mixed-disability groups receive employability, retail, digital, communication, financial-literacy and life-skills content using theory and activity-based learning. Session plans can be adapted to batch capability.
6. **Monitoring and assessment** — Daily attendance is largely manual. Evidence refers to baseline, midline, endline and weekly assessments, individual profiles and trainer observations. Current digital availability is uneven.
7. **Placement readiness and matching** — Resumes, documents, interview readiness and candidate preferences are prepared. Employer vacancies, accessibility needs, role suitability, interviews, offers and joining should be tracked separately.
8. **Placement and retention** — Placement is not the end of the journey. VoN supports adjustment, replacement interviews and job changes. Evidence calls for 3-, 6- and 12-month follow-up, but the current master has no follow-up rows.

## Operating roles identified

- Mobilisers and a senior mobiliser manage sourcing, telecalling, counselling and list follow-up.
- Trainers and co-trainers manage the schedule, classroom delivery, attendance, activities, assessment, counselling and participant profiles.
- Placement staff engage employers, arrange drives and support matching and workplace transition.
- Programme coordinators and managers review batches, documentation, performance and reporting.
- Leadership and named programme owners approve priorities and sign-offs.
- Goalkeep's analyst workstream handles discovery, source audit, data modelling and migration preparation.
- A separate Goalkeep workstream will define the frontend journeys and monitoring questions.

Role names and permissions still need formal approval.

## Programme characteristics that affect the data design

- Historical records span 2017–2026 and multiple donor/project structures.
- The programme has operated across four centres or training locations, but evidence says these are not necessarily permanent hubs. Names vary across files.
- Participants may be sourced repeatedly, re-enrolled, transferred, interviewed multiple times, change jobs or receive multiple follow-ups.
- Outreach leads may never register. They still need a traceable disposition without becoming fabricated training records.
- Incomplete historical records are legitimate. Unknown, not collected, not applicable and not yet completed require different treatment.
- Disability-related information is sensitive and should be collected and exposed only when operationally necessary.
- Programme staff need low-burden data entry, clear next-step alerts and centre/batch/district/donor views.

## Data ecosystem

The accessible folder contains original and translated regional lists, manual-register PDFs, consolidated workbooks, attendance registers, donor reports, portal exports, employer lists and project-management artifacts. The current master sheet attempts to connect source, participant, training, placement and review records.

The current master is a working analytical artifact, not proof of a final database schema. It contains useful provenance and identifiers, but it also mixes source-stage rows with historical trainee rows, carries unresolved identity links and has large completeness gaps.

## System outcomes required

- Trace a person across sourcing, mobilisation, consent/registration, enrolment, training, placement and follow-up without treating each spreadsheet row as a new person.
- Preserve multiple source records and multiple programme events for one person.
- Support batch, session, attendance and assessment operations without forcing historical values that were never collected.
- Track employer requirements and multiple candidate placement attempts or jobs.
- Record follow-up episodes and retention evidence over time.
- Preserve record-level source lineage and the disposition of unresolved records.
- Provide role-appropriate access, aggregate monitoring and participant history.
- Accept future frontend submissions using the same canonical rules as migrated records.

## Important contradictions or unresolved interpretation

| Topic | Evidence conflict or gap | Required review |
| --- | --- | --- |
| Historical scope | A 2 November note referred to a narrow recent-year migration, while the current project brief and consolidated work cover 2017–2026. | Confirm the authoritative migration period and whether older years are phased or fully in scope. |
| Weekly assessments | Operations evidence and the TOC refer to assessments; the 18 November decision excludes weekly assessments from the current system phase. | Confirm whether to omit the first-release workflow but preserve future-compatible structures. |
| Participant identity | The master assigns permanent IDs to outreach-only records and also links repeated source/training rows. | Approve identity-state rules and the review threshold before any merge. |
| Centres | Source files use multiple centre labels, while interviews describe flexible accommodation/training locations rather than fixed hubs. | Approve the location hierarchy and canonical vocabulary. |
| Placement completion | Status values include Placed, Placement Completed, offer waiting and dropout variants without a shared definition. | Define placement, joining, verification, retention and exit statuses. |
| Source authority | Original, translated, consolidated, portal and master versions overlap. | Approve the hierarchy and transformation lineage for each field. |

## Checkpoint 1 request

The analyst should approve or correct the operating journey, Phase 1 boundaries, migration period, location interpretation and the distinction between outreach leads, people, enrolments and programme events. Only then should the conceptual model be treated as canonical.
