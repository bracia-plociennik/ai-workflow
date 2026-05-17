# AUTOPILOT_EVENTS.md

Purpose: owner-facing event log. Only record events that require attention or explain why autopilot stopped.

## Events

```yaml
- at: null
  event_type: null # high_impact_decision | critical_risk | retry_limit | stop | blocking_drift | missing_access | recovery_inconsistency | final_approval_required
  severity: null # warning | blocking | critical
  task_id: null
  phase: null
  summary: null
  owner_action_required: null
  recommendation: null
  alternative: null
  impact_if_recommendation: null
  impact_if_alternative: null
  related_artifacts: []
```
