# example-escalation-2026-05-16.md

Purpose: example escalation artifact.

```yaml
escalation:
  at: 2026-05-16
  task-id: EX-01
  phase: 4. FAZA IMPLEMENTACJI
  escalation-reason: Example critical-risk stop.
  classification: critical-risk
  workflow-effect: STOP

failed-checks:
  - Real external side effect requested in example workspace.

evidence:
  commands: []
  artifacts:
    - docs/projects/EXAMPLE/status.md
  observations:
    - EXAMPLE must not perform real external actions.

suspected-cause: Example scenario.
recommended-path: Stop and request owner approval.
recommended-path-impact: Prevents unsafe execution.
alternative-path: Continue without approval.
alternative-path-impact: Violates workflow stop conditions.
risk-if-ignored: False PASS or real-world side effects.
required-owner-action: Confirm whether to proceed outside EXAMPLE.
```
