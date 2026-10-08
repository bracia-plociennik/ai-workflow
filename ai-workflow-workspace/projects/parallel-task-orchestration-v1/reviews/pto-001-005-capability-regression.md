# PTO-001..005 Capability Regression Review
- Date: 2026-10-04
- Baseline: 8a0eeef plus actual approved001..006source; PTO-D06 protocol-only scope
- Review: full current predecessor source/consumer comparison, not new implementation authority
- Changed shared surfaces: optional check-parallel capability consumer, coordinator explicit schema2 and synthetic test runner/smoke manifest
- Unchanged boundaries: single owner, dependencies, capacity/isolation requirements, actual-file verification, lifecycle/CAS/recovery, serial integration, current parent QA/capture and checkpoint ownership
- Actual regressions: planner25, protocol12, lifecycle23, integration17 and runtime46 passed; compatibility12 passed after correcting one Git-baseline fixture assertion and adding installed-hash/schema and nested-JSON negatives.
- Schema1 literal response fields/default/error behavior remain unchanged; runtime46 includes real QA reader, stale hashes/verdict/HEAD rejection and controlled errors
- No capability JSON grants execution permission or verifies native support; no old worker gate now consumes installed metadata as authentic backend proof
- Frozen674smokeIDs/regions and all prior supplementalIDs preserved; one new supplementalcompatibilitycase, publicfivegroups unchanged
- Producer-consumer audit: actual metadata with six pinned source hashes -> closed bounded reader -> checked template schemas -> optional output; original allocator/lifecycle/integration still need independent observed backend inputs and owner gates. No candidate code executes during discovery.
- Findings: no unresolved material predecessor regression in current semantic review
- Supporting full source validation: pending; earlier full005is historical after currentsourcechanges
- Residual risk: cooperative local controls, finite offline tests and unverified native runtime; no Phase8/commit/push inferred

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Optional installed metadata, explicit schema2 | installed protocol, native unverified | executionfalse and serial fallback | capability as approval or authentic capacity | no dispatch | compatibility10/runtime46 | actualCLI metadata -> output -> no authorizedexecution |
| Missing/stale/unsafe metadata or inputs | unknown/rejected | preserved history and boundaries | native support, silentretry, fakePASS | reject/fallback, retainworker reservations | predecessor77 pluscompatibility10 | malformedmetadata andaccepted-output drift traces |
