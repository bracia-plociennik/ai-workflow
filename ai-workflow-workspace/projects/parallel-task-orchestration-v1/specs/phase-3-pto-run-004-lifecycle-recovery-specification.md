# Task Specification: PTO-RUN-004-lifecycle-recovery
## Metadata
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-RUN-004-lifecycle-recovery
- Date: 2026-10-03
- Workflow phase: phase-3-specification
- Readiness: conditional
- Implementation writes in this planning-range: forbidden

## Sources
planning/phase-2-project-plan.md; quality/phase-2-plan-qa.md; architecture/phase-1-architecture.md; context.md; decisions/owner-decisions.md.
Actual dependency outputs do not exist yet; before implementation refresh this spec against predecessor output rather than claiming those dependencies are satisfied.

## Task Contract
- Goal: Persist safe unit/attempt ownership and reconcile interrupted work.
- Scope: exact planned source paths listed below.
- Out of scope: unrelated refactors, changed approval/risk gates, AI System product, real external effects, secrets, production and recursive workers.
- Definition of Done:
  - PTO-004-AC1: State transitions reject duplicate/stale attempts, invalid owner, revision mismatch and impossible dependencies.
  - PTO-004-AC2: Manifest updates are atomic and single-writer; reservation acquired before dispatch; rejected mutations leave bytes unchanged.
  - PTO-004-AC3: Resume reconciles platform handles, actual files and evidence before restart; unknown liveness keeps reservation.
  - PTO-004-AC4: Failure blocks dependent units, preserves independent evidence and never silently retries unknown external effects.
  - PTO-004-AC5: Retry ceilings respect parent workflow; no auto-deletion of stale locks, force reset, auto commit or recursive spawn.
  - PTO-004-AC6: Canonical orchestration manifest and sanitized result metadata participate in owned runtime inventory/freshness; private raw logs, foreign repos and worktrees do not enter the owned namespace.
- Dependencies: blocking PTO-ISO-003-isolated-delegation; informational AI System preliminary handoff; optional none.
- Risk type: high
- Main risk: Double execution or corruption on resume.
- Start condition: explicit high-risk implementation approval, isolated branch, current Spec QA, known safe tests, current instruction baseline and completed prerequisite gates.
- End condition: AC verified, fresh full-current-diff semantic QA and formal Phase 5, then Phase 6 and Phase 7 when due.
- Requires user decision before implementation: yes

## Planned Write Set
- .systems/scripts/lib/parallel-orchestration.py
- .systems/scripts/manage-parallel-run
- .systems/scripts/lib/validation-scope.py
- .systems/ai/templates/orchestration/run.template.json
- .systems/ai/core/parallel-task-orchestration.md
- .systems/scripts/smoke/core.sh
- .systems/scripts/lib/parallel-orchestration-tests.py
- .systems/scripts/smoke/manifest.json
Existing paths are modified in place; absent listed paths are new files. Extra files discovered necessary require spec refresh and scope approval before writes.
CLI subcommands validate, transition, reconcile. Mutations require explicit run root, expected revision and coordinator ID. Reconcile defaults read-only; accepted mutation only via explicit transition. Lock protects local races, not malicious host/distributed ownership.

## Implementation Slice Plan
- Source: accepted project context, plan and this spec.
- DoD source: PTO-004-AC rows.
- Implementation scope: this task only.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-004-S1 | Refresh inputs and define schema/contract change | listed contracts/schema/helper | approved scope and current predecessor outputs | source digest, reviewed DoD | planned |
| PTO-004-S2 | Implement bounded behavior and regression fixtures | listed scripts/templates/tests | AC and negative cases | test logs and actual diff | planned |
| PTO-004-S3 | Review integrated task and required consumers | changed set and immediate consumers | findings-first DoD/intent/edge/regression review | formal phase-5-quality plus supporting checks | planned |
- Stop rule: scope creep, missing decision, unknown dependency/resource, unsafe effect or permission mismatch stops writes and routes to spec fix-loop/owner.
- Compact mode: not applicable; high-risk task.

## Implementation Plan
1. manage-parallel-run --run-root <owned-path> --coordinator-id <id> validate|transition|reconcile. transition additionally requires --expected-revision N and --request <JSON-path>; no arbitrary shell string executed.
2. Exclusive update lock guards read/check/write; acquire safely, validate old revision/owner, write temp in same directory, fsync, atomic replace, then release own lock. Conflict/parse failure exit nonzero without changing manifest.
3. States: planned->ready after gates; ready->running only after reservation/preflight; running->submitted on matching complete result; submitted->accepted after supplied reviewer decision checked structurally; rejected/blocked/cancelled retain evidence.
4. Attempt ID is never reused. Retry uses new attempt after verified termination and reconciled known write effects, within existing parent retry ceilings. No automatic stale-lock deletion or destructive Git cleanup.
5. reconcile outputs observations/proposed corrections read-only. Unknown process liveness or uncertain partial writes blocks dependent dispatch and retains resource reservation. Explicit transition applies reviewed reconciliation.
6. Freeze finished attempt inputs/results; later edits invalidate acceptance, never overwrite history. Independent outputs survive another unit failure but still need current validation at integration.
7. An accepted unit whose inputs/results drift moves to blocked with an invalidation reason and retained prior acceptance event. Rejected/cancelled attempts are immutable; retry is a new attempt under a ready unit only after reconciliation. Cancel-requested remains running until actual termination is confirmed.
8. Lock/revision/owner reservation applies to distinct active parent task slots as well as worker/resource slots. Reconcile recomputes the checkpoint epoch before admitting any new task.
9. Extend the existing explicit owned runtime inventory to include canonical orchestration run records. The current PROJECT_DIRS allowlist lacks orchestration. Keep all symlink/foreign-repo/privacy rejection and include only sanitized active run metadata/results. Worktrees, raw logs/prompts and fixtures stay outside that canonical namespace; record references/digests, not private contents.

## Dependency Status
PTO-003 now has formal Quality PASS, Phase 6 and the PTO-001..003 checkpoint.
Reviewed actual preflight/result interfaces and their external-observation boundary
on 2026-10-04. Current readiness is reviews/pto-004-prewrite-readiness.md; accepted
scope and AC unchanged. Native observations are not authenticated by JSON.

## Tests And Pass Conditions
| Test / check | Method | Pass condition |
| --- | --- | --- |
| PTO-004-T1 | Competing revision updates, process crash before/after replace, partial/corrupt manifest, stale lock and duplicate submit. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-004-T2 | Crash after write before event; cancel requested vs confirmed stopped; resume twice does not replay completed writes. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-004-T3 | Changed input snapshot invalidates only affected consumers; missing live handle blocks resource reuse. | asserted required behavior and unchanged forbidden state; failures reported |
| PTO-004-T4 | Mutate canonical run manifest/result, then compare runtime inventory; introduce symlink or foreign checkout. | state mutation changes fingerprint; forbidden inputs rejected; no raw data copied |
- Offline behavioral entrypoint to be implemented: python3 .systems/scripts/lib/parallel-orchestration-tests.py --case lifecycle. PTO-001 uses its registered policy smoke cases before the helper is introduced by PTO-002; PTO-007 uses document/handoff review rather than claiming a guidance subcommand.
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
- Testable DoD / acceptance conditions: all PTO-004-AC items and specified failure/compatibility tests
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
- Required user decisions resolved: yes, separate implementation and Quality range approval
- Can enter implementation: yes, after current Spec QA and readiness verification
- Blocking reason: none for this bounded source implementation

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
