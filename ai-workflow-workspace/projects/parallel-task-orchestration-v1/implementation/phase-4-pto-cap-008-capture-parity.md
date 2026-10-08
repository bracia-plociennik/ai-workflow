# Implementation: PTO-CAP-008-capture-parity

## Implementation Slice Plan
- Source: specs/phase-3-pto-cap-008-capture-parity-specification.md
- DoD source: PTO-008-AC1..AC6 in the accepted specification
- Authority: PTO-D08; current Spec QA and autopilot-005 readiness
- Scope: accepted source paths listed by the spec plus PTO-D09 existing capability pin; synthetic tests and owned runtime
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-008-S1 | Shared bounded semantic helper | capture-record.py, contracts | state/version/path invariants | shared parser and references/gate/source checks | completed |
| PTO-008-S2 | Reader and parent consumer parity | capture-state, validation-scope, parallel-orchestration | shared collection, no widened selection | real parent and three public-route regressions | completed |
| PTO-008-S3 | Regressions and fresh Quality | exact tests/smoke/docs | all AC; findings-first semantic review then scripts |54 runtime and89 orchestration regressions; final Quality follows | completed |
- Stop rule: unresolved scope/approval/safety/equivalence condition stops writes

## Slice Execution Evidence
- Initial baseline: existing PTO source retained, empty Git index, current spec008 PASS
- Changed files: capture-record.py, capture-state.py, validation-scope.py, parallel-orchestration.py, check-distillation-state, runtime-integrity.py, distillation-state.md, runtime-integrity.md, changelog.md and approved existing capability pin
- Checks:54 runtime integrity plus25 planner/12 protocol/23 lifecycle/17 integration/12 compatibility tests passed; manifest index valid; project capture consumer passes
- Fix evidence: independent review identified unbound source, contradictory gate, foreign root and normalized-duplicate bypass; all corrected with regressions
- Fixture fixes: public-route test supports the sanitized Gitless dispatcher copy while preserving Git-selected inputs and info/exclude for real repositories; unknown Gitless source rejects
- Full source evidence: run003 passed, exit0 at683 seconds, five groups and one completion marker; formal Quality is recorded separately
- Skipped checks: no native/model/performance tests, outside approved008 scope
- Residual risk: finite synthetic coverage; no native worker/capability or performance claim
- Quality closure route: formal phase-5-quality after all slices
