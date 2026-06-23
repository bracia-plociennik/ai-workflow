# definition-of-done.md

## Task Done Criteria

A task is done only when all applicable items are true:

- implementation matches the accepted spec or approved task instruction;
- all in-scope acceptance criteria are satisfied;
- tests were added or explicitly deemed unnecessary with reason;
- relevant tests passed;
- lint, typecheck, static analysis, or build passed when configured;
- skipped checks are recorded with reason and impact on `PASS`;
- no known bug remains in scope;
- no unrelated files changed;
- status files are updated;
- decision log is updated when assumptions changed;
- contract compliance and knowledge capture decisions are stated before commit or handoff;
- end-of-task capture decision is stated when the owner explicitly ends the task and asks to preserve learnings;
- each completed workflow phase artifact records its optional knowledge capture decision when that phase template applies;
- QA evidence is attached in the project quality artifact;
- security-sensitive changes have required approval;
- rollback notes exist for production-impacting work.

## PASS Rule

`PASS` requires explicit evidence. A declaration without evidence is `FAIL`.

## Commit Readiness

Before commit or handoff, apply `.systems/ai/core/contract-compliance.md`.

The commit readiness decision must state:

- `Work mode compliance: pass|warning|blocked`;
- `Knowledge capture: required|not-required`;
- capture target and reason.

This is advisory-only for git commits, but it does not weaken phase gates, risk approvals, status updates, QA evidence, distillation, checkpoint, or memory requirements when those are otherwise required.

Phase-level `Optional Knowledge Capture` is also advisory. A `no`, `none`, `reject`, `defer-to-distillation`, or `defer-to-checkpoint` decision can be sufficient when supported by the phase evidence.

End-of-Task Capture from `.systems/ai/core/end-of-task-capture.md` is also advisory unless the owner explicitly approves durable capture and the target, scope, privacy, evidence, and write permission are clear. It cannot mark `PASS`, close a project, run final check, or replace required distillation/checkpoint.

## FAIL Rule

Mark `FAIL` when any required criterion is missing, unverified, contradicted by repository state, or blocked by an unresolved decision.

Warnings do not override missing DoD, missing evidence, or failing checks.
