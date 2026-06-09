# events.md

Purpose: owner-facing event log. Only record events that require attention or explain why autopilot stopped.

## Events

```yaml
- at: null
  event-type: null # readiness-blocked | owner-readiness-required | high-impact-decision | critical-risk | retry-limit | stop | blocking-drift | missing-access | recovery-inconsistency | final-approval-required
  severity: null # warning | blocking | critical
  range: null # planning-range | implementation-range | n/a
  task-id: null
  phase: null
  readiness-artifact: null
  readiness-result: null # blocked | awaiting-owner | ready | superseded | n/a
  summary: null
  owner-action-required: null
  stop-condition: null
  recommendation: null
  alternative: null
  impact-if-recommendation: null
  impact-if-alternative: null
  related-artifacts: []
```
