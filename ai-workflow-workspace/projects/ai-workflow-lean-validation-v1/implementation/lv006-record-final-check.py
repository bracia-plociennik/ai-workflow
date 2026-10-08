"""Record the separately owner-triggered final check after actual checkpoint review."""
import importlib.util
from pathlib import Path
import subprocess
import sys

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
spec = importlib.util.spec_from_file_location("assessment", project / "implementation/record-current-assessment.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
checkpoint = project / "checkpoints/phase-7-checkpoint-2026-10-01-final.md"
assert "- Result: PASS" in checkpoint.read_text()
assert "- Distillations processed atomically: yes" in checkpoint.read_text()
assert "- Can continue project workflow: yes" in checkpoint.read_text()
assert "Semantic final re-review: completed" in (project / "reviews/lv006-final-checkpoint-review.md").read_text()
assert subprocess.check_output(["git", "status", "--porcelain"], text=True) == ""
assert subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip() == "0c767da"
for task in ("lv-core-001-verdict-integrity", "lv-obs-002-baseline", "lv-val-003-scoped-selection",
             "lv-test-004-smoke-partition", "lv-qa-006-integration"):
    assert "- State: completed" in (project / "capture-state" / (task + ".md")).read_text()
    assert "- memory-in-repo-memory: true" in (project / "distillations" / ("phase-6-" + task + "-distillation.md")).read_text()
assert "- State: deferred" in (project / "capture-state/lv-ux-005-instruction-efficiency.md").read_text()
assert "- is_distilled derived value: false" in (project / "capture-state/lv-ux-005-instruction-efficiency.md").read_text()

inputs = [("workflow-source", ".systems/ai/core/changelog.md")]
for relative in ("architecture/phase-1-architecture.md", "planning/phase-2-project-plan.md",
                 "planning/lv005-deferral-plan-amendment.md", "plans.md", "tasks.md", "change-requests.md",
                 "decisions/lv-decisions.md", "decisions/lv-dec-010-lv005-deferral.md",
                 "quality/recovery-phase-2-plan-qa.md",
                 "quality/recovery-phase-3-lv-qa-006-integration-spec-qa.md",
                 "checkpoints/phase-7-checkpoint-2026-10-01-final.md", "memory.md",
                 "memory/2026-10-01-included-scope-final-checkpoint.md", "reviews/lv006-final-checkpoint-review.md",
                 "implementation/lv006-checkpoint-full-2026-10-01.log",
                 "implementation/lv006-checkpoint-full-2026-10-01.tsv"):
    inputs.append(("owning-project-evidence", relative))
for task in ("lv-core-001-verdict-integrity", "lv-obs-002-baseline", "lv-val-003-scoped-selection",
             "lv-test-004-smoke-partition", "lv-qa-006-integration"):
    for relative in ("quality/phase-5-" + task + "-quality.md",
                     "distillations/phase-6-" + task + "-distillation.md",
                     "capture-state/" + task + ".md"):
        inputs.append(("owning-project-evidence", relative))
inputs.append(("owning-project-evidence", "capture-state/lv-ux-005-instruction-efficiency.md"))
body = """### Evidence

- Separately owner-triggered under LV-DEC-008 after implementation-range stopped at completed Phase 7.
- Current task, composite plan/spec, included source-bound quality, accepted capture, memory, decisions and no-change-request index reviewed. Historical FAIL and scope-deferral evidence are retained.
- Current full checkpoint log/typed timing execute all 694 IDs once with a single pass completion. Scripts support the semantic review; no baseline speed improvement asserted.
- Local source HEAD 0c767da is clean. Source commit, privacy-safe single External Memory handoff and repo memory were inspected; no counterpart modification or push.

""" + qa.completeness("reviews/lv006-final-checkpoint-review.md; whole current source/artifact, producer-consumer and authority audit.") + """
### Scope Under Final Check

- Plan artifact: preserved planning/phase-2-project-plan.md plus approved planning/lv005-deferral-plan-amendment.md.
- Completed tasks: LV001-LV004 and LV006.
- Deferred tasks: LV005 under LV-DEC-010; failed runtime isolation remains unresolved and undistilled.
- Out-of-scope: model runtime recovery, behavioral promotion, remote CI/push, counterpart implementation and final-owner-yes.

### Completion Review

| Area | Result | Evidence |
| --- | --- | --- |
| All in-scope tasks completed or explicitly deferred | PASS | tasks.md, composite plan, LV-DEC-010 |
| Current implementation Quality exists for completed tasks | PASS | five individually bound Phase 5 current assessments |
| Accepted Phase 6 and completed capture | PASS | five distillations/states; LV005 deferred false |
| Required final checkpoint complete | PASS | phase-7-checkpoint-2026-10-01-final.md, fresh full and targeted consistency |
| Repo, project memory and status consistent | PASS | local 0c767da; scoped final review of both routers and entries |
| External Memory consistent and privacy-safe | PASS | one 2026-09-29-lean-validation-ai-system-handoff.md, accepted included scope only |
| System Insights privacy/scope | PASS | none written; system-specific facts stay in proper memory |
| No unresolved blocking decision in included scope | PASS | LV-DEC-008/010; final closure approval separately awaiting |
| No open blocking change request | PASS | change-requests.md has none |

### Findings

- Blockers: none
- Unresolved findings: none
- Finding scope: included technical scope only; deferred LV005 is explicitly excluded, not resolved
- Critical errors: none found
- Warnings: none in included technical scope; explicit LV005 deferral does not resolve its excluded runtime finding.
- Residual risk: remote Linux CI unrun, no paired current full speed comparison, no claim of absolute defect absence or counterpart adoption.

### Owner Approval

- Technical final check result: PASS
- Owner approval required: yes
- Owner decision: awaiting
- Owner comments captured as change request: not-applicable; none currently submitted

### Change Request Review

| Change request | Timing | Status | Blocks final-owner-yes? | Route |
| --- | --- | --- | --- | --- |
| none | pre-final-approval | none | no | await owner decision; later comments use change-request triage |

### Final Gate

- Can close active plan: awaiting-owner
- Required next phase: owner-final-approval
- Blocking reason: final-owner-yes not given

### Gate Decision

- Result: PASS
- Can proceed: yes
- Scope: technical final-check assessment only; plan remains active, owner closure and push not inferred.

## Owner Decision Checkpoint

- Interaction mode: queued
- Decision state: awaiting-owner
- Material decisions: final-owner-yes for included scope with deferred LV005
- Questions asked: none
- Auto-resolved reversible decisions: none
- Optional owner refinements: separately restart LV005 through its original gates
- Decision artifacts: decisions/lv-decisions.md; decisions/lv-dec-010-lv005-deferral.md
- Next route: owner-final-approval or change-request triage

## Optional Knowledge Capture

- Capture recommended: no
- Target: none
- Reason: accepted Phase 6 and final Phase 7 already synchronized useful knowledge
- Owner decision required: no new capture decision
- Owner decision: not-requested
- Privacy/scope check: pass
- Suggested entry title: none
- Suggested entry summary: no duplicate capture
"""
path = project / "quality/phase-8-final-check.md"
suffix = "-" + sys.argv[1] if len(sys.argv) > 1 else ""
run = "lv-final-check-included-2026-10-01" + suffix
assert not path.exists() or "- Run ID: " + run not in path.read_text(), "Run IDs must remain unique."
qa.record(path, run, "final-check", project.name, inputs, body)
text = path.read_text().replace("- Date: 2026-09-30", "- Date: 2026-10-01").replace(
    "- Result: PASS\n- QA verification contract", "- Result: awaiting-owner-final-yes\n- QA verification contract")
path.write_text(text)
print("Recorded technical final check; final-owner-yes remains awaiting.")
