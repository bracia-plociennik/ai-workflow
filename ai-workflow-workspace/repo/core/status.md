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
| `current-task` | `dev workspace migration to ai-workflow-workspace` |
| `current-phase` | `phase-5-quality` |
| `phase-result` | `completed` |
| `next-phase` | `none` |
| `last-completed-phase` | `phase-5-quality` |
| `blocking-reason` | `none` |
| `autopilot-mode` | `not-active` |
| `autopilot-state` | `not-created` |
| `updated-at` | `2026-05-27` |

## Notes

- This repository is the portable `ai-workflow` template itself.
- In target repositories, AI Workflow should stay in the nested clone directory `ai-workflow/`; target roots get only the `AGENTS.md` shim.
- `.systems/` is system-owned and must not store target-repo runtime facts or user-local workflow changes.
- `ai-workflow-workspace/` stores repo-local runtime/advisory state for this repository, including external memory and user skills.
- Public `main` stays free of active runtime; public `dev` keeps this repository's own runtime in `ai-workflow-workspace/`.
- Do not mark any project phase as `PASS` without evidence in the relevant project `quality/` directory.
