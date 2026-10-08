# Cross-System Upgrade Handoff

## Metadata
- Date: 2026-10-08
- Source system: ai-workflow
- Counterpart: ai-system
- Status: accepted-for-handoff
- Implementation status: implemented on local branch codex/execution-modes-v1; not pushed or installed in the counterpart
- Privacy/scope check: pass
- Authority: advisory coordination context

## Concept And Intended Outcome
Default Auto reduces interaction during approved work, selecting covered reversible technical/preferences/local architecture choices and reporting assumptions and override costs. Explicit Human Coop consults material choices in 1-3 grouped questions. Mode is independent from technical autopilot.mode, phase and permissions.

## Owner Decisions
- Default Auto; Human Coop task-local unless explicitly project/session-wide.
- No deadline/timebox and no implicit 300-minute Auto run budget; retain explicit/legacy limits and retry/no-progress stops.
- Actual accepted concrete scope may cover named local high-risk implementation and formal Quality assessment, not its result.
- One handoff; no counterpart/nested edits, paid evals, push or merge.

## Cross-System Impact
- Owner decision: yes
- Counterpart: ai-system
- Handoff artifact: external-memory/memory/2026-10-08-execution-modes-ai-system-handoff.md

## Safety And Authority Boundaries
Mode never grants approval. New protected effects, production, costs, destructive actions, critical risk and platform approvals retain their boundaries. Git revert cannot undo exposure or external effects. One coordinator owns shared state, decisions, integrated QA and commits. Block affected units/dependents and unknown/shared resources; independent continuation requires actual verified evidence.

Legacy missing execution metadata does not gain autonomy. Resume preserves recorded mode and checks actual baseline, executors, gates and approvals. Planning-only ends with a reviewed plan. Phase8 requires a separately explicit scope and never implies final-owner-yes. Local scoped commits follow phase policy; no automatic push, main merge or branch deletion.

## Source-System References
- .systems/ai/core/execution-modes.md
- .systems/ai/core/owner-decision-checkpoints.md
- .systems/ai/core/autopilot.md
- .systems/ai/core/delivery-constraints.md
- .systems/ai/core/permissions.md
- .systems/ai/templates/autopilot/readiness.template.md
- .systems/ai/templates/autopilot/state.template.md
- .systems/ai/templates/autopilot/task-decisions.template.md
- .systems/ai/templates/autopilot/execution-readiness.template.json
- .systems/scripts/check-execution-modes
- .systems/scripts/lib/execution-modes.py
- .systems/scripts/tests/execution-modes.py

## Implemented Interface
check-execution-modes --state path.json is pure schema/readiness inspection, not dispatch or proof of authority. Schema1 records mode/scope/source/ref, unit actions and dependencies, resource claims and pending/agent-choice/owner-approved dispositions. It rejects malformed explicit modes, duplicate keys, linked input, cyclic/unknown dependencies, uncovered actions, empty implementation metadata and premature completion.
Summary decision IDs do not replace full decision request/alternatives/impact/artifact fields. Verify actual sources before acting.

## Actual Verification
28 offline tests, 16 supplemental smoke cases and full source validation passed after semantic current-diff, adversarial and producer-consumer review. Source-frozen full result=pass, exit0, duration763 seconds. Scripts are supporting-only. Post-commit QA/Phase7/Phase8 confirmation will be recorded in the owning source project; technical closure does not confer owner acceptance.

## Counterpart Adaptation Checklist
- [ ] Compare installed contracts; do not import historical status/approvals.
- [ ] Persist interaction mode separately from technical mode.
- [ ] Resolve task/session/project scope and resume identity.
- [ ] Qualify existing global decision stops into verified affected-unit blocking.
- [ ] Keep actual approval verification and protected-effect gates.
- [ ] Preserve full queued decision records and coordinator ownership.
- [ ] Remove only implicit new Auto time budget, not real limits.
- [ ] Test malformed modes, dependency/resource conflicts, partial completion, plan-only and explicit final-check boundaries.
- [ ] Adapt own quality/capture/commit policy through separately approved counterpart work.

## Privacy Check
- Raw client data included: no
- Secrets or credentials copied: no
- Private runtime or production identifiers copied: no
- Content: reusable workflow integration only; references repository-relative.

## Residual Risk
No model behavior eval, native dispatcher trial, real approval attestation or counterpart rollout was performed. Synthetic tests establish contract/inspector behavior, not perfect model judgment. Interoperability and installed AI System support remain unclaimed.
