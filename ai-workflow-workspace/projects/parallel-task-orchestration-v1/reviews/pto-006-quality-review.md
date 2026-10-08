# PTO-006 Current-Diff Quality Review

- Date: 2026-10-04
- Reviewed baseline: 8a0eeef, approved eight PTO-006 paths and immediate PTO-001..005 consumers.
- Scope source: revised six AC, PTO-D06 protocol-only decision, current Plan/Spec QA.
- Owner intent: release safe installed protocol discovery, not an unverified worker backend.
- Findings-first: two material P2 from independent source review fixed before quality acceptance.
- P2 installed source mismatch: closed six-path SHA-256 map binds actual source bytes; JSON templates and nested units also require schema 1. Candidate source is never imported/executed by discovery.
- P2 deep JSON: bounded parser recursion failure gives generic unknown/serial; actual helper and CLI negative tests pass without traceback or input disclosure.
- Post-fix independent review: completed, no remaining material findings in all eight paths and immediate predecessors. All six pinned hashes match; native/authority separation and old smoke IDs retained. Reviewer performed no writes, workers or tests; parent actual test evidence remains distinct.
- Required source validation: first run failed after five seconds on a runtime phase router (phase4 in-progress cannot route to phase5). Source evidence remains incomplete; update Phase4 completion truthfully, then rerun full. No green result inferred.
- Runtime follow-up: run002 correctly rejected stale Architecture QA; genuine prerequisite re-review and nine schema-produced current assessments preserved history. Run003 rejected the missing derived false boolean in pending-quality capture state; canonical State Evidence was completed without changing its pending state. These are failed runs, not reused full evidence.
- Final supporting source validation: run004 passed exit0 in694seconds;43checks, five public groups and745unique smoke IDs. Authenticated source receipt /tmp/pto-006-full-source-004.json; source bdee89499b5158bac1e6edc42f12272fa26dcc2b153bdefa5f9c566cd91d8dd0. The pending capture had no Quality artifact before actual formal acceptance; unknown/missing pointer was corrected to none, not a fake assessment.
- Final current-diff review: both P2 fixes remain in the frozen source, all six AC aligned; no unresolved P0/P1/material P2. Conditional high-risk human approval applies to this revised gate. No native support or permission inferred.

## DoD And Compliance
| AC | Actual evidence |
| --- | --- |
| AC1 | Default and explicit schema1 exact shape; schema2 adds only optional conservative capability. Real CLI/no-write tests and runtime46 passed. |
| AC2 | Installed metadata separates native unverified, capacity unknown, permission not-assessed; all execution flags false. |
| AC3 | Missing/malformed/duplicate/deep JSON, links, hardlinks, oversize, unknown versions, source mismatch and schema mismatch return unknown/serial; source drift during read rejects output. |
| AC4 | Planner25/protocol12/lifecycle23/integration17 actual filesystem regressions retained; old smoke inventory preserved, new compatibility ID unique. |
| AC5 | Three paired identical payload/assertion offline threaded samples include setup/integration/verification/cleanup totals, zero rework/conflicts in success cases; failure paths separately exercised. Mixed timings, no speedup/native/model claim. |
| AC6 | Native preflight failed isolation before any worker call. Native verification deferred by PTO-D06, unverified and no dispatch; no weakened safety or fake evidence. |

## Adversarial And Producer-Consumer Audit
| Boundary | Negative case | Required result | Evidence |
| --- | --- | --- | --- |
| Capability authority | forged isolation/capacity/owner permission | unknown, no execution | compatibility12 |
| Installed consistency | changed code/template, rehashed schema2 or invalid JSON | unknown, no candidate execution | actual source mismatch tests |
| Parser resource limit | 4001-byte deep JSON | generic unknown without traceback | helper and real CLI tests |
| Read safety | link/hardlink/missing/oversize/changed input | unknown or controlled rejection | compatibility12 |
| Schema compatibility | schema1 default and schema2 opt-in | same legacy fields and independent QA semantics | compatibility12 + runtime46 |
| Dispatch | unknown isolation/capacity | serial, execution false | allocator and compatibility tests |
| Benchmark | threaded file work called native/model speed | claim prohibited, evidence labelled offline only | manual sample/result trace |

Source fingerprint checks are consistency, not authenticity signatures. Metadata
cannot attest native isolation, capacity, owner permission or change parent QA.
Manual success trace: real source bytes -> matching local hashes -> schema checks
-> optional coordinator metadata -> execution false. Failure trace: changed unit
schema or deep JSON -> conservative unknown -> ordinary serial route, no worker.
Known residual risk: finite synthetic tests and cooperative local controls; native
backend still unavailable. No deadline/timebox, commit, push or final-owner-yes.

## Adaptive Data / Integration Verification Matrix
| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Matching installed bytes/schema and explicit v2 | installed protocol only | unverified backend, execution false | metadata as native permission/support | no dispatch | compatibility12/runtime46 | bytes -> hashes -> schema -> optional output |
| Missing, altered, malformed or deep input | unknown | serial fallback | traceback, leaked input, fake compatible protocol | conservative fallback | source/schema/deep CLI negatives | bad input -> unknown -> serial |
| Input drifts during coordinator read | rejected snapshot | controlled failure | mixed-baseline output | reject | patched actual filesystem drift | first read -> change -> second read -> rejection |
| Same synthetic work sequential/threaded | same canonical output digest | honest total/integration/conflict report | native/model acceleration claim | retain no-improvement samples | three paired offline samples | source payload -> local work -> serial integration -> checks |
