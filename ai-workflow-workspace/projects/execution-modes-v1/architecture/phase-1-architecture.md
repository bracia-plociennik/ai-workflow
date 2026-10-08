# Execution Modes Architecture
## Goals
Minimize owner interruptions while preserving approved scope, honest results and current evidence.
## Components And Responsibilities
| Component | Responsibility |
| --- | --- |
| execution-modes.md | canonical mode, scope, decision eligibility and authority |
| existing decisions/autopilot | independent-unit blocking, readiness, resume and queue |
| lib/execution-modes.py | pure JSON inspection of a run's readiness projection; no dispatch or approvals |
| templates | matching persisted execution block without replacing autopilot.mode |
| check-execution-modes | policy/consumer integrity and optional runtime projection validation |
## Main Data / Integration Flows
Owner request -> resolved mode -> scope/approval/DoD -> ready units -> execution and QA -> captured result and pending queue.
## Architectural Decisions
Use existing project/run namespace; one task with five serial slices; optional JSON readiness projection permits stdlib-only deterministic tests. It never attests filesystem isolation or grants execution.
## Failure Scenarios
Unknown dependency/resource proof blocks affected work; cycle/malformed state rejected; fundamental intent uncertainty stops dependent writes; stale baseline requires refreshed readiness. Commit source changes require fresh applicable QA.
## Boundaries And Out Of Scope
No scheduler, native worker calls, paid eval, target edits or external effects.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: context.md and decisions/2026-10-08-owner-scope.md
- Testable DoD / acceptance conditions: mode/approval/resume/readiness behavior agrees across contract, templates and executable synthetic checks; no incomplete DoD marked completed; current integrated QA and full validation.
- Artifact QA route: phase-1-architecture-qa
- Artifact QA trigger: after this artifact, before dependent work
- Implementation Quality Closure route: phase-5-quality
- Required verification: synthetic state tests, adversarial policies, producer-consumer audit, current-diff review, explicit full validator
- Quality-ready criteria: no unresolved P0/P1/material P2; source and owner scope current
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: phase-2-project-plan

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Quality floor: full DoD and findings-first review

