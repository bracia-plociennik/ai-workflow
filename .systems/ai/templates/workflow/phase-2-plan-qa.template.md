# 2.5 Plan QA

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Artifact under review: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/planning/phase-2-project-plan.md`
- Planning router under review: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/plans.md`
- Task index under review: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/tasks.md`
- Workflow phase: `2.5. PLAN QA`
- Result: `<PASS|FAIL>`
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: `<unique-kebab-case-id>`
- Artifact kind: plan-qa
- Project/task identity: `<project>`
- Assessed source HEAD: `<40-hex-commit>`
- Assessed worktree digest: `<64-hex-digest>`
- Input artifacts: see table
- Verdict: `<PASS|FAIL>`
- Gate Decision: `<PASS|FAIL>`

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | planning/phase-2-project-plan.md | `<64-hex-sha256>` |

### Evidence

- Reviewed input hashes, semantic QA checks and findings for this run:

### Review Completeness Gate

- Status: `<complete|incomplete>`
- Reviewed baseline: `<HEAD/worktree/artifact identifiers>`
- Closure freshness: `<current|stale>`
- Post-fix full re-review: `<completed|not-required|incomplete>`
- Policy-boundary adversarial matrix: `<completed|not-applicable|incomplete>`
- Producer-consumer field audit: `<completed|not-applicable|incomplete>`
- Required-field mapping: `<complete|not-applicable|partial|mismatch>`

### QA Verification Scope

- Full QA contract: `.systems/ai/core/full-qa-verification.md`
- QA subject: `plan, planning router, and task index; not implementation code review`

### Artifact QA Completeness Gate

- Owner intent and governing sources reviewed: `<paths|missing>`
- DoD / phase acceptance criteria reviewed: `<yes|no>`
- Scope and out-of-scope consistency: `<aligned|partial|mismatch|unknown>`
- Artifact / relevant diff review: `<completed|incomplete>`
- Findings-first review: `<completed|incomplete>`
- Failure / rework / dependency scenarios: `<completed|not-applicable|incomplete>`
- Repository and source compatibility: `<aligned|partial|mismatch|unknown>`
- Post-fix full artifact re-review: `<completed|not-required|incomplete>`
- Evidence reviewed: `<paths|commands|manual checks>`
- Skipped or unreadable sources: `<none|list>`
- Residual risk: `<none|list>`
- Closure freshness: `<current|stale>`

### Checks

| Check | Result | Evidence | Finding |
| --- | --- | --- | --- |
| Architecture coverage | `<PASS|FAIL>` | | |
| Sequencing | `<PASS|FAIL>` | | |
| Redundancy | `<PASS|FAIL>` | | |
| Architecture consistency | `<PASS|FAIL>` | | |
| Task contract completeness | `<PASS|FAIL>` | | |
| Plan Quality Contract completeness | `<PASS|FAIL>` | | |
| Hidden dependencies | `<PASS|FAIL>` | | |
| Readiness statuses | `<PASS|FAIL>` | | |
| Planning router consistency | `<PASS|FAIL>` | | |
| Task index consistency | `<PASS|FAIL>` | | |

### Findings

- Blockers: `<none|resolved|list>`
- Unresolved findings: `<none|list>`

#### Critical Errors

- 

#### Warnings

- 

### Gate Decision

- Plan QA result: `<PASS|FAIL>`
- Default next phase: `<3. FAZA SPECYFIKACJI|2.6. PLAN FIX LOOP>`
- Optional owner-requested task packaging: `<requested|not-requested>`
- Can proceed to optional task packaging: `<yes|no|not-requested>`
- Required next phase: `<3. FAZA SPECYFIKACJI|2.7. TASK PACKAGING|2.6. PLAN FIX LOOP>`

## Delivery Constraints QA

- Constraint source:
- Must-have outcome:
- Cutline/deferred scope:
- Quality floor:
- Overrun route:
- Result: `<aligned|partial|mismatch|unknown>`

## Validation Execution Record

- Semantic QA result:
- Findings/blockers:
- Product checks:
- Workflow script applicability: <applicable|not-applicable - reason>
- Targeted workflow commands:
- Script evidence role: `supporting-only`
- Final verdict:

## Model Recommendation

- Recommended: <efficient-reasoning|strong-reasoning|source-backed available model>
- Availability source: <current authoritative catalog/docs|unknown, capability class only>
- Reason:
- Criticality:
- Current model known: <yes|no>
- Blocking: `no`

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
