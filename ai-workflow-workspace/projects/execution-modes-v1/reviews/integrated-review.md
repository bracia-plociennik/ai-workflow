# Integrated Current-Diff Review
- Baseline: a9a5c40430af3dec153df94f8b78a30f668bbde3 plus the complete owned diff on codex/execution-modes-v1.
- Instruction refresh: performed-full after continuity transition; AGENTS, execution modes, approvals, autopilot, risk, delivery, quality, commit and capture contracts.
- Owner intent: autonomous approved work with minimal interaction, no permission inflation and honest partial completion.
- Accepted plan/spec: five slices; high risk, isolated upstream, no deadline/timebox, one counterpart handoff, no push/merge/final-owner-yes.
- DoD fit: modes/routing, independent subset, saved scope/source, no hidden timebox, actual QA, phase/Git boundaries and validator coverage reviewed.
- Findings: corrected during review, not hidden by green scripts. No unresolved P0/P1/material P2 in current owned scope.
- Changed-files review: all core integration paragraphs, changed decision/autopilot/delivery clauses, state/readiness/status/decision producers, pure inspector/tests, policy validator, required/check registry/smoke membership, documentation and changelog.
- Negative space: model behavior and true native isolation are not established by declared JSON or synthetic tests. Scope does not add a runtime dispatcher or AI System implementation.
- Post-fix full re-review: completed after action allowlist, high-impact approval references, invalid-mode rejection, required write/resource declarations, Auto queue wording, unit-local AGENTS stop/write conditions and prompt-variable integration corrections. Final source diff is frozen as implementation/source-frozen.patch.
- Automation role: supporting-only; full validation pending at time of this review.
- Final parser re-review: persisted execution.mode must be an explicit auto/human-coop string. Null is valid only as an absent optional resolver argument, never as a persisted mode. Corrected the producer-consumer distinction and verified 28 offline tests including five malformed mode cases; prior full snapshots remain superseded evidence.

## Adversarial Policy Matrix
| Boundary | Enabling attack | Expected rejection | Evidence |
| --- | --- | --- | --- |
| Mode authority | Auto may bypass QA/approval | reject regardless of neighboring prohibition | direct and seven separator smoke cases |
| Premature completion | completed with incomplete DoD | reject | policy smoke and requested completed state tests |
| Plan-only | approved local/product-write | reject | action allowlist tests |
| Scoped approval | new production action or missing scoped high-impact ref | block/reject | approved-actions subset and refs tests |
| Readiness | pending owner decision, unknown deps/isolation, shared case/path alias | exclude all affected units | graph/transitive/resource tests |
| Historical mode | missing execution field | no new autonomy | legacy malformed projection test and nonretroactive contract |
| Resume | previously selected Human Coop | retain | resolver tests; actual coordinator must verify session identity |
| Final closure | implicit final check or final-owner-yes flag | reject | explicit reference and owner-yes tests |
| Input safety | duplicate JSON field or symlink | reject without writes | CLI tests |

## Producer-Consumer Audit
| Producer | Fields | Consumer | Result |
| --- | --- | --- | --- |
| Project status | mode, scope, scope ID, source | mode selection/refresh | aligned; historical missing fields retain old authority |
| Readiness/state | execution separate from autopilot.mode, refs, subsets, blocked/completed/pending | coordinator, policy validator | aligned; declarations require real evidence |
| Task/readiness decisions | disposition, affected units, assumptions, override impacts; existing full queue fields | owner report and dependency gating | aligned |
| JSON readiness | exact schema/work kind/actions/baseline/resources/decision fields | pure inspector and offline tests | aligned; inspection-only |
| Full response | mode, scope/source, choices/override, blocked/pending | owner transparency | aligned |
| Check registry/required/smoke | executable new paths and sixteen supplemental IDs | full validator/fixture runner | aligned; original coverage unchanged |

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Test/Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Auto, covered reversible choice | recorded agent-choice | ready subset | critical/missing facts chosen | reject | offline decisions tests | choice retains high-impact and actual approval verification |
| D blocks U1; U2 disjoint; U3 depends on U1 | U1/U3 blocked | U2 ready | U1 or U3 dispatched | conservative graph block | independent subset test | D -> U1 -> U3; resource claim also blocks neighbors |
| Drifted baseline or unapproved action | unit blocked | no false completion | stale QA or lowered DoD | nonready/reject completed | baseline/approval/completion tests | requested completed cannot erase missing gates |
| Planning action local-write | invalid projection | no readiness | product implementation from plan | diagnostic nonzero | action tests | planning allows only artifact-write/formal-quality/local-commit |
| CLI linked or duplicate-key input | invalid input | no state mutation | hidden override or symlink source | diagnostic nonzero | CLI regressions | parse rejects before readiness result |
