# Voice of Needy Integrated Data System

This repository is the shared engineering workspace for Voice of Needy Foundation's Integrated Data System.

## Current phase

Discovery and reduced canonical data-model review. No production database, Supabase, Vercel or historical migration changes are authorised.

## Version 3 design

- 12 business tables
- 3 migration/audit tables
- 1 access-control table
- 5 dashboard SQL views
- embedded and dedicated Mermaid diagrams

## Review documents

- [Reduced canonical model](docs/data-model.md)
- [Mermaid ERD and flows](docs/data-model-erd.md)
- [Data architecture](docs/data-architecture.md)
- [Logical data dictionary](docs/data-dictionary.md)
- [Dashboard views](docs/dashboard-data-model.md)
- [Key-question traceability](docs/key-question-to-data-model.md)
- [Senior-management review](docs/senior-manager-data-model-review.md)
- [Project status](docs/project-status.md)

## Safety

- Never commit participant data, credentials or secrets.
- Preserve original sources and record-level lineage.
- Never auto-merge uncertain identities.
- Do not create production schema or migrate data before model approval.
