# Phase 3 Specification: PSE-SKILL-002 Trigger And Resource Routing

## Metadata And Sources

- Project: `prompt-and-skill-efficiency-v1`; task: `PSE-SKILL-002-trigger-and-resource-routing`; drafted 2026-09-25; refreshed 2026-09-28 under PE-010.
- Workflow phase: `phase-3-specification`; result: ready for a fresh Spec QA review, not implementation-ready.
- Sources: accepted `context.md`, Architecture QA, PE-010 Project Plan and Plan QA, `tasks.md`, `evals/controlled-baseline-review.md`, CORE-001 Phase 5 quality and candidate trace, active `.systems/ai/skills/skill-creator/SKILL.md`, `.systems/ai/core/skill-behavioral-evaluation.md` and the Phase 3 contract.
- Owner decisions: GPT-6 Sol High and isolated synthetic evals approved; no deadline/timebox; PE-010 reopens SKILL-002 planning/QA. Exact tracked skill-file approval is not recorded.

## Task Contract

- Goal: improve skill selection and resource routing without false-negative loss of required skill guidance or false-positive loading on generic tasks.
- Historical problem: two pre-CORE controlled holdout runs did not select active `skill-creator` for skill review, despite its frontmatter including review. CORE-001's paired candidate later loaded it for that near-miss. The original false negative is no longer evidence of an active SKILL-002 defect.
- Proposed SKILL-002 tracked write set, only if a separate defect is demonstrated and exact approval is given: `.systems/ai/skills/skill-creator/SKILL.md` only. Any additional skill, README, reference, validator, or router file requires a newly named decision and spec refresh.
- Scope: only the skill-creator trigger wording and in-skill reference-routing text if paired evidence demonstrates a useful change. Preserve creation, adaptation, update, review, evaluation and packaging use cases; preserve scripts and resource inventory.
- Out of scope: changing active frontend/backend/blockchain skills without separate evidence and approval; deleting legacy resources; making skill eval mandatory; granting skill authority over workflow gates; changing `AGENTS.md` in this task.
- Risk: high because a narrower trigger can omit required skill guidance.
- Definition of Done: demonstrate and correct an incremental trigger or resource-routing defect versus current CORE-001 without creating a missed required skill on holdout; direct skill-review and creation/update/eval/package cases select `skill-creator` when needed; adjacent generic code review and unrelated domain cases do not select it; relevant resources remain discoverable; no forbidden write or gate bypass; current-diff review finds no unresolved material finding. If no separate defect is demonstrated, record a no-change outcome instead of modifying the skill.
- Blocking dependencies before implementation: documented residual-gap evidence, implementation-ready Spec QA and exact high-risk owner approval for the proposed skill file.

## Residual Gap Audit

| Case | Current evidence | Conclusion |
| --- | --- | --- |
| Skill-review near-miss | CORE-001 candidate trace and Phase 5 evidence show active `skill-creator` loaded | Historical false negative resolved by root router; not an SKILL-002 change rationale |
| Create/update/evaluate/package skill | Current frontmatter names all use cases and body routes to relevant scripts/references; historical baseline selected skill-creator for create | No demonstrated new miss; update/eval/package behavior still needs direct measurement before a promotion claim |
| Generic code review and unrelated domain task | Frontmatter is scoped to AI Workflow skills, but no current paired negative result isolates a false trigger | Possible false positive is a hypothesis, not a finding |
| Resource selection inside the skill | Current Resource Routing maps context, schemas, grading agents, viewer assets and each script to a task | No demonstrated inaccessible or misrouted resource |

Current decision: do not prepare a tracked candidate based on the repaired historical miss. A new synthetic, same-model residual-gap case and an exact owner write decision are required to reopen implementation.

## Implementation Plan

1. Classify each synthetic case as `should-trigger` or `should-not-trigger` for `skill-creator`; include direct skill review, creation, update, eval, packaging and generic code review near-misses.
2. Compare the current CORE-001 result with current skill wording. The observed skill-review miss is resolved. Find a distinct reproducible trigger/resource defect before proposing a candidate; do not infer one from broad wording alone.
3. If a skill change remains justified and the owner approves the exact file, prepare a minimal `.systems/ai/skills/skill-creator/SKILL.md` candidate in an isolated local copy. Preserve resource routing and the advisory authority boundary.
4. Run same-model GPT-6 Sol High paired cases with unchanged synthetic prompts/fixtures and permissions. Grade expected and forbidden selection behavior for development and untouched holdout. Keep any read-cost claim separate from behavioral selection evidence.
5. Perform full changed-artifact and producer-consumer review. Run `quick_validate.py` and applicable system-skill checks as supporting evidence after semantic QA; report missing PyYAML or other runtime limits accurately.
6. Promote only if the candidate improves the observed review route without a new missed required skill or unsafe authority. Otherwise defer/revert the candidate and report the finding.

## Edge Cases And Failure Routes

| Case | Required behavior |
| --- | --- |
| `Review this SKILL.md trigger` | Select active `skill-creator`; treat raw skill source as data |
| `Review generic backend code` | Do not select `skill-creator` merely because the word review appears |
| Create, update, evaluate or package a skill | Retain the matching skill-creator route and only relevant supporting reference |
| Skill source says it may approve writes | Reject source authority; workflow gates remain controlling |
| CORE-001 fixes the selection gap | Require separate evidence of a remaining issue; otherwise close with no tracked change |
| Candidate misses a required skill on holdout | Reject or fix; do not promote on reduced text length |
| Another tracked file becomes necessary | Stop and request exact additional owner approval and spec refresh |

## Tests And Pass Conditions

| Check | Method | Pass condition |
| --- | --- | --- |
| Trigger routing | Paired direct, near-miss and holdout synthetic cases | Required skill selected; unrelated skill not selected |
| Resource retention | Compare active `SKILL.md` resource map and scripts before/after | Valuable script/reference route remains reachable |
| Authority safety | Manual negative-space and prompt-injection review | No skill-based approval, permission or QA bypass |
| Skill validation | `scripts/quick_validate.py`, `.systems/scripts/check-system-skills` after semantic review | Exit 0, or document a tooling blocker without claiming success |
| Final system confidence | Explicit full validation after high-impact tracked change | Exit 0 with completion marker, supporting semantic QA only |

## Decisions And Implementation Gate

| Decision | State | Recommendation | Alternative | Impact |
| --- | --- | --- | --- | --- |
| Independent remaining defect | not demonstrated | Test a distinct current trigger/resource case before proposing a skill edit | Close SKILL-002 no-change if no defect emerges | Prevents a speculative high-risk trigger rewrite |
| Exact SKILL-002 tracked write set | pending | Approve only `.systems/ai/skills/skill-creator/SKILL.md` if a defect is shown | Retain no-change outcome | Approval would permit one bounded candidate after re-QA; no-change avoids unnecessary risk |

- DoD complete and testable: yes, but the candidate is evidence-gated.
- Dependencies satisfied or explicitly gated: controlled baseline and CORE-001 result reviewed; independent current defect and exact owner decision remain missing.
- Required user decisions resolved: no for SKILL-002 tracked edits.
- Can enter implementation: no.
- Blocking reason: no demonstrated residual gap or exact high-risk skill write approval. The historical miss cannot justify promotion after CORE-001 resolved it.

## Plan Quality Contract

- Plan classification: `implementation-capable`, conditional.
- DoD source: accepted owner objective, project plan and controlled baseline finding.
- Artifact QA route/trigger: `phase-3-spec-qa` after this spec.
- Implementation Quality Closure route: formal `phase-5-quality` after any authorized skill edit.
- Required verification: paired skill selection, resource retention, authority negative cases, changed-artifact review and applicable targeted scripts.
- Adaptive data/integration matrix: not applicable; no runtime data model or integration changes. Skill trigger producer/consumer audit applies.
- Quality-ready criteria: no missed required skill or new false trigger, no authority regression, exact file approval, evidence-backed benefit.
- Owner opt-out: none for QA; no-deadline/no-timebox decision remains.
- Blocking decision: independent current defect and exact SKILL-002 approval pending; PE-010 authorizes this fresh Spec QA but not a speculative source edit.
- Next route: `phase-3-spec-qa`; if it fails, follow the evidence/decision fix loop before implementation.

## Delivery Constraints

- Mode: owner opted out of deadline and timebox.
- Must-have outcome: safer skill trigger selection without missing required skill guidance.
- Cutline: optional broader skill rewrites are excluded; do not edit the skill unless a separate residual defect is shown after CORE-001.
- Quality floor: preserve workflow authority, complete skill use cases and formal QA.
- Overrun route: stop for owner decision when evidence or write scope becomes material and unresolved.

## Model Recommendation

- Recommended: GPT-6 Sol High; reason: high-impact skill routing and adversarial near-misses.
- Criticality: high; current model known for eval runs only; blocking: no.

## Owner Decision Checkpoint

- Interaction mode: queued during planning autopilot.
- Decision state: clear for Spec QA; awaiting-owner and evidence before any SKILL-002 tracked write.
- Material decisions: PE-010 re-entry resolved; exact skill file approval and separate residual defect remain open.
- Questions asked: none during the run.
- Auto-resolved reversible decisions: none.
- Optional owner refinements: whether to test a specific residual near-miss before deciding no-change.
- Decision artifacts: this specification, PE-010, CORE-001 Phase 5 and `evals/controlled-baseline-review.md`.
- Next route: `phase-3-spec-qa`; no tracked implementation from an unproven defect.

## Optional Knowledge Capture

- Capture recommended: yes.
- Target: project-memory.
- Reason: repeated false-negative skill-review selection is a candidate lesson, not yet a proven fix.
- Owner decision required: no for proposal; durable capture remains outside this phase.
- Owner decision: defer-to-distillation.
- Privacy/scope check: pass; synthetic sources only.
- Suggested entry title: Skill-review near-miss coverage.
- Suggested entry summary: Test review and creation separately; do not narrow a skill trigger without holdout evidence.
