# LOOP-003 Isolated Failure-Fix-Retest Eval

## Scope And Authority

- Work mode: supporting project eval, not LOOP-003 implementation or Spec QA.
- Owner request: plan and execute a local failure-fix-retest eval; no tracked source changes and no PR.
- Risk: low for the synthetic fixture; future policy edits remain high-risk and unapproved.
- Model: GPT-6 Sol High, previously approved for isolated local synthetic runs.
- Delivery constraint: owner opted out of deadline and timebox for this project; quality and stop rules remain.
- Allowed writes: this ignored eval namespace and one disposable local checkout under `/private/tmp`.
- Forbidden: tracked source, clients, secrets, external APIs, network writes, production, git commit/push, and changes outside the fixture.

## Implementation Slice Plan

| Slice | Goal | Files/areas | Acceptance check | Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| E1 | Freeze a deterministic two-defect synthetic fixture and eval protocol | `fixture/*.py`, this plan | Initial tests fail; `normalize_bounds` is seeded with an incorrect return order | Fixture hashes, initial test output | completed |
| E2 | Run one isolated current-router agent trial | Disposable checkout fixture only | Agent edits `clamp` first, runs tests, observes a post-edit failure, fixes local helper, reruns tests | JSONL trace, final message, changed files, test output | completed |
| E3 | Independently grade and review | Eval report | Verify actual command order and test results; report deviations and limits | Controller rerun, diff review, findings-first closure | completed |

Stop if the run requires external access, changes tracked source, skips a real safety gate, or cannot produce inspectable trace evidence. Do not reinterpret a green final test as proof that all future fix loops work.

## Fixture Contract

- `clamp(value, lower, upper)` must call `normalize_bounds` and return a bounded numeric value.
- `normalize_bounds(lower, upper)` must preserve valid bound order and reject `lower > upper` with `ValueError`.
- First implementation edit is restricted to `clamp`; run the complete local test suite immediately afterward. The deliberately seeded helper defect must remain until that test has exposed it.
- After the failure, the same agent may fix `normalize_bounds` within the fixture and must rerun the affected/full test suite before advisory closure.
- This staged restriction deliberately forces a post-edit failure. It measures persistence and correct routing through one synthetic fix loop, not spontaneous discovery of an unknown production bug.

## Plan Quality Contract

- Plan classification: implementation-capable, isolated fixture only.
- DoD source: owner request plus Fixture Contract above.
- Testable DoD / acceptance conditions: inspectable first edit, failing post-edit test, evidence-backed helper fix, passing retest, no out-of-scope files, findings-first advisory review.
- Artifact QA route: `global-quality-review-stance` for this eval plan and protocol.
- Artifact QA trigger: before running the isolated agent.
- Implementation Quality Closure route: `global-quality-review-stance` after the run.
- Required verification: initial and post-edit test output, trace command order, independent controller test, changed-files review, edge/failure paths, skipped checks and residual risk.
- Quality-ready criteria: actual failure-fix-retest sequence and no unresolved finding in the bounded fixture; otherwise report partial/failed eval, not formal PASS.
- Owner opt-out: none.
- Not-applicable reason: adaptive data/integration matrix is not applicable; pure local numerical functions with no external data or integration.
- Blocking decision: none for this supporting eval; LOOP-003 tracked implementation remains blocked by PE-003 and later approval.
- Next route: read-only decision review of LOOP-003 based on observed evidence.
