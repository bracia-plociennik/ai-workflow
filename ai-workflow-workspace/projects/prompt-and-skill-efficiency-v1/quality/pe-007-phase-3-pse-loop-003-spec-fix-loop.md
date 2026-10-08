# PE-007 Phase 3 Specification Fix Loop: PSE-LOOP-003

## Trigger And Baseline

- Trigger: full validation of the first four-file implementation stopped at `check-naming` on historical, ignored frozen eval files. This is not a defect in the new pre-quality route, but it prevents the accepted full-validation DoD.
- Source baseline: tracked HEAD `6e483fdc26d309ef94d9690d0991fb45c417a3f5`, four approved LOOP-003 files modified, no fifth tracked file changed before this fix loop.
- Owner decision: PE-007 approves `.systems/scripts/check-naming` and related smoke coverage, conditional on fresh Spec QA and pre-write readiness. PE-006 remains the authority for the original four files.

## Specification Correction

- Exact write set is now five files; no other tracked file is authorized.
- DoD item 7 requires a `freeze.md`-scoped exemption only for `fixture/**` and `runs/<run>/checkout/**` raw eval inputs. Canonical eval artifacts, unrelated workspace files and tracked source remain checked.
- L3b adds the naming validator and positive/negative smoke cases. The frozen inputs themselves remain immutable.
- Existing LOOP-003 behavior, risk, permissions, STOP boundaries, paired eval evidence and formal quality route remain unchanged.

## Review And Next Route

- Full amended spec reread against owner instruction, PE-006/PE-007, current source, naming validator, smoke runner and the failed full-validation trace.
- No missing approval for the five named files; this note grants no new permission, phase transition or quality verdict.
- Next: fresh `phase-3-spec-qa` for PE-007 scope before any `check-naming` source write.
