# Decision: PE-005 LOOP-003 Planning Re-Entry

## Date

`2026-09-28`

## Status

`approved` for planning and artifact QA only

## Classification

`high-impact`

## Context

- PE-003 deferred LOOP-003 until the CORE-001 paired result and a separate owner decision. CORE-001 has since completed Phase 7 and its paired quality evidence is recorded.
- Four isolated LOOP-003 evals found directed recovery, a preemptive fix without a failure, safe recovery of a documented runtime fault, and a legitimate stop at an owner-controlled state boundary. None found an early-stop defect.
- The current contracts require implementation checks and quality closure, but do not explicitly describe the in-scope test-inspect-fix-retest route for a failure discovered during implementation before formal Phase 5. Phase 4 also says not to enter the formal fix loop directly.

## Owner Decision

- The owner explicitly lifted PE-003 deferral for LOOP-003 and requested a contract-gap audit, amended project plan, Plan QA, specification and Spec QA, with no tracked source changes.
- This decision does not lift PE-003 for SKILL-002.
- This decision does not approve any tracked policy, validator, template or smoke-test edit; an exact write-set decision remains required before high-risk implementation.

## Consequences

- LOOP-003 may enter a separate planning/specification tranche as `conditional`.
- Its defensible need is contract clarity, not a claimed observed behavioral defect. Candidate implementation must remain optional until the specification and owner approval make its value and scope explicit.
- Formal Phase 5, negative-safety evidence, source-of-truth, risk, permissions, DoD, approvals and existing fix-loop semantics remain unchanged.
