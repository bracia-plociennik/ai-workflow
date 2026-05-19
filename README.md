# AI Workflow Template

## Purpose

This folder is a portable workflow template for repositories that should be operated with AI-assisted planning, gated implementation, QA evidence, distillation, checkpoints, and optional autopilot execution.

It is intentionally repository-neutral. Before using it in another repository, keep workflow-owned files under `docs/ai-workflow/` and `scripts/ai-workflow/`. Put repository-specific runtime facts in `docs/ai-workflow/repo/` and project-specific facts in `docs/ai-workflow/projects/<project>/`.

In this template, `<project>` means the active directory name under `docs/ai-workflow/projects/`.

## Contents

- `AGENTS.md` - execution contract for AI agents.
- `HUMANS.md` - practical runbook for owners, operators, and engineers.
- `docs/ai-workflow/ai/workflow.md` - workflow router and phase index.
- `docs/ai-workflow/ai/installation.md` - safe install and collision policy for existing repositories.
- `docs/ai-workflow/ai/command-routing.md` - user-facing command aliases and safe interpretation rules.
- `docs/ai-workflow/repo/` - target-repository runtime context, intake, status, and aggregate memory.
- `docs/ai-workflow/ai/workflow/` - detailed process rules for every phase.
- `docs/ai-workflow/ai/autopilot.md` - autopilot behavior, gates, runtime files, retry policy, and STOP conditions.
- `docs/ai-workflow/ai/memory.md` - template-local memory for this workflow repository.
- `docs/ai-workflow/ai/external-memory.md` - universal workflow/process memory for improving this template across repositories.
- `docs/ai-workflow/ai/templates/` - reusable templates for repo runtime, workflow, project, human, and autopilot artifacts.
- `docs/ai-workflow/ai/skills/` - optional task-specific skills for AI Workflow, empty by default.
- `docs/ai-workflow/projects/EXAMPLE/` - example project workspace showing the expected artifact layout.
- `docs/ai-workflow/humans/EXAMPLE/` - example human-facing artifacts.

## How To Install In Another Repository

1. Run an installation preflight before copying anything:

   ```bash
   test -e README.md && echo "README.md exists"
   test -e AGENTS.md && echo "AGENTS.md exists"
   test -e HUMANS.md && echo "HUMANS.md exists"
   test -e docs && echo "docs exists"
   test -e docs/ai-workflow && echo "docs/ai-workflow exists"
   test -e scripts && echo "scripts exists"
   test -e scripts/ai-workflow && echo "scripts/ai-workflow exists"
   test -e .github && echo ".github exists"
   test -e .github/workflows/ai-workflow-validate.yml && echo "ai-workflow CI exists"
   ```

2. Copy only workflow-owned namespaces, never the whole target-owned `docs/`, `scripts/`, or `.github/` trees:

   ```bash
   mkdir -p docs scripts .github/workflows
   if [ ! -e docs/ai-workflow ]; then cp -R ../ai-workflow/docs/ai-workflow docs/; else echo "docs/ai-workflow exists: classify before sync"; fi
   if [ ! -e scripts/ai-workflow ]; then cp -R ../ai-workflow/scripts/ai-workflow scripts/; else echo "scripts/ai-workflow exists: classify before sync"; fi
   if [ ! -e .github/workflows/ai-workflow-validate.yml ]; then cp ../ai-workflow/.github/workflows/ai-workflow-validate.yml .github/workflows/; else echo "ai-workflow CI exists: classify before sync"; fi
   if [ ! -e AGENTS.md ]; then cp ../ai-workflow/AGENTS.md AGENTS.md; else echo "AGENTS.md exists: merge required"; fi
   if [ ! -e HUMANS.md ]; then cp ../ai-workflow/HUMANS.md HUMANS.md; else echo "HUMANS.md exists: merge required"; fi
   ```

3. If root `AGENTS.md` or `HUMANS.md` already exists, merge AI Workflow routing into the existing file with owner approval. Do not overwrite it.
4. Do not overwrite target `README.md`; add only an optional link or short section pointing to `HUMANS.md` and `docs/ai-workflow/`.
5. Read `HUMANS.md` first to understand the operating model.
6. Create or refresh `docs/ai-workflow/repo/` from `docs/ai-workflow/ai/templates/repo/`.
   - If copied `docs/ai-workflow/repo/context.md`, `repo-intake.md`, `status.md`, or `memory.md` still describe `ai-workflow`, treat them as stale runtime state and replace them during repo intake.
7. Fill `docs/ai-workflow/repo/context.md` with global repository context:
   - repository purpose, domain, stack, main modules, boundaries, and local rules.
8. Run repo-level intake and fill `docs/ai-workflow/repo/repo-intake.md`:
   - verify `AGENTS.md`, `HUMANS.md`, `docs/ai-workflow/ai`, `docs/ai-workflow/repo`, status, templates, safe command policy, STOP conditions, and memory files;
   - do this even before a project workspace exists.
9. Set `docs/ai-workflow/repo/status.md` for the repository:
   - active workspace;
   - current phase;
   - next phase;
   - whether workflow is mandatory or optional.
10. Run `phase-0-project-workspace` to create or reconcile a real project workspace under `docs/ai-workflow/projects/<project>/` and `docs/ai-workflow/humans/<project>/`.
11. If starting from a rough idea, run `000. IDEA VALIDATION` into `docs/ai-workflow/projects/<project>/intake/phase-0-idea-validation.md`.
12. Create accepted project context in `docs/ai-workflow/projects/<project>/context/context.md`.
13. Run project/context intake into `docs/ai-workflow/projects/<project>/intake/phase-0-repo-intake.md`.
14. Continue through architecture, QA, plan, packaging, specs, implementation, quality, distillation, checkpoints, and final check.

## First-Time Checklist

- root `AGENTS.md` exists or has an approved AI Workflow merge section.
- root `HUMANS.md` exists or has an approved AI Workflow merge section.
- install collisions are resolved according to `docs/ai-workflow/ai/installation.md`.
- `docs/ai-workflow/repo/context.md` exists and describes the target repository.
- `docs/ai-workflow/repo/repo-intake.md` exists and has been filled for the target repository.
- copied `ai-workflow` runtime files under `docs/ai-workflow/repo/*.md` have been replaced when the current repo is not `ai-workflow`.
- `docs/ai-workflow/ai/external-memory.md` exists and is kept universal, not repo-specific.
- `docs/ai-workflow/repo/status.md` points to the current real workspace or explicitly says no workspace is active.
- `docs/ai-workflow/projects/<project>/status.md` exists for active project work.
- `docs/ai-workflow/projects/<project>/context/context.md` exists before architecture work starts.
- `docs/ai-workflow/humans/<project>/` exists when the project needs human-facing approvals, audits, runbooks, plans, or summaries.
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
scripts/ai-workflow/validate-workflow
scripts/ai-workflow/check-naming
scripts/ai-workflow/check-required-artifacts
scripts/ai-workflow/check-status-consistency
scripts/ai-workflow/check-qa-evidence
rg -n "source-repo-name|old-project-name|production-credential" AGENTS.md HUMANS.md docs/ai-workflow/ai docs/ai-workflow/repo
```

Then ask Codex to run:

```text
repo intake
```

The literal `repo intake` prompt is enough after AI Workflow has been copied or merged into the repository. It must adapt the workflow to the new repository, replace stale copied `docs/ai-workflow/repo/*.md` runtime, fill repo-specific command/safety/risk information, and stop on unresolved installation collisions before any implementation work starts.
