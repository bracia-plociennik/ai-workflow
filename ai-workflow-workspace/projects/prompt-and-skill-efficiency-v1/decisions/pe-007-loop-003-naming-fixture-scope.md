# Decision: PE-007 LOOP-003 Frozen Eval Naming Scope

## Date

`2026-09-28`

## Status

`approved` for a narrow fifth tracked file and smoke coverage, conditional on amended Spec QA and pre-write readiness

## Classification

`high-impact`

## Context

- PE-006 approved exactly four LOOP-003 tracked files. Their source work and targeted smoke suite completed.
- `.systems/scripts/validate-workflow --profile full --progress summary --explain` then failed at `check-naming` before later validators because frozen ignored eval inputs include `STATE.md` and an archived checkout with `AGENTS.md`, `HUMANS.md` and `SKILL.md`.
- The owner answered the explicit scope question: "Tak, rozszerz i napraw" for a precise exclusion of frozen eval inputs without modifying the fixtures.

## Owner Decision

- Add `.systems/scripts/check-naming` to the approved tracked write set. Add the necessary smoke cases inside the already approved `.systems/scripts/check-validator-smoke-tests`.
- Exempt only raw fixture files and archived run checkout files in a project-local eval with a `freeze.md` marker. Canonical eval artifacts, unrelated workspace files and tracked source naming remain checked.
- Amend the spec and rerun Spec QA before this fifth tracked file is edited. No commit, push, phase 6/7 or phase 8 is approved here.

## Consequences

- The previous four-file Spec QA remains valid history for its scope but does not authorize the fifth file.
- Full validation must be rerun from the current workspace after the narrow correction; green targeted checks cannot replace it.
