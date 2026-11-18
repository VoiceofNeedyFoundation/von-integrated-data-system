# Decision log

## Accepted

### D-001 — Current work is GitHub-only discovery

**Date:** 18 November 2026  
**Decision:** Inspect evidence and maintain documentation in the Voice of Needy GitHub repository. Do not create or modify Supabase or Vercel resources yet.  
**Reason:** The user explicitly limited the current and upcoming work until the Voice of Needy service connections are available.  
**Consequence:** Database and deployment inspection remain unverified and are not blockers for discovery.

### D-002 — Do not put participant data in GitHub

**Date:** 18 November 2026  
**Decision:** Commit aggregate findings and source metadata only. Raw workbooks, exports, participant rows and credentials remain outside Git.  
**Reason:** The sources contain sensitive personal, disability and livelihood information.  
**Consequence:** Reproducible profiling code and de-identified fixtures will be added later; raw-source access remains controlled.

### D-003 — Preserve original sources and derived lineage

**Date:** 18 November 2026  
**Decision:** Treat Drive sources as read-only and distinguish original, translated, consolidated, portal, master and derived views.  
**Reason:** The source estate contains overlapping and sometimes exact-duplicate workbooks.  
**Consequence:** No derived workbook becomes authoritative merely because it is cleaner or newer.

## Proposed for analyst approval

### P-001 — Separate person identity from programme events

Model one person independently from source records, outreach interactions, registrations, enrolments, batch memberships, placements and follow-ups. Repeated records will not be automatically merged or deleted.

### P-002 — Preserve outreach-only leads

A sourced lead may exist without registration, batch or training. A later registration should link to the lead when evidence supports the match while keeping the original source and interaction history.

### P-003 — Treat repeat enrolment as legitimate

The current master has 2,475 enrolment records for 2,356 people. The canonical model should support repeat enrolment and require review only where records conflict or lack corroboration.

### P-004 — Defer weekly-assessment workflow decision

Evidence supports assessment as part of the programme, but the 18 November meeting excluded weekly assessments from the current system phase. Keep this as an explicit scope decision rather than deleting the concept.

### P-005 — Confirm historical migration scope

The master brief requires historical migration and current sources span 2017–2026. An earlier note suggested a narrower recent-year scope. The analyst should confirm whether older years are fully migrated or phased.

### P-006 — Require definitions for placement and retention

Placed, placement completed, offered, joined, retained, left and re-placed require separate definitions and evidence before modelling approval.
