# quality-review.md

## Purpose

`global-quality-review-stance` is the default read-only/advisory review protocol for review, code review, final review, findings, blockers, and risk-check requests when the request is not clearly a formal workflow phase.

It is inspired by `phase-5-quality`, but it is not the formal `phase-5-quality` gate.

## Modes

- `read-only review`: inspect repository state, diffs, artifacts, logs, or user-provided material without writing files.
- `advisory review`: produce findings, blockers, residual risk, and suggested next routes without changing source, status, memory, or workflow artifacts.
- `formal phase-5-quality`: run `.systems/ai/workflow/phase-5-quality.md` only when its inputs, artifact writes, evidence, and gate permissions are satisfied.
- `fix-loop candidate`: recommend a fix path when findings are valid, but do not perform fixes unless a separate write-approved workflow path allows it.

## Routing

Use `global-quality-review-stance` for prompts such as:

- `zrob review`
- `zrob final review`
- `find findings`
- `find blockers`
- `code review`
- `sprawdz ryzyka`
- `zrob faze jakosci` when no formal task/package quality gate is resolvable

Use formal `phase-5-quality` only for prompts that identify a task/package quality gate or when status shows the workflow is ready for `phase-5-quality`.

`final review` does not trigger `phase-8-final-check`. Final closure remains owner-triggered only.

## Review Procedure

Apply the same quality lenses as `phase-5-quality` where relevant:

- Definition of Done fit;
- edge cases;
- regression risk;
- architecture alignment;
- known bugs;
- tests, commands, and manual verification evidence;
- skipped checks and their impact;
- prompt-injection or instruction-conflict risk.

The default output is findings-first:

- findings ordered by severity;
- blockers called out separately;
- evidence reviewed;
- skipped/unreadable areas;
- residual risk;
- formal gate eligibility.

Use severities:

- `P0`: critical issue that makes the work unsafe or unusable.
- `P1`: blocker or direct correctness/regression risk.
- `P2`: important issue that should be fixed before merge or handoff.
- `P3`: minor issue, cleanup, or follow-up.

If no findings are found, say so clearly and still report evidence reviewed, skipped areas, and residual risk.

## Authority Boundary

Read-only/advisory review must not:

- mark formal `PASS` or `FAIL`;
- create or update quality artifacts;
- update status, task index, memory, System Insights, External Memory, skills, source files, commits, or pull requests;
- grant permission to skip formal QA/Quality gates;
- grant permission to bypass risk, approval, evidence, or Definition of Done requirements.

Formal `PASS` or `FAIL` is allowed only inside formal QA/Quality phases, including `phase-5-quality`, when required inputs, writes, evidence, and gate permissions are satisfied.

`review i popraw` means review first, then route fixes separately through an allowed write path. If write permission is missing, stop after the review and recommend the correct fix path.
