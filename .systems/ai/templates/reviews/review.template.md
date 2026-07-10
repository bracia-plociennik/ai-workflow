# <YYYY-MM-DD> - <TASK-ID> Review

## Metadata

| Field | Value |
| --- | --- |
| Task | `<task-id>` |
| Result | `<PASS|FAIL|blocked>` |
| Reviewer | `<human|agent|pair>` |
| Quality evidence | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/quality/<quality-file>.md` |

## Findings

| Severity | Finding | Evidence | Recommendation |
| --- | --- | --- | --- |
| `<P0|P1|P2|P3>` | `<finding>` | `<path or evidence>` | `<recommendation>` |

## Evidence

- `<reviewed artifact, command, manual check, or QA evidence>`

## Residual Risk

- `<risk or none>`

## Review Completeness Gate

- Cross-contract consistency: `<aligned|partial|mismatch|unknown>`
- Negative-space / adversarial review: `<completed|not-applicable|incomplete>`
- Policy-boundary adversarial matrix: `<completed|not-applicable|incomplete>`
- Producer-consumer field audit: `<completed|not-applicable|incomplete>`
- Producers/consumers reviewed: `<paths or not-applicable>`
- Required-field mapping: `<complete|partial|mismatch|not-applicable>`
- Reviewed baseline: `<HEAD/worktree/diff/artifact identifiers>`
- Closure freshness: `<current|stale>`
