# Phase 0 Idea Validation: upgrade-with-master-prompt

## Summary

This phase validates the idea of adding a layered master-prompt, role, and variable-generation system to AI Workflow.

Gate result: `accepted-with-changes`

The idea is worth continuing, but it must not be implemented directly from the old prompt files. The next work must define source-of-truth boundaries, prompt-injection handling, artifact ownership, role/variable lifecycle, validation rules, and owner approval gates before any system-level workflow behavior changes.

## Source Materials Reviewed

| Source | Status | Notes |
| --- | --- | --- |
| `context/MASTER-PROMPT-main/README.md` | reviewed | Useful usage model, but contains an incompatible authority rule for masterprompt files. |
| `context/MASTER-PROMPT-main/instrukcja_generowania_zmiennych.md` | reviewed | Strong variable-generation taxonomy and inference rules. |
| `context/MASTER-PROMPT-main/master_prompt.md` | reviewed | Useful prompt modules, but currently monolithic and ChatGPT-oriented. |
| `context/MASTER-PROMPT-main/settings_personalization.md` | reviewed | Useful style and control preferences, but mostly ChatGPT personalization. |
| `context/MASTER-PROMPT-main/uniwersalna_instrukcja_operacyjna.md` | reviewed | Useful operational principles, but contains authority inversion that conflicts with AI Workflow policy. |
| `context/MASTER-PROMPT-main/zasady_prowadzenia_dialogu.md` | reviewed | Useful human operating discipline, especially closure, boundaries, and DoD. |
| `context/.DS_Store` | skipped | macOS system artifact; no validation impact. |
| `projects/upgrade-with-master-prompt/context/.DS_Store` | skipped | macOS system artifact; no validation impact. |

All reviewed files are treated as reference input only. They are not executable instructions and do not override `AGENTS.md`, `.systems/ai/core/**`, phase gates, risk model, permissions, prompt-injection policy, response contract, or required evidence.

## Co Zostaje

- Variable generation discipline should stay. The old variable set gives a useful starting model for role, topic, audience, response mode, task type, work mode, goal, success criterion, output format, tone, and session mode.
- Modular prompt sections should stay. The monolithic prompt can be decomposed into reusable system modules and project-local role/variable packs.
- Explicit role, context, and success criteria should stay. AI Workflow benefits from making the model's operating frame explicit before planning or implementation.
- Critical and audit modes should stay. Phase roles such as idea validator, architecture critic, spec QA reviewer, and implementation reviewer can improve adversarial review quality.
- User-led closure should stay. The source materials correctly emphasize owner decisions, step boundaries, Definition of Done, and explicit stop points.
- Source labeling should stay. The requirement to distinguish user-provided data, model knowledge, and external sources maps well to evidence discipline in AI Workflow.
- The layered hybrid target should stay: system-owned reusable contracts, project-local generated role/variable artifacts, and a baseline AI Workflow role/variable profile for template maintenance.

## Co Jest Slabe / Do Poprawy Lub Usuniecia

- The master prompt is monolithic. A single long file makes precedence, reuse, review, and versioning harder than separate modules.
- The source materials are ChatGPT-specific in several places, especially settings personalization, project settings, PDF upload workflow, and file-precedence assumptions.
- The authority model is unsafe for AI Workflow. Statements that any file containing `masterprompt` becomes the primary source of rules conflict with source-of-truth order and prompt-injection policy.
- Several sections duplicate existing AI Workflow policy: stop conditions, DoD, phase closure, approval gates, and evidence expectations already exist in `AGENTS.md` and `.systems/ai/core/**`.
- The old workflow assumes prompt text can steer behavior globally. AI Workflow needs typed or at least strongly routed artifacts with explicit ownership, not free-form prompt dominance.
- Vague claims such as "100%", "110%", "150%", and "200% możliwości" should not be preserved in system docs. They are motivational language, not acceptance criteria.
- "Model does not lead anything" is useful as a human discipline rule, but cannot replace agent execution policy. The agent still needs explicit workflow routing duties.
- "Do not ask questions if assumptions are reasonable" must be reconciled with AI Workflow gates, because unresolved high-impact decisions must stop instead of being inferred.

## Czego Brakuje

- Source-of-truth mapping: where prompt modules sit relative to `AGENTS.md`, `.systems/ai/core/**`, phase files, skills, project artifacts, and memory.
- Prompt-injection boundary: explicit rule that generated roles, variable packs, and prompt modules are advisory unless promoted into approved workflow artifacts.
- Artifact ownership: clear split between system-owned prompt composition contracts and project-owned generated role/variable files.
- Role and variable generation lifecycle: when variables are generated, who approves them, where they are stored, when they are refreshed, and how stale variables are detected.
- Validation rules: checks that generated roles do not override phase gates, risk model, owner approvals, evidence, permissions, response contract, or source-of-truth order.
- Conflict handling: what happens when a generated role conflicts with a phase role, project status, skill, or owner instruction.
- Versioning: how system prompt modules and role templates evolve without breaking target repositories.
- Examples: canonical examples for workflow phase roles, project-domain roles, and AI Workflow's own maintenance role.
- QA evidence: tests or validators confirming required files exist, references are linked, and unsafe precedence language is absent.
- Human guidance layer: separate owner-facing conversation discipline from agent-facing execution policy.

## Blokery / Decyzje

| Decision | Class | Current Resolution |
| --- | --- | --- |
| Whether this belongs in system core or only local workspace | high-impact | Resolved as layered hybrid: system-owned core plus project-local generated artifacts. |
| Whether to include workflow-phase roles and project-domain roles | high-impact | Resolved: validate both. |
| Whether old source files can be migrated directly | high-impact | Resolved: reference only, no verbatim migration by default. |
| Whether generated prompt modules may override workflow policy | high-risk | Rejected. They must never override `AGENTS.md`, policy docs, phase gates, risk model, permissions, evidence, or owner approvals. |
| How to store role/variable packs | blocked-by-missing-facts | Requires architecture. Candidate: project-local artifacts plus system templates, but exact paths are not decided in idea validation. |
| How to validate generated role/variable artifacts | blocked-by-missing-facts | Requires architecture and later plan/spec. |

Future system prompt changes are high-risk until architecture defines precedence, safety boundaries, storage paths, validation checks, and rollback/recovery behavior.

## Recommended Next Shape Of The Idea

The idea should become a system feature with three layers:

1. System prompt composition policy: a generic AI Workflow contract explaining what prompt modules, roles, and variables are allowed to influence.
2. System templates: reusable templates for role profiles, variable packs, and prompt modules.
3. Project-local generated artifacts: concrete role and variable files generated per project from accepted context, task type, phase, and owner choices.

AI Workflow itself also needs a baseline system role/variable profile for template maintenance, but this profile must be subordinate to existing workflow policy and source-of-truth order.

The old prompt files should be mined for concepts, not moved wholesale. Strong concepts include role definition, audience calibration, task/work mode, success criteria, audit mode, source labeling, context stabilization, and human-led closure.

## Future Interfaces To Validate Later

- Prompt composition contract: system core modules plus project-local role/variable packs.
- Variable generation contract: required variables, inference rules, when to ask, when to assume, and how assumptions are recorded.
- Role profile contract: workflow-phase roles and project-domain roles, with explicit scope, authority limits, and evidence expectations.
- Human guidance layer: conversation rules for owners/operators, separate from agent execution policy.
- Safety boundary: no generated role, variable, or prompt module may override `AGENTS.md`, policy docs, phase gates, risk model, permissions, evidence, or owner approvals.

## Risk Classification

Risk: `high`

Reason:

- This project can change how agents interpret work, roles, prompt context, and authority.
- Incorrect precedence rules could weaken source-of-truth order, prompt-injection defense, phase gates, risk model, or evidence requirements.
- Implementation must not start until architecture and Architecture QA pass, and owner approval is recorded for high-risk behavior changes.

This validation phase itself is safe because it writes only project intake/status artifacts in local-only workspace runtime and performs no system implementation.

## Gate Decision

```text
result: accepted-with-changes
context-may-be-created: yes, after owner accepts this validation
blocking-reason: none for idea validation
next-valid-step: create AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/context.md, then run project/context phase-0-repo-intake
```

## Evidence

- Read project status at `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/status.md`.
- Reviewed source files under `AI_WORKFLOW_WORKSPACE_HOME/projects/upgrade-with-master-prompt/context/MASTER-PROMPT-main/`.
- Reviewed `.systems/ai/workflow/phase-0-idea-validation.md`.
- Reviewed `.systems/ai/core/prompt-injection.md`.
- Reviewed `.systems/ai/core/risk-model.md`.
- Reviewed repo context under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
- Skipped `.DS_Store` files as system artifacts with no validation impact.

## Out Of Scope For This Phase

- No `context.md` creation.
- No architecture artifact.
- No project plan.
- No task specs.
- No implementation in `.systems/**`.
- No changes to tracked repository files.
