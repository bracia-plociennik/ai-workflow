# PTO-CR-002-phase-commits

- Project: parallel-task-orchestration-v1
- Timing: pre-final-approval
- Type: scope-add
- Status: done
- Risk: high
- Owner request: default planning/Phase6/Phase7 local commits, Phase8 closure commit after final-owner-yes, dedicated branches for substantive projects.
- Approval source: decisions/pto-008-009-implementation-approval.md; decisions/pto-capability-scope-extension.md.
- Triage result: useful delivery boundary, conditioned on tracked publishable changes and current QA; cannot commit ignored workspace or retroactively authorize current PTO publication.
- Routing decision: new-task-in-active-plan
- Task: PTO-GIT-009-phase-commits
- Affected artifacts/files: autopilot/phase/permission guidance and quality/capture producers/consumers; exact write set in the task specification.
- Dependency: PTO-CAP-008-capture-parity through its required Quality/capture gates.
- Evidence before done: bounded commit policy, no-question/opt-out/worker boundaries, post-commit equivalence and tamper tests, formal Phase5, Phase6/checkpoint and fresh Phase8.
- Final check impact: prevents final-owner-yes; technical Phase8 and owner acceptance remain distinct.
- Post-final impact: not-applicable.
- Exclusions: push/merge/PR automation, empty commits, forced workspace publication, native backend work and target updates.
- Current disposition: implemented; actual formal Quality PASS, accepted Phase6 and final checkpoint008/009. Current nine-task technical final review is documented in reviews/pto-008-009-final-system-review.md and quality/phase-8-final-check.md, without final-owner-yes. Existing no-commit instruction remains in force.
