# changelog.md

## 0.7.0 - 2026-05-19

- Changed the target-repository installation model to a nested clone at `ai-workflow/`.
- Added `root-agents.template.md` as the only root file that target repositories need to copy or merge.
- Clarified `TARGET_REPO_ROOT` and `AI_WORKFLOW_HOME` path resolution across the root shim, internal `AGENTS.md`, installation policy, guide, command routing, repo intake, and workflow router.
- Updated repo intake to treat `ai-workflow/docs/ai-workflow/repo/` as runtime that must be replaced with target-repository facts after installation.
- Kept target-owned `docs/`, `scripts/`, `.github/`, `README.md`, `HUMANS.md`, and existing `AGENTS.md` out of the default install path.

## 0.6.0 - 2026-05-19

- Converted repo context into `context.md` router plus detailed entries under `docs/ai-workflow/repo/context/`.
- Clarified `plans.md` as a router to canonical `planning/` artifacts.
- Converted `tasks.md` into a task index/router with optional task cards under `tasks/`.
- Added project `reviews/` for review artifacts while keeping `quality/` as QA evidence.
- Converted autopilot runtime to run directories under `autopilot/runs/autopilot-XXX/`.

## 0.5.0 - 2026-05-18

- Moved workflow-owned docs under `docs/ai-workflow/`.
- Moved workflow validators under `scripts/ai-workflow/`.
- Added installation collision policy for existing target repositories.
- Clarified that target-owned `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, `docs/`, `scripts/`, and `.github/` must not be overwritten.
- Added `docs/ai-workflow/ai/skills/` as the reserved space for reusable task-specific workflow skills.
- Added `docs/ai-workflow/ai/command-routing.md` as the bilingual catalog for user-facing workflow commands and safe command interpretation.
- Added `docs/ai-workflow/ai/guide.md` for lost-user, next-step, fresh-start, and recovery guidance.
- Added `phase-0-project-workspace` for creating project and human workspaces after repo intake.
- Added `docs/ai-workflow/repo/legacy/` for preserving pre-existing repository workflow material as context-only legacy input during repo intake.
- Moved project context into the dedicated `context/context.md` project context directory.
- Added human-facing `plans.template.md`.
- Renamed repo runtime context template to `context.template.md` to match `docs/ai-workflow/repo/context.md`.
- Clarified that the literal `repo intake` prompt is sufficient for repo-level bootstrap when AI Workflow is installed.

## 0.4.0 - 2026-05-18

- Converted workflow filenames to lowercase kebab-case.
- Added policy docs for operating model, Definition of Done, permissions, risk, commands, prompt injection, rollback, dependencies, and deprecation.
- Converted `AGENTS.md` into a short execution router.
- Added automatic workflow validation scripts and GitHub Actions workflow.
- Added Codex configuration templates.
- Added canonical task ID model and project task index.

## 0.3.0 - 2026-05-18

- Moved repo-specific runtime facts to `docs/ai-workflow/repo/`.
- Added idea validation phase.
- Renamed legacy singular human docs path to `docs/ai-workflow/humans`.
- Made Codex the primary executor with ChatGPT as optional support.
