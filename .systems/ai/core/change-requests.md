# change-requests.md

## Purpose

Change requests formalize owner comments, corrections, additions, removals, and decision changes before or after `final-owner-yes`.

This is not a workflow phase. It is a routing and artifact policy. Product-code writes happen only after the change request is routed into a valid phase, fix loop, micro-task, project iteration, decision rollback, or new project.

## When To Use

Use a change request when:

- final check is technically green, but the owner does not give `final-owner-yes`;
- the owner asks for changes while the project is in `awaiting-owner-final-yes`;
- the owner asks for a correction, addition, removal, or decision rollback after `final-owner-yes`;
- a post-final request needs classification before deciding whether it is a micro-task, new task, new iteration, rollback, or new project.

Do not use change requests to bypass normal phase gates, risk policy, permissions, Definition of Done, evidence, quality, checkpoint, or final owner approval.

## Artifact Locations

Project-local change requests are stored in:

- router: `workspace/projects/<project>/change-requests.md`;
- directory: `workspace/projects/<project>/change-requests/`;
- entry: `workspace/projects/<project>/change-requests/YYYY-MM-DD-<project>-cr-<nnn>-<slug>.md`.

The canonical ID inside an entry is:

```text
<PROJECT>-CR-<NNN>-<slug>
```

## Required Fields

Every change request entry must include:

- change request ID;
- project;
- timing: `pre-final-approval` or `post-final-approval`;
- type: `defect`, `acceptance-gap`, `scope-add`, `scope-remove`, `decision-rollback`, `docs-only`, or `follow-up-enhancement`;
- status: `proposed`, `triaged`, `approved`, `rejected`, `routed`, `in-progress`, `done`, or `superseded`;
- risk: `low`, `medium`, `high`, or `critical`;
- owner request;
- affected artifacts and files, if known;
- triage result;
- routing decision;
- evidence required before the request can be marked done;
- final check impact;
- post-final impact when applicable.

## Routing Values

Use exactly one primary routing value:

- `micro-task`;
- `phase-fix-loop`;
- `new-task-in-active-plan`;
- `new-project-iteration`;
- `decision-rollback`;
- `new-project`;
- `owner-decision-required`.

If the route is not clear, use `owner-decision-required` and stop.

## Pre-final Approval Rules

Before `final-owner-yes`, owner comments are blocking until triaged.

Rules:

- create or update a change request for every material owner comment;
- keep the project open;
- do not accept `final-owner-yes` while any blocking change request is `proposed`, `triaged`, `approved`, `routed`, or `in-progress`;
- route defects and acceptance gaps to the narrowest valid fix loop;
- route scope additions and removals through plan/spec updates before implementation;
- route decision rollback through `.systems/ai/core/command-routing.md` and existing decision rollback policy;
- rerun required quality, checkpoint, and final check after the routed work is done.

Pre-final change requests may be rejected only by explicit owner decision or by evidence that the requested change is already satisfied.

## Post-final Approval Rules

After `final-owner-yes`, the closed scope is immutable history.

Rules:

- do not edit old final approval, final check, or historical decisions to pretend the new request was part of the closed scope;
- create a new change request linked to the closed final check;
- low-risk, local, small work may route to a project-local micro-task;
- medium, high, critical, scope-changing, architectural, data, security, billing, permission, migration, production, or external-effect work must re-enter the full workflow as a new task, new iteration, decision rollback, or new project;
- removals and superseded artifacts must follow `.systems/ai/core/deprecation.md`;
- production-impacting recovery or reversal must follow `.systems/ai/core/rollback.md`.

## Triage Rules

Triage is read-only except for writing change-request artifacts and status.

During triage:

- classify timing, type, risk, scope, and route;
- identify required owner decisions;
- identify which artifacts become stale;
- identify the first valid workflow phase or micro-task route;
- record why a simpler route is not allowed when risk or scope requires the full workflow.

Do not modify product code, specs, architecture, plan, task index, or quality evidence during triage unless the current routed phase explicitly permits it.

## PASS And Closure Rules

A change request can be marked `done` only when:

- routed work is complete;
- required checks/evidence exist;
- affected status, task index, decisions, memory, and final-check artifacts are updated when required;
- skipped checks have explicit reason and impact;
- high-risk or critical-risk approval exists when required.

For pre-final requests, the project must rerun the required quality/checkpoint/final-check path before `final-owner-yes`.

For post-final requests, the change request can close independently only when it is routed as a valid micro-task. Otherwise closure depends on the new workflow route it created.
