# Phase 0: Project Workspace

- Official repository: /Users/jakubplociennik/ai-system/onlinen-workspace/projects/ai-workflow
- Branch: codex/workflow-parity-and-runtime-integrity-v1
- Baseline HEAD: 0c767da0385723560d1b0d4794a9091316c23140
- Runtime: ignored local-only workspace/projects/workflow-parity-and-runtime-integrity-v1.
- Required routers: README.md, status.md, context.md, memory.md and tasks.md.
- Owned evidence: intake, architecture, planning, specs, tasks, implementation, quality, capture-state, decisions, reviews, distillations, checkpoints and memory.
- Intentionally absent unused namespaces: micro-tasks, change-requests, escalations and task packaging; create only if routed.
- Owner approvals are conversation authority documented in decisions/owner-decisions.md, not inferred from this artifact.
- No external handoff, product data, scheduler, model eval, commit/push or final-owner-yes performed.

## Delivery Constraints
- Mode: owner-opt-out
- Deadline: none
- Time budget: none
- Owner override: D4, no deadline or timebox.
- Must-have outcome: all seven accepted differences with no quality-floor weakening.
- Quality floor: testable DoD, semantic review, targeted regression and fresh full validation.
- Cutline rule: stop for a new material decision; never remove coverage to finish.
- Overrun checkpoint: not-applicable, owner opted out.

## Plan Quality Contract
- DoD source: accepted D1-D5 and this plan.
- Testable done conditions: seven routes covered by positive and negative fixtures; old smoke coverage unchanged; no foreign writes; phase 8 awaits owner.
- Plan classification: implementation-capable
- Artifact QA route: architecture-qa, plan-qa and spec-qa.
- Implementation QA route: phase-5-quality
- Required verification: current-diff review, producer-consumer audit, negative/failure-path tests, existing smoke suite, explicit full.
- Quality-ready criteria: no unresolved blockers/material findings; current input hashes and complete evidence.
- Opt-out/not-applicable reason: none for quality.
- Blocking decision: none; D1-D5 resolved.
- Next route: implementation slices after Spec QA.

## Owner Decision Checkpoint
- Interaction mode: none
- Decision state: clear
- Material decisions: D1-D5
- Questions asked: none; already answered.
- Auto-resolved reversible decisions: separate branch and task IDs.
- Optional owner refinements: none
- Decision artifacts: decisions/owner-decisions.md
- Next route: approved phases through 8; no final-owner-yes.

## Optional Knowledge Capture
- Capture recommended: yes
- Target: project-memory
- Reason: record integration boundaries and conservative evidence lessons.
- Owner decision required: no
- Owner decision: defer-to-distillation
- Privacy/scope check: pass
- Suggested entry title: Runtime integrity and selective overhead
- Suggested entry summary: Preserve quality while reducing accidental context and script cost.

