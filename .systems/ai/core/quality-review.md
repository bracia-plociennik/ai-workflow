# quality-review.md

## Purpose

`global-quality-review-stance` is the default read-only/advisory review protocol for review, code review, final review, findings, blockers, and risk-check requests when the request is not clearly a formal workflow phase.

It is inspired by `phase-5-quality`, but it is not the formal `phase-5-quality` gate.

Apply `.systems/ai/core/full-qa-verification.md`. Global review uses its full, artifact-appropriate verification scope and adaptive data/integration matrix when applicable, but remains advisory.

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
- after implementation, slice execution, or fix work, report verify/review evidence, findings, blockers, DoD fit, intent/plan/spec/prompt compliance, changed files review, edge cases, regression risk, skipped checks impact, residual risk, and whether a formal gate can be used;
- include the result in the user-facing response and `Execution Trace`.

Owner opt-out grammar:

- `bez QA`
- `bez review`
- `bez quality`
- `bez weryfikacji`
- `bez sprawdzania`
- `without QA`
- `without review`
- `without verification`
- `no verification`
- `fast path no review`

When the owner opts out, the response must state `Quality skipped by owner opt-out` and report residual risk. Opt-out does not allow continuing as `PASS`, does not satisfy a required QA/Quality gate, does not allow moving to the next phase when QA PASS is required, and does not bypass risk, permissions, evidence, DoD, approvals, or stop conditions.

## PASS Integrity Gate

Formal `PASS` is allowed only inside formal QA/Quality phases, including `phase-5-quality`, when required inputs, writes, evidence, and gate permissions are satisfied.

Formal `PASS` requires findings-first review evidence before the result is declared. The review lens must include:

- blockers;
- findings by severity;
- DoD fit;
- intent/plan/spec/prompt compliance;
- changed files review;
- edge cases;
- regression risk;
- skipped checks impact;
- residual risk.

If unresolved `P0`, `P1`, or material `P2` findings remain, the result cannot be `PASS`.

Do not use empty `zweryfikowane`, `verified`, or `PASS` wording without evidence and findings-first review. Advisory review and default quality closure outside a formal gate must not produce formal `PASS`; use evidence wording such as `No blockers found`, `No findings found`, or `Ready for owner review`.

If a later review finds a material issue that the required review lens should have caught, treat it as a new finding/regression or evidence that the earlier `PASS` was invalid because the required lens or evidence was missing.

## Review Procedure

Read-only review and QA use the non-interactive path from `.systems/ai/core/owner-decision-checkpoints.md`. Finish evidence review before presenting owner decisions. Do not interrupt mid-review; report missing material sources as `unknown`, a blocker, or formal `FAIL` when the formal phase requires it, then queue decisions at the end.

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

When the reviewed scope affects data models, parsers, transformations, integrations, state transitions, executable entrypoints, derived outputs, or persisted error states, complete the `Adaptive Data / Integration Verification Matrix` from `.systems/ai/core/full-qa-verification.md`. Report `not-applicable` with a reason only when no such flow is affected.

## Review Completeness Gate

Every advisory review and formal `phase-5-quality` run must complete this gate before declaring `No findings found`, `Ready for owner review`, `PASS`, or an equivalent quality verdict.

Report:

- Cross-contract consistency: `<aligned|partial|mismatch|unknown>`.
- Risk/work mode compatibility: `<aligned|partial|mismatch|unknown>`.
- Source-of-truth, permissions, phase gates, artifact state, and acceptance criteria reviewed: `<yes|no|not-applicable>`.
- Negative-space / adversarial review: `<completed|not-applicable|incomplete>`.
- Automated evidence role: `supporting-only`.
- Post-fix full re-review: `<completed|not-required|incomplete>`.
- Reviewed baseline: `<HEAD/worktree/diff/artifact identifiers>`.
- Instruction refresh: `<performed-targeted|performed-full|not-needed|blocked>`.
- Instruction baseline: `<current|stale|blocked>`.
- Closure freshness: `<current|stale>`.

### V2: Policy And Schema Change Evidence

When a review covers policy wording, validators, templates, routing, queues, or another contract schema, also report:

- Policy-boundary adversarial matrix: `<completed|not-applicable|incomplete>`.
- Producer-consumer field audit: `<completed|not-applicable|incomplete>`.
- Producers/consumers reviewed: `<paths or not-applicable>`.
- Required-field mapping: `<complete|partial|mismatch|not-applicable>`.

The policy-boundary adversarial matrix is required for every changed validator or policy boundary. It must prove that direct unsafe wording fails, the ordinary safe prohibition passes, and a single line that combines a safe prohibition with a conflicting enablement clause, including `but`, `however`, a period, colon, `unless`, `yet`, or a semicolon-separated clause, fails. A missing or unreadable scan source must fail closed instead of being treated as no unsafe match.

The producer-consumer field audit is required whenever a contract declares required fields that a template, queue, report, response, or durable artifact must produce. It identifies every active producer, verifies its field mapping against the canonical contract, and classifies supporting evidence that is not itself a producer. Presence of a section heading is not field-level evidence.

Cross-contract consistency compares the work against all applicable contracts, not only the accepted plan. At minimum, verify risk class against work mode, source-of-truth order, permissions, phase gates, artifact state, and acceptance criteria. A plan or owner instruction cannot silently authorize a mode that the risk model forbids.

Negative-space / adversarial review asks what equivalent unsafe, incomplete, or contradictory case is not represented by the current tests. For validators and policy regexes, inspect omitted taxonomy values, paraphrases, inverse wording, bypass wording, and plausible false positives and false negatives. Passing only the named smoke example is insufficient.

Automated tests, validators, builds, and smoke tests are supporting evidence, not a standalone verdict. Green automated checks do not prove that the implementation matches every applicable contract or that validator coverage is semantically complete.

Any implementation or documentation fix made after review invalidates the previous closure. Set `Closure freshness: stale`, then repeat the complete review against the full current diff/worktree and applicable artifacts. Post-fix review must not inspect only the fixed lines. A different agent is not required, but the new review must restart from current sources and must not reuse the earlier verdict as evidence.

Recording the review artifact or local evidence after the review does not invalidate closure when that write only records the completed review and does not change reviewed implementation, contracts, scope, decisions, or acceptance evidence. Any substantive correction made while recording closure starts a new fix cycle.

Do not declare `No findings found`, `Ready for owner review`, or formal `PASS` when cross-contract consistency is `partial`, `mismatch`, or `unknown`; negative-space review is required but incomplete; an applicable policy-boundary adversarial matrix or producer-consumer field audit is incomplete; required-field mapping is `partial` or `mismatch`; automated checks are the only evidence; post-fix full re-review is incomplete; or closure freshness is `stale`.

Review uses `.systems/ai/core/instruction-adherence-refresh.md` before evaluating the final baseline. A stale or blocked instruction baseline makes Review Completeness Gate incomplete and prevents a quality-ready verdict.

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
- Review Completeness Gate;
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
