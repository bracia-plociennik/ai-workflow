# Micro-Project: `deadline-aware-delivery-v1`

## Status

- Status: implemented-awaiting-owner-commit
- Date: 2026-07-17
- Work mode for future implementation: `workflow-maintenance`
- Risk: `medium`
- Artifact scope: workspace-only planning evidence
- Tracked source changes: none
- Implementation performed: yes; quality closure complete

## Summary

Add a default delivery-constraint checkpoint before new implementation work. The workflow should ask for the relevant deadline, time budget, and must-have outcome, then adapt scope to deliver the highest-value result within the agreed constraint. The constraint is a planning and prioritization input, not permission to weaken safety, Definition of Done, QA, approvals, or required evidence.

The workflow should avoid asking redundant versions of the same question. It should ask only for missing material delivery decisions and group them into the existing owner-decision checkpoint of at most 1-3 questions.

## Problem And Validation

### What stays

- Delivery needs a visible time boundary because open-ended improvement can otherwise continue indefinitely.
- The owner should control the deadline, time budget, must-have result, and acceptable scope reduction.
- The workflow may reduce optional scope to meet a constraint, while protecting the quality floor.

### What should improve

- Ask one grouped checkpoint instead of separately asking "when", "how long", and "what is the deadline".
- Distinguish hard deadline, timebox, and both.
- Treat estimates as planning estimates, not guarantees.
- Report an overrun or missing-facts checkpoint instead of silently extending scope or time.
- Never use a deadline to justify skipping QA, security review, permissions, evidence, acceptance criteria, or owner approval.

### What is missing

- A canonical delivery-constraints contract and field taxonomy.
- Explicit `must-have`, `should-have`, `stretch`, and deferred scope handling.
- A cutline and overrun route.
- Deadline/timezone normalization and an owner opt-out boundary.
- Fields in task, plan, micro-task, micro-project, and autopilot readiness artifacts.
- Validator and adversarial smoke tests for unsafe scope compression.

### Blockers and decisions

- No implementation blocker for the plan artifact.
- Future implementation must preserve the following owner-approved default: ask for deadline/timebox by default; allow explicit owner opt-out; do not infer a material deadline from chat history when it is absent.

## Proposed Contract

Every implementation-capable new work item should expose:

```text
Delivery Constraints
- Mode: <deadline-and-timebox|deadline-only|timebox-only|owner-opt-out|not-set>
- Deadline: <timestamp|none>
- Timezone: <IANA timezone|none>
- Time budget: <duration|none>
- Must-have outcome: <testable result>
- Should-have scope: <list|none>
- Stretch scope: <list|none>
- Explicitly deferred scope: <list|none>
- Quality floor: <DoD/QA/acceptance boundary>
- Cutline rule: <what is reduced first>
- Overrun checkpoint: <route and owner decision>
- Owner override: <decision or none>
```

Rules:

- `must-have` and the quality floor cannot be reduced automatically.
- AI may defer `stretch` and, where safe, `should-have` scope, but must report the change.
- Changes to scope, DoD, acceptance criteria, architecture, risk, permissions, security, billing, migration, production, or external effects require an owner decision.
- A missing deadline is a decision to ask about, not permission to invent one.
- `owner-opt-out` means no deadline planning for the current scope only, unless the owner explicitly extends the opt-out.
- Autopilot must have a resolved delivery constraint or an explicit owner opt-out before readiness.

## Proposed Routing

1. New implementation request enters task intake and default idea validation.
2. Repository facts and existing artifacts are read first.
3. Owner Decision Discovery asks at most 1-3 grouped delivery questions if a material constraint is missing.
4. The plan records the delivery constraint and maps scope to must-have, should-have, stretch, and deferred work.
5. Implementation slicing uses the cutline without changing permissions or quality gates.
6. Quality closure verifies the delivered result against the agreed must-have outcome, DoD, acceptance criteria, and disclosed scope reductions.
7. If the deadline is at risk, stop at the overrun checkpoint and request a decision; do not silently continue.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| DAD-1 | Add the delivery constraints contract and source-of-truth rules | `.systems/ai/core/`, command routing, task intake, owner decisions | Contract defines modes, fields, cutline, overrun, opt-out, and safety floor | Contract review and policy-boundary matrix | completed |
| DAD-2 | Route deadline questions and scope decisions | `task-intake`, `owner-decision-checkpoints`, `command-routing`, workflow/autopilot docs | Missing material delivery decisions produce grouped questions; discoverable facts do not | Routing smoke tests and producer-consumer field audit | completed |
| DAD-3 | Add delivery fields to plans and work artifacts | plan/spec/task/micro-task/micro-project/autopilot templates | Every implementation-capable plan records a testable delivery constraint or explicit owner opt-out | Template fixtures and required-field validation | completed |
| DAD-4 | Add deadline validator and adversarial tests | `.systems/scripts/check-delivery-constraints`, smoke suite, validation integration | Unsafe deadline wording cannot bypass DoD, QA, risk, permissions, or approvals | Positive/negative validator tests | completed |
| DAD-5 | Run quality closure and document operating guidance | `AGENTS.md`, `HUMANS.md`, `README.md`, commands, changelog | Full review confirms intent, plan, DoD, scope, producer-consumer, and PASS integrity | Targeted and full validation evidence; advisory review | completed |

## Definition Of Done

- The accepted contract defines deadline, timebox, timezone, must-have outcome, cutline, deferred scope, quality floor, overrun, and owner opt-out semantics.
- New implementation-capable work routes through a grouped owner-decision checkpoint when a material delivery decision is missing.
- Future plans and task artifacts contain testable delivery constraints or an explicit, bounded owner opt-out.
- Scope reduction cannot silently alter DoD, acceptance criteria, risk, permissions, security, approvals, or required QA.
- Autopilot and implementation slicing use the same delivery constraint fields.
- Validator and smoke tests catch contradictory or unsafe scope-compression wording.
- Quality closure reports delivered scope, deferred scope, deadline status, DoD fit, findings/blockers, skipped checks, and residual risk.
- Workspace remains ignored and no Codex, scheduler, runtime, or product setting is changed by this plan.

## Plan Quality Contract

- DoD source: owner-approved request in this artifact plus existing `definition-of-done.md`, `plan-quality-contract.md`, `owner-decision-checkpoints.md`, and `implementation-slicing.md`.
- Plan classification: `implementation-capable`.
- Artifact QA route: `global-quality-review-stance` for the workflow-maintenance plan and future contract artifacts.
- Implementation quality route: `global-quality-review-stance` for workflow-maintenance changes; formal `phase-5-quality` remains required if routed into a formal project phase.
- Required verification: targeted validator tests, adversarial policy-boundary cases, producer-consumer field audit, template checks, and explicit `validate-workflow --profile full` before future commit/handoff.
- Quality-ready criteria: no unresolved P0/P1/material P2, aligned intent/plan/spec, complete DoD and delivery fields, fresh review evidence, and no hidden weakening of safety or quality gates.
- Current implementation writes are tracked workflow-maintenance changes; final commit and push remain owner-controlled.
- Blocking decision and next route: no current planning blocker; future implementation must stop for missing deadline, timezone, must-have outcome, or cutline decisions when material.

## Owner Decision Checkpoint

- Interaction mode: `interactive` for future implementation; `none` for this artifact write
- Decision state: `clear`
- Material decisions: `DAD-DELIVERY-DEFAULT`, `DAD-CUTLINE`, `DAD-OVERRUN`
- Questions asked: `none` because the owner accepted separate scopes and the recommended default
- Auto-resolved reversible decisions: `none`
- Optional owner refinements: deadline-only and timebox-only modes may be used when the other constraint is genuinely unavailable
- Decision artifacts: `none`
- Next route: implementation planning after a new owner command

## Evidence

- Read-only baseline reviewed: `HEAD 203a278`, clean `main`, `origin/main` aligned.
- Source scan confirmed no canonical deadline/timebox contract in current core policy, task card, micro-task, or micro-project templates.
- Existing `owner-decision-checkpoints.md` supports grouped 1-3 questions and material-decision classification.
- Existing `plan-quality-contract.md` and `implementation-slicing.md` provide the pre-write DoD and slice-plan boundary.
- Existing quality, validation-profile, autopilot, and response contracts were reviewed as integration points.
- Workspace tracking check before this write: `git ls-files ai-workflow-workspace` was empty.

## Quality Closure

- Closure type: `advisory implementation review`
- Findings/blockers: none known in the plan artifact; future implementation is blocked until its own implementation plan and current refresh are established.
- Intent / Plan / Spec Compliance: `aligned`
- DoD fit: `aligned`
- Risk/work mode compatibility: `aligned` (`medium` / `workflow-maintenance`)
- Cross-contract consistency: `aligned`
- Negative-space/adversarial review: completed at plan level for deadline invention, unsafe scope compression, silent overrun, and opt-out misuse
- Producer-consumer field audit: completed
- Policy-boundary matrix: completed
- Automated evidence role: supporting-only
- Post-fix full re-review: `completed`
- Reviewed baseline: `HEAD 203a278; clean worktree before workspace artifact write`
- Instruction refresh: `performed-full`; current source-of-truth chain reviewed
- Closure freshness: current; fresh full-current-diff QA completed after the fix loop
- Result wording: `Ready for owner review`
- Residual risk: formal phase-6 distillation and commit review remain separate owner-controlled follow-up steps; time estimates remain planning estimates, not guarantees

## Contract Compliance And Knowledge Capture

- Contract compliance: `advisory-compliant`; workflow-maintenance tracked source changes stayed within the accepted write set, with no product-code, permission, or gate changes.
- Knowledge capture: `required`; target `micro-project-artifact`; reason: owner-approved future scope and reusable delivery-policy decisions are recorded in this ignored planning artifact.
- Durable workflow memory or System Insights: not written.

## Follow-up

- Promote to commit/handoff only after owner review of the current diff; no automatic commit, push, or scheduler job is part of this scope.

## Implementation Range Evidence

- Range: sequential phase-4 implementation through quality, capture-state update, and checkpoint preparation.
- Slice status: `DAD-1` through `DAD-5` implemented and reviewed.
- Tracked implementation areas: delivery contract, routing, owner decisions, Plan Quality, implementation slicing, phase artifacts, templates, validators, smoke integration, workspace bootstrap, and guidance.
- Quality state: `ready`; fresh advisory closure completed, formal phase-6 distillation not recorded.
- No commit or push performed.

## Implementation Range Checkpoint

- Quality route: `global-quality-review-stance` for workflow-maintenance scope.
- Findings/blockers: `none known after fix loop and fresh findings-first QA`.
- DoD fit: `aligned`.
- Intent/plan/spec compliance: `aligned`.
- Validation: targeted validators, smoke suite, and explicit full profile completed without reported errors.
- Checkpoint state: `ready for owner review`; stop before any commit, push, or phase-8 equivalent.
