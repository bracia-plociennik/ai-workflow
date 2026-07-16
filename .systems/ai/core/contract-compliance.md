# contract-compliance.md

## Purpose

This policy defines the advisory work-mode compliance check and the commit readiness / knowledge capture gate.

It exists to make every commit decision explicit without creating a mechanical requirement to write memory, distillation, or checkpoint artifacts for every commit.

It is separate from the phase-level `Optional Knowledge Capture` block. Phase capture records whether a phase produced candidate knowledge; commit readiness records whether a commit or handoff still needs a durable synchronization step.

## Advisory Only

This gate is advisory-only. It does not replace phase gates, risk policy, permissions, Definition of Done, required evidence, stop conditions, or owner approvals.

For implementation-capable work, contract compliance also confirms that `.systems/ai/core/plan-quality-contract.md` is complete before implementation-class writes: testable DoD, artifact QA route, implementation quality-closure route, verification criteria, and blocking route are explicit. A read-only plan must justify `not-applicable` and cannot be reported as implementation-ready.

Agents should run the check before committing or preparing a commit summary. A missing runtime capture decision is not a validator hard stop by itself, but the final response or commit-ready summary should state the decision.

If the relevant phase artifact already contains `Optional Knowledge Capture`, use it as evidence for this gate. If the phase decision says `defer-to-distillation` or `defer-to-checkpoint`, do not duplicate durable memory before the routed phase unless the owner explicitly approves capture now and permissions allow it.

## Work Mode Compliance

Before implementation, commit, or handoff, classify the work mode:

| Work mode | Use when | Required contract |
| --- | --- | --- |
| `full-project` | work belongs to an active project plan/task/package | project status, task/spec/quality gates, distillation/checkpoint when required |
| `project-local-micro-task` | small low-risk work inside one project but outside full phase flow | `micro-tasks.md` or detailed micro-task artifact when durable, evidence, promote decision |
| `repo-level-micro-project` | small low-risk repo-level work outside a project workspace | `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/<micro-project>/micro-project.md`, evidence, promote decision |
| `dreaming-mode` | advisory AFK/nightly analysis that writes only Dream Reports | `AI_WORKFLOW_WORKSPACE_HOME/dreams/runs/**`, privacy/scope check, owner decision queue |
| `side-task` | one-off small local low-risk change with no durable project record needed | risk classification, evidence, no conflicts, final response record |
| `workflow-maintenance` | changes to AI Workflow system docs, templates, validators, scripts, or examples in the official repo | changelog/version/docs/validator evidence, branch policy, no runtime tracking |

`global-quality-review-stance` from `.systems/ai/core/quality-review.md` can be used inside any work mode as read-only/advisory quality review. It does not create a formal quality artifact and does not replace work mode compliance, evidence, risk, write permissions, or formal phase gates.

Review Completeness Gate applies to advisory review and formal `phase-5-quality`. It requires cross-contract consistency, explicit risk/work mode compatibility, negative-space/adversarial review when validators or policy boundaries are involved, a policy-boundary adversarial matrix and producer-consumer field audit when applicable, automated evidence treated as supporting-only, a full-current-state post-fix re-review, a reviewed baseline, and `Closure freshness: current` before a quality-ready verdict.

Instruction Adherence Refresh from `.systems/ai/core/instruction-adherence-refresh.md` is required before commit readiness or handoff. Use targeted refresh when continuity is intact and full refresh after resume, compaction, working-directory change, long interruption, or conflict. A stale or blocked instruction baseline blocks commit readiness.

Owner Decision Checkpoint from `.systems/ai/core/owner-decision-checkpoints.md` must be current before commit or handoff. A material `awaiting-owner` or `blocked` decision blocks commit readiness. Optional refinements and disclosed reversible auto-resolved decisions do not block readiness.

`request-batch-triage` from `.systems/ai/core/request-batch-triage.md` can precede any work mode when the owner provides multiple items. It classifies and recommends routes only. It is not itself commit-ready evidence for implementation and does not create projects, tasks, micro-tasks, micro-projects, change requests, commits, or pull requests without the separately approved routed work mode.

Default Quality Closure from `.systems/ai/core/quality-review.md` applies before handoff or commit for substantive work. Use formal QA/Quality when the active workflow defines it; otherwise use advisory `global-quality-review-stance`. After implementation, slice execution, or fix work, quality closure must cover verify/review evidence, findings/blockers, DoD fit, intent/plan/spec/prompt compliance, changed files review, edge cases, regression risk, skipped checks impact, and residual risk. If the owner opts out with `bez QA`, `bez review`, `bez quality`, `bez weryfikacji`, `bez sprawdzania`, `without QA`, `without review`, `without verification`, `no verification`, or `fast path no review`, record `Quality skipped by owner opt-out` plus residual risk. Opt-out does not satisfy required QA PASS and cannot bypass risk, permissions, evidence, DoD, approvals, or stop conditions.

Formal `PASS` requires the PASS Integrity Gate from `.systems/ai/core/quality-review.md`: findings-first review, DoD fit, intent/plan/spec/prompt compliance, and no unresolved `P0`, `P1`, or material `P2` findings. Advisory quality closure for side tasks, micro-tasks, micro-projects, and workflow-maintenance must not create formal `PASS`; use evidence wording such as `No blockers found`, `No findings found`, or `Ready for owner review`.

Validation Profiles from `.systems/ai/core/validation-profiles.md` apply to workflow validation evidence. `.systems/scripts/validate-workflow` with no arguments uses `standard` for daily iteration and ordinary post-implementation quality. Use `full` for checkpoint validation, major distillation, major verification, CI, release/final confidence checks, and high-impact workflow-template changes. `fast` and `scoped` are iteration aids unless the owner explicitly accepts narrow validation with residual risk.

End-of-Task Capture from `.systems/ai/core/end-of-task-capture.md` can precede handoff when the owner says the task is done and asks to preserve learnings. It is capture review/proposal by default. It does not replace this compliance gate, and it does not grant permission to skip evidence, quality, risk, phase gates, memory scope boundaries, or owner approvals.

Knowledge Capture Reminder from `.systems/ai/core/knowledge-capture-reminder.md` applies after implementation, fixes, quality closure, handoff, commit readiness, or before switching to a new unrelated task when previous work may have unresolved capture value. It is a pre-handoff and pre-new-work lens, not a hard requirement for every task. It can recommend capture targets, but durable writes still require target, scope, privacy, evidence, write permission, and the correct phase or artifact path.

The selected mode must match risk, scope, approvals, write set, and artifacts. If the mode does not fit, route to the safer workflow path before continuing.

## Compliance Questions

Answer these before commit or handoff:

- `Work mode compliance: pass|warning|blocked`
- `Work mode: <full-project|project-local-micro-task|repo-level-micro-project|side-task|workflow-maintenance>`
- `Risk/work mode compatible: yes|no`
- `Scope/acceptance clear: yes|no`
- `Risk allowed for mode: yes|no`
- `Required artifacts current: yes|no|not-applicable`
- `Write-set conflicts: none|warning|blocked`
- `Evidence available: yes|no`
- `Quality closure: formal|advisory|skipped-owner-opt-out|not-applicable`
- `Review completeness gate: complete|incomplete|not-applicable`
- `Instruction refresh: performed-targeted|performed-full|not-needed|blocked`
- `Instruction baseline: current|stale|blocked`
- `Owner decision state: clear|awaiting-owner|blocked|queued|not-applicable`
- `Post-fix full re-review: completed|not-required|incomplete`
- `Closure freshness: current|stale|not-applicable`
- `Knowledge capture: required|not-required`
- `Knowledge capture target: <status/evidence|micro-task-artifact|micro-project-artifact|phase-6-distillation|phase-7-checkpoint|project-memory|repo-memory|external-memory|system-insights|not-applicable>`
- `Reason: <short evidence-backed reason>`

If any answer is `blocked` or `no` for a required item, stop before commit unless the current phase explicitly allows recording the blocker.

If risk is not compatible with the selected work mode, route to an allowed mode before implementation or handoff. Medium-risk, high-risk, and critical-risk work must not remain in micro-task or repo-level-micro-project mode. If review completeness is incomplete, post-fix full re-review is incomplete, or closure freshness is stale, do not report commit readiness.

If Instruction refresh is `blocked` or Instruction baseline is `stale|blocked`, stop before commit or handoff. `not-needed` is valid only when the current scope already has a current refresh baseline and no new trigger occurred.

## Knowledge Capture Decision

Do not write memory automatically for every commit. Capture is required only when the work produced durable knowledge or closed a workflow unit that requires synchronization.

Do not write memory automatically after every phase. The phase-level `Optional Knowledge Capture` block may recommend capture, defer capture, reject capture, or record that no capture is needed.

Capture is required when any of these are true:

- a full-project task/package reached Quality PASS and needs `phase-6-distillation`;
- checkpoint cadence is reached or the final in-scope task/package is complete and needs `phase-7-checkpoint`;
- project status, task status, QA evidence, or acceptance state changed;
- a durable micro-task or micro-project completed, blocked, or was promoted;
- a decision, constraint, workaround, residual risk, rollback note, or future blocker changed;
- repo-level reusable facts changed;
- AI Workflow itself needs a reusable improvement proposal for External Memory;
- anonymized reusable operating lessons should become System Insight candidates.

Capture is normally not required when:

- the change is docs-only or typo-only and creates no new operational knowledge;
- validator or formatting-only maintenance has no reusable lesson beyond changelog/version evidence;
- the final response and commit message already contain sufficient non-durable evidence;
- the relevant phase artifact already captured the same fact and no status changed.

When capture is not required, state `Knowledge capture: not-required` with a short reason.

## Mode-Specific Capture Targets

| Work mode | Default capture target |
| --- | --- |
| `full-project` | status/evidence, then `phase-6-distillation` or `phase-7-checkpoint` when gates require it |
| `project-local-micro-task` | micro-task artifact or final response evidence; promote to full workflow if risk/scope grows |
| `repo-level-micro-project` | `micro-project.md` evidence/update; promote if risk/scope grows |
| `dreaming-mode` | Dream Report evidence only; promote candidates through later owner-approved memory, insight, skill, status, task, or workflow route |
| `side-task` | final response evidence unless the owner requested durable capture |
| `workflow-maintenance` | changelog/version/docs/validator evidence; External Memory only for reusable workflow improvement proposals |

Project Memory, Repo Memory, External Memory, and System Insights keep their existing scope boundaries. This gate does not grant permission to write the wrong memory type.

End-of-Task Capture may be used to decide this target at handoff, but it must not duplicate an existing phase `Optional Knowledge Capture`, distillation, checkpoint, or commit-readiness decision.

## Commit Summary Requirement

Before committing, the agent should be able to report:

```text
Contract compliance:
- Work mode: <mode>
- Compliance: <pass|warning|blocked>
- Evidence: <commands/artifacts>
- Knowledge capture: <required|not-required>
- Capture target: <target>
- Reason: <reason>
```

This summary may live in the final response, a phase artifact, a micro-task/micro-project artifact, or a review note. It is not required to be embedded in the git commit message.
