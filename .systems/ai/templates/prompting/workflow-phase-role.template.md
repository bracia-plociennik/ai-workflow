# Workflow Phase Role Template

## Metadata

| Field | Value |
| --- | --- |
| `phase-role-id` | `<kebab-case-id>` |
| `phase` | `<phase-name>` |
| `status` | `draft` |
| `authority` | `advisory` |

## Phase Role

Describe the review stance for this workflow phase.

Examples:

- idea validator;
- architecture critic;
- plan reviewer;
- spec QA reviewer;
- implementation reviewer;
- checkpoint reviewer.

## Phase Contract Preservation

The current phase file remains authoritative for:

- input required;
- output required;
- pass criteria;
- fail criteria;
- evidence required;
- next allowed phases;
- stop conditions;
- writes allowed.

## Role Responsibilities

- Challenge assumptions that affect the phase gate.
- Identify missing required evidence.
- Identify hidden decisions.
- Identify unsafe source use.
- Identify scope creep.
- Prefer stricter review when evidence is weak.

## Forbidden Overrides

The phase role must not:

- change the phase contract;
- mark PASS with missing evidence;
- skip fix loops;
- authorize implementation;
- weaken risk or permissions;
- bypass owner approvals.

## Evidence Expectations

List phase-specific evidence expectations:

- Required artifacts:
- Required commands:
- Required manual checks:
- Required owner decisions:

## Refresh Conditions

Refresh this phase role when:

- phase file changes;
- core policy changes;
- project risk changes;
- accepted architecture, plan, or spec changes.

