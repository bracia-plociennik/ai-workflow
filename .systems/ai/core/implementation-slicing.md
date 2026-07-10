# implementation-slicing.md

## Purpose

Implementation Slicing is the execution discipline for implementation-class writes. Before changing source, docs, templates, validators, scripts, or runtime artifacts as part of implementation work, the agent must create an `Implementation Slice Plan` and then execute slices sequentially with evidence.

This contract applies to:

- formal `phase-4-implementation`;
- implementation or fix-loop work inside a full project;
- side tasks, project-local micro-tasks, repo-level micro-projects, and workflow-maintenance changes when they perform implementation-class writes.

It does not apply to read-only review, idea validation, architecture, planning, specification, command output, status-only inspection, or proposal-only capture.

## Authority Boundary

An `Implementation Slice Plan` is sequencing and evidence discipline only.

It must not:

- grant write permission;
- expand scope;
- change risk classification;
- bypass source-of-truth order;
- bypass accepted spec, accepted owner prompt/context, permissions, phase gates, approvals, evidence, QA/Quality, or Definition of Done;
- replace formal `phase-4-implementation`, micro-task, side-task, micro-project, or workflow-maintenance contracts.

If any required gate is missing, stop before writes even if a slice plan exists.

## Required Fields

Every implementation-class write path must identify:

- Source: accepted spec, or accepted owner prompt/context when no formal spec exists.
- Implementation scope: the exact accepted scope to implement.
- DoD source: the accepted Definition of Done, acceptance criteria, or safely inferable DoD from accepted owner prompt/context.
- Slice table with columns:
  - `slice id`
  - `goal`
  - `expected files/areas`
  - `acceptance check`
  - `evidence required`
  - `status`
- Stop rule: if a slice reveals scope creep, missing decision, dependency conflict, unsafe action, unapproved external effect, or spec/context mismatch, stop and route to the proper phase or owner decision.

## DoD Before Implementation

Implementation-class writes must not start until the work has a clear and testable Definition of Done.

For formal workflow tasks, the DoD comes from the accepted spec and Spec QA evidence. `phase-4-implementation` must stop when the DoD is missing, untestable, stale, or contradictory.

For side tasks, project-local micro-tasks, repo-level micro-projects, and workflow-maintenance changes, the DoD comes from the accepted owner prompt/context, accepted micro-task artifact, or accepted micro-project artifact. If the DoD is not explicit but is safely inferable, record the inference in the `Implementation Slice Plan`. If it is unclear, stop before writes and ask for the missing acceptance decision.

## Slice Execution Evidence

After each slice, record evidence appropriate to the work mode:

- slice id;
- status: `completed|blocked|skipped`;
- files or areas changed;
- checks run or skipped with reason;
- acceptance check result;
- residual risk;
- next slice or stop reason.

Formal `phase-4-implementation` records this in the implementation result artifact. Side tasks, micro-tasks, micro-projects, and workflow-maintenance work may record it in the response, micro-task artifact, micro-project artifact, or final handoff evidence.

## Mandatory Quality Closure

Every implementation-class write path must end with quality closure after implementation, after slice execution, and after fix work.

Use:

- formal `phase-5-quality` for the formal phase path when its inputs, artifacts, evidence, and permissions are satisfied;
- `global-quality-review-stance` for side tasks, project-local micro-tasks, repo-level micro-projects, workflow-maintenance, and other implementation work without a formal quality gate.

Quality closure must cover:

- verify and review evidence;
- findings and blockers;
- DoD fit;
- intent/plan/spec/prompt compliance;
- changed files review;
- edge cases;
- regression risk;
- skipped checks impact;
- residual risk.

Advisory quality closure does not create a formal quality artifact and must not produce formal `PASS` or `FAIL`. It must still be reported in response or artifact evidence with findings/blockers and residual risk.

Owner opt-out is allowed only through explicit wording such as `bez QA`, `bez review`, `bez quality`, `bez weryfikacji`, `bez sprawdzania`, `without QA`, `without review`, `without verification`, `no verification`, or `fast path no review`. Opt-out must report `Quality skipped by owner opt-out` and residual risk. Opt-out does not satisfy formal QA PASS, does not allow a phase gate to pass, and does not bypass risk, permissions, evidence, DoD, approvals, or stop conditions.

## PASS Integrity Gate

Formal `PASS` is allowed only inside a formal QA/Quality phase such as `phase-5-quality`.

Before formal `PASS`, the agent must apply the same findings-first review lens used by `zrob review`, `find blockers`, and `zrob QA`:

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

Do not use empty `zweryfikowane`, `verified`, or `PASS` wording without evidence and findings-first review. For side tasks, micro-tasks, micro-projects, and workflow-maintenance without a formal gate, use advisory wording such as `No blockers found`, `No findings found`, or `Ready for owner review` with evidence.

If a later review finds a material issue that the required lens should have caught, treat it as either a new finding/regression or evidence that the earlier `PASS` was invalid because the required review lens or evidence was missing.

Any fix after quality review invalidates the previous quality closure. Set `Closure freshness: stale` and repeat the complete findings-first review against the full current diff/worktree, applicable artifacts, DoD, and cross-contract boundaries. `Post-fix full re-review` must inspect the complete current state, not only the fixed lines. Automated checks remain supporting evidence and cannot restore `No findings found`, `Ready for owner review`, or formal `PASS` without the full-current-state re-review required by `.systems/ai/core/quality-review.md`.

## Compact Mode

Tiny low-risk implementation work may use compact mode.

Compact mode still requires a one-slice plan with:

- source;
- implementation scope;
- DoD source;
- one slice id;
- goal;
- expected files/areas;
- acceptance check;
- evidence required;
- status.

Compact mode is allowed only when the work is tiny, low-risk, local, has clear acceptance criteria, and does not touch architecture, auth, billing, permissions, migrations, secrets, infrastructure, production data, destructive commands, or real external side effects.

Compact mode must still end with evidence and quality closure unless the owner explicitly opts out.

## Formal Phase-4 Use

For formal `phase-4-implementation`:

- derive slices from the accepted spec and Spec QA evidence;
- confirm the accepted spec has a clear, testable DoD before implementation-class writes;
- keep slices inside the accepted spec and task/package scope;
- execute slices in order unless the implementation result explains a safe reorder;
- update the phase-4 implementation result with `Implementation Slice Plan` and `Slice Execution Evidence`;
- route to `phase-5-quality` only after implementation evidence is complete.

If the accepted spec is incomplete, has missing or untestable DoD, or cannot produce a safe slice plan, stop and route back to specification or owner decision.

## Side Task, Micro-task, And Micro-project Use

When there is no formal spec, the source is the accepted owner prompt/context plus any accepted micro-task or micro-project artifact.

For implementation-class writes in these modes:

- create a compact or full `Implementation Slice Plan` before writes;
- keep slices within the accepted prompt/context;
- record the DoD source before writes;
- do not use slicing to promote medium/high/critical work into side-task or micro-task mode;
- record slice evidence in the final response or durable artifact when one exists.

If slicing reveals missing acceptance criteria, unclear DoD, risk above low for side-task mode, dependency conflict, or unsafe external effects, stop and route to the normal workflow.
