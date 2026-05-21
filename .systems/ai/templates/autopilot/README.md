# Autopilot Templates

Templates for project-local autopilot run artifacts and gate artifacts.

Suggested destinations:

- `autopilot-readme.template.md` -> `workspace/projects/<project>/autopilot/README.md`
- `run-readme.template.md` -> `workspace/projects/<project>/autopilot/runs/autopilot-001/README.md`
- `state.template.md` -> `workspace/projects/<project>/autopilot/runs/autopilot-001/state.md`
- `ledger.template.md` -> `workspace/projects/<project>/autopilot/runs/autopilot-001/ledger.md`
- `events.template.md` -> `workspace/projects/<project>/autopilot/runs/autopilot-001/events.md`
- `qa-evidence.template.md` -> `workspace/projects/<project>/quality/<task-id>-quality.md`
- `escalation.template.md` -> `workspace/projects/<project>/escalations/<task-or-workspace>-escalation-<YYYY-MM-DD>.md`
- `task-decisions.template.md` -> `workspace/projects/<project>/decisions/<task-id>-decisions.md`

Do not create runtime autopilot run files unless autopilot is active.

Root-level `autopilot-state.md`, `autopilot-ledger.md`, and `autopilot-events.md` are not canonical in the run-based model.
