# Decision: PE-003 Skill Work Sequencing

## Date

`2026-09-25`

## Status

`approved`

## Classification

`high-impact`

## Context

- CORE-001 specification passed its artifact QA after the owner approved `AGENTS.md` as the only first-candidate tracked file. No implementation or paired candidate result exists.
- SKILL-002 specification proposes `.systems/ai/skills/skill-creator/SKILL.md` as a separate second-candidate file. This file is not approved.
- Two controlled baseline runs missed active `skill-creator` during skill review despite the current description naming review. The cause may lie in root routing, skill discovery, or both.
- LOOP-003 is also evidence-gated; the baseline completed a safe local test loop but did not exercise a post-edit failure/repair branch.

## Options

| Option | Pros | Cons | Impact |
| --- | --- | --- | --- |
| Defer SKILL-002 and LOOP-003 until CORE-001 paired evidence | Avoids speculative source edits and tests causal effect of the approved first candidate | Requires an owner-approved plan/task-set change before a CORE-only implementation-range | Current planning-range stops; after plan amendment and fresh readiness, CORE-001 may run alone |
| Approve `.systems/ai/skills/skill-creator/SKILL.md` as a separate second-candidate scope | Allows SKILL-002 specification and its first Spec QA to continue | May be redundant if CORE-001 resolves the miss; LOOP-003 still needs separate evidence/routing | Extends planning-range, not the current `AGENTS.md` first-candidate write set |

## Recommendation

- Defer SKILL-002 and LOOP-003 until after a controlled CORE-001 candidate result. This is a plan sequencing decision, not silent cancellation of either task.

## Decision Timing

- Why needed now: SKILL-002 cannot complete its working specification phase or chain to Spec QA with an unapproved high-risk tracked file; autopilot cannot continue with a pending material decision.
- Blocking point: SKILL-002 specification and the current planning-range stop condition of all planned specs passing.
- Can owner override later: yes.
- Override impact: update plan/task index, run-scoped readiness and affected specs/QA before broadening tracked writes.

## Owner Decision

- Chosen option: defer SKILL-002 and LOOP-003 until CORE-001 paired evidence.
- Decided by: owner, explicit chat instruction.
- Decision date: 2026-09-25.

## Consequences

- SKILL-002 and LOOP-003 remain planned but deferred, with no specification or implementation progression in this tranche. Reopening either requires review of CORE-001 paired evidence, an explicit plan/task-set amendment, and renewed applicable QA/readiness and high-risk write approval.
- CORE-001 `AGENTS.md` approval does not extend to SKILL-002, LOOP-003, or any other tracked file.
- Neither option authorizes commit, push, phase-8 or a quality verdict on unimplemented work.

## Follow-Up

- Amend the accepted project plan and task set, perform fresh Plan QA, and prepare separate CORE-only implementation-range readiness without starting implementation.
- If the skill file is approved, complete SKILL-002 specification and run its first Spec QA; retain evidence-gated deferral for LOOP-003 unless separately justified.
