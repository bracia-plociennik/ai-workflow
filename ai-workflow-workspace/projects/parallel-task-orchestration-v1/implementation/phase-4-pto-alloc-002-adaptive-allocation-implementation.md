# PTO-002 Implementation
- Task: PTO-ALLOC-002-adaptive-allocation
- Source HEAD: 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1
- Work mode: formal project, high-risk workflow-maintenance
- Owner approval: decisions/implementation-approval.md
- Prerequisites: reviews/pto-002-prewrite-readiness.md and current Spec QA
- Delivery constraints: no deadline/timebox, owner opt-out

## Implementation Slice Plan
- Source: accepted allocation specification and continuation approval.
- DoD source: PTO-002-AC1..AC5.
- Implementation scope: eight exact source paths in allocation spec.
- Artifact QA route: phase-3-spec-qa.
- Implementation quality route: phase-5-quality.
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | Strict schema and contained paths | helper, run/unit templates | malformed identity/types/paths reject | unit negative cases | completed |
| S2 | DAG, capacity, conflicts and read-only CLI | helper and plan CLI | deterministic bounded proposals | examples and CLI tests | completed |
| S3 | Regressions and full review | tests, supplemental smoke, manifest | DoD, no authority leakage or coverage loss | producer-consumer and adversarial review | completed |
- Stop rule: scope expansion, missing authority, dependency or unsafe effect stops writes.

## Slice Execution Evidence
Initial approved preflight and current predecessor gates reviewed. No dispatch or native isolation claim.

- Strict JSON schema, deterministic DAG order, whole-pool capacity subtraction,
  checkpoint task-slot accumulation and read-only CLI implemented.
- 25 offline behavioral tests passed after the path-boundary fix loop.
- Independent adversarial review found Unicode ancestor aliases, subtree hardlinks
  and symlink ancestors in root/manifest paths. All three were corrected within
  the approved eight-file source scope. A further combining-mark order case was
  corrected by NFC-before-casefold-before-NFC; fresh independent re-review found
  no remaining material technical findings on the final source.
- Paths are conservatively compared with NFC/casefold. Existing hardlinks,
  linked/special subtrees and inventories exceeding 10,000 metadata visits fail
  closed. This is a proposal-time observation, not a filesystem sandbox or
  protection against concurrent malicious filesystem mutation.
- Core smoke before these final fixes passed in 64 seconds. It is historical,
  not current final-source evidence. Final-source full validation later passed
  all five groups, 741 IDs, exit 0, in 656 seconds (smoke 622 seconds).
- Manifest inputs and all runtime bytes stay unchanged by the planner. Malformed
  UTF-8, duplicate keys, non-finite values, unsafe paths and FIFO inputs reject
  without an execution payload. A blocked valid proposal exits 0, not PASS.

## Distillation State
- Record: capture-state/pto-alloc-002-adaptive-allocation.md
- State: pending-quality

## Quality Closure
- Advisory current-diff review: reviews/pto-002-quality-review.md.
- DoD and semantic review complete; no unresolved material technical findings.
- Formal Phase 5 remains awaiting owner approval; no formal PASS issued.
- Formal gate requires evidence and applicable human acceptance.

## Instruction Refresh
- Status: performed-full after continuity restoration, then targeted closure check.
- Trigger: resume/compaction, official working-directory baseline and quality closure.
- Contracts refreshed: AGENTS, operating-model, command-routing, risk, permissions,
  instruction-adherence-refresh, workflow, phase-4, phase-5, quality-review,
  full-qa-verification, response-contract, contract-compliance and prompt-injection.
- Reviewed baseline: 8a0eeef, exact approved source scope and project prerequisites.
- Drift/conflict: none after explicit current status and prerequisite reconciliation.
