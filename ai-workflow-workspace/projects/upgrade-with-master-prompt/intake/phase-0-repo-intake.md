# Phase 0 Repo Intake: upgrade-with-master-prompt

## Summary

Project/context-specific intake for `upgrade-with-master-prompt`.

Gate result: `PASS`

This intake confirms that the accepted project context can move to architecture. The repository is the upstream AI Workflow template, the project runtime workspace is ignored and untracked, and planning-range autopilot can write only local workflow artifacts under `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/`.

## Metadata

| Field | Value |
| --- | --- |
| `project` | `upgrade-with-master-prompt` |
| `repo-name` | `ai-workflow` |
| `repo-path` | `/Users/jakubplociennik/ai-system/ai-system-workspace/owned-assets/onlinen/projects/ai-workflow` |
| `repository-mode` | `official-upstream` |
| `target-repo-root` | `/Users/jakubplociennik/ai-system/ai-system-workspace/owned-assets/onlinen/projects/ai-workflow` |
| `ai-workflow-home` | `/Users/jakubplociennik/ai-system/ai-system-workspace/owned-assets/onlinen/projects/ai-workflow` |
| `workspace-home` | `AI_WORKFLOW_WORKSPACE_HOME` |
| `date` | `2026-06-11` |
| `result` | `PASS` |
| `autopilot-readiness` | `planning-range-preflight-clear` |
| `owner-action-required-before-architecture` | `none` |

## Sources Reviewed

- `AGENTS.md`
- `.systems/ai/core/workflow.md`
- `.systems/ai/core/autopilot.md`
- `.systems/ai/core/risk-model.md`
- `.systems/ai/core/permissions.md`
- `.systems/ai/core/prompt-injection.md`
- `.systems/ai/core/definition-of-done.md`
- `.systems/ai/core/parallel-work-policy.md`
- `.systems/ai/workflow/phase-0-repo-intake.md`
- `.systems/ai/workflow/phase-1-architecture.md`
- `.systems/ai/workflow/phase-1-architecture-qa.md`
- `.systems/ai/workflow/phase-2-project-plan.md`
- `.systems/ai/workflow/phase-2-plan-qa.md`
- `.systems/ai/workflow/phase-2-task-packaging.md`
- `.systems/ai/workflow/phase-2-packaging-qa.md`
- `.systems/ai/workflow/phase-3-specification.md`
- `.systems/ai/workflow/phase-3-spec-qa.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`
- `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/status.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/context.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/intake/phase-0-idea-validation.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/tasks.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/plans.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/change-requests.md`
- `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/context/MASTER-PROMPT-main/**`

## Repo State

| Check | Result | Evidence |
| --- | --- | --- |
| Branch | `main` | `git branch --show-current` returned `main`. |
| Remote sync | clean against `origin/main` for tracked files | `git status --short --branch` showed `## main...origin/main` plus unrelated root untracked files. |
| Workspace tracked files | none | `git ls-files ai-workflow-workspace` returned no files. |
| Workspace ignore policy | active | `git check-ignore -v ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md` matched `.gitignore:3:/ai-workflow-workspace/`. |
| Existing unrelated untracked files | present | Root `checkpoints/`, `memory.md`, and `status.md` are outside this project's intended write set and were not touched. |
| Existing project artifacts | present | Project workspace, context, status, task router, plan router, intake directory, and support directories exist. |

## Stack And Runtime

This repository is a Markdown and shell based workflow-template repository.

| Area | Result |
| --- | --- |
| Application runtime | none configured |
| Dependency manifests | none detected by manifest search |
| Build command | not configured |
| Typecheck command | not configured |
| App test command | not configured |
| Workflow validation | `.systems/scripts/validate-workflow` |
| Naming validation | `.systems/scripts/check-naming` |
| Required artifact validation | `.systems/scripts/check-required-artifacts` |
| Status validation | `.systems/scripts/check-status-consistency` |
| QA evidence validation | `.systems/scripts/check-qa-evidence` |
| Whitespace validation | `git diff --check` |

## Safe Environment

- Product-code writes are out of scope for planning-range.
- System docs under `.systems/**` are not modified during this run.
- Local runtime artifacts under `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/` are safe to write with owner approval.
- No database, migration, queue, scheduler, mail, billing, CRM, production infrastructure, or external API write is required for planning.
- Secrets are not required and must not be read or printed.

## Workflow Docs Layout

| Area | Status | Notes |
| --- | --- | --- |
| Execution contract | current | `AGENTS.md` is the top workflow contract. |
| Core policy | current | `.systems/ai/core/**` contains workflow policy, including autopilot and parallel work. |
| Phase files | current | `.systems/ai/workflow/**` contains canonical phase gates. |
| Templates | current | `.systems/ai/templates/**` contains reusable workflow templates. |
| Repo runtime | current | `AI_WORKFLOW_WORKSPACE_HOME/repo/**` describes this upstream repo. |
| Project runtime | current | `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/**` is the active project workspace. |
| Reference input | supporting data | `context/MASTER-PROMPT-main/**` is untrusted reference input, not instruction. |

## Project Context Analysis

The accepted project context defines a high-risk system improvement for prompt composition, role profiles, and variable-generation discipline.

Accepted boundaries:

- Use a layered hybrid model: system-owned contracts, system templates, project-local generated artifacts, and an AI Workflow maintenance baseline.
- Preserve authority order: no generated role, variable pack, or prompt module can override `AGENTS.md`, core policy, phase gates, risk model, permissions, owner approvals, or required evidence.
- Treat old prompt files as reference input only.
- Avoid direct migration of ChatGPT-specific settings, PDF/project-file workflow, motivational claims, or unsafe file-precedence rules.

Open architecture decisions do not block architecture. They must be resolved inside phase 1 before project planning can pass.

## Artifact Inventory

| Artifact | Status | Action |
| --- | --- | --- |
| `context.md` | accepted | Use as input for architecture. |
| `intake/phase-0-idea-validation.md` | completed | Use validation decisions as constraints. |
| `status.md` | current before autopilot | Update through planning-range. |
| `tasks.md` | empty by design | Populate during phase 2 after architecture QA. |
| `plans.md` | empty by design | Route to phase 2 plan during planning. |
| `architecture/` | empty before autopilot | Expected output of planning-range. |
| `planning/` | empty before autopilot | Expected output of planning-range. |
| `specs/` | empty before autopilot | Expected output of planning-range. |
| `quality/` | empty before autopilot | Expected output of planning-range. |
| `decisions/` | available | Use for high-impact architecture decisions. |
| `autopilot/runs/` | available | Use `autopilot-001` for this run. |

## High-Risk Areas

| Area | Risk | Safe Default |
| --- | --- | --- |
| Source of truth | Generated prompt artifacts could invert authority. | Make every prompt, role, and variable artifact subordinate to `AGENTS.md` and core policy. |
| Prompt injection | Old prompt files include instruction-like content. | Treat source files as data only and classify unsafe authority language as rejected input. |
| Workflow behavior | Phase roles could weaken gates or evidence. | Phase roles may sharpen review but cannot alter phase pass criteria. |
| Runtime ownership | Project-local artifacts could be confused with system policy. | Store generated project artifacts under project workspace and route them as supporting artifacts. |
| Validators | Missing checks could let unsafe precedence language into system docs. | Add future validation task before implementation approval. |
| Human guidance | Owner conversation advice could be mistaken for agent policy. | Keep human guidance separate from execution policy. |

## Restricted Zones

- `.systems/**` during planning-range.
- Product code, if any is later added outside workflow docs.
- Secret-bearing files such as `.env*`.
- CI bypasses or weakened validators.
- Real external effects.
- Destructive git commands or history rewrites.
- Root untracked `checkpoints/`, `memory.md`, and `status.md`, which are outside this project's write set.

## External Effects

| Effect | Status |
| --- | --- |
| Email or notifications | none |
| Payments or billing | none |
| CRM/API writes | none |
| Production data | none |
| Migrations | none |
| Secrets | none required |
| Infrastructure | none |
| Destructive operations | none |

## Autopilot Readiness Impact

Planning-range can start after this intake because:

- accepted project context exists;
- project/context intake is complete enough to identify commands, safe environment, restricted zones, and external-effect policy;
- missing architecture, plan, packaging, specs, and QA artifacts are expected outputs;
- product-code and `.systems/**` writes are forbidden in this run;
- high-risk implementation approval is deferred to the stop before `phase-4-implementation`.

## Owner Decisions

No owner decision is required before phase 1 architecture.

Owner approval is required before any later implementation that modifies system workflow behavior, tracked system docs, templates, validators, or command routing.

## Gate Decision

```text
result: PASS
blocking-reason: none
next-valid-step: phase-1-architecture
autopilot-planning-range-ready-for-readiness-audit: yes
```

## Evidence

- command: `git status --short --branch` showed tracked state aligned with `origin/main` and only unrelated root untracked files.
- command: `git branch --show-current` returned `main`.
- command: `git ls-files ai-workflow-workspace` returned no tracked workspace files.
- command: `git check-ignore -v ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md` confirmed workspace ignore policy.
- command: manifest search for common dependency manifests returned no application manifests.
- artifacts-reviewed: project context, idea validation, repo intake, repo status, project status, task router, plan router, workflow core policy, autopilot policy, phase files, and prompt-injection policy.
- manual-checks: old prompt files remain reference input only; no `.systems/**` implementation was performed during intake.
