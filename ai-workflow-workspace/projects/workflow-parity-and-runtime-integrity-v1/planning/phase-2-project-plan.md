# Project Plan

## Task Order
001 -> 002 -> 003 -> 004 -> 005 -> 006 -> 007. Each task: contract/readiness, implementation, regressions, semantic review, formal Phase 5. Integration review follows final source edits; phases 6/7 then owner-triggered phase 8.

## Definition of Done
- Canonical repo and project records included without foreign namespaces.
- Historic records immutable and distinct from verified current evidence.
- Five smoke groups use selected worktree fixtures, preserving old coverage.
- False short-circuit reads not counted; confirmed earlier reads survive later failure.
- Micro-exempt narrow, testable and reclassified on growth.
- Model names not frozen; named choices are source-backed.
- Compact output cannot hide blockers, skips or formal obligations.
- Read-only CLI provides schema-version, identity, baseline, evidence, freshness and verified/declaration distinction.
- Full validation and fresh findings-first review complete before phase 6/7/8.

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

