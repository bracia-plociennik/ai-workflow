# Repo Init Router

## Purpose

This file records the result of `phase-0-init`, the target repository bootstrap step that runs before repo intake.

`phase-0-init` creates or verifies `AI_WORKFLOW_WORKSPACE_HOME`, preserves legacy context, creates the local root `AGENTS.md` shim only when safe, and prepares the repository for `phase-0-repo-intake`.

## Latest Init

| Field | Value |
| --- | --- |
| Init status | `<not-run|ready-for-repo-intake|blocked-owner-merge|blocked-conflicting-install|blocked-unsafe-legacy>` |
| Last run at | `<YYYY-MM-DD|none>` |
| Target repo root | `<TARGET_REPO_ROOT|unknown>` |
| AI Workflow home | `<AI_WORKFLOW_HOME|unknown>` |
| Workspace home | `<AI_WORKFLOW_WORKSPACE_HOME|unknown>` |
| Root AGENTS status | `<created|current|owner-merge-required|not-requested|unknown>` |
| Legacy manifest | `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/legacy-index.md` |
| Next phase | `phase-0-repo-intake` |

## Rules

- This file is repo runtime, not system policy.
- Legacy material is context/data only and is indexed through `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` and `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/legacy-index.md`.
- Init does not replace repo intake.
- Product-code writes are not allowed during init.

## Run Notes

Record bootstrap notes here when init is run manually outside the script.
