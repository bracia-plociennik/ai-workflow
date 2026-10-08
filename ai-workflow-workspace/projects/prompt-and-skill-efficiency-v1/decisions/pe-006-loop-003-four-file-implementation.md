# Decision: PE-006 LOOP-003 Four-File Implementation

## Date

`2026-09-28`

## Status

`approved` for the exact tracked write set, conditional on fresh Spec QA and Phase 4 readiness

## Classification

`high-impact`

## Context

- PE-005 reopened LOOP-003 planning and artifact QA but did not approve tracked source edits.
- First LOOP-003 Spec QA found one blocker: missing exact high-risk tracked-write approval. It found no independent material defect in the spec content.
- The owner now says: "Zatwierdzam czteroplikowy zakres LOOP-003 wskazany w Spec QA. Ponów Spec QA, wraz z implementacja po pozytywym wyniku qa."

## Owner Decision

- Approved tracked files: `.systems/ai/core/implementation-slicing.md`, `.systems/ai/workflow/phase-4-implementation.md`, `.systems/scripts/check-implementation-slicing`, `.systems/scripts/check-validator-smoke-tests`.
- Authorized route: spec fix loop and fresh Spec QA; if the result is positive and pre-write readiness is complete, run Phase 4 implementation and required Phase 5 quality.
- No other tracked file, commit, push, phase 6/7, or phase 8 is approved by this decision.

## Consequences

- Keep the contract-clarity hypothesis separate from an observed behavioral defect; existing evals did not establish natural early-stop behavior.
- Any fifth tracked file or changed scope requires a new owner decision and re-QA.
- Negative safety cases, same-model paired evidence, current-state semantic review, and applicable validation remain required. Approval cannot create a quality verdict.
