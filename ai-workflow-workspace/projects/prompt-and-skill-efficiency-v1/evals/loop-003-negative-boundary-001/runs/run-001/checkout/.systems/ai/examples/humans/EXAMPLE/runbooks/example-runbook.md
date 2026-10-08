# Runbook: Start EXAMPLE Autopilot

## Purpose

Give a human operator a concise process for starting supervised autopilot.

## Audience

- Project owner
- Operator

## Preconditions

- `.systems/ai/core/autopilot.md` has been reviewed.
- `.systems/ai/examples/projects/EXAMPLE/status.md` points to a ready next task.
- No critical-risk decision is open.

## Steps

1. Review `.systems/ai/examples/projects/EXAMPLE/status.md`.
2. Confirm the next task specification is ready.
3. Ask Codex to start supervised autopilot for the EXAMPLE project.
4. Verify autopilot runtime files are created under `.systems/ai/examples/projects/EXAMPLE/autopilot/runs/<run-id>/`.
5. Monitor `events.md` in the active run for owner-facing stops.

## Validation

- Autopilot ledger has a phase-started entry.
- Status and state agree on current task and phase.

## Rollback / Recovery

Stop autopilot and resume from the last stable PASS recorded in the active run's `state.md` and `ledger.md`.

## Escalation

- Escalate when a critical-risk or high-impact decision appears.
- Required context: status, state, ledger, failed artifact, and recommendation.

## Notes

This is an example runbook only.
