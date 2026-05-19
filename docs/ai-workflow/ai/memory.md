# AI Workflow Template Memory Router

## Purpose

`docs/ai-workflow/ai/memory.md` is the router and index for template memory.

Detailed entries live in `docs/ai-workflow/ai/memory/`.

Use this router only for date, topic, type, status, and route to the detailed memory entry. Do not store long memory content in this file.

## Relationship To Other Memory Files

| Artifact | Scope | Use For |
| --- | --- | --- |
| `docs/ai-workflow/ai/memory.md` | this workflow template | router/index for template maintenance memory |
| `docs/ai-workflow/ai/memory/` | this workflow template | detailed template maintenance memory entries |
| `docs/ai-workflow/ai/external-memory.md` | universal workflow/process memory | router/index for reusable lessons to promote into future versions |
| `docs/ai-workflow/ai/external-memory/` | universal workflow/process memory | detailed reusable lesson entries |
| `docs/ai-workflow/repo/memory.md` | target repository | router/index for repo-local memory |
| `docs/ai-workflow/repo/memory/` | target repository | detailed repo-local memory entries |
| `docs/ai-workflow/projects/<project>/memory.md` | one project workspace | router/index for project-specific memory |
| `docs/ai-workflow/projects/<project>/memory/` | one project workspace | detailed project-specific memory entries |

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| 2026-05-19 | Memory router and directory model | template-change | active | `docs/ai-workflow/ai/memory/2026-05-19-memory-router-and-directory-model.md` |

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed template maintenance facts in `docs/ai-workflow/ai/memory/`.
- Do not store target-repo facts here.
- Do not store project-specific task implementation details here.
- Do not store secrets, credentials, customer data, or production-only operational details.
- Promote reusable workflow lessons to `docs/ai-workflow/ai/external-memory/` and index them in `docs/ai-workflow/ai/external-memory.md` when they should affect future template versions.
