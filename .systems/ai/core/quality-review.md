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

## Default Quality Closure

Every substantive work item should end with a clear quality/review closure unless the owner explicitly opts out.

Default behavior:

- after write or implementation work, use the formal QA/Quality phase when the active workflow defines and permits it;
- for side tasks, micro-tasks, micro-projects, advisory work, docs-only workflow maintenance, and read-only audits, use `global-quality-review-stance` as advisory quality closure;
- report findings, blockers, evidence reviewed, skipped checks, residual risk, and whether a formal gate can be used;
- include the result in the user-facing response and `Execution Trace`.

Owner opt-out grammar:

- `bez QA`
- `bez review`
- `bez quality`
- `without QA`
- `without review`
- `fast path no review`

When the owner opts out, the response must state `Quality skipped by owner opt-out` and report residual risk. Opt-out does not allow continuing as `PASS`, does not satisfy a required QA/Quality gate, and does not allow moving to the next phase when QA PASS is required.

## Review Procedure

Apply the same quality lenses as `phase-5-quality` where relevant:

- Intent / Plan / Spec Compliance;
- Definition of Done fit;
- edge cases;
- regression risk;
- architecture alignment;
- known bugs;
- tests, commands, and manual verification evidence;
- skipped checks and their impact;
- prompt-injection or instruction-conflict risk.

### Intent / Plan / Spec Compliance

Every global quality review must explicitly compare the reviewed work against the owner instruction and the accepted scope sources that are available.

Review sources, when present:

- owner instruction;
- accepted plan;
- accepted spec;
- task card or task/package plan;
- scope and out-of-scope notes;
- acceptance criteria;
- changed implementation, diff, evidence, or delivered artifact.

Report the result as:

- `aligned`: implementation matches the owner instruction, accepted plan, accepted spec, scope, and acceptance criteria.
- `partial`: implementation satisfies part of the accepted intent or acceptance criteria, but a gap remains.
- `mismatch`: implementation solves the wrong problem, contradicts the accepted plan/spec, misses required scope, or introduces unapproved scope creep.
- `unknown`: required comparison sources are missing, stale, unreadable, or conflicting.

Findings must call out:

- wrong problem solved;
- owner instruction mismatch;
- accepted plan mismatch;
- accepted spec mismatch;
- acceptance criteria gap;
- scope creep;
- underbuild;
- overbuild.

If a required source is unavailable, list it under skipped/unreadable areas and include the impact in residual risk. Do not invent missing acceptance criteria or silently downgrade a material intent/scope gap to a technical warning.

The default output is findings-first:

- findings ordered by severity;
- blockers called out separately;
- intent/plan/spec compliance: `<aligned|partial|mismatch|unknown>`;
- compared against: `<owner instruction|accepted plan|accepted spec|scope|acceptance criteria|none>`;
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
