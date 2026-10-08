# Current Compatibility Reassessment

## Metadata

- Project: ai-workflow-lean-validation-v1
- Date: 2026-10-05
- Result: PASS
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: recovery-phase-3-lv-val-003-scoped-selection-spec-qa-dependency-scope-20261005
- Artifact kind: spec-qa
- Project/task identity: ai-workflow-lean-validation-v1:LV-VAL-003-scoped-selection
- Assessed source HEAD: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05
- Assessed worktree digest: 80d3177f4913369e920a7b1902eaf53dea735f2cfa478fad833be6396735c6ec
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts
| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| workflow-source | .systems/scripts/validate-workflow | bbc84b8ad9106d748a141310b0bc847844fa72537e36994857dd74a53b85de6b |
| workflow-source | .systems/scripts/lib/validation-scope.py | 2aaeaa6214dfa56d207ca0b5a6ba1e85ad67388ba87a029947e19ba391e02cb7 |
| workflow-source | .systems/scripts/lib/validation-checks.json | f2c05eeb9e38e7fa3840669e359daa0456f4e39bcf2f3d7ad242c71d9ebd49e6 |
| workflow-source | .systems/scripts/check-status-consistency | 4a721fc4d99511ca706d2ccbd17ea002c7420c1784018f85178000bc77019324 |
| workflow-source | .systems/scripts/check-qa-evidence | 70d603f279aef46c450307d540de96a911bf7ca2de43df233dbc0bb2e1ebcd62 |
| workflow-source | .systems/scripts/check-distillation-state | 20ec43afbcb1409d464a987ed8b28a3514821ba56e237353368713e0a78a3ad9 |
| workflow-source | .systems/scripts/check-naming | 972ed216bfa5d7cfff4a2f6653dbf4443f25e60dc71412ab7e2f4176ae5c76f5 |
| workflow-source | .systems/ai/core/validation-profiles.md | 074455d115e2d084cddd96898fc456a216419cc4b8545e23acb86bd5ff5d0128 |
| workflow-source | .systems/ai/core/validation-routing.md | cddfd9a29953477d24d314b5cc171e55d7bb7e19f4bde3a51e1fb9f36e82aaa1 |
| workflow-source | .systems/ai/core/contract-compliance.md | b58ac40ab35fa5bc3005481f08d0cfb988fa3299abdb2929d6b8a5dc7de32281 |
| workflow-source | .systems/scripts/check-validator-smoke-tests | c78b46e327c13360747246e9c401b02ebaa4cc5840cdd114b5c67bd9023a3c4a |
| workflow-source | .systems/scripts/smoke/common.sh | d27babc3927de3538a42ccbd7dbc98251092e388fddf2745e0962f124453d688 |
| workflow-source | .systems/scripts/smoke/manifest.json | 5ed5310eedc1c7aab47872467cb116ff8d4367dc29465b04282557f260957b14 |
| workflow-source | .systems/scripts/smoke/core.sh | 2fa1ac0c1d34a9622b865e4b3881b2b895ac8020fec905374bb19dcb4189894a |
| workflow-source | .systems/scripts/smoke/policy.sh | d7cd1a55d842128afa039fbcf6b3f9f80a1e0741fb3793c7a9f35e8d86adc6a9 |
| workflow-source | .systems/scripts/smoke/quality.sh | df3e514dd8945369367a4a2d024f2ec121ac9f416db8a8f1e1f411c3e1fc08da |
| workflow-source | .systems/scripts/smoke/skills.sh | 7a5b36cc5fadc9c16329d8e28d363352a2e30a4dc1b995630d4c2397062d414d |
| workflow-source | .systems/scripts/smoke/workspace.sh | 1c36c1035dfaba35a3722536cea159ec6a39dc7c8e8e346da37a3e02a4091c4c |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | specs/phase-3-lv-val-003-scoped-selection-specification.md | 8946cc504318ec55ebf2bdf8736109f44f8dac737740655e5f2bb4bfb1fa9f22 |
| owning-project-evidence | quality/phase-5-lv-core-001-verdict-integrity-quality.md | af3d7f50d4405199cb49c0c77270ba4ee89b987a5965ca26daaa7132bfb491b3 |
| owning-project-evidence | quality/phase-5-lv-obs-002-baseline-quality.md | cee0efee08c647a2efed2b1099db6a92f933b10c2d2107fe3a6afaf4ff6dd19d |
| owning-project-evidence | implementation/lv004-current-source-audit.json | 02c71b7cb8bf635ceaa4ad53efea957ce9ee3b7875e5fe3328dd0638ec891fba |
| owning-project-evidence | implementation/lv004-adversarial-source-final-results.json | 158efe6594e18df72ca1bad3cfc0755357bcce3635715e42b780336d09e86db0 |
| owning-project-evidence | implementation/lv004-equivalence-retest/equivalence-results.json | 4ef2931515af73ca3f6bd01da801184b0b740be98fd684935f44f2626d88892f |
| owning-project-evidence | implementation/lv004-protected-mutations/results.json | 3243e9fd4ee0fc26d43a0bebd9cb69c6f47e52159060d993ecc2cb28df9c40ee |
| owning-project-evidence | implementation/lv004-source-full-final-002.log | 2d8b33366d67adf984631d636cf8c0eb636bc37d1b5335305d8982348a78d988 |
| owning-project-evidence | history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-val-003-scoped-selection-spec-qa.md | 01890099bb897bd57830e37f17923e996b9aa3439aa392e7901156cd7e00b2d0 |

### Evidence
- Current semantic compatibility review: accepted task/specification scopes, completed/deferred task rows, original DoD conclusions and failure boundaries were re-read. All original owning-project inputs matched their recorded hashes before rendering.
- Source deltas add opt-in execution/commit capabilities; legacy V2/schema1/schema2 readers remain strict. The new fixed dependency classification affects inventory and both evidence readers only. Every other runtime link remains rejected; excluded dependencies cannot supply evidence.
- Fresh full product validation in an isolated current-worktree fixture completed with all five smoke groups and no skipped tests; the additional dependency regression and frozen manifest integrity passed. This is source verification, not an assertion that the original upstream runtime had already passed its full gate.
- No old receipt was reused: old HMAC/environment fingerprints and performance results remain historical. This run makes no new timing or whole-agent improvement claim.
- Original findings and project outcomes remain unchanged. LV005 stays deferred with FAIL and unmet paired-model/isolation evidence; there is no new model evaluation or promotion.
- Original report preserved byte-for-byte at history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-val-003-scoped-selection-spec-qa.md; the new assessment has a distinct run identity and current input graph. Historical owner closure remains scoped to its original decision; this review grants no new final-owner-yes, publication or activation.

### QA Verification Scope
Current specification coherence, scope, DoD, producer-consumer mapping and dependency interfaces; not a product implementation verdict.
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
- Producers/consumers reviewed: runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.
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

## Historical Runs
- Run ID: lv003-spec-regression-lv004-2026-09-30
- Original report: history/2026-10-05-pre-dependency-scope/recovery-phase-3-lv-val-003-scoped-selection-spec-qa.md
- Original SHA-256: 01890099bb897bd57830e37f17923e996b9aa3439aa392e7901156cd7e00b2d0
