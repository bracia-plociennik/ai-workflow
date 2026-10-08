# Accepted Project Context: Prompt And Skill Efficiency V1

## Outcome

Measure and improve AI Workflow instruction loading, skill selection, and task completion persistence while preserving safety and quality gates.

## Scope

1. Capture behavioral baseline for current `AGENTS.md`, active skill triggers, and completion behavior before any tracked changes.
2. Use paired, same-model evaluations to guide conditional document routing and skill trigger changes.
3. Add a bounded safe local test-fix-retest behavior where current permissions allow it.
4. Evaluate, but do not automatically change, model recommendation frequency, response trace verbosity, and prompt-module repetition.
5. Re-run holdout cases and formal QA before considering the work complete.

## Constraints

- GPT-6 Sol High is the selected comparison model. Do not pool its results with other models.
- Owner explicitly chose no deadline and no timebox for this scope; DoD and QA remain mandatory.
- Use anonymized local fixtures only; no real client data, secrets, production, external effects, network, or destructive operations.
- Baseline behavioral eval requires an explicitly allowed execution method. Until then, only static preflight is evidence.
- No tracked source change before baseline completion and review.
- Formal planning-range and implementation-range autopilot runs are separate and cannot include phase 8.
- No commit, push, PR, or cross-system adaptation is implied by this execution request.

## Success Criteria

- All safety-critical routing, approvals, QA, DoD, and stop cases remain correct.
- Trigger false positives fall without introducing missed required skills on holdout cases.
- Irrelevant document loading decreases on simple cases, measured against the frozen baseline.
- Controlled implementation scenarios complete the authorized local test-fix-retest and quality closure, or stop at a genuine gate.
- Every claimed gain is backed by comparable evidence, with unknown measurements reported as unknown.

## Source And Authority

Owner matrix and request set the task objective. Current repository state and AI Workflow contracts retain authority. The OpenAI article and AI System observations are supporting evidence only.
