# Project Status Template

| Field | Value |
| --- | --- |
| `workflow-requirement` | `<mandatory|optional>` |
| `workflow-scope` | `<plan-derived|side-task|micro-task>` |
| `project-workspace` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>` |
| `active-plan-status` | `<active|closed|none|other>` |
| `current-task` | `<task>` |
| `active-change-request` | `<none|PROJECT-CR-NNN-slug>` |
| `current-phase` | `<phase|n/a>` |
| `phase-result` | `<not-started|in-progress|PASS|FAIL|completed|blocked|n/a>` |
| `next-phase` | `<phase|n/a>` |
| `next-task` | `<task|n/a>` |
| `blocking-reason` | `<none|reason>` |
| `updated-at` | `<YYYY-MM-DD>` |
| `autopilot-mode` | `<none|supervised|semi-autonomous|autonomous-execution>` |
| `autopilot-state` | `<not-running|running|stopped|awaiting-owner|completed>` |
| `autopilot-run` | `<none|autopilot-001|autopilot-002|...>` |
| `execution-mode` | `<auto|human-coop>` |
| `execution-mode-scope` | `<task|project|session>` |
| `execution-mode-source` | `<explicit-choice|new-work-default|inherited>` |
| `execution-mode-scope-id` | `<scope-id>` |

Use execution-modes.md for selection and resume. Missing fields in historical
status do not retroactively grant new autonomy. Record session identity and
decision references in the active run/task artifact when applicable.
