# Autopilot Templates

Templates for project-local autopilot run artifacts and gate artifacts.

Suggested destinations:

- `autopilot-readme.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/README.md`
- `run-readme.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/README.md`
- `readiness.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/readiness.md`
- `state.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/state.md`
- `ledger.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/ledger.md`
- `events.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/events.md`
- `qa-evidence.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/<task-id>-quality.md`
- `escalation.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/escalations/<task-or-workspace>-escalation-<YYYY-MM-DD>.md`
- `task-decisions.template.md` -> `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/decisions/<task-id>-decisions.md`

Do not create runtime autopilot run files unless autopilot is requested or active. Always create or update `readiness.md` before `state.md` can move to `running`.

Root-level `autopilot-state.md`, `autopilot-ledger.md`, and `autopilot-events.md` are not canonical in the run-based model.
