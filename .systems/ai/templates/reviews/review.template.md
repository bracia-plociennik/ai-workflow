# <YYYY-MM-DD> - <TASK-ID> Review

Execution efficiency (when applicable): record check applicability, invocation reason, executed/reused/invalidated evidence, source receipt and fresh artifact checks under .systems/ai/core/execution-efficiency.md. Supplied reviewer evidence may use prepare-quality-record; technical verification does not grant owner approval.

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

## Adaptive Data / Integration Verification Matrix

- Applicability: `<required|not-applicable>`
- Not-applicable reason: `<reason|required when not-applicable>`

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| | | | | | | |

## Validation Execution Record

- Semantic QA result:
- Findings/blockers:
- Product checks:
- Workflow script applicability: <applicable|not-applicable - reason>
- Targeted workflow commands:
- Script evidence role: `supporting-only`
- Final verdict: <No blockers found|No findings found|Ready for owner review|findings remain>

## Model Recommendation

- Recommended: <efficient-reasoning|strong-reasoning|source-backed available model>
- Availability source: <current authoritative catalog/docs|unknown, capability class only>
- Reason:
- Criticality:
- Current model known: <yes|no>
- Blocking: `no`
