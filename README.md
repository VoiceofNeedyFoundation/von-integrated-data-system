# Voice of Needy Integrated Data System

This repository contains the discovery, data architecture and professional logical data model for the Voice of Needy Foundation Integrated Data System.

## Current status

The project is at data-model review. No production schema, Supabase configuration, Vercel change or historical migration is authorised.

## Version 4 model

- 13 canonical core tables
- 2 staging/migration tables
- 1 audit table
- 1 security/access table
- 5 read-only reporting views
- editable two-page diagrams.net model with detailed fields and relationships

## Main deliverables

- [Professional data model](docs/data-model.md)
- [Editable draw.io model](docs/diagrams/von-ids-data-model-v4.drawio)
- [SVG preview](docs/diagrams/von-ids-data-model-v4.svg)
- [PNG preview](docs/diagrams/von-ids-data-model-v4.png)
- [Field-level data dictionary](docs/data-dictionary.md)
- [Data architecture](docs/data-architecture.md)
- [Reporting model](docs/dashboard-data-model.md)
- [Key-question traceability](docs/key-question-to-data-model.md)
- [Senior-management review](docs/senior-manager-data-model-review.md)
- [Project status](docs/project-status.md)

## Safety

- Never commit real participant data, credentials or secrets.
- Preserve original sources and record-level lineage.
- Never auto-merge uncertain identities.
- Do not create production schema or migrate data before model approval.
