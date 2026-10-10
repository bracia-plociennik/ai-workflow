# Execution Modes

## Intent brief and private style context

Use intent-to-execution-brief.md during existing intake: minimal inline/embedded fields with provenance and disposition; preserve original request/accepted decisions as independent QA anchors. Batch triage and current action/phase ceilings remain first. This adds no phase or approval. Use style-profile.md for optional explicitly enabled local style; recording needs actual exact-target consent and minimal provenance/privacy, observations stay tentative and current instruction overrides profile. Invalid/disabled profile supplies no preferences. Auto chooses only covered reversible options and queues protected owner decisions; Human groups material questions, settled answers not repeated and noninteractive routes stay so.


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

## Source-bound Capability

The portable support record is `.systems/ai/capabilities/execution-modes-v1.json`, contract 1. Exact mode_mapping is auto -> auto and human -> human-coop; auto-unconstrained maps conceptually to auto-unbounded. Required behaviors: scoped-approval, dependency-local-blocking, auto-unconstrained, three-stalled-attempts, technical-phase-8 and human-material-questions.
Sources pin all approval, recovery, readiness and quality producer/consumer files listed by the pure inspector. Missing, unknown, linked, incomplete or stale metadata cannot establish support. Capability metadata never grants approval, proves native/model behavior or replaces a counterpart's own reviewed installed-source profile.

## Bounded Recovery

New readiness uses projection schema 2. Persist chronological attempts with unique attempt_id, unit_id, stable cause_id and optional progress_evidence SHA-256. The coordinator verifies meaningful progress and stable cause identity against real evidence; hashes and labels alone are declarations. Do not relabel a cause to reset its history. Preserve history across resume.
After three consecutive unproductive attempts for one unit and stable cause, exclude that unit, its dependents and shared reservations. A new, independently verified fingerprint resets only that cause's stalled count; repeated fingerprints and claimed progress do not. Different units/causes are counted separately; a stalled cause remains blocking until verified new progress addresses that cause.
Persist retry_counts per unit (spec, quality) and total for the run. Existing limits remain 2 Spec fix loops, 2 Quality fix loops and 32 total retries. An exhausted limit blocks further retries; progress never resets these budgets. The first reached limit wins. A budget override requires its existing explicit project decision, not an execution-mode field.
Schema 1 inspection remains readable and reports recovery_status legacy-unverified; it cannot attest the new guard. Fresh schema 2 readiness and reconstructed verified history/budgets are required for future execution relying on bounded recovery.

The chronological list is the authoritative declared attempt order. Unit IDs and cause IDs are stable across resume; the coordinator must not delete/reorder history or rename units/causes to evade limits. A newly introduced unit without any attempts may omit its zero-valued budget entry; any unit with attempt history requires explicit counters. Projection counters are declarations; aggregate the parent task/package's existing Spec/Quality budgets across its delegated units and verify them in real run state before execution. Splitting a task never grants another retry budget. Completion after the last allowed successful fix remains valid; execution beyond an exhausted budget does not.

## Verification

Use check-execution-modes, synthetic readiness tests, producer-consumer audit and adversarial policy review. Green scripts remain supporting evidence; mode metadata never proves model behavior or interoperability with AI System.
