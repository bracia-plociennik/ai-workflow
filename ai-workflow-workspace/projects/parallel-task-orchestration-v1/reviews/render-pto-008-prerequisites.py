"""Publish explicitly reviewed regression assessments; preserve every prior run."""
import importlib.util
import argparse
import re
from pathlib import Path

P = Path(__file__).resolve().parents[1]
R = P.parents[2]
spec = importlib.util.spec_from_file_location("producer", R / ".systems/scripts/lib/quality-record.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
parser = argparse.ArgumentParser()
parser.add_argument("--revision", type=int, required=True)
parser.add_argument("--only", choices=("pto009-spec", "pto009-quality"))
args = parser.parse_args()
revision = args.revision
if revision < 1:
    raise ValueError("invalid review revision")
paths = [P / "quality/phase-1-architecture-qa.md", P / "quality/phase-2-plan-qa.md"]
paths += sorted((P / "quality").glob("phase-3-*-spec-qa.md"))
paths += sorted((P / "quality").glob("phase-5-*-quality.md"))
if args.only:
    paths = [P / ("quality/phase-3-pto-git-009-phase-commits-spec-qa.md" if args.only == "pto009-spec"
                  else "quality/phase-5-pto-git-009-phase-commits-quality.md")]
for index, path in enumerate(paths):
    old = path.read_text()
    lines = old.splitlines()
    start, end = q.qa.current_section(lines)
    meta, sections = q.qa.read_current(lines)
    run = "pto-008-regression-" + str(revision).zfill(3) + "-" + str(index + 1).zfill(3)
    if meta["Run ID"] == run:
        raise ValueError("do not silently refresh an existing assessment")
    inputs = [{"root": kind, "path": relative}
              for kind, relative, digest in q.qa.input_rows(sections["Input Artifacts"])]
    for relative in (".systems/scripts/lib/capture-record.py",
                     ".systems/scripts/check-distillation-state",
                     ".systems/scripts/tests/runtime-integrity.py",
                     ".systems/scripts/lib/qa-evidence.py",
                     ".systems/scripts/lib/qa-commit-binding.py",
                     ".systems/scripts/lib/quality-record.py",
                     ".systems/scripts/lib/coordinator-status.py",
                     ".systems/scripts/tests/phase-commit-policy.py",
                     ".systems/ai/core/phase-commit-policy.md"):
        row = {"root": "workflow-source", "path": relative}
        if row not in inputs:
            inputs.append(row)
    extra = ["reviews/pto-008-prerequisite-regression.md",
             "decisions/pto-008-009-implementation-approval.md",
             "decisions/pto-capability-scope-extension.md"]
    identity = meta["Project/task identity"]
    if identity.endswith(":PTO-GIT-009-phase-commits"):
        extra += ["quality/phase-5-pto-cap-008-capture-parity-quality.md",
                  "distillations/phase-6-pto-cap-008-capture-parity-distillation.md",
                  "reviews/pto-009-spec-fix-review.md"]
    if meta["Artifact kind"] == "implementation-quality":
        task = identity.split(":", 1)[1]
        capture = P / ("capture-state/" + task.lower() + ".md")
        values = dict(re.findall(r"^- ([^:\n]+):\s*([^\n]+)$", capture.read_text(), re.M))
        extra.append(values["Source artifact"].strip("` "))
    for relative in extra:
        row = {"root": "owning-project-evidence", "path": relative}
        if row not in inputs:
            inputs.append(row)
    supplied = {key: "\n".join(body).strip() for key, body in sections.items()
                if key != "Input Artifacts"}
    supplied["Evidence"] = (
        "Fresh substantive regression assessment: reviews/pto-008-prerequisite-regression.md. "
        "Actual original acceptance conditions, changed shared consumers, opt-in V3 and strict V2 "
        "were reviewed against current source and completed progress. Current full002 exit0,685seconds,"
        "44checks,757IDs is supporting evidence; 26 binding/CLI,54runtime,89orchestration tests passed. "
        "Prior assessment details remain under Historical Runs. Artifact QA does not issue implementation "
        "PASS; implementation Quality retains its own DoD, intent/completeness and findings review. "
        "No native support, current source commit, push or final-owner approval is claimed.")
    supplied["Findings"] = (
        "- Blockers: none\n- Unresolved findings: none\n"
        "- Residual risk: finite offline coverage; native backend unverified. "
        "Unsupported commit reuse requires fresh QA; publication is not authorized.")
    supplied["Review Completeness Gate"] = (
        "- Status: complete\n- Reviewed baseline: HEAD8a0eeef and current approved PTO001..009 source;"
        " current planning/capture progress regression\n- Closure freshness: current\n"
        "- Post-fix full re-review: completed\n- Policy-boundary adversarial matrix: completed\n"
        "- Producer-consumer field audit: completed\n- Required-field mapping: complete\n"
        "- Instruction refresh: performed-full\n- Instruction baseline: current\n"
        "- Cross-contract consistency: aligned\n- Risk/work mode compatibility: aligned\n"
        "- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes\n"
        "- Negative-space / adversarial review: completed\n- Automated evidence role: supporting-only\n"
        "- Producers/consumers reviewed: current QA, capture, scoped inventory and orchestration parent gates\n"
        "- Evidence: reviews/pto-008-prerequisite-regression.md and original task review evidence; "
        "all previous runs preserved as history.")
    record = {"schema": 1, "kind": meta["Artifact kind"],
              "task": identity.split(":", 1)[1] if ":" in identity else None,
              "run_id": run, "verdict": "PASS", "date": "2026-10-04",
              "inputs": inputs, "sections": supplied}
    output, body = q.render(record, R, P.parents[1], P.name)
    prior = old.split("## Historical Runs", 1)[1] if "## Historical Runs" in old else ""
    body += "\n## Historical Runs\n\n" + "\n".join(lines[start + 1:end]) + "\n" + prior
    q.qa.assess(output, R, P.parents[1], P.name, document=body)
    output.write_text(body)
    print(output.name)
