# Decision: EXAMPLE Execution Mode

## Date

`2026-05-16`

## Status

`approved`

## Context

The owner needs to decide whether EXAMPLE work should run manually or with autopilot.

## Options

| Option | Pros | Cons | Impact |
| --- | --- | --- | --- |
| Manual | More owner control | Slower | Lower automation risk |
| Supervised autopilot | Faster with checkpoints | Requires clean status artifacts | Balanced control and speed |
| Autonomous autopilot | Fastest | Requires strong trust in gates | Highest automation reliance |

## Recommendation

Use supervised autopilot first.

## Owner Decision

- Chosen option: supervised autopilot
- Decided by: example owner
- Decision date: 2026-05-16

## Consequences

Autopilot may proceed through low-risk gates but must stop for high-impact or critical-risk decisions.

## Follow-Up

Create project-local autopilot runtime files when execution starts.
