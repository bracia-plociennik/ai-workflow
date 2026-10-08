# QA Evidence And Project Scope: AI System Handoff

## Outcome

AI Workflow accepts exact SHA-256 admissions in both historical three-column and five-column QA evidence registries. An incomplete V1 QA artifact may be classified `superseded-invalid-v1` only with a same-project, fingerprinted recovery artifact that satisfies the current V1 QA contract. `validate-workflow --project <slug>` scopes runtime status, QA evidence, and naming to that project while product checks stay global.

## Owner Decisions

- Owner approved the upstream fix, commit and push after QA, followed by an update of the AI System nested workflow clone.
- Project-scoped validation must not hide a failure in the selected project. No argument retains global validation.

## Boundaries

- Registry entries never amend historical QA files or grant PASS by themselves.
- Recovery requires exact original and replacement paths and SHA-256 values; changing either file invalidates admission.
- `--project` does not suppress global product contract checks, privacy checks, or secret scanning.
- This handoff is advisory; it does not authorize runtime status changes or final owner approval.

## Source References

- `.systems/scripts/check-qa-evidence`
- `.systems/scripts/check-status-consistency`
- `.systems/scripts/check-naming`
- `.systems/scripts/validate-workflow`
- `.systems/ai/core/full-qa-verification.md`
- `.systems/ai/core/validation-profiles.md`

## Validation And Adaptation

- Upstream full profile and smoke tests completed with success markers before commit.
- After nested update, run `check-status-consistency --project ai-system`, `check-qa-evidence --project ai-system`, and `validate-workflow --project ai-system`.
- Register any incomplete V1 artifact only after reviewing a complete recovery artifact and fingerprinting both files.
- Keep failures in other workflow projects visible in global validation, but separate from AI System's project-scoped result.

## Privacy And Residual Risk

- This handoff contains no raw project evidence, client data, secrets, credentials, or production identifiers.
- A valid fingerprint establishes immutability, not the truth of historical QA claims. Formal closure still needs current evidence and owner approval.
