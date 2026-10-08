# Task Specification: PTO-QA-005-integration-acceptance
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-QA-005-integration-acceptance
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: conditional
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual dependency outputs were refreshed on 2026-10-04: PTO-004 lifecycle, formal
Quality PASS and Phase 6, full source 641 seconds/743 IDs and fresh artifact closure.
Earlier planning-only limitations below remain historical, not new permissions.

## Task Contract
- Goal: Separate submitted/accepted/integrated results and preserve formal task gates.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-005-AC1: Acceptance checks actual worker diff, provenance, allowed changes, DoD and check evidence, not prose done.
  - PTO-005-AC2: Same-task dependents bind accepted immutable outputs; cross-task gates retain Quality/capture/checkpoint prerequisites.
  - PTO-005-AC3: Integration is serial with destination before/after fingerprints; conflicts stop without auto resolve.
  - PTO-005-AC4: Common QA reviews integrated behavior, consumers and failure paths; no combining worker PASS into task PASS.
  - PTO-005-AC5: Checkpoint counts tasks rather than units; dispatch respects every-three-task/final barriers; one capture writer.
- Dependencies: blocking PTO-RUN-004-lifecycle-recovery; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Local evidence mistakenly promoted to global PASS.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- .systems/scripts/lib/parallel-orchestration.py
- .systems/ai/core/parallel-task-orchestration.md
- .systems/ai/core/quality-review.md
- .systems/ai/core/full-qa-verification.md
- .systems/ai/workflow/phase-5-quality.md
- .systems/ai/templates/orchestration/integration-review.template.md
- .systems/scripts/smoke/core.sh
- .systems/scripts/lib/parallel-orchestration-tests.py
- .systems/scripts/smoke/manifest.json
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
Tool verifies structural evidence and source bindings only, never generates semantic acceptance or owner approval. Reviewer supplies decision; rejection leaves integrated baseline unchanged. Do not auto merge/cherry-pick inside generic manifest validator.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-005-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-005-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-005-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-005-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. Add structured reviewer-supplied acceptance fields; helper verifies actual source hashes, scope and evidence presence, not semantic correctness. Missing source is fail-closed.
2. Same-task consumer receives immutable accepted predecessor snapshot. A parent task's required Spec QA/Quality/capture remains external canonical evidence via existing reader, not a new PASS parser.
3. Integration owner reviews one accepted diff at a time against current destination. Platform/Git integration is an explicit gated action outside generic manifest helper; conflicts stop for review, no automatic preferred winner.
4. Record destination before/after, accepted attempt digests and actual changed paths. Common QA reruns relevant integrated tests and reviews producer-consumer/failure behavior on merged tree.
5. Task PASS only after full DoD/review evidence and required human gate. No per-unit PASS counts as task completion. Use existing qa-evidence.py for reading formal evidence.
6. Scheduler-free orchestration loop counts parent completed tasks for capture cadence. When third completion is reached stop new task dispatch; reconcile already-running permitted units before checkpoint; no fourth task may start across an unresolved barrier.
7. Enforce the barrier at reservation, not only completion: completed plus distinct active tasks cannot exceed three in a checkpoint epoch. Several units of one task share its single slot. Failed task slots are not silently released while liveness/writes remain unknown.

## Dependency Status
PTO-004 actual accepted output and existing QA/capture consumers were reviewed.
Current readiness uses decisions/implementation-approval.md and the conditional
high-risk Quality approval, with unchanged nine-path scope and AC1..AC5.

## Current Bounded Integration Design
Integration preparation/confirmation use the existing CAS helper and an optional
closed lifecycle integrations list. Freeze the entire declared target subtree,
including hashes/modes/deletions, outside canonical runtime. Compare changed
entries to the worker baseline; conflicts fail before external integration.
Persist the integration reservation across the external action. No helper performs
copy, Git operations or rollback. Confirm actual expected-after plus supplied review;
this is supporting metadata, never task PASS. Unknown outcomes retain reservations.
Explicit reviewed abandonment admits only no-change/known partial original-or-intended
entries, preserves history, blocks affected dependents and retains parent slots.
Dependency delivery verifies a separately copied isolated consumer tree, not paths
to a mutable predecessor. Cross-task dependencies still stop for external formal
Quality/capture/checkpoint routing; no in-helper shortcut is implemented.
Unsupported Git-bearing/oversized/unsafe trees fail closed. Native support remains
unverified; bounded offline fixtures cannot prove general write isolation.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-005-T1 | Two units pass separately but integration test fails: formal task cannot pass. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-005-T2 | Submitted dependency never starts downstream; accepted output later changed invalidates downstream evidence. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-005-T3 | Checkpoint at third task blocks next-task dispatch while allowing safe reconciliation; five units of one task do not trigger false cadence. | asserted required behavior and unchanged forbidden state; failures reported |
- Offline behavioral entrypoint to be implemented: python3 .systems/scripts/lib/parallel-orchestration-tests.py --case integration. PTO-001 uses its registered policy smoke cases before the helper is introduced by PTO-002; PTO-007 uses document/handoff review rather than claiming a guidance subcommand.
- Relevant smoke category: core supplemental tests, preserving existing manifest and all old IDs.
- Targeted contract check: .systems/scripts/check-parallel-task-orchestration (new in PTO-001).
- Final source gate after semantic QA: .systems/scripts/validate-workflow --profile full --project parallel-task-orchestration-v1 --explain.
- These are future implementation checks, not checks executed during specification.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Valid approved unit and compatible inputs | scoped owned execution/evidence | task-specific output satisfying AC | authority expansion or extra writes | reject unsafe extension | task tests above | follow producer through consumer for successful unit |
| Missing/stale input, competing owner or failed evidence | blocked/unknown | reason and preserved evidence | accepted/PASS despite missing proof | stop dependent work, preserve independent results | task negative cases | follow one failure to rejection without side effects |
Planning defines these flows; runtime traces will be evidence from implementation, not invented here.

## Potential Errors And Edge Cases
Missing backend -> safe serial/blocked. Duplicate attempt -> reject. Malformed JSON/path -> reject without writes.
Unrelated file drift -> classify scope; affected baseline -> invalidate evidence. Submitted result -> no automatic acceptance.
Tests pass but DoD mismatch -> fix-loop, not PASS. Operator opt-out cannot supply a required gate.

## User Decisions
PTO-D01 dynamic count; PTO-D02 isolation/integration QA; PTO-D03 handoff; PTO-D04 no delivery deadline/timebox; PTO-D05 planning only.
Future high-risk implementation approval is required; live synthetic worker/backend check requires applicable runtime permissions. No additional planning question is needed.

## Assumptions And Revalidation
Standard library and existing shell entrypoints suffice; verify before writes. Platform backend support is unknown until observed.
Safe serial fallback is mandatory. A future unsupported backend does not justify false native-support or performance claims.

## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: task AC above, accepted context and project plan
- Testable DoD / acceptance conditions: all PTO-005-AC items and specified failure/compatibility tests
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after this specification is complete; repeat if predecessor changes its assumptions
- Implementation Quality Closure route: phase-5-quality
- Required verification: automated task regressions, manual success/failure trace, intent/DoD/current-diff review, applicable full supporting source validation.
- Quality-ready criteria: exact scope and consumer contracts, tests available, no unresolved material findings, current evidence and required owner approval.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: high-risk implementation approval; not required to finish this artifact QA
- Next route: phase-3-spec-qa

## Implementation Gate
- DoD complete and testable: yes
- Dependencies satisfied or explicitly gated: yes
- Required user decisions resolved: yes, current implementation and conditional Quality approval recorded
- Can enter implementation: yes, after current Spec QA and pre-write readiness
- Blocking reason: none for this bounded offline scope

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Source: owner explicitly requested no deadline or timebox for this project.
- Must-have outcome: safe dynamic delegation, single execution owner, integrated QA.
- Cutline/deferred scope: scheduler, recursive delegation, production effects and AI System implementation.
- Quality floor: current artifact QA, scoped evidence, no unresolved material findings.
- Overrun checkpoint: stop for new scope or permissions, never invent a delivery deadline.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D01 through PTO-D05
- Questions asked: none; prior owner answers remain applicable.
- Auto-resolved reversible decisions: canonical artifact names and serial planning.
- Optional owner refinements: none required for planning.
- Decision artifacts: decisions/owner-decisions.md
- Next route: artifact-specific gate; implementation approval remains separate.

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: preserve ownership and safety decisions.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Dynamic orchestration without duplicate authority
- Suggested entry summary: Single execution owner and evidence-backed integration; final AI System handoff after actual QA.
