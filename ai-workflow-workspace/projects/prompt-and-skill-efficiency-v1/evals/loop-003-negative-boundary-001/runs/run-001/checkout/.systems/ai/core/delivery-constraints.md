# delivery-constraints.md

## Purpose

Delivery constraints give new implementation work a time boundary without turning schedule pressure into permission to weaken safety, scope, Definition of Done, QA, evidence, approvals, or stop conditions.

This is a planning contract. It does not grant write permission and does not replace task intake, Plan Quality Contract, Implementation Slice Plan, risk routing, or quality closure.

## Default Rule

Before new implementation work, ask for the material delivery constraint when it is not already present in the accepted owner request or artifacts. Group missing questions with Owner Decision Discovery, at most `1-3` questions. Do not ask redundant versions of deadline, time budget, and duration.

If the owner gives no deadline or timebox, do not invent one. Record `Mode: not-set` and ask the nearest material question before dependent planning or implementation. An explicit owner opt-out is allowed only for the current scope unless it explicitly says otherwise.

## Delivery Constraints Block

Implementation-capable plans and work artifacts should include:

```text
Delivery Constraints
- Mode: <deadline-and-timebox|deadline-only|timebox-only|owner-opt-out|not-set>
- Deadline: <timestamp|none>
- Timezone: <IANA timezone|none>
- Time budget: <duration|none>
- Must-have outcome: <testable result>
- Should-have scope: <list|none>
- Stretch scope: <list|none>
- Explicitly deferred scope: <list|none>
- Quality floor: <DoD/QA/acceptance boundary>
- Cutline rule: <what is reduced first>
- Overrun checkpoint: <route and owner decision>
- Owner override: <decision or none>
```

## Scope And Quality Boundaries

- The must-have outcome and quality floor are protected.
- AI may defer stretch scope and, when safe, should-have scope, but must report the change.
- AI must not silently change scope, DoD, acceptance criteria, architecture, risk, permissions, security, billing, migration, production, external effects, or owner approvals.
- Deadline pressure never authorizes skipping QA, review, evidence, security checks, or phase gates.
- Estimates are planning estimates, not guarantees.

## Overrun And Opt-Out

When the deadline or timebox is at risk, stop at the overrun checkpoint and report delivered scope, remaining scope, quality state, and the owner decision required. Do not silently extend the run.

Supported opt-out wording includes `bez deadlinu`, `bez planowania z deadlinem`, `no deadline`, `without deadline`, `bez timeboxu`, and `no timebox`. The opt-out must be reported in the Execution Trace with residual risk. It does not bypass risk, permissions, DoD, QA, evidence, approvals, or stop conditions.

Autopilot readiness must contain a resolved delivery constraint or an explicit owner opt-out before `running`. Active autopilot remains non-interactive; a new material delivery decision stops the run as `awaiting-owner`.

## Routing And Ownership

- `task-intake` discovers whether deadline, time budget, must-have outcome, and cutline are missing.
- `owner-decision-checkpoints` asks only material missing delivery questions.
- `plan-quality-contract` requires the delivery block for implementation-capable plans.
- `implementation-slicing` uses the cutline to sequence slices, but never changes permission or quality gates.
- `phase-5-quality` and global quality review compare delivered and deferred scope with the agreed constraints.
- Deadline state is supporting evidence; repository state and accepted artifacts remain the source of truth.

## Evidence

Quality closure records the agreed deadline/timebox, delivered scope, deferred scope, deadline status, quality floor, skipped checks, overrun decisions, and residual risk.
