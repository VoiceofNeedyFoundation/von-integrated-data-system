# Initial data inventory and profiling

**Status** — Read-only discovery profile on 18 November 2026. No source file was modified. No production migration was performed.

## Method

- Recursively inventoried the supplied project folder and relevant subfolders.
- Structurally opened every accessible spreadsheet file in that folder set.
- Recorded workbook, worksheet, non-empty-row estimate, used-column estimate and a heuristic domain.
- Reviewed the current master and primary consolidation sources in more detail.
- Used aggregate results only in GitHub. Raw participant records remain in authorised Drive sources.

The heuristic domain in spreadsheet-structure.csv is a discovery aid, not an authoritative classification. Many source sheets lack reliable headers and require manual source mapping.

## Coverage

| Measure | Result |
| --- | ---: |
| Inventoried folder items | 184 |
| Folders | 11 |
| Spreadsheet files structurally opened | 120 |
| Worksheets structurally inspected | 400 |
| Google Sheets | 23 |
| Excel workbooks | 97 |
| Drive shortcuts | 28 |
| PDFs | 14 |

The largest derived workbook includes 12,523 non-empty rows in a sheet titled Trainee Data and 8,170 rows in an Age 18-35 view. These appear to be derived/staging views and must not be counted as independent people without lineage review.

## Current master completeness

| Area | Finding |
| --- | --- |
| Participant identity | 4,826 unique participant IDs. Basic contact exists for most records, but email is 75.7% missing; disability type is 51.7% missing and disability percentage is 57.7% missing. The outreach-only population drives much of this gap. |
| Sourcing | 4,945 rows: 2,475 consolidated trainee-source rows and 2,470 sourced leads without training enrolment. Source channel is 99.5% missing, centre/location 66.4% missing and project/donor 49.9% missing. |
| Mobilisation | 4,945 rows are present, but 90.9% lack a call response and 99.4% lack source channel. Many historical trainee rows are explicitly labelled as having no verified mobilisation interaction. |
| Training | 2,475 enrolment rows represent 2,356 people and 103 batches. Registration date is 91.9% missing; start and end dates are each 22.4% missing; status is 30.7% missing; days attended is 95.6% missing. |
| Attendance | Only 108 training rows have any day-level attendance mark, totalling 2,808 non-blank day marks. A separate 185-row verification register remains largely unresolved. |
| Assessment | The weekly assessment grid has no populated week scores in the current master. Kredo fields exist for a subset of historical Pankh records. |
| Placement | 1,399 rows have at least one placement detail. Employer is missing for 48.5%, job role for 50.4%, salary for 53.1%, joining date for 54.6% and offer-letter availability for 97.3%. |
| Follow-up | The current follow-up tab contains zero rows despite the programme requirement for retention tracking. |
| Employers | 131 employer IDs exist; 118 are marked as unverified with VoN and additional records have missing or disputed contact data. |

## Identity and reconciliation findings

- Sourcing has 4,945 records linked to 4,826 people.
- Training has 2,475 enrolment records linked to 2,356 people.
- Candidate/enrolment IDs are unique across all 2,475 training rows.
- The additional records may be repeat enrolments, repeated source observations or unresolved links. They are not safe to delete or merge.
- The attendance verification tab has 185 source rows: 133 need VoN verification, 26 have an identity match but uncertain batch, 12 are high-confidence links and the remainder are cross-source, ambiguous or conflict cases.
- Outreach-only IDs are distinct and traceable, but project, centre and source-channel fields are absent for essentially all 2,470 outreach records.

## Source-quality risks

1. **Original versus derived sources** — Original, translated, consolidated, portal and master versions overlap. Counting all versions would duplicate records.
2. **Stage leakage** — Historical trainee rows appear in sourcing and mobilisation views even when no mobilisation interaction is verified. Database events must represent observed events, not inferred history.
3. **Header and format inconsistency** — Many regional and attendance workbooks use title rows, missing column names, merged cells, Kannada or corrupted text.
4. **Translation lineage** — Translated workbooks are valuable but must point back to the exact original file, sheet and row. Temporary translation files should not become authoritative.
5. **Exact duplicate workbooks** — Two Attendance_All_Batches files are exact duplicates. The available Database Irrapa original and English-named copy are also byte-identical, so the name alone does not prove translation.
6. **Location ambiguity** — Centre names and casing vary, and some batches use UNK placeholders.
7. **Status fragmentation** — Placement, completion and dropout values contain several variants without definitions.
8. **Manual evidence** — Attendance, admission, assessment and follow-up evidence often remains in PDFs, paper registers or separate trackers.
9. **Sensitive data** — Source workbooks contain names, phone numbers, addresses, identity-document fields, disability and income information. Profiling outputs must stay aggregated.

## Migration readiness

The sources are not ready for production migration. Before migration:

- approve the source-authority hierarchy;
- define stage-specific source-to-target mappings;
- preserve observed versus inferred distinctions;
- resolve or queue uncertain identities;
- standardise vocabularies without overwriting original values;
- reconcile source, staged, accepted, rejected and unresolved counts;
- obtain the required model and production-migration approvals.
