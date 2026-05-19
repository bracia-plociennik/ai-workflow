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
| `current-task` | `nested clone installation model` |
| `current-phase` | `phase-5-quality` |
| `phase-result` | `completed` |
| `next-phase` | `none` |
| `last-completed-phase` | `phase-5-quality` |
| `blocking-reason` | `none` |
| `autopilot-mode` | `not-active` |
| `autopilot-state` | `not-created` |
| `updated-at` | `2026-05-19` |

## Notes

- This repository is the portable `ai-workflow` template itself.
- In target repositories, AI Workflow should stay in the nested clone directory `ai-workflow/`; target roots get only the `AGENTS.md` shim.
- `docs/ai-workflow/ai/` is template-owned and must not store target-repo facts.
- `docs/ai-workflow/repo/` stores repo-local runtime state for this repository.
- Do not mark any project phase as `PASS` without evidence in the relevant project `quality/` directory.
