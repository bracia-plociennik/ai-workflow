# PTO-001..003 Lifecycle Regression Review
- Date: 2026-10-04
- Baseline: 8a0eeef plus approved PTO-001..004 source.
- Scope: actual predecessor re-review, not PTO-004 PASS.

## Reviewed Compatibility
Read current policy/router contracts, templates, allocator/preflight/result helper,
smoke wrapper/inventory and accepted PTO-001..003 specs. Optional null lifecycle
preserves allocation inputs. Unit origin, DoD/minimal context, root identity and
exact actual inventory remain intact. Foreign-root/hardlink checks strengthen safe
handling without new authority. Submitted stays separate from accepted.
25 planner and 12 protocol cases passed on current lifecycle source. Old 645-second
full remains historical after edits; fresh full required before PTO-004 Quality.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Legacy allocator input | optional lifecycle absent or empty | bounded proposal | metadata gives writes | no authority | planner25 | template -> DAG -> proposal |
| Frozen worker result | origin/root/input/diff bound | verified submission | replay/omission/task PASS | reject | protocol12 | preflight -> actual tree -> verify |
| Unsafe runtime evidence | inadmissible | controlled rejection | private alias ingested | fail closed | lifecycle safety cases | path metadata -> reject before read |

## Findings And Limits
No material predecessor regression found after full current-source re-review.
Earlier review/QA remains immutable history. Native operational evidence remains
separate. Scripts support, not replace, this intent/AC/consumer assessment.

Post-fix complete re-review also covered completed-parent invalidation and checkpoint
task-slot consistency; allocator/protocol APIs and all predecessor DoD remain intact.
