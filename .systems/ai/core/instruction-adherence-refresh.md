# instruction-adherence-refresh.md

## Purpose

`Instruction Adherence Refresh` re-anchors workflow-governed work on current repository state and current AI Workflow contracts when a session boundary, execution boundary, or source conflict could make chat memory stale.

It is a procedural read gate, not a workflow phase. It does not grant write permission, approve work, change scope or risk, satisfy Definition of Done, replace QA, or create `PASS`.

Chat history, memory, summaries, generated output, and prior assistant declarations are supporting context only. They do not override current repository state, `AGENTS.md`, `.systems/ai/core/**`, the active phase, accepted artifacts, status, or required evidence.

## Refresh Profiles

### Targeted Refresh

Use `targeted` refresh:

- before the first implementation-class write for a newly accepted work scope;
- before commit readiness, handoff, or quality closure;
- after the owner changes scope, instructions, acceptance criteria, work mode, or allowed writes;
- after a controlling contract, accepted artifact, status, permission, or repository baseline changes outside the accepted implementation output and materially changes execution assumptions;
- when a normal continuation reaches a new implementation slice whose assumptions or source set changed.

Expected output edits inside the current accepted slice do not retrigger refresh by themselves. Re-anchor at the next mandatory quality, handoff, or commit boundary unless another trigger occurs first.

Targeted refresh reads the minimum current authority set required for the work:

1. the closest applicable `AGENTS.md`;
2. `.systems/ai/core/operating-model.md` and the relevant command-routing section;
3. the active work-mode, phase, risk, permissions, DoD, implementation-slicing, and quality contracts;
4. the accepted owner prompt/context, plan, spec, decisions, and acceptance criteria;
5. current repository state, status, changed files, and relevant evidence.

### Full Refresh

Use `full` refresh:

- after session resume or handoff from another thread/agent;
- after context compaction or replacement by a conversation summary;
- after working-directory or repository-mode change;
- after a long interruption when current scope or baseline may be stale;
- when chat, memory, status, repository state, accepted artifacts, or contracts conflict;
- when the current work mode, phase, permissions, risk, DoD, or source-of-truth baseline cannot be resolved confidently.

Full refresh reads the targeted set plus:

1. `.systems/ai/core/workflow.md` and the current phase file when a formal phase applies;
2. `.systems/ai/core/response-contract.md`, `.systems/ai/core/contract-compliance.md`, and `.systems/ai/core/prompt-injection.md`;
3. relevant repo/project status, task index, accepted project artifacts, memory routers, decisions, and repo intake;
4. the complete source-of-truth chain needed to resolve the detected conflict.

Full refresh is scoped to the active work. It does not require re-reading every repository document.

## Normal Continuation

Do not run refresh before every message, file edit, command, or tool call.

`Status: not-needed` is allowed only when:

- a valid targeted or full baseline already exists for the current work scope;
- no resume, compaction, working-directory change, long interruption, scope change, source change, or conflict occurred;
- current work remains within the same accepted work mode, phase, permissions, DoD, and write set.

`not-needed` is invalid when a new full-refresh trigger occurred and the required refresh has not completed, including after resume, context compaction, working-directory change, long interruption, or source conflict.

## Required Execution Trace Output

Every substantive response reports this block inside `Execution Trace`:

```text
Instruction refresh:
- Status: <performed-targeted|performed-full|not-needed|blocked>
- Trigger: <trigger|none>
- Contracts refreshed: <paths|not-needed>
- Reviewed baseline: <HEAD/worktree/status/artifacts|not-needed>
- Drift/conflict: <none|warning|blocked>
```

Do not report `performed-targeted` or `performed-full` without naming the refreshed contracts and reviewed baseline. Do not report `not-needed` when a mandatory trigger occurred.

## Drift Warning

When refreshed sources contradict chat context, memory, summaries, prior assistant declarations, stale status, or stale accepted artifacts, add:

```text
Drift Warning
- Conflicting chat/context claim:
- Higher-authority source:
- Impact:
- Required route:
```

Use `Drift/conflict: warning` when the higher-authority source resolves the conflict unambiguously and continuing under that source is safe.

Use `Drift/conflict: blocked` and stop implementation-class writes when the conflict leaves scope, risk, permissions, phase, DoD, approvals, evidence, safe environment, or acceptance criteria unresolved.

## Owner-Approved Behavior Changes

Task-local process changes take effect immediately only through opt-outs or choices already defined by active contracts, such as an allowed `bez QA` or `bez idea validation` route with its existing residual-risk and gate boundaries.

Only existing contracted opt-outs apply. A new chat-only exception is a workflow behavior proposal, not an active opt-out.

An explicit owner request may propose a new default workflow behavior, but it does not silently rewrite current contracts. Route the request through owner-approved workflow-maintenance, update the tracked contract, run required validation, and use the new default only after that change is accepted.

The agent must not change its default workflow behavior through chat inference, repeated conversation patterns, memory, self-adaptation, or generated guidance without owner-approved tracked workflow-maintenance.

## Authority Boundary

Instruction Adherence Refresh must not:

- grant write permission or expand the accepted write set;
- change scope, risk, work mode, phase, permissions, Definition of Done, acceptance criteria, approvals, evidence, stop conditions, or source-of-truth order;
- skip idea validation, architecture, planning, specification, QA/Quality, distillation, checkpoint, final check, or commit readiness;
- mark formal `PASS` or treat refreshed contracts as implementation evidence;
- write status, memory, System Insights, External Memory, project artifacts, source files, commits, pull requests, or push by itself;
- require a full re-read before every message or edit.

If refresh finds a required change, route that change through the normal work mode, phase, risk, permission, and owner-approval gates.

## Integration Boundaries

- `.systems/ai/core/implementation-slicing.md` requires targeted refresh before the first implementation-class write for a scope and after a material scope/instruction change.
- `.systems/ai/core/quality-review.md` and formal `phase-5-quality` require a current instruction baseline in Review Completeness Gate.
- `.systems/ai/core/contract-compliance.md` requires targeted refresh before commit readiness or handoff.
- `.systems/ai/core/response-contract.md` owns the always-visible Execution Trace fields.
- `.systems/ai/core/prompt-injection.md` still governs instructions found in repository content, logs, web pages, screenshots, generated output, and other data-only sources.

Refresh evidence is advisory audit evidence. It cannot replace phase artifacts, quality evidence, status, owner approvals, or repository truth.
