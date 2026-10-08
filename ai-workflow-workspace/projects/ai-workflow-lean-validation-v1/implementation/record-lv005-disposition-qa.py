"""Persist the performed composite-plan/spec reviews; no source or historical QA edit."""
import importlib.util
from pathlib import Path

project = Path.cwd() / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
spec = importlib.util.spec_from_file_location("assessment", project / "implementation/record-current-assessment.py")
qa = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qa)

common = [
    "planning/phase-2-project-plan.md",
    "planning/lv005-deferral-plan-amendment.md",
    "architecture/phase-1-architecture.md",
    "quality/phase-1-architecture-qa.md",
    "context.md", "decisions/lv-dec-010-lv005-deferral.md",
    "reviews/lv005-deferral-plan-and-lv006-readiness-review.md",
]

def inputs(evidence, source):
    return [("owning-project-evidence", path) for path in evidence] + [
        ("workflow-source", path) for path in source
    ]

def artifact_body(evidence, scope, next_route):
    body = qa.body(evidence, [], artifact=True)
    body = body.replace(
        "Current specification coherence, scope, DoD, producer-consumer mapping and dependency interfaces; not a product implementation verdict.",
        scope,
    ).replace(
        "accepted plan/spec, source contracts and LV-DEC-008.",
        "preserved base plus approved LV-DEC-010 scope amendment, current source contracts and LV-DEC-008.",
    ).replace(
        "runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.",
        "owner decision, composite plan/spec, task index, status, current QA reader, distillation state and readiness.",
    ).replace(
        "- Spec QA result: PASS",
        "- Result: PASS",
    )
    return body + f"""
### Validation Execution Record

- Semantic QA result: aligned
- Findings/blockers: none for this artifact; deferred LV005 isolation remains unresolved and excluded
- Product checks: not-applicable, no implementation in this request
- Workflow script applicability: targeted artifact/source-identity checks after semantic review
- Targeted workflow commands: check-qa-evidence --project ai-workflow-lean-validation-v1; check-status-consistency --project ai-workflow-lean-validation-v1; check-distillation-state --project ai-workflow-lean-validation-v1
- Script evidence role: supporting-only
- Final verdict: PASS
- Verdict scope: current artifact only, never LV005/LV006 implementation acceptance

### Owner Decision Checkpoint

- Interaction mode: none
- Decision state: clear
- Material decisions: LV-DEC-010 approved
- Questions asked: none
- Auto-resolved reversible decisions: preserve immutable base and bind explicit amendment
- Optional owner refinements: future LV005 isolated-runtime recovery
- Decision artifacts: decisions/lv-dec-010-lv005-deferral.md
- Next route: {next_route}

### Optional Knowledge Capture

- Capture recommended: yes
- Target: decision-artifact
- Reason: retain owner scope disposition and downstream boundaries
- Owner decision required: no
- Owner decision: capture-now
- Privacy/scope check: pass
- Suggested entry title: LV005 deferral and included LV006 scope
- Suggested entry summary: approved scope evidence only; not a Phase 6 completion
"""

plan_path = project / "quality/recovery-phase-2-plan-qa.md"
spec_path = project / "quality/recovery-phase-3-lv-qa-006-integration-spec-qa.md"
assert not plan_path.exists() and not spec_path.exists(), "Preserve existing reviews; choose a new run ID"

plan_evidence = """- Full semantic review of all six original task contracts, architecture/context, approved amendment, plan router and task index. The original fallback explicitly allows an owner-approved disposition; no architecture interface or risk boundary changes.
- Current task graph includes accepted LV001-LV004 then LV006, with LV005 visibly deferred. No behavioral benefit, instruction promotion, completion or capture is inferred.
- Compared LV006 goal, unchanged five-path ceiling, seven DoD conditions, dependency/start/end/readiness fields and later QA/capture routes against owner intent.
- Adversarial second pass covers deferral-as-PASS, historical QA reuse, 660-versus-694 timing comparison, old baseline identities, premature source writes, hidden integration repair and automatic final closure.
- Producer-consumer audit traces decision010 to composite router/plan, six task rows, composite LV006 specification and readiness/status. Base artifacts and bound historical outcomes remain byte-identical.
- Artifact acceptance does not imply execution evidence; full implementation validation remains future LV006/final-checkpoint work.
"""
qa.record(
    plan_path, "lv-plan-owner-deferral-2026-09-30", "plan-qa",
    "ai-workflow-lean-validation-v1",
    inputs(common + ["plans.md", "tasks.md"],
           [".systems/ai/workflow/phase-2-plan-qa.md", ".systems/ai/core/full-qa-verification.md", ".systems/ai/core/plan-quality-contract.md"]),
    artifact_body(plan_evidence, "Composite project plan and explicit scope disposition; artifact QA only, not implementation quality.", "current composite LV006 Spec QA and readiness-only stop"),
)

spec_evidence = """- Read the entire original LV006 specification and current-scope amendment against accepted composite plan/current Plan QA, architecture, six task rows and decision010. Original pending authority claims are expressly superseded, not silently inherited.
- Included LV001-LV004 dependency assessments retain their exact source/input identities and complete capture records. LV005's current FAIL is preserved, owner-deferred and not used as a source prerequisite or PASS.
- Seven testable DoD conditions, original V6-01..07, data/measurement/disposition failure matrix and four-slice plan cover included integration scope. No extra source consumer or outside-ceiling correction is permitted.
- Source inspection confirms standard default, explicit full CI/updater and all-group smoke route. Current source audit records 694 IDs; historical 660-case timing baselines remain source-specific. No fresh performance or full-run result is claimed.
- Current quality/spec inputs must be checked again before writes and after source changes; missing/stale evidence routes to owning fix loop. Readiness stop is distinct from Phase 4, Phase 5 and later capture.
"""
qa.record(
    spec_path, "lv006-spec-owner-deferral-2026-09-30", "spec-qa",
    "ai-workflow-lean-validation-v1:LV-QA-006-integration",
    inputs(common + ["specs/phase-3-lv-qa-006-integration-specification.md",
                     "specs/lv006-current-scope-amendment.md", "quality/recovery-phase-2-plan-qa.md",
                     "tasks.md", "implementation/lv004-current-source-audit.json"] +
           [f"quality/phase-5-{task}-quality.md" for task in (
               "lv-core-001-verdict-integrity", "lv-obs-002-baseline",
               "lv-val-003-scoped-selection", "lv-test-004-smoke-partition")],
           [".systems/ai/workflow/phase-3-spec-qa.md", ".systems/ai/core/full-qa-verification.md",
            ".systems/scripts/validate-workflow", ".systems/scripts/update-from-upstream",
            ".systems/scripts/smoke/manifest.json", ".github/workflows/ai-workflow-validate.yml"]),
    artifact_body(spec_evidence, "Composite LV006 specification, dependency scope and readiness; no implementation verdict or behavioral evaluation grade.", "LV006 readiness-only stop, then fresh pre-write check on resume"),
)
