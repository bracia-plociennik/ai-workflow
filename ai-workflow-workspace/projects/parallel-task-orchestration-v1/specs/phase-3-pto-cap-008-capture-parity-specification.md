# Specification: PTO-CAP-008-capture-parity
## Metadata
- Task/package ID: PTO-CAP-008-capture-parity
- Project: parallel-task-orchestration-v1
- Date: 2026-10-04
- Risk: high
- Readiness: conditional, planning only
- Source CR: PTO-CR-001-capture-parity

## Goal And Scope
Use one semantic validator for existing capture populations; correct both historical false rejection and scoped false acceptance. No freshness-policy change in this task.
Sources: canonical architecture/plan, architecture/pre-final-capture-and-commit-delta.md, PTO-D07, actual capture-state.py and validation-scope.py.
Out of scope: target installation/data/product, history mutation, schema2 downgrade, broad scanning and commit/push.

## Definition Of Done
- PTO-008-AC1: Identical selected records have identical structural/quality classifications through no-arg, --project and --runtime-only; differences due to intentionally different populations are reported, not widened.
- PTO-008-AC2: Valid schema1 historical/advisory records including legacy ID/gate and absent derived output remain unchanged; historical integrity never supplies current QA PASS.
- PTO-008-AC3: Schema2 ready/completed requires current owning-project implementation-quality PASS, matching source HEAD/hash/identity and explicit derived state; completed additionally requires one unique accepted owned distillation. Ready may have no distillation yet.
- PTO-008-AC4: Reject missing references required by the state, foreign evidence paths, unsafe paths/symlinks, unknown schema, duplicate fields/work IDs/distillation reuse, inconsistent derived output and unaccepted completed distillation. Wrong QA kind/identity/freshness rejects schema2 ready/completed; schema1 remains historical/advisory rather than being promoted to current QA.
- PTO-008-AC5: Historical scoped manifest populations and foreign/nested repository exclusions are unchanged; all selected records, not just successful rows, participate in duplicate detection.
- PTO-008-AC6: Consumer conformance tests exercise positive and negative completed/ready records, not only pending-quality; full supporting validation and current-diff review preserve PTO.

## Planned Write Set
- .systems/ai/capabilities/parallel-task-orchestration-v1.json
- .systems/scripts/lib/capture-record.py
- .systems/scripts/lib/capture-state.py
- .systems/scripts/lib/validation-scope.py
- .systems/scripts/lib/parallel-orchestration.py
- .systems/scripts/lib/parallel-orchestration-tests.py
- .systems/scripts/check-distillation-state
- .systems/scripts/tests/runtime-integrity.py
- .systems/scripts/smoke/core.sh
- .systems/scripts/smoke/manifest.json
- .systems/ai/core/distillation-state.md
- .systems/ai/core/runtime-integrity.md
- .systems/ai/core/changelog.md
New helper accepts bounded path/QA/Git adapters from trusted callers, never executable callbacks from runtime input. No import cycle. Population selectors retain existing scope rules. Schema1's documented legacy source-reference exception remains narrowly bounded; never generalize it to arbitrary foreign project paths.
PTO-D09 explicitly approves maintenance of the existing capability source pin. Refresh only installed source hashes after final source changes; retain schema/protocol and native-unverified/serial/authority boundaries. This is compatibility maintenance, not native capability verification.
Preserve diagnostic exit codes and avoid exposing raw contents. Omitted derived output allowed only by the legacy contract; wrong supplied output always rejects.
State-specific requirements are explicit: pending-quality may have Quality artifact: none; ready may have Distillation artifact: none; completed requires the owned accepted distillation. Existing referenced paths still must be safe and resolvable.
The public single-record API is structural only. Any consumer using a record for current parent/task/checkpoint eligibility must validate the entire owning capture-state collection first. Change parallel-orchestration.check_parent_gate to use the bounded collection result, then select the requested record. Invalid sibling records, duplicate Work IDs or reused distillations block that gate; no scans outside the owning project. Test parent completion and checkpoint consumers, not only inventory CLI.

## Adaptive Data / Integration Verification Matrix
| Source shape | Expected canonical state | Expected derived output | Forbidden state | Failure behavior | Automated check | Manual trace |
| --- | --- | --- | --- | --- | --- | --- |
| schema1 accepted historical completed, legacy Work ID/gate, derived absent | structurally valid, historical/advisory | true for display, not QA eligibility | current PASS from history | missing referenced evidence still rejects | same fixture via three public paths | history -> collection -> consumer |
| schema2 ready/completed, actual current QA | verified-current | false/true by state | conflicting identity or boolean | reject mismatch | real V2 positive plus one mutation per invariant | QA -> record -> gate |
| stale HEAD/hash, FAIL, wrong kind/owner | invalid schema2 | no promotion | accepted current | nonzero diagnostic | consumer parity negative table | rejection preserves source bytes |
| links, traversal, reused distillation, duplicate Work ID/field | invalid selected collection | no accepted duplicate | scan escape or hidden duplicate | reject before promotion | cross-record/path tests | bounded selector -> validator |
| repo/core legacy manifest and unrelated invalid project | original narrow population only | unchanged count and no foreign data | broadened inventory | retain exclusion | mixed-population fixture | selection separate from semantics |

## Verification
Test assertions compare structured classification and exit behavior for the same selected population, not total no-arg/project counts. Use synthetic temporary repositories only, no TechGrow writes or provider calls. Include root/missing namespace, foreign repository and no-project formal schema2 cases.
Targeted: runtime-integrity and parallel-orchestration test suites and check-distillation-state paths with explicit fixture workspace. Include parent completion/checkpoint negatives for duplicate sibling Work ID, reused distillation and invalid sibling, plus legitimate ready without distillation and pending-quality without Quality. Preserve all existing smoke IDs; new supplemental cases and manifest hashes only. Manual trace one historical success and one schema2 stale failure.
Full source gate after semantic QA: validate-workflow --profile full --project parallel-task-orchestration-v1 --progress summary --explain. Historical project assessments must be explicitly accounted for; fixture-only success is not full-project PASS.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: accepted owner request, PTO-D07, architecture delta and PTO-008 AC
- Testable DoD / acceptance conditions: every numbered AC maps to a regression and semantic review below
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: after full specification and prerequisite Plan QA
- Implementation Quality Closure route: phase-5-quality
- Required verification: adversarial and producer-consumer matrix, unit/integration tests, targeted scripts, smoke suite, fresh full source gate after semantic review
- Quality-ready criteria: all AC evidenced with no unresolved P0/P1/material P2; no borrowed historical/current verdict
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: separate high-risk implementation/Phase5 approval before relevant gate
- Next route: stop before implementation-range readiness

## Implementation Slice Plan
- Source: this spec, canonical plan and PTO-D07
- DoD source: numbered AC in this specification
- Scope: exact paths above; extra path or behavior requires Spec Fix Loop before writes
| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-008-S1 | Introduce bounded shared contract/helper | listed helper and contract files | design invariants and negative cases | tests and source diff | planned |
| PTO-008-S2 | Integrate actual producers and consumers | listed consumers/templates | same inputs give agreed outcome | conformance matrix and failure traces | planned |
| PTO-008-S3 | Regress policy/runtime and document | listed tests/smoke/docs | all AC and preserved coverage | current-diff review and full source result | planned |
- Stop rule: scope growth, missing facts/approval, unprovable equivalence or unsafe effects stop dependent writes.
- Compact mode: not-applicable for high-risk work.

## Gates, Rollback And Delivery
Dependency: none from009; existing approved PTO source is the preserved baseline, not permission for new edits. Each task has separate Spec QA, formal Phase5 and Phase6. Final Phase7 after009; existing checkpoint cadence is not counted per slice.
No deadline/timebox, inherited owner opt-out. No cut of the quality floor to save time.
Rollback: stop using newly advertised capability; preserve evidence; reviewed source rollback only after explicit approval. Never rewrite history or downgrade schema to pass.
Implementation unstarted. Existing PTO001..007 approvals do not authorize these writes. Commit/push/final-owner-yes remain outside current planning.
Before final closure, rereview affected prior PTO evidence and original native-unverified limitation; do not rebind old hashes without a real assessment.

## Owner Decision Checkpoint
- Interaction mode: queued
- Decision state: clear
- Material decisions: PTO-D07 planning scope
- Questions asked: none
- Auto-resolved reversible decisions: serial execution design and exact names
- Optional owner refinements: added-scope cross-system impact remains pending; resolve before local commit or handoff, not optional and not push-only
- Decision artifacts: decisions/pto-pre-final-planning-authorization.md
- Next route: Spec QA then stop

## Optional Knowledge Capture
- Capture recommended: yes
- Target: decision-artifact
- Reason: retain design and safety boundaries
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: PTO-008 design boundaries
- Suggested entry summary: Scope, proof obligations and skipped implementation are explicit.
