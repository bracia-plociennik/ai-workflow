# contract-compliance.md

## Purpose

This policy defines the advisory work-mode compliance check and the commit readiness / knowledge capture gate.

It exists to make every commit decision explicit without creating a mechanical requirement to write memory, distillation, or checkpoint artifacts for every commit.

It is separate from the phase-level `Optional Knowledge Capture` block. Phase capture records whether a phase produced candidate knowledge; commit readiness records whether a commit or handoff still needs a durable synchronization step.

## Advisory Only

This gate is advisory-only. It does not replace phase gates, risk policy, permissions, Definition of Done, required evidence, stop conditions, or owner approvals.

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

The selected mode must match risk, scope, approvals, write set, and artifacts. If the mode does not fit, route to the safer workflow path before continuing.

## Compliance Questions

Answer these before commit or handoff:

- `Work mode compliance: pass|warning|blocked`
- `Work mode: <full-project|project-local-micro-task|repo-level-micro-project|side-task|workflow-maintenance>`
- `Scope/acceptance clear: yes|no`
- `Risk allowed for mode: yes|no`
- `Required artifacts current: yes|no|not-applicable`
- `Write-set conflicts: none|warning|blocked`
- `Evidence available: yes|no`
- `Knowledge capture: required|not-required`
- `Knowledge capture target: <status/evidence|micro-task-artifact|micro-project-artifact|phase-6-distillation|phase-7-checkpoint|project-memory|repo-memory|external-memory|system-insights|not-applicable>`
- `Reason: <short evidence-backed reason>`

If any answer is `blocked` or `no` for a required item, stop before commit unless the current phase explicitly allows recording the blocker.

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
