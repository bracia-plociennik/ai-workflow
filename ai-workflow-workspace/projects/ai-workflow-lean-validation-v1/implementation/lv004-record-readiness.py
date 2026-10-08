"""Persist the explicitly reviewed, refreshed LV004 specification gate."""
import importlib.util
from pathlib import Path

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
module = importlib.util.spec_from_file_location("assessment", project / "implementation/record-current-assessment.py")
qa = importlib.util.module_from_spec(module)
module.loader.exec_module(qa)
evidence = """- Fresh whole-spec review compares owner LV-DEC-008, accepted architecture/plan, current dependency quality and completed checkpoint with HEAD 03fb788.
- Frozen actual inventory contains 674 executed IDs, 110 lexical assertion candidates and 32 source-consumer references. Those counts are not claimed equivalence; exact semantic ownership, mutation and cleanup comparison remain implementation DoD.
- Reviewed all five slice interfaces and V4-01..09: pure common imports, disposable independent roots, all union, exact status/diagnostics, external assertions, marker/timing parents, repeat/permutation and failure cleanup.
- Existing literal consumer references require a live-validated coverage index. A disconnected comment/index cannot substitute for actual test membership. New outside-ceiling consumers require reconciliation before writes.
- Exploratory workspace group passed in isolation. A quality prototype exposed a split backup/mutation transaction at original line 4052; the boundary was corrected and retest is ongoing. Neither the failed attempt nor the pending equivalence is an implementation PASS.
- Findings-first artifact review: no unresolved specification blocker. Source implementation, actual equivalence and formal Phase 5 remain separate gates; no speed claim, push or closure.
"""
inputs = [("workflow-source", x) for x in (
    ".systems/scripts/check-validator-smoke-tests",
    ".systems/scripts/lib/validation-timing.py",
    ".systems/scripts/report-validation-comparison",
    ".systems/scripts/check-validation-completion",
    ".systems/scripts/check-validation-observability",
    ".systems/ai/core/validation-observability.md",
)]
inputs += [("owning-project-evidence", x) for x in (
    "planning/phase-2-project-plan.md",
    "specs/phase-3-lv-test-004-smoke-partition-specification.md",
    "quality/phase-5-lv-core-001-verdict-integrity-quality.md",
    "quality/phase-5-lv-obs-002-baseline-quality.md",
    "quality/phase-5-lv-val-003-scoped-selection-quality.md",
    "checkpoints/phase-7-checkpoint-2026-09-30-lv001-lv003.md",
    "implementation/lv004-reference/inventory.json",
)]
body = qa.body(evidence, [], artifact=True)
body = body.replace(
    "runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.",
    "smoke entrypoint, pure helpers, five isolated group producers, manifest ownership, source-consumer references and nine-column timing consumer."
).replace(
    "Full source/artifact review and before/after failure traces; mapped schemas, typed readers and exact check/ID coverage.",
    "Full refreshed specification, current source and dependency review; explicit assertion/equivalence requirements, CLI/timing and coverage-index field mapping. Runtime equivalence remains an implementation gate."
)
qa.record(project / "quality/recovery-phase-3-lv-test-004-smoke-partition-spec-qa.md",
          "lv004-refreshed-spec-2026-09-30", "spec-qa",
          "ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition", inputs, body)
