# AI Docs

This directory contains template-owned AI operational knowledge and workflow infrastructure.

Do not store target-repository-specific facts in `docs/ai-workflow/ai/`. Runtime repo context, intake, status, and aggregate memory belong in `docs/ai-workflow/repo/`.

## Contents

- `operating-model.md` - primary operating contract behind the short `AGENTS.md` router.
- `workflow.md` - phase router and canonical phase index.
- `installation.md` - safe installation and collision policy for existing repositories.
- `update-from-upstream.md` - safe upstream update policy for target repositories using the nested clone.
- `autopilot.md` - autopilot launch and runtime rules.
- `command-routing.md` - user-facing workflow command aliases and interpretation rules.
- `guide.md` - orientation rules for lost, starting, next-step, and recovery prompts.
- `definition-of-done.md` - evidence-backed done criteria.
- `risk-model.md` - risk classes and approval routing.
- `commands.md` - verification command contract.
- `permissions.md` - forbidden actions and safe defaults.
- `prompt-injection.md` - defense rules for untrusted repository content.
- `rollback.md` - rollback requirements for high-risk work.
- `dependencies.md` - dependency approval and review policy.
- `deprecation.md` - archive and supersession policy.
- `version.md` and `changelog.md` - workflow version and migration history.
- `memory.md` and `memory/` - template-local memory router and detailed maintenance entries.
- `external-memory.md` and `external-memory/` - universal advisory memory router and entries for improving AI Workflow across repositories.
- `workflow/` - detailed phase-level workflow rules.
- `templates/` - reusable templates for repo runtime, workflow, autopilot, project, human, and Codex artifacts.
- `skills/` - optional task-specific execution guidance, empty by default.

## Runtime Boundaries

In target repositories, this directory normally lives under `AI_WORKFLOW_HOME`, usually `ai-workflow/docs/ai-workflow/ai/`. Product files, app commands, tests, builds, migrations, and target-owned root docs remain in `TARGET_REPO_ROOT`.

- Repo-specific facts belong in `docs/ai-workflow/repo/`; detailed repo context belongs in `docs/ai-workflow/repo/context/` and is indexed by `docs/ai-workflow/repo/context.md`.
- Project-specific facts belong in `docs/ai-workflow/projects/<project>/`, with accepted project context under `docs/ai-workflow/projects/<project>/context.md`.
- Repo-level low-risk micro-projects belong in `docs/ai-workflow/micro-projects/`.
- Human-facing coordination docs belong in `docs/ai-workflow/humans/<project>/`.
- Template/process docs belong in `docs/ai-workflow/ai/`.
- Template maintenance memory belongs in `docs/ai-workflow/ai/memory/` and is indexed by `docs/ai-workflow/ai/memory.md`.
- Universal AI Workflow improvement lessons belong in `docs/ai-workflow/ai/external-memory/` and are indexed by `docs/ai-workflow/ai/external-memory.md`.
- Reusable AI Workflow skills belong in `docs/ai-workflow/ai/skills/`.

## Manual Iterations

For a new repository or a repository where `ai-workflow/` was just cloned, start from `docs/ai-workflow/repo/context.md`, `docs/ai-workflow/repo/context/`, and `docs/ai-workflow/repo/repo-intake.md`, using `templates/repo/` if the runtime files are missing or still describe the upstream `ai-workflow` repository.

Before installing into an existing repository, follow `installation.md`. Do not overwrite target-owned `README.md`, `AGENTS.md`, `HUMANS.md`, `docs/`, `scripts/`, or `.github/`. The default install keeps workflow internals inside `ai-workflow/` and uses only the root `AGENTS.md` shim from `docs/ai-workflow/ai/templates/root-agents.template.md`.

For project-level workflow work, start from `workflow.md`, verify `docs/ai-workflow/repo/status.md`, then open the relevant phase file under `workflow/`.

Before planning, specifying, implementing, or reviewing a task, check `skills/` for a relevant task-specific skill. If no matching skill exists, continue with the normal workflow.

## Autopilot Iterations

Global autopilot rules and templates live here. Runtime autopilot artifacts belong in the active project workspace, under run directories such as `docs/ai-workflow/projects/<project>/autopilot/runs/autopilot-001/`.

Do not store project task specs, project plans, project QA evidence, project decisions, or target-repo runtime facts directly in `docs/ai-workflow/ai/`.
