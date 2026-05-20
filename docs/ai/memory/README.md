# memory

## Purpose

`docs/ai/memory/` stores detailed memory entries for maintaining this `ai-workflow` template repository.

The router/index is `docs/ai/core/memory.md`.

## Entry Naming

Create one file per memory entry:

```text
YYYY-MM-DD-short-kebab-title.md
```

Use `docs/ai/templates/memory/date-memory-entry.template.md` for new entries.

## What Belongs Here

- template maintenance decisions;
- layout changes for the workflow template;
- validator and CI maintenance notes;
- migration notes for template-owned files;
- reasons behind template-specific refactors.

## What Does Not Belong Here

- target-repository facts;
- project-specific facts;
- universal workflow recommendations that should travel between repositories;
- secrets, credentials, client data, or production-only operational details.

Universal workflow recommendations belong in `docs/ai/external-memory/` and are indexed by `docs/ai/core/external-memory.md`.

Repo-local facts belong in `docs/repo/memory/` and are indexed by `docs/repo/core/memory.md`.

## Router Rule

After adding or updating an entry, update `docs/ai/core/memory.md` with only:

- date;
- topic;
- type;
- status;
- route.
