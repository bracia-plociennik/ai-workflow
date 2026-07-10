# knowledge-capture-reminder.md

## Purpose

`Knowledge Capture Reminder` is a soft reminder used after implementation, fixes, quality closure, handoff, commit readiness, or before switching to a new unrelated task when previous work may have unresolved capture value.

It exists to prevent useful decisions, lessons, status changes, and reusable evidence from being lost. It does not automatically write memory, distillation, checkpoints, External Memory, System Insights, status, commits, or pull requests.

The reminder is advisory unless an existing gate already requires capture, such as `phase-6-distillation`, `phase-7-checkpoint`, status/evidence synchronization, or commit readiness from `.systems/ai/core/contract-compliance.md`.

## Triggers

Use Knowledge Capture Reminder when any of these are true:

- implementation work completed;
- fix work completed;
- quality closure completed;
- handoff is being prepared;
- commit readiness is being checked;
- the owner starts a new unrelated task while the previous work has an unresolved capture decision;
- a phase or artifact says `defer-to-distillation`, `defer-to-checkpoint`, `capture-now`, or `capture recommended: yes`;
- a completed side task, micro-task, micro-project, or workflow-maintenance change produced decisions, reusable lessons, status changes, or evidence worth preserving.

If the previous work scope is unclear or there is no source evidence, report `Capture state: unknown` instead of guessing.

## Required Output

Use this output block when the reminder is relevant:

```text
Knowledge Capture Reminder

- Trigger:
- Previous work scope:
- Capture state:
- Recommended target:
- Required vs optional:
- Writes allowed:
- Commit needed:
- Push allowed:
- Owner skip:
- Residual risk:
```

## Routing

When capture is required by existing workflow gates, route to the required mechanism instead of writing memory ad hoc:

- `phase-6-distillation` when Quality PASS exists and distillation is required;
- `phase-7-checkpoint` when checkpoint cadence or final in-scope task completion requires it;
- `status/evidence` synchronization when source-backed state changed;
- commit readiness when tracked capture artifacts were written and a local commit is in scope.

When capture is useful but not required, show the reminder as a proposal and allow the owner to continue, defer, or skip it.

When capture target, source scope, privacy, evidence, or write permission is unclear, recommend `proposal-only` or ask for the missing decision.

## Owner Skip

The owner can explicitly skip optional capture with:

- `pomijam capture`
- `bez utrwalania wiedzy`
- `skip knowledge capture`
- `no capture`
- `owner-approved skip capture`

Owner skip must report residual risk. It does not bypass phase 6, phase 7, QA/Quality, required evidence, privacy checks, status synchronization, risk policy, permissions, phase gates, stop conditions, or final owner approval.

## Commit And Push Policy

Durable capture that writes tracked source or tracked workflow artifacts must go through commit readiness before a local commit.

Durable capture that writes only ignored or local-only workspace artifacts, such as `ai-workflow-workspace/**`, does not create a git commit by default. Report `Commit needed: no, workspace ignored`.

If capture requires distillation or checkpoint, recommend that formal phase route instead of writing memory directly.

Push is disabled by default. Report `Push allowed: no, owner request required` unless the owner explicitly asks to push.

## Memory Boundaries

Knowledge Capture Reminder uses the existing memory scope boundaries:

- project memory for one-project facts needed later in that project;
- repo memory for repo-wide facts, commands, constraints, integrations, risks, or reusable repo rules;
- External Memory only for AI Workflow improvement proposals;
- System Insights only for anonymized cross-project operating lessons and skill candidates;
- status/evidence only for source-backed state synchronization;
- `proposal-only` when durable writes are not approved or not safe;
- `none` when no useful capture exists.

The reminder may propose System Insight or External Memory candidates, but durable writes still require the privacy, scope, owner approval, and write gates from `.systems/ai/core/system-insights.md`, `.systems/ai/core/memory.md`, and `.systems/ai/core/contract-compliance.md`.

## Safety Boundaries

Knowledge Capture Reminder must not:

- automatically write memory, External Memory, System Insights, distillation, checkpoint, status, commits, pull requests, or push;
- make optional capture a hard gate when no existing workflow gate requires it;
- bypass `phase-6-distillation`, `phase-7-checkpoint`, QA/Quality, evidence, privacy, status synchronization, risk, permissions, phase gates, stop conditions, or owner approvals;
- commit ignored or local-only workspace artifacts by default;
- store frontend, backend, SEO, ads, smart-contract, product, or client-work lessons in External Memory;
- store raw client data, client names, secrets, credentials, production identifiers, repo-specific facts, or project-specific details in System Insights.

## Relationship To End-of-Task Capture

End-of-Task Capture is owner-triggered by completion/capture wording such as `to koniec zadania` or `utrwal wiedzę`.

Knowledge Capture Reminder is proactive and can appear without owner capture wording after implementation, fixes, quality closure, handoff, commit readiness, or before unrelated new work. It remains proposal-oriented unless existing gates require capture.

If the owner gives a direct End-of-Task Capture command, use `.systems/ai/core/end-of-task-capture.md` first and include Knowledge Capture Reminder only as supporting context when useful.
