# Conditional Instruction Router Handoff

## Metadata

- Date: 2026-09-25
- Source system: ai-workflow
- Counterpart: ai-system
- Status: accepted-for-handoff
- Privacy/scope check: pass
- Raw client data included: no

## Improvement Proposal

Keep a small, always-on root safety and authority router. Open detailed contracts and domain skills when the current task, phase, risk or domain triggers them, rather than requiring every policy at the start of every task. Treat the root file as routing guidance, not a replacement for the detailed contracts.

## Decisions

- The owner approved sharing this concept with AI System. This handoff does not approve implementing it there.
- AI Workflow changed only its root `AGENTS.md` in the first candidate; skill contracts and workflow policy remained unchanged.
- Use observed paired behavior and direct contract-read evidence before adopting a shorter router. A shorter file by itself does not establish lower context cost.

## Safety Boundaries

- Keep source-of-truth order, risk, permissions, DoD, QA, stop conditions, evidence, owner approvals and prompt-injection handling unconditional where required.
- Conditional skill discovery must not miss near-miss cases such as skill review versus skill creation.
- No target-repository, client, production or private runtime data is transferred through this handoff.
- The counterpart must use its own owner decisions, accepted plan, write set, QA and commit gates.

## Source-System Reference Map

- `AGENTS.md`: compact always-on entry and conditional task/phase/risk/domain routes.
- `.systems/ai/core/operating-model.md`, `command-routing.md`, `risk-model.md`, `permissions.md`: root routing authorities.
- `.systems/ai/core/quality-review.md`, `full-qa-verification.md`, `validation-routing.md`: quality and evidence boundaries.
- `AGENTS.md` Skill Routing section and active skill `SKILL.md` contracts: supporting guidance only.
- `.systems/ai/workflow/`: formal phase contracts remain authoritative for their gates and writes.

## Adaptation Checklist

1. Inventory AI System's root instructions, unconditional reads, conditional routes, phase requirements and skill triggers.
2. Freeze representative synthetic tasks and a before/after relevance rubric before changing the router.
3. Draft a minimal candidate without deleting detailed contracts or weakening unconditional safety rules.
4. Run matched-model, matched-prompt baseline and candidate cases; inspect completed file-read traces and safety/phase behavior, including near misses.
5. Review the entire diff, mandatory autoload coverage, risk boundaries and producer-consumer references. Reject any missed mandatory rule even if reading cost improves.
6. Use AI System's own quality, owner approval, checkpoint and commit route; do not copy AI Workflow runtime artifacts.

## Validation Expectations

- Include a small task-routing matrix covering a trivial edit, formal phase QA, security review, skill review, mixed-domain work, completion/capture and ambiguous owner decisions.
- Measure irrelevant explicit contract reads and disclose telemetry limits; do not infer token savings unless separately measured.
- Validate mandatory policy and skill discovery, wrong-route negative cases, instruction autoload/truncation, current diff and post-fix freshness.
- Treat green scripts as supporting evidence after semantic findings-first review.

## Residual Risk

Synthetic cases cannot cover every real phrasing. Conditional routing can fail silently if a future task lacks an explicit trigger; AI System must preserve conservative fallback behavior and review failures independently.
