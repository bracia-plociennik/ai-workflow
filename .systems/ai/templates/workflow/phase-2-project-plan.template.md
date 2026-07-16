# 2. Project Plan

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Workflow phase: `2. FAZA PLANU PROJEKTU`
- Result: `<PASS|blocked|draft>`

## Sources

- Architecture: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/architecture/phase-1-architecture.md`
- Architecture QA: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/phase-1-architecture-qa.md`
- Initial audit: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/intake/phase-0-repo-intake.md`
- Context: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md` or `none`
- Planning router: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md`
- Task index: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks.md`
- Workflow rules: `.systems/ai/workflow/phase-2-project-plan.md`

## Planning Constraints

- 

## Decisions Closed During Planning

| Decision | Chosen Option | Reason | Impact |
| --- | --- | --- | --- |
| | | | |

## Task Contract Template

Each task must contain: ID in `<PROJECT>-<AREA>-<NNN>-<slug>` format, name, goal, scope, out-of-scope, DoD, dependencies, risk type, main risk, start condition, end condition, readiness status, and user-decision flag.

The same task IDs must be present in `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks.md`. Optional task cards may be created under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks/` when additional task-level context is useful.

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

## Plan Quality Contract

- Plan classification: `implementation-capable`
- DoD source: `<accepted owner intent|approved architecture|project plan acceptance criteria>`
- Testable DoD / acceptance conditions: `<conditions that make the plan executable without hidden scope or dependencies>`
- Artifact QA route: `phase-2-plan-qa`
- Artifact QA trigger: `after the project plan and task index are complete`
- Implementation Quality Closure route: `phase-5-quality` for each later formal implementation task
- Required verification: `<artifact review|task/index consistency|edge/regression review|adaptive data/integration matrix or not-applicable with reason>`
- Quality-ready criteria: `<all task contracts are complete and routing is evidence-backed>`
- Owner opt-out: `<none|Quality skipped by owner opt-out>`
- Not-applicable reason: `<none|reason>`
- Blocking decision: `<decision ID|none>`
- Next route: `phase-2-plan-qa`

## Plan Gate Decision

- All tasks have full contract: `<yes|no>`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md` routes to this plan: `<yes|no>`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks.md` exists and matches the plan: `<yes|no>`
- Dependencies are labeled: `<yes|no>`
- Blocking decisions resolved or task marked conditional/blocked: `<yes|no>`
- Ready for Plan QA: `<yes|no>`
- Blocking reason: `<none|reason>`

## Owner Decision Checkpoint

- Interaction mode: `<interactive|queued|suppressed-owner-opt-out|none>`
- Decision state: `<clear|awaiting-owner|blocked|queued>`
- Material decisions: `<decision IDs|none>`
- Questions asked: `<decision IDs|none>`
- Auto-resolved reversible decisions: `<decision IDs|none>`
- Optional owner refinements: `<list|none>`
- Decision artifacts: `<paths|none>`
- Next route:

## Optional Knowledge Capture

- Capture recommended: `<yes|no>`
- Target: `<project-memory|repo-memory|external-memory|system-insights|decision-artifact|status|none>`
- Reason:
- Owner decision required: `<yes|no>`
- Owner decision: `<capture-now|defer-to-distillation|defer-to-checkpoint|reject|not-requested>`
- Privacy/scope check: `<pass|fail|n/a>`
- Suggested entry title:
- Suggested entry summary:
