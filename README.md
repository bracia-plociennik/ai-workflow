# AI Workflow Template

## Purpose

This folder is a portable workflow template for repositories that should be operated with AI-assisted planning, gated implementation, QA evidence, distillation, checkpoints, and optional autopilot execution.

It is intentionally repository-neutral. Before using it in another repository, keep `AGENTS.md`, `HUMANS.md`, root workflow files, and `docs/ai/` template-owned. Put repository-specific runtime facts in `docs/repo/` and project-specific facts in `docs/projects/<project>/`.

Some workflow files use `<project>` and some use `<project>`. In this template they mean the same thing: the active directory name under `docs/projects/`.

## Contents

- `AGENTS.md` - execution contract for AI agents.
- `HUMANS.md` - practical runbook for owners, operators, and engineers.
- `docs/ai/workflow.md` - workflow router and phase index.
- `docs/repo/` - target-repository runtime context, intake, status, and aggregate memory.
- `docs/ai/workflow/` - detailed process rules for every phase.
- `docs/ai/autopilot.md` - autopilot behavior, gates, runtime files, retry policy, and STOP conditions.
- `docs/ai/memory.md` - template-local memory for this workflow repository.
- `docs/ai/external-memory.md` - universal workflow/process memory for improving this template across repositories.
- `docs/ai/templates/` - reusable templates for AI runtime, workflow, project, human, and autopilot artifacts.
- `docs/projects/EXAMPLE/` - example project workspace showing the expected artifact layout.
- `docs/humans/EXAMPLE/` - example human-facing artifacts.

## How To Install In Another Repository

1. Copy `AGENTS.md`, `HUMANS.md`, and `docs/` into the repository root.
2. Read `HUMANS.md` first to understand the operating model.
3. Create or refresh `docs/repo/` from `docs/ai/templates/ai/`.
4. Fill `docs/repo/context.md` with global repository context:
   - repository purpose, domain, stack, main modules, boundaries, and local rules.
5. Run repo-level intake and fill `docs/repo/repo-intake.md`:
   - verify `AGENTS.md`, `HUMANS.md`, `docs/ai`, `docs/repo`, status, templates, safe command policy, STOP conditions, and memory files;
   - do this even before a project workspace exists.
6. Set `docs/repo/status.md` for the repository:
   - active workspace;
   - current phase;
   - next phase;
   - whether workflow is mandatory or optional.
7. Create a real project workspace under `docs/projects/<project>/`.
8. If starting from a rough idea, run `000. IDEA VALIDATION` into `docs/projects/<project>/intake/phase-0-idea-validation.md`.
9. Create accepted project context in `docs/projects/<project>/intake/context.md`.
10. Run project/context intake into `docs/projects/<project>/intake/phase-0-repo-intake.md`.
11. Continue through architecture, QA, plan, packaging, specs, implementation, quality, distillation, checkpoints, and final check.

## First-Time Checklist

- `AGENTS.md` exists in repo root and remains template-owned.
- `HUMANS.md` exists in repo root.
- `docs/repo/context.md` exists and describes the target repository.
- `docs/repo/repo-intake.md` exists and has been filled for the target repository.
- `docs/ai/external-memory.md` exists and is kept universal, not repo-specific.
- `docs/repo/status.md` points to the current real workspace or explicitly says no workspace is active.
- `docs/projects/<project>/status.md` exists for active project work.
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
git diff --check
scripts/validate-workflow
scripts/check-naming
scripts/check-required-artifacts
scripts/check-status-consistency
scripts/check-qa-evidence
rg -n "source-repo-name|old-project-name|production-credential" AGENTS.md HUMANS.md docs/ai docs/repo
```

Then ask Codex to run:

```text
repo intake
```

The first intake should adapt the workflow to the new repository before any implementation work starts.
