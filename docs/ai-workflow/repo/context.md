# Repo Context Router

## Purpose

`docs/ai-workflow/repo/context.md` is the router and index for global repository context.

Detailed repo context lives in `docs/ai-workflow/repo/context/`.

Use this router only for date, topic, type, status, and route to detailed context entries. Do not store the full repository context body in this file.

## Context Index

| Topic | Type | Status | Route |
| --- | --- | --- | --- |
| Repository overview | overview | current | `docs/ai-workflow/repo/context/overview.md` |
| Stack and runtime | stack | current | `docs/ai-workflow/repo/context/stack.md` |
| Main repository areas | areas | current | `docs/ai-workflow/repo/context/areas.md` |
| Boundaries | boundaries | current | `docs/ai-workflow/repo/context/boundaries.md` |
| Local operating rules | local-rules | current | `docs/ai-workflow/repo/context/local-rules.md` |

## Rules

- Keep this file short. It is an index, not the context body.
- Store detailed repo-wide context in `docs/ai-workflow/repo/context/`.
- Commands, safe environments, high-risk areas, and restricted zones belong in `docs/ai-workflow/repo/repo-intake.md`.
- Repo memory entries belong in `docs/ai-workflow/repo/memory/` and are indexed by `docs/ai-workflow/repo/memory.md`.
- Project-specific context belongs in `docs/ai-workflow/projects/<project>/context/`.
