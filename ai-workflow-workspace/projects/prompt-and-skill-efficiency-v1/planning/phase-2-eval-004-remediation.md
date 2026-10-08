# Phase 2 Plan Addendum: PSE-FIX-004 Discovery And Eval Integrity

## Scope And Source

- Owner instruction: adversarially review Eval 004, then plan and implement fixes for its findings.
- Source evidence: `evals/skill-discovery-routine-004/result.md`, `reviews/2026-09-28-eval-004-adversarial-review.md`, current contracts and script code.
- Work mode: formal task in `prompt-and-skill-efficiency-v1`; risk `high`; PE-012 records owner implementation approval.
- Deadline/timebox: owner-approved no-deadline/no-timebox decision for this project still applies. It does not relax QA, DoD, evidence or stop conditions.
- Must-have: stop routine full reads of irrelevant skill bodies without losing required activation, and stop changed graded eval plans before stale evidence can be aggregated.
- Out of scope: edits to active `skill-creator/SKILL.md`, P3 context-route candidate, client/target repositories, CI policy, model defaults, Phase 8, commit and push.

## Exact Tracked Write Set

1. `AGENTS.md`: metadata-first skill discovery route.
2. `.systems/ai/core/operating-model.md`: canonical two-stage discovery contract.
3. `.systems/scripts/check-phase-skill-discovery`: static contract guard.
4. `.systems/ai/skills/skill-creator/scripts/run_eval.py`: pre-write compatibility guard for graded run reuse.
5. `.systems/scripts/test-skill-eval-freshness`: focused synthetic regression tests.
6. `.systems/scripts/check-validator-smoke-tests`: negative/positive policy and freshness smoke integration.

No other tracked path is approved by this plan. A need to edit `run_loop.py`, `aggregate_benchmark.py` or active skill text requires an amendment, new QA and owner decision before that write.

## Implementation Slice Plan

| Slice ID | Goal | Expected files/areas | Acceptance check | Evidence required | Status |
| --- | --- | --- | --- | --- | --- |
| S1 | Select skills from frontmatter before loading body | `AGENTS.md`, operating model, discovery validator/smoke | 3 negative synthetic cases avoid full irrelevant `SKILL.md`; positive control loads active skill | Tool-open traces, validator negative/positive tests | planned |
| S2 | Prevent stale grades on changed eval plan | `run_eval.py`, focused test, smoke integration | Changed graded run fails before mutation; unchanged graded run succeeds; ungraded overwrite remains allowed; orphan grades fail | Runtime tests, pre/post file hash checks, error messages | planned |
| S3 | Integration and quality closure | approved files only | semantic current-diff review, targeted checks, fresh behavioral eval, full validation after semantic QA | findings-first Phase 5 evidence and residual risk | planned |

Stop if a slice requires new file ownership, destructive deletion, broader safety authority, or unresolved approval. A slice plan does not grant write permission or PASS.

## Dependencies And Failure Paths

- S1 depends on current CORE-001 conditional router and `Phase Skill Discovery` ordering; workspace skills still precede system skills.
- S2 depends on current `run_eval.py --overwrite` and `aggregate_benchmark.py` formats. Keep existing grades intact, reject incompatible reuse, and avoid partial rewrites on rejection.
- Repeated model runs are directional. If docs/validator changes do not improve actual tool-open behavior, Phase 5 must not PASS this DoD; route to a fix loop rather than declaring success from text checks.
- If an existing graded plan lacks metadata or contains orphan grading files, fail closed with an actionable message; do not delete or silently ignore evidence.

## Plan Quality Contract

- Plan classification: `implementation-capable`; implementation writes planned: yes, exact files above.
- DoD source: owner instruction and confirmed Eval 004 findings.
- Testable DoD / acceptance conditions: 3/3 routine negative cases avoid full irrelevant skill-body read and select no skill; positive skill review reads relevant body; changed graded eval plan fails before any run artifact change; same-plan graded rerun and ungraded changed-plan overwrite remain supported; orphan grade fails.
- Artifact QA route: `phase-2-plan-qa` for this addendum and task index, then `phase-3-spec-qa` for the detailed task spec.
- Artifact QA trigger: before tracked source write.
- Implementation Quality Closure route: formal `phase-5-quality` after both slices.
- Required verification: focused Python tests, discovery validator and smoke negatives, actual read-only GPT-6 Sol High synthetic eval, changed-files review, edge/failure-path review, and applicable full workflow validation after semantic QA. Adaptive data/integration matrix: not-applicable to product data; producer-consumer eval metadata/grading audit is required.
- Quality-ready criteria: no unresolved P0/P1/material P2, all acceptance checks met with tool-open and file-hash evidence.
- Owner opt-out: none.
- Not-applicable reason: no product data/model migration; evidence integrity is handled as producer-consumer rather than product data matrix.
- Blocking decision: none for this bounded owner-approved write set; any expansion needs a new PE decision.
- Next route: `phase-2-plan-qa`, then specification and Spec QA.

## Knowledge Capture Decision

- Capture candidate: project memory after formal quality/distillation; no ad hoc System Insight, External Memory, commit or push during implementation.
