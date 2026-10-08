# Current Compatibility Reassessment

## Metadata

- Project: ai-workflow-lean-validation-v1
- Date: 2026-10-05
- Result: FAIL
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: recovery-phase-3-lv-ux-005-instruction-efficiency-spec-qa-dependency-scope-20261005
- Artifact kind: spec-qa
- Project/task identity: ai-workflow-lean-validation-v1:LV-UX-005-instruction-efficiency
- Assessed source HEAD: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05
- Assessed worktree digest: 32ed4d3b568962290b5ca921dcb7052dce1a0a30907bff11b3bddb27b1c8331f
- Input artifacts: see table
- Verdict: FAIL
- Gate Decision: FAIL

### Input Artifacts
| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | specs/phase-3-lv-ux-005-instruction-efficiency-specification.md | 6fb05dabf1af09c0ca25c61e57670d1ca797f4fde61a0d1bf104503abccd9853 |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | architecture/phase-1-architecture.md | 0b3f2c625b0149b8df515d5558e8977bcc638850b8a5e912756126d2198c80be |
| owning-project-evidence | decisions/lv-dec-009-eval-isolation.md | 503d3d2f63715ce9b15d893fe1821a6ad8a6c2b7993f2ebcaac41048201391c3 |
| owning-project-evidence | reviews/lv005-infrastructure-readiness-review.md | 8cffe2e9772a1bc5a6a67044e824525b41279d65351d73173389a4299a683fa2 |
| owning-project-evidence | implementation/lv005-runtime-preflight-004/metadata.json | 8b9e9e28a9692b7ea25d9da56637f13c0d18e0096ba786ae7831a50275e4a8f4 |
| owning-project-evidence | implementation/lv005-exec-context-probe-002/summary.json | 1fd8f213e82b60b7d3786b12f20616eb9fe78a8b35b42196b5cda9295a5aa960 |
| workflow-source | .systems/ai/core/permissions.md | 8de3eaefc9dc09e39fc061ed92aa66d5078b40d4166c6aa16e008c78b1d64baa |
| workflow-source | .systems/ai/core/autopilot.md | 6b747b35b75b10f5b4601def1986eb9101b868f50770449fa32513ef3470b5ae |
| owning-project-evidence | history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-ux-005-instruction-efficiency-spec-qa.md | 480179376bdae65e8a4f3dcd5df02ef5404366b40792b4100d998af5908ed4a7 |

### Evidence
- Current semantic compatibility review: accepted task/specification scopes, completed/deferred task rows, original DoD conclusions and failure boundaries were re-read. All original owning-project inputs matched their recorded hashes before rendering.
- Source deltas add opt-in execution/commit capabilities; legacy V2/schema1/schema2 readers remain strict. The new fixed dependency classification affects inventory and both evidence readers only. Every other runtime link remains rejected; excluded dependencies cannot supply evidence.
- Fresh full product validation in an isolated current-worktree fixture completed with all five smoke groups and no skipped tests; the additional dependency regression and frozen manifest integrity passed. This is source verification, not an assertion that the original upstream runtime had already passed its full gate.
- No old receipt was reused: old HMAC/environment fingerprints and performance results remain historical. This run makes no new timing or whole-agent improvement claim.
- Original findings and project outcomes remain unchanged. LV005 stays deferred with FAIL and unmet paired-model/isolation evidence; there is no new model evaluation or promotion.
- Original report preserved byte-for-byte at history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-ux-005-instruction-efficiency-spec-qa.md; the new assessment has a distinct run identity and current input graph. Historical owner closure remains scoped to its original decision; this review grants no new final-owner-yes, publication or activation.

### QA Verification Scope
Specification coherence, accepted DoD, current dependencies, runtime safety, testability, failure handling and implementation readiness. This is not an implementation Phase 5 verdict.
Current follow-up is source compatibility re-review of the same accepted artifact scope, not new implementation or final owner closure.

### Artifact QA Completeness Gate
- Owner intent and governing sources reviewed: accepted plan/architecture, LV-DEC-002/003/008 and current spec, permission/autopilot contracts.
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned; unchanged tracked source, current a7d66c7
- Post-fix full artifact re-review: completed; stale authority wording corrected, real runtime limitation retained
- Evidence reviewed: nine bound current input artifacts, local and model infrastructure traces, readiness protocol
- Skipped or unreadable sources: full authenticated hosted-provider context unavailable; no behavioral baseline/candidate runs
- Residual risk: custom-provider local request capture is not hosted-provider context/tool equality; global context remains uncontrolled
- Closure freshness: current

### Checks
| Check | Result | Evidence | Finding |
| --- | --- | --- | --- |
| Source/authority/dependencies | PASS | Original execution approvals resolved; accepted LV003/LV004 outputs preserved | none |
| Scope and DoD preservation | PASS | No shorter text promoted or behavioral criteria waived | none |
| Historical approval drift | PASS | Current spec no longer claims original decisions/model unselected | corrected preparation drift |
| Safe controlled runtime context | FAIL | Actual exec has four host entries and one global AGENTS block; empty-home login unavailable | material P2 open |
| Execution readiness | FAIL | No verified frozen same-context method or paired behavioral evidence | LV-DEC-009 required |

### Review Completeness Gate
- Status: complete for this failing artifact assessment
- Cross-contract consistency: aligned
- Risk/work mode compatibility: aligned
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes
- Negative-space / adversarial review: completed; zero exit, unobserved denial claim, interpreter failure, preview/exec mismatch, ambient guidance, credential-copy boundary
- Automated evidence role: supporting-only
- Post-fix full re-review: completed
- Reviewed baseline: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05; exact current input table; reviewed compatibility follow-up on 2026-10-05
- Instruction refresh: performed-full
- Instruction baseline: current
- Closure freshness: current
- Policy-boundary adversarial matrix: not-applicable; no policy/validator source change in LV005 preparation
- Producer-consumer field audit: completed; configuration, request composer, command trace, fixture result, preflight and promotion consumer audited
- Producers/consumers reviewed: infrastructure review evidence table and refreshed LV005 protocol
- Required-field mapping: complete; missing safety evidence is not replaced by unrelated successful fields
- Compatibility re-review: current accepted specs and source producer/consumer graph reviewed; fixed dependency exclusion, metadata/status, immutable smoke assertions and failed-state rejection checked.
- Freshness evidence: new current hashes and isolated full product verification; original measurements and approval facts remain only historical.

### Findings
- Blockers: material P2 open; actual context isolation is not established.
- Unresolved findings: LV-DEC-009 runtime setup or explicit scope disposition.
- Corrected findings: code-mode host setup, false process-success interpretation, unobserved denial evidence, system Python/xcrun dependence and stale original-approval wording.
- No assertion of private-data exposure or absence of private ambient context is supported by this limited evidence.

### Gate Decision
- Result: FAIL
- Next route: deferred owner-controlled restart; original blockers remain

## Historical Runs
- Run ID: lv005-spec-readiness-2026-09-30
- Original report: history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-ux-005-instruction-efficiency-spec-qa.md
- Original SHA-256: 480179376bdae65e8a4f3dcd5df02ef5404366b40792b4100d998af5908ed4a7
