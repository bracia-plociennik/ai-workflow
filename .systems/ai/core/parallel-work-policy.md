# parallel-work-policy.md

## Purpose

This policy defines how multiple Codex threads, project workspaces, micro-tasks, and micro-projects may operate against one target repository without corrupting status, memory, evidence, or product-code write sets.

This is a status-only coordination policy for v1. It does not introduce lock files, new status fields, or a scheduler.

## Coordination Model

Use one main repo coordination thread for repository-wide state and one focused thread per project, task/package, micro-task, or micro-project.

- Main repo thread: coordinates repo-level status, global blockers, owner decisions, repo memory, external memory, system insights, and cross-project write-set conflicts.
- Project thread: works within exactly one `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/` workspace and one approved task/package or phase at a time.
- Micro-task thread: works within one project-local micro-task when the work is small, local, low-risk, and outside the active plan or explicitly marked as a micro-task.
- Micro-project thread: works within one `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/<slug>/` workspace and only for low-risk repo-level work.

`AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` is a repo focus snapshot, not a multi-project scheduler. It may point to the currently coordinated project or blocker, but it does not mean other project workspaces do not exist.

`AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/status.md` is the project-local source for that project's current phase, task, blockers, active change request, and autopilot state.

## When Parallel Work Is Allowed

Parallel work is allowed only when all of the following are true:

- each thread has a clear project, task, micro-task, or micro-project identity;
- no two threads intend to modify the same status router, memory router, quality artifact, task/spec artifact, or product-code write set;
- no blocking dependency exists between the active tasks/packages;
- no shared unresolved architecture, business, security, data, migration, or external-effect decision is required;
- no shared risky integration is being changed from multiple threads;
- each thread can produce its own evidence without relying on another in-progress thread's unverified result.

Because v1 has no lock files, scheduler state, or active-thread registry, active parallel work is known only from owner direction, the main repo coordination thread, current status artifacts, and current repository state. If the active threads or their intended write sets are unknown, treat overlap as unknown and stop before writing.

Default to linear execution when independence is uncertain.

## Status Ownership

- Repo status owns repository focus, global blockers, active coordination context, repo-level side tasks, micro-project focus, and cross-project conflicts.
- Project status owns a single project's current task/package, phase, result, next phase, active change request, and autopilot run.
- `tasks.md`, `plans.md`, `quality/`, `distillations/`, and `checkpoints/` remain project-local.
- `micro-tasks.md` owns project-local low-risk micro-task routing.
- `micro-project.md` owns one repo-level low-risk micro-project.

Do not use repo status as the source of truth for every active project. When resuming a project thread, read that project's status and task artifacts directly.

When a repo-level micro-project is the current repo focus, use existing repo status fields only: set `workflow-scope` to `micro-project`, keep `active-project` as `none`, and identify the micro-project in `current-task` as `micro-project:<slug>`.

## Memory Ownership

- Project memory stores durable knowledge for one project only.
- Repo memory stores repo-wide facts, constraints, command notes, and risks only.
- External memory stores AI Workflow improvement proposals only and is advisory until promoted.
- System Insights store anonymized cross-project operating lessons and skill candidates only and are advisory until accepted or promoted.

Parallel threads must not update project memory, repo memory, external memory, or system insights ad hoc unless the owner explicitly approves that memory update, or the routed checkpoint/final-check phase permits it.

When several threads produce related lessons, aggregate them through checkpoint or an owner-approved memory task instead of duplicating entries.

## Write-Set Discipline

Before implementation or artifact writes, each thread must identify its intended write set from the accepted plan, spec, micro-task, micro-project, change request, or owner command.

Stop before writing when:

- `git status` shows dirty tracked or untracked files in the intended write set, status routes, memory routes, artifact roots, or product-code paths that are not understood;
- another active thread may be modifying the same files or artifacts, or active threads/write sets cannot be identified clearly;
- two active implementation runs or implementation-range autopilot runs target the same project;
- a thread would update a status router or memory router already being updated by another thread;
- a thread would rely on unverified output from another in-progress thread;
- the change would cross project boundaries without owner approval.

If overlap is intentional, the main repo coordination thread must record the owner decision and the safe execution order before work continues. Owner-approved overlap may allow read-only parallel work or serialized writes, but it must not allow simultaneous writes to the same status router, memory router, artifact, or file.

Within one project, parallel task/package threads are read-only, planning, or specification work by default. Product-code writes, project status updates, checkpoint writes, and project memory updates must be serialized unless the main repo coordination thread records non-overlapping write sets and a single writer for the shared project router.

## Autopilot

Do not run two implementation-range autopilots in the same project at the same time.

Parallel planning-range autopilots are allowed only when their project workspaces, owner decisions, architecture scope, and write sets are independent.

Checkpoint cadence remains mandatory for implementation-range autopilot. Parallel work cannot be used to skip distillation, checkpoint, quality, evidence, or owner approval.

## Recovery

If parallel work causes drift:

- stop the affected threads;
- read `git status`, repo status, project statuses, task indexes, active change requests, quality evidence, checkpoints, and memory;
- classify the conflict as critical, warning, or informational;
- route to recovery, checkpoint, fix loop, or owner decision before continuing.

Do not silently choose one thread's status or memory over repository state.
