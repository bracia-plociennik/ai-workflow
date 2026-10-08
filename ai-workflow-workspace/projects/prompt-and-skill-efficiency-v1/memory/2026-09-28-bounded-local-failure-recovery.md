# 2026-09-28 - Bounded Local Failure Recovery

- Date: `2026-09-28`
- Topic: `PSE-LOOP-003 local failure routing and eval limits`
- Type: `project-constraint`
- Status: `active`
- Scope: `PSE-LOOP-003-local-completion-persistence` and later efficiency review.
- Source: `distillations/phase-6-pse-loop-003-local-completion-persistence-distillation.md` and its formal Phase 5 quality artifact.
- Evidence:
  - Five-file approved diff and full workflow validation passed after semantic current-diff review.
  - Two paired synthetic GPT-6 Sol High cases showed safe recovery/STOP in both baseline and candidate; no measured behavior gain.
- Summary: A failed safe local check before the first quality verdict may be diagnosed and corrected only inside the accepted slice, authority, and safe environment. Record failure evidence, rerun the failed and relevant regression checks, or stop at the blocking gate. Post-quality fixes use the separate formal fix loop and full current-state re-review.
- Applies to: later implementation-loop, validator, and behavioral-eval work in this project.
- Rule: Do not infer permission or PASS from a green retest. Pair unsafe policy examples with safe conditional examples; a baseline tie is evidence of tested safety, not improvement.
- Review trigger: a new implementation-loop change, a broader eval, or an observed runtime-fault regression.
