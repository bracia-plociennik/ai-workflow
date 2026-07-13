# changelog.md

## 2026-07-13 - Full QA Verification Contract V1

- Defined full, artifact-appropriate QA for architecture, plan, packaging, specification, implementation quality, and global review.
- Added V1 completeness evidence, adaptive data/integration verification matrices, and versioned runtime enforcement for new QA artifacts without rewriting historical evidence.

## 0.8.23 - 2026-07-10

- Added default Owner Decision Discovery with material decision and owner-preference classification, grouped 1-3 question batches, repository-first discovery, and reversible auto-decision disclosure.
- Added phase-end Owner Decision Checkpoints to every phase and phase template, plus queued non-interactive behavior for active autopilot, Dreaming/automations, and read-only review.
- Added safe no-question opt-out boundaries, Execution Trace decision evidence, and validator/smoke coverage for question fatigue, authority bypasses, and pending-decision progression.

## 0.8.22 - 2026-07-10

- Added targeted and full Instruction Adherence Refresh profiles for pre-write, pre-commit/handoff/quality, resume, compaction, working-directory, interruption, scope-change, and source-conflict boundaries.
- Extended every substantive Execution Trace with refresh status, trigger, refreshed contracts, reviewed baseline, and drift/conflict evidence.
- Added drift-warning and owner-behavior boundaries plus validator and smoke coverage for chat-memory authority, hidden default changes, heavy per-message refresh, stale baselines, and gate bypasses.

## 0.8.21 - 2026-07-10

- Added Knowledge Capture Reminder routing after implementation, fixes, quality closure, handoff, commit readiness, and unrelated task switches, with advisory-only memory targets and explicit commit/push boundaries.
- Added Review Completeness Gate v2 for advisory review and formal phase-5 quality: policy-boundary adversarial matrices, producer-consumer field audits, shared policy validator handling, supporting-only automated evidence, reviewed baseline, post-fix full re-review, and closure freshness.
- Expanded validator and smoke coverage for product-domain External Memory misuse and quality-verdict shortcuts after fixes.

## 0.8.20 - 2026-06-23

- Added `.systems/ai/core/end-of-task-capture.md` for chat-end knowledge capture prompts such as `to koniec zadania`, `dziękuję, utrwal wiedzę`, and `end task and capture knowledge`.
- Preserved precedence for `final-owner-yes`, change requests, explicit formal phases, global quality review, and commit readiness before End-of-Task Capture.
- Added `.systems/ai/templates/capture/end-of-task-capture.template.md` plus validator and smoke coverage for required fields, routing conflicts, unsafe PASS/final-check/project-close wording, raw client System Insights, and product-domain External Memory misuse.

## 0.8.19 - 2026-06-22

- Added Default Idea Validation routing: single new work uses Task Idea Validation, broad project ideas use formal `phase-0-idea-validation`, and owner lists use request batch triage plus the selected validation route.
- Added explicit owner opt-out grammar for idea validation and required `Idea validation skipped by owner opt-out` reporting with residual risk in `Execution Trace`.
- Clarified that idea-validation opt-out cannot bypass source-of-truth order, risk model, permissions, safe environment checks, required evidence, QA/Quality, owner approvals, phase gates, change-request routing, or final owner approval.
- Added `.systems/scripts/check-default-idea-validation-opt-out` with smoke coverage for default validation routing, opt-out reporting, and unsafe bypass wording.

## 0.8.18 - 2026-06-22

- Added `Execution Trace` for substantive responses with sources, evidence, workflow procedures, skills/roles, commands/checks, skipped sources, and residual uncertainty before the final `Co dalej?` footer.
- Added Phase Skill Discovery so phases and procedures check existing workspace skills before system skills and report `Skills used: none` when no matching active `SKILL.md` exists.
- Added Default Quality Closure for substantive work, using formal QA/Quality where available and advisory global quality review otherwise, with owner opt-out reporting and residual risk.
- Added validators and smoke tests for response trace, phase skill discovery, and default quality closure.

## 0.8.17 - 2026-06-22

- Added `.systems/ai/core/request-batch-triage.md` for owner-provided lists, checklists, brain dumps, mixed improvements, and `2+ owner items`.
- Required a triage matrix with item, group, theme, risk, routing, target project/workspace, dependencies, owner decision, and reason before ordinary task intake for multi-item requests.
- Clarified grouping, split, high-risk, mixed active-project/repo-level, and change-request-candidate rules.
- Added `.systems/scripts/check-request-batch-triage` with smoke coverage for missing contract, missing matrix fields, mixed-list splitting, unsafe automatic implementation wording, and high-risk routing.

## 0.8.16 - 2026-06-19

- Added `.systems/ai/core/quality-review.md` for read-only/advisory global quality review stance.
- Routed review, code review, final review, findings, blockers, and generic quality-check prompts through the global review stance unless formal `phase-5-quality` is resolvable.
- Clarified that advisory review is findings-first and cannot mark formal `PASS`/`FAIL`, create quality artifacts, update status, or trigger `phase-8-final-check`.
- Added `.systems/scripts/check-global-quality-review-stance` with smoke coverage for routing, unsafe PASS/final-check wording, and findings-first output fields.

## 0.8.15 - 2026-06-19

- Added `.systems/ai/core/dreaming-mode.md` for advisory-only AFK/nightly Dream Reports.
- Added the target-owned `AI_WORKFLOW_WORKSPACE_HOME/dreams/runs/` namespace and bootstrap templates for Dream Reports.
- Defined `workflow-artifacts-only` and owner-requested `full-repo` Dreaming Mode variants, with prompt-injection, privacy, full-repo exclusion, and no-scheduler boundaries.
- Added `.systems/scripts/check-dreaming-mode` plus smoke coverage for missing policy/template fields, unsafe automatic-write wording, raw client data, invalid full-repo reports, and workspace update preservation.

## 0.8.14 - 2026-06-15

- Added context-intake routing for system and workspace skills: `<skill>/context/**` is raw source data, not active guidance.
- Required `skill-intake-plan.md` before context-driven skill builds write final `SKILL.md`, `README.md`, or resource artifacts.
- Added `.systems/ai/templates/workspace/skills/skill-intake-plan.template.md` for reviewed sources, trigger fit, keep/fix/missing/blockers, artifact map, approval, validation, and residual risk.
- Extended skill validators and smoke tests to enforce compact `SKILL.md` contracts, block `context/**` authority grants, require intake plans when context and active artifacts coexist, and allow source-like filenames under system skill `context/**`.
- Updated `skill-creator` scaffolding so `--resources context` creates a raw source directory plus an intake plan skeleton.

## 0.8.13 - 2026-06-15

- Added phase-level `Optional Knowledge Capture` to every workflow phase and workflow phase template.
- Defined the soft capture taxonomy for project memory, repo memory, External Memory, System Insights, decision artifacts, status, and none.
- Added `.systems/scripts/check-knowledge-capture-gate` with smoke coverage for missing blocks, missing fields, hard-gate regressions, and valid no-capture decisions.
- Clarified that phase capture is advisory and does not create automatic durable memory writes or replace phase 6 distillation, phase 7 checkpoint, phase 8 final-check capture, owner approvals, or memory scope boundaries.

## 0.8.12 - 2026-06-15

- Defined the system skill layout contract with canonical `SKILL.md` agent contracts and short `README.md` human summaries.
- Added `.systems/scripts/check-system-skills` plus validator smoke coverage for skill frontmatter, authority boundaries, unsafe external-model markers, undeclared YAML imports, and external CDN resources.
- Exempted `AI_WORKFLOW_WORKSPACE_HOME/skills/<skill>/context/**` supporting source materials from strict Markdown filename checks.
- Preserved the imported Anthropic `skill-creator` under `.systems/ai/skills/legacy/skill-creator-old/` as context/data only.
- Added the active `.systems/ai/skills/skill-creator/` system skill contract with AI Workflow-native resource routing, A/B eval schemas, expectation-level grading, timing/metrics benchmark aggregation, trigger-description review, grader/analyzer/comparator rubrics, offline review templates, and stdlib-only scaffold/validation/eval/report/packaging helpers.

## 0.8.11 - 2026-06-12

- Added `.systems/ai/core/contract-compliance.md` for advisory work mode compliance and commit readiness knowledge capture decisions.
- Added `.systems/scripts/check-contract-compliance` plus validator/smoke coverage for the contract references and micro-task/micro-project template hints.
- Updated DoD, command routing, workflow routing, human docs, and micro-task/micro-project templates to require explicit `Knowledge capture: required|not-required` decisions before commit or handoff.

## 0.8.10 - 2026-06-12

- Added `.systems/scripts/update-workspace` as an idempotent workspace schema backfill for existing target-owned workspaces after upstream updates.
- Updated `update-from-upstream` to print a copy-paste `update-workspace` command after successful completion without modifying `AI_WORKFLOW_WORKSPACE_HOME/**` itself.
- Documented the split between fresh `phase-0-init` bootstrap and existing-workspace schema backfill.
- Added validator and smoke coverage for the new workspace update path.

## 0.8.9 - 2026-06-12

- Added `.systems/ai/core/system-insights.md` for anonymized cross-project operating lessons, privacy rules, categories, status lifecycle, write routing, and skill-candidate boundaries.
- Added `AI_WORKFLOW_WORKSPACE_HOME/system-insights/` bootstrap templates and documentation examples for frontend, backend, client-work/process, and skill-candidate insights.
- Kept External Memory scoped to AI Workflow improvement proposals and routed product-domain lessons to System Insights instead.
- Connected System Insights to phase 6 candidates, phase 7 checkpoint writes, phase 8 privacy/scope checks, command routing, guide mode, human docs, and repo intake.
- Added `.systems/scripts/check-system-insights` plus validator smoke coverage for missing privacy checks, missing operational validation, raw client data, and product-domain lessons in External Memory.

## 0.8.8 - 2026-06-11

- Added `.systems/ai/core/prompt-composition.md` for advisory prompt modules, role profiles, variable packs, project-local prompting lifecycle, and authority boundaries.
- Added reusable prompt composition templates under `.systems/ai/templates/prompting/`.
- Routed prompt composition questions through `AGENTS.md`, workflow routing, and command routing without changing phase gates or approval rules.
- Added `.systems/scripts/check-prompt-composition` plus required artifact and smoke coverage for prompt composition files and unsafe-authority grant patterns.
- Added human guidance and documentation-only examples under `.systems/ai/examples/prompting/`.

## 0.8.7 - 2026-06-10

- Added `.systems/ai/core/parallel-work-policy.md` as the formal status-only coordination policy for multiple projects, tasks, micro-tasks, micro-projects, and Codex threads.
- Clarified that `repo/core/status.md` is a repo focus snapshot, while each `projects/<project>/status.md` owns project execution state.
- Added command routing, guide, human runbook, and validator references for parallel work questions.
- Kept v1 parallel coordination lock-free: no new lock files, scheduler state, or status fields.

## 0.8.6 - 2026-06-10

- Removed the tracked runtime exception for `ai-workflow-workspace/**` in the official workflow repository.
- Updated `.systems/scripts/check-branch-policy` so tracked `workspace/**` and `ai-workflow-workspace/**` fail in every policy mode.
- Updated validator smoke coverage so `AI_WORKFLOW_BRANCH_POLICY=dev` cannot bypass the `ai-workflow-workspace/**` tracking block.
- Clarified that target repositories may commit their sibling `ai-workflow-workspace/**`, while the official nested `ai-workflow/` clone must not track runtime.

## 0.8.5 - 2026-06-09

- Added formal Autopilot Range Model with `planning-range` for phase 1 through phase 3 Spec QA and `implementation-range` for phase 4 through phase 7 checkpoint.
- Made `phase-8-final-check` owner-triggered only and removed it from automatic autopilot execution.
- Extended readiness, state, ledger, events, run README, command routing, guide, workflow routing, and human docs with range-aware start and stop conditions.
- Made checkpoint cadence a hard gate for implementation-range autopilot after every 3 completed tasks/packages and after the final task/package.

## 0.8.4 - 2026-06-08

- Added `phase-0-init` as the first bootstrap phase after cloning AI Workflow into a target repository.
- Extended `.systems/scripts/init-workspace` to create `repo/core/init.md`, preserve safe legacy context, and write `repo/legacy/legacy-index.md`.
- Updated install, guide, command routing, repo intake, workflow routing, templates, and validators so fresh target repos route through init before repo intake.
- Added smoke coverage for fresh workspace init, legacy preservation, root `AGENTS.md` owner-merge blocking, and `.env` non-copy behavior.

## 0.8.3 - 2026-05-27

- Added `.systems/ai/core/repository-modes.md` and `.systems/scripts/resolve-workflow-env` to formalize official repo mode versus target repo mode.
- Split target runtime out of the nested clone: public `main` no longer tracks `workspace/**`.
- Added `AI_WORKFLOW_WORKSPACE_HOME`, normally `ai-workflow-workspace/`, as the target-owned tracked runtime workspace.
- Added `.systems/scripts/check-branch-policy` to block runtime workspace files on public `main`; this rule was later tightened in `0.8.6` to block tracked `ai-workflow-workspace/**` in every policy mode.
- Added `.systems/scripts/init-workspace` and workspace bootstrap templates.
- Changed target root `AGENTS.md` shim handling to local-only via `.git/info/exclude` together with `/ai-workflow/`.
- Updated `update-from-upstream` so it updates only the nested `ai-workflow/` clone and never touches `AI_WORKFLOW_WORKSPACE_HOME/**`.
- Added `/workspace/` to the public template `.gitignore` to prevent accidental runtime commits on `main`.

## 0.8.2 - 2026-05-25

- Added mandatory run-scoped Autopilot Readiness Audit before starting or resuming autopilot.
- Added `.systems/ai/templates/autopilot/readiness.template.md` and connected it to autopilot runtime templates.
- Updated autopilot routing, guide, response contract, workflow aliases, human docs, and validators so autopilot cannot enter `running` before readiness is `ready`.

## 0.8.1 - 2026-05-25

- Added `.systems/ai/core/task-intake.md` as the mandatory Task Idea Validation lens for new tasks, planning requests, approach requests, side-tasks, micro-tasks, change requests, and autopilot requests.
- Required new task responses to identify what stays, what is weak or should change, what is missing, blockers/decisions, and recommended routing before presenting a plan.
- Connected task intake to `AGENTS.md`, command routing, operating model, workflow routing, response contract, human documentation, and validators.

## 0.8.0 - 2026-05-21

- Split the nested clone into system-owned `.systems/**` and target-owned `AI_WORKFLOW_WORKSPACE_HOME/**`.
- Made `update-from-upstream` block dirty system-owned files and preserve the full `AI_WORKFLOW_WORKSPACE_HOME/**` tree.
- Moved External Memory to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` with detailed entries in `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/`.
- Added `AI_WORKFLOW_WORKSPACE_HOME/skills/` for user-defined local skills that take precedence over system skills as supporting guidance.
- Moved EXAMPLE workspaces to `.systems/ai/examples/` so active runtime stays under `AI_WORKFLOW_WORKSPACE_HOME/`.

## 0.7.4 - 2026-05-21

- Added `.systems/ai/core/change-requests.md` as the formal owner change request policy before and after `final-owner-yes`.
- Added project-local change request router, directory templates, and EXAMPLE artifacts.
- Updated final check, command routing, guide, workflow routing, and project workspace setup to block final approval on open pre-final change requests and route post-final changes safely.

## 0.7.3 - 2026-05-20

- Added `.systems/ai/core/response-contract.md` as the canonical user-facing response contract.
- Required substantive Codex responses to end with `Co dalej?`, one recommendation with impact and copy-paste prompt, and one safe alternative with impact and copy-paste prompt.
- Connected the response contract to `AGENTS.md`, operating model, workflow routing, guide mode, command routing, and human documentation.

## 0.7.2 - 2026-05-20

- Flattened the old internal documentation namespace so the nested clone now uses `.systems/ai/`, `AI_WORKFLOW_WORKSPACE_HOME/repo/`, `AI_WORKFLOW_WORKSPACE_HOME/projects/`, `AI_WORKFLOW_WORKSPACE_HOME/humans/`, and `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` directly.
- Moved canonical AI router and policy files into `.systems/ai/core/` while keeping workflow phases, templates, skills, memory entries, and external-memory entries in their dedicated directories.
- Moved canonical repo runtime routers into `AI_WORKFLOW_WORKSPACE_HOME/repo/core/` while keeping detailed repo context, legacy, and memory entries in `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`, `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`, and `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/`.
- Moved validators from the old nested validator subdirectory to `.systems/scripts/` for the nested-clone installation model.

## 0.7.1 - 2026-05-20

- Added project-local `micro-tasks.md` and `micro-tasks/` plus repo-level `AI_WORKFLOW_WORKSPACE_HOME/micro-projects/` for low-risk work that does not need full workflow phases.
- Added the official `update-from-upstream` flow for safely updating target repository nested clones while preserving runtime, workspaces, local External Memory, and legacy source filenames.
- Excluded preserved legacy workflow inputs under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` and detailed repo context entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/` from strict Markdown naming checks while keeping canonical repo context at `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`.
- Added `AI_WORKFLOW_WORKSPACE_HOME/repo/core/legacy.md` as the canonical router and summary for preserved legacy material under `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/`.
- Simplified canonical accepted project context from the previous nested context-file model to `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context.md`.
- Excluded supporting project source materials under `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/context/` from strict Markdown naming checks while keeping canonical project `context.md` required and status-validated before architecture and later phases.
- Added validator smoke coverage for legacy/context naming exemptions and missing canonical project context.

## 0.7.0 - 2026-05-19

- Changed the target-repository installation model to a nested clone at `ai-workflow/`.
- Added `.systems/ai/templates/root-agents.template.md` as the only file that target repositories need to copy or merge into root `AGENTS.md`.
- Clarified `TARGET_REPO_ROOT` and `AI_WORKFLOW_HOME` path resolution across the root shim, internal `AGENTS.md`, installation policy, guide, command routing, repo intake, and workflow router.
- Updated repo intake to treat `ai-workflow-workspace/repo/` as runtime that must be replaced with target-repository facts after installation.
- Kept target-owned `docs/`, `.systems/`, `.github/`, `README.md`, `HUMANS.md`, and existing `AGENTS.md` out of the default install path.

## 0.6.0 - 2026-05-19

- Converted repo context into `context.md` router plus detailed entries under `AI_WORKFLOW_WORKSPACE_HOME/repo/context/`.
- Clarified `plans.md` as a router to canonical `planning/` artifacts.
- Converted `tasks.md` into a task index/router with optional task cards under `tasks/`.
- Added project `reviews/` for review artifacts while keeping `quality/` as QA evidence.
- Converted autopilot runtime to run directories under `autopilot/runs/autopilot-XXX/`.

## 0.5.0 - 2026-05-18

- Moved workflow-owned docs under `docs/`.
- Moved workflow validators under `.systems/scripts/`.
- Added installation collision policy for existing target repositories.
- Clarified that target-owned `README.md`, existing `AGENTS.md`, existing `HUMANS.md`, `docs/`, `.systems/`, and `.github/` must not be overwritten.
- Added `.systems/ai/skills/` as the reserved space for reusable task-specific workflow skills.
- Added `.systems/ai/core/command-routing.md` as the bilingual catalog for user-facing workflow commands and safe command interpretation.
- Added `.systems/ai/core/guide.md` for lost-user, next-step, fresh-start, and recovery guidance.
- Added `phase-0-project-workspace` for creating project and human workspaces after repo intake.
- Added `AI_WORKFLOW_WORKSPACE_HOME/repo/legacy/` for preserving pre-existing repository workflow material as context-only legacy input during repo intake.
- Moved project context into a dedicated project context area.
- Added human-facing `plans.template.md`.
- Renamed repo runtime context template to `context.template.md` to match `AI_WORKFLOW_WORKSPACE_HOME/repo/core/context.md`.
- Clarified that the literal `repo intake` prompt is sufficient for repo-level bootstrap when AI Workflow is installed.

## 0.4.0 - 2026-05-18

- Converted workflow filenames to lowercase kebab-case.
- Added policy docs for operating model, Definition of Done, permissions, risk, commands, prompt injection, rollback, dependencies, and deprecation.
- Converted `AGENTS.md` into a short execution router.
- Added automatic workflow validation scripts and GitHub Actions workflow.
- Added Codex configuration templates.
- Added canonical task ID model and project task index.

## 0.3.0 - 2026-05-18

- Moved repo-specific runtime facts to `AI_WORKFLOW_WORKSPACE_HOME/repo/`.
- Added idea validation phase.
- Renamed legacy singular human docs path to `AI_WORKFLOW_WORKSPACE_HOME/humans`.
- Made Codex the primary executor with ChatGPT as optional support.
