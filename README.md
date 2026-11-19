# Voice of Needy Integrated Data System

This repository is the shared engineering workspace for Voice of Needy Foundation's Integrated Data System.

## Current phase

The project is in discovery and canonical data-model review. Work is limited to GitHub documentation and design; no production database, Supabase, Vercel or historical migration changes are authorised yet.

## Current design outputs

- [Data architecture](docs/data-architecture.md)
- [Canonical relational model and Mermaid ERD](docs/data-model.md)
- [Logical data dictionary](docs/data-dictionary.md)
- [Dashboard/mart model](docs/dashboard-data-model.md)
- [Key-question traceability](docs/key-question-to-data-model.md)
- [Senior-management review pack](docs/senior-manager-data-model-review.md)
- [Project status](docs/project-status.md)

The version 2 model is driven by VoN's 13 high-priority key questions and uses 22 canonical business-data tables, plus minimal staff/access and audit structures. It separates operational records, migration/audit evidence and dashboard marts so that frontend entry, historical migration and reporting do not become mixed together.

## Safety rules

- Never commit participant data, credentials or secrets.
- Preserve original source files and record-level lineage.
- Never auto-merge uncertain identities.
- Obtain approval before physical schema creation, destructive changes or production migration.
- Keep the pull request in draft until business and technical reviewers approve the model.
