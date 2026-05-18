# AI Docs

This directory contains template-owned AI operational knowledge and workflow infrastructure.

Do not store target-repository-specific facts in `docs/ai/`. Runtime repo context, intake, status, and aggregate memory belong in `docs/repo/`.

## Contents

- `operating-model.md` - primary operating contract behind the short `AGENTS.md` router.
- `workflow.md` - phase router and canonical phase index.
- `autopilot.md` - autopilot launch and runtime rules.
- `definition-of-done.md` - evidence-backed done criteria.
- `risk-model.md` - risk classes and approval routing.
- `commands.md` - verification command contract.
- `permissions.md` - forbidden actions and safe defaults.
- `prompt-injection.md` - defense rules for untrusted repository content.
- `rollback.md` - rollback requirements for high-risk work.
- `dependencies.md` - dependency approval and review policy.
- `deprecation.md` - archive and supersession policy.
- `version.md` and `changelog.md` - workflow version and migration history.
- `workflow/` - detailed phase-level workflow rules.
- `templates/` - reusable templates for repo runtime, workflow, autopilot, project, human, and Codex artifacts.

## Runtime Boundaries

- Repo-specific facts belong in `docs/repo/`.
- Project-specific facts belong in `docs/projects/<project>/`.
- Human-facing coordination docs belong in `docs/humans/<project>/`.
- Template/process docs belong in `docs/ai/`.

## Manual Iterations

For a new repository or a repository where `ai-workflow` was just installed, start from `docs/repo/context.md` and `docs/repo/repo-intake.md`, using `templates/ai/` if the runtime files are missing.

For project-level workflow work, start from `workflow.md`, verify `docs/repo/status.md`, then open the relevant phase file under `workflow/`.

## Autopilot Iterations

Global autopilot rules and templates live here. Runtime autopilot artifacts belong in the active project workspace, for example `docs/projects/<project>/autopilot/`.

Do not store project task specs, project plans, project QA evidence, project decisions, or target-repo runtime facts directly in `docs/ai/`.
