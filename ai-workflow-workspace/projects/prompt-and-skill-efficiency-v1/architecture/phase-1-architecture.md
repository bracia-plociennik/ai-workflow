# Phase 1 Architecture: Prompt And Skill Efficiency V1

## Metadata

- Project: `prompt-and-skill-efficiency-v1`
- Date: 2026-09-24
- Workflow phase: `phase-1-architecture`
- Architecture result: `PASS` for the working-phase artifact; independent Architecture QA follows

## Sources

- Owner priority matrix, request for stages 0-5, no-deadline/timebox decision, and GPT-6 Sol High eval decision.
- Repo baseline: official `main` at `7a904f736eaf029bea750c3a735cd53fa61ef4c0`, tracked worktree clean at intake.
- Project context: `context.md`, `intake/phase-0-idea-validation.md`, `intake/phase-0-repo-intake.md`.
- Workflow: `AGENTS.md`, `operating-model.md`, `workflow.md`, `autopilot.md`, `risk-model.md`, `permissions.md`, `skill-behavioral-evaluation.md`, `implementation-slicing.md`, `quality-review.md`.
- Supporting source: OpenAI article on skills and prompts, not authority for workflow gates.

## Goals And Testable DoD

1. Reduce irrelevant instruction and skill reads on small tasks without omitting required policy or domain guidance.
2. Narrow ambiguous skill triggers only when paired eval evidence shows a net improvement.
3. Ensure an authorized local implementation continues through test, inspection, repair, retest, and quality closure, or stops at an actual gate.
4. Preserve risk, permission, owner-decision, source-of-truth, DoD, QA, and evidence boundaries.
5. Compare current and candidate behavior under GPT-6 Sol High on the same frozen development and holdout prompts; report missing instrumentation as unknown.

Architecture is ready for project planning when component ownership, evidence flow, decision gates, failure modes, and out-of-scope boundaries are explicit and Architecture QA finds no unresolved material defect.

## Boundaries

In scope: upstream AI Workflow `AGENTS.md`, relevant core routing/quality contracts, active system skill descriptions and selected skill router content, validators/smoke tests where contract enforcement is changed, and ignored project eval evidence.

Out of scope: target repositories, client data, actual Codex global settings, model switch automation, wholesale prompt-module deletion, weaker safety rules, unattended external effects, mandatory skill evals, phase-8 final check, commit/push, and adaptation in `ai-system`.

## Components And Responsibilities

| Component | Responsibility | Existing or new | Boundary |
| --- | --- | --- | --- |
| Root instruction router | Small always-on rule set plus conditional links for phase/risk/task/domain | Existing `AGENTS.md`, revised if evidence supports | Does not demote safety or source-of-truth order |
| Core contract index | Explicit triggers and dependencies for detailed policy reads | Existing core docs or compact map | Canonical detailed rules remain in core docs |
| Phase skill discovery | Select workspace skill before system skill; load only applicable active `SKILL.md` and needed references | Existing, refine only on evidence | Skill advisory; never grants approval |
| Skill-creator router | Trigger for creation/update/review/evaluation/packaging as justified by cases | Existing skill, possible narrowed description | Preserve valuable scripts and eval resources |
| Local completion loop | Keep safe implementation going through test, inspect, fix, retest, QA | Existing implementation/quality contracts, targeted clarification | No bypass for missing DoD, safe env, permission, or required owner decision |
| Eval and comparison | Freeze synthetic cases, capture exact opens/actions, grade expected and forbidden behavior, compare paired runs | Ignored workspace artifacts | Cannot claim behavior from static count or scaffold |
| Validator and smoke layer | Detect policy omissions and contract conflicts after semantic review | Existing scripts, targeted changes only | Scripts are supporting evidence, never sole QA PASS |

## Dependencies And Sequence

| Dependency | Direction | Risk and control |
| --- | --- | --- |
| Current tracked instruction snapshot | Baseline eval -> candidate edit | No tracked edits before complete reviewed baseline |
| Owner-approved isolated GPT-6 Sol High run | Eval harness -> behavioral evidence | Local synthetic fixtures only; no network/client data |
| Architecture/Plan/Spec QA | Planning -> implementation readiness | Separate formal QA of each artifact; no gate inferred from scaffold |
| High-risk owner approval | Spec QA -> tracked implementation | Record approval before tracked policy/router writes |
| Candidate edit | Implementation -> paired eval and phase-5 quality | Rerun identical prompts/settings, including untouched holdout |

## Main Execution And Evidence Flows

1. Owner task and repo facts enter task intake, work-mode/risk classification, and phase routing.
2. Minimal always-on safety/router instructions identify the relevant core phase, risk, permissions, quality, and domain sources; conditional reads are reported in Execution Trace.
3. Workspace skills are considered before active system skills; selected `SKILL.md` may route to narrow references, while `context/**` and legacy imports remain data.
4. Authorized implementation uses accepted spec or owner prompt, DoD, slice plan, safe test environment, write permission, local test-fix-retest, then formal phase-5 or advisory review as appropriate.
5. Eval captures source opens, skill triggers, missed required sources, irrelevant sources, actions, stop reason, QA result, and uncertainty per case. Grading and comparison are separate from agent self-report.

## Architectural Decisions Made

| Decision | Chosen option | Reason | Impact |
| --- | --- | --- | --- |
| Evaluation model | GPT-6 Sol High for both configurations | Explicit owner choice | No cross-model pooling |
| Delivery constraint | Owner opt-out of deadline and timebox | Explicit owner choice | No invented runtime limit; retry/stop safety remains |
| Eval execution | Isolated local subagents on synthetic fixtures | Explicit owner approval | Behavioral evidence allowed, with no production effects |
| Workflow route | Formal high-risk project, separate planning and implementation autopilot runs | Existing risk/autopilot contract | No single run can silently cross planning/implementation boundary |
| Candidate promotion | Evidence-led and fail-closed on safety regression | PASS integrity and skill eval contracts | Convenience gains never trump required gates |
| Packaging | Not requested | Owner-only optional phase | Solo task/spec route by default |

## Decisions Still Open

| Decision | Blocking? | Owner | Required by | Impact if delayed |
| --- | --- | --- | --- | --- |
| Approval of exact high-risk tracked policy write set | Yes for implementation, no for architecture/planning | Owner | Before phase-4 | No tracked implementation until approved |
| Whether to simplify model recommendation or response verbosity | No | Owner after paired evidence | Candidate scope selection | Leave existing behavior unchanged in V1 if evidence inconclusive |

## Risks And Failure Paths

| Risk | Severity | Owner | Mitigation / close condition |
| --- | --- | --- | --- |
| Conditional router misses safety rule on edge task | High | Workflow owner | Negative-space cases, policy dependency map, holdout regression, full-current-diff review |
| Trigger narrowing misses required skill | High | Workflow owner | Should-trigger and should-not-trigger cases; preserve broader route if false negatives appear |
| Eval cases lack concrete input or agent isolation | Medium | Eval owner | Fixture completeness check; reject pilot baseline-001; rerun both configurations after any fixture correction |
| Agent self-report differs from actual file access | Medium | Eval owner | Compare transcript/tool trace where exposed; mark unobservable metrics unknown |
| Local completion loop overruns permission or unsafe environment | High | Workflow owner | Existing risk/permission/stop checks remain dominant; only safe local tests and fixes in accepted write set |
| Prompt shortening hides authority boundary | High | Workflow owner | Keep exact source-of-truth, risk, approval, QA, and prompt-injection anchors always on |
| Plan claims readiness on static evidence | Medium | Project owner | Baseline completion and review required before phase-4; architecture/plan/spec QA remain separate |

## Assumptions And Unknowns

- Acceptable now: no product data migrations or external integrations are part of V1; synthetic fixtures represent routing and closure behavior, not production correctness.
- Non-blocking: token counts and wall time may be unavailable; report `unknown`, do not infer from file length.
- Non-blocking: if actual file-open traces are unavailable, self-reported source lists are a proxy only. Do not claim measured file-load or token savings, or promote a risky router change on that proxy alone.
- Blocking before candidate edit: incomplete baseline or missing owner approval for exact high-risk tracked writes.
- Blocking before release confidence: any mandatory-policy omission, false formal PASS, unapproved write, or missed required skill on holdout.

## Impact On Project Plan

- Sequence: finish baseline-002 and grade -> exact scoped source plan/spec -> owner high-risk approval -> implementation slices -> paired candidate eval -> formal phase-5 quality.
- Architecture/Plan/Spec QA can proceed while baseline runs, but no tracked edit may start until the baseline is complete and reviewed.
- Keep skill changes, root router changes, and completion-loop clarification as separately reviewable implementation slices.
- Defer model recommendation and response verbosity edits if paired evidence is weak or changes would enlarge scope.

## Plan Quality Contract

- Plan classification: `implementation-capable`.
- DoD source: accepted owner outcome and project context; testable conditions listed above.
- Artifact QA route: `phase-1-architecture-qa` immediately after this artifact.
- Implementation Quality Closure route: formal `phase-5-quality` after every later formal implementation task.
- Required verification: source and dependency review, counterexamples for missing policy/skill, paired behavioral eval, changed-files review, edge/failure-path analysis, targeted checks, full validation when appropriate.
- Quality-ready criteria: architecture aligned with owner intent, component ownership and boundaries explicit, no unresolved blocker for planning.
- Owner opt-out: none for QA; deadline/timebox opt-out recorded separately.
- Not-applicable reason: data/integration matrix is not applicable to this architecture document because it changes neither data model nor runtime integration; review eval artifact flows and failure handling explicitly.
- Blocking decision: high-risk tracked write approval before implementation, not before planning.
- Next route: `phase-1-architecture-qa`.

## Architecture Gate

- Blocking unknowns resolved for planning: yes.
- Risks have owner/mitigation: yes.
- Ready for project plan: only after Architecture QA PASS.
- Blocking reason: none for artifact QA; tracked writes remain gated.

## Delivery Constraints

- Mode: `owner-opt-out`; deadline: none; time budget: none.
- Must-have outcome: measured efficiency improvement without mandatory-gate regression.
- Cutline: defer optional verbosity/model-guidance changes before reducing eval or QA coverage.
- Quality floor: no safety/skill recall regression; formal QA and reviewed baseline/candidate evidence.
- Overrun checkpoint: owner decision if evidence becomes inconclusive or scope expands.

## Model Recommendation

- Recommended: GPT-6 Sol High (explicit owner-selected eval model; recommendation advisory).
- Reason: high-impact instruction and skill routing change with adversarial evaluation.
- Criticality: high-risk workflow-maintenance.
- Current model known: selected for subagent comparisons; main-agent runtime not asserted.
- Blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued for implementation approval; none needed for architecture QA.
- Decision state: clear for planning; awaiting-owner before tracked phase-4 writes.
- Material decisions: exact high-risk tracked write approval deferred until specifications identify write set.
- Questions asked: PE-001 answered.
- Auto-resolved reversible decisions: packaging not requested, so solo route.
- Optional owner refinements: model-guidance and response-verbosity scope after evidence.
- Decision artifacts: `intake/phase-0-idea-validation.md`, `autopilot/runs/autopilot-001/readiness.md`.
- Next route: `phase-1-architecture-qa`.

## Optional Knowledge Capture

- Capture recommended: no.
- Target: none.
- Reason: architecture decisions are recorded here; reusable lessons await implementation/eval evidence.
- Owner decision required: no.
- Owner decision: not-requested.
- Privacy/scope check: pass.
- Suggested entry title: none.
- Suggested entry summary: none.
