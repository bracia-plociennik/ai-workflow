# 3.5 Spec QA

## Metadata

- Project: `<project>`
- Task/package ID:
- Date: `<YYYY-MM-DD>`
- Artifact under review: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/specs/phase-3-<task-id>-specification.md`
- Workflow phase: `3.5. SPEC QA`
- Result: `<PASS|FAIL>`
- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: `<unique-kebab-case-id>`
- Artifact kind: spec-qa
- Project/task identity: `<project>:<task-id>`
- Assessed source HEAD: `<40-hex-commit>`
- Assessed worktree digest: `<64-hex-digest>`
- Input artifacts: see table
- Verdict: `<PASS|FAIL>`
- Gate Decision: `<PASS|FAIL>`

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | specs/phase-3-<task-id>-specification.md | `<64-hex-sha256>` |

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
- QA subject: `specification readiness and correctness; not implementation code review`

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
| Spec contract complete | `<PASS|FAIL>` | | |
| Plan Quality Contract completeness | `<PASS|FAIL>` | | |
| Implementation Gate correct | `<PASS|FAIL>` | | |
| Architecture consistency | `<PASS|FAIL>` | | |
| Project-plan consistency | `<PASS|FAIL>` | | |
| Dependencies explicit | `<PASS|FAIL>` | | |
| No hidden decisions | `<PASS|FAIL>` | | |
| Tests and edge cases adequate | `<PASS|FAIL>` | | |

### Findings

- Blockers: `<none|resolved|list>`
- Unresolved findings: `<none|list>`

#### Critical Errors

- 

#### Warnings

- 

### Gate Decision

- Spec QA result: `<PASS|FAIL>`
- Can enter implementation: `<yes|no>`
- Required next phase: `<4. FAZA IMPLEMENTACJI|3.7. SPEC FIX LOOP>`

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

- Recommended: <GPT-5.6 Luna High|GPT-5.6 Sol High>
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
