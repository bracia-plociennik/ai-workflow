# 2. Project Plan

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Workflow phase: `2. FAZA PLANU PROJEKTU`
- Result: `<PASS|blocked|draft>`

## Sources

- Architecture: `docs/projects/<project>/architecture/phase-1-architecture.md`
- Architecture QA: `docs/projects/<project>/quality/phase-1-architecture-qa.md`
- Initial audit: `docs/projects/<project>/intake/phase-0-repo-intake.md`
- Context: `docs/projects/<project>/context.md` or `none`
- Planning router: `docs/projects/<project>/plans.md`
- Task index: `docs/projects/<project>/tasks.md`
- Workflow rules: `docs/ai/workflow/phase-2-project-plan.md`

## Planning Constraints

- 

## Decisions Closed During Planning

| Decision | Chosen Option | Reason | Impact |
| --- | --- | --- | --- |
| | | | |

## Task Contract Template

Each task must contain: ID in `<PROJECT>-<AREA>-<NNN>-<slug>` format, name, goal, scope, out-of-scope, DoD, dependencies, risk type, main risk, start condition, end condition, readiness status, and user-decision flag.

The same task IDs must be present in `docs/projects/<project>/tasks.md`. Optional task cards may be created under `docs/projects/<project>/tasks/` when additional task-level context is useful.

## Tasks

### `<TASK-ID> <Task Name>`

- Goal:
- Scope:
- Out of scope:
- Definition of Done:
- Dependencies:
  - blocking:
  - informational:
  - optional:
- Risk type:
- Main risk:
- Start condition:
- End condition:
- Readiness status: `<ready|conditional|blocked>`
- Requires user decision before implementation: `<yes|no>`

## Final Execution Order

1. `<TASK-ID>`

## Task Index Sync

| Task ID | Present in `tasks.md`? | Risk matches? | Status matches? | Task card needed? | Spec path set? | Quality path set? |
| --- | --- | --- | --- | --- | --- | --- |
| `<TASK-ID>` | `<yes|no>` | `<yes|no>` | `<yes|no>` | `<yes|no>` | `<yes|no>` | `<yes|no>` |

## Dependency Map

| Task | Blocking | Informational | Optional |
| --- | --- | --- | --- |
| | | | |

## Highest-Risk Tasks

| Task | Risk | Mitigation |
| --- | --- | --- |
| | | |

## Conditional / Blocked / Spike Tasks

| Task | Status | Blocking Condition | Required Decision |
| --- | --- | --- | --- |
| | | | |

## Architecture Coverage Map

| Architecture Area | Covered By Task(s) | Gap? |
| --- | --- | --- |
| | | `<yes|no>` |

## Plan Gate Decision

- All tasks have full contract: `<yes|no>`
- `docs/projects/<project>/plans.md` routes to this plan: `<yes|no>`
- `docs/projects/<project>/tasks.md` exists and matches the plan: `<yes|no>`
- Dependencies are labeled: `<yes|no>`
- Blocking decisions resolved or task marked conditional/blocked: `<yes|no>`
- Ready for Plan QA: `<yes|no>`
- Blocking reason: `<none|reason>`
