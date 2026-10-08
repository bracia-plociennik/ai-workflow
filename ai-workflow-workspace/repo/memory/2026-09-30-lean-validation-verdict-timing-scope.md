# Lean Validation Verdict, Timing And Scope

- Type: testing-note
- Scope: repo-wide
- Status: active
- Source: ai-workflow-lean-validation-v1 Phase 7 checkpoint, LV001-LV003 quality and distillations.

This official checkout contains local commits for verdict integrity, source-bound validation timing and explicit scoped dependency selection. The dedicated branch is not published by this checkpoint.

Validation evidence must distinguish process success, required coverage, source/runtime freshness and final eligibility. A scope manifest grants neither permission nor semantic QA. Full source gates retain all validators and smoke tests; no-argument validation remains standard.

Current source support: actual-runtime full run on the reviewed LV003 source passed in 637 seconds (smoke 595), forty checks and 674 unique smoke IDs. This is verification, not a measured speed gain. LV002's three earlier source-specific baselines remain immutable history.

Future smoke partition must preserve post-call assertions, fixture isolation, failure/timeout/interrupt and consumer contracts. See the active project and source files rather than inferring readiness from this memory.
