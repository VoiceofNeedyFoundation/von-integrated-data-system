# Project status

**Current stage** — Discovery, source audit and professional data-architecture review; preparing Checkpoints 1–3.

**Last reviewed** — 18 November 2026, India time.

## Verified infrastructure state

- Repository: VoiceofNeedyFoundation/von-integrated-data-system.
- Visibility: private.
- Connected Voice of Needy GitHub account has admin, maintain, push and pull access.
- `feature/backend-discovery` contains discovery, architecture and model documentation.
- Draft pull request #1 is open. It should remain unmerged until discovery, architecture and data-model decisions are recorded.
- `main` is not protected. This is a collaboration risk to address before implementation work begins.
- No Supabase or Vercel resource was inspected or changed.

## Evidence reviewed

### VoN evidence

- Goalkeep/KC2 guidance and VoN project documents.
- Project kickoff, livelihood operations worksheet, Theory of Change and feedback.
- Fifteen VoN meeting-note documents from 28 October through 18 November 2026.
- Project folder tree, shared source folder, Document Center and Discovery workbook.
- Current Master Sheet.
- Structural inspection of 120 spreadsheet files containing 400 worksheets.
- Detailed profiling of the Master Sheet, consolidated trainees, original trainees, attendance and portal sources.

### Goalkeep modelling references

The architecture revision also reviewed Goalkeep examples for design standards:

- Project Khel Source Tables and its source mappings.
- Project Khel Staging, Intermediate, Dimension and Final/Fact tables.
- Tamahar Staging–Intermediate–Final table index and cardinality definitions.
- Goalkeep destination-table design training.
- Feedback on another IDS data model covering schema separation, FK naming, stage statuses, assessment grain, provenance and diagram clarity.

The VoN model applies those standards to VoN's actual workflow and source evidence; it does not copy another organisation's tables.

## Source estate snapshot

- 184 accessible items inventoried, including 11 folders.
- 120 spreadsheet files structurally profiled: 23 native Google Sheets and 97 Excel workbooks.
- 400 worksheets inspected structurally.
- Other items include 28 Drive shortcuts, 14 PDFs, 2 native Docs, 2 native Slides, 4 Word files and 3 PowerPoint files.

## Current Master Sheet snapshot

| Area | Verified current count |
| --- | ---: |
| Participant Registry | 4,826 unique participant IDs |
| Sourcing/source-stage records | 4,945 rows |
| Outreach-only sourced leads | 2,470 |
| Training/enrolment records | 2,475 |
| People represented in training records | 2,356 |
| Batches | 103 |
| Employers | 131 |
| Training rows with any day-level attendance mark | 108 |
| Placement rows with any placement detail | 1,399 |
| Follow-up rows | 0 |
| Attendance-register rows awaiting or undergoing identity review | 185 |

The 119 training records beyond unique trained people may represent repeat enrolment or multiple historical records. They must not be collapsed automatically.

## Completed in this milestone

- Documented the participant journey, roles, source estate and system requirements.
- Created machine-readable source and spreadsheet inventories.
- Recorded aggregate completeness and reconciliation risks.
- Established the GitHub-only boundary and data-safety rules.
- Replaced the initial conceptual model with a layered professional architecture.
- Defined source, raw, staging, reference, canonical core, audit, intermediate, mart/final and API layers.
- Defined staging tables, core operational tables, intermediate models and dashboard facts/dimensions with declared grain.
- Defined frontend-facing views/operations without implementing them.
- Added detailed Mermaid architecture and ER diagrams for identity, sourcing, training, placement, retention, lineage and access.
- Mapped every Master Sheet tab through staging, core and dashboard destinations.
- Defined cardinality, reconciliation, idempotency and dashboard-transformation rules.
- Aligned the field dictionary with the layered schema names.
- Expanded the senior-manager review pack to include architecture and dashboard decisions.
- Updated draft pull request #1. No database schema or production pipeline was created.

## Review documents

- [Layered data architecture](data-architecture.md)
- [Core relational model and Mermaid ERDs](data-model.md)
- [Dashboard fact and dimension model](dashboard-data-model.md)
- [Draft logical data dictionary](data-dictionary.md)
- [Senior-manager review pack](senior-manager-data-model-review.md)

## Decisions still required

1. Canonical participant creation point and identity-review authority.
2. Historical migration coverage.
3. Field-level source authority.
4. Repeat enrolment, transfer and repeat employment rules.
5. Weekly assessment and instrument scope.
6. Training completion and attendance thresholds.
7. Placement, joining, employment and retention definitions.
8. Location/training-site hierarchy and canonical vocabularies.
9. Dashboard pages, charts, filters and approved metrics.
10. Frontend journeys and role/access matrix.

## Next actions

1. Analyst reviews draft pull request #1 and the detailed architecture.
2. Share the senior-manager review pack with VoN/Goalkeep decision owners.
3. Record decisions as approved, approved with changes, not approved, deferred or needing VoN verification.
4. Revise the architecture, model, dashboard definitions and decision log.
5. Merge the documentation only after explicit checkpoint approval.
6. Complete field-level source-to-target mappings for the approved first migration scope.
7. Create physical SQL/migrations only when Supabase work is separately authorised.
