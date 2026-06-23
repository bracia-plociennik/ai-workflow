# AI Workflow Template Memory Router

## Purpose

`.systems/ai/core/memory.md` is the router and index for template memory.

Detailed entries live in `.systems/ai/memory/`.

Use this router only for date, topic, type, status, and route to the detailed memory entry. Do not store long memory content in this file.

## Relationship To Other Memory Files

| Artifact | Scope | Use For |
| --- | --- | --- |
| `.systems/ai/core/memory.md` | this workflow template | router/index for template maintenance memory |
| `.systems/ai/memory/` | this workflow template | detailed template maintenance memory entries |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` | AI Workflow improvement memory | router/index for proposed workflow, gate, template, validator, autopilot, recovery, or system-skill improvements |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` | AI Workflow improvement memory | detailed workflow improvement proposals |
| `AI_WORKFLOW_WORKSPACE_HOME/system-insights/system-insights.md` | anonymized cross-project operating lessons | router/index for reusable frontend, backend, smart-contract, SEO, ads, offer, process, quality, client-work, product, and skills insights |
| `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/` | anonymized cross-project operating lessons | detailed System Insight entries |
| `AI_WORKFLOW_WORKSPACE_HOME/dreams/runs/` | advisory Dreaming Mode reports | source-backed recommendation queues for owner decisions |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md` | target repository | router/index for repo-local memory |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/` | target repository | detailed repo-local memory entries |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory.md` | one project workspace | router/index for project-specific memory |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory/` | one project workspace | detailed project-specific memory entries |

## Optional Phase Knowledge Capture

Every workflow phase artifact includes an `Optional Knowledge Capture` decision. This is a soft capture gate, not a durable write gate.

Use it to decide whether the phase produced reusable knowledge, where that knowledge belongs, and whether the owner must approve capture now or defer it to phase 6 distillation or phase 7 checkpoint.

Allowed targets are:

- `project-memory` - project decisions, constraints, risks, implementation notes, testing notes, or watch items useful for later project work.
- `repo-memory` - repo-wide facts, commands, constraints, integrations, risks, and reusable repo rules.
- `external-memory` - AI Workflow improvement proposals only.
- `system-insights` - anonymized cross-project operating lessons and skill candidates only.
- `decision-artifact` - decisions that affect scope, risk, architecture, permissions, acceptance criteria, or approvals.
- `status` - status or task state synchronization only.
- `none` - no useful durable knowledge was produced.

`Capture recommended: <no>` and `Target: <none>` are valid outcomes.

The phase capture decision may propose memory or insight content inside the phase artifact. It must not create durable memory entries unless the current phase's `Writes allowed` permits that target and the required owner approval is present.

## End-of-Task Capture

`.systems/ai/core/end-of-task-capture.md` handles chat-end prompts such as `to koniec zadania`, `dziękuję, utrwal wiedzę`, and `end task and capture knowledge`.

It uses the same memory scope boundaries as this router:

- project memory for one-project facts;
- repo memory for repo-wide facts;
- External Memory only for AI Workflow improvement proposals;
- System Insights only for anonymized cross-project operating lessons and skill candidates;
- status/evidence only for source-backed state synchronization.

Default End-of-Task Capture output is proposal-only. Durable memory writes require explicit owner capture intent plus clear target, scope, privacy, evidence, and write permission.

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| 2026-05-19 | Memory router and directory model | template-change | active | `.systems/ai/memory/2026-05-19-memory-router-and-directory-model.md` |

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed template maintenance facts in `.systems/ai/memory/`.
- Do not store target-repo facts here.
- Do not store project-specific task implementation details here.
- Do not store secrets, credentials, customer data, or production-only operational details.
- Treat `Optional Knowledge Capture` as a candidate/proposal mechanism unless a phase explicitly permits durable writes.
- Promote reusable workflow-system improvement proposals to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` and index them in `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` when they should affect future template versions.
- Promote anonymized operating lessons from projects to `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/` and index them in `AI_WORKFLOW_WORKSPACE_HOME/system-insights/system-insights.md` only through checkpoint/final-check routing or explicit owner-approved capture.
- Treat Dream Reports as advisory recommendation queues, not memory entries. Promotion from `AI_WORKFLOW_WORKSPACE_HOME/dreams/runs/**` to durable memory, External Memory, System Insights, skills, status, or source changes requires a later owner-approved route.
