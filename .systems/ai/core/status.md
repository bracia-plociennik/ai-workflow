# status.md

## Purpose

This file is system-owned. It is not the runtime status for a target repository.

Runtime workflow status belongs in:

```text
workspace/repo/core/status.md
```

`.systems/ai/core/status.md` exists only to make the template layout self-describing and to prevent old workflows from treating `.systems/ai` as repo-specific state.

## Template Status

| Field | Value |
| --- | --- |
| `template-role` | `workflow-source` |
| `runtime-status-path` | `workspace/repo/core/status.md` |
| `repo-specific-data-allowed-here` | `no` |
| `active-project` | `see workspace/repo/core/status.md` |
| `next-runtime-step` | `see workspace/repo/core/status.md` |

## Rules

- Do not update this file during normal project execution.
- Do not store active task, active phase, blockers, repo commands, or project state here.
- Update `workspace/repo/core/status.md` instead.
