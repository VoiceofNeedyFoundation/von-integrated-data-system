# Project status

**Current stage** — Organisational discovery, source audit and proposed data-model review; preparing Checkpoint 1, Checkpoint 2 and Checkpoint 3 evidence.

**Last reviewed** — 18 November 2026, India time.

## Verified infrastructure state

- Repository: VoiceofNeedyFoundation/von-integrated-data-system.
- Visibility: private.
- Connected Voice of Needy GitHub account has admin, maintain, push and pull access.
- `main` contains the initial README at commit `30f7dc1`.
- `feature/backend-discovery` contains discovery and proposed data-model documentation.
- Draft pull request #1 is open and mergeable. It should remain unmerged until discovery and data-model review decisions are recorded.
- `main` is not protected. This is a collaboration risk to address before implementation work begins.
- No Supabase or Vercel resource was inspected or changed, following the current user instruction.

## Evidence reviewed

- The requested Goalkeep/KC2 guidance tab.
- Project kickoff presentation, livelihood operations worksheet, livelihood Theory of Change and TOC feedback.
- Fifteen accessible VoN meeting-note documents from 28 October through 18 November 2026.
- The project folder tree and shared source folder.
- Document Center, Discovery workbook and current Master Sheet.
- Structural inspection of 120 spreadsheet files containing 400 worksheets.
- Content profiling of the current Master Sheet, consolidated trainees, all-trainees workbook, attendance registers and portal export.

See [evidence-register.md](evidence-register.md) for links and review scope.

## Source estate snapshot

- 184 accessible items were inventoried under the supplied project folder, including 11 folders.
- 120 spreadsheet files were structurally profiled: 23 native Google Sheets and 97 Excel workbooks.
- Those workbooks contain 400 worksheets.
- Other folder items include 28 Drive shortcuts, 14 PDFs, 2 native Docs, 2 native Slides, 4 Word files and 3 PowerPoint files.
- Shortcut targets need a separate target-resolution pass; the inventory records them without assuming their contents.

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

The 119 additional training records beyond unique trained people may represent repeat enrolment or multiple historical records. They must not be collapsed automatically.

## Completed in this milestone

- Replaced earlier access-blocked assumptions with verified Drive and GitHub evidence.
- Documented the participant journey, operational roles, source estate and system requirements.
- Created machine-readable file and spreadsheet-structure inventories.
- Recorded aggregate completeness and reconciliation risks without committing participant data.
- Established the current GitHub-only operating boundary.
- Created an evidence-based conceptual/logical data model.
- Mapped all current Master Sheet tabs to proposed canonical entities.
- Created a draft logical data dictionary.
- Created a plain-language senior-manager review pack with decision questions and an approval template.
- Added the model documents to draft pull request #1; no database schema was created.

## Review documents

- [Proposed data model](data-model.md)
- [Draft logical data dictionary](data-dictionary.md)
- [Senior-manager review pack](senior-manager-data-model-review.md)

## Blockers and decisions

1. Analyst and senior-management confirmation is required for the canonical workflow and first-release boundary.
2. Historical migration coverage must be confirmed.
3. Source authority must be agreed among original workbooks, translated copies, consolidated workbooks, portal exports and the evolving Master Sheet.
4. Repeated person links and uncertain attendance matches need a controlled review process.
5. Weekly assessment treatment conflicts across evidence.
6. Placement, joining and retention definitions need approval.
7. The location/training-site hierarchy and canonical vocabularies need approval.
8. Frontend user journeys and role/access requirements are not yet approved.

## Next actions

1. Analyst reviews draft pull request #1 and the senior-manager review pack; do not merge yet.
2. Share the review pack with the responsible VoN/Goalkeep senior managers.
3. Record decisions as approved, approved with changes, not approved, deferred or needing VoN verification.
4. Revise the model and decision log from the review.
5. Merge the documentation only after the corrected discovery/model checkpoint is explicitly approved.
6. Then complete field-level source-to-target mapping, identity review rules and reproducible profiling.
7. Supabase/Vercel work remains out of scope until separately authorised.
