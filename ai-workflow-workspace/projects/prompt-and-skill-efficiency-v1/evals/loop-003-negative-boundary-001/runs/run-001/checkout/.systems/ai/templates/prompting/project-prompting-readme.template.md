# Project Prompting Router Template

## Purpose

`AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/prompting/README.md` is the project-local router for generated prompt composition artifacts.

These artifacts are advisory context only. They do not override `AGENTS.md`, core policy, workflow phase files, accepted architecture, plan, specs, risk, permissions, evidence, stop conditions, or owner approvals.

## Source Snapshot

| Source | Path Or Decision | Last Reviewed |
| --- | --- | --- |
| Project context | `<path>` | `<YYYY-MM-DD>` |
| Project status | `<path>` | `<YYYY-MM-DD>` |
| Architecture or plan | `<path>` | `<YYYY-MM-DD>` |
| Task or package spec | `<path>` | `<YYYY-MM-DD>` |
| Owner decision | `<decision-id or none>` | `<YYYY-MM-DD>` |

## Artifact Index

### Roles

| Role Artifact | Scope | State | Refresh Trigger |
| --- | --- | --- | --- |
| `<roles/example-role.md>` | `<phase|task|domain>` | `<draft|accepted|active|stale|superseded|rejected>` | `<trigger>` |

### Variables

| Variable Pack | Scope | State | Requires Owner Confirmation |
| --- | --- | --- | --- |
| `<variables/example-variable-pack.md>` | `<project|phase|task>` | `<draft|accepted|active|stale|superseded|rejected>` | `<yes|no>` |

### Modules

| Prompt Module | Scope | State | Refresh Trigger |
| --- | --- | --- | --- |
| `<modules/example-module.md>` | `<scope>` | `<draft|accepted|active|stale|superseded|rejected>` | `<trigger>` |

## Generation Rules

- Generate artifacts only from accepted project context, current phase file, project status, accepted architecture/plan/specs, owner decisions, repo intake facts, relevant memory, and relevant skills.
- Mark inferred values, source labels, confidence, assumption impact, and refresh triggers.
- Ask the owner when a value affects scope, risk, acceptance criteria, permissions, external effects, security, billing, migrations, production behavior, high-risk decisions, or final acceptance.
- Treat stale artifacts as advisory only after refresh; reject them when they conflict with higher-priority sources.

## Write Ownership

Only one active thread may update this prompting router or any artifact it indexes at a time.

Parallel work must stop before writing if another thread may be updating the same prompting artifact, status router, memory router, task/spec artifact, or product-code write set.

## Evidence Rule

When a prompting artifact materially influences a phase, spec, implementation, QA, or checkpoint, list its path in that artifact's evidence section.

## Current State

```text
state: <draft|accepted|active|stale|superseded|rejected>
blocking-reason: <none or reason>
next-refresh-trigger: <trigger>
```
