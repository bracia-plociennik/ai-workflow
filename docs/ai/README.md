# AI Docs

This directory contains template-owned AI operational knowledge and workflow infrastructure.

Do not store target-repository-specific facts in `docs/ai/`. Runtime repo context, intake, status, and aggregate memory belong in `docs/repo/`.

## Contents

- `WORKFLOW.md` - main workflow guide and phase router.
- `AUTOPILOT.md` - repo-level autopilot launch checklist.
- `workflow/` - detailed phase-level workflow rules.
- `STATUS.md` - template-owned pointer to `docs/repo/STATUS.md`.
- `REPO-INTAKE.md` - template-owned guidance for repo-level intake.
- `MEMORY.md` - aggregate memory for this workflow template, not target-repo facts.
- `EXTERNAL-MEMORY.md` - universal workflow/process memory for improving `ai-workflow` across repositories.
- `templates/` - reusable templates for AI runtime, workflow, autopilot, project workspace, and human-facing artifacts.

## Manual Iterations

For a new repository or a repository where `ai-workflow` was just installed, start from `docs/repo/CONTEXT.md` and `docs/repo/REPO-INTAKE.md`, using `templates/ai/` if the runtime files are missing.

For project-level workflow work, start from `WORKFLOW.md`, verify `docs/repo/STATUS.md`, then open the relevant phase file under `workflow/`.

## Autopilot Iterations

Global autopilot rules and templates live here. Runtime autopilot artifacts belong in the active project workspace, for example `docs/projects/<project>/autopilot/`.

Do not store project task specs, project plans, project QA evidence, project decisions, or target-repo runtime facts directly in `docs/ai/`.
