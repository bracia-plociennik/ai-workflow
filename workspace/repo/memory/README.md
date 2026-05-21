# memory

## Purpose

`workspace/repo/memory/` stores detailed memory entries for the current target repository.

The router/index is `workspace/repo/core/memory.md`.

## Entry Naming

Create one file per memory entry:

```text
YYYY-MM-DD-short-kebab-title.md
```

Use `.systems/ai/templates/repo/date-memory-entry.template.md` for new entries.

## What Belongs Here

- durable repo-level facts;
- local constraints that affect future tasks;
- repo-wide testing, build, deployment, or integration notes;
- repo-level risks found through checkpoint or final check;
- repo-level decisions that are not project-specific.

## What Does Not Belong Here

- template maintenance memory;
- universal workflow/process lessons;
- project-specific task details;
- secrets, credentials, private client data, or production-only operational details.

Template maintenance memory belongs in `.systems/ai/memory/`.

Universal workflow lessons belong in `workspace/external-memory/memory/` and are indexed by `workspace/external-memory/external-memory.md`.

Project-specific facts belong in `workspace/projects/<project>/memory/` and are indexed by `workspace/projects/<project>/memory.md`.

## Router Rule

After adding or updating an entry, update `workspace/repo/core/memory.md` with only:

- date;
- topic;
- type;
- status;
- route.
