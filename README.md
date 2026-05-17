# AI Workflow Template

## Purpose

This folder is a portable workflow template for repositories that should be operated with AI-assisted planning, gated implementation, QA evidence, distillation, checkpoints, and optional autopilot execution.

It is intentionally repository-neutral. Before using it in another repository, adapt the repo-specific parts in `AGENTS.md`, `docs/ai/STATUS.md`, and the project workspace under `docs/projects/<project>/`.

Some workflow files use `<what_we_doing>` and some use `<project>`. In this template they mean the same thing: the active directory name under `docs/projects/`.

## Contents

- `AGENTS.md` - execution contract for AI agents.
- `HUMANS.md` - practical runbook for owners, operators, and engineers.
- `docs/ai/WORKFLOW.md` - workflow router and phase index.
- `docs/ai/REPO-INTAKE.md` - repo-level workflow/bootstrap intake for repositories with or without an active project workspace.
- `docs/ai/workflow/` - detailed process rules for every phase.
- `docs/ai/AUTOPILOT.md` - autopilot behavior, gates, runtime files, retry policy, and STOP conditions.
- `docs/ai/EXTERNAL-MEMORY.md` - universal workflow/process memory for improving this template across repositories.
- `docs/ai/templates/` - reusable templates for workflow, project, human, and autopilot artifacts.
- `docs/projects/EXAMPLE/` - example project workspace showing the expected artifact layout.
- `docs/human/EXAMPLE/` - example human-facing artifacts.

## How To Install In Another Repository

1. Copy `AGENTS.md`, `HUMANS.md`, and `docs/` into the repository root.
2. Read `HUMANS.md` first to understand the operating model.
3. Adapt `AGENTS.md`:
   - fill the repo adaptation layer;
   - define commands for install, test, lint, build, migrations, scheduler, and e2e if present;
   - define safe test environment rules;
   - define high-risk areas and restricted zones;
   - add domain operating rules.
4. Run repo-level intake and fill `docs/ai/REPO-INTAKE.md`:
   - verify `AGENTS.md`, `HUMANS.md`, `docs/ai`, status, templates, safe command policy, STOP conditions, and memory files;
   - do this even before a project workspace exists.
5. Set `docs/ai/STATUS.md` for the repository:
   - active workspace;
   - current phase;
   - next phase;
   - whether workflow is mandatory or optional.
6. Create a real project workspace under `docs/projects/<project>/`.
7. Run project/context intake into `docs/projects/<project>/intake/0_initial_audit.md`.
8. Continue through architecture, QA, plan, packaging, specs, implementation, quality, distillation, checkpoints, and final check.

## First-Time Checklist

- `AGENTS.md` exists in repo root and no longer contains template placeholders that affect execution.
- `HUMANS.md` exists in repo root.
- `docs/ai/REPO-INTAKE.md` exists and has been filled for the target repository.
- `docs/ai/EXTERNAL-MEMORY.md` exists and is kept universal, not repo-specific.
- `docs/ai/STATUS.md` points to the current real workspace or explicitly says no workspace is active.
- `docs/projects/<project>/STATUS.md` exists for active project work.
- Repo commands are recorded and verified.
- Safe test environment is documented.
- STOP conditions are accepted by the owner.
- Decision classes are understood: `auto-resolvable`, `high-impact`, `critical-risk`.
- Autopilot runtime files are created only after architecture, plan, packaging, specs, and QA gates are satisfied.

## Template Boundaries

This template should not contain:

- real project names;
- real client names;
- production credentials;
- production environment details;
- paid vendor commitments;
- repository-specific architecture decisions;
- historical project artifacts from the source repository.

The included `EXAMPLE` workspaces are illustrative only. Replace them or keep them as examples, but do not treat them as active project state.

## Validation Before Reuse

After copying this template to a new repository, run:

```bash
rg -n "<fill|TO[D]O|TB[D]|FIX[M]E|source-repo-name|old-project-name" AGENTS.md HUMANS.md docs
git diff --check
```

Then ask Codex to run:

```text
repo intake
```

The first intake should adapt the workflow to the new repository before any implementation work starts.
