# Backend and frontend collaboration

**Status** — Proposed working agreement for both contributors to review. The frontend developer owns frontend implementation. The backend workstream owns data discovery, migration and backend interfaces. Both coordinate changes that affect shared behaviour.

## Repository workflow

- Use Voice of Needy's `von-integrated-data-system` repository. Use `feature/backend-*` and `feature/frontend-*` branches for independent changes. Keep `main` as the stable integration branch and use pull requests for review.
- Fetch current `main` and check active branches and open pull requests before overlapping work. Reference related changes in both pull requests. Follow existing branch protections and merge only after required checks and reviews.
- Keep shared decisions and approved contracts under `docs/`. Record the evidence or decision behind business rules. Record changes to shared interfaces with compatibility impact, sequencing and verification in the relevant pull request.

## Interface agreement

Start from frontend user journeys, required forms, reporting outputs and permitted roles. Agree together which operations belong in the first integration contract. For each operation, document its version, authentication, authorisation, fields, validation, response and errors. Use synthetic request and response examples.

Keep changes additive where practical. For breaking changes, document the affected consumers, agree on the transition and verify both implementations before merging. Backend data models and role policies go through the project review checkpoints. Until the contract is agreed, the frontend can use synthetic data based on the journeys under discussion.

Supabase is the intended persistence platform. Select the exposed integration interface together after reviewing workflows and access requirements. Any frontend integration should use approved least-privilege access, with privileged credentials held server-side. Track environment and release decisions separately from contract changes.
