#!/usr/bin/env python3
"""Generate the editable draw.io and Graphviz previews for the VoN IDS model."""

from __future__ import annotations

import html
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


OUT = Path("docs/diagrams")
OUT.mkdir(parents=True, exist_ok=True)


ENTITIES = [
    {
        "id": "participants",
        "title": "1. core.participants",
        "purpose": "One canonical person; current identity, profile, contact and support details.",
        "color": "#dae8fc",
        "stroke": "#6c8ebf",
        "fields": [
            ("PK", "participant_id", "uuid NOT NULL"),
            ("UQ", "participant_code", "text NOT NULL"),
            ("", "first_name", "text NOT NULL"),
            ("", "middle_name", "text NULL"),
            ("", "last_name", "text NULL"),
            ("", "gender_code", "text NULL"),
            ("", "date_of_birth", "date NULL"),
            ("", "primary_mobile", "text NULL, restricted"),
            ("", "primary_email", "text NULL, restricted"),
            ("", "mobile_verified", "boolean NOT NULL"),
            ("", "email_verified", "boolean NOT NULL"),
            ("", "disability_type", "text NULL, restricted"),
            ("", "disability_percent", "numeric(5,2) NULL"),
            ("", "education_level", "text NULL"),
            ("", "address", "text NULL, restricted"),
            ("", "district", "text NULL"),
            ("", "state", "text NULL"),
            ("", "pin_code", "text NULL"),
            ("", "family_income", "numeric NULL, restricted"),
            ("", "parent_guardian", "jsonb NULL, validated"),
            ("", "support_preferences", "jsonb NULL, validated"),
            ("", "external_file_number", "text NULL"),
            ("", "identity_status", "text NOT NULL, check"),
            ("", "record_status", "text NOT NULL, check"),
        ],
    },
    {
        "id": "participant_identifiers",
        "title": "2. core.participant_identifiers",
        "purpose": "Multiple VoN, legacy, candidate, roster and external identifiers per participant.",
        "color": "#dae8fc",
        "stroke": "#6c8ebf",
        "fields": [
            ("PK", "participant_identifier_id", "uuid NOT NULL"),
            ("FK", "participant_id", "uuid NOT NULL"),
            ("", "identifier_type", "text NOT NULL, check"),
            ("", "identifier_value", "text NOT NULL, restricted"),
            ("", "normalised_hash", "text NULL"),
            ("", "is_primary", "boolean NOT NULL"),
            ("", "is_verified", "boolean NOT NULL"),
            ("", "verified_at", "timestamptz NULL"),
            ("", "source_record_id", "uuid NULL"),
            ("UQ", "type + value/hash", "partial uniqueness"),
        ],
    },
    {
        "id": "projects",
        "title": "3. core.projects",
        "purpose": "Programme/donor project context used across mobilisation, delivery and outcomes.",
        "color": "#d5e8d4",
        "stroke": "#82b366",
        "fields": [
            ("PK", "project_id", "uuid NOT NULL"),
            ("UQ", "project_code", "text NOT NULL"),
            ("", "project_name", "text NOT NULL"),
            ("", "donor_name", "text NULL"),
            ("", "financial_year", "text NULL"),
            ("", "start_date", "date NULL"),
            ("", "end_date", "date NULL"),
            ("", "target_participants", "integer NULL >= 0"),
            ("", "centre_codes", "text[] NULL"),
            ("", "is_active", "boolean NOT NULL"),
        ],
    },
    {
        "id": "outreach_events",
        "title": "4. core.outreach_events",
        "purpose": "One sourcing, mobilisation, call or eligibility event; may precede identity resolution.",
        "color": "#dae8fc",
        "stroke": "#6c8ebf",
        "fields": [
            ("PK", "outreach_event_id", "uuid NOT NULL"),
            ("FK", "participant_id", "uuid NULL"),
            ("FK", "project_id", "uuid NULL"),
            ("", "event_type", "text NOT NULL, check"),
            ("", "event_date", "date NULL"),
            ("", "source_channel", "text NULL"),
            ("", "source_name", "text NULL"),
            ("", "call_response", "text NULL"),
            ("", "eligibility_status", "text NULL, check"),
            ("", "outcome_status", "text NULL, check"),
            ("", "outcome_reason", "text NULL"),
            ("", "next_followup_date", "date NULL"),
            ("", "owner_user_id", "uuid NULL"),
            ("", "record_classification", "text NULL"),
            ("", "source_attributes", "jsonb NULL, validated"),
        ],
    },
    {
        "id": "batches",
        "title": "5. core.batches",
        "purpose": "One training cohort with planned and actual delivery context.",
        "color": "#fff2cc",
        "stroke": "#d6b656",
        "fields": [
            ("PK", "batch_id", "uuid NOT NULL"),
            ("UQ", "batch_code", "text NOT NULL"),
            ("FK", "project_id", "uuid NOT NULL"),
            ("", "original_batch_ids", "jsonb NULL, validated"),
            ("", "financial_year", "text NULL"),
            ("", "centre_code", "text NULL"),
            ("", "centre_name", "text NULL"),
            ("", "planned_intake", "integer NULL >= 0"),
            ("", "planned_start_date", "date NULL"),
            ("", "planned_end_date", "date NULL"),
            ("", "actual_start_date", "date NULL"),
            ("", "actual_end_date", "date NULL"),
            ("", "planned_session_count", "integer NULL >= 0"),
            ("", "trainer_details", "jsonb NULL, validated"),
            ("", "planned_topics", "jsonb NULL, validated"),
            ("", "batch_status", "text NOT NULL, check"),
            ("", "plan_evidence_url", "text NULL"),
            ("", "completion_evidence_url", "text NULL"),
        ],
    },
    {
        "id": "enrolments",
        "title": "6. core.enrolments",
        "purpose": "One participant attempt in one batch; training, completion, dropout and readiness.",
        "color": "#fff2cc",
        "stroke": "#d6b656",
        "fields": [
            ("PK", "enrolment_id", "uuid NOT NULL"),
            ("FK", "participant_id", "uuid NOT NULL"),
            ("FK", "batch_id", "uuid NOT NULL"),
            ("UQ", "participant + batch + attempt", "unique"),
            ("", "candidate_enrolment_code", "text NULL"),
            ("", "attempt_number", "integer NOT NULL"),
            ("", "registration_date", "date NULL"),
            ("", "training_start_date", "date NULL"),
            ("", "training_end_date", "date NULL"),
            ("", "status", "text NOT NULL, check"),
            ("", "completion_status", "text NULL, check"),
            ("", "completion_date", "date NULL"),
            ("", "dropout_stage", "text NULL"),
            ("", "dropout_reason_category", "text NULL"),
            ("", "dropout_reason_detail", "text NULL"),
            ("", "reentry_date", "date NULL"),
            ("", "profile_complete", "boolean NULL"),
            ("", "documents_verified", "boolean NULL"),
            ("", "resume_current", "boolean NULL"),
            ("", "interview_ready", "boolean NULL"),
            ("", "readiness_review_date", "date NULL"),
            ("", "readiness_notes", "text NULL"),
        ],
    },
    {
        "id": "sessions",
        "title": "7. core.sessions",
        "purpose": "One planned/delivered session for one batch; normalises Session 01–45 columns.",
        "color": "#fff2cc",
        "stroke": "#d6b656",
        "fields": [
            ("PK", "session_id", "uuid NOT NULL"),
            ("FK", "batch_id", "uuid NOT NULL"),
            ("UQ", "batch + session_number", "unique"),
            ("", "session_number", "integer NOT NULL > 0"),
            ("", "module_code", "text NULL"),
            ("", "topic", "text NULL"),
            ("", "planned_date", "date NULL"),
            ("", "actual_date", "date NULL"),
            ("", "delivery_status", "text NOT NULL, check"),
            ("", "status_reason", "text NULL"),
            ("", "facilitator_details", "jsonb NULL, validated"),
            ("", "evidence_url", "text NULL"),
            ("", "session_notes", "text NULL"),
        ],
    },
    {
        "id": "attendance",
        "title": "8. core.attendance",
        "purpose": "One enrolment-session result; normalises Day 01–46 marks and source rosters.",
        "color": "#fff2cc",
        "stroke": "#d6b656",
        "fields": [
            ("PK", "attendance_id", "uuid NOT NULL"),
            ("FK", "enrolment_id", "uuid NOT NULL"),
            ("FK", "session_id", "uuid NOT NULL"),
            ("UQ", "enrolment + session", "unique"),
            ("", "attendance_date", "date NULL"),
            ("", "attendance_status", "text NOT NULL, check"),
            ("", "reason", "text NULL"),
            ("", "source_register_id", "text NULL"),
            ("", "source_mark", "text NULL"),
            ("", "verified", "boolean NOT NULL"),
            ("", "verification_notes", "text NULL"),
        ],
    },
    {
        "id": "assessments",
        "title": "9. core.assessments",
        "purpose": "One enrolment, assessment point/week and domain result.",
        "color": "#fff2cc",
        "stroke": "#d6b656",
        "fields": [
            ("PK", "assessment_id", "uuid NOT NULL"),
            ("FK", "enrolment_id", "uuid NOT NULL"),
            ("UQ", "enrolment + type + period + domain + attempt", "unique"),
            ("", "assessment_type", "text NOT NULL, check"),
            ("", "period_code", "text NULL"),
            ("", "domain_code", "text NULL"),
            ("", "domain_label", "text NULL"),
            ("", "attempt_number", "integer NOT NULL"),
            ("", "assessment_date", "date NULL"),
            ("", "rubric_version", "text NULL"),
            ("", "score_value", "numeric NULL"),
            ("", "maximum_score", "numeric NULL > 0"),
            ("", "score_percent", "numeric generated/derived"),
            ("", "completion_status", "text NOT NULL, check"),
            ("", "missing_reason", "text NULL"),
            ("", "source_result", "jsonb NULL, validated"),
        ],
    },
    {
        "id": "employers",
        "title": "10. core.employers",
        "purpose": "One employer organisation and its current engagement profile.",
        "color": "#f8cecc",
        "stroke": "#b85450",
        "fields": [
            ("PK", "employer_id", "uuid NOT NULL"),
            ("UQ", "employer_code", "text NOT NULL"),
            ("", "employer_name", "text NOT NULL"),
            ("", "location_address", "text NULL"),
            ("", "contact_name", "text NULL, restricted"),
            ("", "contact_designation", "text NULL"),
            ("", "contact_number", "text NULL, restricted"),
            ("", "contact_email", "text NULL, restricted"),
            ("", "sector", "text NULL"),
            ("", "disability_types_considered", "text[] NULL"),
            ("", "accessibility_notes", "text NULL"),
            ("", "existing_staff_with_disability", "integer NULL >= 0"),
            ("", "required_staff_with_disability", "integer NULL >= 0"),
            ("", "last_contact_date", "date NULL"),
            ("", "verification_status", "text NOT NULL, check"),
        ],
    },
    {
        "id": "job_opportunities",
        "title": "11. core.job_opportunities",
        "purpose": "One role/vacancy at one employer; supports open-vacancy and matching questions.",
        "color": "#f8cecc",
        "stroke": "#b85450",
        "fields": [
            ("PK", "job_opportunity_id", "uuid NOT NULL"),
            ("FK", "employer_id", "uuid NOT NULL"),
            ("FK", "project_id", "uuid NULL"),
            ("", "role_title", "text NOT NULL"),
            ("", "work_type", "text NULL"),
            ("", "location", "text NULL"),
            ("", "education_required", "text NULL"),
            ("", "skills_required", "jsonb NULL, validated"),
            ("", "accessibility_requirements", "text NULL"),
            ("", "salary_amount", "numeric NULL >= 0"),
            ("", "salary_period", "text NULL, check"),
            ("", "vacancies_count", "integer NULL >= 0"),
            ("", "open_date", "date NULL"),
            ("", "close_date", "date NULL"),
            ("", "status", "text NOT NULL, check"),
        ],
    },
    {
        "id": "placement_attempts",
        "title": "12. core.placement_attempts",
        "purpose": "One candidate-opportunity attempt from mapping through verified joining/exit.",
        "color": "#f8cecc",
        "stroke": "#b85450",
        "fields": [
            ("PK", "placement_attempt_id", "uuid NOT NULL"),
            ("FK", "enrolment_id", "uuid NOT NULL"),
            ("FK", "job_opportunity_id", "uuid NULL"),
            ("UQ", "enrolment + opportunity + attempt", "unique when linked"),
            ("", "attempt_number", "integer NOT NULL"),
            ("", "skills_fit", "boolean NULL"),
            ("", "preference_fit", "boolean NULL"),
            ("", "location_fit", "boolean NULL"),
            ("", "accessibility_fit", "boolean NULL"),
            ("", "suitability_status", "text NULL, check"),
            ("", "suitability_reason", "text NULL"),
            ("", "pipeline_stage", "text NOT NULL, check"),
            ("", "referral_date", "date NULL"),
            ("", "interview_date", "date NULL"),
            ("", "offer_date", "date NULL"),
            ("", "joining_date", "date NULL"),
            ("", "actual_employer_name", "text NULL"),
            ("", "actual_job_role", "text NULL"),
            ("", "joining_salary", "numeric NULL >= 0"),
            ("", "salary_period", "text NULL, check"),
            ("", "offer_letter_available", "boolean NOT NULL"),
            ("", "joining_verified", "boolean NOT NULL"),
            ("", "placement_status", "text NOT NULL, check"),
            ("", "rejection_or_exit_reason", "text NULL"),
            ("", "status_date", "date NULL"),
            ("", "evidence_url", "text NULL"),
        ],
    },
    {
        "id": "followups",
        "title": "13. core.followups",
        "purpose": "One employment follow-up/checkpoint attempt after placement.",
        "color": "#f8cecc",
        "stroke": "#b85450",
        "fields": [
            ("PK", "followup_id", "uuid NOT NULL"),
            ("FK", "placement_attempt_id", "uuid NOT NULL"),
            ("UQ", "placement + checkpoint + attempt", "unique"),
            ("", "checkpoint_month", "integer NULL"),
            ("", "attempt_number", "integer NOT NULL"),
            ("", "due_date", "date NULL"),
            ("", "followup_date", "date NULL"),
            ("", "employment_status", "text NULL, check"),
            ("", "current_workplace", "text NULL"),
            ("", "previous_workplace", "text NULL"),
            ("", "current_job_role", "text NULL"),
            ("", "monthly_salary", "numeric NULL >= 0"),
            ("", "salary_period", "text NULL, check"),
            ("", "reason_for_leaving", "text NULL"),
            ("", "verification_status", "text NOT NULL, check"),
            ("", "evidence_url", "text NULL"),
            ("", "notes", "text NULL"),
        ],
    },
    {
        "id": "import_runs",
        "title": "14. staging.import_runs",
        "purpose": "One repeatable import execution with reconciliation counts.",
        "color": "#e1d5e7",
        "stroke": "#9673a6",
        "fields": [
            ("PK", "import_run_id", "uuid NOT NULL"),
            ("", "source_asset_name", "text NOT NULL"),
            ("", "source_asset_id", "text NULL"),
            ("", "source_version", "text NULL"),
            ("", "pipeline_version", "text NOT NULL"),
            ("", "started_at", "timestamptz NOT NULL"),
            ("", "completed_at", "timestamptz NULL"),
            ("", "status", "text NOT NULL, check"),
            ("", "source_count", "integer NOT NULL >= 0"),
            ("", "staged_count", "integer NOT NULL >= 0"),
            ("", "loaded_count", "integer NOT NULL >= 0"),
            ("", "rejected_count", "integer NOT NULL >= 0"),
            ("", "unresolved_count", "integer NOT NULL >= 0"),
            ("", "error_summary", "text NULL"),
        ],
    },
    {
        "id": "source_records",
        "title": "15. staging.source_records",
        "purpose": "One immutable source row plus validation, identity decision and target lineage.",
        "color": "#e1d5e7",
        "stroke": "#9673a6",
        "fields": [
            ("PK", "source_record_id", "uuid NOT NULL"),
            ("FK", "import_run_id", "uuid NOT NULL"),
            ("", "source_file_id", "text NULL"),
            ("", "source_file_name", "text NOT NULL"),
            ("", "source_sheet_name", "text NULL"),
            ("", "source_row_number", "integer NULL"),
            ("", "source_record_key", "text NOT NULL"),
            ("", "source_checksum", "text NOT NULL"),
            ("", "raw_payload", "jsonb NOT NULL, restricted"),
            ("", "standardised_payload", "jsonb NULL"),
            ("", "validation_status", "text NOT NULL, check"),
            ("", "validation_issues", "jsonb NULL"),
            ("", "identity_match_status", "text NULL, check"),
            ("", "match_confidence", "numeric NULL"),
            ("", "review_decision", "text NULL, check"),
            ("", "reviewed_by", "uuid NULL"),
            ("", "reviewed_at", "timestamptz NULL"),
            ("", "target_table", "text NULL"),
            ("", "target_record_id", "uuid NULL"),
            ("", "disposition", "text NOT NULL, check"),
        ],
    },
    {
        "id": "change_log",
        "title": "16. audit.change_log",
        "purpose": "Material change history for protected operational records.",
        "color": "#e1d5e7",
        "stroke": "#9673a6",
        "fields": [
            ("PK", "change_log_id", "uuid NOT NULL"),
            ("", "target_table", "text NOT NULL"),
            ("", "target_record_id", "uuid NOT NULL"),
            ("", "operation", "text NOT NULL, check"),
            ("", "changed_fields", "text[] NULL"),
            ("", "before_values", "jsonb NULL, restricted"),
            ("", "after_values", "jsonb NULL, restricted"),
            ("", "actor_user_id", "uuid NULL"),
            ("", "changed_at", "timestamptz NOT NULL"),
            ("", "request_id", "text NULL"),
        ],
    },
    {
        "id": "user_access",
        "title": "17. security.user_access",
        "purpose": "Role and optional project/centre access scope for an authenticated user.",
        "color": "#e1d5e7",
        "stroke": "#9673a6",
        "fields": [
            ("PK", "user_access_id", "uuid NOT NULL"),
            ("FK", "auth_user_id", "uuid NOT NULL -> auth.users"),
            ("", "role_code", "text NOT NULL, check"),
            ("FK", "project_id", "uuid NULL"),
            ("", "centre_code", "text NULL"),
            ("", "valid_from", "date NULL"),
            ("", "valid_to", "date NULL"),
            ("", "is_active", "boolean NOT NULL"),
            ("", "granted_by", "uuid NULL"),
            ("", "granted_at", "timestamptz NOT NULL"),
        ],
    },
]


RELATIONSHIPS = [
    ("participants", "participant_identifiers", "1 to many"),
    ("participants", "outreach_events", "0/1 to many"),
    ("projects", "outreach_events", "0/1 to many"),
    ("projects", "batches", "1 to many"),
    ("participants", "enrolments", "1 to many"),
    ("batches", "enrolments", "1 to many"),
    ("batches", "sessions", "1 to many"),
    ("enrolments", "attendance", "1 to many"),
    ("sessions", "attendance", "1 to many"),
    ("enrolments", "assessments", "1 to many"),
    ("employers", "job_opportunities", "1 to many"),
    ("projects", "job_opportunities", "0/1 to many"),
    ("enrolments", "placement_attempts", "1 to many"),
    ("job_opportunities", "placement_attempts", "0/1 to many"),
    ("placement_attempts", "followups", "1 to many"),
    ("import_runs", "source_records", "1 to many"),
    ("projects", "user_access", "0/1 to many"),
]


SOURCE_GROUPS = [
    ("Participant and outreach", ["Participant Registry", "Sourcing", "Mobilization", "Outreach Contacts - Verify"]),
    ("Training delivery", ["Training", "Training Batch", "Training - session planned vs complete", "Training Plans - Source References"]),
    ("Attendance and assessment", ["Training - Daily attendance", "Training - Weekly assessments", "2026 Attendance - Source Roster", "2026 Attendance - Verify"]),
    ("Employment outcomes", ["Employers Data", "Placements", "Follow-ups", "Training and Placement Dropouts"]),
    ("Identity and exceptions", ["ID Mapping & Source Trace", "2026-27 Extra Trainees - Verify"]),
]


DASHBOARD_VIEWS = [
    "reporting.vw_candidate_funnel",
    "reporting.vw_training_delivery",
    "reporting.vw_assessment_progress",
    "reporting.vw_placement_pipeline",
    "reporting.vw_retention_income",
]


def table_html(entity: dict) -> str:
    lines = [
        f"<div style='font-size:15px'><b>{html.escape(entity['title'])}</b></div>",
        f"<div style='font-size:10px;color:#444'><i>{html.escape(entity['purpose'])}</i></div>",
        "<hr>",
    ]
    for marker, name, typ in entity["fields"]:
        prefix = f"<b>{html.escape(marker)}</b> " if marker else ""
        lines.append(f"<div>{prefix}<b>{html.escape(name)}</b> : {html.escape(typ)}</div>")
    lines.append("<hr><div style='font-size:9px;color:#666'>Common audit: created_at, updated_at, created_by, updated_by where applicable.</div>")
    return "".join(lines)


def new_graph_model(width: int, height: int) -> tuple[ET.Element, ET.Element]:
    model = ET.Element("mxGraphModel", {
        "dx": "1422", "dy": "794", "grid": "1", "gridSize": "10",
        "guides": "1", "tooltips": "1", "connect": "1", "arrows": "1",
        "fold": "1", "page": "1", "pageScale": "1", "pageWidth": str(width),
        "pageHeight": str(height), "math": "0", "shadow": "0",
    })
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", {"id": "0"})
    ET.SubElement(root, "mxCell", {"id": "1", "parent": "0"})
    return model, root


def add_vertex(root: ET.Element, cell_id: str, value: str, x: float, y: float, w: float, h: float, style: str) -> None:
    cell = ET.SubElement(root, "mxCell", {
        "id": cell_id, "value": value, "style": style, "vertex": "1", "parent": "1"
    })
    ET.SubElement(cell, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})


def add_edge(root: ET.Element, edge_id: str, source: str, target: str, label: str = "") -> None:
    cell = ET.SubElement(root, "mxCell", {
        "id": edge_id, "value": label,
        "style": "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=ERmany;endFill=0;startArrow=ERone;startFill=0;strokeWidth=1.5;",
        "edge": "1", "parent": "1", "source": source, "target": target,
    })
    ET.SubElement(cell, "mxGeometry", {"relative": "1", "as": "geometry"})


def add_overview(mxfile: ET.Element) -> None:
    diagram = ET.SubElement(mxfile, "diagram", {"id": "von-overview-v4", "name": "1. Architecture and lineage"})
    model, root = new_graph_model(3200, 1800)
    title_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1f4e78;strokeColor=#1f4e78;fontColor=#ffffff;fontSize=22;fontStyle=1;align=left;spacingLeft=16;"
    add_vertex(root, "overview_title", "Voice of Needy IDS — architecture, source lineage and dashboard flow", 40, 30, 3050, 60, title_style)

    group_style = "rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=12;fillColor=#f5f5f5;strokeColor=#666666;fontSize=12;"
    x = 60
    source_ids = []
    for idx, (name, tabs) in enumerate(SOURCE_GROUPS, 1):
        value = f"<b>{html.escape(name)}</b><hr>" + "<br>".join(html.escape(t) for t in tabs)
        sid = f"source_group_{idx}"
        source_ids.append(sid)
        add_vertex(root, sid, value, x, 150 + (idx - 1) * 250, 520, 190, group_style)

    layer_style = "rounded=1;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=14;fontSize=13;"
    add_vertex(root, "staging_layer", "<b>STAGING + MIGRATION CONTROL</b><hr><b>import_runs</b><br><b>source_records</b><br><br>Immutable row evidence; typed/standardised payload; validation; identity review; target lineage; rerun and reconciliation controls.", 760, 330, 520, 360, layer_style + "fillColor=#e1d5e7;strokeColor=#9673a6;")

    core_groups = [
        ("core_people", "<b>PARTICIPANT JOURNEY</b><hr>participants<br>participant_identifiers<br>outreach_events", 1480, 180, "#dae8fc", "#6c8ebf"),
        ("core_training", "<b>TRAINING DELIVERY</b><hr>projects<br>batches<br>enrolments<br>sessions<br>attendance<br>assessments", 1480, 500, "#fff2cc", "#d6b656"),
        ("core_employment", "<b>EMPLOYMENT PATHWAY</b><hr>employers<br>job_opportunities<br>placement_attempts<br>followups", 1480, 930, "#f8cecc", "#b85450"),
    ]
    for cid, value, cx, cy, fill, stroke in core_groups:
        add_vertex(root, cid, value, cx, cy, 540, 260 if cid != "core_training" else 330, layer_style + f"fillColor={fill};strokeColor={stroke};")

    views_value = "<b>SECURE REPORTING VIEWS</b><hr>" + "<br>".join(DASHBOARD_VIEWS)
    add_vertex(root, "reporting_views", views_value, 2240, 430, 620, 360, layer_style + "fillColor=#d5e8d4;strokeColor=#82b366;")
    add_vertex(root, "dashboard", "<b>VoN MANAGEMENT DASHBOARD</b><hr>Mobilisation conversion<br>Intake and delivery<br>Attendance and assessment<br>Employer and placement pipeline<br>12/24-month retention and income<br>Centre/batch/donor comparison", 2240, 940, 620, 310, layer_style + "fillColor=#ffe6cc;strokeColor=#d79b00;")
    add_vertex(root, "controls", "<b>CROSS-CUTTING CONTROLS</b><hr>security.user_access<br>audit.change_log<br>Row-level security<br>PII masking<br>Approved enums/check constraints<br>Versioned SQL migrations", 760, 910, 520, 330, layer_style + "fillColor=#e1d5e7;strokeColor=#9673a6;")

    e = 1
    for sid in source_ids:
        add_edge(root, f"ov_e{e}", sid, "staging_layer"); e += 1
    for cid, *_ in core_groups:
        add_edge(root, f"ov_e{e}", "staging_layer", cid); e += 1
        add_edge(root, f"ov_e{e}", cid, "reporting_views"); e += 1
    add_edge(root, f"ov_e{e}", "reporting_views", "dashboard"); e += 1
    add_edge(root, f"ov_e{e}", "controls", "core_training", "governs")
    diagram.append(model)


def add_detailed(mxfile: ET.Element) -> None:
    diagram = ET.SubElement(mxfile, "diagram", {"id": "von-detailed-v4", "name": "2. Detailed logical model"})
    model, root = new_graph_model(4300, 4300)
    title_style = "rounded=1;whiteSpace=wrap;html=1;fillColor=#1f4e78;strokeColor=#1f4e78;fontColor=#ffffff;fontSize=22;fontStyle=1;align=left;spacingLeft=16;"
    add_vertex(root, "detailed_title", "Voice of Needy IDS — detailed logical data model (version 4 proposal)", 40, 30, 4100, 60, title_style)

    positions = {
        "participants": (80, 140), "participant_identifiers": (80, 880), "outreach_events": (80, 1290),
        "projects": (1120, 140), "batches": (1120, 590), "enrolments": (1120, 1170),
        "sessions": (1120, 1890), "attendance": (1120, 2390), "assessments": (1120, 2840),
        "employers": (2200, 140), "job_opportunities": (2200, 680), "placement_attempts": (2200, 1260),
        "followups": (2200, 2100),
        "import_runs": (3260, 140), "source_records": (3260, 650), "change_log": (3260, 1370), "user_access": (3260, 1830),
    }
    widths = {eid: 820 for eid in positions}
    for entity in ENTITIES:
        x, y = positions[entity["id"]]
        height = 115 + len(entity["fields"]) * 20
        style = (
            "rounded=0;whiteSpace=wrap;html=1;align=left;verticalAlign=top;spacing=10;"
            f"fillColor={entity['color']};strokeColor={entity['stroke']};fontSize=11;"
        )
        add_vertex(root, entity["id"], table_html(entity), x, y, widths[entity["id"]], height, style)

    for idx, (source, target, label) in enumerate(RELATIONSHIPS, 1):
        add_edge(root, f"rel_{idx}", source, target, label)
    diagram.append(model)


def write_drawio() -> Path:
    mxfile = ET.Element("mxfile", {
        "host": "app.diagrams.net", "modified": "2026-11-20T00:00:00.000Z",
        "agent": "OpenAI Codex", "version": "24.7.17", "pages": "2",
    })
    add_overview(mxfile)
    add_detailed(mxfile)
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ")
    path = OUT / "von-ids-data-model-v4.drawio"
    tree.write(path, encoding="utf-8", xml_declaration=True)
    return path


def write_dot() -> Path:
    colors = {e["id"]: (e["color"], e["stroke"]) for e in ENTITIES}
    titles = {e["id"]: e["title"].split(". ", 1)[-1] for e in ENTITIES}
    lines = [
        "digraph G {", "graph [rankdir=LR, bgcolor=white, pad=0.3, nodesep=0.45, ranksep=1.0, splines=ortho];",
        "node [shape=box, style=\"rounded,filled\", fontname=\"Arial\", fontsize=10, margin=0.12];",
        "edge [fontname=\"Arial\", fontsize=8, color=\"#555555\", arrowsize=0.7];",
    ]
    for entity in ENTITIES[:13]:
        eid = entity["id"]
        field_lines = []
        for marker, name, typ in entity["fields"][:8]:
            field_lines.append(f"{marker + ' ' if marker else ''}{name} : {typ}")
        if len(entity["fields"]) > 8:
            field_lines.append(f"… {len(entity['fields']) - 8} more fields")
        label = titles[eid] + "\\l" + "\\l".join(field_lines) + "\\l"
        fill, stroke = colors[eid]
        lines.append(f'"{eid}" [label="{label}", fillcolor="{fill}", color="{stroke}"];')
    for source, target, label in RELATIONSHIPS:
        if source in titles and target in titles and source not in {"import_runs", "source_records"} and target not in {"import_runs", "source_records", "user_access"}:
            lines.append(f'"{source}" -> "{target}" [label="{label}"];')
    lines.append("}")
    path = OUT / "von-ids-data-model-v4.dot"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def render_preview(dot_path: Path) -> tuple[Path, Path]:
    svg = OUT / "von-ids-data-model-v4.svg"
    png = OUT / "von-ids-data-model-v4.png"
    subprocess.run(["dot", "-Tsvg", str(dot_path), "-o", str(svg)], check=True)
    subprocess.run(["dot", "-Tpng", str(dot_path), "-o", str(png)], check=True)
    return svg, png


def write_dictionary_markdown() -> Path:
    lines = [
        "# Voice of Needy IDS logical data dictionary",
        "",
        "**Version:** 4 field-level proposal  ",
        "**Status:** For analyst, frontend and senior-management review. Types and constraints are logical until SQL migrations are approved.",
        "",
        "The editable diagram and this dictionary are generated from the same entity specification. All operational tables also carry `created_at`, `updated_at`, `created_by` and `updated_by` where applicable.",
        "",
    ]
    for entity in ENTITIES:
        lines.extend([
            f"## {entity['title']}", "", entity["purpose"], "",
            "| Key | Field | Type / constraint |", "|---|---|---|",
        ])
        for marker, name, typ in entity["fields"]:
            lines.append(f"| {marker or '—'} | `{name}` | {typ} |")
        lines.append("")
    lines.extend([
        "## Controlled values", "",
        "Stable status fields use PostgreSQL check constraints or enum/domain types defined in version-controlled migrations. A separate lookup table is introduced only when VoN needs users to administer the values at runtime.",
        "",
        "Minimum controlled lists include outreach event/outcome/eligibility, batch/enrolment/session/attendance/assessment status, placement pipeline/status, follow-up employment/verification status, identifier type, salary period, user role and import disposition.",
        "",
        "## Privacy", "",
        "Phone, email, address, government/external identifiers, disability/support information, income and raw source payloads are restricted. Reporting views exclude direct identifiers unless an authorised operational use requires them.",
    ])
    path = Path("docs/data-dictionary.md")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_model_markdown() -> Path:
    core = [e for e in ENTITIES if e["title"].split(". ", 1)[-1].startswith("core.")]
    controls = [e for e in ENTITIES if e not in core]
    lines = [
        "# Voice of Needy IDS professional data model",
        "",
        "**Version:** 4 proposal  ",
        "**Status:** Detailed logical model for review; no production schema or migration is authorised.",
        "",
        "## Deliverables", "",
        "- Editable two-page diagrams.net model: [`docs/diagrams/von-ids-data-model-v4.drawio`](diagrams/von-ids-data-model-v4.drawio)",
        "- SVG preview: [`docs/diagrams/von-ids-data-model-v4.svg`](diagrams/von-ids-data-model-v4.svg)",
        "- PNG preview: [`docs/diagrams/von-ids-data-model-v4.png`](diagrams/von-ids-data-model-v4.png)",
        "- Field-level dictionary: [`docs/data-dictionary.md`](data-dictionary.md)",
        "",
        "The draw.io model follows the supplied reference structure: page 1 shows source/staging/core/reporting lineage; page 2 shows every table with business purpose, fields, data types, PK/FK markers, nullability/constraints and relationship lines.",
        "",
        "## Model size", "",
        "| Layer | Physical tables | Notes |", "|---|---:|---|",
        "| Canonical core | 13 | Participant journey, programme delivery and employment outcomes |",
        "| Staging/migration | 2 | Import execution and record-level source lineage/identity review |",
        "| Audit | 1 | Material change history |",
        "| Security | 1 | Auth role and project/centre scope |",
        "| Reporting | 0 | Five SQL views; no duplicated dashboard tables |",
        "| **Total** | **17** | Reduced but properly normalised |",
        "",
        "## Canonical core tables", "",
        "| # | Table | Grain / responsibility |", "|---:|---|---|",
    ]
    for i, entity in enumerate(core, 1):
        title = entity["title"].split(". ", 1)[-1]
        lines.append(f"| {i} | `{title}` | {entity['purpose']} |")
    lines.extend([
        "", "## Control tables", "", "| Table | Responsibility |", "|---|---|",
    ])
    for entity in controls:
        title = entity["title"].split(". ", 1)[-1]
        lines.append(f"| `{title}` | {entity['purpose']} |")
    lines.extend([
        "", "## Main relationships", "",
        "```mermaid", "erDiagram",
        "    PARTICIPANTS ||--o{ PARTICIPANT_IDENTIFIERS : has",
        "    PARTICIPANTS ||--o{ OUTREACH_EVENTS : has",
        "    PROJECTS ||--o{ OUTREACH_EVENTS : supports",
        "    PROJECTS ||--o{ BATCHES : funds",
        "    PARTICIPANTS ||--o{ ENROLMENTS : undertakes",
        "    BATCHES ||--o{ ENROLMENTS : contains",
        "    BATCHES ||--o{ SESSIONS : schedules",
        "    ENROLMENTS ||--o{ ATTENDANCE : receives",
        "    SESSIONS ||--o{ ATTENDANCE : records",
        "    ENROLMENTS ||--o{ ASSESSMENTS : has",
        "    EMPLOYERS ||--o{ JOB_OPPORTUNITIES : offers",
        "    ENROLMENTS ||--o{ PLACEMENT_ATTEMPTS : attempts",
        "    JOB_OPPORTUNITIES ||--o{ PLACEMENT_ATTEMPTS : receives",
        "    PLACEMENT_ATTEMPTS ||--o{ FOLLOWUPS : monitored_by",
        "    IMPORT_RUNS ||--o{ SOURCE_RECORDS : contains",
        "```", "",
        "## Source-to-core mapping", "",
        "| Master Sheet/source area | Staging treatment | Canonical destination |", "|---|---|---|",
        "| Participant Registry | One source row with identity checks | `participants`, `participant_identifiers` |",
        "| Sourcing; Mobilization; Outreach Contacts - Verify | Standardise source/contact event and resolve participant | `outreach_events`; participant profile updates only when verified |",
        "| Training | Standardise participant-batch record and dropout/readiness fields | `enrolments`; score fields to `assessments` |",
        "| Training Batch; Training Plans - Source References | Resolve project, centre, batch identity and plan evidence | `projects`, `batches` |",
        "| Training - session planned vs complete | Unpivot Session 01–45 and retain planned/actual status | `sessions` |",
        "| Training - Daily attendance; attendance roster/verify tabs | Unpivot Day 01–46 and verify participant/batch/session | `attendance` |",
        "| Training - Weekly assessments | Unpivot Week 1–6 | `assessments` |",
        "| Employers Data | Standardise organisation; split verified roles/vacancies | `employers`, `job_opportunities` |",
        "| Placements | Resolve enrolment and opportunity; retain stage/joining/evidence | `placement_attempts` |",
        "| Follow-ups | Resolve placement and append checkpoint attempt | `followups` |",
        "| ID Mapping, extra-trainee, dropout and other verify tabs | Preserve review evidence and apply only approved changes | `staging.source_records` plus approved core update |",
        "",
        "## Reporting views", "",
    ])
    for view in DASHBOARD_VIEWS:
        lines.append(f"- `{view}`")
    lines.extend([
        "", "Views are read-only and reproducible from core tables. They do not perform identity matching or overwrite operational records.",
        "", "## Why the model is not one table per Master Sheet tab", "",
        "Master Sheet tabs are collection/reporting surfaces, not database entities. Session and attendance columns are normalised into rows; verification tabs remain staging/audit evidence; participant identity is stored once and linked to repeated enrolment, placement and follow-up records. This preserves information while avoiding duplication and spreadsheet-shaped database design.",
        "", "## Approval gate", "",
        "Senior managers approve the business journey and KPI definitions. The analyst/technical reviewer approves table grains, field definitions, keys, constraints, source mappings and privacy boundaries. SQL migrations and production loading begin only after that approval is recorded.",
    ])
    path = Path("docs/data-model.md")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def write_erd_markdown() -> Path:
    text = """# Voice of Needy IDS diagrams

The professional data model is available in three formats:

- [Editable diagrams.net source](diagrams/von-ids-data-model-v4.drawio)
- [SVG preview](diagrams/von-ids-data-model-v4.svg)
- [PNG preview](diagrams/von-ids-data-model-v4.png)

The editable file contains:

1. **Architecture and lineage** — Master Sheet/source groups → staging/migration control → canonical domains → secure reporting views → dashboard.
2. **Detailed logical model** — 17 physical tables with purpose, fields, PostgreSQL-oriented types, PK/FK/UQ markings, nullability/constraints and relationships.

The draw.io file is the visual design source. The data dictionary is generated from the same entity specification so the diagram and documentation remain consistent.
"""
    path = Path("docs/data-model-erd.md")
    path.write_text(text, encoding="utf-8")
    return path


if __name__ == "__main__":
    drawio = write_drawio()
    dot = write_dot()
    svg, png = render_preview(dot)
    model_md = write_model_markdown()
    dictionary_md = write_dictionary_markdown()
    erd_md = write_erd_markdown()
    ET.parse(drawio)
    print(drawio)
    print(svg)
    print(png)
    print(model_md)
    print(dictionary_md)
    print(erd_md)
