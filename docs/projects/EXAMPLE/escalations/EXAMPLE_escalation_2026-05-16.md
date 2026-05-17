# EXAMPLE_escalation_2026-05-16.md

Purpose: example escalation artifact.

```yaml
escalation:
  at: 2026-05-16
  task_id: EX-01
  phase: 4. FAZA IMPLEMENTACJI
  escalation_reason: Example critical-risk stop.
  classification: critical_risk
  workflow_effect: STOP

failed_checks:
  - Real external side effect requested in example workspace.

evidence:
  commands: []
  artifacts:
    - docs/projects/EXAMPLE/STATUS.md
  observations:
    - EXAMPLE must not perform real external actions.

suspected_cause: Example scenario.
recommended_path: Stop and request owner approval.
recommended_path_impact: Prevents unsafe execution.
alternative_path: Continue without approval.
alternative_path_impact: Violates workflow stop conditions.
risk_if_ignored: False PASS or real-world side effects.
required_owner_action: Confirm whether to proceed outside EXAMPLE.
```
