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
| Root docs | Execution contract and human runbook | `AGENTS.md`, `HUMANS.md`, `README.md` remain template-owned. |
| `docs/ai/` | Workflow source and templates | Must stay generic and updateable from upstream. |
| `docs/repo/` | Repo-specific runtime docs | Contains this repo's context, intake, status, and memory. |
| `docs/projects/EXAMPLE/` | Example project workspace | Demonstrates artifact layout only. |
| `docs/humans/EXAMPLE/` | Example human-facing docs | Demonstrates summaries, decisions, runbooks, audits, approvals, and human plans. |

## Boundaries

- In scope for this repository: workflow docs, templates, example artifacts, repo-local runtime artifacts, and human runbook docs.
- Out of scope for this repository: application code, real product architecture, production deployment, secrets, customer data, paid vendor commitments, and target-repository domain facts outside `docs/repo/` examples.
- Shared ownership boundaries: `docs/ai/` is template-owned; `docs/repo/` is runtime state for the repository using the template; `docs/projects/<project>/` is project-specific.

## Local Operating Rules

- Do not put repo-specific facts in `AGENTS.md`, `HUMANS.md`, root workflow docs, or `docs/ai/`.
- Put global repo facts in `docs/repo/CONTEXT.md`, `docs/repo/REPO-INTAKE.md`, `docs/repo/STATUS.md`, and `docs/repo/MEMORY.md`.
- Put project-specific execution artifacts in `docs/projects/<project>/`.
- Put human-facing coordination artifacts in `docs/humans/<project>/`.

## Open Questions

| Question | Impact | Owner |
| --- | --- | --- |
| Should uppercase template filenames be converted from `_` to `-` later? | Naming consistency, larger reference migration. | Owner |
