# Architecture

## Accepted Design
One owner-root inventory separates capture namespace from referenced evidence. Existing schema-v1 scoped manifests retain their exact repo/core and project population; a new standalone capture inventory covers canonical repo records without broadening old manifests. Historical/advisory evidence is labelled unknown/legacy, never promoted to formal PASS.

A standalone safe fixture builder selects tracked product files from the current worktree, with explicit new-file opt-in for this implementation. Each smoke group invokes it; existing test bodies and assertions stay unchanged. No git blob substitution or ignored runtime copy.

A conservative scorer reads completed command events and classifies uncertain shell control flow as unknown; it does not execute commands. Coordinator output reuses the authoritative QA reader and catches baseline drift; output is evidence, never permission.

Micro-exempt, response mode and model guidance are policy changes with producer/template/validator alignment. None modifies formal QA gates.

## Rejected Alternatives
- Copying the whole directory: exposes ignored/private context.
- Converting historical completed records into current PASS: falsifies freshness.
- Parsing all shell syntax as proof: impossible from aggregate logs.
- Inferring approvals from CLI fields: violates authority boundary.

## Failure And Rework
Missing evidence, symlink or foreign root yields invalid/unknown; unsafe copy fails before completion. Trace uncertainty yields unknown, not false confirmation. Scope growth revokes micro-exempt. All runtime consumers stay read-only.

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

