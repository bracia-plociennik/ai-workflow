# Pre-final Planning Review: CR001 And CR002

## Scope And Baseline
2026-10-04; branch codex/parallel-task-orchestration-v1; HEAD 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1 with pre-existing PTO source changes. PTO-D07 authorizes artifact-only planning. Reviewed original seven-task architecture/plan, two added CRs, delta, task index and both specifications against capture-state.py, validation-scope.py, qa-evidence.py, quality-record.py, parallel-orchestration.py and coordinator-status.py. External TechGrow handoff is a defect hypothesis; no target/client repository was inspected or modified.

## Findings And Fix Loop
- Resolved: snapshot containing QA hash while QA binds snapshot would be circular. Final design is immutable source snapshot -> new reviewer assessment -> recomputed commit binding; no result SHA inside its own commit.
- Resolved: coverage map, decision references and handoff wording still described seven tasks. Plan now maps nine tasks and PTO-D07, with additions' shared impact pending before local commit/handoff.
- Resolved P2: initial AC3/4 blurred ready/completed requirements. Ready may lack distillation; pending-quality may lack Quality. Completed has accepted unique owned distillation. Schema1 structural validity and current qualification remain separate.
- Resolved P2: parent/checkpoint direct-record consumer could miss invalid/duplicate siblings. Task008 now includes bounded collection validation in orchestration plus negative consumer regressions and exact source paths.
- Resolved P2: optional fields could be ignored by old readers. Task009 specifies distinct V3 QA marker/kind and capture schema3, explicit capability dispatch, frozen old-reader rejection tests and no silent migration. Existing V2/schema2 strictness remains.
- Resolved P2: leaf-spec shared-impact wording was publication-only/optional. It now expressly blocks local commit and handoff while pending.
Independent read-only reviewer Lagrange identified the latter four; parent independently confirmed state-specific and source-consumer behavior. Semantic re-review covers whole revised artifact scope, not just changed sentences.
Independent post-fix resolution review found no remaining material blockers. Its remaining non-material delta checkpoint wording was aligned to the same mandatory pre-commit/handoff decision. Parent then reread the delta, both specs and canonical plan for that boundary.

## Adversarial Design Matrix
| Attack / failure | Reviewed design response | Planned executable evidence |
| --- | --- | --- |
| Historical schema1 used as current PASS | Historical validity separate; no gate promotion | Three consumer paths and current gate rejection |
| Schema2 stale HEAD/hash, FAIL or wrong identity | Preserve strict existing current QA | Positive ready/completed then one mutation per invariant |
| Valid target record with duplicate/invalid sibling | Gate requires bounded collection before selecting row | Parent completion and checkpoint negatives |
| repo/core manifest expanded into other projects | Preserve selector population, share semantics only | Foreign/nested/mixed-population fixture |
| QA and source snapshot hash each other | Snapshot excludes reviewer/result output by typed role; QA binds snapshot | Cycle rejection and manual directional trace |
| Commit changes only HEAD | Compare actual scoped tree plus index/live state and immutable QA | Exact-content commit fixture, no restamping |
| Partial staging, hook changes, mode/delete/extra file | Full declared population and live-state mismatch reject | Git mutation table and fail paths |
| Wrong workflow/product repository | Typed identities and explicit approved target root | Equal contents in foreign repository rejected |
| Old reader ignores new proof metadata | Distinct version/discriminator; old consumer must reject current qualification | Frozen old-reader and legacy fallback tests |
| Stored eligible result is replayed | Recompute from live state; output is not authority | Forged binding, changed evidence/approval negatives |
| Missing source proof or unknown dependencies | Unknown/ineligible, re-QA, no PASS | Missing proof/environment coverage tests |
| Explicit no-commit/ignored-only/no-op/worker commit | No commit; one owner controls index; never push/PR/merge by default | Boundary scenarios in isolated Git only |
| Earlier PTO high-risk approval reused for008/009 | New implementation approval/readiness required | Current plan explicitly stops before writes |
| New scope closed with old Phase8 | Old report remains untouched and stale for expanded scope | Final whole-project QA/checkpoint/new Phase8 after implementation |

## Producer-Consumer Audit
| Producer | Consumer | Fields / population obligation | Review disposition |
| --- | --- | --- | --- |
| record and owned capture collection | canonical, scoped, runtime-only readers | schema, identity, state, references, privacy, derived value, duplicates | shared pure validation with trusted adapters; selectors unchanged |
| owning collection | orchestration task/parent/checkpoint gate | unique task row, completed, independently current quality | updated exact write set and regressions |
| source snapshot | new QA producer | typed roots, real baselines, complete population, modes/hashes/deletions/environment | no QA self-reference; immutable checksum binding |
| V3 assessment and schema3 capture | QA dispatch, inventory, scoped, coordinator, parent gates | explicit supported version, original verdict/identity, proof and approvals | fail-closed old-reader coverage required |
| actual local commit/index/worktree | read-only binding verifier | expected commit chain and all assessed input identities | unrelated history/unknown coverage reject |
| phase output | execution owner / Git boundary | publishable tracked scope, QA, consent, no prohibition | no forced workspace tracking; no empty/artificial commits |
| planning range | future implementation readiness | two CRs, nine-task plan, exact write sets, DoD, artifact QA | planning PASS is not source-write permission |

## Acceptance And Traceability
008 AC1-6 map to its five-row adaptive matrix plus parent/checkpoint collection tests. 009 AC1-7 map to its six-row adaptive matrix plus version/failure/authority tests. Both have three implementation slices, formal Phase5, Phase6 and final required Phase7. Execution is serial because source/evidence consumers overlap. Task009 refreshes Spec QA after008; neither native backend nor client runtime is added.

## History And Residual Risk
Old Phase8 now fails current input fingerprint comparison after the architecture revision. This is expected and is not repaired by rehashing. Earlier implementation evidence is not approval of new work. Original seven phase5 records remained current when individually assessed before new planning QA was rendered; whole-project final readiness is not claimed.
Implementation tests, old-reader interoperability, commit equivalence and full source validation are future work, not results of this planning review. No exact runtime speed or native isolation claim. No broad validators or model evals needed for artifact-only planning.
