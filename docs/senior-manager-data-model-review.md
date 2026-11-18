# Senior-management review pack: proposed VoN IDS data model

**Purpose:** Obtain business approval for how the Integrated Data System represents VoN's participant journey before any production database schema or historical migration is created.

**Review scope:** Managers are being asked to approve business meanings, ownership and reporting rules. They are not being asked to review SQL, database indexes or technical code.

**Supporting documents:**

- [Project understanding](project-understanding.md)
- [Data profiling findings](data-profiling.md)
- [Proposed data model](data-model.md)
- [Draft data dictionary](data-dictionary.md)
- [Decision log](decisions.md)

## 1. Proposed participant journey

The system will allow a person to move through:

1. Sourcing or identification
2. Mobilisation and counselling
3. Registration and document verification
4. Training enrolment and batch allocation
5. Sessions, attendance and assessments
6. Training completion
7. Placement attempts and employment
8. Post-placement follow-up and support

The stages are connected, but not every person must complete every stage. Historical gaps will remain visible rather than being filled with assumptions.

## 2. What the model changes compared with a spreadsheet

The model does not treat one spreadsheet row as the complete participant.

A single person can have:

- more than one sourcing record;
- several calls or mobilisation interactions;
- more than one programme registration;
- repeat training enrolment;
- many attendance and assessment records;
- several employer referrals/interviews;
- more than one job;
- multiple follow-up interactions.

This separation is necessary because the current Master Sheet contains 4,945 sourcing rows for 4,826 people and 2,475 training records for 2,356 people. Automatically collapsing these differences could delete valid history.

## 3. Recommended decisions

| Decision | Recommendation | Why it matters |
| --- | --- | --- |
| What is a participant? | Keep one canonical person record from the earliest safely identifiable stage; do not imply enrolment | Preserves outreach-only leads without classifying them as trainees |
| Sourced lead without response | Keep the lead and disposition; do not create a fake mobilisation interaction | Current historical interaction evidence is incomplete |
| Repeat training | Allow multiple enrolments for one participant | Current data already has more enrolments than trained people |
| Registration vs enrolment | Treat as separate events | A registered person may not join a batch |
| Session tracking | Store each planned/actual session as a row linked to a batch | Supports changing curricula and avoids adding new database columns |
| Attendance | Record attendance by enrolment and scheduled session/date | Prevents same-name and wrong-batch matches |
| Placement | Track referral, interview, selection, offer and joining separately | Current labels mix different stages |
| Placement reporting | Recommended primary definition: joined employment with an approved evidence state | Selection or offer does not prove employment began |
| Repeat jobs | Allow multiple employment episodes | Participants may change jobs or receive replacement support |
| Follow-up | Track due and completed 3-, 6- and 12-month follow-ups per employment episode | Supports retention rather than placement-only reporting |
| Historical blanks | Preserve as unknown/not collected; never invent data | Protects accuracy |
| Identity matching | Human review for uncertain matches; never merge on name alone | Prevents combining different people |
| Source authority | Approve authority by field and source class, not one workbook for everything | Original, translated, consolidated, portal and master values overlap |
| Assessments | Keep model capability; decide whether weekly entry is first release or later | Evidence and current scope notes conflict |
| Access | Approve role-based, minimum-necessary access | Data includes contact, disability, income and employment information |

## 4. Questions requiring manager approval

### A. Scope and historical period

1. Should historical migration include all available data from 2017–2026?
2. If phased, which years and projects are mandatory for the first migration?
3. Which programmes other than the livelihood/training pathway must be included now?

### B. Participant identity

4. At what point should a sourced name become a canonical participant: when sourced, first contacted, registered or enrolled?
5. Should the existing Master Sheet participant IDs remain the business identifiers?
6. Who is authorised to approve or reject uncertain identity matches?
7. Can one person legitimately attend multiple programmes or batches? The proposed answer is yes.

### C. Mobilisation and registration

8. What outcomes must mobilisers record after every call or visit?
9. How many follow-up attempts are expected before a lead is closed?
10. Which registration documents are mandatory for future participants?
11. Which missing documents should block enrolment, and which may remain pending?

### D. Training

12. Is the 45-day residential model universal or programme-dependent?
13. Can sessions be modified for different batches and disability/access needs?
14. What attendance threshold determines completion?
15. Who can correct attendance after submission?
16. Are baseline, weekly, midline and endline assessments required in the first release?

### E. Placement and employment

17. Which event officially counts as "placed": selected, offer received, joined or verified after joining?
18. What evidence is required for the placement count?
19. How should self-employment, internships and informal employment be represented?
20. Who owns employer verification and placement updates?
21. When is an employment episode considered ended?

### F. Follow-up and retention

22. Are 3-, 6- and 12-month follow-ups mandatory for every joined participant?
23. Is the schedule measured from joining date or placement-record date?
24. What counts as retained at each point?
25. What outcomes and support needs must be recorded?
26. Who is responsible for overdue follow-ups?

### G. Locations, projects and reporting

27. Should "centre" mean a permanent VoN centre, a temporary training site or either?
28. Which geographic levels are required: state, district, taluk/block, city/village?
29. Which donor/project/financial-year fields are mandatory?
30. What are the official batch naming and coding rules?
31. Which management reports and indicators must reconcile to donor reports?

### H. Privacy and access

32. Which roles can view disability, identity-document, address, salary and income information?
33. Which roles can export participant-level data?
34. How long should unsuccessful leads and document evidence be retained?
35. Who approves participant merges, major corrections and deletions/restrictions?

## 5. Source-of-truth proposal for review

No single workbook is proposed as authoritative for every field.

| Source class | Proposed use |
| --- | --- |
| Original source/register | Best evidence of what was originally recorded |
| Verified portal record | Strong source for recent registration fields, subject to date and ownership |
| Translated copy | Interpretation aid linked to the exact original; not independently counted |
| Consolidated workbook | Cross-source staging and analysis; not automatically authoritative |
| Current Master Sheet | Organised business reference, working IDs and review queues |
| Meeting notes/approved decisions | Business definitions and scope, not participant-level facts |
| Derived/temp sheet | Reproducible analysis only; never an independent source |

Managers should approve the principle. Field-by-field authority will then be documented in the source-to-target mapping.

## 6. Review outcome template

For each item, record one of:

- **Approved**
- **Approved with changes**
- **Not approved**
- **Deferred**
- **Needs VoN verification**

| Review area | Outcome | Required change/clarification | Decision owner | Date |
| --- | --- | --- | --- | --- |
| Participant journey |  |  |  |  |
| Identity and IDs |  |  |  |  |
| Historical period |  |  |  |  |
| Mobilisation |  |  |  |  |
| Registration |  |  |  |  |
| Training and sessions |  |  |  |  |
| Attendance |  |  |  |  |
| Assessments |  |  |  |  |
| Placement definition |  |  |  |  |
| Follow-up/retention |  |  |  |  |
| Location hierarchy |  |  |  |  |
| Source authority |  |  |  |  |
| Roles and privacy |  |  |  |  |
| First-release scope |  |  |  |  |

## 7. Approval gate

The draft pull request should remain unmerged while the review is in progress. After review:

1. Record manager decisions and required corrections.
2. Update the model and decision log.
3. Obtain explicit approval of the corrected model.
4. Merge the discovery/model documentation into `main`.
5. Continue to detailed source-to-target mapping and migration preparation.
6. Create Supabase schema work only when that separate work is authorised.

Approval of this document does not authorise a production migration or a Supabase/Vercel change.
