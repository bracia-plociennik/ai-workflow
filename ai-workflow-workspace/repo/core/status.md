# Repo Status

## Purpose

This is the workflow status snapshot for this repository.

## Current Status

| Field | Value |
| --- | --- |
| `workflow-requirement` | `optional` |
| `workflow-scope` | `template-maintenance` |
| `active-project` | `none` |
| `active-plan-status` | `none` |
| `current-task` | `maintain ai-workflow public template and dev workspace` |
| `current-phase` | `not-applicable` |
| `phase-result` | `completed` |
| `next-phase` | `none` |
| `last-completed-phase` | `not-applicable` |
| `blocking-reason` | `none` |
| `autopilot-mode` | `not-active` |
| `autopilot-state` | `not-created` |
| `updated-at` | `2026-06-09` |

## Notes

- This repository is the portable `ai-workflow` template itself.
- In target repositories, AI Workflow should stay in the nested clone directory `ai-workflow/`; target roots get only the `AGENTS.md` shim.
- `.systems/` is system-owned and must not store target-repo runtime facts or user-local workflow changes.
- `ai-workflow-workspace/` stores repo-local runtime/advisory state for this repository, including external memory and user skills.
- Public `main` stays free of active runtime; public `dev` keeps this repository's own runtime in `ai-workflow-workspace/`.
- Do not mark any project phase as `PASS` without evidence in the relevant project `quality/` directory.
- The former `ai-system` branch/prototype has been removed from this repository and is treated as moved to a separate repository. Historical workflow artifacts remain under `ai-workflow-workspace/projects/ai-system/`.
