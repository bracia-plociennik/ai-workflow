# Decision: PE-002 AGENTS-Only First Candidate

## Date

`2026-09-25`

## Status

`approved`

## Classification

`high-impact`

## Context

- The CORE-001 specification requires explicit approval for the exact first-candidate tracked write set.
- The owner said: "Zatwierdzam AGENTS.md jako jedyny plik pierwszego wariantu. Wznów planning-range od Spec Fix Loop i Spec QA, bez commita."
- The later owner command starts a separate CORE-only implementation-range, again limiting tracked writes to `AGENTS.md` and forbidding a commit.

## Owner Decision

- Chosen option: root `AGENTS.md` is the only approved tracked file for the first CORE-001 candidate.
- Decided by: owner, explicit chat instruction.
- Decision date: 2026-09-25.

## Consequences

- Candidate preparation, paired synthetic evaluation, and implementation may proceed only after applicable spec QA, readiness and pre-write checks.
- No other tracked source, validator, skill, template or CI file is approved for this range.
- This decision does not authorize a commit, push, formal quality PASS, phase 8, or any SKILL-002/LOOP-003 implementation.
- A required change outside `AGENTS.md` must stop and seek a new owner decision.
