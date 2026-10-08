# PTO-005 Current-Diff Review

- Date: 2026-10-04
- Baseline: 8a0eeef with approved PTO-001..005 union; exact nine-path PTO-005 scope.
- Review status: parent and independent post-fix semantic review complete; fresh full supporting gate passed.
- Formal gate eligibility: yes, all AC reviewed with current evidence and conditional high-risk owner approval.

## Intent And DoD
AC1 actual accepted worker provenance/diff/checks is reverified at integration.
AC2 start requires every same-task delivery, separately copied immutable input
hashes/modes/current producer; cross-task formal route is not implemented by helper.
AC3 CAS reserves serial integration before external effects and binds actual
bounded destination before/expected-after/observed-after; conflicts reject.
AC4 current common QA contracts require integrated consumers/failure/regression
review and real owning QA/capture readers. Verified metadata is not parent PASS.
AC5 completed/active parent slots remain at most three per checkpoint epoch;
partial/unknown integration does not release affected task slots or perform capture.

## Findings And Corrections
Parent review found optional dependency-copy verifier was not enforced at start.
Fixed closed start payload for every dependency and tested missing proof, stale
producer and changed copied modes. Directory mode review found the integration
root mode freeze rejected legitimate intended mode changes; actual before/after
inventory now controls modes while physical root identity remains unchanged.
Test-fixture failures were corrected without weakening assertions: refreshed
manifest objects must be mutated, and an uncertain post-replace OSError preserves
the committed reservation. No clean final verdict while independent/full pending.
Independent source review found P1 incomplete caller-selected delivery coverage
and P2 lost destination identity at later parent/checkpoint gates. Fixed both.
The frozen consumer contract now requires exact name-preserving coverage, including
unchanged owned files, directory modes and deletion tombstones. Counterfeit bytes
cannot hide behind an unrelated correct path. Persisted target inode identity is
checked again at parent/checkpoint. Full run 001 was controlled-interrupted (143,
199 seconds), not PASS evidence. Post-fix full current-state review is renewed.
The next independent review found P1 unaccepted extra consumer-directory entries
and P2 a later integration absorbing earlier destination drift. Both are fixed:
exact producer-owned/read namespace coverage rejects extra files and empty dirs;
prepare revalidates all prior current integration inventories, physical identities
and review hashes before freezing the next baseline. Real filesystem regressions
include legitimate serial A/B integration after rejecting destination/evidence
drift; unrelated input outside the producer namespace remains allowed. Full run
002 was controlled-interrupted (143, 380 seconds), not PASS. Fresh final review
and full source run are still required after these fixes.

## Producer-Consumer Audit
Unit/result/private preflight -> accepted_snapshot -> prepare -> persisted CAS
reservation -> separately permitted external integration -> actual inventory plus
review -> verified metadata -> existing parent QA/capture readers. No executor or
new transport. Template identity/baseline and semantic fields produce the exact
closed transition review; all flags are supplied assertions, not verification of
semantic reasoning. Shared helper optional integrations is read by lifecycle and
owned runtime inventory without raw worker logs/roots. Sealed result digests,
actual worker output, target scope/inode and actual integration review fingerprint
are independently bound. Copied dependencies cannot use a mutable producer path.

## Adversarial Matrix
| Boundary | Safe case | Unsafe case | Evidence |
| --- | --- | --- | --- |
| Provenance | accepted current sealed result | submitted/stale/tampered attempt | actual result/inventory negatives |
| Delivery | current same-task isolated copy | no payload, wrong mode, stale producer, cross-task | required start and delivery assertions |
| Integration | one reserved declared subtree | competing preparation, conflicting destination | CAS/proof/no-mutation tests |
| Partial effects | reviewed original-or-intended entries | unknown data or missing effects review | retains reservation, no rollback |
| Root/mode | same physical root and intended mode | replaced inode or unintended mode | actual filesystem negatives |
| Parent gate | verified integration plus real formal evidence | fake QA, destination regression, stale review | adapter not called on drift; real reader rejects fake QA |
| Policy | shared safe boundaries | existing unsafe compound claims | registered policy smoke suite |
| Directory namespace | exact accepted owned inputs | injected file or empty directory | actual consumer-start rejection; manifest unchanged |
| Sequential integration | current verified A then accepted B | B freezes corrupted A or stale A review | actual A/B prepare rejection; restored positive confirms |

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Accepted producer and separate copied consumer | bound current dependency at start | reserved consumer attempt | hash-only/mutable path start | reject missing/stale proofs | dependency delivery test | accepted result -> copy -> read-scope/preflight -> start |
| Current accepted output and conflict-free target | pending integration | private before/after proof, no effects | submitted integrated or automatic copy | fail before mutation | prepare/conflict tests | acceptance -> destination inventory -> reserve -> external copy |
| Expected actual target plus current review | verified integration metadata | eligibility for separate common QA | metadata becomes task PASS | existing parent reader required | integration/fake-QA test | whole target -> review -> confirm -> parent consumer |
| Unknown/partial integration | pending/blocked reservation | known reviewed abandonment only | rollback/retry or fourth parent | retain slots and preserve attempts | partial/crash/invalidation tests | partial write -> unknown reject -> explicit known review -> abandon |
| Deleted file/mode/unrelated entries | exact intended inventory | current source fingerprint | unnoticed extra write | reject unexpected differences | deletion/mode/root tests | actual delta -> freeze -> expected-after -> compare |
| Integrated regression/stale review | parent gate ineligible | fix/review route | unit tests substitute integrated QA | reject before parent completion | drift tests | verify metadata -> changed destination/review -> recheck -> reject |

## Review Completeness Gate
- Cross-contract consistency: aligned
- Risk/work mode compatibility: aligned, formal high-risk project
- Sources/permissions/phase gates/AC reviewed: yes
- Instruction refresh: performed-full after compaction; stage-specific current contracts
- Instruction baseline: current
- Negative-space/adversarial review: parent and independent completed
- Policy-boundary adversarial matrix: completed, documented review plus full negative smoke support
- Producer-consumer field audit: completed, mapping complete
- Automated evidence role: supporting-only
- Post-fix full re-review: parent and independent completed
- Closure freshness: current, source unchanged after the final reviewed fixes

## Checks And Limits
Targeted planner25, protocol12, lifecycle23 and integration17 passed; manifest
coverage verification passed with one new supplemental ID and no removed old IDs.
Current QA/status readers and quality/policy contracts passed targeted checks.
Full source gate 003 passed (exit 0, 703 seconds, smoke 663 seconds); all five
public groups passed. Authenticated source receipt: /tmp/pto-005-full-source-003.json.
Earlier pending statements above are historical fix-loop evidence, not current
gate eligibility. No native operational, model-speed, malicious-host
or power-loss guarantees; no commit, push, counterpart write or final-owner-yes.

## Independent Final Re-Review
Lagrange read all nine current paths and immediate QA/capture consumers after the
last fixes, found no new material findings and confirmed both correction pairs.
Reviewer helper fingerprint b406516efa9d; unchanged during probes. Actual parent
filesystem suites above are separate from the reviewer's in-memory mocked probes.
The reviewer did not perform full validation, native tests or issue formal PASS.
Disjoint producer scopes and outside-scope inputs remain supported; undocumented
shared producer namespaces fail closed. Cooperative observations cannot prove
native write enforcement or unknown external/transient effects.

## Final Decision
DoD AC1..AC5 and owner intent/plan/spec scope are aligned. No unresolved P0/P1 or
material P2 findings after parent and independent full-current-diff review.
All nine source paths remain frozen at the reviewed fingerprints. Supporting
full validation is not the semantic verdict; formal Quality uses the actual
review, AC coverage, current implementation result and recorded human approval.
