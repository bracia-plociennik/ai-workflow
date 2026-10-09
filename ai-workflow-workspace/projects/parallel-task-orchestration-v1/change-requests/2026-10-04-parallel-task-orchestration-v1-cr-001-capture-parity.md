# PTO-CR-001-capture-parity

- Project: parallel-task-orchestration-v1
- Timing: pre-final-approval
- Type: defect
- Status: done
- Risk: high
- Owner request: unify historical/advisory capture validation and formal schema2 safety; use the supplied TechGrow handoff as advisory evidence.
- Approval source: decisions/pto-008-009-implementation-approval.md; decisions/pto-capability-scope-extension.md.
- Triage result: duplicated scoped validator ignores Capture schema and omits canonical collection/HEAD checks. Confirmed in upstream source; target counts/timing remain handoff testimony, not independently reproduced.
- Routing decision: new-task-in-active-plan
- Task: PTO-CAP-008-capture-parity
- Affected artifacts/files: capture-state.py, validation-scope.py, check-distillation-state, runtime-integrity tests and capture contracts; exact write set in the task specification.
- Evidence before done: all consumer paths agree for identical populations; schema1 is never current PASS by structural validity; schema2 remains strict; negative matrix, semantic/adversarial review, formal Phase5, Phase6, required checkpoint and fresh final check.
- Final check impact: prevents final-owner-yes until routed work is done and current final verification covers it.
- Post-final impact: not-applicable, owner has not closed PTO.
- Exclusions: no target/nested clone edits, history rewrites, schema downgrade, validator bypass, provider calls or automatic target update.
- Current disposition: implemented; formal Phase5 PASS and accepted Phase6. Final checkpoint008/009 completed; current nine-task technical final review is documented in reviews/pto-008-009-final-system-review.md and quality/phase-8-final-check.md. This does not grant final-owner-yes.
