# AUTOPILOT_EVENTS.md - EXAMPLE

Purpose: example owner-facing event log. Not an active autopilot run.

```yaml
- at: 2026-05-16
  event_type: stop
  severity: warning
  task_id: EX-01
  phase: 4. FAZA IMPLEMENTACJI
  summary: EXAMPLE workspace is documentation-only.
  owner_action_required: none
  recommendation: Do not use EXAMPLE for active execution.
  alternative: Copy templates into a real project workspace.
  impact_if_recommendation: Avoids false workflow state.
  impact_if_alternative: Enables a real run after proper setup.
  related_artifacts:
    - docs/projects/EXAMPLE/README.md
```
