"""Publish reviewed expanded technical Phase8, without owner approval."""
import importlib.util
from pathlib import Path
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parents[1]
R = P.parents[2]
spec = importlib.util.spec_from_file_location("producer", R / ".systems/scripts/lib/quality-record.py")
q = importlib.util.module_from_spec(spec)
spec.loader.exec_module(q)
review_path = "reviews/pto-008-009-final-system-review.md"
if "Independent final artifact re-review: completed" not in (P / review_path).read_text():
    raise SystemExit("current independent artifact review is required")

inputs = set()
qualities = sorted((P / "quality").glob("phase-5-*-quality.md"))
if len(qualities) != 9:
    raise SystemExit("nine actual task Quality records required")
for path in qualities:
    q.qa.assess(path, R, P.parents[1], P.name, require_pass=True)
    _, sections = q.qa.read_current(path.read_text().splitlines())
    for kind, relative, _ in q.qa.input_rows(sections["Input Artifacts"]):
        inputs.add((kind, relative))
    inputs.add(("owning-project-evidence", str(path.relative_to(P))))

distillations = sorted((P / "distillations").glob("phase-6-*-distillation.md"))
if len(distillations) != 9 or any("- memory-in-repo-memory: true" not in path.read_text()
                                for path in distillations):
    raise SystemExit("nine accepted synchronized Phase6 records required")
for pattern in ("quality/phase-1-architecture-qa.md", "quality/phase-2-plan-qa.md",
                "quality/phase-3-*-spec-qa.md", "specs/phase-3-*-specification.md",
                "distillations/phase-6-*-distillation.md", "capture-state/*.md",
                "checkpoints/*.md", "memory/*.md", "change-requests/*.md",
                "decisions/pto-008-009-implementation-approval.md",
                "decisions/pto-capability-scope-extension.md",
                "decisions/phase-8-pre-cr-history-storage.md"):
    for path in sorted(P.glob(pattern)):
        inputs.add(("owning-project-evidence", str(path.relative_to(P))))
for relative in ("context.md", "architecture/phase-1-architecture.md",
                 "architecture/pre-final-capture-and-commit-delta.md",
                 "planning/phase-2-project-plan.md", "tasks.md", "status.md", "memory.md",
                 "change-requests.md", "quality-assessments.json",
                 "quality/recovery-phase-8-final-check.md",
                 "decisions/owner-decisions.md", "decisions/implementation-approval.md",
                 "decisions/pto-quality-range-approval.md",
                 "decisions/pto-006-007-protocol-only-scope.md",
                 "decisions/phase-8-request.md", review_path,
                 "autopilot/runs/autopilot-005/state.md"):
    inputs.add(("owning-project-evidence", relative))

record = {
    "schema": 1, "kind": "final-check", "task": None,
    "run_id": "pto-expanded-final-check-001", "date": "2026-10-04", "verdict": "PASS",
    "inputs": [{"root": root, "path": path} for root, path in sorted(inputs)],
    "sections": {
        "Evidence": (
            "- Actual current parent and independent final review: " + review_path + ".\n"
            "- Nine current formal task Quality records,49AC,accepted Phase6 and synchronized capture/checkpoints.\n"
            "- Source full002 exit0,685seconds,44checks,757IDs,fivegroups; /tmp/pto-009-full-source-002.json.\n"
            "- Pre-final checkpoint closure002 exit0,complete,all four consumers; source unchanged.\n"
            "- Fresh final artifact closure is required after this report/status, never inferred from prior runtime fingerprint.\n"
            "- Original seven-task Phase8 retained byte-for-byte as registered superseded recovery report."),
        "Review Completeness Gate": (
            "- Status: complete\n- Reviewed baseline: HEAD8a0eeef,approved PTO001..009 source and current owned inputs\n"
            "- Closure freshness: current\n- Post-fix full re-review: completed\n"
            "- Policy-boundary adversarial matrix: completed\n- Producer-consumer field audit: completed\n"
            "- Required-field mapping: complete\n- Instruction refresh: performed-full\n"
            "- Instruction baseline: current\n- Automated evidence role: supporting-only\n"
            "- Evidence: " + review_path + "; source/adversarial tests and real current task gates."),
        "Scope Under Final Check": (
            "- Plan artifact: planning/phase-2-project-plan.md\n"
            "- Completed tasks/packages: PTO001..009,49AC within accepted protocol-only release and PTO-D08/D09 additions\n"
            "- Deferred tasks/packages: native operational verification under PTO-D06,not a completed test\n"
            "- Out-of-scope: scheduler,backend executor/API,model/native speedup,target/AI System implementation,Git publication"),
        "Completion Review": (
            "| Area | Result | Evidence |\n| --- | --- | --- |\n"
            "| Owner intent/architecture/plan/spec/49AC | PASS | actual final review,current artifact QA,PTO-D06/D08/D09 |\n"
            "| Nine implementation Quality records | PASS | current formal Phase5 and preserved original runs |\n"
            "| Phase6 and capture | PASS | nine accepted distillations,completed states,derived true |\n"
            "| Checkpoint and memory sync | PASS | checkpoints/phase-7-checkpoint-2026-10-04-pto-008-009.md |\n"
            "| Source/runtime freshness | PASS | authenticated full002 and actual fresh four-consumer closure |\n"
            "| Historical integrity | PASS | registered recovery Phase8 SHA4896697ce908,unchanged bytes |\n"
            "| Memory/privacy and existing handoff | PASS | concise owned facts; existing001..007 handoff unchanged |\n"
            "| Added-scope counterpart impact | awaiting | publication-only under PTO-D08; no commit/handoff requested |\n"
            "| Change requests | PASS | CR001/002 implemented and reviewed through required technical closure |\n"
            "| Final owner approval | awaiting | no final-owner-yes artifact or closure claim |"),
        "Findings": (
            "- Blockers: none\n- Finding scope: approved technical scope, publication decisions excluded\n- Unresolved findings: none\n"
            "- Critical errors: none\n- System warnings: native backend remains unverified by design\n"
            "- Residual risk: finite offline coverage,cooperative local controls; native isolation/capacity unverified. "
            "Unsupported binding needs fresh QA. Added-scope publication awaits separate owner decisions."),
        "Owner Approval": (
            "- Technical final check result: PASS\n- Owner approval required: yes\n"
            "- Owner decision: awaiting\n- Owner comments captured as change request: CR001/002 resolved technically"),
        "Change Request Review": (
            "| Change request | Timing | Status | Blocks final-owner-yes? | Route |\n"
            "| --- | --- | --- | --- | --- |\n"
            "| PTO-CR-001-capture-parity | pre-final-approval | done | no | included technical closure; owner approval separate |\n"
            "| PTO-CR-002-phase-commits | pre-final-approval | done | no | included technical closure; publication decision separate |"),
        "Final Gate": (
            "- Can close active plan: awaiting-owner\n- Required next phase: owner approval\n"
            "- Blocking reason: none for technical scope; counterpart impact blocks later commit/handoff\n"
            "- Commit/push/final-owner-yes: not authorized"),
        "Owner Decision Checkpoint": (
            "- Interaction mode: queued\n- Decision state: awaiting-owner\n"
            "- Material decisions: final-owner-yes; counterpart impact before any commit/handoff\n"
            "- Questions asked: none\n- Auto-resolved reversible decisions: history-preserving canonical filename\n"
            "- Optional owner refinements: separately isolated native verification\n"
            "- Decision artifacts: decisions/pto-008-009-implementation-approval.md; decisions/phase-8-request.md\n"
            "- Next route: owner-final-approval,not automatic project closure or publication"),
        "Optional Knowledge Capture": (
            "- Capture recommended: no\n- Target: none\n"
            "- Reason: Phase6 and checkpoint already preserve current technical facts\n"
            "- Owner decision required: no\n- Owner decision: not-requested\n"
            "- Privacy/scope check: pass\n- Suggested entry title: none\n"
            "- Suggested entry summary: no duplicate or unapproved counterpart handoff")
    }
}
output, body = q.render(record, R, P.parents[1], P.name)
q.publish(output, body)
print(output)
