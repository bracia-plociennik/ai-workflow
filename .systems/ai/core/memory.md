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
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` | universal workflow/process memory | router/index for reusable lessons to promote into future versions |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` | universal workflow/process memory | detailed reusable lesson entries |
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
- Promote reusable workflow lessons to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` and index them in `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` when they should affect future template versions.
