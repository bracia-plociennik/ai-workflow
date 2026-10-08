# <task-or-workspace>-escalation-<YYYY-MM-DD>.md

Purpose: required artifact when autopilot cannot safely continue. Store project-specific copies under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/escalations/`.

```yaml
escalation:
  at: null
  task-id: null
  phase: null
  escalation-reason: null
  classification: null # retry-limit | critical-risk | blocking-drift | recovery-inconsistency | missing-access | unresolved-owner-preference | unresolved-high-impact-decision | budget-exceeded
  workflow-effect: STOP

failed-checks: []

evidence:
  commands: []
  artifacts: []
  observations: []

suspected-cause: null
recommended-path: null
recommended-path-impact: null
alternative-path: null
alternative-path-impact: null
risk-if-ignored: null
required-owner-action: null
```
