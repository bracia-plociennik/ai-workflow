# upgrade-with-master-prompt Autopilot

Autopilot runtime router for `upgrade-with-master-prompt`.

Do not store run readiness, state, ledger, or events in this file. Runtime details belong in run directories under `autopilot/runs/`.

## Run Model

```text
autopilot/
  README.md
  runs/
    autopilot-001/
      README.md
      readiness.md
      state.md
      ledger.md
      events.md
```

## Current Run

| Field | Value |
| --- | --- |
| Current run | `none` |
| Latest run | `none` |
| Range | `none` |
| Status | `not-running` |
| Readiness | `draft` |
| Route | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/autopilot/runs/<run-id>/` |

## Rules

- Create a new `autopilot-XXX` directory for each supervised autopilot run.
- Keep run-specific `readiness.md`, `state.md`, `ledger.md`, and `events.md` inside the selected run directory.
- Root-level `autopilot-state.md`, `autopilot-ledger.md`, and `autopilot-events.md` are not canonical.
- Each run must declare `planning-range` or `implementation-range`.
- `phase-8-final-check` is owner-triggered only and must not be run automatically by autopilot.
- Do not start autopilot unless readiness is `ready`, workflow gates pass, and the risk model allows it.
