# <phase_task_name>_decisions.md

Purpose: decision artifact for one task/package.

Every decision made during spec, implementation, QA, fix loop, distillation, checkpoint, or final check must be recorded here or in a phase-specific decision artifact.

## Decisions

```yaml
- decision_id: <TASK-ID>-D001
  phase: null
  classification: auto-resolvable # auto-resolvable | high-impact | critical-risk | blocked-by-missing-facts
  status: chosen # chosen | awaiting_owner | superseded
  chosen: recommendation # recommendation | alternative | none
  recommendation: null
  recommendation_impact: null
  alternative: null
  alternative_impact: null
  why_chosen: null
  why_rejected: null
  can_user_override_later: true
  override_impact: null
  related_artifacts: []
```

## Owner Overrides

```yaml
- owner_override: true
  at: null
  overrides_decision_id: null
  previous_choice: null
  new_choice: null
  requires:
    - re-spec
    - re-QA
  impact: null
```
