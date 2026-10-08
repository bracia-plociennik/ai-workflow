# Micro-Project: `distillation-state-tracking-v1`

## Status

- Status: implemented-awaiting-owner-commit
- Date: 2026-07-17
- Work mode for future implementation: `workflow-maintenance`
- Risk: `medium`
- Artifact scope: workspace-only planning evidence
- Tracked source changes: none
- Implementation performed: yes; quality closure complete
- Dreaming mode: `advisory-only`; report the queue of unrealized distillations and do not write or promote anything

## Summary

Add explicit per-work-item distillation state so completed implementation, fixes, quality closures, handoffs, and other meaningful work cannot disappear without a visible capture disposition. The state should be producer-owned by the workflow event that knows the work outcome and consumed by reminders, checkpoints, end-of-task capture, and Dreaming reports.

This scope does not make Dreaming an automatic writer. Dreaming only reads available state and artifacts, produces an advisory `Undistilled Work Queue` inside its Dream Report, and leaves all durable distillation, memory, System Insights, External Memory, status, commits, and pushes unchanged.

## Problem And Validation

### What stays

- Formal `phase-6-distillation` remains the canonical durable distillation route.
- `phase-7-checkpoint` remains the synchronization/checkpoint route.
- Knowledge Capture Reminder, End-of-Task Capture, and Optional Knowledge Capture keep their existing boundaries.
- Dreaming remains advisory-only and writes only Dream Reports.

### What should improve

- Replace implicit absence/presence checks with an explicit state for each meaningful work item.
- Make `ready`, `deferred`, `blocked`, and owner-skipped work visible instead of treating all non-distilled work as identical.
- Ensure micro-tasks, side-tasks, micro-projects, workflow-maintenance changes, and formal tasks can all produce a state record.
- Let consumers identify stale or unresolved capture without writing memory ad hoc.

### What should be removed or avoided

- Do not add a single global boolean ledger that loses project, scope, or privacy boundaries.
- Do not make `is_distilled=false` a permission to write automatically.
- Do not let Dreaming silently change state, create distillation artifacts, promote skills, or update memory.
- Do not use `memory-in-repo-memory` as the only source of truth for all work types.

### What is missing

- A canonical state machine and per-work record schema.
- Producer responsibilities after implementation, quality closure, checkpoint, and owner opt-out.
- Consumer rules for reminders, phase 6, phase 7, End-of-Task Capture, and Dreaming.
- Privacy/scope rules for records containing no client raw data and no secrets.
- Validator, fixture set, update-workspace support, and migration/compatibility guidance.

### Blockers and decisions

- No planning blocker after the owner explicitly confirmed Dreaming is advisory-only.
- Future implementation must use derived `is_distilled` compatibility reporting only if needed. The state enum is the source of truth because a boolean cannot distinguish pending quality, ready, deferred, blocked, owner-skipped, and not-applicable.

## Proposed State Model

Each work item gets a local record with the minimum fields:

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

State meanings:

- `pending-quality`: implementation or meaningful write happened, but required quality closure is not complete.
- `ready`: quality closure is complete and durable distillation is recommended or required.
- `completed`: accepted distillation exists and points to the source evidence.
- `deferred`: owner or workflow deferred capture with a reason and next trigger.
- `owner-skipped`: owner explicitly rejected capture; residual risk remains visible.
- `blocked`: missing scope, privacy, permission, evidence, or another hard gate prevents capture.
- `not-applicable`: the work produced no reusable knowledge and the reason is recorded.

`is_distilled` compatibility rule: report `true` only when `State: completed`; report `false` for every other state, but never use that boolean alone for routing or authorization.

## Producer And Consumer Contract

| Producer/event | Required state update | Consumer |
| --- | --- | --- |
| First implementation-class write | create `pending-quality` | quality closure and reminder |
| Quality closure complete | move to `ready`, unless no reusable knowledge is justified | phase 6, reminder, Dreaming queue |
| Phase 6 accepted distillation | move to `completed` and record artifact path | checkpoint, status, future reviews |
| Owner defers capture | move to `deferred` with reason and next trigger | reminder and Dreaming queue |
| Owner rejects capture | move to `owner-skipped` with residual risk | reminder and Dreaming queue |
| Missing privacy/permission/evidence | move to `blocked` | owner decision and fix route |
| Explicit no-value determination | move to `not-applicable` with rationale | audit and future deduplication |

State records should be per-work-item to reduce parallel write collisions. Suggested namespaces:

- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/capture-state/<work-id>.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/capture-state/<work-id>.md`

The record is workspace runtime evidence and must remain ignored/local-only unless a later policy explicitly defines a tracked artifact.

## Dreaming Boundary

Dreaming consumes only readable state records and supporting artifacts. Its report must include an `Undistilled Work Queue` with:

- work ID and scope;
- current state;
- source and quality evidence paths;
- recommended capture target;
- why capture is useful;
- blocker or missing decision;
- privacy/scope status;
- owner action required;
- residual risk.

Dreaming must report `Durable writes performed: no` and `Scheduler/automation used: no` for this scope. It must not:

- change `Distillation State`;
- create a phase-6 distillation;
- write project/repo memory;
- write External Memory or System Insights;
- create or promote skills;
- update status, commit, push, or approve work.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| DST-1 | Define the state machine and record template | `.systems/ai/core/`, capture-state template, naming/schema docs | All states, derived boolean rule, privacy fields, and transitions are explicit | Contract review and schema producer-consumer audit | completed |
| DST-2 | Add state producers | phase 4/5/6, task/micro-task/micro-project/workflow-maintenance templates and routes | Meaningful writes create or update the correct state without granting permissions | Producer fixtures for each work mode | completed |
| DST-3 | Add state consumers | knowledge-capture-reminder, end-of-task-capture, phase 7, response contract | Consumers route `ready/deferred/blocked` correctly and do not confuse them with completed | Consumer matrix and adversarial stale-state tests | completed |
| DST-4 | Add Dreaming queue reporting | dreaming-mode contract/template/validator and report examples | Dreaming reports all applicable unresolved states and performs no durable writes | Positive/negative Dreaming smoke tests | completed |
| DST-5 | Add validator, migration, and quality closure | `check-distillation-state`, update-workspace, required artifacts, smoke suite, docs | Invalid transitions, missing fields, raw data, auto-write and auto-push wording fail | Targeted checks plus explicit full validation before commit | completed |

## Definition Of Done

- A canonical per-work-item state schema and transition table exists.
- `pending-quality`, `ready`, `completed`, `deferred`, `owner-skipped`, `blocked`, and `not-applicable` have unambiguous semantics.
- Implementation, quality closure, phase 6, owner dispositions, and no-value decisions have explicit producer responsibilities.
- Reminder, checkpoint, End-of-Task Capture, and Dreaming have explicit consumer behavior.
- Dreaming reports an `Undistilled Work Queue` but never performs durable writes, state changes, commits, pushes, or promotions.
- `is_distilled` is derived from `completed` and cannot bypass privacy, permissions, QA, evidence, or approval gates.
- Validator and smoke tests cover missing fields, invalid transitions, stale state, raw client data, auto-write, auto-push, and queue completeness.
- Workspace remains ignored and no existing formal phase semantics are weakened.

## Plan Quality Contract

- DoD source: owner-approved request in this artifact plus existing `definition-of-done.md`, `plan-quality-contract.md`, `phase-6-distillation.md`, `phase-7-checkpoint.md`, `knowledge-capture-reminder.md`, `end-of-task-capture.md`, and `dreaming-mode.md`.
- Plan classification: `implementation-capable`.
- Artifact QA route: `global-quality-review-stance` for the workflow-maintenance plan and future state/template artifacts.
- Implementation quality route: `global-quality-review-stance` for workflow-maintenance changes; formal `phase-5-quality` remains required if the work is routed into a formal project phase.
- Required verification: producer-consumer field audit, state-transition matrix, privacy/adversarial policy tests, Dreaming no-write tests, targeted validators, and explicit `validate-workflow --profile full` before future commit/handoff.
- Quality-ready criteria: no unresolved P0/P1/material P2, complete fields and transitions, aligned intent/plan/spec, fresh re-review after fixes, and no weakening of phase 6/7 or Dreaming boundaries.
- Current implementation writes are tracked workflow-maintenance changes; final commit and push remain owner-controlled.
- Blocking decision and next route: no current planning blocker; future implementation must stop for missing state ownership, privacy scope, or migration compatibility decisions.

## Owner Decision Checkpoint

- Interaction mode: `interactive` for future implementation; `none` for this artifact write
- Decision state: `clear`
- Material decisions: `DST-DREAMING-BOUNDARY`, `DST-STATE-SOURCE`, `DST-RECORD-NAMESPACE`
- Questions asked: `none` because the owner explicitly confirmed advisory-only Dreaming and accepted a separate scope
- Auto-resolved reversible decisions: `DST-DERIVED-BOOLEAN` - `is_distilled` is derived from `completed`
- Optional owner refinements: a later owner decision may select a different per-work record namespace, but it must preserve per-scope ownership and ignore rules
- Decision artifacts: `none`
- Next route: implementation planning after a new owner command

## Evidence

- Read-only baseline reviewed: `HEAD 203a278`, clean `main`, `origin/main` aligned.
- Existing phase 6 defines durable distillation and project memory writes after Quality `PASS`.
- Existing phase 7 counts accepted phase-6 distillations and performs checkpoint synchronization, but has no global state for work that has not reached phase 6.
- Existing Knowledge Capture Reminder and End-of-Task Capture are advisory/proposal routes and do not persist a universal distillation disposition.
- Existing Dreaming Mode and validator define advisory-only Dream Reports with no automatic memory, insight, skill, status, commit, push, or scheduler writes.
- Search found no canonical `is_distilled`, `distillation-state`, or `undistilled` field in current contracts, templates, or scripts.
- Workspace tracking check before this write: `git ls-files ai-workflow-workspace` was empty.

## Quality Closure

- Closure type: `advisory implementation review`
- Findings/blockers: none known in the plan artifact; future implementation is blocked until its own implementation plan and current refresh are established.
- Intent / Plan / Spec Compliance: `aligned`
- DoD fit: `aligned`
- Risk/work mode compatibility: `aligned` (`medium` / `workflow-maintenance`)
- Cross-contract consistency: `aligned`
- Negative-space/adversarial review: completed at plan level for auto-write, auto-push, state loss, stale state, raw client data, invalid transitions, and Dreaming authority expansion
- Producer-consumer field audit: completed
- Policy-boundary matrix: completed
- Automated evidence role: supporting-only
- Post-fix full re-review: `completed`
- Reviewed baseline: `HEAD 203a278; clean worktree before workspace artifact write`
- Instruction refresh: `performed-full`; current source-of-truth chain reviewed
- Closure freshness: current; fresh full-current-diff QA completed after the fix loop
- Result wording: `Ready for owner review`
- Residual risk: formal phase-6 distillation and commit review remain separate owner-controlled follow-up steps; later migration must not misclassify old work or create raw client-data records

## Contract Compliance And Knowledge Capture

- Contract compliance: `advisory-compliant`; workflow-maintenance tracked source changes stayed within the accepted write set, with no product-code, permission, or gate changes.
- Knowledge capture: `required`; target `micro-project-artifact`; reason: owner-approved state-tracking and Dreaming boundary decisions are recorded in this ignored planning artifact.
- Durable workflow memory or System Insights: not written.

## Follow-up

- Promote to commit/handoff only after owner review of the current diff; no automatic commit or push is part of this scope.
- Keep Dreaming advisory-only in V1. Any future automatic durable capture must be a separately approved scope with explicit permissions, privacy, rollback, and owner controls.

## Implementation Range Evidence

- Range: sequential phase-4 implementation through quality, capture-state update, and checkpoint preparation.
- Slice status: `DST-1` through `DST-5` implemented and reviewed.
- Tracked implementation areas: state contract, capture template, phase producers, reminder/end-task consumers, phase 7 review, Dreaming queue, workspace bootstrap, validator, smoke integration, and guidance.
- Quality state: `ready`; fresh advisory closure completed, formal phase-6 distillation not recorded.
- Dreaming boundary: advisory-only queue reporting; no durable writes, state changes, commits, pushes, or scheduler automation.
- No commit or push performed.

## Implementation Range Checkpoint

- Quality route: `global-quality-review-stance` for workflow-maintenance scope.
- Findings/blockers: `none known after fix loop and fresh findings-first QA`.
- DoD fit: `aligned`.
- Intent/plan/spec compliance: `aligned`.
- Producer-consumer audit: complete for phase producers, capture consumers, and Dreaming queue boundary.
- Validation: targeted validators, smoke suite, and explicit full profile completed without reported errors.
- Checkpoint state: `ready for owner review`; stop before any commit, push, or phase-8 equivalent.
