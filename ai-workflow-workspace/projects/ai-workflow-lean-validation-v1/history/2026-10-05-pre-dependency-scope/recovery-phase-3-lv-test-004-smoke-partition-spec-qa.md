# spec-qa: ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition

## Metadata

- Project: ai-workflow-lean-validation-v1
- Task/package ID: LV-TEST-004-smoke-partition
- Date: 2026-09-30
- Result: PASS
- QA verification contract: `full-qa-verification-v2`
- Owner approval: LV-DEC-008; evidence-backed gate only.

## Historical Run: lv004-refreshed-spec-2026-09-30

- Run ID: lv004-refreshed-spec-2026-09-30
- Artifact kind: spec-qa
- Project/task identity: ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition
- Assessed source HEAD: 03fb78819a0d0f8e413e05e2f7d13573f63c85d8
- Assessed worktree digest: bd4a0d5c902d578974f07e799879b27bad4456682b38c323bf04c64546cde5af
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| workflow-source | .systems/scripts/check-validator-smoke-tests | d8f5b05e482b65def729dc3b65c5ec89e1e438b1aa0213e21b51038449902ff6 |
| workflow-source | .systems/scripts/lib/validation-timing.py | 7bde59bbd1508ad435d950bb538cf5e5242d525ef2ac09f9e17dadad2e349678 |
| workflow-source | .systems/scripts/report-validation-comparison | e9310176a9ef3f8756d7f894561dff814363b5cb06d74b6c46b2435a64833fdf |
| workflow-source | .systems/scripts/check-validation-completion | 85b2097a03e137ebcb68fb7100856c6548a30c95e08ff793cec77b3e0fec4770 |
| workflow-source | .systems/scripts/check-validation-observability | 166fa0b7e1c8ddbd626b3e470223c61e13d8e755330f6e3a94217e5940d1aea3 |
| workflow-source | .systems/ai/core/validation-observability.md | 4f6040032b67d966a3fd6bb688a6aeb1e701eb446687a02d2439de0c77082e52 |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | specs/phase-3-lv-test-004-smoke-partition-specification.md | 8b8bf088f844113e9dc3aec72ccf7ef84eb045a27442857df22abf0b73d01ab5 |
| owning-project-evidence | quality/phase-5-lv-core-001-verdict-integrity-quality.md | 943977a502486203d643e1f679d27233b0224425c18227fc8fc39a2c8345d919 |
| owning-project-evidence | quality/phase-5-lv-obs-002-baseline-quality.md | e13d55cf632102a353364e69041f03466e817d560607f4c2021506ec3641aa45 |
| owning-project-evidence | quality/phase-5-lv-val-003-scoped-selection-quality.md | d71c1c935b81c7884283e7a1b9138e01b8731b85ba390d5f014c43aa8985fec2 |
| owning-project-evidence | checkpoints/phase-7-checkpoint-2026-09-30-lv001-lv003.md | ec30db858ae4e39e4eff73d7b79b2eb0d37f2c15064a9027da0c59b2446cfad9 |
| owning-project-evidence | implementation/lv004-reference/inventory.json | 1f6a0a32edfd4d1f227968329bb3724d49098c631afb99bd8ec00479963e6c96 |

### Evidence

- Fresh whole-spec review compares owner LV-DEC-008, accepted architecture/plan, current dependency quality and completed checkpoint with HEAD 03fb788.
- Frozen actual inventory contains 674 executed IDs, 110 lexical assertion candidates and 32 source-consumer references. Those counts are not claimed equivalence; exact semantic ownership, mutation and cleanup comparison remain implementation DoD.
- Reviewed all five slice interfaces and V4-01..09: pure common imports, disposable independent roots, all union, exact status/diagnostics, external assertions, marker/timing parents, repeat/permutation and failure cleanup.
- Existing literal consumer references require a live-validated coverage index. A disconnected comment/index cannot substitute for actual test membership. New outside-ceiling consumers require reconciliation before writes.
- Exploratory workspace group passed in isolation. A quality prototype exposed a split backup/mutation transaction at original line 4052; the boundary was corrected and retest is ongoing. Neither the failed attempt nor the pending equivalence is an implementation PASS.
- Findings-first artifact review: no unresolved specification blocker. Source implementation, actual equivalence and formal Phase 5 remain separate gates; no speed claim, push or closure.


### QA Verification Scope

Current specification coherence, scope, DoD, producer-consumer mapping and dependency interfaces; not a product implementation verdict.

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
- Reviewed baseline: current HEAD and individually bound input sources; prior runs preserved, not reused as current verdict.
- Instruction refresh: performed-full
- Instruction baseline: current
- Closure freshness: current
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Producers/consumers reviewed: smoke entrypoint, pure helpers, five isolated group producers, manifest ownership, source-consumer references and nine-column timing consumer.
- Required-field mapping: complete
- Evidence: Full refreshed specification, current source and dependency review; explicit assertion/equivalence requirements, CLI/timing and coverage-index field mapping. Runtime equivalence remains an implementation gate. Tests support rather than determine this verdict.

### Findings

- Blockers: none
- Unresolved findings: none
- Residual risk: Linux CI unrun; local synthetic tests and explicit source scope are bounded evidence, not an absolute guarantee.

### Gate Decision

- Spec QA result: PASS
- Can proceed: yes
- Scope: only the assessed artifact/task under LV-DEC-008; no push or final-owner-yes.

## Current QA Run

- Run ID: lv004-spec-current-source-2026-09-30
- Artifact kind: spec-qa
- Project/task identity: ai-workflow-lean-validation-v1:LV-TEST-004-smoke-partition
- Assessed source HEAD: 03fb78819a0d0f8e413e05e2f7d13573f63c85d8
- Assessed worktree digest: 839f5a1b035e5db5ebc5958d84da957561742ad6a1f5614bfef1730b3add3d32
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| workflow-source | .systems/scripts/check-validator-smoke-tests | a2c50575a3dba189d3ad3aef5976da7db67eea468c8540be39b095457dbe465d |
| workflow-source | .systems/scripts/smoke/common.sh | 3caa22344730df6b565b687eb0d68e2964ed0d143ee69c27c218508e03aa1db9 |
| workflow-source | .systems/scripts/smoke/manifest.json | 64dc59a39ab2862643010c22e898cfcd16601674fb85909e70589656535696d4 |
| workflow-source | .systems/scripts/smoke/core.sh | fbb76e3894444f91a527ce41628ea984c0ec7d8ff811a3587077f8e11bd2ba2d |
| workflow-source | .systems/scripts/smoke/policy.sh | 9260731823487ef869be343da6ef8f3754d7b56dcc39c5edb44be17df85331b5 |
| workflow-source | .systems/scripts/smoke/quality.sh | e45a8254d9739094962dde329847ddfe117672f9b4f126254f623d848c396de6 |
| workflow-source | .systems/scripts/smoke/skills.sh | 99c5db23482ea390c991973d4f6a11155a4f88365d50f65df661ad6e99b6a30b |
| workflow-source | .systems/scripts/smoke/workspace.sh | 7e9a435dcbaae8f5e5357ad50e68236e2c1eaa040134017d4b7d2f0ef6e07d68 |
| workflow-source | .systems/scripts/check-validation-observability | 6309030c4497d3b3d59794053e1bf4770ab0623f98b48402b26474846bf6b17f |
| workflow-source | .systems/scripts/check-validation-completion | ea357f5fb71f3c0522554c135cfcebfb0064d76e32fb762ea4e583b592b6a3ba |
| workflow-source | .systems/ai/core/commands.md | 0f5419df7215119197e3251648863e693cf94224657a6830d3bf57ee4f2a3e26 |
| workflow-source | .systems/ai/core/validation-observability.md | 42ab0c5c3df49f65f1736ecc93e69d89a2037fc12f3b4ed192474db3a8dfbf26 |
| workflow-source | README.md | 3a97a1633219a72c0b414b50fe8bc810bc049b99a69f8a71a0b8b2bacf6ffccf |
| owning-project-evidence | planning/phase-2-project-plan.md | b1259cfb3b25226f51d00d2db8c94923283ac78a37709eb7ea4176fc0640c2a1 |
| owning-project-evidence | specs/phase-3-lv-test-004-smoke-partition-specification.md | 8b8bf088f844113e9dc3aec72ccf7ef84eb045a27442857df22abf0b73d01ab5 |
| owning-project-evidence | quality/phase-5-lv-core-001-verdict-integrity-quality.md | 23cf6b0eebd45a7d47bddb147be775a1a1f42b86ed843b3b899686be3f08af9a |
| owning-project-evidence | quality/phase-5-lv-obs-002-baseline-quality.md | bddb115b40967e975a496392199f9de7d6b294031fe587cec4eb4282dd6d9166 |
| owning-project-evidence | quality/phase-5-lv-val-003-scoped-selection-quality.md | dde6206c7bbd96d669c3a646ede580483ace034b030abdd14303cdb76228afa7 |
| owning-project-evidence | implementation/lv004-current-source-audit.json | 02c71b7cb8bf635ceaa4ad53efea957ce9ee3b7875e5fe3328dd0638ec891fba |
| owning-project-evidence | implementation/lv004-adversarial-source-final-results.json | 158efe6594e18df72ca1bad3cfc0755357bcce3635715e42b780336d09e86db0 |
| owning-project-evidence | implementation/lv004-equivalence-retest/equivalence-results.json | 4ef2931515af73ca3f6bd01da801184b0b740be98fd684935f44f2626d88892f |
| owning-project-evidence | implementation/lv004-protected-mutations/results.json | 3243e9fd4ee0fc26d43a0bebd9cb69c6f47e52159060d993ecc2cb28df9c40ee |
| owning-project-evidence | implementation/lv004-source-full-final-002.log | 2d8b33366d67adf984631d636cf8c0eb636bc37d1b5335305d8982348a78d988 |

### Evidence

- Fresh full LV004 specification and V4-01..09 review against all thirteen current paths, whole preserved transactions, exact field-level ownership and updated direct consumers.
- All 674 old cases, 110 semantically classified outside-wrapper points, 34 nested Python assertion/failure lines and 21 frozen regions have one explicit ownership mapping. Pure helper import has no setup effects.
- Actual reference/candidate all, repeated reverse standalone groups, 552 cause/status matches and two protected mutations prove preserved-reference behavior; final 694-case source full and twelve latest process/integrity probes cover subsequent supplemental/mapping/supervisor fixes.
- Missing system-skills literal discovered by the prior full is fixed as a live source/command binding, not a decorative comment or bypass. Re-read all 32 inventoried direct consumers including full runner structural checks; no consumer edit outside ceiling needed.
- Fallback is explicit and remains available from the frozen parent source; no speedup, CI execution, task completion or owner-final closure is inferred from counts.


### QA Verification Scope

Current specification coherence, scope, DoD, producer-consumer mapping and dependency interfaces; not a product implementation verdict.

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
- Reviewed baseline: current HEAD and individually bound input sources; prior runs preserved, not reused as current verdict.
- Instruction refresh: performed-full
- Instruction baseline: current
- Closure freshness: current
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Producers/consumers reviewed: runner, scope JSON/registry, runtime consumers, current QA reader, timing and checkpoint contract.
- Required-field mapping: complete
- Evidence: Full source/artifact review and before/after failure traces; mapped schemas, typed readers and exact check/ID coverage. Tests support rather than determine this verdict.

### Findings

- Blockers: none
- Unresolved findings: none
- Residual risk: Linux CI unrun; local synthetic tests and explicit source scope are bounded evidence, not an absolute guarantee.

### Gate Decision

- Spec QA result: PASS
- Can proceed: yes
- Scope: only the assessed artifact/task under LV-DEC-008; no push or final-owner-yes.
