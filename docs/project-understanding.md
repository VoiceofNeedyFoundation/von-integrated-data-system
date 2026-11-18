# Project understanding and requirements

**Review status** — Preliminary assessment for Checkpoint 1. Based on the master project brief. The Goalkeep guide, VoN operating documents and source sheets are pending access.

Voice of Needy is a nonprofit that works with persons with disabilities. The brief describes sourcing and mobilising potential participants, facilitating registration and enrolment, delivering training, monitoring progress and supporting employability. Goalkeep is supporting the project. Voice of Needy owns the system and will operate it after handover.

## Confirmed requirements from the brief

- Consolidate historical records and support new operational data entry and reporting. Preserve legitimate incomplete histories, including sourcing records that never led to registration.
- Use stable internal identifiers that are independent of source row numbers. Preserve original identifiers and source lineage. Require human review before resolving uncertain participant matches.
- Preserve source files and retain unresolved records for review. Make imports repeatable and reconcile source, staged, loaded, rejected and unresolved records before accepting a migration.
- Protect sensitive participant information through data minimisation, role-based access and secure environments. Keep participant records and credentials out of Git, issues, pull requests and shared logs. Use synthetic data for repository tests.
- Coordinate the backend with the independently developed frontend through reviewed, versioned interface contracts. Supabase is the intended backend platform. Current work takes place in GitHub during discovery.

## Workflows to verify

| Candidate workflow from the brief | Evidence needed from VoN |
| --- | --- |
| Sourcing and mobilisation | How referrals and outreach are recorded, who owns follow-ups, and when a potential participant enters the programme records |
| Registration and enrolment | Registration criteria, whether registration and enrolment are separate events, assigned identifiers, and how repeat or changed enrolments are handled |
| Batches and sessions | Programme and centre structure, roster ownership, transfers, and how scheduled and delivered sessions are distinguished |
| Attendance, progress and completion | Attendance entry and correction, assessment criteria, completion rules, and how these differed historically |
| Employment and follow-up | Definition of placement, evidence and verification, follow-up cadence, and recognition of multiple outcomes |
| Reporting and access | Approved indicators, reporting periods, data owners, operating roles and who may view or change sensitive fields |

These workflows are planning inputs. Each needs supporting process documentation, sheet evidence or analyst validation before it drives a schema or API design.

## Sources and gaps

| Reference | Status | What it can establish |
| --- | --- | --- |
| Master project brief | Reviewed | Project goals, operating constraints, review checkpoints and preliminary workflow scope |
| Goalkeep kickoff guide and SOP | Guide URL supplied. Cloud proxy denied access. SOP availability unconfirmed | Goalkeep framework, scopes of the two kickoff projects and additional review requirements |
| Source-sheet Drive folder and additional Drive folder from the brief | URLs supplied. Cloud proxy denied both. Contents unverified | Workbook and worksheet inventory, historical coverage, available fields and possible relationships |
| VoN process documents, meeting notes and dictionaries | Pending discovery | Workflow owners, definitions and data collection practices |
| Frontend requirements | Pending coordination | Priority forms, read/write scenarios and reporting outputs |

Sheet names, periods, identifiers, record counts and quality findings are pending source review. No conflicts among source documents can be assessed yet. Compare the two Drive folders during discovery and record their coverage and any overlap.

## Checkpoint 1 review

Once the guide and process evidence are available, the analyst reviews the workflow boundaries, the scopes of the two kickoff projects and the Phase 1 priorities. Record the source or analyst decision behind each confirmed rule. Resolve contradictions by identifying the source purpose, date and owner. Carry unresolved decisions forward with their impact and owner.
