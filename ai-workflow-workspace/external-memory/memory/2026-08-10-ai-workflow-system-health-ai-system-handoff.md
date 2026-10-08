# External Memory Handoff: AI Workflow System Health

## Scope

- Counterpart: `ai-system`
- Source system: `ai-workflow`
- Date: `2026-08-10`
- Privacy status: no client data, secrets, credentials, product data, or runtime contents copied.
- Purpose: conceptual adaptation context for a later `ai-system` implementation.

## Reusable Patterns

1. **Advisory workspace freshness**
   - Keep repository facts and ignored runtime notes separate.
   - Generate a metadata-only freshness ledger with path, branch, HEAD,
     upstream, worktree state, baseline, drift, and recommended action.
   - Stale or dirty state is advisory unless an existing source-of-truth stop
     condition applies.
   - Reference implementation: `.systems/ai/core/workspace-freshness.md` and
     `.systems/scripts/report-workspace-freshness`.

2. **Advisory contract topology**
   - Map contracts to routers, validators, smoke tests, templates, producers,
     and consumers.
   - Use `linked|partial|orphaned|unknown` as diagnostic statuses; do not make
     topology itself a new hard gate.
   - Reference implementation: `.systems/ai/core/contract-topology.md` and
     `.systems/scripts/report-contract-topology`.

3. **Dream recommendation lifecycle**
   - New Dream Reports use schema v2 with stable recommendation IDs,
     lifecycle, previous evidence, and decision artifact.
   - Historical v1 reports remain immutable and legacy-valid.
   - Resolved lifecycle states require decision evidence; repeated findings
     require previous evidence.
   - Reference implementation: `.systems/ai/core/dreaming-mode.md`,
     `.systems/ai/templates/dreaming/dream-report.template.md`, and
     `.systems/scripts/check-dreaming-mode`.

4. **Validation observability before partitioning**
   - Record validator/smoke timing metadata first and run three clean baselines.
   - Preserve the monolithic smoke runner until an equivalence audit proves
     every existing test ID is retained exactly once.
   - Group labels may be introduced before execution splitting, but must not
     imply reduced coverage.
   - Reference implementation: `.systems/ai/core/validation-observability.md`,
     `.systems/scripts/validate-workflow`, and
     `.systems/scripts/check-validator-smoke-tests`.

5. **Optional behavioral skill evaluation**
   - Use a shared contract with trigger/non-trigger scenarios, baseline,
     with-skill behavior, expected/forbidden behavior, evidence, result, and
     residual risk.
   - Missing evals remain valid; runtime output belongs outside active skill
     directories.
   - Reference implementation: `.systems/ai/core/skill-behavioral-evaluation.md`
     and `.systems/scripts/check-skill-evaluation-contract`.

## Safety Boundaries

- These patterns are supporting guidance only.
- They cannot override source-of-truth order, risk, permissions, approvals,
  phase gates, QA, evidence, or stop conditions.
- Dreaming remains advisory-only and does not write this handoff automatically.
- Adoption in `ai-system` requires its own owner-approved plan, validation,
  quality closure, and local privacy review.

## Adaptation Checklist

- [ ] Identify `ai-system` workspace/repository mode and current runtime roots.
- [ ] Add freshness and topology reports as advisory artifacts only.
- [ ] Define Dream schema compatibility without rewriting historical reports.
- [ ] Add timing output before considering smoke partitioning.
- [ ] Run three clean baselines and perform an equivalence audit before any split.
- [ ] Add optional skill behavioral eval contract without mandatory backfill.
- [ ] Add producer-consumer and policy-boundary smoke coverage.
- [ ] Run semantic QA before scripts and retain full validation for applicable gates.
