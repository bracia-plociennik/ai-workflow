# AGENTS.md

## Purpose

This file is the execution contract for AI agents working in a repository that uses this workflow template.

Use it to:

- keep work aligned with repository state;
- prevent guessing across unresolved decisions;
- enforce gates, evidence, QA, fix loops, checkpoints, and final owner approval;
- make the workflow portable across repositories.

`AGENTS.md` is for agents. `HUMANS.md` is the companion runbook for humans.

---

## Source Of Truth

Follow this order when sources disagree:

1. Current repository state.
2. Root `AGENTS.md`.
3. Approved project architecture, project plan, task specification, or task package specification.
4. `docs/ai/WORKFLOW.md`.
5. The relevant phase file in `docs/ai/workflow/`.
6. Repo-local runtime artifacts in `docs/repo/`, including `STATUS.md`, `CONTEXT.md`, `REPO-INTAKE.md`, and `MEMORY.md`.
7. Project status in `docs/projects/<project>/STATUS.md`.
8. Context, chat history, repo memory, external workflow memory, and other supporting notes.

Repository state is authoritative for actual implementation.
Workflow docs are authoritative for process.
Context is supporting input only.
Repo memory is an aggregate, not source of truth.
`docs/ai/EXTERNAL-MEMORY.md` is universal workflow/process memory only. It can inform future workflow improvements, but it does not override a concrete repo's execution contract, workflow gates, status, architecture, plan, specs, or repository state.

If process documents conflict or a shortcut is insufficient, stop and follow the most specific applicable phase file in `docs/ai/workflow/` together with this file.

---

## Core Operating Rules

- Make the smallest correct change that satisfies the approved task.
- Do not introduce implicit product, architecture, integration, security, legal, financial, or data decisions during implementation.
- Do not continue past unsatisfied gates.
- Do not mark `PASS` without explicit evidence.
- Do not guess across unresolved decisions.
- Do not modify product code during analysis, architecture, planning, or QA phases.
- During implementation, modify only files needed by the approved task scope.
- Do not revert user or unrelated changes unless explicitly asked.
- If a blocking unknown affects correctness, scope, sequencing, or implementation, stop and ask for the missing input or route to the correct fix loop.

Write operations are allowed only after:

- a plan or accepted execution instruction exists;
- required decisions are resolved or classified as auto-resolvable;
- the relevant implementation gate is satisfied;
- the user explicitly approves implementation or the active autopilot state allows it.

---

## Canonical Artifact Layout

Template-owned AI docs:

- `docs/ai/WORKFLOW.md` - operational workflow router.
- `docs/ai/workflow/` - detailed phase specifications.
- `docs/ai/AUTOPILOT.md` - autopilot operating guide.
- `docs/ai/MEMORY.md` - aggregate memory for this workflow template, not target-repo facts.
- `docs/ai/EXTERNAL-MEMORY.md` - universal workflow/process memory for improving this template.
- `docs/ai/templates/` - reusable artifact templates.

Repo-local runtime docs:

- `docs/repo/CONTEXT.md` - global description of the target repository, domain, stack, modules, boundaries, and local constraints.
- `docs/repo/REPO-INTAKE.md` - repo-level workflow/bootstrap readiness artifact for the target repository.
- `docs/repo/STATUS.md` - cross-project workflow status for the target repository.
- `docs/repo/MEMORY.md` - aggregate target-repo memory after checkpoints and final checks.

Project-local docs:

- `docs/projects/<project>/STATUS.md`
- `docs/projects/<project>/PROJECT-MEMORY.md`
- `docs/projects/<project>/intake/`
- `docs/projects/<project>/architecture/`
- `docs/projects/<project>/planning/`
- `docs/projects/<project>/specs/`
- `docs/projects/<project>/quality/`
- `docs/projects/<project>/decisions/`
- `docs/projects/<project>/escalations/`
- `docs/projects/<project>/distillations/`
- `docs/projects/<project>/checkpoints/`
- `docs/projects/<project>/autopilot/`

Some workflow artifacts use `<what_we_doing>` as the placeholder name. Treat `<what_we_doing>` and `<project>` as the same active project workspace directory.

Human-facing docs:

- `HUMANS.md` - global human runbook.
- `docs/humans/` - human-readable audits, runbooks, approvals, summaries, and decisions.

When an artifact is moved or renamed, update all repo-local references in workflow, status, plan, and task artifacts before considering the phase complete.

---

## Workflow Contract

Full phased workflow is mandatory for tasks derived from an active project plan under `docs/projects/<project>/planning/2_project_plan.md` while that plan still has open in-scope work or has not passed `8. FINAL CHECK`.

Full workflow is optional for side tasks after a project plan has passed final check, unless the user explicitly requests workflow mode or correctness requires formal gates.

For workflow-governed tasks, update `STATUS.md` whenever:

- a task or package becomes active;
- a phase starts;
- a phase ends with `PASS`, `FAIL`, `completed`, or `blocked`;
- a fix loop becomes the next phase;
- `8. FINAL CHECK` closes the active plan;
- operational drift is detected and resolved.

Do not skip required predecessor phases, QA gates, fix loops, or implementation gates.

---

## `/plan`, Specification, And Implementation

If this repository uses `/plan` as the phase-3 input:

- `/plan` means the execution plan for implementing the task or package.
- After an accepted `/plan`, treat the accepted task execution plan as the source text for the phase-3 specification artifact.
- If the user says `implement now`, first persist the accepted `/plan` into the phase-3 specification artifact, then continue into implementation if no gate blocks it.
- If the user says `spec qa`, first persist the accepted `/plan` into the phase-3 specification artifact, then run `3.5. SPEC QA` before implementation.
- The persisted specification should preserve the accepted plan in substance and structure unless the user explicitly asks for a rewrite.

Dependency-gated specifications may exist before implementation. Before implementation, refresh them against completed dependency outputs and run Spec QA again.

---

## Autopilot Contract

Autopilot may run only when the user explicitly requests autonomous execution or the active workflow state says the current work is under autopilot.

Autopilot is allowed only after the active project workspace has:

- repo-level workflow readiness recorded in `docs/repo/REPO-INTAKE.md`;
- context or explicit project input;
- repo intake / initial audit artifact;
- architecture artifact;
- Architecture QA `PASS`;
- project plan artifact;
- Plan QA `PASS`;
- task packaging result or explicit solo-execution decision;
- task specification for the next task or package;
- Spec QA `PASS` for the next task or package.

Autopilot executes implementation-stage work as a state machine:

```text
spec refresh/create
-> spec QA
-> spec fix loop when needed
-> implementation
-> quality
-> fix loop when needed
-> distillation
-> checkpoint after every 3 completed tasks/packages and after the final task/package
-> next task/package
-> final check
-> AWAITING_OWNER_FINAL_YES
```

Autopilot runtime artifacts:

- `docs/projects/<project>/autopilot/AUTOPILOT_STATE.md`
- `docs/projects/<project>/autopilot/AUTOPILOT_LEDGER.md`
- `docs/projects/<project>/autopilot/AUTOPILOT_EVENTS.md`

Use templates from `docs/ai/templates/autopilot/` when creating runtime artifacts.

Autopilot artifacts are workflow memory only. Repository state remains authoritative for implementation.

---

## Autopilot Preflight

Before each autopilot phase, check:

- `docs/repo/STATUS.md`;
- `docs/projects/<project>/STATUS.md`;
- `docs/projects/<project>/autopilot/AUTOPILOT_STATE.md`;
- `docs/projects/<project>/autopilot/AUTOPILOT_LEDGER.md`;
- required phase artifacts;
- duplicate, incomplete, outdated, or conflicting artifacts;
- task dependencies and implementation gates;
- dirty workspace and overlapping write set;
- drift between repo, architecture, plan, spec, implementation, checkpoint, and status;
- external workflow memory if the task promotes universal process lessons;
- critical-risk triggers;
- retry counters and execution budget.

If preflight finds a blocking issue, stop or route to the correct fix loop. Do not continue by guessing.

---

## Decision Protocol

Classify every unresolved decision:

- `auto-resolvable`: choose the recommendation, write the decision artifact, continue.
- `high-impact`: write recommendation and alternative, then stop for owner decision.
- `critical-risk`: hard stop and require explicit owner approval.
- `blocked-by-missing-facts`: explore repo and artifacts first; if still unknown and correctness is affected, stop.

Decision artifacts must include:

- decision class;
- recommendation;
- recommendation impact;
- alternative;
- alternative impact;
- chosen option;
- reason;
- owner override impact;
- date and scope.

Decision artifacts live in `docs/projects/<project>/decisions/`.

---

## Critical-Risk STOP

Stop before any materially irreversible, production-affecting, legal, financial, security-sensitive, destructive, or real-external-side-effect action.

Examples:

- production deploy or production infrastructure change;
- destructive database migration or bulk production data change;
- secrets, credentials, private keys, OAuth credentials, or production environment changes;
- billing, pricing, payments, compliance, KYC, funds flow, or contract decisions;
- legal or ToS-sensitive data collection, scraping, privacy, consent, or retention changes;
- paid vendor selection with material cost, lock-in, limits, contract, or data-rights impact;
- real emails, alerts, tickets, invoices, payments, or external API writes to real users or customers;
- force-push, release publishing, branch/tag deletion, destructive git operations, or destructive database operations.

Do not classify a normal implementation choice as critical-risk only because it is complex.

---

## Artifact Reconciliation

If a phase artifact already exists, do not create a duplicate by default.

Classify it:

- `current`: reuse it.
- `incomplete`: update missing required parts only.
- `outdated`: refresh minimally and record drift.
- `conflicting`: run the correct fix loop or stop if correctness/scope is affected.
- `duplicate`: choose a canonical artifact, record the duplicate, and do not delete without owner approval unless it is inside a newly created template copy and the user explicitly requested cleanup.

Before implementation, reconcile the task spec with current repo state, completed dependency outputs, and status.

---

## Recovery And Idempotency

After interruption, context compaction, restart, or partial run:

1. Read `docs/repo/STATUS.md`.
2. Read project-local `STATUS.md`.
3. Read autopilot state and ledger if autopilot is active.
4. Check the relevant phase artifacts.
5. Check `git status`.
6. Resume only from the last stable `PASS` with evidence.

If status, state, ledger, artifacts, and repo do not agree, write an escalation artifact in `docs/projects/<project>/escalations/` and stop.

---

## Retry And Escalation

Default autopilot limits:

- max 2 Spec QA fix loops per task or package;
- max 2 Quality fix loops per task or package;
- max 32 total retries per 16-task autopilot run, unless the project decision states otherwise;
- max 1 parallel task unless packaging explicitly permits more;
- checkpoint every 3 completed tasks/packages and after the final task/package.

When a retry limit is reached:

- write an escalation artifact in `docs/projects/<project>/escalations/`;
- update status and autopilot state;
- stop for owner action.

---

## Quality Contract

`PASS` and `FAIL` are binary.

`PASS` requires:

- 100% of task or package DoD satisfied;
- no known bug in scope;
- no regression in changed and directly dependent paths;
- edge cases covered or explicitly rejected with justification;
- required test, QA, or manual verification evidence recorded.

`FAIL` applies if any condition above is unmet.

Warnings do not override unmet DoD, regressions, correctness issues, missing evidence, or unsatisfied gates.

---

## Task Intake Modes

### Micro-task

Allowed only when the task is:

- small;
- local;
- low risk;
- not in a high-risk area;
- free of unresolved decisions;
- free of architecture, integration, data, or external side-effect impact.

Micro-tasks still require repo-first execution, stop conditions, and evidence-based quality.

### Standard Task

Required when any micro-task condition is false.

Standard tasks require a task or package contract:

- goal;
- scope;
- out-of-scope;
- DoD;
- dependencies;
- risk type;
- main risk;
- start conditions;
- end conditions;
- readiness status: `ready`, `conditional`, or `blocked`;
- user-decision flag.

A task that requires owner decision must not be treated as ready for implementation.

---

## Repo Runtime Layer

Do not adapt `AGENTS.md` when installing this template into a target repository.

Repo-specific facts discovered during `0. REPO INTAKE / INITIAL AUDIT` belong in `docs/repo/`, primarily:

- `docs/repo/CONTEXT.md` for the global repository description;
- `docs/repo/REPO-INTAKE.md` for command discovery, safe environment policy, risks, restricted zones, and readiness;
- `docs/repo/STATUS.md` for current cross-project workflow state;
- `docs/repo/MEMORY.md` for aggregate repo memory after checkpoints or final checks.

If a command cannot be discovered from repo state, record `not configured` in `docs/repo/REPO-INTAKE.md` rather than inventing it.

### Safe Test Environment

Define the safe local/test environment in `docs/repo/REPO-INTAKE.md` before implementation:

- test database strategy;
- fake or test service adapters;
- mail/notification strategy;
- queue/background job strategy;
- external API strategy;
- commands that must never run against production.

If no safe test environment exists, autopilot must stop before implementation that requires it.

### High-Risk Areas

Every repository should refine this list in `docs/repo/REPO-INTAKE.md`. Default high-risk areas:

- environment configuration and secrets;
- authentication, authorization, and permission boundaries;
- database migrations and persistent data models;
- scheduler, cron, queue workers, and background jobs;
- external integrations, webhooks, mail, notifications, and API writes;
- billing, pricing, payments, legal, compliance, and data retention;
- destructive operations and bulk data changes;
- security-sensitive user or customer data;
- deployment and release automation.

High-risk areas are not eligible for micro-task handling.

### Restricted Zones

Every repository should refine this list in `docs/repo/REPO-INTAKE.md`. Default restricted zones:

- secret-bearing files such as `.env*`;
- dependency directories;
- generated/runtime/cache/build artifacts;
- local databases and backups;
- production deployment manifests;
- historical project docs outside the active task scope;
- aggregate memory files unless the active phase explicitly updates them.
- `docs/ai/EXTERNAL-MEMORY.md`, unless the task is workflow maintenance or a checkpoint has a universal workflow lesson to promote.

Do not edit restricted zones unless the approved task explicitly targets them.

### Domain Operating Rules

Add repository-specific domain rules to `docs/repo/CONTEXT.md`, `docs/repo/REPO-INTAKE.md`, and project artifacts during intake and architecture.

Do not keep real project names, clients, credentials, production details, or vendor-specific assumptions in `AGENTS.md`, `HUMANS.md`, root workflow files, or `docs/ai/`.

---

## Git Policy

Default policy:

- use a task or autopilot branch, for example `codex/<project-or-scope>`;
- commit after task/package `QUALITY PASS`;
- do not commit known-failing work unless the commit is explicitly marked as blocked/partial and the owner asked for it;
- push and PR only according to owner policy;
- never force-push, delete branches/tags, or rewrite shared history without explicit owner approval.

---

## Final Owner Approval

Final check cannot close an active plan with full `PASS` without explicit owner approval.

If final check finds no issues, set the project to `AWAITING_OWNER_FINAL_YES` and wait for the owner to close the project.
