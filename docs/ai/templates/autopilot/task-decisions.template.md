# <task-id>-decisions.md

Purpose: decision artifact for one task/package.

Every decision made during spec, implementation, QA, fix loop, distillation, checkpoint, or final check must be recorded here or in a phase-specific decision artifact.

## Decisions

```yaml
- decision-id: <TASK-ID>-D001
  phase: null
  classification: auto-resolvable # auto-resolvable | high-impact | critical-risk | blocked-by-missing-facts
  status: chosen # chosen | awaiting-owner | superseded
  chosen: recommendation # recommendation | alternative | none
  recommendation: null
  recommendation-impact: null
  alternative: null
  alternative-impact: null
  why-chosen: null
  why-rejected: null
  can-user-override-later: true
  override-impact: null
  related-artifacts: []
```

## Owner Overrides

```yaml
- owner-override: true
  at: null
  overrides-decision-id: null
  previous-choice: null
  new-choice: null
  requires:
    - re-spec
    - re-QA
  impact: null
```
