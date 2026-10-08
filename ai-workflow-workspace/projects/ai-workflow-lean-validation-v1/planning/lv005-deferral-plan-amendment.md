# Active Plan Amendment: LV005 Deferral

## Authority And Versioning

Owner decision LV-DEC-010 updates the effective project plan. Read planning/phase-2-project-plan.md together with this amendment; this amendment controls the current execution disposition where the preserved base says all six tasks must execute. The base plan remains byte-identical because accepted earlier assessments bind it. This is versioned scope change, not a historical rewrite or automatic acceptance.

Source baseline: a7d66c7; branch codex/ai-workflow-lean-validation-v1; tracked tree clean. No deadline/timebox remains LV-DEC-001. Shared impact remains yes under LV-DEC-004.

## Task Dispositions And Dependency Map

| Task | Current disposition | Included result | Next dependency |
| --- | --- | --- | --- |
| LV001 | done | verdict integrity, accepted quality/capture | preserve source-specific evidence |
| LV002 | done | immutable timing baselines, accepted quality/capture | comparisons must reject unequal coverage |
| LV003 | done | explicit scope and dependency selection, accepted quality/capture | no subset reported as full |
| LV004 | done | independent assertion-preserving groups, accepted quality/capture | all retains 694 current IDs |
| LV005 | deferred | no implementation, no promotion, no behavioral benefit | future controlled runtime and paired eval remain required |
| LV006 | conditional until current Spec QA/readiness | integrate only LV001-LV004 and visible LV005 disposition | current dependency evidence and composite specification |

Execution graph: accepted LV001 -> LV002 -> LV003 -> LV004 -> LV006. LV005 is excluded from implementation scope under LV-DEC-010, not replaced by a fake PASS. LV006 consumes the approved disposition in place of a LV005 implementation outcome. Original LV005 DoD and future gates are unchanged.

## Revised LV006 Contract

- Goal: coherent integration and honest measured conclusions for LV001-LV004, with deferred LV005 visible.
- Scope: original five-path documentation/consolidation ceiling; semantic cross-contract review, complete CI/updater coverage, comparison eligibility, final full supporting validation and single handoff.
- Out of scope: LV005 source promotion, instruction/response/template compaction, model evals, scope inference/cache, lost smoke assertions, hidden deferral, unrelated source changes or counterpart edits.
- Definition of Done: each included implemented task has supported quality/capture; original baseline identities preserved; all current assertions retained; no material unresolved finding in included scope; partial or incomparable performance is disclosed; full verification after semantic QA; later Phase 6/7 and final-check boundaries explicit.
- Risk: high.
- Main risk: scope deferral mistaken for implementation completion or incompatible timing populations compared.
- Start: Plan QA of this composite plan, refreshed composite LV006 Spec QA, fresh pre-write baseline and slice/state records.
- End: supported high-risk Phase 5 after actual integration evidence; later Phase 6 and required final checkpoint.
- Readiness: conditional until current Spec QA and task-scoped readiness.
- Decisions: LV-DEC-002/004/008/010 resolved; none newly pending.
- Spec: preserved specs/phase-3-lv-qa-006-integration-specification.md plus specs/lv006-current-scope-amendment.md.
- Quality route: quality/recovery-phase-3-lv-qa-006-integration-spec-qa.md, then formal phase-5-quality.
- Task card: none; complete composite task contract is canonical.

## Acceptance And Failure Cases

- Deferral cannot set task status done, produce Phase 5 PASS for LV005 or set is_distilled true.
- Original LV005 infrastructure FAIL stays evidence of unmet future requirements.
- Baseline 660 IDs and current 694 IDs are different full populations; lower duration alone cannot establish a full speed gain.
- Integration may report correctly measured scoped execution separately, not as equivalent full coverage.
- Prior source hashes remain valid only for their exact input set; a later source/document change requires fresh affected regression assessments.
- No source correction outside LV006's ceiling is allowed through integration; route to owning fix loop and Spec QA.
- Source edits, a final checkpoint and Phase 8 are not performed by this planning/readiness request.
- Phase 8, if later run under LV-DEC-008, reports excluded LV005 and still awaits final-owner-yes.

## Plan Quality Contract

- Plan classification: implementation-capable
- DoD source: accepted base context/architecture, LV-DEC-010 and revised LV006 contract
- Testable DoD / acceptance conditions: five included delivery tasks (LV001-LV004 and LV006), one explicit unchanged deferred task; acyclic graph, complete current artifacts and no false benefit/completion
- Artifact QA route: phase-2-plan-qa
- Artifact QA trigger: after amendment/router/task-index synchronization
- Implementation Quality Closure route: phase-5-quality
- Required verification: full plan/index diff review, adversarial scope/comparison/failure cases, producer-consumer audit; LV006 later semantic QA and explicit full
- Quality-ready criteria: no unresolved planning blocker; conditional future execution evidence is not a current implementation result
- Owner opt-out: none for QA
- Not-applicable reason: none
- Blocking decision: none for this disposition; future LV005 restart needs a safe runtime
- Next route: current Plan QA, LV006 specification refresh/Spec QA and readiness only

## Delivery Constraints And Capture

Owner-opt-out, no deadline/timebox; no safety or quality reduction. Must-have: verified integration of included work. Deferred: LV005 instruction-efficiency and its runtime setup/eval. Stop on missing required evidence, unsafe action, stale inputs or outside-ceiling correction. Optional knowledge capture: capture-now to decision-artifact/status evidence under this owner-approved scope. No Phase 6 completion is implied by storing a planning decision.

