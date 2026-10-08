# Current Compatibility Reassessment

## Metadata

- Project: ai-workflow-lean-validation-v1
- Date: 2026-10-05
- Result: PASS
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: recovery-phase-3-lv-qa-006-integration-spec-qa-dependency-scope-20261005
- Artifact kind: spec-qa
- Project/task identity: ai-workflow-lean-validation-v1:LV-QA-006-integration
- Assessed source HEAD: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05
- Assessed worktree digest: 9d9a87999320a1806d2cfed328e1e56596f5b686da85a7d120f0cf480d455d60
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts
| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | planning/lv005-deferral-plan-amendment.md | f056ccdc2b632568346a213afeaccd09550d6616d93cd664cf5ecbe65e948da8 |
| owning-project-evidence | architecture/phase-1-architecture.md | 0b3f2c625b0149b8df515d5558e8977bcc638850b8a5e912756126d2198c80be |
| owning-project-evidence | quality/phase-1-architecture-qa.md | 502da3e34dc881799e30e92ac800ee2c6c2311e108412717518d4038bbdde4b6 |
| owning-project-evidence | context.md | 147bfd7aab2cd26c86eee4661b18bb6de3d7ddd89b67095f1b1cf4d6455987d6 |
| owning-project-evidence | decisions/lv-dec-010-lv005-deferral.md | 9d7a9e3e447861781ee6809cae3722def162927f025e78988ada9d6945f3576d |
| owning-project-evidence | reviews/lv005-deferral-plan-and-lv006-readiness-review.md | 0a61da94909623f8d8121ae271f8225839588bf1e16a7be72e85e1d171179716 |
| owning-project-evidence | specs/phase-3-lv-qa-006-integration-specification.md | deb8f9694d0ad4049d6684a668224be76d4f54796c0941d35ea36da6550ef74b |
| owning-project-evidence | specs/lv006-current-scope-amendment.md | 065d1157dcc5bf97d0e3142e7059aca5abbe7c476cebd628ec80ff1579e91c38 |
| owning-project-evidence | quality/recovery-phase-2-plan-qa.md | 6ce95a7d00cf79826e97d13f6345b44784f630167b013882f5556deec33fba90 |
| owning-project-evidence | tasks.md | 2a32cd41678f4720320d69bf51cf12bb1783832ed8586df14237ba8a3aa90387 |
| owning-project-evidence | implementation/lv004-current-source-audit.json | 02c71b7cb8bf635ceaa4ad53efea957ce9ee3b7875e5fe3328dd0638ec891fba |
| owning-project-evidence | quality/phase-5-lv-core-001-verdict-integrity-quality.md | af3d7f50d4405199cb49c0c77270ba4ee89b987a5965ca26daaa7132bfb491b3 |
| owning-project-evidence | quality/phase-5-lv-obs-002-baseline-quality.md | cee0efee08c647a2efed2b1099db6a92f933b10c2d2107fe3a6afaf4ff6dd19d |
| owning-project-evidence | quality/phase-5-lv-val-003-scoped-selection-quality.md | 6bc135036731deb285276fc8bd0dca002b06cec476f54358b6a82883e4c55e0c |
| owning-project-evidence | quality/phase-5-lv-test-004-smoke-partition-quality.md | cd8a81ca9b6e91134e25a4ca28216aec4ebb38176e070902aa83ac145539afd3 |
| workflow-source | .systems/ai/workflow/phase-3-spec-qa.md | adbfcdd945f59c6f9e3fe9819264162a853d6c77c6c6a34f2579b3d05e56f7cc |
| workflow-source | .systems/ai/core/full-qa-verification.md | 7ecdb8e2affc94f14460717ad28635dd02cf43be9445a55a2991589752ae5002 |
| workflow-source | .systems/scripts/validate-workflow | bbc84b8ad9106d748a141310b0bc847844fa72537e36994857dd74a53b85de6b |
| workflow-source | .systems/scripts/update-from-upstream | a157da8343bc7ef2fb2997684889b71a417005da57a28adcea8bb49c6be2d1c9 |
| workflow-source | .systems/scripts/smoke/manifest.json | 5ed5310eedc1c7aab47872467cb116ff8d4367dc29465b04282557f260957b14 |
| workflow-source | .github/workflows/ai-workflow-validate.yml | ecf8ecb9563336fbe94085f89fbf8f094eca52263677858a8280e0ae4b38a9ff |
| owning-project-evidence | reviews/lv006-post-capture-review.md | 31b23237a9623d34dfd805f227055736c34b4241a22f9fa7441a9cbad679bcfe |
| owning-project-evidence | history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-qa-006-integration-spec-qa.md | f120b799174a6e96262febd2380997f090e4c5b25c107fe22cc0f83efd78b014 |

### Evidence
- Current semantic compatibility review: accepted task/specification scopes, completed/deferred task rows, original DoD conclusions and failure boundaries were re-read. All original owning-project inputs matched their recorded hashes before rendering.
- Source deltas add opt-in execution/commit capabilities; legacy V2/schema1/schema2 readers remain strict. The new fixed dependency classification affects inventory and both evidence readers only. Every other runtime link remains rejected; excluded dependencies cannot supply evidence.
- Fresh full product validation in an isolated current-worktree fixture completed with all five smoke groups and no skipped tests; the additional dependency regression and frozen manifest integrity passed. This is source verification, not an assertion that the original upstream runtime had already passed its full gate.
- No old receipt was reused: old HMAC/environment fingerprints and performance results remain historical. This run makes no new timing or whole-agent improvement claim.
- Original findings and project outcomes remain unchanged. LV005 stays deferred with FAIL and unmet paired-model/isolation evidence; there is no new model evaluation or promotion.
- Original report preserved byte-for-byte at history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-qa-006-integration-spec-qa.md; the new assessment has a distinct run identity and current input graph. Historical owner closure remains scoped to its original decision; this review grants no new final-owner-yes, publication or activation.

### QA Verification Scope
Composite LV006 spec and dependency/closure disposition; artifact quality only.
Current follow-up is source compatibility re-review of the same accepted artifact scope, not new implementation or final owner closure.

### Artifact QA Completeness Gate
- Owner intent and governing sources reviewed: accepted plan/spec, source contracts and LV-DEC-008.
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned
- Post-fix full artifact re-review: completed
- Evidence reviewed: individual bound current sources and semantic scenario/failure traces.
- Skipped or unreadable sources: none required.
- Residual risk: QA applies only to this artifact; runtime correctness assessed separately.
- Closure freshness: current

### Review Completeness Gate
- Status: complete
- Cross-contract consistency: aligned
- Risk/work mode compatibility: aligned
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: yes
- Negative-space / adversarial review: completed
- Automated evidence role: supporting-only
- Post-fix full re-review: completed
- Reviewed baseline: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05; exact current input table; reviewed compatibility follow-up on 2026-10-05
- Instruction refresh: performed-full
- Instruction baseline: current
- Closure freshness: current
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Producers/consumers reviewed: composite plan/spec, task index, actual quality/capture, deferral decision, current QA reader and checkpoint.
- Required-field mapping: complete
- Evidence: Full source/artifact review and before/after failure traces; mapped schemas, typed readers and exact check/ID coverage. Tests support rather than determine this verdict.
- Compatibility re-review: current accepted specs and source producer/consumer graph reviewed; fixed dependency exclusion, metadata/status, immutable smoke assertions and failed-state rejection checked.
- Freshness evidence: new current hashes and isolated full product verification; original measurements and approval facts remain only historical.

### Findings
- Blockers: none
- Unresolved findings: none
- Residual risk: Linux CI unrun; local synthetic tests and explicit source scope are bounded evidence, not an absolute guarantee.

### Gate Decision
- Result: PASS
- Next route: compatibility review complete; original closure remains historical

### Current Disposition
Included implementation, Phase 6 and required final checkpoint completed; Phase 8 remains separately owner-triggered. LV005 remains deferred, never accepted by this artifact.

## Historical Runs
- Run ID: lv006-spec-included-completion-2026-10-01-final-route
- Original report: history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-qa-006-integration-spec-qa.md
- Original SHA-256: f120b799174a6e96262febd2380997f090e4c5b25c107fe22cc0f83efd78b014
