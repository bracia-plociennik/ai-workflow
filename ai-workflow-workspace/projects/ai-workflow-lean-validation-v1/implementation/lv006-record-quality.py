"""Persist the completed semantic review plus successful current full evidence."""
import importlib.util
import csv
import json
from pathlib import Path
import re
import subprocess

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
log = project / "implementation/lv006-full-2026-10-01-approved.log"
text = log.read_text()
markers = re.findall(r"^AI_WORKFLOW_VALIDATE_COMPLETE .*$", text, re.M)
assert len(markers) == 1 and "result=pass exit_code=0 " in markers[0], markers
manifest = json.loads((root / ".systems/scripts/smoke/manifest.json").read_text())
ids = re.findall(r"^AI_WORKFLOW_SMOKE_PROGRESS test=([^ ]+) status=started$", text, re.M)
assert len(ids) == len(set(ids)) == 694 and set(ids) == set(manifest["test_groups"])
with (project / "implementation/lv006-full-2026-10-01-approved.tsv").open() as stream:
    timing_rows = list(csv.DictReader(stream, delimiter="\t"))
check_count = sum(row["record_kind"] == "child" and row["parent_id"] == "validation-wall" for row in timing_rows)
subprocess.run([".systems/scripts/check-qa-evidence", "--project", project.name], check=True)
assert subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines() == [".systems/ai/core/changelog.md"]
spec = importlib.util.spec_from_file_location("assessment", project / "implementation/record-current-assessment.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)
evidence = """- Explicit high-risk authority: LV-DEC-008, current resume and composite LV006 scope; LV005 remains excluded under LV-DEC-010.
- Reviewed the complete current changelog diff, included source interfaces, immutable baseline/partition evidence, latest input-bound QA and current composite plan/spec before the supporting full run.
- Producer-consumer and adversarial review: reviews/lv006-integration-review.md; local real-reader/policy probes: implementation/lv006-integration-probes.json.
- Ten probes succeeded with intended statuses and diagnostics, including safe/direct/compound policy, missing source, unequal synthetic comparison, invalid CLI and structural-only coverage check.
- Full 2026-10-01 approved run completed with forty top-level checks, 694 unique current IDs and exactly one parent completion; log and versioned timing are attached as supporting evidence.
- Earlier sandbox full failed before any smoke child because ps was unavailable; failure log remains immutable. Escalated local verification used the existing cleanup preflight, not a weakened test.
- Manual full trace: public full -> validators -> all owned groups -> exact executed ledger -> one suite marker -> one parent marker. CI/updater still invoke explicit full.
- Comparison trace: three source-bound historical 660-test baselines validate as baselines; current 694-test population differs. Unequal synthetic populations are rejected by the real comparison CLI. No speed improvement or model behavior claim.
- Source writes are changelog-only, within the accepted five-path ceiling. No counterpart edit, network/model payload, global configuration, push or final-owner approval.
"""
dod = [
    ("Included dependency/current source coherence", "Current reader validates LV001-LV004 and composite LV006 Spec QA; original sources unchanged outside changelog."),
    ("Full/CI/updater exact coverage", "Current full executes 694 unique manifest-owned IDs; CI/updater explicit full unchanged."),
    ("Honest measurement", "Original three-run 660-test baseline preserved; changed population explicitly ineligible for speed comparison; real CLI rejects mismatch."),
    ("Explicit deferred LV005", "Decision010, composite plan/spec and deferred false-distilled record; original failed runtime evidence preserved."),
    ("Semantic review before full", "Whole current diff, intent/DoD, producer-consumer/adversarial and manual failure traces recorded before supporting run."),
    ("Single privacy-safe handoff and no counterpart writes", "Existing one handoff contains accepted LV001-LV004 only; LV006 extends it only through authorized Phase 6 after this gate."),
    ("Distinct capture and final authority", "LV-DEC-008 authorizes separate Phase 6/local source commit/final checkpoint and owner-triggered Phase 8; no push/final-owner-yes."),
]
body = qa.body(evidence, dod).replace(
    "runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.",
    "composite plan/spec, current QA reader, smoke manifest/ledger, full/CI/updater, comparison schema, capture and handoff routes."
).replace("- Post-fix full re-review: completed", "- Post-fix full re-review: not-required")
body = body.replace("forty top-level checks", str(check_count) + " top-level checks")
body += """
### Validation Execution Record

- Semantic QA result: aligned
- Findings/blockers: none in included LV006 integration scope
- Product checks: not-applicable; workflow integration docs/source interfaces, no application implementation
- Workflow script applicability: full-required, shared system integration
- Targeted workflow commands: real CLI/policy probes; current QA reader; manifest structural verification
- Script evidence role: supporting-only
- Final verdict: PASS
- Verdict scope: LV006 only; never acceptance of deferred LV005 or final-owner-yes

### Owner Decision Checkpoint

- Interaction mode: autopilot-non-interactive
- Decision state: clear
- Material decisions: LV-DEC-008/010 resolved
- Questions asked: none
- Auto-resolved reversible decisions: changelog-only documentation needed; other ceiling files already accurate
- Optional owner refinements: future LV005 runtime recovery
- Decision artifacts: decisions/lv-decisions.md; decisions/lv-dec-010-lv005-deferral.md
- Next route: authorized Phase 6/local commit and final Phase 7

### Optional Knowledge Capture

- Capture recommended: yes
- Target: project-memory
- Reason: preserve integration, honest measurement and scope disposition
- Owner decision required: no additional approval; LV-DEC-008
- Owner decision: capture-now
- Privacy/scope check: pass
- Suggested entry title: Included lean-validation integration
- Suggested entry summary: exact coverage, current source and unchanged deferred behavioral scope
"""
source = [".systems/ai/core/changelog.md", ".systems/scripts/validate-workflow", ".systems/scripts/check-validator-smoke-tests",
          ".systems/scripts/smoke/manifest.json", ".systems/scripts/report-validation-comparison",
          ".systems/scripts/update-from-upstream", ".github/workflows/ai-workflow-validate.yml",
          ".systems/scripts/lib/validation-scope.py", ".systems/scripts/lib/qa-evidence.py"]
inputs = ["planning/phase-2-project-plan.md", "planning/lv005-deferral-plan-amendment.md",
          "specs/phase-3-lv-qa-006-integration-specification.md", "specs/lv006-current-scope-amendment.md",
          "quality/recovery-phase-2-plan-qa.md", "quality/recovery-phase-3-lv-qa-006-integration-spec-qa.md",
          "reviews/lv006-integration-review.md", "implementation/lv006-integration-probes.json",
          "implementation/lv006-full-2026-10-01-approved.log", "implementation/lv006-full-2026-10-01-approved.tsv"]
target = project / "quality/phase-5-lv-qa-006-integration-quality.md"
assert not target.exists(), "Preserve existing assessment; choose a reviewed new run"
qa.record(target, "lv006-quality-2026-10-01", "implementation-quality",
          project.name + ":LV-QA-006-integration",
          [("workflow-source", p) for p in source] + [("owning-project-evidence", p) for p in inputs], body)
target.write_text(target.read_text().replace("- Date: 2026-09-30", "- Date: 2026-10-01", 1))
print(markers[0])
