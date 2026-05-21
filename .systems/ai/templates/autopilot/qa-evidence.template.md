# <task-id>-quality.md

Purpose: standard evidence artifact for SPEC QA, QUALITY, final check, or other PASS/FAIL gates. Store project-specific copies under `workspace/projects/<project>/quality/`.

## Result

```yaml
phase: null
task-id: null
result: null # PASS | FAIL
date: null
artifact-under-review: null
```

## Evidence

```yaml
commands:
  - command: null
    result: null
    notes: null

manual-checks:
  - check: null
    result: null
    notes: null

artifacts-reviewed: []
```

## Findings

```yaml
critical-errors: []
warnings: []
residual-risk: []
skipped-checks:
  - check: null
    reason: null
    affects-pass: true
```

## Gate Decision

```yaml
all-dod-satisfied: false
no-known-bug-in-scope: false
no-regression-in-changed-paths: false
edge-cases-covered-or-rejected: false
explicit-evidence-attached: false
can-proceed: false
```
