# Installation And Collision Policy

This file is the canonical policy for installing AI Workflow into an existing repository.

The installation rule is: merge first, never overwrite target-owned files.

## Workflow-Owned Namespaces

AI Workflow owns only these paths:

- `docs/ai-workflow/`
- `scripts/ai-workflow/`
- `.github/workflows/ai-workflow-validate.yml`
- root `AGENTS.md` only when absent or explicitly merged
- root `HUMANS.md` only when absent or explicitly merged

The target repository owns everything else, including:

- `README.md`
- existing `AGENTS.md`
- existing `HUMANS.md`
- existing `docs/`
- existing `scripts/`
- existing `.github/`
- all product code, app config, CI workflows, deployment files, secrets, and generated runtime files.

## Preflight

Before copying anything into a target repository, inspect collisions:

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

If a workflow-owned namespace already exists, classify it before copying:

- `absent`: safe to create.
- `current`: reuse it.
- `outdated`: update through a controlled template sync.
- `conflicting`: stop for owner decision.
- `target-owned`: do not overwrite.

## Copy Rules

Use namespace copy only:

```bash
mkdir -p docs scripts .github/workflows
if [ ! -e docs/ai-workflow ]; then cp -R ../ai-workflow/docs/ai-workflow docs/; else echo "docs/ai-workflow exists: classify before sync"; fi
if [ ! -e scripts/ai-workflow ]; then cp -R ../ai-workflow/scripts/ai-workflow scripts/; else echo "scripts/ai-workflow exists: classify before sync"; fi
if [ ! -e .github/workflows/ai-workflow-validate.yml ]; then cp ../ai-workflow/.github/workflows/ai-workflow-validate.yml .github/workflows/; else echo "ai-workflow CI exists: classify before sync"; fi
```

Do not run broad recursive copies of the source `docs`, `scripts`, or `.github` directories into the target repository root.

Root entrypoints require explicit handling:

```bash
if [ ! -e AGENTS.md ]; then cp ../ai-workflow/AGENTS.md AGENTS.md; else echo "AGENTS.md exists: merge required"; fi
if [ ! -e HUMANS.md ]; then cp ../ai-workflow/HUMANS.md HUMANS.md; else echo "HUMANS.md exists: merge required"; fi
```

Never overwrite target-owned `README.md`. If the owner wants README integration, add only a short link or section that points to `HUMANS.md` and `docs/ai-workflow/`.

## Root EntryPoint Merge

If the target repository already has `AGENTS.md` or `HUMANS.md`:

1. Read the existing file first.
2. Preserve target-repository rules.
3. Add AI Workflow routing only as a clearly marked section.
4. Do not weaken existing safety, security, CI, deployment, or ownership rules.
5. Stop for owner approval if the existing file conflicts with AI Workflow gates, permissions, risk model, or source-of-truth order.

## Repo Runtime Replacement

After installation, `docs/ai-workflow/repo/*.md` may still describe the upstream `ai-workflow` repository.

During `phase-0-repo-intake`, replace these runtime files with target-repository facts using templates from `docs/ai-workflow/ai/templates/repo/`:

- `docs/ai-workflow/repo/context.md`
- `docs/ai-workflow/repo/repo-intake.md`
- `docs/ai-workflow/repo/status.md`
- `docs/ai-workflow/repo/memory.md`

If stale upstream runtime cannot be replaced, repo intake must report `STALE_RUNTIME_COPY` and stop before architecture, planning, specification, implementation, or autopilot.

## CI Policy

AI Workflow may add only `.github/workflows/ai-workflow-validate.yml`.

It must not:

- modify unrelated target CI workflows;
- disable target checks;
- weaken required checks;
- bypass failing checks;
- change deployment, release, or production workflows without explicit owner approval.
