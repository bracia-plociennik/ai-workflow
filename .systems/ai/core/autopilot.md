# autopilot.md

## Purpose

This file defines how Codex may run workflow ranges autonomously after the matching readiness gates pass.

It does not replace:

- `AGENTS.md`
- `.systems/ai/core/operating-model.md`
- `.systems/ai/core/workflow.md`
- `.systems/ai/core/risk-model.md`
- current phase files under `.systems/ai/workflow/`

## Autopilot Ranges

Autopilot has explicit ranges. A run must declare exactly one range in `readiness.md` before it can enter `running`.

### `planning-range`

`planning-range` covers pre-implementation project design work:

```text
phase-1-architecture
-> phase-1-architecture-qa
-> phase-1-architecture-fix-loop when needed
-> phase-2-project-plan
-> phase-2-plan-qa
-> phase-2-plan-fix-loop when needed
-> phase-3-specification for every planned task by default
   or optional owner-requested phase-2-task-packaging -> phase-2-packaging-qa when packages exist -> phase-2-package-fix-loop when needed -> phase-3-specification for every planned package
-> phase-3-spec-qa for every planned task/package
-> phase-3-spec-fix-loop when needed
-> stop before implementation
```

`planning-range` may write workflow artifacts only. It must not write product code. Its output is a project state that is ready or not ready for implementation-range.

### `implementation-range`

`implementation-range` covers task execution after planning gates are satisfied:

```text
phase-3-specification refresh for current task/package when needed
-> phase-3-spec-qa
-> phase-3-spec-fix-loop when needed
-> phase-4-implementation
-> phase-5-quality
-> phase-5-fix-loop when needed
-> phase-6-distillation
-> phase-7-checkpoint when checkpoint cadence requires it
-> next task/package
-> final phase-7-checkpoint after the last task/package
-> stop before phase 8
```

Before implementing task/package `N+1`, Codex must review the previous implementation result, quality evidence, distillation, checkpoint state, project memory, repo memory, decisions, and drift findings. If task/package `N` changed assumptions for `N+1`, Codex must refresh the `N+1` spec and rerun Spec QA before implementation.

For implementation-range, checkpoint after every 3 completed tasks/packages and after the final task/package is a hard autopilot gate. Autopilot must stop or run `phase-7-checkpoint` before continuing when the checkpoint cadence is reached.

### Owner-only `phase-8-final-check`

`phase-8-final-check` is owner-triggered only.

Autopilot must not automatically run `phase-8-final-check`.

After planning-range, autopilot stops before implementation.

After implementation-range, autopilot stops after the final required `phase-7-checkpoint` and reports whether the project appears ready for owner-triggered final check.

Only the owner can start `phase-8-final-check` with an explicit request. Technical final check still cannot close the project without `final-owner-yes`.

## Start Conditions

Autopilot may start only when:

- the user explicitly requests autonomous execution or project status says autopilot is active;
- run-scoped readiness audit exists at `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/<run-id>/readiness.md`;
- readiness audit has `readiness-result: ready`;
- readiness audit declares `requested-range` as `planning-range` or `implementation-range`;
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`, `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`, `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`, and `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` exist;
- active project status exists at `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/status.md`;
- risk class permits autopilot under `.systems/ai/core/risk-model.md`;
- required commands are known through `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md` and `.systems/ai/core/commands.md`.

Additional `planning-range` start conditions:

- accepted project context exists at `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md`;
- project/context repo intake is complete enough to identify safe commands, restricted zones, and external-effect policy;
- missing architecture, plan, optional owner-requested packaging, and specs are expected outputs of the range and must be listed as planned writes, not blockers;
- owner decisions needed before architecture or planning are resolved or listed as `awaiting-owner`.

Additional `implementation-range` start conditions:

- architecture and Architecture QA have `PASS`;
- project plan and Plan QA have `PASS`;
- task packaging is complete, explicitly skipped, or not requested for solo-by-default execution;
- the first task/package spec exists;
- Spec QA for the first task/package has `PASS`;
- implementation write scope is limited to the accepted spec and approved task/package range.

## Runtime Files

Runtime files live under run directories in `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/`.

Each run uses a monotonic ID such as `autopilot-001`:

- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/readiness.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/state.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/ledger.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/autopilot-001/events.md`

Root-level `autopilot-state.md`, `autopilot-ledger.md`, and `autopilot-events.md` are not canonical.

Templates live under `.systems/ai/templates/autopilot/`.

## Autopilot Readiness Audit

Before starting or resuming autopilot, Codex must create or update the run-scoped readiness artifact:

```text
AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/autopilot/runs/<run-id>/readiness.md
```

The readiness audit checks every likely blocker before the requested range begins:

- repo context, repo intake, repo status, command map, safe environment, restricted zones, and git policy;
- active project status, project context, architecture, plan, packaging, tasks, specs, quality expectations, decisions, change requests, escalations, checkpoints, and previous autopilot runs;
- risk model, permissions, Definition of Done, rollback, dependencies, prompt-injection policy, response contract, task intake, and matching skills;
- external effects including email, payments, CRM/API writes, migrations, production data, secrets, destructive operations, and infrastructure changes.

Readiness status values are:

- `draft`: audit is being prepared;
- `blocked`: workflow gates, status, artifacts, commands, safe env, or evidence requirements are missing;
- `awaiting-owner`: owner decisions or approvals are required;
- `ready`: all blocking items are resolved, approved, or not applicable;
- `superseded`: scope, mode, task set, or run changed and a newer readiness artifact replaces this one.

Autopilot cannot enter `running` until readiness is `ready`. If readiness is `blocked` or `awaiting-owner`, run state must remain `stopped` or `awaiting-owner`, and the owner-facing prompt must list every required decision.

If no run exists, create the next `autopilot-XXX` directory and fill `readiness.md` before `state.md` can move to `running`. If an existing run is `awaiting-owner`, update the same `readiness.md` after owner answers unless scope, mode, or task set changed. If scope changes, supersede the old readiness artifact and create a new one for the new run or scope.

## State Machine

Use the range state machines above. Do not run `phase-8-final-check` from autopilot.

## Default Execution Rules

- Execute sequentially unless task packaging explicitly permits a package or parallel execution.
- Continue only after evidence-backed `PASS`.
- STOP on critical risk, retry limit, blocking drift, or missing required evidence.
- Record auto-resolvable decisions before continuing.
- Stop for human approval on high-risk and critical-risk decisions.
- Use fake/log/test adapters by default for external effects.
- Do not send real emails, alerts, tickets, invoices, payments, production cron, or external API writes without explicit owner approval.

## Retry Limits

- Max 2 Spec QA fix loops per task/package.
- Max 2 Quality fix loops per task/package.
- Max 32 total retries per 16-task autopilot run unless a project decision overrides it.
- Checkpoint after every 3 completed tasks/packages and after the final task/package.
- In `implementation-range`, checkpoint cadence is a hard gate. Do not continue to the next task/package when the cadence is reached until `phase-7-checkpoint` is complete or the owner explicitly stops autopilot.

## Git Policy

- Use an isolated branch such as `codex/<project>-autopilot`.
- Commit only after `QUALITY PASS`.
- Push and PR only under explicit owner approval or repository policy.
- Never force-push, delete branches/tags, or rewrite shared history without explicit approval.

## Stop Conditions

Autopilot must stop and write an escalation artifact when:

- required gates are unsatisfied;
- repo, status, plan, spec, ledger, or runtime state conflicts;
- risk class requires human approval;
- retry or budget limit is reached;
- a required command is missing or unsafe;
- evidence cannot support `PASS`;
- prompt-injection defense is triggered;
- a destructive or production-affecting action would be needed.
