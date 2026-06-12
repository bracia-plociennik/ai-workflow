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
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md` | target repository | router/index for repo-local memory |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/` | target repository | detailed repo-local memory entries |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory.md` | one project workspace | router/index for project-specific memory |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory/` | one project workspace | detailed project-specific memory entries |

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
- Promote reusable workflow-system improvement proposals to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` and index them in `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` when they should affect future template versions.
- Promote anonymized operating lessons from projects to `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/` and index them in `AI_WORKFLOW_WORKSPACE_HOME/system-insights/system-insights.md` only through checkpoint/final-check routing or explicit owner-approved capture.
