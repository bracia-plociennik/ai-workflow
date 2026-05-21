# memory

## Purpose

`.systems/ai/memory/` stores detailed memory entries for maintaining this `ai-workflow` template repository.

The router/index is `.systems/ai/core/memory.md`.

## Entry Naming

Create one file per memory entry:

```text
YYYY-MM-DD-short-kebab-title.md
```

Use `.systems/ai/templates/memory/date-memory-entry.template.md` for new entries.

## What Belongs Here

- template maintenance decisions;
- layout changes for the workflow template;
- validator and CI maintenance notes;
- migration notes for system-owned files;
- reasons behind template-specific refactors.

## What Does Not Belong Here

- target-repository facts;
- project-specific facts;
- universal workflow recommendations that should travel between repositories;
- secrets, credentials, client data, or production-only operational details.

Universal workflow recommendations belong in `workspace/external-memory/memory/` and are indexed by `workspace/external-memory/external-memory.md`.

Repo-local facts belong in `workspace/repo/memory/` and are indexed by `workspace/repo/core/memory.md`.

## Router Rule

After adding or updating an entry, update `.systems/ai/core/memory.md` with only:

- date;
- topic;
- type;
- status;
- route.
