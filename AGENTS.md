# Voice of Needy IDS agent instructions

## Purpose

Build a trustworthy, maintainable data foundation for Voice of Needy Foundation's livelihood programme and related workflows. Understand the organisation and sources before modelling or migration.

## Current operating boundary

- Work in this GitHub repository only unless the user explicitly expands the scope.
- Do not create or modify Supabase or Vercel resources in the current phase.
- Do not migrate production data or make irreversible infrastructure changes.
- Continue from the current project status and decision log; do not restart discovery without evidence that it is stale.

## Data safety

- Never commit raw participant-level data, personally identifiable information, source exports, credentials or secrets.
- Use aggregate findings and metadata in repository documentation.
- Preserve source lineage. Do not modify original Drive sources.
- Do not merge uncertain identities. Treat same-name matches as unresolved without corroborating evidence.
- Separate people from source records, outreach interactions, enrolments, batches, attendance, placements and follow-ups.

## Workflow

1. Inspect the latest main branch, active branches and open pull requests.
2. Read docs/project-status.md, docs/decisions.md and the relevant evidence.
3. Work on a feature branch. Keep main stable and use pull requests.
4. Update documentation and project status with every meaningful milestone.
5. Run reproducible checks with synthetic or de-identified data.
6. Request analyst review at the defined checkpoints before canonical modelling, production schema work or migration.

## Known open questions

- Historical migration coverage and the authoritative source hierarchy.
- Review of repeated participant links and repeat enrolments.
- Final treatment of weekly assessments in the first release.
- Canonical centre, donor/project, batch and status vocabularies.
- Placement and 3-, 6- and 12-month follow-up ownership and evidence.
- Frontend journeys, role matrix and integration contract.
