# commands.md

Official dev workspace publication: run `.systems/scripts/check-workspace-publication` against the staged index, or add `--ref HEAD` for the committed snapshot. `check-branch-policy` permits only actual official dev or verified detached CI targeting dev; main/other branches and nested installations remain forbidden. CI full source verification uses a separate empty `AI_WORKFLOW_WORKSPACE_HOME`; it does not attest current runtime QA. Use `/tmp` for validation output.
Execution Modes: use check-execution-modes for contract/capability validation and check-execution-modes --state <execution-readiness.json> for pure declared readiness inspection. Schema 2 adds persisted stable-cause recovery and stricter retry budgets; schema 1 remains legacy-unverified. Source-bound capability is support metadata, not approval or installed counterpart compatibility. See execution-modes.md; the inspector neither dispatches workers nor verifies actual approval/resource evidence.
Read-only cross-system inspection: `.systems/scripts/inspect-parallel-compatibility
--workflow PATH --repo PATH --run FILE --mapping FILE`. See
`parallel-compatibility.md` and `compatibility.template.json`. Exit0 means static
inspection only; no native dispatch, operational support, saved transition or PASS.
For future approved scopes, use `.systems/ai/core/phase-commit-policy.md` at planning-range end and phases 6/7/8. Explicit no-commit is not overridden; current PTO approval is non-retroactive. Ignored-only/no-op creates no commit. Phase8 requires actual final-owner-yes, counterpart impact must be resolved, one coordinator owns the index, and push is never inferred. Bound V3/schema3 is opt-in and current-only; unsupported proof needs fresh QA. Fresh owned artifact closure remains separate from source equivalence. Validator: `check-phase-commit-policy`.


Execution efficiency commands follow `.systems/ai/core/execution-efficiency.md`. Use `prepare-quality-record --review <supplied-json> --workflow-root <root> --workspace-root <workspace> --project <slug>` for canonical QA publication. `check-execution-efficiency` checks contracts; `check-execution-efficiency --behavioral` tests the seven capabilities, also exercised by full smoke. Full source receipts and fresh artifact closure are explicit commands, not automatic skip flags.

## Explicit Scoped Evidence

Generate a manifest read-only, then pass its unchanged path to scoped validation:

```sh
python3 .systems/scripts/lib/validation-scope.py snapshot --repo "$TARGET_REPO_ROOT" --workspace "$AI_WORKFLOW_WORKSPACE_HOME" --base <approved-base> --scope <approved-path> --runtime-root projects/<project> --intent checkpoint
.systems/scripts/validate-workflow --profile scoped --checks check-distillation-state --scope-manifest <saved-json> --explain
```

The snapshot command emits JSON only; the owner-approved local artifact writer
may save it outside tracked source. `--scope` and `--runtime-root` may repeat.
Select checks explicitly; the registry adds dependencies but never infers
selection. Include all runtime-required checks for checkpoint eligibility:
`check-distillation-state,check-qa-evidence,check-status-consistency,check-naming,check-contract-compliance,check-full-qa-verification`.
No manifest means unverified coverage. Report execution/coverage/eligibility
separately; source/system impact escalates to full. CI/updater stay explicit full.

## Purpose

Runtime integrity: `.systems/scripts/check-runtime-integrity` runs synthetic regressions; `.systems/scripts/report-coordinator-status --project <slug> --format json|human` is read-only and never grants execution authority. See runtime-integrity.md for canonical capture inventory and safe fixture/scorer inputs.

Codex must know how to verify work. Repository-specific commands live in `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`. This file defines the required command categories and workflow-template checks.

## Required Command Categories

### Parallel Protocol Commands

See `parallel-task-orchestration.md` and `runtime-integrity.md` before use.
`plan-parallel-work --manifest <owned-manifest> --format json|human` is a read-only
allocation proposal, not dispatch. `manage-parallel-run --run-root <owned-run>
--coordinator-id <owner> validate|reconcile` inspects state. Explicit `transition
--expected-revision <n> --request <closed-json>` requires the existing approved
write scope; it records metadata, never spawns, copies, merges or approves work.
`report-coordinator-status --project <slug> --schema-version 2` opts into installed
protocol metadata; schema1 remains default. Native backend is unverified, all
execution authority false; missing/unsafe capability uses unknown/serial.
Verification: `check-parallel-task-orchestration` and offline
`python3 .systems/scripts/lib/parallel-orchestration-tests.py --case
planner|protocol|lifecycle|integration|compatibility`. These are supporting checks,
not a replacement for integrated semantic QA or authentic runtime isolation.

Each target repository should define these in `AI_WORKFLOW_WORKSPACE_HOME/repo/core/repo-intake.md`:

- Install
- Development server
- Lint/style
- Typecheck/static analysis
- Unit tests
- Integration tests
- E2E/browser tests
- Build
- Migration/schema check
- Scheduler/cron/queue check

If a command is not configured, write `not configured`. Do not invent commands.

## Before Final Answer

For implementation work, run the relevant configured checks for the changed area.

For final workflow-template maintenance, reuse checks, checkpoint validation, major verification, or other high-impact changes, run the explicit `full` profile. The no-arg `.systems/scripts/validate-workflow` remains the `standard` profile for daily iteration.

```sh
git diff --check
.systems/scripts/validate-workflow --profile full
.systems/scripts/check-naming
.systems/scripts/check-required-artifacts
.systems/scripts/check-status-consistency
.systems/scripts/check-qa-evidence
.systems/scripts/check-full-qa-verification
.systems/scripts/check-system-insights
.systems/scripts/check-system-skills
.systems/scripts/check-contract-compliance
.systems/scripts/check-knowledge-capture-gate
.systems/scripts/check-default-quality-phase-chaining
.systems/scripts/check-dreaming-mode
.systems/scripts/check-global-quality-review-stance
.systems/scripts/check-review-completeness-gate
.systems/scripts/check-intent-plan-spec-compliance-review
.systems/scripts/check-implementation-slicing
.systems/scripts/check-plan-quality-contract
.systems/scripts/check-validation-profiles
.systems/scripts/check-validation-completion
.systems/scripts/check-knowledge-capture-reminder
.systems/scripts/check-instruction-adherence-refresh
.systems/scripts/check-owner-decision-checkpoints
.systems/scripts/check-request-batch-triage
.systems/scripts/check-response-evidence-trace
.systems/scripts/check-phase-skill-discovery
.systems/scripts/check-default-quality-closure
.systems/scripts/check-default-idea-validation-opt-out
.systems/scripts/check-end-of-task-capture
.systems/scripts/check-cross-system-upgrade-handoff
.systems/scripts/check-worktree-bootstrap
.systems/scripts/check-validation-routing
.systems/scripts/check-model-selection-guidance
```

The full validator emits `AI_WORKFLOW_VALIDATE_START`, progress markers, and
exactly one `AI_WORKFLOW_VALIDATE_COMPLETE` marker. Use
`--progress summary|verbose|quiet` to control detail. Slow nested checks are
bounded by the portable `.systems/scripts/run-with-timeout` wrapper; timeout
returns code `124` and is not a passing validation result. The updater uses
`--profile full --progress summary` and also reports canonical upstream state;
an `ahead` or `diverged` nested clone stops before validation.

`check-knowledge-capture-gate` validates the phase-level `Optional Knowledge Capture` blocks and keeps them advisory rather than mandatory durable memory writes.

`check-default-quality-phase-chaining` validates default working-phase to QA/Quality chaining, owner opt-out wording, and owner-requested task packaging boundaries.

`check-dreaming-mode` validates the advisory-only Dreaming Mode contract, report templates, workspace bootstrap namespace, privacy boundaries, and the split between `workflow-artifacts-only` and `full-repo` reports.

`check-global-quality-review-stance` validates the read-only/advisory review stance, review/findings/blockers routing, formal `phase-5-quality` separation, and final-review/final-check boundary.

`check-review-completeness-gate` validates Review Completeness Gate v2, including policy-boundary adversarial evidence, producer-consumer field audits, canonical queue producers, and the ban on whole-line negation filters in policy validators.

`check-full-qa-verification` validates artifact-appropriate full QA across early formal QA phases, phase 5, and global review, including the adaptive data/integration matrix boundary.

Use `.systems/ai/core/full-qa-verification.md` to decide the required QA lens. Earlier formal QA phases validate their own artifact; `phase-5-quality` validates implementation, and global review remains advisory.

`check-intent-plan-spec-compliance-review` validates the shared review/quality lens that compares implementation against owner instruction, accepted plan, accepted spec, scope, and acceptance criteria, and blocks technical-only PASS/review wording.

`check-implementation-slicing` validates the Implementation Slice Plan contract, DoD source, mandatory quality closure, PASS Integrity Gate, phase-4/template integration, side-task/micro-task/micro-project routing, and the boundary that slicing cannot bypass spec, scope, risk, permissions, approvals, or QA.

`check-plan-quality-contract` validates the Plan Quality Contract for formal and micro-work plans, Codex `/plan` routing, testable DoD, artifact QA and implementation quality routes, read-only `not-applicable` reasons, pre-write readiness, and opt-out boundaries.

`check-validation-profiles` validates `.systems/ai/core/validation-profiles.md`, `validate-workflow --profile` behavior, the no-arg `standard` validation default, explicit `full` smoke-test coverage, and the boundary that `scoped` and `fast` profiles are iteration aids unless the owner explicitly accepts narrow validation with residual risk.

`check-knowledge-capture-reminder` validates the advisory post-implementation/fix/quality/handoff reminder, owner skip grammar, tracked-vs-ignored commit boundary, push-disabled default, and the rule that reminders cannot bypass phase 6, phase 7, QA, evidence, privacy, status, risk, permissions, or memory scope gates.

`check-instruction-adherence-refresh` validates targeted/full refresh triggers, always-visible Execution Trace fields, drift-warning routing, contracted opt-out boundaries, lightweight normal continuation, and the rule that refresh cannot grant writes or bypass source-of-truth, risk, permissions, DoD, QA, evidence, or approvals.

`check-owner-decision-checkpoints` validates default material decision discovery, owner-preference classification, 1-3 question batches, phase-end checkpoints, no-question opt-out boundaries, non-interactive autopilot/Dreaming/review queues, and Execution Trace decision evidence.

`check-request-batch-triage` validates owner request batch triage, triage matrix fields, mixed-list routing, high-risk routing, and the boundary that triage cannot automatically implement, commit, or create workflow artifacts.

`check-response-evidence-trace` validates the required `Execution Trace` for substantive responses and preserves `Co dalej?` as the final footer.

`check-phase-skill-discovery` validates phase/procedure skill discovery, workspace-before-system skill precedence, `Skills used: none` fallback, and skill authority boundaries.

`check-default-quality-closure` validates default quality/review closure for substantive work, owner opt-out grammar, and the rule that opt-out cannot satisfy required QA PASS.

`check-default-idea-validation-opt-out` validates Default Idea Validation for single new work, broad project ideas, and batch validation routes, plus owner opt-out grammar and the boundary that opt-out cannot bypass safety gates.

`check-end-of-task-capture` validates chat-end knowledge capture routing, conflict-free precedence against formal phase/review/final commands, required output fields, and safety boundaries for memory, System Insights, External Memory, status, and final approval.

`check-cross-system-upgrade-handoff` validates the owner shared-impact decision, pending commit/handoff block, required External Memory handoff for `yes`, privacy boundary, and autopilot queue behavior.

`check-worktree-bootstrap` validates the strong-marker, approval, origin, collision, dirty-clone, self-clone, canonical command, and portable bootstrap boundaries.

`check-validation-routing` validates semantic/product QA before applicable workflow scripts, supporting-only script evidence, phase-specific routing, and the ban on `green scripts = PASS`.

`check-model-selection-guidance` validates Luna/Sol classification, required recommendation fields, advisory-only authority, and `Blocking: no`.

`.systems/scripts/report-workspace-freshness --output <path>` writes an advisory Workspace Freshness Ledger. `.systems/scripts/report-contract-topology --output <path>` writes an advisory Contract Topology Map. These reports never become hard gates.

`.systems/scripts/validate-workflow --timing-output <new-ignored-or-tmp-path>` records monotonic, versioned command and smoke timing metadata without repository content. Use `.systems/scripts/report-validation-comparison capture --timing <path> --output <new-manifest-path> --scope-fingerprint <id> --input-fingerprint <id> --setup-regime <id>` after each run, then `summarize <manifest...>` for at least three complete full runs or `compare --baseline <manifest...> --candidate <manifest...>` for conservative same-coverage comparison. Failed runs remain evidence but cannot enter a speed comparison. `.systems/scripts/check-validator-smoke-tests --group <all|core|policy|quality|skills|workspace>` supports measured group runs; `--group all` preserves full coverage and remains the default.

Named smoke groups execute only their manifest-owned tests/assertions in fresh
fixtures; full/CI still execute all groups. Use the public entrypoint, never
internal `smoke/*.sh` directly. `--verify-manifest` checks structural integrity
only and is not execution or QA evidence. The public completion/timing parent
is unique; group markers are namespaced. Cleanup needs local `ps` metadata and
fails closed if the platform denies it. Read `validation-observability.md`
before changing membership, preserved reference regions or shared helpers;
update hashes/field mapping and repeat the actual equivalence/failure audit.

`check-workspace-freshness`, `check-contract-topology`, `check-validation-observability`, and `check-validation-completion` validate advisory reporting, measurement, lifecycle markers, canonical update boundaries, and timeout safety. `check-skill-evaluation-contract` validates optional behavioral skill evals; existing skills without evals remain valid.

Before creating a commit, also apply `.systems/ai/core/contract-compliance.md` and report the advisory work mode compliance plus knowledge capture decision. If capture is required, run the appropriate phase/artifact path before committing.

## New Workflow Validators

`check-delivery-constraints` validates deadline/timebox fields and safety boundaries. `check-distillation-state` validates the state machine, producer-consumer boundary, and Dreaming no-write rule.

## Skipped Checks

Skipped checks must include:

- command name;
- reason skipped;
- whether the skip affects `PASS`;
- fallback evidence, if any.
