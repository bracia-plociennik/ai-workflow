# Specification: PAR-CORE-004

## Scope
One reversible low-risk local change in at most three files; exclusions and growth reclassification; compact DoD/slice/QA still mandatory.

## Definition of Done
- Implement the exact bounded behavior above with read-only safety where applicable.
- Positive, missing-input and adversarial cases tested; failure output cannot imply approval or PASS.
- Current producer/consumer references agree and old consumers retain compatibility.
- Changed files and edge/failure paths reviewed; full integration validation after all tasks.

## Implementation Slice Plan
- Source: accepted plan, architecture and task card.
- DoD source: this specification.

| Slice id | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Contract and schema | Matching core docs | Authority and compatibility review | Producer-consumer map | planned |
| 2 | Reader/validator/template | Matching scripts and templates | Targeted positive/negative fixtures | Test output | planned |
| 3 | Integration and QA | Public runner/docs | Current diff and regression review | Formal quality evidence | planned |

Stop for scope creep, missing approval, unsafe path or dependency conflict. No write permission derives from slicing.

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Owner override: D4, no deadline or timebox.
- Must-have outcome: all seven accepted differences with no quality-floor weakening.
- Quality floor: testable DoD, semantic review, targeted regression and fresh full validation.
- Cutline rule: stop for a new material decision; never remove coverage to finish.
- Overrun checkpoint: not-applicable, owner opted out.

## Plan Quality Contract
- DoD source: accepted D1-D5 and this plan.
- Testable done conditions: seven routes covered by positive and negative fixtures; old smoke coverage unchanged; no foreign writes; phase 8 awaits owner.
- Plan classification: implementation-capable
- Artifact QA route: architecture-qa, plan-qa and spec-qa.
- Implementation QA route: phase-5-quality
- Required verification: current-diff review, producer-consumer audit, negative/failure-path tests, existing smoke suite, explicit full.
- Quality-ready criteria: no unresolved blockers/material findings; current input hashes and complete evidence.
- Opt-out/not-applicable reason: none for quality.
- Blocking decision: none; D1-D5 resolved.
- Next route: implementation slices after Spec QA.

## Owner Decision Checkpoint
- Interaction mode: none
- Decision state: clear
- Material decisions: D1-D5
- Questions asked: none; already answered.
- Auto-resolved reversible decisions: separate branch and task IDs.
- Optional owner refinements: none
- Decision artifacts: decisions/owner-decisions.md
- Next route: approved phases through 8; no final-owner-yes.

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: record integration boundaries and conservative evidence lessons.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Runtime integrity and selective overhead
- Suggested entry summary: Preserve quality while reducing accidental context and script cost.

