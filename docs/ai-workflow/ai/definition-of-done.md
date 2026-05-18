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
- QA evidence is attached in the project quality artifact;
- security-sensitive changes have required approval;
- rollback notes exist for production-impacting work.

## PASS Rule

`PASS` requires explicit evidence. A declaration without evidence is `FAIL`.

## FAIL Rule

Mark `FAIL` when any required criterion is missing, unverified, contradicted by repository state, or blocked by an unresolved decision.

Warnings do not override missing DoD, missing evidence, or failing checks.
