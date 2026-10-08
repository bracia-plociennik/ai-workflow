# EM-CORE-001 Specification
## Task Contract
- Goal: default Auto and explicit Human Coop with minimal interactions.
- Scope: accepted five slices.
- Definition of Done: see the concrete acceptance checks in Implementation Slice Plan.
- Risk type: high
- Approval: decisions/2026-10-08-owner-scope.md
## Implementation Slice Plan
- Source: accepted owner plan, architecture and project plan
- DoD source: this task contract and owner's D1-D8
| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| EM-S1 | mode/decisions/approvals | core routing/risk/delivery and AGENTS | Auto safe choices; no permission creation | contract consistency review | planned |
| EM-S2 | dependency-aware readiness | autopilot and pure evaluator | transitive blocking, safe independent continuation | synthetic tests | planned |
| EM-S3 | producers/resume | project/run/decision templates | mode precedence, resume, legacy conservatism | field audit and tests | planned |
| EM-S4 | closure/Git | quality/phase/response consumers | no completed partial DoD; Phase 8 only requested | adversarial review | planned |
| EM-S5 | validators/docs/handoff | scripts, smoke registry, docs, ignored handoff | targeted/full checks and source review | logs, QA, capture | planned |
- Stop rule: stop affected writes on unsafe action, unknown dependency, scope creep or missing approval; continue only proven independent work.
## Interface
Pure inspection accepts JSON schema 1 with execution mode/context, scoped unit gate/decision/dependency/resource records and optional asserted run state; returns ready/blocked/completed sets and decision queue. Source evidence fields are declarations, not authenticated authority.
## Tests And Pass Conditions
Auto/human preference; unknown facts; unapproved high/critical effects; dependencies, shared resources and cycles; approval scope; legacy/resume; no deadline; no premature completed; final check authorization; no push.
## Plan Quality Contract
- Plan classification: implementation-capable
- DoD source: accepted owner plan and this specification
- Testable DoD / acceptance conditions: synthetic state and policy scenarios enforce declared boundaries; integrated current-diff review; full validation
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: before implementation
- Implementation Quality Closure route: phase-5-quality
- Required verification: behavioral tests, adversarial policies, producer-consumer audit, full validation
- Quality-ready criteria: all scenarios reviewed, no material unresolved findings
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: phase-4-implementation
## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none

