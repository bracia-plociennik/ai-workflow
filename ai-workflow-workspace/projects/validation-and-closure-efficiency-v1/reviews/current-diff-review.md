# Current Diff Review

Scope: EFF-001 through EFF-007, high-risk upstream workflow maintenance. Owner-authorized implementation and technical Phase 8; no deadline/timebox, handoff, commit/push or final-owner-yes. Review precedes final scripts. Scripts cannot supply semantic PASS.

## Intent / Plan / Spec Compliance

Aligned with seven accepted specifications. No management checkout, nested clone, product/client data, remote effect or global settings changed. Existing project mode and risk classes remain intact. Capabilities have explicit boundaries rather than implicit cache/skip flags.

## Findings And Fix Evidence

Resolved during implementation: macOS platform path aliases falsely rejected temporary outputs; Bash 3.2 empty-array expansion prevented public execution; runtime inventory omitted the history registry; producer used a raw substring for owner decision; refresh lacked live HEAD comparison. Each now has behavioral or public-interface regression coverage. Runtime task router was corrected to canonical IDs and root-relative paths without changing accepted specs or rewriting QA.

## Adversarial Matrix

| Boundary | Forbidden state | Evidence |
| --- | --- | --- |
| Reuse | forged, failed, timeout, interrupted or incomplete success | unit tests verify authentication and successful state; changed binding executes fresh |
| Applicability | iteration result impersonates full/CI or arbitrary command | fixed registry/dependencies, CI/full rejection, non-final output |
| Process lifecycle | success marker before actual execution | public shell test requires output, executed check and exactly one completion; real integration fresh/reuse/tamper |
| History | old PASS supplies current gate; live source rewrite | checksum-bound explicit admission, integrity-only path and current consumer rejection, including combined flags |
| Quality producer | generated findings/approval, injected headings, overwrite | all six QA kinds roundtrip supplied sections; missing evidence rejects; atomic no-clobber |
| Owner approval | technical final check closes project or approves owner | awaiting-only technical producer; separate matching owning decision and current final-check hashes |
| Output privacy | linked/traversal/sensitive paths or public evidence | canonical containment, safe output and owner-only explicit keys |
| Bounded defect | high/unknown impact or medium risk becomes micro | strict eligibility with unchanged formal modes and approvals |
| Refresh | stale scope/approval/HEAD silently continues | authority hashes, live HEAD and required full refresh after compaction |
| Timing | sums overlapping intervals or pretends model telemetry | union of observed intervals, estimates excluded, unmeasured phases explicit |

## Producer-Consumer Audit

| Producer | Consumer | Required mapping |
| --- | --- | --- |
| full runner source-start/finish | verify-source/artifact-closure | complete registered checks, whole source/tool/env digest, HMAC, state/exit |
| execution plan | validate-workflow/execute_plan | fixed IDs, applicability, inputs, dependency closure, reason and non-final coverage |
| supplied reviewer JSON | quality-record / qa-evidence / status-consistency | canonical filenames, identities, current sections and bound input digests |
| quality-assessments registry | qa-evidence and runtime inventory | report/decision checksums, explicit admission/state, no current PASS |
| owner decision record | separate owner-approval consumer | exact scope, source, final-owner-yes and current final check |
| process intervals | timing summary | monotonic, finite, observed vs estimated, overlap union |
| opened-source snapshot | refresh | scope/stage/repository/HEAD/contracts/authority inputs; no write permission |

## Failure And Regression Review

Post-fix review: the first full attempt failed in an isolated non-Git smoke fixture because the newly added policy validator also ran Git-dependent behavioral tests. The default validator now checks policy/structure only; full smoke explicitly executes all behavioral tests from the real source root. No behavioral coverage was removed. Additional real EXIT-trap regression tests confirm receipt-write failures preserve original failure/timeout/interrupt exit codes. Existing receipt destinations reject before any expensive validator. New JSON templates are required artifacts. Twenty-eight behavioral tests and the live smoke manifest pass after these fixes. The failed full attempt is immutable evidence, not a quality PASS.

CI ambient-state review exposed that isolated iteration unit probes inherited CI=true and therefore hit the intentional production no-reuse gate. Synthetic probes now explicitly clear CI inside their disposable test scope, while the dedicated CI rejection test overrides it back to true. The enclosing validator still has CI=true and executes fresh full validation. Twenty-eight tests pass with outer CI=true. The obsolete in-progress full run was interrupted with exit 143; its receipt is failed, not reused. A new full run on the final source with CI=true is the final gate candidate.

Final input/failure audit: key opening could block on a FIFO before fstat rejected the non-regular file. O_NONBLOCK now makes that opening bounded, while regular owner-only file checks and minimum key length remain intact. A disposable FIFO probe with a two-second subprocess bound confirms immediate rejection without a writer. Twenty-nine tests pass with outer CI=true. The previous source run was interrupted, retained as non-final evidence and is never reused. All changed and new source was reread after the final key/test change; no unresolved P0/P1/material P2 identified. The final full run begins only after this semantic review.

Fresh full CI/updater remains mandatory. Source/environment drift invalidates source-backed artifact closure. New output and explicit key required; no global cache. Unknown coverage does not become final evidence. History bytes remain immutable. Public CLI was tested separately from internal helpers to catch orchestration bugs. Existing 700 smoke IDs, 674 frozen reference IDs and audited assertions remain; three supplemental tests added.

## Measurement

Three baseline/candidate samples per scenario retain the same four assertions. Synthetic medians: bounded defect 49.49 vs 110.16 ms; runtime-only 49.88 vs 113.29 ms; changed source 55.96 vs 152.79 ms. Result: no synthetic wall-time improvement for cheap checks; authentication/publication overhead dominates. Two unchanged cases reduce executions from two to one; changed-source case executes both. Real public interface: fresh 0.549 s, reused 0.469 s; one sample, not a benchmark. No whole-agent speedup claim.

## Review Completeness Gate

- Status: complete
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Required-field mapping: complete
- Post-fix full re-review: completed
- Reviewed baseline: a758bb4 plus current tracked and new source diff
- Closure freshness: current at this review; final source/runtime checks pending
- Instruction refresh: performed-full after compaction; AGENTS, source/diff, accepted project plan/specs and active quality/capture contracts reviewed
- Blockers: none identified in semantic review
- Unresolved findings: none
- Skipped/unreadable areas: no AI System or client data analysis; model/production performance not measured
- Residual risk: explicit keys and applicability declarations depend on local integrity; conservative allowlist may provide little benefit for cheap checks. Current full validation completed after the final source edit: 703 smoke IDs, 29 behavioral tests, exit 0, one completion marker. Source receipt independently verified in the same resolved Bash environment. Standalone invocation from a different shell environment invalidates reuse conservatively; use the same recorded executing context or run fresh. No whole-agent speedup claim.
