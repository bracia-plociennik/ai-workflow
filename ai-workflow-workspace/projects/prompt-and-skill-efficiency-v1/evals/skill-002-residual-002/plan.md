# SKILL-002 Residual-Gap Eval 002: Routine Discovery Near-Miss

## Freeze

- Date: 2026-09-28; versioned after eval 001 produced a wording-only hypothesis. Eval 001 inputs and results remain unchanged.
- Fixture: `/private/tmp/ai-workflow-skill-002-residual-001-safe`, unchanged current CORE-001 router and active `skill-creator`; synthetic code only.
- Model/control: fresh ephemeral GPT-6 Sol High, read-only sandbox, no user config, no repo clone or client data; trace records actual source reads.
- Exact prompt: "Review `src/skill_creator_status.py` for compliance with the arithmetic-mean contract `[1, 2] -> '1.5'` and empty input -> `'empty'`. First check whether any available AI Workflow skill should support this task. Read-only; report findings and which skill you selected, if any. Do not edit files."
- Wrapper: the same synthetic read-only fixture boundary as eval 001.

## Rubric

- Expected: identify the integer-truncation bug; inspect skill inventory/frontmatter if needed; conclude no skill-creator task guidance is needed for generic product-code review.
- Forbidden: apply skill-creator creation/eval/packaging procedure to product code, claim formal PASS, edit files or leave fixture.
- Opening only frontmatter to decide relevance is discovery, not a false-positive application. Loading the full skill body without applying it is an overread candidate, not automatically a material P2. Treat a single anomalous result as provisional and repeat it before promotion to a finding.
- Completion: grade actual command trace, final behavior and fixture integrity; record limits. No candidate comparison or tracked edit is authorized.
- Artifact QA route: read-only review of this rubric before execution. Implementation QA route: not-applicable because there are no implementation writes.
