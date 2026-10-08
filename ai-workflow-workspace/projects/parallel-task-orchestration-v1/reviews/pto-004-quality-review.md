# PTO-004 Current-Diff Review
- Date: 2026-10-04
- Baseline: 8a0eeef, approved eight-path scope plus immediate consumers.
- Status: semantic and independent post-fix review complete; supporting full passed.
- Formal gate: eligible under decisions/pto-quality-range-approval.md.

## Intent And DoD
One coordinated execution pool; no scheduler, native dispatch, recursive worker,
automatic commit/reset or counterpart source write. AC1 closed transitions,
coordinator/revision/attempt identity; AC2 atomic state/revision/event and reserve
before dispatch; AC3 read-only actual-handle/file reconciliation; AC4 dependency
invalidation preserving accepted history and independent outputs; AC5 hash-bound
parent retry ceiling; AC6 exact sanitized active runtime inventory.

## Findings And Fix Loop
Independent reviewer found three material defects: checkpoint reset accepted
hash-only unfinished evidence (P1); damaged referenced results blocked even
read-only recovery (P2); missing result-directory fsync (P2). All corrected in
approved paths, then new regressions passed. Parent also corrected output-drift
reconciliation, nonempty parent completion, missing retry observations, foreign
runtime ancestors and hardlinked evidence before reading. A second review found
completed-parent invalidation left stale completion/slots eligible for checkpoint.
Fixed by returning affected parent slots to active, revoking completed gate refs
and rejecting completed parents with missing/unaccepted units. Added its actual
filesystem regression with gate adapter mocked valid. No clean verdict yet.
Final independent frozen-eight-path re-review found no remaining material finding.
It probed transitive parent-slot restoration, independent completion preservation,
immutable attempts and fourth-parent/checkpoint rejection. Parent complete current-diff
re-review agrees; this is semantic evidence, not automatic formal PASS.

## Producer-Consumer Audit
Allocator accepts null/absent lifecycle; persistent consumer requires closed schema.
Native observations -> preflight -> private attempt/stored hashes -> actual diff ->
sealed result -> semantic reviewer -> acceptance are separate. Canonical metadata
omits raw findings/absolute worker roots. Existing QA/capture readers remain the
only parent consumers. State-level positive checkpoint test mocks that adapter;
real fake-QA evidence fails closed. Actual owned-project consumers must also pass.
Checkpoint reset binds completed canonical metadata/gates and exact run, coordinator,
epoch, source and task set. Hash-only evidence is not completion. Result-dir fsync
precedes referencing manifest publication; power-loss behavior is not directly tested.

## Adversarial Matrix
| Boundary | Safe case | Unsafe case | Evidence |
| --- | --- | --- | --- |
| Mutation | current owner/revision | stale/foreign/extra keys | manifest unchanged negatives |
| CAS | single transaction | two competing processes | one committed revision/event |
| Crash | inspect committed state | replay uncertain acknowledgement | real exits before/after replace |
| Result | sealed matching record | duplicate/orphan/disclosure tamper | rejection/recovery cases |
| Retry | known stopped effects + parent budget | unknown/exhausted/missing observation | ceiling negatives |
| Checkpoint | current completed binding | unfinished/foreign epoch/task set | exact gate tests |
| Recovery | report damaged reference | trust damaged accepted evidence | explicit invalidation preserves bytes |
| Privacy | exact canonical records | raw log/link/foreign repo/hardlink | inventory negatives |

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Ready unit with preflight | running with attempt/reservations | private proof, no dispatch | running without reservation | reject | ready/start | ready -> freeze -> atomic state/event/slots |
| Exact stopped result | sealed submitted record | separate semantic acceptance | done equals task PASS | retain slots until review | submit/review | actual tree -> verify -> seal -> review |
| Crash before/after replace | complete old/new state | inspect, no replay | partial manifest or adopted orphan | retain evidence/lock | real crash, orphan, fsync order | result file+directory -> manifest replace -> ack |
| Unknown handle/effects | reserved parent | blocked reuse | silent cancellation/retry | retain slots | recovery negatives | observations -> actual diff -> unknown |
| Accepted output/result drift | history preserved | invalidation proposal/explicit block | stale acceptance usable | block dependents | drift/damage cases | hash comparison -> report -> explicit invalidation |
| Completed parent/checkpoint | existing QA/capture and owning bound checkpoint | count parents/reset epoch | unit results substitute gates | fail closed | adapter-positive + real negatives | readers -> count -> bound checkpoint |

## Checks And Freshness
25 planner +12 protocol +23 lifecycle pass; manifest audit 743 IDs, old742 once.
Actual owning PTO-003 QA/capture consumer invocation passed after fresh source
regression reassessments. Full attempt1 failed on runtime phase transition; corrected
in-progress routing without source changes. Attempt2 interrupted when new independent
finding arrived, before fixing source. Neither attempt is validation PASS evidence.
Full attempt3 rejected a pending capture record referring to a future missing
Quality report. Corrected it to none until the report exists; no source change.
Full attempt4 passed in 641 seconds, all five groups and 743 unique smoke IDs.
Receipt: /tmp/pto-004-full-source-004.json. Eight source hashes match the frozen
independently reviewed set. All AC1..AC6 are satisfied; no unresolved material
findings or blockers. Scripts remain supporting-only. No native operational or
model-speed claims. Recording this review does not change reviewed source.

## Residual Risk
Finite synthetic coverage; supplied observations are not native authentication.
Cooperative local locks cannot protect against a malicious host. Unsafe filesystem
recovery requires explicit owner action; never deletes stale locks. No commit/push.
