# Workflow Operator Efficiency And Parity Handoff

## Metadata

- Date: `2026-07-24`
- Source system: `ai-workflow`
- Counterpart: `ai-system`
- Status: `accepted-for-handoff`
- Privacy/scope check: `pass`
- Raw client data included: `no`

## Improvement Proposal

Adapt the following system-level behaviors from AI Workflow into AI System:

1. Exact terminal completion phrases route to durable capture intent rather than an acknowledge-only response.
2. A target worktree can bootstrap a missing workflow clone only after a strong installation marker and platform-approved network/write action.
3. Semantic QA, DoD compliance, findings-first review, failure-path analysis, and product checks happen before applicable workflow scripts.
4. Workflow scripts remain supporting evidence and cannot independently justify `PASS`.
5. New planning, implementation, and QA scopes receive an advisory Luna/Sol recommendation.
6. Every substantive system upgrade records whether it should be mirrored to the counterpart system.

## Decisions

- `Koniec pracy` and `Koniec zadania` mean `capture-now`.
- Capture still respects QA, privacy, evidence, permissions, memory boundaries, and formal phase precedence.
- Worktree bootstrap uses the canonical upstream clone URL and stops on missing approval, weak markers, existing root instructions, wrong origin, dirty clone, or self-clone.
- Workspace layout remains unchanged.
- Luna High is recommended for bounded, reversible work; Sol High for high-impact, ambiguous, adversarial, security, migration, production, or broad integration work.
- Model choice is advisory-only.
- Cross-system impact remains an explicit owner decision; no-question opt-out cannot infer it.

## Safety Boundaries

- Do not turn completion wording into formal Quality PASS, final approval, or permission to bypass privacy and evidence.
- Do not clone into arbitrary directories or overwrite an existing workflow clone or root `AGENTS.md`.
- Do not use green system validators as a substitute for semantic or product QA.
- Do not let model recommendation change risk, permissions, approvals, DoD, or validation requirements.
- Do not include client data, secrets, credentials, production identifiers, or project-specific runtime details in cross-system handoffs.

## AI Workflow Reference Map

- `.systems/ai/core/cross-system-upgrade-handoff.md`
- `.systems/ai/core/end-of-task-capture.md`
- `.systems/ai/core/worktree-bootstrap.md`
- `.systems/ai/core/validation-routing.md`
- `.systems/ai/core/model-selection-guidance.md`
- `.systems/scripts/bootstrap-target-worktree`
- `.systems/scripts/check-cross-system-upgrade-handoff`
- `.systems/scripts/check-end-of-task-capture`
- `.systems/scripts/check-worktree-bootstrap`
- `.systems/scripts/check-validation-routing`
- `.systems/scripts/check-model-selection-guidance`

## Adaptation Checklist

- [ ] Map the AI System equivalents of source-of-truth, QA, memory, checkpoint, and approval contracts.
- [ ] Add exact completion triggers with formal-route precedence.
- [ ] Add a safe bootstrap preflight appropriate to AI System installation modes.
- [ ] Separate semantic/product QA from system validator execution.
- [ ] Add applicability fields to QA artifacts and templates.
- [ ] Add advisory model recommendation to planning, implementation, and QA output.
- [ ] Add explicit shared-impact owner decision and counterpart handoff.
- [ ] Add negative, compound-policy, producer-consumer, and local bare-remote smoke tests.
- [ ] Run AI System's own full quality closure and validation before adopting defaults.

## Validation Expectations

- Trigger tests must reject acknowledge-only behavior.
- Bootstrap tests must use a local bare remote and cover weak marker, missing approval, wrong origin, existing root instructions, dirty clone, and self-clone.
- QA tests must reject `green scripts = PASS` and broad workflow scripts during ordinary product implementation.
- Model tests must confirm both Luna and Sol classifications and `Blocking: no`.
- Shared-impact tests must reject `pending` at handoff and `yes` without a handoff artifact.

## Residual Risk

This artifact is advisory. AI System must adapt names, paths, runtime producers, and validators to its own contracts rather than copying AI Workflow implementation blindly.
