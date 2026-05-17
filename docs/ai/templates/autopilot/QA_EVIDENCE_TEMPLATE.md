# <phase_task_name>_quality.md

Purpose: standard evidence artifact for SPEC QA, QUALITY, final check, or other PASS/FAIL gates. Store project-specific copies under `docs/projects/<project>/quality/`.

## Result

```yaml
phase: null
task_id: null
result: null # PASS | FAIL
date: null
artifact_under_review: null
```

## Evidence

```yaml
commands:
  - command: null
    result: null
    notes: null

manual_checks:
  - check: null
    result: null
    notes: null

artifacts_reviewed: []
```

## Findings

```yaml
critical_errors: []
warnings: []
residual_risk: []
skipped_checks:
  - check: null
    reason: null
    affects_pass: true
```

## Gate Decision

```yaml
all_dod_satisfied: false
no_known_bug_in_scope: false
no_regression_in_changed_paths: false
edge_cases_covered_or_rejected: false
explicit_evidence_attached: false
can_proceed: false
```
