# changelog.md

## 0.8.0 - 2026-05-21

- Split the nested clone into system-owned `.systems/**` and target-owned `workspace/**`.
- Made `update-from-upstream` block dirty system-owned files and preserve the full `workspace/**` tree.
- Moved External Memory to `workspace/external-memory/external-memory.md` with detailed entries in `workspace/external-memory/memory/`.
- Added `workspace/skills/` for user-defined local skills that take precedence over system skills as supporting guidance.
- Moved EXAMPLE workspaces to `.systems/ai/examples/` so active runtime stays under `workspace/`.

## 0.7.4 - 2026-05-21

- Added `.systems/ai/core/change-requests.md` as the formal owner change request policy before and after `final-owner-yes`.
- Added project-local change request router, directory templates, and EXAMPLE artifacts.
- Updated final check, command routing, guide, workflow routing, and project workspace setup to block final approval on open pre-final change requests and route post-final changes safely.

## 0.7.3 - 2026-05-20

- Added `.systems/ai/core/response-contract.md` as the canonical user-facing response contract.
- Required substantive Codex responses to end with `Co dalej?`, one recommendation with impact and copy-paste prompt, and one safe alternative with impact and copy-paste prompt.
- Connected the response contract to `AGENTS.md`, operating model, workflow routing, guide mode, command routing, and human documentation.

## 0.7.2 - 2026-05-20

- Flattened the old internal documentation namespace so the nested clone now uses `.systems/ai/`, `workspace/repo/`, `workspace/projects/`, `workspace/humans/`, and `workspace/micro-projects/` directly.
- Moved canonical AI router and policy files into `.systems/ai/core/` while keeping workflow phases, templates, skills, memory entries, and external-memory entries in their dedicated directories.
- Moved canonical repo runtime routers into `workspace/repo/core/` while keeping detailed repo context, legacy, and memory entries in `workspace/repo/context/`, `workspace/repo/legacy/`, and `workspace/repo/memory/`.
- Moved validators from the old nested validator subdirectory to `.systems/scripts/` for the nested-clone installation model.

## 0.7.1 - 2026-05-20

- Added project-local `micro-tasks.md` and `micro-tasks/` plus repo-level `workspace/micro-projects/` for low-risk work that does not need full workflow phases.
- Added the official `update-from-upstream` flow for safely updating target repository nested clones while preserving runtime, workspaces, local External Memory, and legacy source filenames.
- Excluded preserved legacy workflow inputs under `workspace/repo/legacy/` and detailed repo context entries under `workspace/repo/context/` from strict Markdown naming checks while keeping canonical repo context at `workspace/repo/core/context.md`.
- Added `workspace/repo/core/legacy.md` as the canonical router and summary for preserved legacy material under `workspace/repo/legacy/`.
- Simplified canonical accepted project context from the previous nested context-file model to `workspace/projects/<project>/context.md`.
- Excluded supporting project source materials under `workspace/projects/<project>/context/` from strict Markdown naming checks while keeping canonical project `context.md` required and status-validated before architecture and later phases.
- Added validator smoke coverage for legacy/context naming exemptions and missing canonical project context.

## 0.7.0 - 2026-05-19

- Changed the target-repository installation model to a nested clone at `ai-workflow/`.
- Added `.systems/ai/templates/root-agents.template.md` as the only file that target repositories need to copy or merge into root `AGENTS.md`.
- Clarified `TARGET_REPO_ROOT` and `AI_WORKFLOW_HOME` path resolution across the root shim, internal `AGENTS.md`, installation policy, guide, command routing, repo intake, and workflow router.
- Updated repo intake to treat `ai-workflow/workspace/repo/` as runtime that must be replaced with target-repository facts after installation.
- Kept target-owned `docs/`, `.systems/`, `.github/`, `README.md`, `HUMANS.md`, and existing `AGENTS.md` out of the default install path.

## 0.6.0 - 2026-05-19

- Converted repo context into `context.md` router plus detailed entries under `workspace/repo/context/`.
- Clarified `plans.md` as a router to canonical `planning/` artifacts.
- Converted `tasks.md` into a task index/router with optional task cards under `tasks/`.
- Added project `reviews/` for review artifacts while keeping `quality/` as QA evidence.
- Converted autopilot runtime to run directories under `autopilot/runs/autopilot-XXX/`.

## 0.5.0 - 2026-05-18

- Moved workflow-owned docs under `docs/`.
- Moved workflow validators under `.systems/scripts/`.
- Added installation collision policy for existing target repositories.
- Clarified that target-owned `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, `docs/`, `.systems/`, and `.github/` must not be overwritten.
- Added `.systems/ai/skills/` as the reserved space for reusable task-specific workflow skills.
- Added `.systems/ai/core/command-routing.md` as the bilingual catalog for user-facing workflow commands and safe command interpretation.
- Added `.systems/ai/core/guide.md` for lost-user, next-step, fresh-start, and recovery guidance.
- Added `phase-0-project-workspace` for creating project and human workspaces after repo intake.
- Added `workspace/repo/legacy/` for preserving pre-existing repository workflow material as context-only legacy input during repo intake.
- Moved project context into a dedicated project context area.
- Added human-facing `plans.template.md`.
- Renamed repo runtime context template to `context.template.md` to match `workspace/repo/core/context.md`.
- Clarified that the literal `repo intake` prompt is sufficient for repo-level bootstrap when AI Workflow is installed.

## 0.4.0 - 2026-05-18

- Converted workflow filenames to lowercase kebab-case.
- Added policy docs for operating model, Definition of Done, permissions, risk, commands, prompt injection, rollback, dependencies, and deprecation.
- Converted `AGENTS.md` into a short execution router.
- Added automatic workflow validation scripts and GitHub Actions workflow.
- Added Codex configuration templates.
- Added canonical task ID model and project task index.

## 0.3.0 - 2026-05-18

- Moved repo-specific runtime facts to `workspace/repo/`.
- Added idea validation phase.
- Renamed legacy singular human docs path to `workspace/humans`.
- Made Codex the primary executor with ChatGPT as optional support.
