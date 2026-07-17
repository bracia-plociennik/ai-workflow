# plan-quality-contract.md

## Purpose

`Plan Quality Contract` makes the Definition of Done and quality path explicit before a plan can authorize implementation-class writes.

It applies to formal architecture, project-plan, and specification artifacts; task cards; micro-task and micro-project plans; and every substantive Codex `plan` or `/plan` response that can lead to writes.

This contract does not create a workflow phase, grant write permission, replace an accepted spec, or turn an advisory review into formal `PASS`.

## Required Plan Quality Contract

Every applicable plan contains this block before implementation readiness is declared:

```text
## Plan Quality Contract

- Plan classification: <implementation-capable|read-only>
- DoD source:
- Testable DoD / acceptance conditions:
- Artifact QA route: <phase-1-architecture-qa|phase-2-plan-qa|phase-3-spec-qa|global-quality-review-stance|not-applicable>
- Artifact QA trigger:
- Implementation Quality Closure route: <phase-5-quality|global-quality-review-stance|not-applicable>
- Required verification: <automated checks|manual checks|edge/regression review|adaptive data/integration matrix or not-applicable with reason>
- Quality-ready criteria:
- Owner opt-out: <none|Quality skipped by owner opt-out>
- Not-applicable reason: <reason|none>
- Blocking decision: <decision ID|none>
- Next route:
```

`DoD source` and `Testable DoD / acceptance conditions` must be concrete enough to decide whether the work is done. A generic statement such as `test later` is not a quality route.

## Delivery Constraint Integration

Implementation-capable plans must use `.systems/ai/core/delivery-constraints.md` and record a deadline/timebox or a bounded owner opt-out. The plan must identify must-have outcome, cutline, deferred scope, quality floor, and overrun route. A read-only plan may mark delivery constraints `not-applicable` only with a reason. Delivery pressure never satisfies the DoD or bypasses QA, risk, permissions, approvals, or evidence.

## Route Selection

Use these defaults:

| Plan type | Artifact QA route | Implementation Quality Closure route |
| --- | --- | --- |
| formal architecture | `phase-1-architecture-qa` | `phase-5-quality` for each later formal implementation task |
| formal project plan | `phase-2-plan-qa` | `phase-5-quality` for each later formal implementation task |
| formal task/package specification | `phase-3-spec-qa` | `phase-5-quality` |
| side-task, micro-task, micro-project, or workflow-maintenance plan | `global-quality-review-stance` when artifact review is needed | `global-quality-review-stance` |
| read-only analysis or planning-only output | `not-applicable` only with a reason | `not-applicable` only with a reason and no implementation writes |

An `implementation-capable` plan must not use `not-applicable` for its Implementation Quality Closure route. It must select the formal or advisory route that matches its work mode.

## Codex Plan And `/plan` Responses

For every substantive `plan`, `/plan`, approach, or implementation plan response, render the Required Plan Quality Contract in the response before claiming that writes can begin.

Inside AI Workflow, `/plan` routes to `phase-3-specification` when a task/package specification is resolvable. The response must identify `phase-3-spec-qa` as the artifact QA route and `phase-5-quality` as the formal implementation quality route.

For a plan outside a resolvable formal project phase, classify the work mode first. A small low-risk implementation route may use advisory `global-quality-review-stance`; it must not be presented as formal `PASS`.

## Read-Only And Owner Opt-Out

A read-only plan may use `not-applicable` only when it declares no implementation writes and gives a specific Not-applicable reason. It remains a plan, not implementation readiness.

Recognized owner opt-out grammar remains governed by `.systems/ai/core/quality-review.md`. When an owner explicitly opts out, the plan still records its normal quality route and reports `Quality skipped by owner opt-out` plus residual risk. Opt-out does not satisfy formal QA PASS, permit phase progression where QA PASS is required, or bypass risk, permissions, evidence, DoD, approvals, or stop conditions.

## Pre-Write Boundary

Implementation-class writes must not start from a plan that lacks a complete Plan Quality Contract, a testable DoD, the applicable artifact QA route, or the applicable post-implementation quality closure route.

Before the first write, `.systems/ai/core/implementation-slicing.md` still requires its Implementation Slice Plan and current Instruction Adherence Refresh. Plan Quality Contract is an additional readiness requirement, not a replacement.

## Authority Boundary

Plan Quality Contract must not:

- grant write permission, change risk, or expand scope;
- bypass source-of-truth order, accepted artifacts, phase gates, permissions, evidence, approvals, or stop conditions;
- make `not-applicable` valid for implementation-capable work without a justified non-write route;
- make `Quality skipped by owner opt-out` a formal PASS;
- replace findings-first QA, Review Completeness Gate, or PASS Integrity Gate.
