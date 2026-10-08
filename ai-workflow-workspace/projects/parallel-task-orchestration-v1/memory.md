# Project Memory

PTO-002 accepted: allocation is a read-only proposal. Canonical path normalization
uses NFC before and after casefold; hardlinks and unsafe subtrees fail closed.
Capacity and checkpoint slots include all active work, not just selected units.
PTO-003 protocol consistency checks are accepted; actual native sandbox enforcement
remains unverified and separate from a JSON observation.

Planning decisions: decisions/owner-decisions.md.

## PTO-001 Accepted Contract Facts
Formal Quality: quality/phase-5-pto-core-001-contract-routing-quality.md.
Distillation: distillations/phase-6-pto-core-001-contract-routing-distillation.md.

One execution owner and one pool; units reference existing task/slice and do not
create phase chains. Packaging is optional. Accepted unit output is not task PASS.
Cross-task prerequisites retain Quality/capture/checkpoint gates. Count all active
worker capacity and distinct parent task slots before dispatch; unknown isolation
or capacity cannot enable parallel writes. Allocator and bounded protocol are now
implemented. The original lifecycle/integration deferral is historical; current
accepted facts follow below. Native capability remains unverified future work.

Policy scans need all consumers and both unsafe/prohibition clause orders.
Lexical regressions and green scripts are supporting evidence, not semantic QA.

## Memory Index
| Date | Topic | Type | Status | Route |
| --- | --- | --- | --- | --- |
| 2026-10-04 | Contract, allocation and submission boundaries | project-constraint | active | memory/2026-10-04-contract-allocation-protocol.md |
| 2026-10-04 | Serial integration and immutable copied inputs | project-constraint | active | distillations/phase-6-pto-qa-005-integration-acceptance-distillation.md |
| 2026-10-04 | Lifecycle, integration and protocol-only capability | project-constraint | active | memory/2026-10-04-lifecycle-integration-capability.md |
| 2026-10-04 | Capture parity and immutable commit proof | project-constraint | active | memory/2026-10-04-capture-parity-phase-commits.md |
| 2026-10-04 | Compatibility inspection without authority | project-constraint | active | memory/2026-10-04-compatibility-inspection.md |

## PTO-004..005 Accepted Facts
Lifecycle preserves single-writer revisions, immutable attempts and unknown-effect
reservations. Serial integration reserves a bounded destination, verifies actual
before/after and retains explicit recovery. Copied inputs cover the full relevant
producer namespace, including unchanged files, modes and deleted paths; extra
consumer entries fail. Before another integration, recheck prior destination and
review evidence so drift cannot become a baseline. Metadata is not parent QA PASS.
Sources: current PTO-004/005 Quality and Phase 6 artifacts. Native backend support
and actual write enforcement are unverified; PTO-006 permission remains separate.

## PTO-006 Accepted Protocol-Only Facts
Current formal Quality and Phase6 accepted schema2 opt-in, closed capability,
six-source consistency pins and template schema checks. Deep JSON returns unknown.
Default schema1 remains unchanged. Native operational support is deferred/unverified;
zero native calls and no model speedup claim. Synthetic paired timings are mixed.
Sources: current006Quality and its Phase6 record. The owning004..006checkpoint
completed before007; full006004 is historical after guidance source changes.

## PTO-007 Accepted Guidance And Handoff
All seven protocol tasks have actual formal Quality and Phase6. Guidance routes
to the canonical contract; one External Memory handoff is accepted for AI System
gap analysis. Native verification remains deferred/unverified and no counterpart
implementation is claimed. Final source full007 passed665seconds/43checks/745IDs.
Final checkpoint and technical Phase8 remain distinct from final-owner-yes.
Sources: current007Quality, its Phase6 and final checkpoint.

## PTO-008 Accepted Capture Facts
One shared capture-record assessment now serves inventory, scoped/runtime
validation and orchestration parent gates. Historical schema1 is structurally
valid without implying current QA. Schema2 completion binds owning implementation
QA, exact source artifact and unique accepted distillation. Invalid sibling claims
still count for duplicate detection. Nested Git evidence and ambiguous gates are
rejected. Source-backed tests and all five smoke groups passed; predecessor Quality
received a real regression assessment, not hash-only repair. Source008 is complete;
subsequent009 changes received fresh affected regression assessments before closure.
Sources: quality/phase-5-pto-cap-008-capture-parity-quality.md and
distillations/phase-6-pto-cap-008-capture-parity-distillation.md.

## PTO-009 Accepted Commit And QA Facts
Actual formal Quality and Phase6 are accepted; all sevenAC reviewed. The current
source full002 passes with757IDs. Future commit policy does not authorize current
publication. Complete immutable proof, raw Git history and all-input closing
checks are required for opt-in reuse; unsupported cases require fresh QA.
Detailed facts: memory/2026-10-04-capture-parity-phase-commits.md.
