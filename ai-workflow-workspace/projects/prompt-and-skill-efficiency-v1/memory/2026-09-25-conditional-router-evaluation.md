# 2026-09-25 - Conditional Router Evaluation

- Date: `2026-09-25`
- Topic: `CORE-001 conditional root instruction routing`
- Type: `testing-note`
- Status: `active`
- Scope: `PSE-CORE-001-conditional-instruction-router` and later efficiency slices.
- Source: `distillations/phase-6-pse-core-001-conditional-instruction-router-distillation.md` and Phase 5 quality evidence.
- Evidence:
  - Frozen GPT-6 Sol High paired synthetic cases with a predeclared read-relevance rubric.
  - Completed command-level JSONL traces: irrelevant explicit core reads 28 baseline versus 12 candidate, without a mandatory-policy miss in the tested cases.
  - Candidate autoload warning check and full current-diff review.
- Summary: A shorter root instruction router is worth promoting only when direct read evidence improves and safety, skill, phase and approval routes remain intact. Text length alone is not evidence of efficiency.
- Applies to: later CORE variants and deferred SKILL-002/LOOP-003 comparison planning.
- Rule: Freeze model, prompts, fixtures and rubric before comparison; reject any safety-critical regression regardless of aggregate read gains. CLI read traces do not prove every OS open or token savings.
- Review trigger: any further root-router edit, changed CLI instruction budget, or new paired eval scope.
