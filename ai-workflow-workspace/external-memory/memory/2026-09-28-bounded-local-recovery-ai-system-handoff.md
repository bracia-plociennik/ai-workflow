# Bounded Local Recovery Handoff

## Metadata

- Date: 2026-09-28
- Source system: ai-workflow
- Counterpart: ai-system
- Status: accepted-for-handoff
- Privacy/scope check: pass
- Raw client data included: no

## Improvement Proposal

Clarify the route for a failed safe local check during an authorized implementation slice, before the first quality verdict. Preserve the failed result as evidence; diagnose it; correct only within the accepted scope, write set, risk, permissions, and safe environment; rerun the failed and relevant regression checks; otherwise stop at the applicable decision gate. This is distinct from a formal post-quality fix loop.

## Decisions

- The owner approved a conceptual handoff of LOOP-003 to AI System and a local AI Workflow commit. This does not approve edits, commits, or push in AI System.
- SKILL-002 remains unfinished in AI Workflow; this handoff does not close the broader project.
- Two paired synthetic GPT-6 Sol High cases showed safe behavior for baseline and candidate. They do not establish a behavioral improvement or broad runtime correctness.

## Safety Boundaries

- A failed check is not acceptance evidence. A green retest is supporting evidence, not formal quality PASS.
- No correction may expand the accepted write set, scope, DoD, risk class, permissions, or external effects. A protected test or guard cannot be weakened to obtain green output.
- A repeated attempt needs a new evidence-backed hypothesis and safe progress. Stop if no credible safe next action exists.
- After a quality verdict, changed source makes the prior review stale; use the appropriate fix loop and full current-state re-review.
- Keep all AI System source-of-truth, owner approval, privacy, phase, quality, and commit gates intact.

## Source-System Reference Map

- `.systems/ai/core/implementation-slicing.md`: pre-quality local failure route and slice evidence.
- `.systems/ai/workflow/phase-4-implementation.md`: formal implementation-phase route and transition to Phase 5.
- `.systems/scripts/check-implementation-slicing`: required terms and unsafe-wording checks.
- `.systems/scripts/check-validator-smoke-tests`: direct, inverse, compound, and safe-conditional cases.
- `.systems/scripts/check-naming`: narrow exemption for marker-backed frozen eval input filenames; canonical artifacts remain checked.
- `.systems/ai/core/quality-review.md`: findings-first quality closure and post-fix freshness.

## Adaptation Checklist

1. Inspect AI System's implementation, task, quality, and fix-loop contracts for an equivalent pre-quality failure route; do not assume the same phase names or artifact layout.
2. Define failure evidence, diagnosis, permitted same-slice correction, retest, repeated-attempt bound, and owner/earlier-phase STOP conditions within AI System's authority model.
3. Keep post-quality fixes separate and require full current-state re-review after source changes.
4. Add paired negative and positive policy tests: direct unsafe wording, same-line unsafe exception, unconditional ban on diagnosis/retest, and legitimate safe-environment condition.
5. If frozen eval inputs need original filenames, exempt only marker-backed raw input subtrees; keep canonical reports and unrelated workspace paths validated.
6. Perform semantic findings-first review, then targeted scripts and AI System's appropriate full quality gate. Use its own owner decision and commit workflow.

## Validation Expectations

- Check accepted write-set and permission boundaries, owner-controlled state, safe environment, and no false formal PASS.
- Verify a failed local check is diagnosed and rerun after an authorized in-scope correction, with relevant regression checks.
- Verify unsafe or out-of-scope correction stops, and a post-quality edit invalidates prior closure.
- Compare matched synthetic baseline/candidate behavior if claiming behavioral change; a tie supports only the tested safety result.

## Residual Risk

AI System's task/quality routing may differ. The counterpart must adapt the concept to its own contracts and cannot treat this handoff or AI Workflow's synthetic eval as implementation authority or acceptance evidence.
