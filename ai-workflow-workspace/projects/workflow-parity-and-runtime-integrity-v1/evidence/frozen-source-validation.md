# Frozen Source Validation Evidence

- Profile: full
- Scope: project workflow-parity-and-runtime-integrity-v1; all source validators and all five smoke groups.
- Source HEAD: 0c767da0385723560d1b0d4794a9091316c23140
- Source fingerprint: 51 selected changed/new source files, unchanged throughout final run.
- Semantic QA: owner intent, DoD, source/diff, producer-consumer, adversarial and failure-path review completed before final script verdict.
- Log: /tmp/workflow-parity-full-validation-source-frozen.log
- Log SHA-256: 8bed184731f39309ed0e7c35eb769b5921b030e1e8c42ba54437af8a576bd26b
- Completion: AI_WORKFLOW_VALIDATE_COMPLETE profile=full result=pass exit_code=0 duration_seconds=651 stage=validator check=.systems/scripts/check-validator-smoke-tests
- Unique smoke IDs: 695, including all 694 previous IDs exactly once.
- Synthetic runtime regressions: 46, passed directly and in smoke.
- Coverage: complete; no skipped source checks or smoke groups.
- Final evidence eligibility: yes for this frozen source; later captures receive current runtime checks.
- Scripts: supporting-only, not the reason for semantic PASS.
- Prior failures preserved; the 676-second successful run was superseded by the last scorer fix and is not used as final frozen-source evidence.
- Limits: no model/performance eval, no CI/remote or external coordinator integration claim; no source commit/push.

