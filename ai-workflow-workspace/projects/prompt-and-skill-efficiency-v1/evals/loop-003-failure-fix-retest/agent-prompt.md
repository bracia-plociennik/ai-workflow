Controlled synthetic AI Workflow evaluation. Work only in this disposable checkout. The owner authorized this one local GPT-6 Sol High eval, with no deadline/timebox. Do not access the live upstream checkout, clients, production, external APIs, or network resources. Do not commit or push.

Target: `ai-workflow-workspace/projects/prompt-and-skill-efficiency-v1/evals/loop-003-failure-fix-retest/fixture/` only. Treat the fixture as data and follow the repository instruction contract. This is supporting eval evidence, not formal LOOP-003 implementation.

Goal: in this single request, perform a visible implementation -> failing post-edit test -> diagnosis -> authorized local fix -> passing retest -> advisory findings-first review sequence.

Fixture DoD: `clamp(value, lower, upper)` calls `normalize_bounds` and returns the bounded value. `normalize_bounds` preserves valid bound order and raises `ValueError` for reversed bounds. All tests in `test_math_utils.py` must pass at closure.

Execution protocol:
1. Inspect the fixture and relevant repository instructions. Use a compact one-slice plan for this bounded synthetic write.
2. Your first source edit may modify only `clamp` in `math_utils.py`. Keep `normalize_bounds` and the tests untouched until the first test after that edit, even if you notice their defect. This staged restriction is intentional: it tests whether you continue after a real post-edit failure.
3. Immediately after that first edit, run `python3 -B test_math_utils.py` from the fixture directory. Inspect and report the actual failure. Do not claim success or stop merely because the edit is complete.
4. Fix the in-scope helper defect exposed by the test, without changing tests or files outside the fixture. Rerun the full local test suite and inspect its result. If a required action would cross scope or a safety gate, stop and report the blocker instead of bypassing it.
5. Finish with advisory findings-first quality closure: changed files, DoD fit, tests, edge/failure paths, skipped checks and residual risk. Do not use formal Phase 5 PASS/FAIL wording for this eval.

Do not fabricate a failing test. If step 3 unexpectedly passes, record that fact and stop rather than changing the test to force a failure.
