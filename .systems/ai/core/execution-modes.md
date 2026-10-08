# Execution Modes

## Mode Selection

New work defaults to `auto`. `Human Coop`, `pracujmy wspólnie` and `konsultuj decyzje` select `human-coop`. Explicit `Auto Mode` selects `auto`. This interaction mode is independent of the work mode, formal phase, autopilot range and technical `autopilot.mode`.

Resolve the most specific explicit choice: task, then declared session override, then project, then default. Record the mode, scope, source and scope ID before dependent work. A task choice expires with that task. A session choice requires explicit session-wide wording and does not leak into a new session. Resume preserves the recorded choice; it does not reset Human Coop to Auto.

Legacy artifacts without an execution field remain historical under their original approvals. At readiness for future work, explicitly resolve and record the new mode and permission baseline. Do not rewrite old artifacts or grant retrospective autonomy.

## Autonomous Choices

Auto discovers facts first and takes the recommended safe, reversible choice inside the accepted goal, constraints and permissions. This includes local implementation strategy, testing, reversible owner preferences and local architecture choices. Record significant assumptions, why the choice serves DoD and the impact of a later override. A material choice can remain classified `high-impact`; record disposition `agent-choice` only if its local effects are already covered by the accepted scope and approvals. Classification is not downgraded to obtain permission.

When owner intent is clear, derive and record a testable DoD before implementation. Fundamental ambiguity about the goal, protected data, required permission or acceptance criteria blocks dependent writes. Do not lower accepted DoD or hide a stub as completed work.

Human Coop discovers facts and asks at most 1-3 material questions with recommendation, alternatives and impacts. Safe trivial choices and previously answered questions do not need repetition. Auto queues owner-only decisions without live questions; read-only review, Dreaming and active autopilot remain non-interactive even when Human Coop is selected.

## Approval Scope

An owner's acceptance of a concrete plan can cover its explicitly described local high-risk implementation and formal Phase 5 assessment. Record the actual approval reference, task scope, actions and risk; verify them at each gate without asking again. Plan acceptance does not predetermine QA PASS. Unknown or new risk, expanded scope and uncovered effects require their own approval.

Execution mode must not grant permissions, approve critical-risk actions, production, billing, destructive operations or real external effects. Platform approvals still apply. Critical-risk remains human-led unless explicitly delegated with existing controls. A Git revert cannot undo external effects, disclosure or lost data.

## Independent Continuation

Pending decisions block their affected units and transitive dependents, not automatically every unit in the run. Readiness selects an explicit runnable subset with current gates, approval coverage, DoD, known dependencies and verified write/resource independence. Unknown dependency or isolation evidence blocks the unit. Shared uncertainty blocks every affected unit; a global permission/baseline conflict blocks the run.

One coordinator owns shared status, decisions, integration, QA and commits. Subagents inherit the resolved mode and exact approved subset; they cannot spawn approvals or treat submission as acceptance. Continue independent units serially unless the installed parallel policy independently permits dispatch.

An active run may remain running with a queued decision for an excluded unit only while a proven independent runnable unit exists. It must not execute a unit blocked by a pending material decision. If no safe unit remains, stop as `awaiting-owner` for owner decisions or `blocked` for other failures, and present one queue.

## Runtime Evidence

Use existing project status, task decisions and run readiness/state. Templates persist `execution` separately from technical `autopilot.mode`: mode, scope, scope-id, source, approval-reference, completed-units, blocked-units and pending-decisions. Task decision records add disposition, affected-units, blocking reason, assumption and override impact; full queued records retain the existing Decision Request Contract.

Projection decision IDs and reasons are summaries, not replacements for the full queued decision records, alternatives/impacts or durable decision-artifact references required by owner-decision-checkpoints.md.
Implementation projections must declare at least one write action and exclusive resource claims; no-op/read-only work must use the matching work kind rather than empty write metadata. Claims still require real coordinator verification.

The optional `execution-readiness.template.json` projection is inspected by `check-execution-modes --state <file>`. It contains declared unit prerequisites, work kind, decisions, approved actions, baseline and exclusive resources. The pure inspector computes readiness, transitive blocking and completion. Planning unit action set: artifact-write, formal-quality and local-commit only. Read-only units reject write actions. Unknown action names are rejected. High-impact agent choices require scoped approval references for all affected units. It performs no writes, launches or approval verification. A declared reference or true flag is not proof: the coordinator must verify real sources, gates, repository baseline and resource isolation before execution. An unknown or malformed projection is rejected.

On resume, inspect actual repo/worker state and verify the saved baseline, approval scope, mode and dependencies. Accepted output is not repeated. Baseline drift requires refreshed readiness and affected QA; a worker message is not completion evidence.

## Delivery And Completion

For new Auto work, absent deadline/timebox is `auto-unbounded`, with no interactive deadline question and no invented time budget. Preserve explicit limits and existing platform/resource budgets. Retry limits and no-progress stops remain required; no deadline does not authorize infinite repetition. Human Coop retains delivery discovery. A recorded legacy deadline is not silently removed.

Planning-only requests end with the reviewed plan. Implementation requests execute the authorized scope, QA/fix loops and required capture/checkpoint. If the owner-approved scope includes final check, perform Phase 8 as a separate authorized route after implementation-range; an Auto label alone is not a final-check trigger. Final-owner-yes must not be inferred.

Report `completed` only when all requested units satisfy DoD, actual QA and required capture. Report `partial / awaiting-owner` when owner decisions prevent full delivery; report `blocked` when no useful safe work remains for other reasons. Review completed work and disclose unverified/deferred areas. Distinguish technical completion from final owner acceptance.

Scoped local commits follow phase-commit-policy.md on the owned branch after applicable QA. Ignored-only/no-op creates no commit. Auto must not authorize push, merge, branch deletion or changes to another writer's index. Phase 8 closure commit requires actual final-owner-yes.

## Owner Report

Full Execution Trace records mode, scope/source, significant choices and pending/blocked units. At closure give result versus DoD, evidence, AI choices with override impact, owner decision queue and remaining scope. Do not manufacture questions when the queue is empty.

## Verification

Use check-execution-modes, synthetic readiness tests, producer-consumer audit and adversarial policy review. Green scripts remain supporting evidence; mode metadata never proves model behavior or interoperability with AI System.
