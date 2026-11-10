# <task-id>-decisions.md

Purpose: decision artifact for one task/package.

Every decision made during spec, implementation, QA, fix loop, distillation, checkpoint, or final check must be recorded here or in a phase-specific decision artifact.

## Decisions

```yaml
- decision-id: <TASK-ID>-D001
  phase: null
  classification: auto-resolvable # auto-resolvable | owner-preference | high-impact | critical-risk | blocked-by-missing-facts
  status: chosen # chosen | awaiting-owner | superseded
  disposition: agent-choice # pending | agent-choice | owner-approved
  execution-mode: <auto|human-coop>
  affected-units: []
  blocking-reason: null
  approval-reference: null
  assumption: null
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

## AFK/ZW continuation references

Use execution-modes.md. Keep unresolved owner decisions in this existing list with stable IDs, affected units/dependents, blocking reason, actual sources tried, options/recommendation, impacts and unlocked work. Existing readiness/state references runnable independent work, preparation, source owner-absence/return and resume point. Do not add AFK fields to the strict V1/V2 projection JSON or create a second queue. Owner absence grants no new permission.
