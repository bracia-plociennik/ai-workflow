# AI System Accepted Context

## Product Goal

Create a local Mac AI workspace system for managing clients, projects, tasks, documents, materials, memory, and improvement insights.

The system is built as a dedicated project in the current `ai-workflow` repository first. The final reusable variant may later move to a dedicated `ai-system` branch after project final approval.

## Accepted Owner Decisions

- System root on the Mac: `~/ai-system/`.
- Local runtime workspace: `~/ai-system/ai-system-workspace/`.
- Git branch for the final reusable variant: `ai-system`, created only after the project is complete.
- No separate dev branch for this variant.
- `core/` is used inside the workspace instead of `repo/`.
- `external-memory/` is for improving `ai-system`.
- `system-insights/` is for improving owner competence, offer, process, and client work quality.
- Client memory may be raw.
- `system-insights` receives processed and anonymized lessons through a dedicated prompt supplied by the owner later.
- AI should periodically remind the owner to perform distillation.
- Client data, secrets, names, domains, contract details, and identifiable project facts must be anonymized before entering `system-insights`.
- Files in `dump/` are classified first. Moving, copying, deleting, or renaming requires `owner-approved`.

## System Boundary

System-owned files live under `.systems/`, `AGENTS.md`, `HUMANS.md`, `README.md`, `.github/`, and supporting template/docs files.

Workspace-owned private data lives under `ai-system-workspace/` and is not committed.

## Out Of Scope For The First Implementation Package

- Real API integration with Mail, Notion, Google Drive, Notes, or similar tools.
- Automatic account sync.
- Real customer data processing in tests.
- Destructive file operations without approval.
- Creating the final `ai-system` branch before final project closure.

## Soft Integration Model

External tools are represented by links, exported notes, copied references, or owner-provided context.

AI may classify and summarize these references, but it must not call external APIs or write to external systems in this implementation package.

