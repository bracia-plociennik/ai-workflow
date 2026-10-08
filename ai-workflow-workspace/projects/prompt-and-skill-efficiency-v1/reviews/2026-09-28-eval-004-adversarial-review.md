# Eval 004 Adversarial Review

## Baseline And Scope

- Date: 2026-09-28; branch `codex/prompt-and-skill-efficiency-core-001`, tracked worktree clean at `b9ec176` before this remediation.
- Sources: Eval 004 plan, four model traces and result, current `AGENTS.md`, operating model, phase-skill validator, active skill, `run_loop.py`, `run_eval.py`, `aggregate_benchmark.py`, and a synthetic runtime probe.
- Review is read-only. PE-011's SKILL-002 no-change closeout and historical Spec QA FAIL remain unchanged.

## Findings And Counterarguments

1. **Routine discovery overread: confirmed behavior, root cause not proven.** The three negative prompts explicitly requested skill discovery, which may increase the chance of opening the only available skill. The agent selected `none` correctly each time, so this is not a false-activation safety bug. Still, all three command traces used `cat` on the full 14,393-byte contract, even for catalog-only selection. Current higher-level contracts require checking active `SKILL.md` but never distinguish metadata-based candidate selection from full-body execution. A metadata-first router is a narrow, testable fix hypothesis; it must be validated behaviorally after the edit rather than assumed effective from passing text checks.
2. **Stale grading: confirmed through the real entrypoint.** `run_loop.py` invokes `run_eval.py --overwrite`, then aggregates any `grading.json`. The updated probe executed `run_loop.py` after changing a synthetic eval prompt/expectation and observed new metadata with the old passing grade in the benchmark. `quick_validate.py` is stdlib-only and passed; the earlier PyYAML explanation was false and is corrected in Eval 004. A pre-write compatibility check must refuse changed graded runs without deleting evidence. Direct callers of `run_eval.py --overwrite` need the same protection; patching only `run_loop.py` would leave a bypass.
3. **Unconfirmed context-route concern:** positive-control review suggested a possible `context/` review wording issue. No failing context-driven review case exists. Exclude it from this write set.

## Adversarial Requirements

- Discovery: inspect frontmatter name/description first; preserve workspace-before-system precedence, active `SKILL.md` requirement, positive activation, ambiguity escalation, and supporting-only skill authority. Reject a fix that merely narrows skill-creator's description without changing the discovery consumer.
- Eval freshness: unchanged graded plan must remain resumable. Changed prompt, expected behavior, assertions, configurations, eval membership or source-plan identity with existing grades must fail before any output mutation. Orphan grades must fail. An ungraded scaffold may be overwritten under the existing flag. No silent deletion, reset or stale PASS.
- Evidence: add a focused automated regression test and smoke integration; run a new isolated model eval after the router edit. If the negative cases still load the full irrelevant skill, do not claim the overread fixed or give formal Phase 5 PASS.
- Privacy/permissions: synthetic fixtures only for model eval; no client content, production effects, commit or push. Scripts remain supporting evidence after semantic QA.

## Review Outcome

Both P2 findings warrant a new formal task in this active project. Owner's current instruction approves planning and implementation of their remediation; exact file set and acceptance checks are recorded in the new plan/spec. Phase 8 remains blocked until a fresh post-fix quality gate and checkpoint path are complete.
