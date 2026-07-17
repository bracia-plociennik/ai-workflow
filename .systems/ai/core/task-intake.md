# task-intake.md

## Purpose

Task Idea Validation is the default pre-routing lens for any single new task, new idea, planning request, approach request, uncertainty request, side task, micro-task, change request, or autopilot request.

It is not a workflow phase and it does not grant write permission. It decides whether the user's raw request is clear, safe, complete, and routed to the correct workflow path before planning, specification, implementation, or automation begins.

Formal project-level brain dumps still use `.systems/ai/workflow/phase-0-idea-validation.md`. Multi-item owner lists first use `.systems/ai/core/request-batch-triage.md`. Task Idea Validation applies to smaller or already scoped work where creating a full project idea-validation artifact would be too heavy.

## Default Idea Validation And Owner Opt-Out

Default Idea Validation is required unless the owner explicitly opts out.

- Single new work defaults to Task Idea Validation before planning, specification, implementation, side-task, micro-task, micro-project, change request, or autopilot routing.
- New or broad project ideas default to formal `phase-0-idea-validation`.
- Batch/list/checklist input with `2+ owner items` defaults to `.systems/ai/core/request-batch-triage.md` first, then the selected item or group uses the appropriate validation route: Task Idea Validation for scoped work or formal `phase-0-idea-validation` for broad project ideas.

Owner opt-out grammar:

- `bez idea validation`;
- `bez walidacji pomysłu`;
- `without idea validation`;
- `skip idea validation`;
- `fast path no idea validation`.

When the owner uses one of these phrases, skip only the Task Idea Validation or idea-validation lens output. The response must report `Idea validation skipped by owner opt-out` and residual risk in `Execution Trace`.

The opt-out must not skip source-of-truth order, risk model, permissions, safe environment checks, required evidence, QA/Quality, owner approvals, phase gates, change-request routing, final owner approval, Definition of Done, prompt-injection policy, or status/evidence reconciliation.

If the opt-out leaves acceptance criteria, target project/workspace, risk, safe environment, write permission, or required evidence unclear, stop and request the missing decision instead of planning or executing. When owner no-question opt-out is also active, state the exact missing decision without interactive questioning.

## When To Use

Use this lens before acting on user requests such as:

- `mam nowe zadanie`;
- `trzeba zrobić`;
- `zaplanuj`;
- `wymyśl podejście`;
- `nie wiem jak to zrobić poprawnie`;
- `co będzie najlepszym rozwiązaniem`;
- `implementuj`, when the request introduces new scope;
- `side-task`, `micro-task`, or `micro-project`;
- `autopilot` or `autonomous-execution` for a new task set;
- a change request before or after `final-owner-yes`.

If the user provides a list, checklist, brain dump, mixed improvements, or `2+ owner items`, run request batch triage first through `.systems/ai/core/request-batch-triage.md`. After the batch is split and routed, apply the validation route to the selected single route or routed item unless the owner explicitly opts out and the remaining gates are clear.

If the user asks only for factual status, command output, or a narrow clarification that does not introduce new work, use guide or normal command routing instead.

## Required Validation Summary

Before presenting a plan or starting execution, provide or record a concise summary with these sections. Every substantive plan then includes `.systems/ai/core/plan-quality-contract.md` before implementation readiness is claimed.

### Co zostaje

State what is good, useful, already clear, and should remain part of the task.

### Co jest słabe / do poprawy lub usunięcia

State what is vague, risky, over-scoped, unsafe, duplicated, unnecessary, or should be changed before planning or implementation.

### Czego brakuje

State missing acceptance criteria, scope boundaries, inputs, target project, affected files, risk class, safe environment, evidence expectations, owner approvals, rollback expectations, or dependencies.

### Blokery / decyzje

List decisions or blockers that prevent safe planning, implementation, autopilot, or PASS. If there are no blockers, say so explicitly.

### Rekomendowany routing

Choose the safest workflow path:

- formal `phase-0-idea-validation` for a new project or large product idea;
- `phase-0-project-workspace` when the project workspace does not exist;
- project planning/specification when the task belongs to an active project;
- side-task or project-local micro-task only for low-risk, local work;
- repo-level micro-project only for low-risk work outside a full project workspace;
- change request triage through `.systems/ai/core/change-requests.md`;
- supervised autopilot only when task set, risk, gates, safe environment, and evidence are clear;
- STOP for missing approvals, unresolved high/critical risk, unsafe commands, or unknown safe environment.

## Owner Decision Discovery

After validation and before presenting a dependent plan or starting execution, use `.systems/ai/core/owner-decision-checkpoints.md`.

- Inspect repository and accepted artifacts before asking.
- Classify remaining choices as `auto-resolvable`, `owner-preference`, `high-impact`, `critical-risk`, or `blocked-by-missing-facts`.
- Ask at most 1-3 material questions that block the nearest safe next step.
- Put the recommendation first and state impact for every option.
- Report safe reversible decisions that were auto-resolved.
- If no material decision exists, continue and report `No owner decision needed`.

The owner no-question opt-out is separate from idea-validation opt-out. It suppresses interactive questions within the accepted scope but cannot make an unresolved hard gate executable.

## Modes

### Owner Request Batch

If the request contains `2+ owner items`, a checklist, a `lista rzeczy`, a mixed improvement list, or an explicit batch triage request, route to `.systems/ai/core/request-batch-triage.md` before ordinary Task Idea Validation.

The batch result must classify each item by group, theme, risk, routing, target project/workspace, dependencies, owner decision, and reason. It must split active-project work from repo-level work, split new project ideas from small workflow improvements, and route pre-final or post-final owner comments as change request candidates.

Batch triage is advisory and classificatory only. It does not grant write permission, does not start implementation, and does not automatically create projects, tasks, micro-tasks, micro-projects, change requests, commits, or pull requests.

After the owner chooses a route, continue with the normal single-item or single-group Task Idea Validation, workflow phase, change request, micro-task, micro-project, or project setup path.

### Project Idea

If the request is a new product/project idea, a broad feature concept, or a brain dump that should create project context, route to `phase-0-idea-validation`. The validation must use both chat input and raw source materials under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/` when present.

### Task In Active Project

If the request belongs to an active project, validate the task against `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/status.md`, `tasks.md`, `plans.md`, accepted architecture, accepted spec, and current blockers before routing. The result may be response-only or recorded in the next spec, task card, quality artifact, or change request.

### Side Task Or Micro-task

If the request is small, local, low-risk, and outside active plan scope, the validation can be short. It must still confirm low risk, local scope, no hidden external effects, no active-plan conflict, and required evidence.

If any side-task or micro-task condition fails, route into the normal workflow.

### Micro-project

If the request is small repo-level work outside a full project workspace, validate it as a micro-project only when it is low-risk and self-contained. Medium, high, or critical risk requires normal project workflow or owner approval.

### Change Request

If the request changes, corrects, removes, or adds scope before or after `final-owner-yes`, validate it first and then route through `.systems/ai/core/change-requests.md`. Do not treat owner comments as chat-only instructions.

### Autopilot

If the request starts or resumes autopilot, validate the requested range and task set before execution. Autopilot is allowed only when the range, tasks, risk classes, safe environment, approvals, gates, evidence, and stop conditions are clear.

Use `planning-range` when the owner wants Codex to run phase 1 architecture through phase 3 Spec QA and then stop before implementation. Use `implementation-range` when the owner wants Codex to run phase 4 implementation through required phase 7 checkpoint and then stop before owner-triggered final check.

### High Or Critical Risk

If the task touches auth, billing, permissions, migrations, security, production data, secrets, infrastructure, destructive operations, or real external side effects, stop unless the required approval and routing are already satisfied. Critical-risk work is human-led only.

## Artifact Rules

Task Idea Validation may be:

- included in the user-facing response when no durable artifact exists yet;
- recorded inside a task card, spec, micro-task artifact, micro-project artifact, change request, or plan artifact when one is being created or updated anyway;
- referenced from status or quality evidence when it affects routing or risk.

Do not create a separate artifact just to satisfy this lens unless the routed workflow path already requires one.

Do not store task-level validation in `.systems/**`. Target-specific validation belongs under `AI_WORKFLOW_WORKSPACE_HOME/**`.

## Delivery Constraint Discovery

For new implementation work, apply `.systems/ai/core/delivery-constraints.md` after repository facts are known. Discover an existing deadline, time budget, must-have outcome, and safe cutline before dependent planning. Ask only material missing questions through Owner Decision Discovery. A missing delivery constraint is not permission to invent one, and deadline pressure cannot bypass DoD, QA, evidence, permissions, risk, or approvals.

## Stop Conditions

Stop before planning or implementation when:

- the active project or target workspace is unknown;
- acceptance criteria or out-of-scope are missing and cannot be inferred safely;
- risk class is unknown or high/critical without required approval;
- safe commands or safe environment are unknown;
- external side effects are possible but not approved;
- requested writes are outside the phase write allowance;
- the request would bypass tests, evidence, Definition of Done, risk policy, permissions, or final owner approval.

## Response Pattern

For planning or approach responses, start with:

```text
Task Idea Validation

Co zostaje:
- ...

Co jest słabe / do poprawy lub usunięcia:
- ...

Czego brakuje:
- ...

Blokery / decyzje:
- ...

Rekomendowany routing:
- ...
```

Then provide the plan, clarification, or safe next step. Finish the whole response with the required `Co dalej?` footer from `.systems/ai/core/response-contract.md`.
