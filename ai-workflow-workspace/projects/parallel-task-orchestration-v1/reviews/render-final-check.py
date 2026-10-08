"""Render the supplied completed final assessment through the installed schema."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parents[2]
module = importlib.util.spec_from_file_location(
    "quality_record", ROOT / ".systems/scripts/lib/quality-record.py")
producer = importlib.util.module_from_spec(module)
module.loader.exec_module(producer)

review = (PROJECT / "reviews/pto-final-system-review.md").read_text()
if "Independent final artifact re-review: completed" not in review:
    raise SystemExit("Independent final artifact re-review not completed")

inputs = {("workflow-source", ".systems/ai/core/parallel-task-orchestration.md"),
          ("workflow-source", ".systems/ai/core/execution-efficiency.md")}
for path in sorted((PROJECT / "quality").glob("phase-5-*-quality.md")):
    metadata, sections = producer.qa.read_current(path.read_text().splitlines())
    if metadata["Verdict"] != "PASS":
        raise SystemExit("Current task Quality not accepted")
    for line in sections["Input Artifacts"]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) == 3 and cells[0] in {"workflow-source", "owning-project-evidence"}:
            inputs.add((cells[0], cells[1]))
    inputs.add(("owning-project-evidence", str(path.relative_to(PROJECT))))

for pattern in ("quality/phase-1-architecture-qa.md", "quality/phase-2-plan-qa.md",
                "quality/phase-3-*-spec-qa.md", "specs/phase-3-*-specification.md",
                "distillations/phase-6-*-distillation.md", "capture-state/*.md",
                "checkpoints/*.md", "memory/*.md"):
    for path in sorted(PROJECT.glob(pattern)):
        inputs.add(("owning-project-evidence", str(path.relative_to(PROJECT))))
for path in ("context.md", "architecture/phase-1-architecture.md",
             "planning/phase-2-project-plan.md", "tasks.md", "status.md", "memory.md",
             "change-requests.md", "decisions/owner-decisions.md",
             "decisions/implementation-approval.md",
             "decisions/pto-quality-range-approval.md",
             "decisions/pto-006-007-protocol-only-scope.md",
             "decisions/phase-8-request.md", "reviews/pto-final-system-review.md",
             "reviews/pto-final-checkpoint-closure.md",
             "autopilot/runs/autopilot-003/state.md"):
    inputs.add(("owning-project-evidence", path))

record = {
    "schema": 1, "kind": "final-check", "task": None,
    "run_id": "pto-final-check-001", "date": "2026-10-04", "verdict": "PASS",
    "inputs": [{"root": root, "path": path} for root, path in sorted(inputs)],
    "sections": {
        "Evidence": (
            "- Actual parent and independent final review: reviews/pto-final-system-review.md.\n"
            "- Current seven formal task Quality records,36AC,Phase6,capture and checkpoints reviewed.\n"
            "- Actual full007 exit0,665seconds,43checks,745IDs,fivegroups; /tmp/pto-007-full-source-001.json.\n"
            "- Final checkpoint fresh artifact closure002 exit0,complete,all4consumers; source unchanged.\n"
            "- Current ancillary handoff/repo-memory hashes recorded in reviewed evidence; no AI System/source publication claim."),
        "Review Completeness Gate": (
            "- Status: complete\n"
            "- Reviewed baseline: HEAD8a0eeef,actual approved001..007source and current final runtime inputs\n"
            "- Closure freshness: current\n- Post-fix full re-review: completed\n"
            "- Policy-boundary adversarial matrix: completed\n"
            "- Producer-consumer field audit: completed\n"
            "- Required-field mapping: complete\n- Instruction refresh: performed-full\n"
            "- Instruction baseline: current\n"
            "- Evidence: reviews/pto-final-system-review.md; current task/QA/capture/owner source chain,source scripts supporting-only."),
        "Scope Under Final Check": (
            "- Plan artifact: planning/phase-2-project-plan.md\n"
            "- Completed tasks/packages: PTO001..007,all36AC in accepted protocol-only release\n"
            "- Deferred tasks/packages: native operational verification under PTO-D06,not a completed test\n"
            "- Out-of-scope: backend executor/API,scheduler,recursive dispatch,model/native speedup,AI System implementation,Git publication"),
        "Completion Review": (
            "| Area | Result | Evidence |\n| --- | --- | --- |\n"
            "| Owner intent/architecture/plan/specs/36AC | PASS | actual final review,current artifact QA and PTO-D06 |\n"
            "| All seven included task Quality | PASS | seven current formal Phase5 records |\n"
            "| Phase6 and completed capture | PASS | seven accepted distillations/state records,derived true |\n"
            "| Final checkpoint and memory sync | PASS | checkpoints/phase-7-checkpoint-2026-10-04-pto-final.md |\n"
            "| Source/runtime freshness | PASS | full007665seconds + fresh checkpoint four consumers |\n"
            "| External Memory/privacy/scope | PASS | one portable accepted handoff,manual hash/claim review |\n"
            "| System Insights boundaries | PASS | unused,no raw client data or domain-memory promotion |\n"
            "| Blocking decisions/change requests | PASS | no open CR,current D06 approved; final closure still awaits owner |\n"
            "| Final owner approval | awaiting | no final-owner-yes granted or artifact generated |"),
        "Findings": (
            "- Blockers: none\n- Unresolved findings: none\n"
            "- Critical errors: none\n- System warnings: none in the approved release\n"
            "- Residual risk: finite offline coverage,cooperative local controls; native isolation/capacity/support unverified. No speedup or publication claim."),
        "Owner Approval": (
            "- Technical final check result: PASS\n- Owner approval required: yes\n"
            "- Owner decision: awaiting\n- Owner comments captured as change request: not-applicable"),
        "Change Request Review": (
            "| Change request | Timing | Status | Blocks final-owner-yes? | Route |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| none | pre-final-approval | none | no | owner approval or future change-request triage |"),
        "Final Gate": (
            "- Can close active plan: awaiting-owner\n"
            "- Required next phase: owner approval\n- Blocking reason: none\n"
            "- Commit/push/final-owner-yes: not authorized"),
        "Owner Decision Checkpoint": (
            "- Interaction mode: queued\n- Decision state: awaiting-owner\n"
            "- Material decisions: final-owner-yes for protocol-only release\n"
            "- Questions asked: none\n- Auto-resolved reversible decisions: canonical quality filename\n"
            "- Optional owner refinements: separately isolated native backend verification\n"
            "- Decision artifacts: decisions/phase-8-request.md; decisions/pto-006-007-protocol-only-scope.md\n"
            "- Next route: owner-final-approval,not automatic closure"),
        "Optional Knowledge Capture": (
            "- Capture recommended: no\n- Target: none\n"
            "- Reason: accepted Phase6/final checkpoint and one handoff already preserve durable knowledge\n"
            "- Owner decision required: no\n- Owner decision: not-requested\n"
            "- Privacy/scope check: pass\n"
            "- Suggested entry title: none\n- Suggested entry summary: no duplicate capture")
    }
}
output, body = producer.render(record, ROOT, PROJECT.parents[1], PROJECT.name)
producer.publish(output, body)
print(output)
