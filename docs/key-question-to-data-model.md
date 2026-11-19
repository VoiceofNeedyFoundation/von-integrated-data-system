# VoN key-question-to-data-model traceability

**Source reviewed:** `Voice of Needy Livelihood Program | Key Questions`, tab `KQs`, 13 high-priority questions.

This register proves that the proposed model is sufficient for the requested dashboard and identifies information that VoN must begin collecting.

| KQ | Decision question | Required core tables | Minimum fields | Availability/gap |
|---|---|---|---|---|
| KQ01 | Who converts from mobilisation to enrolment, and why do others not join? | `mobilisation_cases`, `mobilisation_interactions`, `participants`, `participant_identifiers`, `enrolments` | source, first contact, eligibility/outcome, denial/non-join reason, participant link, enrolment date | Partial; consistent reasons and verified dedupe identifiers required |
| KQ02 | Are centres/batches meeting planned intake? | `projects`, `locations`, `batches`, `enrolments` | planned intake, batch dates, centre, donor/project, enrolment date/status | Partial; planned intake must be consistently recorded |
| KQ03 | Were planned modules delivered, rescheduled or cancelled? | `batches`, `sessions` | module, planned/actual date, status, reason, batch/project/centre | Partial; standard module and status lists required |
| KQ04 | Are employers active, vacancies current and candidates mapped? | `employers`, `vacancies`, `candidate_vacancy_matches` | engagement/verification dates, sector, vacancy status/openings, accessibility, match stage | Partial; vacancy and candidate mapping workflow must be introduced |
| KQ05 | Are baseline, midline and endline assessments complete? | `enrolments`, `assessment_events`, `assessment_results`, `assessment_rubrics` | assessment point/date, eligible enrolment, domain scores, missing reason, rubric version | Partial; assessment-point definitions and denominator rule required |
| KQ06 | Who attends consistently, completes 45 days, drops out or re-enters? | `sessions`, `attendance`, `enrolments` | roster marks, session status, completion/dropout/re-entry dates and reasons | Partial; approve attendance and completion rules |
| KQ07 | Is each candidate placement-ready? | `readiness_reviews`, `enrolments` | profile complete, documents verified, resume updated, interview ready, review date | Partial; one standard readiness checklist required |
| KQ08 | Who was placed and actually joined? | `enrolments`, `candidate_vacancy_matches`, `employments` | referral/offer stages, verified join date, role, employer, completion date | Partial; offer and joining must be separated and evidence rules approved |
| KQ09 | What changed from baseline to midline/endline? | `assessment_events`, `assessment_results`, `assessment_rubrics` | point, domain, score/max, rubric version | Partial; comparable rubrics and domains required |
| KQ10 | Is the job suitable for the candidate? | `participant_support_profiles`, `vacancies`, `candidate_vacancy_matches`, `employments` | skill/preference/location/accessibility checks, suitability result/reason | Partial; standard suitability criteria required |
| KQ11 | Are participants retained at 12 and 24 months? | `employments`, `employment_followups` | checkpoint due/completed date, same/different employer, status, verification | Partial; scheduled checkpoint process required |
| KQ12 | Has income improved at 24 months? | `employments`, `employment_followups` | comparable joining and checkpoint income, period/currency, verification | Not available; new collection required |
| KQ13 | How do centres, batches and donor projects compare? | All facts joined to `projects`, `locations`, `batches` | common delivery-context keys | Partial; all operational records need batch/project/centre links |

## New data collection required

1. Controlled non-enrolment, dropout and cancellation reasons.
2. Planned intake and planned sessions before delivery starts.
3. Active vacancy records and candidate-vacancy mappings.
4. Standard readiness review with evidence status.
5. Verified joining evidence distinct from offer/selection.
6. Scheduled 12- and 24-month follow-ups.
7. Comparable income at joining and follow-up, with currency and periodicity.
8. Consistent donor/project and centre assignment on batches.

## Dashboard readiness rule

A KPI is not production-ready merely because the table exists. Its denominator, reporting window, status treatment, verification rule and historical completeness must all be approved and tested.
