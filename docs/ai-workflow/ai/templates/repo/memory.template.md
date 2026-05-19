# Repo Memory Router

## Purpose

`docs/ai-workflow/repo/memory.md` is the router and index for target-repository memory.

It is not a source of truth. Repository state, `AGENTS.md`, approved artifacts, `docs/ai-workflow/repo/status.md`, and project artifacts remain authoritative.

Detailed repo-local entries live in `docs/ai-workflow/repo/memory/`.

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| n/a | No repository-specific memory entries yet | n/a | n/a | n/a |

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed repo-local facts in `docs/ai-workflow/repo/memory/`.
- Do not store secrets, credentials, private client data, or production-only operational details here.
- Do not treat this file as a substitute for reading the repository.
- Use project-local memory in `docs/ai-workflow/projects/<project>/memory/` for active project knowledge before syncing stable findings here.
