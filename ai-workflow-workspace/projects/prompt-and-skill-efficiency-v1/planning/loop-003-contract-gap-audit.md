# LOOP-003 Contract Gap Audit

## Question

Do current AI Workflow contracts unambiguously route a local test failure discovered after authorized implementation, before formal quality closure?

## Current Coverage

| Source | What it already requires | Remaining ambiguity |
| --- | --- | --- |
| `.systems/ai/core/implementation-slicing.md` | Testable DoD, slice acceptance checks, evidence, mandatory quality closure and fresh post-fix review | No explicit decision sequence for a failing local check before the first quality review: inspect, repair only within accepted scope, retest, or stop |
| `.systems/ai/workflow/phase-4-implementation.md` | Tests from the spec, strict scope, evidence and transition to Phase 5 | Says not to go directly to the formal fix loop and allows only bounded minor corrections, but does not distinguish an in-spec implementation correction from a new-scope fix after a local failure |
| `.systems/ai/core/quality-review.md` and `phase-5-quality.md` | Findings-first quality closure, DoD fit, no false PASS; post-review fixes make closure stale | They govern the formal/advisory review boundary, not the first local failure while Phase 4 is still being executed |
| `.systems/ai/workflow/phase-5-fix-loop.md` | Formal repair after Phase 5 FAIL, with later quality rerun | It is not the route for an in-scope correction before the first Phase 5 verdict |

## Behavioral Evidence

- `evals/loop-003-failure-fix-retest/result.md`: agent followed an explicitly instructed fix/retest sequence.
- `evals/loop-003-blind-001/result.md`: agent fixed a defect before a failing test; persistence branch untested.
- `evals/loop-003-runtime-fault-001/result.md`: safe repair of one documented synthetic runtime fault.
- `evals/loop-003-negative-boundary-001/result.md`: legitimate stop when a green suite required owner-controlled state outside the allowed write set.
- No eval demonstrated a natural early-stop bug. Do not claim behavioral regression or quantified improvement.

## Defensible Narrow Need

Define the local pre-quality failure decision explicitly: inspect the failing check; if the defect is within the accepted spec/prompt, current write set, safe environment and permissions, correct it and rerun the affected check plus required regression checks; otherwise stop and report the exact gate. Repeat only with a new evidence-backed hypothesis and progress, never to chase green tests by changing tests or protected state. This clarifies existing authority rather than expanding it.

## Scope And Decision

- Proposed tracked write set for a later owner decision: `.systems/ai/core/implementation-slicing.md`, `.systems/ai/workflow/phase-4-implementation.md`, `.systems/scripts/check-implementation-slicing`, `.systems/scripts/check-validator-smoke-tests`.
- No tracked writes are authorized by this audit, PE-005, Plan QA or Spec QA.
- If a full Spec QA finds this merely restates existing rules without a testable clarity gain, reject or defer the source change rather than manufacture an early-stop finding.
