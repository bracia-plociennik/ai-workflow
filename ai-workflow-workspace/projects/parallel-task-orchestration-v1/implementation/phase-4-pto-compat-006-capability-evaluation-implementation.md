# PTO-006 Implementation
- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-COMPAT-006-capability-evaluation
- Date: 2026-10-04
- Source: revised006spec and PTO-D06; native verification explicitly deferred
- DoD source: revised AC1..6
- Baseline: 8a0eeef on codex/parallel-task-orchestration-v1 with approved predecessor source

## Implementation Slice Plan
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-006-S1 | Closed capability and schema2 | capability/coordinator/wrapper/runtime | default1 parity, opt-in2, unverified operational support | actual CLI and bounded malformed-file tests | completed |
| PTO-006-S2 | Compatibility/regressions/measurement | validator/tests/core/manifest | all offline cases, three paired samples, unique preserved IDs | tests and sample output | completed |
| PTO-006-S3 | Current review/Quality/capture | owning project evidence | six AC and formal gate | current review, full validation, phase6/checkpoint | in-progress |

## Slice Execution Evidence
Twelve compatibility tests and77 predecessor tests passed; check-runtime-integrity
ran46 passing regressions. Actual CLI emits schema1 by default and schema2 only
when requested. Both reject implicit execution authority; capability is protocol
vocabulary with unverified native backend, no observed capacity or owner permission.
Missing/malformed/version/type/duplicate-key/linked/hardlinked/oversized/missing
installed files produce conservative unknown/serial. Source changed during schema2
query rejects output. Actual file inventory remains unchanged after CLI queries.

Three paired offline file/hash workloads used identical payloads, assertions and
serial integration. Total includes setup, work, integration, verification/cleanup;
rework and conflicts were zero in these success samples, not assumed for failures.
Serial totals were1.486/1.635/1.438ms; threaded1.807/1.442/1.502ms.
Evidence /tmp/pto-006-compatibility-001.log. Tiny noisy samples support no speedup
or model/backend conclusion. Negative failure/conflict/recovery coverage is in
separate actual filesystem protocol/lifecycle/integration tests.

## Initial Test Correction
First compatibility run failed a fixture assertion comparing Git baseline before
and after deleting a tracked capability. Git correctly changed its baseline.
Corrected expectation verifies unchanged schema1 contract fields and changed
baseline; no production safety weakening. Fresh suite passed after correction.

## Review Completeness Gate
- Instruction baseline: current contracts/spec/PTO-D06 before writes
- Current full diff: reviewed original eight006 paths plus immediate consumers
- Producer-consumer audit: capability -> closed parser -> schema2 output -> consumer fallback; permission remains separate
- Adversarial matrix: versions/types/authority, forged native support, filesystem aliases/missing source/drift, default schema compatibility
- Automated evidence role: supporting-only
- Independent review: post-fix completed; both P2 findings fixed and no remaining material finding
- Closure freshness: source review complete, final supporting full pending
- Residual risk: no native backend verification, no model/network/production test

## Adversarial Fix Loop
Capability now pins all six installed source hashes and validates template schemas
without executing candidate source. Deep JSON parser exhaustion returns generic
unknown/serial. Actual source-drift/schema/deep helper and CLI regressions passed.
The parent re-reviewed all eight current paths and immediate predecessors;
independent reviewer confirmed the fixes and preserved authority boundaries.
Full source support remains pending; earlier partial runs are failed history.

## Quality Route
Formal phase-5-quality under existing conditional high-risk approval after fresh
complete semantic review and applicable full source validation, then phase6 and
checkpoint at cadence3/3. Native test is deferred scope, never passed by simulation.
