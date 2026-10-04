# Integration Review

## Identity And Baseline

- Run ID:
- Coordinator ID:
- Parent task / slice:
- Unit / accepted attempt:
- Source snapshot / unit digest / accepted output digest:
- Target scope:
- Confirmed physical destination identity (device/inode):
- Private preparation proof digest:
- Actual destination before / intended after / observed after digests:
- Actual changed paths, modes and deletions:
- Review evidence path and fingerprint:

## Semantic Acceptance

- Reviewer:
- Decision: <accept|abandon>
- Actual diff reviewed:
- Scope and DoD reviewed:
- Conflicts reviewed:
- Findings by severity / blockers:
- Effects known, including partial or no-change outcome:
- Integrated consumer checks / failure paths:
- Skipped checks and impact:
- Residual risk:
- Required recovery / next route:

## Transition Mapping

The orchestrator supplies the closed JSON review fields `reviewer`, `decision`,
`diff_checked`, `scope_checked`, `conflicts_checked`, `findings_reviewed`,
`effects_known`, `after_digest` and `evidence` to integration-confirm or
integration-abandon. Flags reflect the actual review above, not a generated PASS.
`evidence` is a readable relative owning-project path. Hashes bind the observed
destination and evidence. The helper does not perform or authorize integration.

Acceptance verifies integration metadata only. Common task QA, formal Quality,
Phase 6, checkpoint cadence and human approval remain separate. Unknown effects
retain reservations; abandonment does not roll back or release parent task slots.
