# Runbook: Start EXAMPLE Autopilot

## Purpose

Give a human operator a concise process for starting supervised autopilot.

## Audience

- Project owner
- Operator

## Preconditions

- `docs/ai/AUTOPILOT.md` has been reviewed.
- `docs/projects/EXAMPLE/STATUS.md` points to a ready next task.
- No critical-risk decision is open.

## Steps

1. Review `docs/projects/EXAMPLE/STATUS.md`.
2. Confirm the next task specification is ready.
3. Ask Codex to start supervised autopilot for the EXAMPLE project.
4. Verify autopilot runtime files are created under `docs/projects/EXAMPLE/autopilot/`.
5. Monitor `AUTOPILOT_EVENTS.md` for owner-facing stops.

## Validation

- Autopilot ledger has a phase-started entry.
- Status and state agree on current task and phase.

## Rollback / Recovery

Stop autopilot and resume from the last stable PASS recorded in `AUTOPILOT_STATE.md` and `AUTOPILOT_LEDGER.md`.

## Escalation

- Escalate when a critical-risk or high-impact decision appears.
- Required context: status, state, ledger, failed artifact, and recommendation.

## Notes

This is an example runbook only.
