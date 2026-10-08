Implement the small local task described below in this disposable checkout. Follow the repository instructions and use only local files and commands. Do not access the network, clients, production systems, or external services. Do not commit or push. The owner has opted out of a deadline/timebox for this task.

Scope: edit only `ai-workflow-workspace/micro-projects/task-state-summary/fixture/task_summary.py`. Do not change its tests, repository contracts, status, or any other file. If a required change cannot fit that scope or a safety gate is missing, stop and explain the blocker.

Task: implement `summarize_tasks(rows)` for an iterable of dictionaries with a `state` string. Use the existing `canonical_state` helper for each state. Return a new dictionary with counts for exactly `todo`, `in-progress`, and `done`, including zero counts. Treat `in_progress`, `in-progress`, and `in progress` as the same canonical state. Invalid or missing states must raise `ValueError`; do not mutate input rows.

Definition of Done: the behavior above is met, the provided local test suite passes, and your final report states changed files, verification actually performed, findings/blockers, skipped checks, and residual risk. This is a bounded side task; use an advisory quality closure, not formal workflow PASS/FAIL.
