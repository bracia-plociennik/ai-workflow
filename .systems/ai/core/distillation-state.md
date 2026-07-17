# distillation-state.md

## Purpose

`Distillation State` is a per-work-item disposition that makes reusable knowledge and unresolved capture visible. It is workspace runtime evidence, not permission to write memory. The formal phase 6 distillation remains the canonical durable distillation route.

## State Record

Every implementation-class write must create or update a scoped record before quality closure. A meaningful fix, quality closure, handoff, or owner capture decision may then update that same record under project or repo workspace:

```text
Distillation State
- Work ID:
- Work mode:
- Project/repo scope:
- Source artifact:
- Quality artifact:
- State: <pending-quality|ready|completed|deferred|owner-skipped|blocked|not-applicable>
- Distillation artifact: <path|none>
- Last reminder: <timestamp|none>
- Owner disposition: <capture-now|defer|skip|blocked|not-requested>
- Privacy/scope check: <pass|fail|unknown>
- Residual risk:
```

Suggested per-work namespaces:

- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/capture-state/<work-id>.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/capture-state/<work-id>.md`

## State Semantics And Transitions

- `pending-quality`: meaningful write happened, required quality closure is incomplete.
- `ready`: quality closure passed and durable distillation is recommended or required.
- `completed`: accepted phase-6 distillation exists and is linked.
- `deferred`: owner or workflow deferred capture with reason and next trigger.
- `owner-skipped`: owner explicitly rejected capture with residual risk.
- `blocked`: privacy, scope, permission, evidence, or another hard gate blocks capture.
- `not-applicable`: no reusable knowledge was produced and the reason is recorded.

Allowed normal transitions are `pending-quality -> ready`, `pending-quality -> not-applicable`, `ready -> completed`, `ready -> deferred`, `ready -> owner-skipped`, `ready -> blocked`, and `ready -> not-applicable`. A later fix or new quality result may move a record back to `pending-quality`; invalid jumps must be escalated rather than silently rewritten. `not-applicable` requires a recorded no-reusable-knowledge rationale.

`is_distilled` is compatibility output only: it is `true` exactly when `State: completed`, and `false` for every other state. The enum remains the source of truth and the boolean never authorizes a write, promotion, commit, push, or phase transition.

## Producers

- The first implementation-class write must create `pending-quality` before or atomically with the write evidence; a missing record is a pre-commit/quality finding.
- Quality closure moves the record to `ready`, or directly to `not-applicable` only when a justified no-reusable-knowledge result is recorded.
- Phase 6 moves accepted work to `completed` and records the distillation path.
- Owner defer/reject and missing privacy or evidence create `deferred`, `owner-skipped`, or `blocked` with reason and residual risk.

## Consumers

- Knowledge Capture Reminder reports `ready`, `deferred`, and `blocked` records.
- End-of-Task Capture proposes the correct route and never writes ad hoc.
- Phase 7 checkpoint must account for accepted `completed` records and unresolved states in its drift review.
- Dreaming reads records and reports an `Undistilled Work Queue` only.

## Enforcement And Completeness

Phase 4, implementation-slicing evidence, and implementation-capable micro-work artifacts must expose the record path and state. The delivery/quality validators must verify these producer fields and the Dreaming validator must verify the queue fields. A contract heading without field-level evidence is not sufficient.

## Dreaming Boundary

Dreaming remains advisory-only. It may scan state records and add queue rows to a Dream Report, but it must not change state, create distillation, write memory, write External Memory or System Insights, promote skills, update status, commit, push, or run scheduler automation.

Dream Reports for this contract must state `Durable writes performed: no` and `Scheduler/automation used: no`.

## Privacy And Scope

State records contain paths and workflow metadata only. Do not copy raw client data, secrets, API keys, credentials, private keys, production data, or project-specific domain content into cross-project insights or External Memory.
