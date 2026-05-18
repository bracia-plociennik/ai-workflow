# autopilot-events.md

Purpose: owner-facing event log. Only record events that require attention or explain why autopilot stopped.

## Events

```yaml
- at: null
  event-type: null # high-impact-decision | critical-risk | retry-limit | stop | blocking-drift | missing-access | recovery-inconsistency | final-approval-required
  severity: null # warning | blocking | critical
  task-id: null
  phase: null
  summary: null
  owner-action-required: null
  recommendation: null
  alternative: null
  impact-if-recommendation: null
  impact-if-alternative: null
  related-artifacts: []
```
