#!/usr/bin/env python3
"""Render reviewer-supplied formal QA with the same schema as its consumer."""
import argparse
from datetime import date
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("qa_record_schema", HERE / "qa-evidence.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
spec = importlib.util.spec_from_file_location("quality_boundaries", HERE / "execution-efficiency.py")
eff = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eff)


def strict_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate producer field")
            result[key] = value
        return result
    if path.is_symlink():
        raise ValueError("linked review input")
    return json.loads(path.read_text(), object_pairs_hook=pairs)


def render(record, workflow, workspace, project):
    workflow = eff.canonical_path(workflow).resolve(strict=True)
    workspace = eff.canonical_path(workspace).resolve(strict=True)
    if record.get("kind") == "owner-approval":
        required = {"schema", "kind", "approval_reference", "final_check"}
        if set(record) != required or record["schema"] != 1:
            raise ValueError("invalid supplied owner approval record")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project):
            raise ValueError("unsafe approval project")
        owner = workspace / "projects" / project
        approval = qa.contained(owner, record["approval_reference"])
        final = qa.contained(owner, record["final_check"])
        output = owner / "quality/phase-8-final-owner-approval.md"
        body = ("# Owner Approval\n\n## Evidence\n- Owner approval contract: owner-approval-v1\n"
                f"- Scope: {project}\n- Owner decision: final-owner-yes\n"
                f"- Approval reference: {record['approval_reference']}\n"
                f"- Approval SHA-256: {hashlib.sha256(approval.read_bytes()).hexdigest()}\n"
                f"- Final check: {record['final_check']}\n"
                f"- Final check SHA-256: {hashlib.sha256(final.read_bytes()).hexdigest()}\n")
        qa.owner_approval(output, workflow, workspace, project, document=body)
        return output, body
    required = {"schema", "kind", "task", "run_id", "verdict", "inputs", "sections", "date"}
    if set(record) != required or record["schema"] != 1:
        raise ValueError("invalid reviewer record")
    kind = record["kind"]
    if kind not in qa.KINDS or record["verdict"] not in {"PASS", "FAIL"}:
        raise ValueError("unsupported quality kind or supplied verdict")
    task = record["task"]
    if kind in qa.FIXED_REPORTS.values():
        if task is not None:
            raise ValueError("project QA kind does not accept task identity")
        name = next(name for name, value in qa.FIXED_REPORTS.items() if value == kind)
    else:
        if not isinstance(task, str) or not re.fullmatch(r"[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)*", task):
            raise ValueError("unsafe task identity")
        name = ("phase-3-" + task.lower() + "-spec-qa.md") if kind == "spec-qa" else ("phase-5-" + task.lower() + "-quality.md")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project):
        raise ValueError("unsafe project")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", record["date"]):
        raise ValueError("invalid date")
    date.fromisoformat(record["date"])
    owner = workspace / "projects" / project
    output = owner / "quality" / name
    roots = {"workflow-source": workflow, "owning-project-evidence": owner}
    entries = []
    for entry in record["inputs"]:
        if set(entry) != {"root", "path"} or entry["root"] not in roots:
            raise ValueError("unapproved producer input root")
        path = qa.contained(roots[entry["root"]], entry["path"])
        if path == output:
            raise ValueError("self-referential input")
        entries.append((entry["root"], entry["path"], hashlib.sha256(path.read_bytes()).hexdigest()))
    if not entries or len({(root, path) for root, path, _ in entries}) != len(entries):
        raise ValueError("empty or duplicate producer inputs")
    bound = "".join(sorted(root + ":" + path + "=" + checksum + "\n" for root, path, checksum in entries))
    head = subprocess.check_output(["git", "-C", str(workflow), "rev-parse", "HEAD"], text=True).strip()
    sections = record["sections"]
    if not isinstance(sections, dict) or not sections:
        raise ValueError("reviewer must supply semantic sections")
    for heading, body in sections.items():
        if not isinstance(heading, str) or "\n" in heading or heading == "Input Artifacts":
            raise ValueError("unsafe or generated section heading")
        if not isinstance(body, str) or not body.strip() or re.search(r"^#{1,3} ", body, re.M):
            raise ValueError("missing or injected semantic section")
    owner_fields = qa.section_fields(sections.get("Owner Approval", "").splitlines())
    if kind == "final-check" and owner_fields.get("Owner decision") != "awaiting":
        raise ValueError("producer keeps technical final check awaiting explicit owner approval record")
    verdict = record["verdict"]
    final_state = "awaiting-owner-final-yes" if kind == "final-check" and verdict == "PASS" else verdict
    body = f"# Quality Record\n\n## Metadata\n- Project: {project}\n- Date: {record['date']}\n- Result: {final_state}\n- QA verification contract: `full-qa-verification-v2`\n\n## Current QA Run\n"
    for field, value in (("Run ID", record["run_id"]), ("Artifact kind", kind),
                         ("Project/task identity", project + (":" + task if task else "")),
                         ("Assessed source HEAD", head), ("Assessed worktree digest", hashlib.sha256(bound.encode()).hexdigest()),
                         ("Input artifacts", "see table"), ("Verdict", verdict), ("Gate Decision", verdict)):
        body += f"- {field}: {value}\n"
    body += "\n### Input Artifacts\n| Root kind | Relative path | SHA-256 |\n| --- | --- | --- |\n"
    for root, path, checksum in entries:
        if "|" in path:
            raise ValueError("unsafe Markdown input path")
        body += f"| {root} | {path} | {checksum} |\n"
    for heading, content in sections.items():
        body += f"\n### {heading}\n{content.rstrip()}\n"
    qa.assess(output, workflow, workspace, project, document=body)
    return output, body


def publish(output, body):
    if any(p.is_symlink() for p in (output, *output.parents)):
        raise ValueError("linked quality output")
    if output.exists():
        raise ValueError("quality output already exists; preserve history")
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix=".quality-", delete=False) as stream:
        temp = Path(stream.name)
        try:
            stream.write(body.encode())
            stream.flush()
            os.fsync(stream.fileno())
            os.link(temp, output)
        finally:
            temp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--workflow-root", type=Path, required=True)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        workflow = eff.canonical_path(args.workflow_root).resolve(strict=True)
        workspace = eff.canonical_path(args.workspace_root).resolve(strict=True)
        owner = qa.contained(workspace, "projects/" + args.project + "/context.md").parent
        if not (owner / "quality").is_dir():
            raise ValueError("missing owning quality directory")
        output, body = render(strict_json(args.review), workflow, workspace, args.project)
        if args.dry_run:
            print(body)
        else:
            publish(output, body)
            print(str(output))
        return 0
    except (ValueError, OSError, qa.InvalidAssessment, subprocess.SubprocessError, TypeError, KeyError) as error:
        print("Quality producer error: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
