# SKILL-002 Separate Routine Discovery Eval 004: Result

## Findings First

1. **P2, material to this efficiency project: routine discovery reads the full irrelevant skill contract.** All three distinct non-trigger cases opened the complete 14,393-byte `skill-creator/SKILL.md` with `cat`, then correctly selected `none`. The cases were neutral product-code review, a filename collision, and catalog-only future-skill selection. This meets the predeclared material threshold of at least two distinct routine negative cases. It demonstrates systematic context overread, not wrong skill application or measured token/time savings.
2. **P2, confirmed evidence-integrity gap: `run_loop.py` can aggregate stale grades.** The current `run_loop.py` calls `run_eval.py --overwrite` and then aggregates any existing `grading.json`. A local synthetic probe changed the eval prompt/expected behavior, reran the full `run_loop.py` entrypoint, and obtained `metadata_is_new: true, old_grade_reused: true`. `aggregate_benchmark.py` accepted the older `passed: true` grade without matching it to current metadata. An earlier statement that PyYAML was required by `quick_validate.py` was wrong; the validator is stdlib-only and passed locally.
3. **P3 candidate, not promoted:** the positive-control agent suggested a narrower `context/` review route. This was not reproduced as a failing context-driven review case, so it is not a confirmed blocker from this eval.

## Case Evidence

| Case | Run | Full skill-body read | Skill selection | Other result |
| --- | --- | --- | --- | --- |
| `generic-review` | `runs/generic-review/002/` | yes, `cat` | none, correct | Found the synthetic integer-division bug |
| `name-collision-review` | `runs/name-collision-review/001/` | yes, `cat` | none, correct | Filename did not cause false activation; found the bug |
| `catalog-only` | `runs/catalog-only/001/` | yes, `cat` | none, correct | Did not inspect product code |
| `direct-skill-review` | `runs/direct-skill-review/001/` | yes, expected | `skill-creator`, correct | Read skill/resource code; raised stale-grade hypothesis confirmed by probe |

The first `generic-review/001` attempt exited 1 before model execution because the outer sandbox denied Codex state DB initialization. It was excluded from grading. The identical prompt retry at `002` exited 0. All four completed model runs exited 0 and reported `fixture_unchanged: true`, with the same fixture SHA-256 `93067d16...` before and after. The synthetic fixture contains current public AI Workflow contract copies and toy product code, no client data or secrets. The active `SKILL.md` and `run_loop.py` hashes match their fixture copies byte-for-byte.

## Adversarial Review

- **Owner intent / DoD:** the isolated eval answered whether routine discovery avoids unnecessary full-body reads while preserving positive activation. It did not implement a source fix or reopen SKILL-002.
- **Producer-consumer:** AGENTS Phase Skill Discovery is the consumer of skill metadata; the three negative traces show full body loaded before rejecting the skill. For grading, `run_eval.py --overwrite` produces fresh metadata, while `aggregate_benchmark.py` consumes old `grading.json` without freshness binding.
- **Failure paths:** the first environment failure was excluded; all completed traces were inspected for actual commands. No tracked file changed. The temp probe deleted its own test directory on exit.
- **Limits:** one successful run per case; the 3/3 pattern is directional, not statistical confidence. No measured model token delta or candidate router comparison. The stale-grade probe now exercises the full `run_loop.py` entrypoint with a synthetic plan and grade, but not an LLM grading run.
- **Privacy/scope:** pass for the reviewed traces; commands remained within the synthetic fixture and did not show client paths or external file reads. The CLI model service received synthetic fixture content only.

## Quality Closure And Routing

- No formal `PASS/FAIL` is claimed for SKILL-002 or Phase 8. The prior PE-011 no-change decision and historical SKILL Spec QA FAIL remain unchanged.
- The predeclared material threshold was met. **Do not execute `phase-8-final-check` under the owner's conditional instruction.** Resolve owner routing for the discovery-consumer overread and stale-grade evidence integrity first, then repeat a focused eval and final readiness review.
- Do not edit tracked source, create a new task, commit, push, or claim final owner approval from this report. A later fix requires a separate accepted scope, risk/approval decision, plan/spec QA and quality closure.
- Knowledge capture: this ignored result is the durable project evidence for now. Promotion to project memory or External Memory is deferred to an authorized distillation/checkpoint or owner-approved capture.
