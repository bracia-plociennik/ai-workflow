# <task_or_workspace>_escalation_<YYYY-MM-DD>.md

Purpose: required artifact when autopilot cannot safely continue. Store project-specific copies under `docs/projects/<project>/escalations/`.

```yaml
escalation:
  at: null
  task_id: null
  phase: null
  escalation_reason: null
  classification: null # retry_limit | critical_risk | blocking_drift | recovery_inconsistency | missing_access | unresolved_high_impact_decision | budget_exceeded
  workflow_effect: STOP

failed_checks: []

evidence:
  commands: []
  artifacts: []
  observations: []

suspected_cause: null
recommended_path: null
recommended_path_impact: null
alternative_path: null
alternative_path_impact: null
risk_if_ignored: null
required_owner_action: null
```
