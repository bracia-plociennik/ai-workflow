# Prompt Module Template

## Metadata

| Field | Value |
| --- | --- |
| `module-id` | `<kebab-case-id>` |
| `module-type` | `prompt-module` |
| `status` | `draft` |
| `owner` | `<system|project|human>` |
| `applies-to` | `<phase|task-type|project-type|global-support>` |

## Purpose

Describe the narrow behavior this module frames.

## Inputs

- Required context:
- Optional context:
- Source artifacts:

## Allowed Influence

This module may:

- organize context;
- shape output format;
- require explicit assumptions;
- require source labels;
- sharpen review stance.

## Forbidden Overrides

This module must not:

- authorize writes;
- approve implementation;
- skip phases or gates;
- weaken risk, permissions, evidence, or Definition of Done;
- override `AGENTS.md`, core policy, phase files, accepted specs, or owner decisions.

## Output Contract

Expected output shape:

- Section or field:
- Required evidence:
- Required assumptions:

## Source Labels

Label inputs as:

- `owner-provided`
- `accepted-artifact`
- `repo-state`
- `memory`
- `generated`
- `inferred`

## Refresh Conditions

Refresh this module use when:

- accepted context changes;
- project status changes;
- architecture, plan, or spec changes;
- owner decision changes;
- source conflict is detected.

## Notes

Add module-specific guidance here.

