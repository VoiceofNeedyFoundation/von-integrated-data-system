# Key-question traceability for reduced model

| KQ | Core tables | Reporting view | Main gap/decision |
|---|---|---|---|
| KQ01 | `participants`, `outreach_records`, `enrolments` | Candidate funnel | Eligibility denominator and non-join reasons |
| KQ02 | `projects`, `batches`, `enrolments` | Candidate funnel | Planned intake ownership |
| KQ03 | `batches`, `sessions` | Training delivery | Standard module/status/reason values |
| KQ04 | `employers`, `job_opportunities`, `placements` | Employer opportunities; placement pipeline | Formal vacancy/mapping workflow |
| KQ05 | `enrolments`, `assessments` | Training delivery | Assessment point and eligibility rules |
| KQ06 | `enrolments`, `sessions`, `attendance` | Training delivery | Attendance and 45-day completion rules |
| KQ07 | `enrolments` | Training delivery | Readiness checklist/evidence standard |
| KQ08 | `enrolments`, `placements` | Placement pipeline | Verified joining distinct from offer |
| KQ09 | `assessments` | Training delivery | Comparable domains and rubric versions |
| KQ10 | `participants`, `job_opportunities`, `placements` | Placement pipeline | Suitability criteria and approval |
| KQ11 | `placements`, `followups` | Retention and income | 12/24-month process and unreachable treatment |
| KQ12 | `placements`, `followups` | Retention and income | New comparable income collection required |
| KQ13 | All tables with project/batch/centre fields | All views | Consistent context keys |

The reduced model still covers all 13 questions. Table reduction changes storage structure, not the information required.
