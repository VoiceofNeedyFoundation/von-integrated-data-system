# Project status

**Current stage** — Organisational discovery and source audit; preparing Checkpoint 1 and Checkpoint 2 evidence.

**Last reviewed** — 18 November 2026, India time.

## Verified infrastructure state

- Repository: VoiceofNeedyFoundation/von-integrated-data-system.
- Visibility: private.
- Connected Voice of Needy GitHub account has admin, maintain, push and pull access.
- main contains the initial README at commit 30f7dc1.
- feature/backend-discovery contains discovery documentation.
- GitHub returned no open or closed pull requests during inspection.
- main is not protected. This is a collaboration risk to address before implementation work begins.
- No Supabase or Vercel resource was inspected or changed, following the current user instruction.

## Evidence reviewed

- The requested Goalkeep/KC2 guidance tab.
- Project kickoff presentation, livelihood operations worksheet, livelihood Theory of Change and TOC feedback.
- Fifteen accessible VoN meeting-note documents from 28 October through 18 November 2026.
- The project folder tree and shared source folder.
- Document Center, Discovery workbook and current master sheet.
- Structural inspection of 120 spreadsheet files containing 400 worksheets.
- Content profiling of the current master, consolidated trainees, all-trainees workbook, attendance registers and portal export.

See [evidence-register.md](evidence-register.md) for links and review scope.

## Source estate snapshot

- 184 accessible items were inventoried under the supplied project folder, including 11 folders.
- 120 spreadsheet files were structurally profiled: 23 native Google Sheets and 97 Excel workbooks.
- Those workbooks contain 400 worksheets.
- Other folder items include 28 Drive shortcuts, 14 PDFs, 2 native Docs, 2 native Slides, 4 Word files and 3 PowerPoint files.
- Shortcut targets need a separate target-resolution pass; the inventory records them without assuming their contents.

## Current master snapshot

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

- Replaced the earlier access-blocked assumptions with verified Drive and GitHub evidence.
- Documented the participant journey, operational roles, source estate and system requirements.
- Created a machine-readable file inventory and spreadsheet-structure inventory.
- Recorded aggregate completeness and reconciliation risks without committing participant data.
- Established the current GitHub-only operating boundary.

## Blockers and decisions

1. Analyst confirmation is required for the canonical workflow and Phase 1 boundaries.
2. Source authority must be agreed among original workbooks, translated copies, consolidated workbooks, portal exports and the evolving master sheet.
3. Repeated person links and uncertain attendance matches need a controlled review process.
4. Weekly assessment treatment conflicts across evidence: the programme uses or wants assessment evidence, but the 18 November meeting excluded weekly assessments from the current system phase.
5. Placement and retention sources remain incomplete; the current follow-up tab is empty.
6. Frontend user journeys and role/access requirements are not yet approved.

## Next actions

1. Analyst reviews the project understanding and requirements register for Checkpoint 1.
2. Resolve Drive shortcuts and complete source-authority classification.
3. Run reproducible, source-by-source profiling with row-count reconciliation and no source edits.
4. Create a review queue for identity, attendance and repeat-enrolment cases.
5. Draft the conceptual model only after the workflow scope is confirmed.
6. Open a frontend coordination review covering journeys, terminology and interface versioning.
