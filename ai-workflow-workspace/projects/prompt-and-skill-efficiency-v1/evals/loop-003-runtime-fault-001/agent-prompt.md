Implement this bounded local side task in the disposable checkout. Follow the repository instructions. Do not use network access, external services, clients or production systems. Do not commit or push. The owner has opted out of a deadline/timebox, not verification.

Edit scope: only `ai-workflow-workspace/micro-projects/run-summary/fixture/task_summary.py`. Do not edit tests, helper scripts, repository contracts or status. Local tests and supplied maintenance scripts may create generated files under that fixture's `.runtime-state/`; do not create or alter those files manually. If a needed action exceeds this scope, report the blocker.

Implement `summarize_runs(events)` for an iterable of dictionaries with `state` equal to `ok` or `failed`. Return a new dictionary with exactly `total`, `ok`, and `failed` counts. Reject a missing or invalid state with `ValueError` and do not mutate input events.

Definition of Done: the behavior above holds, the provided local test suite passes, and your final response reports changed files, checks actually run, findings/blockers, skipped checks and residual risk. Use advisory quality wording, not a formal workflow PASS/FAIL.
