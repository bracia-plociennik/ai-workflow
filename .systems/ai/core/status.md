# status.md

## Purpose

This file is system-owned. It is not the runtime status for a target repository.

Runtime workflow status belongs in:

```text
AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md
```

`.systems/ai/core/status.md` exists only to make the template layout self-describing and to prevent old workflows from treating `.systems/ai` as repo-specific state.

## Template Status

| Field | Value |
| --- | --- |
| `template-role` | `workflow-source` |
| `runtime-status-path` | `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` |
| `repo-specific-data-allowed-here` | `no` |
| `active-project` | `see AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` |
| `next-runtime-step` | `see AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` |

## Rules

- Do not update this file during normal project execution.
- Do not store active task, active phase, blockers, repo commands, or project state here.
- Update `AI_WORKFLOW_WORKSPACE_HOME/repo/core/status.md` instead.

For a project status reporting formal QA `PASS`, `check-status-consistency` must resolve a matching current V2 QA assessment, when present, through the same `.systems/scripts/lib/qa-evidence.py` reader used by `check-qa-evidence`. When the phase has V2 reports, status cannot point to another task with no corresponding assessment. The selected current V2 verdict must itself be `PASS`; a valid current `FAIL`, stale input, conflicting gate, cross-task identity or duplicate current assessment cannot support status `PASS`. Existing V1 and exact registered legacy reports retain their original evidence route. This source file is not a runtime status record.
