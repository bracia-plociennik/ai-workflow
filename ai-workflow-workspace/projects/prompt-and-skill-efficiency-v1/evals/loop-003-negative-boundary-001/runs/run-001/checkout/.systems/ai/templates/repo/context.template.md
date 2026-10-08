# Repo Context Router

## Purpose

`AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md` is the router and index for global repository context.

Detailed repo context lives in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.

Use this router only for topic, type, status, and route to detailed context entries. Do not store the full repository context body in this file.

## Context Index

| Topic | Type | Status | Route |
| --- | --- | --- | --- |
| Repository overview | overview | `<current|missing|incomplete>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/context/overview.md` |
| Stack and runtime | stack | `<current|missing|incomplete>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/context/stack.md` |
| Main repository areas | areas | `<current|missing|incomplete>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/context/areas.md` |
| Boundaries | boundaries | `<current|missing|incomplete>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/context/boundaries.md` |
| Local operating rules | local-rules | `<current|missing|incomplete>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/context/local-rules.md` |

## Rules

- Keep this file short. It is an index, not the context body.
- Store detailed repo-wide context in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
- Files in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/` are supporting context and are exempt from `.systems/scripts/check-naming`; this router remains the canonical `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`.
- Commands, safe environments, high-risk areas, and restricted zones belong in `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`.
- Repo memory entries belong in `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/` and are indexed by `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md`.
- Project-specific context belongs in `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/`.
