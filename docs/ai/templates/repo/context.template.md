# Repo Context Router

## Purpose

`docs/repo/core/context.md` is the router and index for global repository context.

Detailed repo context lives in `docs/repo/context/`.

Use this router only for topic, type, status, and route to detailed context entries. Do not store the full repository context body in this file.

## Context Index

| Topic | Type | Status | Route |
| --- | --- | --- | --- |
| Repository overview | overview | `<current|missing|incomplete>` | `docs/repo/context/overview.md` |
| Stack and runtime | stack | `<current|missing|incomplete>` | `docs/repo/context/stack.md` |
| Main repository areas | areas | `<current|missing|incomplete>` | `docs/repo/context/areas.md` |
| Boundaries | boundaries | `<current|missing|incomplete>` | `docs/repo/context/boundaries.md` |
| Local operating rules | local-rules | `<current|missing|incomplete>` | `docs/repo/context/local-rules.md` |

## Rules

- Keep this file short. It is an index, not the context body.
- Store detailed repo-wide context in `docs/repo/context/`.
- Files in `docs/repo/context/` are supporting context and are exempt from `scripts/check-naming`; this router remains the canonical `docs/repo/core/context.md`.
- Commands, safe environments, high-risk areas, and restricted zones belong in `docs/repo/core/repo-intake.md`.
- Repo memory entries belong in `docs/repo/memory/` and are indexed by `docs/repo/core/memory.md`.
- Project-specific context belongs in `docs/projects/<project>/context/`.
