# Specification Review
- Date: 2026-10-03
- Scope: all seven PTO specifications, accepted architecture/plan and task index.
- Baseline: 8a0eeef; planning artifacts only.

## Findings Resolved In Specification
- P2: checkpoint gating only after third completion could admit task four while earlier tasks still run. PTO-002/004/005 now reserve distinct parent-task slots before dispatch; completed plus active tasks per checkpoint epoch cannot exceed three. Units within one task share one task slot.
- P3: generic future test command named contract/guidance cases not owned by those tasks. PTO-001 now uses its own policy smoke fixtures and PTO-007 actual document/handoff checks.
- Lifecycle ambiguity: accepted output becoming stale now transitions to blocked retaining the prior acceptance record; cancellation is not termination; retry gets a new attempt ID.
These are refinements within accepted architecture/plan, not new authority or changed task scope.

## Full Post-Fix Review
| Task | Intent/DoD and feasibility | Adversarial/failure checks reviewed | Producer -> consumer |
| --- | --- | --- | --- |
| PTO-001 | one owner; serial compatibility; packaging optional; activation withheld | contradictory policy clauses, second autopilot, approval escalation | canonical policy -> router/readiness/validator |
| PTO-002 | deterministic bounded allocation; task checkpoint reservations | cycle/missing dependency, read-write overlap, capacity unknown, fourth task early | manifest + observations -> proposal/reservations |
| PTO-003 | explicit worker context, isolation and output | shared cwd/resources, path escape, injected instructions, unknown real backend | approved spec/snapshot -> worker -> result |
| PTO-004 | atomic revisioned state and recovery | competing writers, stale lock, partial write, duplicate submit/cancel/retry | run + observation -> safe transition, preserved history |
| PTO-005 | actual diff acceptance and integrated QA | green unit tests with integration failure, stale accepted data, task-vs-unit cadence | accepted output -> integration -> canonical QA |
| PTO-006 | compatible schema 1/opt-in 2 and honest measurement | malformed capabilities, old provider, fake-vs-native evidence, missing actual test | installed source -> coordinator -> counterpart |
| PTO-007 | concise docs and one actual-results handoff | false implementation claim, client/approval import, automatic nested update | verified implementation -> privacy-safe conceptual handoff |

## Success And Failure Traces
Success: same-task independent units from approved snapshot reserve separate paths/resources -> observed native isolation -> attempts submit -> parent verifies actual scope/DoD/checks -> immutable accepted outputs -> serial integration -> common formal task QA -> canonical capture/cadence.
Failure: worker finishes with unexpected shared-router write -> result not accepted, resource retained until termination/reconciliation -> dependents blocked; independent unchanged results remain candidates but still need freshness and QA.
Resume: missing handle means unknown, not automatic retry; source drift invalidates affected outputs and consumers before new work.
Current planning does not perform these runtime actions; these are specification traces for future fixture assertions.

## Required-Field Mapping
Run identity/owner/revision -> CAS and coordinator identity checks.
Unit task/slice/DoD/approval/read-write/resources/dependencies -> planner, worker preflight and receiver.
Attempt handle/baseline/workspace/output digest -> recovery and acceptance.
Result actual diff/tests/findings/risks -> semantic reviewer and integration.
Integrated input/output baseline -> common QA and canonical status/capture consumers.
Capability/schema/source version -> counterpart handshake, never execution_authorized.

## Final Findings And Limits
No unresolved material artifact findings after complete post-fix re-review.
All seven specifications remain conditional for execution: high-risk approval, live predecessor refresh and safe backend evidence are not supplied by Spec QA.
Native platform support, real-model overhead and performance benefit not tested. Offline fixtures and fake adapters are planned evidence, not an implementation success claim.

## Task Index Refresh
Task index future implementation-quality paths were replaced with none until those reports exist. Full re-review of seven specifications against the corrected index and Plan QA run 002: no scope, DoD, write-set or dependency changes; existing implementation approvals remain pending. Spec QA run 002 supersedes initial run input bindings.

## Final Consumer Audit
Confirmed current validation-scope.py PROJECT_DIRS omits orchestration. Added the exact consumer path, sanitized inventory boundary and fingerprint/rejection regression to PTO-004 and plan; re-reviewed all specs against that final plan. Changes in run metadata must invalidate scoped evidence instead of disappearing from inventory. Native runtime/approval limitations remain unchanged. Current Spec QA is run 003.
