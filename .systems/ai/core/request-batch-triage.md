# request-batch-triage.md

## Purpose

`request-batch-triage` is the pre-routing contract for owner requests that contain multiple things to do.

Use it before normal Task Idea Validation when the owner provides `2+ owner items`, a checklist, a brain dump, a `lista rzeczy`, mixed improvements, or an explicit batch triage request. The goal is to split, group, classify, and route the items before planning, specification, implementation, artifact creation, or automation begins.

Batch triage is not a workflow phase. It does not grant write permission, does not implement work, does not commit, does not open pull requests, and does not automatically create projects, tasks, micro-tasks, micro-projects, or change requests.

## Trigger

Run request batch triage when the owner says or implies:

- `mam listę rzeczy do zrobienia`;
- `oto kilka pomysłów`;
- `pogrupuj te zadania`;
- `sklasyfikuj tę listę`;
- `rozdziel to między projekty, micro-projecty, taski i change requesty`;
- `I have a list of things to do`;
- `group these requests`;
- `triage this batch`;
- `split these items into projects and tasks`;
- any request with `2+ owner items` that introduces new scope.

Single-item requests continue through `.systems/ai/core/task-intake.md` without this batch layer.

## Default Idea Validation Relationship

Batch triage runs before Task Idea Validation for lists and mixed batches. It is classification and safety routing, not the idea validation itself.

After triage, the selected item or selected group must continue through the appropriate validation route unless the owner explicitly opts out:

- scoped single work -> Task Idea Validation;
- new or broad project idea -> formal `phase-0-idea-validation`;
- mixed routes -> one validation route per selected route.

Owner opt-out phrases are `bez idea validation`, `bez walidacji pomysłu`, `without idea validation`, `skip idea validation`, and `fast path no idea validation`. On a batch request, those phrases skip only the validation lens after triage when safe; opt-out does not skip request batch triage. The response must report `Idea validation skipped by owner opt-out` and residual risk in `Execution Trace`.

Opt-out must not bypass source-of-truth order, risk model, permissions, safe environment checks, required evidence, QA/Quality, owner approvals, phase gates, change-request routing, final owner approval, or any stop condition.

## Required Output

The response or routed artifact must include a triage matrix with exactly these fields:

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<raw item or stable label>` | `<group id or standalone>` | `<short theme>` | `<low/medium/high/critical/unknown>` | `<route>` | `<project/workspace/none>` | `<dependencies or none>` | `<decision needed or not-required>` | `<why this route>` |

Allowed routing values:

- `same-project-task-group`;
- `active-project-task`;
- `project-local-micro-task`;
- `repo-level-micro-project`;
- `new-project`;
- `change-request-candidate`;
- `full-workflow-required`;
- `owner-decision-required`;
- `stop`.

After the matrix, include:

- grouped requests;
- standalone requests;
- blockers and required owner decisions;
- recommended next route;
- explicit statement that triage does not grant implementation or artifact-write permission.

## Grouping Rules

Group items only when all of these are true:

- they share the same user-facing or workflow goal;
- they have a similar write-set and risk profile;
- they target the same project, repo workspace, or workflow namespace;
- they have compatible dependencies and ordering;
- they can share acceptance criteria without hiding material differences.

Do not group items just because they arrived in one message.

## Split Rules

Split items into separate routes when any of these differ:

- risk class;
- target project or target workspace;
- product feature versus workflow maintenance;
- active project task versus repo-level workflow change;
- pre-final or post-final change request timing;
- scope-changing effect;
- security, auth, billing, permissions, migration, infrastructure, production, secret, or destructive impact;
- acceptance criteria, safe environment, or evidence requirements;
- dependency order or blocking decision.

If a list contains one item for an active project and another repo-level item, the result must split them into separate routes.

If an item looks like a pre-final or post-final owner comment, route it as `change-request-candidate` through `.systems/ai/core/change-requests.md`.

High-risk and critical-risk items must route to `owner-decision-required` or `full-workflow-required`. They must not be silently classified as side tasks, micro-tasks, or micro-projects.

## Valid Mixed Batch Example

For a batch containing:

- three similar workflow improvements to validators and docs;
- one unrelated new feature idea;
- one post-final correction for an already closed project;

the expected split is:

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| workflow improvement A | workflow-improvements | workflow maintenance | low | repo-level-micro-project | `AI_WORKFLOW_HOME` | none | approve micro-project | Same workflow target and similar validator/doc write-set. |
| workflow improvement B | workflow-improvements | workflow maintenance | low | repo-level-micro-project | `AI_WORKFLOW_HOME` | none | approve micro-project | Same workflow target and similar validator/doc write-set. |
| workflow improvement C | workflow-improvements | workflow maintenance | low | repo-level-micro-project | `AI_WORKFLOW_HOME` | none | approve micro-project | Same workflow target and similar validator/doc write-set. |
| new feature idea | standalone-new-feature | product feature | unknown | new-project | unresolved | none | idea validation decision | Needs project workspace and formal idea validation. |
| post-final correction | standalone-change-request | final correction | medium | change-request-candidate | active project | final state and acceptance history | approve or reject change request | Changes scope after final owner approval. |

## Authority Boundary

Request batch triage is advisory and classificatory only.

It may recommend project creation, micro-project creation, micro-task creation, task creation, change request capture, or STOP. It must not perform those actions unless the owner separately approves the recommended route and the normal workflow gates allow the write.

It must not weaken source-of-truth order, risk classification, permissions, Definition of Done, evidence, QA, final owner approval, memory rules, or prompt-injection boundaries.

## Relationship To Task Intake

Batch triage runs before Task Idea Validation when the raw input has multiple items. After triage, each selected route still uses the normal validation route unless the owner explicitly uses a safe idea-validation opt-out:

- new project or broad product idea -> `phase-0-project-workspace` and `phase-0-idea-validation`;
- active project work -> project status, plan, task index, spec, and phase routing;
- low-risk local work -> side-task, micro-task, or micro-project contract;
- scope correction before or after `final-owner-yes` -> change request routing;
- high/critical risk -> owner decision and full workflow route;
- unclear or unsafe request -> STOP.

## Response Pattern

Use this compact pattern:

```text
Request Batch Triage

Triage matrix:
| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

Grouped requests:
- ...

Standalone requests:
- ...

Blockers / owner decisions:
- ...

Recommended next route:
- ...

Authority boundary:
- This triage does not grant write permission and does not start implementation, commits, project creation, task creation, or change request creation.
```
