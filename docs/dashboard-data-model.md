# Voice of Needy IDS reporting model

The dashboard uses five SQL views. They do not add physical fact/dimension tables in release 1.

| View | Grain | Main questions |
|---|---|---|
| `reporting.vw_candidate_funnel` | One outreach event with participant/enrolment context | Mobilisation conversion, non-joining and intake |
| `reporting.vw_training_delivery` | One enrolment-session with attendance/assessment context | Session delivery, attendance, completion, assessment and readiness |
| `reporting.vw_assessment_progress` | One enrolment-assessment period-domain | Baseline/midline/endline and weekly change |
| `reporting.vw_placement_pipeline` | One placement attempt | Employer opportunity, mapping, suitability, referral, offer and joining |
| `reporting.vw_retention_income` | One placement-follow-up checkpoint | 12/24-month retention and income change |

Every view includes project, donor, financial year, centre and batch context where applicable. Direct participant identifiers are excluded from management views unless a separately authorised operational view requires them.

KPI denominators, timing windows, present-equivalent attendance, completion, readiness, verified joining, unreachable follow-up and comparable-income rules require management approval.
