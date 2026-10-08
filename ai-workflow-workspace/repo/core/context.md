# Repo Context Router

## Purpose

`ai-workflow-workspace/repo/core/context.md` is the router and index for global repository context.

Detailed repo context lives in `ai-workflow-workspace/repo/context/`.

Use this router only for date, topic, type, status, and route to detailed context entries. Do not store the full repository context body in this file.

## Context Index

| Topic | Type | Status | Route |
| --- | --- | --- | --- |
| Repository overview | overview | current | `ai-workflow-workspace/repo/context/overview.md` |
| Stack and runtime | stack | current | `ai-workflow-workspace/repo/context/stack.md` |
| Main repository areas | areas | current | `ai-workflow-workspace/repo/context/areas.md` |
| Boundaries | boundaries | current | `ai-workflow-workspace/repo/context/boundaries.md` |
| Local operating rules | local-rules | current | `ai-workflow-workspace/repo/context/local-rules.md` |

## Rules

- Keep this file short. It is an index, not the context body.
- Store detailed repo-wide context in `ai-workflow-workspace/repo/context/`.
- Files in `ai-workflow-workspace/repo/context/` are supporting context and are exempt from `.systems/scripts/check-naming`; this router remains the canonical `ai-workflow-workspace/repo/core/context.md`.
- Commands, safe environments, high-risk areas, and restricted zones belong in `ai-workflow-workspace/repo/core/repo-intake.md`.
- Repo memory entries belong in `ai-workflow-workspace/repo/memory/` and are indexed by `ai-workflow-workspace/repo/core/memory.md`.
- Project-specific context belongs in `ai-workflow-workspace/projects/<project>/context/`.
