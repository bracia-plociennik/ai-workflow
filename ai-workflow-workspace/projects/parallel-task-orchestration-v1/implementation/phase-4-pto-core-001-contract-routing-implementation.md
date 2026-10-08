# Phase 4 Implementation: PTO-CORE-001-contract-routing

## Metadata

- Project: parallel-task-orchestration-v1
- Task/package ID: PTO-CORE-001-contract-routing
- Source HEAD: 8a0eeef5dcee4a4c9852cb495bdae6e92115a0e1
- Branch: codex/parallel-task-orchestration-v1
- Risk: high
- Owner approval: decisions/implementation-approval.md
- Delivery constraints: owner-opt-out; no deadline or timebox
- Implementation result: source completed; fresh advisory review and full validation complete; formal high-risk gate awaiting owner

## Implementation Slice Plan

- Source: accepted specification, project plan and owner implementation command.
- DoD source: PTO-001-AC1 through PTO-001-AC4 in accepted specification.
- Implementation scope: exactly the eighteen authorized source paths.
- Artifact QA route: phase-3-spec-qa, current input-bound prerequisite refresh.
- Implementation quality route: phase-5-quality with required human gate.

| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| PTO-001-S1 | Define authority and dispatch contract | core contract and nine policy/template consumers | one execution owner and unchanged formal gates | full source and prerequisite review | completed |
| PTO-001-S2 | Add validator and adversarial regressions | validator, registries, core smoke and manifest | direct/compound unsafe claims fail, safe prohibition passes | core smoke logs and manifest audit | completed |
| PTO-001-S3 | Complete current-diff quality review | entire approved task write set and its consumers | DoD/intent/edges/failure/coverage review | review evidence plus fresh full supporting validation; formal human acceptance pending | awaiting-owner |

Stop rule: scope creep, unknown ownership, dependency conflict, missing decision,
unsafe effect or write outside the accepted spec stops dependent work.

## Slice Execution Evidence

S1: Added parallel-task-orchestration.md; updated parallel-work-policy, autopilot,
implementation-slicing, command-routing, operating-model, workflow, project-plan
phase, readiness and state templates. No capabilities/backend/helper announced.

S2: Added check-parallel-task-orchestration with shared policy-boundaries.sh and
registered it in required artifacts, validation-checks, standard/full runner,
Review Completeness Gate policy audit and smoke coverage index.
Supplemental core tests preserve the 674 frozen reference IDs and all old
supplemental tests. No sixth public group or frozen-region rewrite.

The first independent review found four issues: consumer-scan omission,
independent-task predecessor contradiction, equivalent unsafe wording and
may-not false positive. All corrected within authorized paths before closure.
Additional negative-space cases cover recursive delegation, scope expansion
and unauthorized Phase 8.

Initial standard validation correctly rejected source-stale prerequisite QA
and task-index paths not resolvable in the non-runtime-only consumer.
Re-reviewed architecture/plan/spec prerequisites, retained superseded runs and
used canonical workspace references in the local task index.

Initial core run could not inspect ps inside sandbox. An authorized outside
sandbox run then identified omitted untracked product inputs. Existing explicit
AI_WORKFLOW_SMOKE_EXTRA_FILES includes only the two new authorized product files.
No fixture helper or frozen test was weakened to obtain a passing result.

## Definition Of Done Validation

| DoD | Evidence | State |
| --- | --- | --- |
| PTO-001-AC1 | one-owner contract and autopilot delegated-unit exception; competing independent runs still prohibited | implemented, pending formal acceptance |
| PTO-001-AC2 | observed-capacity/resource/input/checkpoint limits and serial fallback | policy implemented; runtime behavior belongs to PTO-002+ |
| PTO-001-AC3 | optional packaging, unit-not-task, common QA and per-parent capture | implemented, pending formal acceptance |
| PTO-001-AC4 | all-consumer adversarial checker and 37 supplemental smoke regressions | fresh full validation passed; formal acceptance pending |

## Adaptive Data / Integration Verification Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| installed contract and all consumers | one owner, real prerequisite gates | valid serial/default route | two independent autopilots | reject unsafe permission statement | valid/dual-owner smoke cases | router to autopilot to unit acceptance boundary |
| safe prohibition then unsafe clause | unsafe enabling clause remains visible | validator rejects | green result due to preceding negation | nonzero diagnostic | six separators and but tests | policy helper matches enabling clause after separator |
| unsafe wording in any consumer | source-wide rejection | nonzero diagnostic | unchecked routing/template exception | reject before gate | nine consumer mutations | consumer list includes every changed policy/template |
| explicit independent tasks | current Spec QA and real dependencies | scoped concurrent eligibility after future backend preflight | fictitious prior-task completion | actual dependency blocks | contract checks and semantic trace | sequential route remains default, independent exception retains quality/capture |

## Known Limits

No allocator, lifecycle CLI, write-isolation backend or native benchmark exists
yet. This task establishes policy, not full feature availability. Lexical
validators supplement semantic review and do not prove every natural-language
policy paraphrase safe. No AI System file, model config or nested clone changed.

## Quality Closure

- Formal verdict: not issued; high-risk gate remains required.
- Current-diff review: completed; no unresolved material technical findings found.
- Findings-first review and post-fix freshness: complete for the eighteen-file source snapshot.
- Supporting full validation: result=pass, exit 0, duration 666 seconds; all five groups passed, 740 unique smoke IDs retained.
- Formal acceptance blocker: high-risk Phase 5 requires human approval; no gate verdict inferred from green scripts.
- Knowledge capture: defer to Phase 6 after accepted formal Quality.
- Commit/push/Phase 8: not performed or authorized.
