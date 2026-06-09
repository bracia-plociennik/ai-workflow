# changelog.md

## 0.8.5 - 2026-06-09

- Added formal Autopilot Range Model with `planning-range` for phase 1 through phase 3 Spec QA and `implementation-range` for phase 4 through phase 7 checkpoint.
- Made `phase-8-final-check` owner-triggered only and removed it from automatic autopilot execution.
- Extended readiness, state, ledger, events, run README, command routing, guide, workflow routing, and human docs with range-aware start and stop conditions.
- Made checkpoint cadence a hard gate for implementation-range autopilot after every 3 completed tasks/packages and after the final task/package.

## 0.8.4 - 2026-06-08

- Added `phase-0-init` as the first bootstrap phase after cloning AI Workflow into a target repository.
- Extended `.systems/scripts/init-workspace` to create `repo/core/init.md`, preserve safe legacy context, and write `repo/legacy/legacy-index.md`.
- Updated install, guide, command routing, repo intake, workflow routing, templates, and validators so fresh target repos route through init before repo intake.
- Added smoke coverage for fresh workspace init, legacy preservation, root `AGENTS.md` owner-merge blocking, and `.env` non-copy behavior.

## 0.8.3 - 2026-05-27

- Added `.systems/ai/core/repository-modes.md` and `.systems/scripts/resolve-workflow-env` to formalize official repo mode versus target repo mode.
- Split target runtime out of the nested clone: public `main` no longer tracks `workspace/**`.
- Added `AI_WORKFLOW_WORKSPACE_HOME`, normally `ai-workflow-workspace/`, as the target-owned tracked runtime workspace.
- Added `.systems/scripts/check-branch-policy` to block runtime workspace files on public `main` while allowing `ai-workflow-workspace/**` on `dev`.
- Added `.systems/scripts/init-workspace` and workspace bootstrap templates.
- Changed target root `AGENTS.md` shim handling to local-only via `.git/info/exclude` together with `/ai-workflow/`.
- Updated `update-from-upstream` so it updates only the nested `ai-workflow/` clone and never touches `AI_WORKFLOW_WORKSPACE_HOME/**`.
- Added `/workspace/` to the public template `.gitignore` to prevent accidental runtime commits on `main`.

## 0.8.2 - 2026-05-25

- Added mandatory run-scoped Autopilot Readiness Audit before starting or resuming autopilot.
- Added `.systems/ai/templates/autopilot/readiness.template.md` and connected it to autopilot runtime templates.
- Updated autopilot routing, guide, response contract, workflow aliases, human docs, and validators so autopilot cannot enter `running` before readiness is `ready`.

## 0.8.1 - 2026-05-25

- Added `.systems/ai/core/task-intake.md` as the mandatory Task Idea Validation lens for new tasks, planning requests, approach requests, side-tasks, micro-tasks, change requests, and autopilot requests.
- Required new task responses to identify what stays, what is weak or should change, what is missing, blockers/decisions, and recommended routing before presenting a plan.
- Connected task intake to `AGENTS.md`, command routing, operating model, workflow routing, response contract, human documentation, and validators.

## 0.8.0 - 2026-05-21

- Split the nested clone into system-owned `.systems/**` and target-owned `AI_WORKFLOW_WORKSPACE_HOME/**`.
- Made `update-from-upstream` block dirty system-owned files and preserve the full `AI_WORKFLOW_WORKSPACE_HOME/**` tree.
- Moved External Memory to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` with detailed entries in `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/`.
- Added `AI_WORKFLOW_WORKSPACE_HOME/skills/` for user-defined local skills that take precedence over system skills as supporting guidance.
- Moved EXAMPLE workspaces to `.systems/ai/examples/` so active runtime stays under `AI_WORKFLOW_WORKSPACE_HOME/`.

## 0.7.4 - 2026-05-21

- Added `.systems/ai/core/change-requests.md` as the formal owner change request policy before and after `final-owner-yes`.
- Added project-local change request router, directory templates, and EXAMPLE artifacts.
- Updated final check, command routing, guide, workflow routing, and project workspace setup to block final approval on open pre-final change requests and route post-final changes safely.

## 0.7.3 - 2026-05-20

- Added `.systems/ai/core/response-contract.md` as the canonical user-facing response contract.
- Required substantive Codex responses to end with `Co dalej?`, one recommendation with impact and copy-paste prompt, and one safe alternative with impact and copy-paste prompt.
- Connected the response contract to `AGENTS.md`, operating model, workflow routing, guide mode, command routing, and human documentation.

## 0.7.2 - 2026-05-20

- Flattened the old internal documentation namespace so the nested clone now uses `.systems/ai/`, `AI_WORKFLOW_WORKSPACE_HOME/repo/`, `AI_WORKFLOW_WORKSPACE_HOME/projects/`, `AI_WORKFLOW_WORKSPACE_HOME/humans/`, and `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` directly.
- Moved canonical AI router and policy files into `.systems/ai/core/` while keeping workflow phases, templates, skills, memory entries, and external-memory entries in their dedicated directories.
- Moved canonical repo runtime routers into `AI_WORKFLOW_WORKSPACE_HOME/repo/core/` while keeping detailed repo context, legacy, and memory entries in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`, `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`, and `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/`.
- Moved validators from the old nested validator subdirectory to `.systems/scripts/` for the nested-clone installation model.

## 0.7.1 - 2026-05-20

- Added project-local `micro-tasks.md` and `micro-tasks/` plus repo-level `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` for low-risk work that does not need full workflow phases.
- Added the official `update-from-upstream` flow for safely updating target repository nested clones while preserving runtime, workspaces, local External Memory, and legacy source filenames.
- Excluded preserved legacy workflow inputs under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` and detailed repo context entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/` from strict Markdown naming checks while keeping canonical repo context at `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`.
- Added `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` as the canonical router and summary for preserved legacy material under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`.
- Simplified canonical accepted project context from the previous nested context-file model to `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md`.
- Excluded supporting project source materials under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/` from strict Markdown naming checks while keeping canonical project `context.md` required and status-validated before architecture and later phases.
- Added validator smoke coverage for legacy/context naming exemptions and missing canonical project context.

## 0.7.0 - 2026-05-19

- Changed the target-repository installation model to a nested clone at `ai-workflow/`.
- Added `.systems/ai/templates/root-agents.template.md` as the only file that target repositories need to copy or merge into root `AGENTS.md`.
- Clarified `TARGET_REPO_ROOT` and `AI_WORKFLOW_HOME` path resolution across the root shim, internal `AGENTS.md`, installation policy, guide, command routing, repo intake, and workflow router.
- Updated repo intake to treat `ai-workflow-workspace/repo/` as runtime that must be replaced with target-repository facts after installation.
- Kept target-owned `docs/`, `.systems/`, `.github/`, `README.md`, `HUMANS.md`, and existing `AGENTS.md` out of the default install path.

## 0.6.0 - 2026-05-19

- Converted repo context into `context.md` router plus detailed entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
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
- Added `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` for preserving pre-existing repository workflow material as context-only legacy input during repo intake.
- Moved project context into a dedicated project context area.
- Added human-facing `plans.template.md`.
- Renamed repo runtime context template to `context.template.md` to match `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`.
- Clarified that the literal `repo intake` prompt is sufficient for repo-level bootstrap when AI Workflow is installed.

## 0.4.0 - 2026-05-18

- Converted workflow filenames to lowercase kebab-case.
- Added policy docs for operating model, Definition of Done, permissions, risk, commands, prompt injection, rollback, dependencies, and deprecation.
- Converted `AGENTS.md` into a short execution router.
- Added automatic workflow validation scripts and GitHub Actions workflow.
- Added Codex configuration templates.
- Added canonical task ID model and project task index.

## 0.3.0 - 2026-05-18

- Moved repo-specific runtime facts to `AI_WORKFLOW_WORKSPACE_HOME/repo/`.
- Added idea validation phase.
- Renamed legacy singular human docs path to `AI_WORKFLOW_WORKSPACE_HOME/humans`.
- Made Codex the primary executor with ChatGPT as optional support.
