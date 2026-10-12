# Execution Modes Project Plan
## Tasks
### EM-COMPAT-002-compatibility
- Goal: source-bound compatibility and bounded recovery.
- Scope: capability, schema 2 inspector/templates, validator/regressions, frozen counterpart integration and current Quality/capture/final check.
- Risk type: high
- Dependencies: accepted compatibility architecture/plan/spec QA.
- DoD: seven conditions in specs/phase-3-em-compat-002-compatibility-specification.md.
- Start condition: current Spec QA and decisions/2026-10-08-compatibility-scope.md.
- End condition: current Quality, Phase 6/7 and renewed technical Phase 8 awaiting owner.
- Readiness status: ready
- Requires user decision before implementation: no, accepted named scope.
### EM-CORE-001-execution-modes
- Goal: integrate two interaction modes with dependency-aware safety.
- Scope: five slices below, formal Quality, distillation/checkpoint and requested technical final check.
- Out of scope: target/AI System writes, dispatch, push and final-owner-yes.
- Definition of Done: all eight accepted decisions represented; producer-consumer fields consistent; synthetic boundary scenarios pass; no unresolved material findings; fresh full source validation.
- Dependencies: accepted architecture and artifact QA.
- Risk type: high
- Main risk: accidental approval expansion or falsely completed partial run.
- Start condition: current Spec QA and owner approval reference.
- End condition: current formal Quality and capture, technical final check awaiting owner.
- Readiness status: ready
- Requires user decision before implementation: no; accepted plan covers named local risk.
## Final Execution Order
EM-CORE-001-execution-modes: contract; dependent readiness; templates/resume; quality/Git; validators/docs/handoff.
EM-COMPAT-002-compatibility follows CORE: capability/recovery contract; inspector/templates; synthetic frozen adapter integration; fresh integrated Quality; Phase 6/7; renewed whole-project technical Phase 8 awaiting owner.
## Dependency Map
All slices integrate into one source change; later slices depend on canonical contract. No separate task QA claims per slice.
The compatibility CR is a separate reviewed source scope after CORE, not a parallel independent workflow. Its final regression QA covers both tasks; no task is omitted from delivery or final check.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: context.md and decisions/2026-10-08-owner-scope.md
- Testable DoD / acceptance conditions: mode/approval/resume/readiness behavior agrees across contract, templates and executable synthetic checks; no incomplete DoD marked completed; current integrated QA and full validation.
- Artifact QA route: phase-2-plan-qa
- Artifact QA trigger: after this artifact, before dependent work
- Implementation Quality Closure route: phase-5-quality
- Required verification: synthetic state tests, adversarial policies, producer-consumer audit, current-diff review, explicit full validator
- Quality-ready criteria: no unresolved P0/P1/material P2; source and owner scope current
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: phase-3-specification

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Quality floor: full DoD and findings-first review
