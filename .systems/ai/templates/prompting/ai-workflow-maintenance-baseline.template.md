# AI Workflow Maintenance Baseline Template

## Metadata

| Field | Value |
| --- | --- |
| `baseline-id` | `ai-workflow-maintenance-baseline` |
| `role-type` | `maintenance` |
| `status` | `draft` |
| `authority` | `advisory` |

## Purpose

Frame work on the AI Workflow template itself.

This baseline helps agents maintain workflow docs, templates, validators, examples, and runtime contracts without weakening source-of-truth order or target-repository safety.

## Maintenance Lens

Prioritize:

- source-of-truth clarity;
- phase gate integrity;
- validator coverage;
- target-repository portability;
- runtime/system ownership boundaries;
- evidence quality;
- owner approval for high-risk changes.

## Required Variables

| Variable | Expected Value Or Source |
| --- | --- |
| `repository-mode` | official upstream or target repository mode |
| `change-type` | policy, template, validator, example, runtime, docs |
| `risk-class` | derived from `.systems/ai/core/risk-model.md` |
| `write-set` | tracked files plus runtime artifacts |
| `validation-commands` | repo intake command map and workflow validators |
| `owner-approval` | required for high-risk or critical-risk changes |

## Forbidden Overrides

This baseline must not:

- treat itself as higher priority than `AGENTS.md`;
- change phase gates without explicit implementation scope;
- weaken validators to pass;
- track official `ai-workflow-workspace/**`;
- write target-repository runtime facts into `.systems/**`;
- skip owner approval for high-risk changes.

## Evidence Expectations

Maintenance work should record:

- changed files;
- relevant policy references;
- validation commands;
- skipped checks and impact;
- residual risks;
- migration or compatibility notes.

## Refresh Conditions

Refresh this baseline when:

- repository mode policy changes;
- phase workflow changes;
- validator policy changes;
- runtime workspace ownership changes;
- autopilot range policy changes.

