# Repo Memory Router

## Purpose

`workspace/repo/core/memory.md` is the router and index for target-repository memory.

Detailed repo-local entries live in `workspace/repo/memory/`.

Use this router only for date, topic, type, status, and route to the detailed memory entry. Do not store long memory content in this file.

It is not a source of truth. Repository state, `AGENTS.md`, approved artifacts, `workspace/repo/core/status.md`, and project artifacts remain authoritative.

## Memory Index

| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| n/a | No repository-specific memory entries yet | n/a | n/a | n/a |

Populate this index only through checkpoint/final-check updates after the workflow has produced evidence-backed repo-level knowledge.

Universal workflow/process lessons belong in `workspace/external-memory/memory/` and are indexed by `workspace/external-memory/external-memory.md`.
Template maintenance memory belongs in `.systems/ai/memory/` and is indexed by `.systems/ai/core/memory.md`.

## Rules

- Keep this file short. It is an index, not the memory body.
- Store detailed repo-local facts in `workspace/repo/memory/`.
- Do not store secrets, credentials, private client data, or production-only operational details here.
- Do not treat this file as a substitute for reading the repository.
- Do not copy project-specific memory from another repository into this file.
- Use project-local memory in `workspace/projects/<project>/memory/` for active project knowledge before syncing stable findings here.
