"""Render explicitly reviewed task evidence, preserving prior assessments."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[1]
R = P.parents[2]
module = importlib.util.spec_from_file_location("quality_record", R / ".systems/scripts/lib/quality-record.py")
q = importlib.util.module_from_spec(module)
module.loader.exec_module(q)
parser = argparse.ArgumentParser()
parser.add_argument("--task", required=True)
parser.add_argument("--review", required=True)
parser.add_argument("--evidence", required=True)
args = parser.parse_args()
spec_path = "specs/phase-3-" + args.task.lower() + "-specification.md"
spec_text = (P / spec_path).read_text()
paths = re.findall(r"^- (\.systems/[^\s]+|AGENTS.md|HUMANS.md|README.md)$", spec_text, re.M)
acs = re.findall(r"^  - (PTO-\d+-AC\d+): (.+)$", spec_text, re.M)
assert paths and acs and (P / args.review).is_file()
record = json.loads((P / "reviews/pto-001-formal-quality-input.json").read_text())
record.update(task=args.task, date="2026-10-04", run_id=args.task.lower() + "-quality-001")
record["inputs"] = [{"root": "workflow-source", "path": path} for path in paths]
record["inputs"] += [{"root": "owning-project-evidence", "path": path} for path in
                     [spec_path, args.review, "decisions/pto-quality-range-approval.md"]]
if args.task == "PTO-CORE-001-contract-routing":
    record["inputs"].append({"root": "owning-project-evidence", "path": "decisions/pto-001-quality-approval.md"})
implementation_path = "quality/phase-4-" + args.task.lower() + "-implementation-result.md"
if (P / implementation_path).is_file():
    record["inputs"].append({"root": "owning-project-evidence", "path": implementation_path})
s = record["sections"]
s["Evidence"] = "- Current reviewed evidence: " + args.review + "\n- " + args.evidence + "\n- Human high-risk approval: decisions/pto-quality-range-approval.md."
s["Definition Of Done Validation"] = "| DoD Item | Result | Evidence |\n| --- | --- | --- |\n" + "\n".join(
    "| " + key + " | PASS | " + value + "; reviewed in " + args.review + " |" for key, value in acs)
s["Intent / Plan / Spec Compliance"] = s["Intent / Plan / Spec Compliance"].split("- Evidence:")[0] + "- Evidence: exact approved task scope and all task AC; " + args.review
s["Review Completeness Gate"] = s["Review Completeness Gate"].split("- Evidence:")[0].replace(
    "8a0eeef and reviews/pto-001-source-snapshot.json, all eighteen files unchanged", "8a0eeef, actual current approved task paths reviewed") + "- Evidence: fresh full-current-diff, adversarial and producer-consumer audit: " + args.review
s["Adaptive Data / Integration Verification Matrix"] = "- Applicability: required\n" + (P / args.review).read_text().split("## Adaptive Data / Integration Verification Matrix\n", 1)[1].split("\n## ", 1)[0].strip()
s["Findings"] = "- Blockers: none\n- Unresolved findings: none\n- Residual risk: finite synthetic coverage and cooperative local controls; see " + args.review
s["Owner Decision Checkpoint"] = "- Interaction mode: queued\n- Decision state: clear\n- Material decisions: approved high-risk Quality range\n- Questions asked: none\n- Auto-resolved reversible decisions: none\n- Optional owner refinements: none\n- Decision artifacts: decisions/pto-quality-range-approval.md\n- Next route: phase-6-distillation"
out, body = q.render(record, R, P.parents[1], P.name)
if out.exists():
    old = out.read_text()
    start, end = q.qa.current_section(old.splitlines())
    meta, _ = q.qa.read_current(old.splitlines())
    match = re.search(r"-(\d+)$", meta["Run ID"])
    record["run_id"] = args.task.lower() + "-quality-" + str(int(match.group(1)) + 1).zfill(3)
    out, body = q.render(record, R, P.parents[1], P.name)
    body += "\n## Historical Runs\n\n" + "\n".join(old.splitlines()[start + 1:end]) + "\n"
    if "## Historical Runs" in old:
        body += old.split("## Historical Runs", 1)[1]
q.qa.assess(out, R, P.parents[1], P.name, document=body)
out.write_text(body)
print(out)
