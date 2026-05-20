# events.md - EXAMPLE

Purpose: example owner-facing event log for one autopilot run. Not an active autopilot run.

```yaml
- at: 2026-05-16
  event-type: stop
  severity: warning
  task-id: EX-01
  phase: 4. FAZA IMPLEMENTACJI
  summary: EXAMPLE workspace is documentation-only.
  owner-action-required: none
  recommendation: Do not use EXAMPLE for active execution.
  alternative: Copy templates into a real project workspace.
  impact-if-recommendation: Avoids false workflow state.
  impact-if-alternative: Enables a real run after proper setup.
  related-artifacts:
    - docs/projects/EXAMPLE/README.md
```
