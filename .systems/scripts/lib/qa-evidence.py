#!/usr/bin/env python3
"""Validate one versioned current QA assessment without consulting historical runs."""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path, PurePosixPath


REQUIRED = {
    "Run ID",
    "Artifact kind",
    "Project/task identity",
    "Assessed source HEAD",
    "Assessed worktree digest",
    "Input artifacts",
    "Verdict",
    "Gate Decision",
}
KINDS = {
    "architecture-qa",
    "plan-qa",
    "packaging-qa",
    "spec-qa",
    "implementation-quality",
    "final-check",
}
ROOTS = {"workflow-source", "approved-target-source", "owning-project-evidence"}
FORBIDDEN_PARTS = {".env", "secrets", "credentials", "private", "id_rsa"}
ARTIFACT_QA_KINDS = {"architecture-qa", "plan-qa", "packaging-qa", "spec-qa"}
FIXED_REPORTS = {
    "phase-1-architecture-qa.md": "architecture-qa",
    "phase-2-plan-qa.md": "plan-qa",
    "phase-2-packaging-qa.md": "packaging-qa",
    "phase-8-final-check.md": "final-check",
}


class InvalidAssessment(ValueError):
    pass


def outside_fences(lines):
    fence = None
    for number, line in enumerate(lines):
        stripped = line.lstrip()
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if marker:
            if fence is None:
                fence = marker.group(1)
            elif marker.group(1)[0] == fence[0] and len(marker.group(1)) >= len(fence):
                fence = None
            continue
        if fence is None:
            yield number, line


def headings(lines):
    for number, line in outside_fences(lines):
        match = re.match(r"^(#{2,3}) ([^#].*?)\s*$", line)
        if match:
            yield number, len(match.group(1)), match.group(2)


def current_section(lines):
    positions = list(headings(lines))
    starts = [number for number, level, title in positions if level == 2 and title == "Current QA Run"]
    if len(starts) != 1:
        raise InvalidAssessment("exactly one top-level Current QA Run is required")
    start = starts[0]
    end = next((number for number, level, _ in positions if level == 2 and number > start), len(lines))
    return start, end


def verify_run_ids(lines, current_id):
    seen = set()
    section = None
    for _, line in outside_fences(lines):
        heading = re.match(r"^## ([^#].*?)\s*$", line)
        if heading:
            section = heading.group(1)
            continue
        if section not in {"Current QA Run", "Historical Runs"}:
            continue
        match = re.match(r"^- Run ID:\s*`?([a-z0-9-]+)`?(?:\s*[;.]|\s*$)", line)
        if not match:
            continue
        run_id = match.group(1)
        if run_id in seen:
            raise InvalidAssessment("duplicate QA run ID")
        seen.add(run_id)
    if current_id not in seen:
        raise InvalidAssessment("current QA run ID is not recorded")


def declared_report_results(lines):
    section = None
    results = {}
    for _, line in outside_fences(lines):
        if line.startswith("## "):
            section = line[3:] if line in {"## Metadata", "## Validation Execution Record"} else None
            continue
        if section is None:
            continue
        field = "Result" if section == "Metadata" else "Final verdict"
        match = re.match(r"^- " + field + r":\s*(.*?)\s*$", line)
        if match:
            if section in results:
                raise InvalidAssessment("duplicate report-level " + field + " field")
            results[section] = match.group(1).strip("` ")
    return results


def wire_version(lines):
    section, versions = None, []
    for _, line in outside_fences(lines):
        if line.startswith('## '):
            section = line[3:]
        declaration = re.fullmatch(r'\s*-\s*QA verification contract\s*:\s*(.*?)\s*', line, re.I)
        if declaration:
            match = re.fullmatch(r'\x60full-qa-verification-v([0-9]+)\x60', declaration.group(1))
            if not match or section not in {None, 'Metadata'}:
                raise InvalidAssessment('malformed or misplaced QA wire declaration')
            version = int(match.group(1))
            if section is None and version != 2:
                raise InvalidAssessment('nonlegacy QA wire requires Metadata')
            versions.append(version)
    if not versions:
        return 2  # A legacy marker is still required by the ordinary V2 parser.
    if len(versions) != 1 or versions[0] not in {1, 2, 3}:
        raise InvalidAssessment('exactly one metadata QA wire version is required')
    return versions[0]


def read_current(lines):
    start, end = current_section(lines)
    subsection_headings = {
        number: title
        for number, level, title in headings(lines)
        if level == 3 and start < number < end
    }
    metadata = {}
    subsections = {}
    heading = None
    visible = {number for number, _ in outside_fences(lines)}
    for number in range(start + 1, end):
        line = lines[number]
        if number in subsection_headings:
            heading = subsection_headings[number]
            if heading in subsections:
                raise InvalidAssessment("duplicate current subsection: " + heading)
            subsections[heading] = []
            continue
        if heading is None:
            if number in visible:
                field = re.match(r"^- ([^:]+):\s*(.*?)\s*$", line)
                if field:
                    key, value = field.groups()
                    if key in metadata:
                        raise InvalidAssessment("duplicate current field: " + key)
                    metadata[key] = value.strip("` ")
        else:
            subsections[heading].append(line)
    missing = REQUIRED - metadata.keys()
    if missing:
        raise InvalidAssessment("missing current fields: " + ", ".join(sorted(missing)))
    for heading in ("Input Artifacts", "Findings", "Evidence", "Review Completeness Gate"):
        if heading not in subsections or not any(line.strip() for line in subsections[heading]):
            raise InvalidAssessment("missing or empty current subsection: " + heading)
    return metadata, subsections


def contained(root, relative):
    path = PurePosixPath(relative)
    if not relative or "\\" in relative or path.is_absolute() or any(part in ("", ".", "..") for part in relative.split("/")):
        raise InvalidAssessment("unsafe input path")
    if any(part.lower() in FORBIDDEN_PARTS or part.lower().endswith((".pem", ".key")) for part in path.parts):
        raise InvalidAssessment("sensitive input path is not approved for hashing")
    if any(path.parts[index:index + 3] == ("quality", "artifacts", "node_modules")
           for index in range(len(path.parts) - 2)):
        raise InvalidAssessment("runtime dependency directory is not evidence")
    candidate = root.joinpath(*path.parts)
    try:
        resolved = candidate.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise InvalidAssessment("missing or unreadable input artifact") from error
    if os.path.commonpath((str(root), str(resolved))) != str(root) or not resolved.is_file():
        raise InvalidAssessment("input artifact escapes approved root")
    parents_inside_root = []
    parent = candidate.parent
    while parent != root:
        parents_inside_root.append(parent)
        parent = parent.parent
    if candidate.is_symlink() or any(parent.is_symlink() for parent in parents_inside_root):
        raise InvalidAssessment("symlink input artifact is not approved")
    return resolved


def input_rows(lines):
    rows = []
    for _, line in outside_fences(lines):
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            raise InvalidAssessment("input artifact table must have three columns")
        if cells[0] == "Root kind" or all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
            continue
        rows.append(tuple(cells))
    if not rows:
        raise InvalidAssessment("current input artifact table has no rows")
    return rows


def section_fields(lines):
    values = {}
    for _, line in outside_fences(lines):
        match = re.match(r"^- ([^:]+):\s*(.*?)\s*$", line)
        if match:
            key, value = match.groups()
            if key in values:
                raise InvalidAssessment("duplicate current evidence field: " + key)
            values[key] = value.strip("` ")
    return values


def validate_gate_subsection(kind, verdict, sections):
    lines = sections.get("Gate Decision")
    if lines is None:
        if verdict == "PASS" and kind in ARTIFACT_QA_KINDS:
            raise InvalidAssessment("missing current Gate Decision subsection")
        return
    values = {}
    for line in lines:
        match = re.match(r"^\s*(?:-\s*)?([A-Za-z][A-Za-z /-]*):\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        key = key.lower().replace("-", " ")
        if key in values:
            raise InvalidAssessment("duplicate current Gate Decision field: " + key)
        values[key] = value.strip("`\"' ").lower()
    kind_result_key = {
        "architecture-qa": "architecture qa result",
        "plan-qa": "plan qa result",
        "packaging-qa": "packaging qa result",
        "spec-qa": "spec qa result",
        "implementation-quality": "result",
    }.get(kind)
    result_keys = {"result", "qa result", "quality result", kind_result_key}
    declared_results = {key: value for key, value in values.items() if key in result_keys}
    if (verdict == "PASS" and not declared_results) or any(value != verdict.lower() for value in declared_results.values()):
        raise InvalidAssessment("current Gate Decision subsection conflicts with verdict")
    for key, value in values.items():
        if key.startswith("can proceed") or key.startswith("can enter"):
            if key == "can proceed to optional task packaging":
                continue
            if verdict == "PASS" and value not in {"yes", "true"}:
                raise InvalidAssessment("current Gate Decision blocks progression despite PASS")
            if verdict == "FAIL" and value in {"yes", "true"}:
                raise InvalidAssessment("current Gate Decision allows progression despite FAIL")
    if verdict == "PASS":
        for key in ("required next phase", "default next phase"):
            if re.search(r"fix[ -]loop", values.get(key, ""), re.I):
                raise InvalidAssessment("current Gate Decision routes PASS to a fix loop")


def require_values(values, expected, context):
    for field, allowed in expected.items():
        value = values.get(field, "")
        if not value or re.search(r"<[^>]+>|\b(?:TODO|TBD|null)\b", value, re.I):
            raise InvalidAssessment("missing or incomplete " + context + ": " + field)
        if allowed is not None and value not in allowed:
            raise InvalidAssessment("unsatisfied " + context + ": " + field)


def require_substantive(values, fields, context):
    require_values(values, {field: None for field in fields}, context)
    for field in fields:
        if values[field].lower() in {"missing", "unknown", "incomplete", "stale", "none", "n/a"}:
            raise InvalidAssessment("unsatisfied " + context + ": " + field)


def table_rows(lines, header, width, context):
    rows = []
    for _, line in outside_fences(lines):
        if not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells[0] == header or all(re.fullmatch(r"[-: ]+", cell) for cell in cells):
            continue
        if len(cells) != width or any(not cell or re.search(r"<[^>]+>|\b(?:TODO|TBD|null)\b", cell, re.I) for cell in cells):
            raise InvalidAssessment("incomplete current " + context + " row")
        rows.append(cells)
    if not rows:
        raise InvalidAssessment("missing current " + context + " row")
    return rows


def validate_current_pass(kind, sections):
    check_lines = sections["Evidence"]
    for heading in ("Checks", "Commands", "Manual Checks", "Edge Cases"):
        check_lines.extend(sections.get(heading, []))
    if any(re.search(r"^\s*(?:-\s*)?result:\s*[`\"']?FAIL\b|\|\s*FAIL\s*\|", line, re.I) for line in check_lines):
        raise InvalidAssessment("current PASS has a failed check or manual result")
    findings = section_fields(sections["Findings"])
    require_values(findings, {"Blockers": {"none", "resolved"}, "Unresolved findings": {"none"}}, "Findings")
    completeness = section_fields(sections["Review Completeness Gate"])
    require_values(
        completeness,
        {
            "Status": {"complete"},
            "Reviewed baseline": None,
            "Closure freshness": {"current"},
            "Post-fix full re-review": {"completed", "not-required"},
            "Policy-boundary adversarial matrix": {"completed", "not-applicable"},
            "Producer-consumer field audit": {"completed", "not-applicable"},
            "Required-field mapping": {"complete", "not-applicable"},
        },
        "Review Completeness Gate",
    )
    require_substantive(completeness, ("Reviewed baseline",), "Review Completeness Gate")
    if kind in ARTIFACT_QA_KINDS:
        if "QA Verification Scope" not in sections or not any(line.strip() for line in sections["QA Verification Scope"]):
            raise InvalidAssessment("missing current QA Verification Scope")
        gate = section_fields(sections.get("Artifact QA Completeness Gate", []))
        require_values(
            gate,
            {
                "Owner intent and governing sources reviewed": None,
                "DoD / phase acceptance criteria reviewed": {"yes"},
                "Scope and out-of-scope consistency": {"aligned"},
                "Artifact / relevant diff review": {"completed"},
                "Findings-first review": {"completed"},
                "Failure / rework / dependency scenarios": {"completed", "not-applicable"},
                "Repository and source compatibility": {"aligned"},
                "Post-fix full artifact re-review": {"completed", "not-required"},
                "Evidence reviewed": None,
                "Skipped or unreadable sources": None,
                "Residual risk": None,
                "Closure freshness": {"current"},
            },
            "Artifact QA Completeness Gate",
        )
        require_substantive(gate, ("Owner intent and governing sources reviewed", "Evidence reviewed"), "Artifact QA Completeness Gate")
    elif kind == "implementation-quality":
        for heading in ("Definition Of Done Validation", "Intent / Plan / Spec Compliance", "Adaptive Data / Integration Verification Matrix", "Quality Gate"):
            if heading not in sections or not any(line.strip() for line in sections[heading]):
                raise InvalidAssessment("missing current implementation quality section: " + heading)
        dod_rows = table_rows(sections["Definition Of Done Validation"], "DoD Item", 3, "DoD validation")
        if any(row[1] != "PASS" for row in dod_rows):
            raise InvalidAssessment("implementation PASS lacks complete current DoD validation")
        intent = section_fields(sections["Intent / Plan / Spec Compliance"])
        require_values(intent, {
            "Result": {"PASS"}, "Owner instruction reviewed": {"yes"},
            "Accepted plan reviewed": {"yes", "not-applicable"},
            "Accepted spec reviewed": {"yes", "not-applicable"},
            "Scope/out-of-scope reviewed": {"yes", "not-applicable"},
            "Acceptance criteria reviewed": {"yes"}, "Compliance status": {"aligned"},
            "Wrong problem solved": {"no"}, "Owner instruction mismatch": {"no"},
            "Accepted plan mismatch": {"no", "not-applicable"},
            "Accepted spec mismatch": {"no", "not-applicable"},
            "Acceptance criteria gap": {"no"}, "Scope creep": {"no"},
            "Underbuild": {"no"}, "Overbuild": {"no"}, "Evidence": None,
        }, "Intent / Plan / Spec Compliance")
        require_substantive(intent, ("Evidence",), "Intent / Plan / Spec Compliance")
        require_values(completeness, {
            "Cross-contract consistency": {"aligned"},
            "Risk/work mode compatibility": {"aligned"},
            "Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed": {"yes", "not-applicable"},
            "Negative-space / adversarial review": {"completed", "not-applicable"},
            "Automated evidence role": {"supporting-only"},
            "Instruction refresh": {"performed-targeted", "performed-full", "not-needed"},
            "Instruction baseline": {"current"},
            "Producers/consumers reviewed": None,
            "Evidence": None,
        }, "Review Completeness Gate")
        require_substantive(completeness, ("Evidence",), "Review Completeness Gate")
        gate = section_fields(sections["Quality Gate"])
        for field in (
            "Intent / Plan / Spec Compliance PASS", "Review Completeness Gate PASS",
            "Cross-contract consistency aligned", "Risk/work mode compatibility aligned",
            "Negative-space / adversarial review complete or not applicable",
            "Automated evidence treated as supporting-only", "Post-fix full re-review complete or not required",
            "Instruction baseline current", "Closure freshness current",
            "Policy-boundary adversarial matrix complete or not applicable",
            "Producer-consumer field audit complete or not applicable",
            "Required-field mapping complete or not applicable", "100% DoD satisfied",
            "No known bug in scope", "No regression in changed/direct paths",
            "Edge cases covered or explicitly rejected", "Explicit evidence attached",
        ):
            require_values(gate, {field: {"yes"}}, "Quality Gate")
        require_values(gate, {"Quality result": {"PASS"}}, "Quality Gate")
        if re.search(r"fix[ -]loop", gate.get("Required next phase", ""), re.I):
            raise InvalidAssessment("current Quality Gate routes PASS to a fix loop")
        matrix = section_fields(sections["Adaptive Data / Integration Verification Matrix"])
        require_values(matrix, {"Applicability": {"required", "not-applicable"}}, "Adaptive Data / Integration Verification Matrix")
        if matrix["Applicability"] == "not-applicable":
            require_values(matrix, {"Not-applicable reason": None}, "Adaptive Data / Integration Verification Matrix")
        else:
            table_rows(sections["Adaptive Data / Integration Verification Matrix"], "Source Shape", 7, "adaptive matrix")
    elif kind == "final-check":
        for heading in ("Completion Review", "Owner Approval", "Final Gate"):
            if heading not in sections or not any(line.strip() for line in sections[heading]):
                raise InvalidAssessment("missing current final-check section: " + heading)
        completion_rows = table_rows(sections["Completion Review"], "Area", 3, "Completion Review")
        if any(row[1] not in {"PASS", "awaiting"} for row in completion_rows):
            raise InvalidAssessment("final check PASS has failed completion area")
        owner = section_fields(sections["Owner Approval"])
        require_values(owner, {"Technical final check result": {"PASS"}, "Owner approval required": {"yes"}, "Owner decision": {"awaiting", "approved"}}, "Owner Approval")
        gate = section_fields(sections["Final Gate"])
        require_values(gate, {"Can close active plan": {"awaiting-owner", "yes"}}, "Final Gate")
        if owner["Owner decision"] != "approved" and gate["Can close active plan"] == "yes":
            raise InvalidAssessment("final check cannot close plan before owner approval")


def report_kind_and_identity(report, project):
    filename = report.name.removeprefix("recovery-")
    if filename in FIXED_REPORTS:
        return FIXED_REPORTS[filename], project
    match = re.fullmatch(r"phase-3-([a-z0-9-]+)-spec-qa\.md", filename)
    if match:
        return "spec-qa", project + ":" + match.group(1)
    match = re.fullmatch(r"phase-5-([a-z0-9-]+)-quality\.md", filename)
    if match:
        return "implementation-quality", project + ":" + match.group(1)
    raise InvalidAssessment("V2 report filename does not identify a formal QA phase")


def owner_approval(report, workflow, workspace, project, document=None):
    if report.is_symlink() or any(parent.is_symlink() for parent in report.parents if parent != Path("/")):
        raise InvalidAssessment("linked owner approval report")
    owner = workspace.resolve(strict=True) / "projects" / project
    if report.parent.resolve(strict=True) != (owner / "quality").resolve(strict=True):
        raise InvalidAssessment("approval is outside owning quality root")
    text = report.read_text() if document is None else document
    values = section_fields(text.splitlines())
    require_values(values, {"Owner approval contract": {"owner-approval-v1"}, "Scope": {project},
                           "Owner decision": {"final-owner-yes"}, "Approval reference": None,
                           "Approval SHA-256": None, "Final check": None, "Final check SHA-256": None},
                   "Owner Approval")
    approval = contained(owner, values["Approval reference"])
    if not values["Approval reference"].startswith("decisions/"):
        raise InvalidAssessment("approval requires explicit owning decision")
    final = contained(owner, values["Final check"])
    if hashlib.sha256(approval.read_bytes()).hexdigest() != values["Approval SHA-256"]:
        raise InvalidAssessment("approval reference integrity mismatch")
    if hashlib.sha256(final.read_bytes()).hexdigest() != values["Final check SHA-256"]:
        raise InvalidAssessment("final check integrity mismatch")
    decision = section_fields(approval.read_text().splitlines())
    require_values(decision, {"Owner decision": {"final-owner-yes"}, "Approved scope": {project},
                             "Source": None}, "Explicit owner decision")
    assess(final, workflow, workspace, project, expected_kind="final-check", require_pass=True)
    return {"owner_decision": "final-owner-yes", "scope": project, "reference": values["Approval reference"]}


def history_entry(report, owner_project_root):
    registry = owner_project_root / "quality-assessments.json"
    if not registry.exists():
        return None
    if registry.is_symlink():
        raise InvalidAssessment("linked history registry")
    def unique_pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise InvalidAssessment("duplicate history field")
            result[key] = value
        return result
    data = json.loads(registry.read_text(), object_pairs_hook=unique_pairs)
    if set(data) != {"schema", "assessments"} or data["schema"] != 1 or not isinstance(data["assessments"], list):
        raise InvalidAssessment("invalid history registry")
    selected = None
    seen = set()
    for entry in data["assessments"]:
        if set(entry) != {"path", "sha256", "state", "assessed_head", "decision", "decision_sha256"}:
            raise InvalidAssessment("invalid historical assessment fields")
        if entry["state"] not in {"historical", "superseded"} or entry["path"] in seen:
            raise InvalidAssessment("invalid or duplicate historical assessment")
        seen.add(entry["path"])
        original = contained(owner_project_root, entry["path"])
        if original.parent != owner_project_root / "quality":
            raise InvalidAssessment("historical report must stay in owning quality root")
        decision = contained(owner_project_root, entry["decision"])
        if not entry["decision"].startswith("decisions/") or not decision.read_text().strip():
            raise InvalidAssessment("history requires an explicit decision artifact")
        permission = section_fields(decision.read_text().splitlines())
        require_values(permission, {"History decision": {"approved"}, "Approved report": {entry["path"]},
                                   "Approved state": {entry["state"]}, "Source": None}, "Historical admission")
        for source, field in ((original, "sha256"), (decision, "decision_sha256")):
            if not re.fullmatch(r"[0-9a-f]{64}", entry[field]) or hashlib.sha256(source.read_bytes()).hexdigest() != entry[field]:
                raise InvalidAssessment("historical integrity mismatch")
        if not re.fullmatch(r"[0-9a-f]{40}", entry["assessed_head"]):
            raise InvalidAssessment("invalid historical baseline")
        if original == report:
            selected = entry
    return selected


def assess(report, workflow_root, workspace_root, project, target_root=None, expected_kind=None, expected_identity=None, schema_only=False, require_pass=False, document=None, verify_inputs=True, history_integrity=False, _v3_normalized=False):
    report = report.resolve(strict=document is None)
    workflow_root = workflow_root.resolve(strict=True)
    workspace_root = workspace_root.resolve(strict=not schema_only)
    if schema_only:
        if project != "EXAMPLE":
            raise InvalidAssessment("schema-only validation is reserved for bundled examples")
        owner_project_root = workflow_root / ".systems/ai/examples/projects/EXAMPLE"
    else:
        owner_project_root = workspace_root / "projects" / project
    owner_root = (owner_project_root / "quality").resolve(strict=True)
    if os.path.commonpath((str(owner_root), str(report))) != str(owner_root):
        raise InvalidAssessment("assessment is outside its owning project quality root")
    historical = None if schema_only or document is not None else history_entry(report, owner_project_root)
    if historical:
        if not history_integrity or require_pass:
            raise InvalidAssessment("historical assessment cannot supply current PASS")
        verify_inputs = False
    lines = (report.read_text(encoding="utf-8") if document is None else document).splitlines()
    if not _v3_normalized and wire_version(lines) == 3:
        if historical:
            raise InvalidAssessment('historical V3 cannot supply current eligibility')
        import importlib.util
        spec = importlib.util.spec_from_file_location('qa_binding', Path(__file__).with_name('qa-commit-binding.py'))
        binding = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(binding)
        return binding.assess_v3(report, workflow_root, workspace_root, project, target_root,
                                 expected_kind, expected_identity, schema_only, require_pass,
                                 document, verify_inputs, False, sys.modules[__name__] if __name__ in sys.modules else binding.load('qa-evidence'))
    if "QA verification contract: `full-qa-verification-v2`" not in "\n".join(lines):
        raise InvalidAssessment("missing V2 contract marker")
    metadata, sections = read_current(lines)
    if historical and metadata["Assessed source HEAD"] != historical["assessed_head"]:
        raise InvalidAssessment("historical baseline does not match registered assessment")
    verify_run_ids(lines, metadata["Run ID"])
    if metadata["Artifact kind"] not in KINDS:
        raise InvalidAssessment("invalid artifact kind")
    filename_kind, filename_identity = report_kind_and_identity(report, project)
    if metadata["Artifact kind"] != filename_kind:
        raise InvalidAssessment("artifact kind does not match report filename")
    if expected_kind is not None and metadata["Artifact kind"] != expected_kind:
        raise InvalidAssessment("current artifact kind does not match consumer")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", metadata["Run ID"]):
        raise InvalidAssessment("invalid run ID")
    identity = metadata["Project/task identity"]
    if not re.fullmatch(re.escape(project) + r"(?::[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)*)?", identity):
        raise InvalidAssessment("current assessment belongs to another project")
    if expected_identity is not None and identity != expected_identity:
        raise InvalidAssessment("current identity does not match consumer")
    if identity.lower() != filename_identity.lower():
        raise InvalidAssessment("current identity does not match report filename")
    if not re.fullmatch(r"[0-9a-f]{40}", metadata["Assessed source HEAD"]):
        raise InvalidAssessment("invalid assessed source HEAD")
    if not re.fullmatch(r"[0-9a-f]{64}", metadata["Assessed worktree digest"]):
        raise InvalidAssessment("invalid assessed worktree digest")
    verdict = metadata["Verdict"]
    if verdict not in ("PASS", "FAIL") or metadata["Gate Decision"] != verdict:
        raise InvalidAssessment("current verdict and gate decision conflict")
    allowed_results = {verdict}
    if metadata["Artifact kind"] == "final-check" and verdict == "PASS":
        allowed_results.add("awaiting-owner-final-yes")
    for section, result in declared_report_results(lines).items():
        if result not in allowed_results:
            raise InvalidAssessment("report-level " + ("Result" if section == "Metadata" else "Final verdict") + " conflicts with current verdict")
    validate_gate_subsection(metadata["Artifact kind"], verdict, sections)
    if require_pass and verdict != "PASS":
        raise InvalidAssessment("status PASS conflicts with current QA verdict")
    if metadata["Input artifacts"] != "see table":
        raise InvalidAssessment("Input artifacts must refer to the current table")

    allowed = {"workflow-source": workflow_root, "owning-project-evidence": owner_project_root}
    if target_root is not None:
        allowed["approved-target-source"] = target_root.resolve(strict=True)
    digest_lines = []
    seen = set()
    for root_kind, relative, checksum in input_rows(sections["Input Artifacts"]):
        if root_kind not in ROOTS or root_kind not in allowed:
            raise InvalidAssessment("input root is not approved: " + root_kind)
        if not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise InvalidAssessment("invalid input SHA-256")
        key = root_kind + ":" + relative
        if key in seen:
            raise InvalidAssessment("duplicate input artifact")
        seen.add(key)
        if schema_only:
            path = PurePosixPath(relative)
            if not relative or "\\" in relative or path.is_absolute() or any(part in ("", ".", "..") for part in relative.split("/")):
                raise InvalidAssessment("unsafe example input path")
            if any(part.lower() in FORBIDDEN_PARTS for part in path.parts):
                raise InvalidAssessment("sensitive example input path")
            continue
        if not verify_inputs:
            path = PurePosixPath(relative)
            if not relative or "\\" in relative or path.is_absolute() or any(part in ("", ".", "..") for part in relative.split("/")):
                raise InvalidAssessment("unsafe historical input path")
            if any(part.lower() in FORBIDDEN_PARTS or part.lower().endswith((".pem", ".key")) for part in path.parts):
                raise InvalidAssessment("sensitive historical input path")
            digest_lines.append(key + "=" + checksum + "\n")
            continue
        source = contained(allowed[root_kind].resolve(strict=True), relative)
        if source == report:
            raise InvalidAssessment("assessment cannot hash itself")
        try:
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
        except OSError as error:
            raise InvalidAssessment("unreadable input artifact") from error
        if actual != checksum:
            raise InvalidAssessment("stale or mismatched input SHA-256: " + key)
        digest_lines.append(key + "=" + checksum + "\n")
    digest = hashlib.sha256("".join(sorted(digest_lines)).encode("utf-8")).hexdigest()
    if not schema_only and digest != metadata["Assessed worktree digest"]:
        raise InvalidAssessment("stale or mismatched assessed worktree digest")

    for name in ("Findings", "Evidence", "Review Completeness Gate"):
        content = "\n".join(sections[name]).strip()
        if not content or re.search(r"<[^>]+>|\b(?:TODO|TBD|null)\b", content, re.I):
            raise InvalidAssessment("incomplete current " + name)
    completeness = "\n".join(sections["Review Completeness Gate"])
    if verdict == "PASS":
        findings = "\n".join(sections["Findings"])
        if not re.search(r"\b(none|resolved)\b", findings, re.I) or re.search(r"\b(P0|P1|material P2)\b.*\b(open|unresolved|active)\b", findings, re.I):
            raise InvalidAssessment("PASS has unresolved or undocumented findings")
        validate_current_pass(metadata["Artifact kind"], sections)
    return {
        "run_id": metadata["Run ID"],
        "artifact_kind": metadata["Artifact kind"],
        "identity": identity,
        "assessed_source_head": metadata["Assessed source HEAD"],
        "worktree_digest": digest,
        "verdict": verdict,
        "input_count": len(seen),
        "lifecycle": historical["state"] if historical else "current",
        "current_gate_eligible": historical is None,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    parser.add_argument("--workflow-root", required=True, type=Path)
    parser.add_argument("--workspace-root", required=True, type=Path)
    parser.add_argument("--project", required=True)
    parser.add_argument("--approved-target-root", type=Path)
    parser.add_argument("--expected-kind", choices=sorted(KINDS))
    parser.add_argument("--expected-identity")
    parser.add_argument("--schema-only", action="store_true", help="Validate bundled EXAMPLE structure without claiming runtime hash evidence")
    parser.add_argument("--require-pass", action="store_true", help="Require current QA verdict PASS for status progression")
    parser.add_argument("--history-integrity", action="store_true", help="Validate explicitly registered immutable history, never current progression")
    parser.add_argument("--owner-approval", action="store_true", help="Validate explicit owner approval provenance")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.project) and not (args.schema_only and args.project == "EXAMPLE"):
        parser.error("unsafe project slug")
    try:
        if args.owner_approval:
            print(json.dumps(owner_approval(args.report, args.workflow_root, args.workspace_root, args.project), sort_keys=True))
            return 0
        result = assess(
            args.report,
            args.workflow_root,
            args.workspace_root,
            args.project,
            args.approved_target_root,
            args.expected_kind,
            args.expected_identity,
            args.schema_only,
            args.require_pass,
            history_integrity=args.history_integrity,
        )
    except (ValueError, TypeError, KeyError, OSError, UnicodeError) as error:
        print("Invalid current QA assessment: " + str(error), file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
