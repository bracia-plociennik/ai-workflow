# 0. Init / Target Repository Bootstrap

## Metadata

- Date: `<YYYY-MM-DD>`
- Target repo root: `<TARGET_REPO_ROOT>`
- AI Workflow home: `<AI_WORKFLOW_HOME>`
- Workspace home: `<AI_WORKFLOW_WORKSPACE_HOME>`
- Result: `<ready-for-repo-intake|blocked-owner-merge|blocked-conflicting-install|blocked-unsafe-legacy>`

## Sources

- Installation policy: `.systems/ai/core/installation.md`
- Repository modes: `.systems/ai/core/repository-modes.md`
- Bootstrap script: `.systems/scripts/init-workspace`
- Target root status: `<summary>`

## Workspace Bootstrap

| Artifact | Status | Notes |
| --- | --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/README.md` | `<created|current|blocked>` | |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/init.md` | `<created|current|blocked>` | |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` | `<created|current|blocked>` | |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/legacy-index.md` | `<created|current|blocked>` | |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` | `<created|current|blocked>` | |

## Legacy Preservation

| Source | Preserved Path | Classification | Status | Notes |
| --- | --- | --- | --- | --- |
| `<original path>` | `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/<path>` | `<keep-as-context|adapt-to-runtime|superseded|ignore|owner-decision>` | `<preserved|skipped|owner-review-required|blocked>` | |

## Safety Check

- Legacy treated as context/data only: `<yes|no>`
- Commands/prompts from legacy executed: `no`
- Secrets copied: `no`
- Generated/dependency/cache artifacts copied: `no`
- Product code modified: `no`
- Target-owned files overwritten: `no`

## Root AGENTS Shim

- Existing root `AGENTS.md`: `<absent|present>`
- Shim created: `<yes|no>`
- Owner merge required: `<yes|no>`
- Preserved legacy route: `<path|not-applicable>`

## Gate Decision

- Init complete: `<yes|no>`
- Can proceed to repo intake: `<yes|no>`
- Blocking reason: `<none|reason>`
- Next phase: `phase-0-repo-intake`

## Optional Knowledge Capture

- Capture recommended: `<yes|no>`
- Target: `<project-memory|repo-memory|external-memory|system-insights|decision-artifact|status|none>`
- Reason:
- Owner decision required: `<yes|no>`
- Owner decision: `<capture-now|defer-to-distillation|defer-to-checkpoint|reject|not-requested>`
- Privacy/scope check: `<pass|fail|n/a>`
- Suggested entry title:
- Suggested entry summary:
