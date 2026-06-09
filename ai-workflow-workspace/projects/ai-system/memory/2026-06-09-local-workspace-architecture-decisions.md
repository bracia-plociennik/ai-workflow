# Local Workspace Architecture Decisions

## Date

2026-06-09

## Summary

The owner accepted a local Mac workspace model named `ai-system`, with private runtime under `~/ai-system/ai-system-workspace/`.

## Durable Decisions

- Use `core/` inside the workspace instead of `repo/`.
- Keep `external-memory/` for development of `ai-system`.
- Keep `system-insights/` for owner competence, offer, process, and work-quality lessons.
- Classify `dump/` files first and require owner approval before moving files.
- Keep real integrations soft through links and manual context in the first implementation package.

