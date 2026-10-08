# PTO-003 Implementation
- Date: 2026-10-04
- Task: PTO-ISO-003-isolated-delegation
- Source: accepted eight-path spec and reviews/pto-003-prewrite-readiness.md
- Baseline: 8a0eeef, approved existing PTO-001/002 changes preserved
- DoD source: PTO-003 AC1..AC5
- Implementation approval: decisions/implementation-approval.md
- Quality approval: decisions/pto-quality-range-approval.md, conditional on actual evidence

## Implementation Slice Plan
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | Explicit dispatch/result/prompt contract | helper, unit/result/prompt, core contract | strict producer-consumer fields and no new authority | field audit | completed |
| S2 | Actual inventory and protocol negatives | helper, tests | stale/foreign/omitted/unsafe output rejected | 25 planner and 12 protocol tests | completed |
| S3 | Current-diff adversarial review | all eight paths and shared predecessors | DoD, permissions, evidence and regression fit | independent review and full validation 645 seconds | completed |
- Stop rule: scope, approval, dependency or unsafe effect mismatch stops writes.
- Artifact QA route: phase-3-spec-qa; implementation QA: phase-5-quality.

## Slice Execution Evidence
- Execution metadata is optional for allocator inputs; mandatory for dispatch preflight.
- Preflight requires observed backend identity/handle, isolated physical workspace,
  bounded actual inventory, explicit input hashes and constrained writable roots.
- Submitted result is checked against parent-owned baseline and current worker files,
  including deletion and executable mode. Missing required evidence/actual scope
  mismatch fails closed. Results do not change accepted state or canonical routers.
- Initial protocol fixture inherited planner tests but pre-populated unit-a, causing
  duplicate IDs. Corrected fixture class separation; all original 25 planner tests
  remain separate. Two independent review findings corrected: bind attempts to
  originating run/project/coordinator/owner; all reported failed/skipped checks
  block quality readiness. A third independent finding added root mode/device/inode
  binding. Twelve current protocol tests pass; no assertion removed.
- Supplemental smoke ID added; all old IDs/frozen regions preserved, manifest verified.

## Instruction Refresh
- Status: performed-full on continuation then targeted at task pre-write.
- Trigger: resume, next accepted task and quality boundary.
- Contracts refreshed: AGENTS, operating-model, routing, risk, permissions,
  instruction refresh, phase-4/5, slicing, quality and parallel orchestration.
- Reviewed baseline: current branch/source, task spec and accepted predecessor outputs.
- Drift/conflict: none.

## Limits And Residual Risk
Cooperative before/after inventories do not detect write-and-restore or effects
outside the observed root. Independent backend enforcement and fresh observations
are required; JSON booleans are not proof. Git metadata requires a separately
verified adapter, so this bounded helper cannot silently claim native worktree support.
No native spawning, worktree cleanup, model call, commit or push occurred.

## Distillation State
- Record: capture-state/pto-iso-003-isolated-delegation.md
- State: ready; formal Quality follows completed current-diff review and owner approval.
