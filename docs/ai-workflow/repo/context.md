# Repo Context

## Purpose

This file describes this repository at a global level.

## Repository Summary

| Field | Value |
| --- | --- |
| Repository name | `ai-workflow` |
| Repository path | `/Users/jakubplociennik/Code/ai-workflow` |
| Primary purpose | Portable AI workflow template for repositories operated with Codex, gated planning, QA evidence, distillation, checkpoints, and optional autopilot. |
| Primary audience/users | Repository owners, operators, engineers, and AI agents using this workflow in target repositories. |
| Main domain | AI-assisted software delivery workflow and documentation system. |
| Current lifecycle stage | template repository |

## Stack And Runtime

- Languages: Markdown documentation only.
- Frameworks: none detected.
- Package managers: none detected.
- Runtime services: none.
- Datastores: none.
- Queues/schedulers: none.
- External integrations: none configured in repository state.

## Main Areas

| Area | Purpose | Notes |
| --- | --- | --- |
| Root entrypoints | Execution contract and human runbook | In target repos, existing `AGENTS.md`, `HUMANS.md`, and `README.md` are merged, not overwritten. |
| `docs/ai-workflow/ai/` | Workflow source and templates | Must stay generic and updateable from upstream. |
| `docs/ai-workflow/repo/` | Repo-specific runtime docs | Contains this repo's context, intake, status, and memory. |
| `docs/ai-workflow/projects/EXAMPLE/` | Example project workspace | Demonstrates artifact layout only. |
| `docs/ai-workflow/humans/EXAMPLE/` | Example human-facing docs | Demonstrates summaries, decisions, runbooks, audits, approvals, and human plans. |

## Boundaries

- In scope for this repository: workflow docs, templates, example artifacts, repo-local runtime artifacts, and human runbook docs.
- Out of scope for this repository: application code, real product architecture, production deployment, secrets, customer data, paid vendor commitments, and target-repository domain facts outside `docs/ai-workflow/repo/` examples.
- Shared ownership boundaries: `docs/ai-workflow/` and `scripts/ai-workflow/` are workflow-owned; target-root `docs/`, `scripts/`, `.github/`, and `README.md` are target-owned outside explicit workflow paths.

## Local Operating Rules

- Do not put repo-specific facts in root entrypoints or `docs/ai-workflow/ai/`.
- Put global repo facts in `docs/ai-workflow/repo/context.md`, `docs/ai-workflow/repo/repo-intake.md`, `docs/ai-workflow/repo/status.md`, and `docs/ai-workflow/repo/memory.md`.
- Put project-specific execution artifacts in `docs/ai-workflow/projects/<project>/`.
- Put human-facing coordination artifacts in `docs/ai-workflow/humans/<project>/`.

## Open Questions

| Question | Impact | Owner |
| --- | --- | --- |
| Should uppercase template filenames be converted from `_` to `-` later? | Naming consistency, larger reference migration. | Owner |
