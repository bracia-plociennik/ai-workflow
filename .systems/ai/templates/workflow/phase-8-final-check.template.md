# 8. Final Check

Execution efficiency (when applicable): record check applicability, invocation reason, executed/reused/invalidated evidence, source receipt and fresh artifact checks under .systems/ai/core/execution-efficiency.md. Supplied reviewer evidence may use prepare-quality-record; technical verification does not grant owner approval.

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Workflow phase: `8. FINAL CHECK`
- Result: `<PASS|FAIL|awaiting-owner-final-yes>`
- QA verification contract: `full-qa-verification-v2` (technical assessment only; owner approval remains separate)

## Current QA Run

- Run ID: `<unique-kebab-case-id>`
- Artifact kind: final-check
- Project/task identity: `<project>`
- Assessed source HEAD: `<40-hex-commit>`
- Assessed worktree digest: `<64-hex-digest>`
- Input artifacts: see table
- Verdict: `<PASS|FAIL>`
- Gate Decision: `<PASS|FAIL>`

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | status.md | `<64-hex-sha256>` |

### Evidence

- Reviewed input hashes, completion matrix, unresolved decisions and findings for this run:

### Review Completeness Gate

- Status: `<complete|incomplete>`
- Reviewed baseline: `<HEAD/worktree/artifact identifiers>`
- Closure freshness: `<current|stale>`
- Post-fix full re-review: `<completed|not-required|incomplete>`
- Policy-boundary adversarial matrix: `<completed|not-applicable|incomplete>`
- Producer-consumer field audit: `<completed|not-applicable|incomplete>`
- Required-field mapping: `<complete|not-applicable|partial|mismatch>`

### Scope Under Final Check

- Plan artifact:
- Completed tasks/packages:
- Deferred tasks/packages:
- Out-of-scope:

### Completion Review

| Area | Result | Evidence |
| --- | --- | --- |
| All in-scope tasks completed or deferred | `<PASS|FAIL>` | |
| Quality PASS exists for completed tasks | `<PASS|FAIL>` | |
| Distillations complete | `<PASS|FAIL>` | |
| Checkpoint complete | `<PASS|FAIL>` | |
| Repo/memory/status consistent | `<PASS|FAIL>` | |
| External workflow memory consistent, if used | `<PASS|FAIL|n/a>` | |
| System insights anonymized and scope-correct, if used | `<PASS|FAIL|n/a>` | |
| No unresolved blocking decisions | `<PASS|FAIL>` | |
| No open blocking change requests | `<PASS|FAIL>` | `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/change-requests.md` |

### Findings

- Blockers: `<none|resolved|list>`
- Unresolved findings: `<none|list>`

#### Critical Errors

- 

#### Warnings

- 

#### Residual Risks

- 

### Owner Approval

- Technical final check result: `<PASS|FAIL>`
- Owner approval required: `yes`
- Owner decision: `<awaiting|approved|rejected>`
- Owner comments captured as change request: `<yes|no|not-applicable>`

### Change Request Review

| Change request | Timing | Status | Blocks final-owner-yes? | Route |
| --- | --- | --- | --- | --- |
| `<none|CR ID>` | `<pre-final-approval|post-final-approval>` | `<status>` | `<yes|no|not-applicable>` | `<route>` |

### Final Gate

- Can close active plan: `<yes|no|awaiting-owner>`
- Required next phase: `<owner approval|change-request-triage|fix loop|closed>`
- Blocking reason: `<none|reason>`

## Owner Decision Checkpoint

- Interaction mode: `<interactive|queued|suppressed-owner-opt-out|none>`
- Decision state: `<clear|awaiting-owner|blocked|queued>`
- Material decisions: `<decision IDs|none>`
- Questions asked: `<decision IDs|none>`
- Auto-resolved reversible decisions: `<decision IDs|none>`
- Optional owner refinements: `<list|none>`
- Decision artifacts: `<paths|none>`
- Next route:

## Optional Knowledge Capture

- Capture recommended: `<yes|no>`
- Target: `<project-memory|repo-memory|external-memory|system-insights|decision-artifact|status|none>`
- Reason:
- Owner decision required: `<yes|no>`
- Owner decision: `<capture-now|defer-to-distillation|defer-to-checkpoint|reject|not-requested>`
- Privacy/scope check: `<pass|fail|n/a>`
- Suggested entry title:
- Suggested entry summary:
