# PTO-001..004 Integration Regression Review

- Date: 2026-10-04
- Baseline: 8a0eeef, current approved PTO-001..005 source union.
- Scope: current predecessor AC and immediate consumers, not PTO-005 PASS.

## Genuine Current Source Reassessment

Read the unchanged accepted predecessor specs and current policy/allocator/
protocol/lifecycle sources, templates, owned runtime consumer and smoke manifest.
PTO-001 authority stays one execution owner with no recursive worker or default
phase bypass. PTO-002 allocator-only optional lifecycle remains valid and preserves
DAG/capacity/resource/task-slot semantics. PTO-003 origin/root/mode/input/diff/check
bindings still reject hidden writes and stale evidence. PTO-004 closed CAS schema
and immutable attempts remain intact; optional integrations strengthens parent
completion instead of accepting a worker verdict. Legacy parent completion without
integration is intentionally inadmissible for write units and requires actual
current integration evidence, not an old hash-only record.

25 planner, 12 protocol and 23 lifecycle tests passed after integration changes;
existing parent/checkpoint positives now include real temporary destination
integration before the mock formal-reader adapter. Existing fake-QA negative still
calls the real consumer and rejects. No source or test gate was weakened.
Same-task start now requires actual accepted producer and separately copied inputs;
cross-task start remains outside the bounded helper's support. Failure is conservative,
not a new formal approval mechanism. Checkpoint counts owning tasks and retains
partial-effect slots; unit/integration metadata never supplies Quality or capture.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Optional lifecycle allocator | compatible input | bounded read-only proposal | metadata grants execution | reject unknown authority | planner25 | DAG -> wave -> slots |
| Frozen result | actual provenance/diff/checks | submitted then reviewed | message becomes PASS | reject changed output | protocol12 | inventory -> checks -> review |
| Accepted write unit | verified destination plus existing parent gates | task completion only with both | no integration parent complete | fail closed | lifecycle23 + integration12 | accepted -> prepare -> external copy -> confirm -> existing readers |
| Unknown integration effects | reserved current state | no new dispatch/checkpoint | automatic release or rollback | retain record/slots | integration12 | pending -> drift -> blocked review |

## Limits
Post-fix source reassessment covers exact delivery coverage (including unchanged
owned outputs and deletion tombstones) and persisted target identity at parent/
checkpoint. These strengthen the stated predecessor bounds, not phase authority.
The further producer-consumer and serial-integration re-review checks extra copied
entries and prohibits laundering prior destination/review drift into a new
baseline. The shared current-integration reader is used at prepare and parent/
checkpoint without changing formal QA/capture consumers. All predecessor cases
and the 17 integration cases remain compatible. Historical
source assessments remain preserved; fresh full PTO-005 validation is still pending.

No material predecessor regression found in this semantic assessment. Historical
QA is preserved. Native runtime, adversarial host and model performance remain
unverified. Final full source gate003 subsequently passed (703seconds, five groups,
744 smoke IDs) with unchanged source after the genuine post-fix reviews above.
