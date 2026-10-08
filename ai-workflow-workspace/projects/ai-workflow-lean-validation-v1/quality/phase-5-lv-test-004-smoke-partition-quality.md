# Current Compatibility Reassessment

## Metadata

- Project: ai-workflow-lean-validation-v1
- Date: 2026-10-05
- Result: PASS
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: phase-5-lv-test-004-smoke-partition-quality-dependency-scope-20261005
- Artifact kind: implementation-quality
- Project/task identity: ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition
- Assessed source HEAD: b234eb6d8dd13cdab1f5be26fd6efa1b5834fc05
- Assessed worktree digest: 457c37184405830fc17cbe26387369db23d88a7e4742b5d68e3df9f6fe85ec93
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts
| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| workflow-source | .systems/ai/core/commands.md | aba9ca74b7441af8560c6f6d9f36f96feb39a442608202ada348cf9ffbe07c9f |
| workflow-source | .systems/ai/core/validation-observability.md | e7a07bf6904be007b782368e6a279f9fa012f16dc685c06987633cee430ab347 |
| workflow-source | .systems/scripts/check-validation-completion | ea357f5fb71f3c0522554c135cfcebfb0064d76e32fb762ea4e583b592b6a3ba |
| workflow-source | .systems/scripts/check-validation-observability | 6309030c4497d3b3d59794053e1bf4770ab0623f98b48402b26474846bf6b17f |
| workflow-source | .systems/scripts/check-validator-smoke-tests | c78b46e327c13360747246e9c401b02ebaa4cc5840cdd114b5c67bd9023a3c4a |
| workflow-source | .systems/scripts/smoke/common.sh | d27babc3927de3538a42ccbd7dbc98251092e388fddf2745e0962f124453d688 |
| workflow-source | .systems/scripts/smoke/core.sh | 2fa1ac0c1d34a9622b865e4b3881b2b895ac8020fec905374bb19dcb4189894a |
| workflow-source | .systems/scripts/smoke/manifest.json | 5ed5310eedc1c7aab47872467cb116ff8d4367dc29465b04282557f260957b14 |
| workflow-source | .systems/scripts/smoke/policy.sh | d7cd1a55d842128afa039fbcf6b3f9f80a1e0741fb3793c7a9f35e8d86adc6a9 |
| workflow-source | .systems/scripts/smoke/quality.sh | df3e514dd8945369367a4a2d024f2ec121ac9f416db8a8f1e1f411c3e1fc08da |
| workflow-source | .systems/scripts/smoke/skills.sh | 7a5b36cc5fadc9c16329d8e28d363352a2e30a4dc1b995630d4c2397062d414d |
| workflow-source | .systems/scripts/smoke/workspace.sh | 1c36c1035dfaba35a3722536cea159ec6a39dc7c8e8e346da37a3e02a4091c4c |
| workflow-source | README.md | 929044c1fbafd59509a6925ca745664ba5067cab9e8a67010ba8cfd9bdc8c77d |
| workflow-source | .systems/scripts/validate-workflow | bbc84b8ad9106d748a141310b0bc847844fa72537e36994857dd74a53b85de6b |
| workflow-source | .systems/scripts/update-from-upstream | a157da8343bc7ef2fb2997684889b71a417005da57a28adcea8bb49c6be2d1c9 |
| workflow-source | .github/workflows/ai-workflow-validate.yml | ecf8ecb9563336fbe94085f89fbf8f094eca52263677858a8280e0ae4b38a9ff |
| workflow-source | .systems/scripts/lib/validation-timing.py | 7bde59bbd1508ad435d950bb538cf5e5242d525ef2ac09f9e17dadad2e349678 |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | specs/phase-3-lv-test-004-smoke-partition-specification.md | 8b8bf088f844113e9dc3aec72ccf7ef84eb045a27442857df22abf0b73d01ab5 |
| owning-project-evidence | quality/recovery-phase-3-lv-test-004-smoke-partition-spec-qa.md | 715898134e4f58b1aa0ae10458c3a2f7eea66241ce8222c75cb864d461d3bde6 |
| owning-project-evidence | quality/phase-4-lv-test-004-smoke-partition-implementation-result.md | f9ef4e89ef748b2822999be23c99c37949eb98c133ed1aec174df810f07605a5 |
| owning-project-evidence | quality/phase-5-lv-core-001-verdict-integrity-quality.md | af3d7f50d4405199cb49c0c77270ba4ee89b987a5965ca26daaa7132bfb491b3 |
| owning-project-evidence | quality/phase-5-lv-obs-002-baseline-quality.md | cee0efee08c647a2efed2b1099db6a92f933b10c2d2107fe3a6afaf4ff6dd19d |
| owning-project-evidence | quality/phase-5-lv-val-003-scoped-selection-quality.md | 6bc135036731deb285276fc8bd0dca002b06cec476f54358b6a82883e4c55e0c |
| owning-project-evidence | implementation/lv004-current-source-audit.json | 02c71b7cb8bf635ceaa4ad53efea957ce9ee3b7875e5fe3328dd0638ec891fba |
| owning-project-evidence | implementation/lv004-adversarial-source-final-results.json | 158efe6594e18df72ca1bad3cfc0755357bcce3635715e42b780336d09e86db0 |
| owning-project-evidence | implementation/lv004-equivalence-retest/equivalence-results.json | 4ef2931515af73ca3f6bd01da801184b0b740be98fd684935f44f2626d88892f |
| owning-project-evidence | implementation/lv004-protected-mutations/results.json | 3243e9fd4ee0fc26d43a0bebd9cb69c6f47e52159060d993ecc2cb28df9c40ee |
| owning-project-evidence | implementation/lv004-source-full-final-002.log | 2d8b33366d67adf984631d636cf8c0eb636bc37d1b5335305d8982348a78d988 |
| owning-project-evidence | implementation/lv004-actual-runtime-full-001.log | c6e75556ea4f97c2c321238980afc4465c19bcd4061b15622a3be919b9e2a7b0 |
| owning-project-evidence | history/2026-10-05-pre-dependency-scope/phase-5-lv-test-004-smoke-partition-quality.md | 970c253a995d415e1886200b8a428318a8dd77d48b622959106eb9b659ef7901 |

### Evidence
- Current semantic compatibility review: accepted task/specification scopes, completed/deferred task rows, original DoD conclusions and failure boundaries were re-read. All original owning-project inputs matched their recorded hashes before rendering.
- Source deltas add opt-in execution/commit capabilities; legacy V2/schema1/schema2 readers remain strict. The new fixed dependency classification affects inventory and both evidence readers only. Every other runtime link remains rejected; excluded dependencies cannot supply evidence.
- Fresh full product validation in an isolated current-worktree fixture completed with all five smoke groups and no skipped tests; the additional dependency regression and frozen manifest integrity passed. This is source verification, not an assertion that the original upstream runtime had already passed its full gate.
- No old receipt was reused: old HMAC/environment fingerprints and performance results remain historical. This run makes no new timing or whole-agent improvement claim.
- Original findings and project outcomes remain unchanged. LV005 stays deferred with FAIL and unmet paired-model/isolation evidence; there is no new model evaluation or promotion.
- Original report preserved byte-for-byte at history/2026-10-05-pre-dependency-scope/phase-5-lv-test-004-smoke-partition-quality.md; the new assessment has a distinct run identity and current input graph. Historical owner closure remains scoped to its original decision; this review grants no new final-owner-yes, publication or activation.

### Definition Of Done Validation
| DoD Item | Result | Evidence |
| --- | --- | --- |
| V4-01 complete unique ownership | PASS | 674 reference + 20 supplemental IDs; exact command/group/line/digest/region mapping and missing/duplicate mutation rejection. |
| V4-02 real outside assertion preservation | PASS | 21 exact raw regions, 95 assertion points / 14 failure branches / one fixture; removal of a post-call assertion rejected. |
| V4-03..04 independent repeat/order | PASS | Fresh standalone groups in reverse order and repeated all runs; pure common import without filesystem effects. |
| V4-05 failure, timeout, interrupt and cleanup | PASS | Twelve latest actual fault probes; original statuses and one parent marker retained; no live own orphan in measured paths. |
| V4-06 protected real mutations | PASS | Both original and split reject unconditional-zero status and observability validators with the same case/cause. |
| V4-07 all coverage and typed outcome equivalence | PASS | All 674 original identities executed; 552 negative diagnostic/status matches; actual final full 694 unique cases. |
| V4-08 invalid CLI/manifest cannot succeed | PASS | Enum parser and exact live manifest rejection; missing fields/source, duplicate JSON keys, altered owner/region/source tested. |
| V4-09 fallback and honest evidence | PASS | Immutable parent runner retained; completed reference equivalence permits split, not speed/quality inference; full/CI/updater untouched. |

### Intent / Plan / Spec Compliance
- Result: PASS
- Owner instruction reviewed: yes
- Accepted plan reviewed: yes
- Accepted spec reviewed: yes
- Scope/out-of-scope reviewed: yes
- Acceptance criteria reviewed: yes
- Compliance status: aligned
- Wrong problem solved: no
- Owner instruction mismatch: no
- Accepted plan mismatch: no
- Accepted spec mismatch: no
- Acceptance criteria gap: no
- Scope creep: no
- Underbuild: no
- Overbuild: no
- Evidence: Accepted task scope and current owner approval; no external effects, inferred authority, lost coverage or unsupported performance claim.

### Adaptive Data / Integration Verification Matrix
- Applicability: required
- Not-applicable reason: none; executable/typed evidence flow.

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| 674 reference / 20 supplemental cases and source-bound manifest | exactly one owner/command/region per ID, pure common setup | standalone subset or complete all | omitted/moved assertion, duplicate/missing execution, false full | nonzero before launch or final coverage failure | current full and manifest corruption cases | manifest to live command to ledger to parent completion |
| negative helper and mutated protected validator | exact expected status and cause | same rejection as original runner | reserved or unrelated exit accepted as intended failure | original failure propagated | 552 matched diagnostics and two old/new mutations | mutated status consumer to typed negative outcome |
| observed own process tree and timing sink | retained PID/start identity plus one wall | truthful failure/interrupt/timeout, no live own orphan in tested paths | successful completion on incomplete execution or cleanup failure | preserved nonzero; cleanup failure explicitly fails | twelve final-source fault probes | failing leader to retained descendant to cleanup to marker/wall |

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
- Producers/consumers reviewed: manifest/group/common producers, exact executed ledger, public/group lifecycle, full/CI/updater structural consumers, timing reader and current QA inputs.
- Required-field mapping: complete
- Evidence: Full source/artifact review and before/after failure traces; mapped schemas, typed readers and exact check/ID coverage. Tests support rather than determine this verdict.
- Compatibility re-review: current accepted specs and source producer/consumer graph reviewed; fixed dependency exclusion, metadata/status, immutable smoke assertions and failed-state rejection checked.
- Freshness evidence: new current hashes and isolated full product verification; original measurements and approval facts remain only historical.

### Findings
- Blockers: none
- Unresolved findings: none
- Residual risk: Linux CI unrun; local synthetic tests and explicit source scope are bounded evidence, not an absolute guarantee.

### Quality Gate
- Intent / Plan / Spec Compliance PASS: yes
- Review Completeness Gate PASS: yes
- Cross-contract consistency aligned: yes
- Risk/work mode compatibility aligned: yes
- Negative-space / adversarial review complete or not applicable: yes
- Automated evidence treated as supporting-only: yes
- Post-fix full re-review complete or not required: yes
- Instruction baseline current: yes
- Closure freshness current: yes
- Policy-boundary adversarial matrix complete or not applicable: yes
- Producer-consumer field audit complete or not applicable: yes
- Required-field mapping complete or not applicable: yes
- 100% DoD satisfied: yes
- No known bug in scope: yes
- No regression in changed/direct paths: yes
- Edge cases covered or explicitly rejected: yes
- Explicit evidence attached: yes
- Quality result: PASS
- Required next phase: phase-6-distillation

### Gate Decision
- Result: PASS
- Next route: compatibility review complete; original closure remains historical

## Historical Runs
- Run ID: lv004-quality-2026-09-30
- Original report: history/2026-10-05-pre-dependency-scope/phase-5-lv-test-004-smoke-partition-quality.md
- Original SHA-256: 970c253a995d415e1886200b8a428318a8dd77d48b622959106eb9b659ef7901
