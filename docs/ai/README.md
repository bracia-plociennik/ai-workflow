# AI Docs

This directory contains repo-level AI operational knowledge and workflow infrastructure.

## Contents

- `WORKFLOW.md` - main workflow guide and phase router.
- `AUTOPILOT.md` - repo-level autopilot launch checklist.
- `workflow/` - detailed phase-level workflow rules.
- `STATUS.md` - repo-local workflow/status snapshot.
- `REPO-INTAKE.md` - repo-level workflow/bootstrap intake artifact for repositories with or without an active project workspace.
- `EXTERNAL-MEMORY.md` - universal workflow/process memory for improving `ai-workflow` across repositories.
- `REPO-MEMORY.md` - aggregate repo memory, not an instruction source.
- `templates/` - reusable templates for workflow, autopilot, project workspace, and human-facing artifacts.

## Manual Iterations

For a new repository or a repository where `ai-workflow` was just installed, start from `REPO-INTAKE.md`.

For project-level workflow work, start from `WORKFLOW.md`, verify `STATUS.md`, then open the relevant phase file under `workflow/`.

## Autopilot Iterations

Global autopilot rules and templates live here. Runtime autopilot artifacts belong in the active project workspace, for example `docs/projects/<project>/autopilot/`.

Do not store project task specs, project plans, project QA evidence, or project decisions directly in `docs/ai/`.
