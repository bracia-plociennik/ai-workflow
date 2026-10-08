# PTO-001/002 Current Protocol Regression Review

- Date: 2026-10-04
- Baseline: HEAD 8a0eeef, actual PTO-003 additions; approved predecessor paths reviewed.
- All PTO-001 authority, routing, checkpoint and validator consumers remain aligned.
  New bounded protocol requires actual observed enforcement, never supplies authority,
  and verified submission remains distinct from acceptance and formal Quality.
- PTO-002 optional execution metadata accepts old allocator unit keys unchanged;
  strict execution schema applies only when non-null. No DAG/capacity/reservation
  algorithm or read-only planner output change. The result schema is separate.
- Shared supplemental core adds one protocol ID without replacing earlier IDs.
  Frozen 674 entries and five group boundaries stay unchanged. Manifest verified.
- Semantic current-diff review: DoD, owner intent, specs and all affected consumers
  checked; no material predecessor regression identified. Existing native/TOCTOU
  limits remain explicit, not proven by synthetic tests.
- Root-mode/device/inode drift now rejects before result inventory; restored-root
  positive control passes. Independent review confirms all three protocol fixes.
- Supporting tests: 25 planner + twelve protocol cases pass; contract validator and
  manifest audit pass. Full current-source run passed in 645 seconds, exit 0,
  all five groups and 742 smoke IDs. Earlier 656-second full is historical.
- Formal high-risk owner approval: original PTO-001 approval and new PTO-002..007
  conditional range approval. The reassessment preserves original history.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| legacy allocator unit | exact retained schema semantics | same deterministic proposal | new permission or hard-coded worker cap | reject unsafe inputs | 25 planner cases | old template -> validate -> plan |
| optional execution and bounded workspace | frozen minimal inputs and actual diff | verified submission only | promoted worker PASS or extra writes | reject | twelve protocol cases | preflight inventory -> actual files -> verify_result |
| shared smoke addition | old tests unchanged plus unique protocol ID | five-group coverage | duplicate/lost frozen ID | fail manifest check | manifest verification | supplemental ID -> ownership -> command contract |

## Review Completeness Gate
- Status: complete for current predecessor regression review
- Closure freshness: current after protocol source corrections
- Policy-boundary adversarial matrix: original 37 cases retained; contract checker passed
- Producer-consumer field audit: optional execution/legacy unit, run/result and smoke wiring reviewed
- Post-fix full re-review: completed for predecessor paths, not future PTO-004 interfaces
- Automated evidence role: supporting-only
- Residual risk: finite coverage, native backend and hostile concurrent host not verified
