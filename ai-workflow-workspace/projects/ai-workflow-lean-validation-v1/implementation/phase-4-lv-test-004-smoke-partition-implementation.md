# LV004 Implementation Slice Plan

- Source: refreshed specs/phase-3-lv-test-004-smoke-partition-specification.md
- DoD source: accepted task contract, V4-01..09 and manifest/equivalence requirements
- Work mode: formal project, workflow-maintenance
- Risk: high
- Owner approval: LV-DEC-008
- Baseline: clean 03fb788; LV001-LV003 checkpoint completed
- Implementation writes: yes, only thirteen enumerated source paths in spec
- Artifact QA route: fresh Spec QA
- Implementation QA route: phase-5-quality
- Quality floor: findings-first current-diff review, exact assertion/behavior equivalence, producer-consumer audit, lifecycle cleanup and full validation
- Stop rule: unknown assertion, cross-group state, scope expansion or inconclusive equivalence blocks promotion; monolith retained
- Deadline/timebox: owner-opt-out LV-DEC-001
- No push or final-owner-yes

| Slice ID | Goal | Expected Files/Areas | Acceptance Check | Evidence Required | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | freeze actual reference and ownership | ignored reference inventory and live source review | all 674 actual IDs and outside assertions accounted | immutable bytes/log hashes, semantic assertion audit | completed |
| 2 | literal independent partition | runner, common, five groups, manifest | named groups use fresh fixtures and pure imports | standalone checks, unchanged raw regions, ownership map | implemented, ownership and isolation verified |
| 3 | compatibility and observability | two allowed validators, docs | live coverage index, one parent wall, actual group routing | producer-consumer and CLI failure traces | implemented within thirteen-path ceiling |
| 4 | equivalence and protected mutations | ignored fixtures, in-scope smoke helpers | all IDs/assertions exactly once, same rejection, repeats/order/cleanup | old-vs-new logs/diagnostics and negative matrices | completed for preserved reference; final full after last added regressions pending |
| 5 | quality closure | Phase 4/5 artifacts and applicable full scripts | all DoD evidence complete, no material unresolved finding | full-current-diff semantic QA before full scripts | source review recorded, full verification and current prerequisite assessments pending |

## Slice Execution Evidence

- Slice 1: frozen post-LV003 runner and complete execution log yield 674 unique IDs; 110 lexical assertion candidates and 32 consumer references inventoried. Lexical candidates still need semantic classification.
- Slice 2 prototype: workspace group passed (95 seconds) in disposable fixture. Quality attempt failed because original backup line 4052 was assigned to policy and its mutation/restoration to quality. Corrected boundary keeps the complete transaction together; fresh quality group retest passed (247 seconds). Remaining groups and equivalence are pending.
- Historical prototype failures are retained. Backup/mutation/restore transactions at 1967, 3216 and 4052 are now owned together; the executable entrypoint retains its original mode. Fixture parents avoid canonical quality/ path components interpreted by legacy readers.
- Current tracked source: exactly thirteen accepted paths, only after actual independent/equivalence/fault and protected-mutation evidence. No changes to CI, full runner, updater or other runtime consumers.
- Frozen reference all: 674 IDs, exit 0, 710 seconds. Partition all before final supplemental additions: 681 IDs, exit 0, 686 seconds. Standalone groups executed in reverse order with exact ownership: workspace 95, skills 29, quality 343, policy 157, core 57. These are correctness evidence, not a speed claim or the final source gate.
- Typed negative diagnostics: 552 reference outcomes matched by ID/status/cause, normalizing only disposable host paths in comparison. Raw evidence remains unchanged.
- Two real protected mutations (status and observability validators incorrectly returning zero) were rejected by both reference and candidate for the same case and status. Evidence: implementation/lv004-protected-mutations/results.json.
- Lifecycle investigation found and repaired start-time padding mismatch and missing cleanup after leader failure. Owned descendant identities are retained during execution; zombie processes are not live orphans. Twelve actual synthetic adversarial cases cover direct failure, early zero, interrupt, timeout, cleanup failure and manifest corruption. No unrelated process-name killing or network calls.
- Producer-consumer review strengthened assertion source-line/group and per-test region/command mappings; twenty supplemental cases distinguish these controls from the 674 reference IDs. Final core after mapping corrections passed in 61 seconds, including safe/direct/compound policy and missing-source tests.
- Current source audit: 13 paths, digest 3442e58e35be136297ee3468499ebadd5b7ad486cbe1c4c8e4f84e5d5b512a0f; 21 exact frozen regions; 95 assertion points, 14 failure branches, one failure fixture and 34 nested Python assertions; pure common import has no filesystem effects. Files byte-match the final isolated fixture.
- Skipped checks: final source-only full is running; actual-runtime full and genuine current predecessor/Spec assessments follow. No formal Phase 5 result, capture or commit for LV004 yet.
- Residual risk: local macOS evidence is bounded; no Linux CI run, no full performance improvement claimed, and the supervisor is not an isolation boundary for arbitrary malicious detached jobs.

## Producer-Consumer Audit

| Producer | Consumer | Verified mapping |
| --- | --- | --- |
| immutable reference regions | manifest loader and group source | all 674 executed identities, 110 classified outside points and 34 nested assertions, exact line/group/hash ownership |
| group source and pure helpers | dispatcher and disposable fixtures | independent owned setup/mutation/restore, no accidental setup on import |
| public compatibility index | existing policy validators and manifest loader | each literal route binds a live ID and its real command contract, not a disconnected comment |
| private executed-ID ledger | public completion | every selected ID exactly once and in its actual group; early zero without coverage rejected |
| group completion/progress | lifecycle consumer | namespaced group markers, public active test IDs, exactly one public completion |
| child timing rows | LV002 timing/comparison consumer | unchanged nine columns, smoke-all child profile for all, one smoke-suite-wall; subset not full |
| current diff and actual runtime | Spec/regression/Phase 5 consumers | historical source/grades retained; current assessments require substantive review, not renewed hashes |

## Semantic Review Before Final Scripts

- Intent/plan/spec: thirteen accepted paths, V4-01..09 and explicit fallback; no lost old assertions, automatic source inference, cache, push or external model call.
- Changed files reviewed: entire public dispatcher, shared helper, all five complete source regions/groups, full manifest schema/line bindings, both consumers and all three docs. Raw-region comparisons support rather than replace the semantic transaction review.
- Failure/manual trace: tampered manifest -> nonzero before launch; early child zero -> ledger mismatch -> one fail completion; leader failure/interrupt -> retained owned identities -> cleanup -> original nonzero. Timing failure cannot convert to pass.
- Policy/adversarial lens: safe prohibition, direct enablement, seven compound separators and missing source exercised; unsafe wording is checked clause-wise via existing shared helper. Reviewed missing fields, symlink paths, duplicate IDs/JSON keys, misleading live index and altered post-call assertion.
- Regression lens: original negative helper contracts and all frozen mutations/restore paths preserved. Current LV001/LV002/LV003 and Spec QA re-assessments remain required after expected source changes; prior grades are not implicitly current.
- Current source review: no additional source defect identified after the last mapping/CLI correction. This is not formal implementation PASS; final source and actual-runtime full, freshness assessments and high-risk formal gate remain pending.

## Instruction Refresh

- Status: performed-full after context compaction
- Contracts: AGENTS, operating model, routing, risk, permissions, autopilot, phase 3/4/7, quality and contract compliance
- Reviewed baseline: clean 03fb788, accepted plan/spec, current dependency QA, checkpoint, reference inventory
- Drift/conflict: none unresolved; historical planning approvals remain historical

## Accepted Closure After Final Verification

- The pending statements above describe the preserved pre-verdict boundary, not the current task state.
- Final reviewed thirteen-path digest: a70de995e0acc04c539624fbd979c9b8e3eea1677a64786379d41bde6a6b9cf5.
- Current source full passed in 765 seconds and actual-runtime full in 612 seconds, with 694 unique smoke cases and one completion marker; first structural-consumer failure remains recorded.
- Genuine current prerequisite regression and LV004 Spec QA completed before formal quality. Current Phase 5 run lv004-quality-2026-09-30 is PASS with findings-first review, complete producer-consumer/adversarial evidence and no unresolved material findings.
- Phase 6, completed Distillation State and the single AI System handoff are recorded. Cadence 1/3; final checkpoint remains due after LV006. Local source commit authorized; no push.
