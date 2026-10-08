# Phase 6 Distillation: PSE-CORE-001 Conditional Instruction Router

## Metadata

- Project: `prompt-and-skill-efficiency-v1`
- Task/package ID: `PSE-CORE-001-conditional-instruction-router`
- Date: `2026-09-25`
- Workflow phase: `phase-6-distillation`
- Quality artifact: `quality/phase-5-pse-core-001-conditional-instruction-router-quality.md`; formal high-risk quality gate approved.
- memory-in-repo-memory: true

## What Was Done

- Replaced the blanket root `AGENTS.md` read-first list with a four-policy always-on set and conditional task/phase/risk/domain routes. Detailed contracts remain authoritative and unchanged.
- Compared the frozen baseline and candidate in 10 matched GPT-6 Sol High synthetic cases using completed command traces and a predeclared relevance rubric. Rubric-irrelevant explicit core reads fell from 28 to 12; no mandatory-policy or skill miss was found in these cases.
- Confirmed the candidate stays below the observed 32,768-byte instruction warning threshold and does not emit a truncation warning in the tested CLI path.

## Problems Encountered

| Problem | Resolution | Future Relevance |
| --- | --- | --- |
| Earlier candidates either increased irrelevant reads or tied the baseline. | Rejected them; promoted only v4 after directly observed improvement and holdout review. | Do not equate shorter instructions with lower actual reading cost. |
| A scoped Distillation State record was missing at the first implementation write. | Created the record before quality closure and disclosed the original timing violation. | Produce capture state before or atomically with the first implementation write. |
| The smoke fixture's Git bare clone failed under default macOS `TMPDIR`; slash normalization did not fix it. | A complete full validation passed using `TMPDIR=/private/tmp`. Exact default-temp cause remains unknown. | Treat fixture reliability as a separate workflow-maintenance finding; do not silently count the failed run. |

## Decisions

| Decision | Reason | Future Impact |
| --- | --- | --- |
| Keep CORE-001 tracked scope to root `AGENTS.md`. | Owner-approved PE-002 exact-file boundary. | SKILL-002 and LOOP-003 require later planning/approval, not implicit expansion. |
| Retain all detailed contracts and phase gates. | The root is a router, not a replacement authority. | Conditional loading must never weaken risk, permissions, evidence, QA or owner approvals. |
| Share the concept with AI System via one External Memory handoff. | Owner approved cross-system impact. | AI System can adapt the idea after its own analysis and gates; no direct counterpart write. |

## Rules For Future Tasks

- Freeze the same model, prompts, fixture snapshot, rubric and CLI settings before comparing instruction routers; grade completed file-read commands rather than self-reported source lists.
- Test mandatory routing and near misses, including security review, formal QA, skill review and mixed-domain work. A missed safety rule blocks promotion even when aggregate reads improve.
- Check mandatory instruction autoload and current diff after every router edit; CLI traces do not expose every OS file open or prove token savings.
- Create the scoped Distillation State producer record before or atomically with the first implementation write, then transition it only against quality and distillation evidence.

## Repo / Project Memory Candidate

- Should sync to memory: yes, project memory.
- Reason: CORE comparisons and deferred-task planning can reuse the evaluation method and limitations.
- Suggested memory entry: `memory/2026-09-25-conditional-router-evaluation.md`.
- Repo memory: no; the detailed evaluation belongs to this project rather than a repo-wide runtime fact.

## External Workflow Memory Candidate

- Should sync to `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/`: yes, by the separately approved cross-system handoff route.
- Reason: conditional contract routing is a system-level improvement relevant to the counterpart.
- Suggested external memory entry file: `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/2026-09-25-conditional-instruction-router-ai-system-handoff.md`.
- Suggested external memory router update: `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md`.
- Suggested insight summary: Adapt a compact always-on safety router and conditional detailed-contract discovery, using paired behavioral and direct-read evidence before adoption.

## System Insight Candidate

- Should sync to `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/`: no.
- Category: n/a.
- Reason: the current lesson is specific to AI Workflow contract routing, not a general product-domain insight.
- Source scope: project distillation.
- Privacy check: pass; synthetic/system evidence only.
- Skill candidate: no.

## Artifacts Updated

| Artifact | Update |
| --- | --- |
| This distillation | Compact decisions, constraints, warnings and future rules. |
| Scoped Distillation State | Transition from `ready` to `completed` after accepting this artifact. |
| Project memory | Phase 7 will synchronize the reusable project-local method. |
| External Memory | Owner-approved counterpart handoff prepared before commit. |

## Distillation Gate

- Captures reusable knowledge: yes.
- Avoids local noise: yes; the full iteration diary stays in Phase 4 and eval artifacts.
- Ready for checkpoint processing: yes.

## Distillation State

- Work ID: `PSE-CORE-001-conditional-instruction-router`
- Previous state: `ready`
- State after accepted distillation: `completed`
- Distillation artifact: this file.
- `is_distilled` derived value: `true`
- Privacy/scope check: `pass`
- Residual risk: controlled synthetic coverage is finite; the default-temp smoke fixture remains a separate reliability concern.

## Owner Decision Checkpoint

- Interaction mode: none.
- Decision state: clear for this CORE-only checkpoint.
- Material decisions: PE-002, PE-003, PE-004.
- Questions asked: none during this phase.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: decide later whether to pursue SKILL-002, LOOP-003 or a fixture reliability fix.
- Decision artifacts: `decisions/pe-004-core-quality-and-cross-system-handoff.md`.
- Next route: `phase-7-checkpoint`.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: the evaluation method and routing limits will matter for remaining project tasks.
- Owner decision required: no; capture was explicitly requested.
- Owner decision: capture-now.
- Privacy/scope check: pass.
- Suggested entry title: Conditional router evaluation.
- Suggested entry summary: Preserve direct-read paired eval method, autoload limit and stop-on-safety-regression rule.
