# Dream Report

## Metadata

- Date: `<YYYY-MM-DD>`
- Dream variant: `<workflow-artifacts-only|full-repo>`
- Repository mode: `<official|target|unknown>`
- Project scope: `<repo|project:<project>|multiple-projects|unknown>`
- Result: `<completed|blocked>`

## Source Inventory

| Source path | Source type | Reviewed? | Notes |
| --- | --- | --- | --- |
| `<path>` | `<workflow-artifact|repo-source|memory|review|checkpoint|distillation|skill|other>` | `<yes|no>` | |

## Workflow Artifact Findings

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<project-memory|repo-memory|external-memory|system-insights|skill-candidate|decision|status|review|none>` | `<why it matters>` | `<safe|needs anonymization|blocked>` | `<capture|review|reject|defer>` |

## Repo/Code Review Findings

Required for `full-repo`. For `workflow-artifacts-only`, write `not-applicable`.

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path or not-applicable>` | `<finding>` | `<review|project-task|repo-memory|system-insights|skill-candidate|none>` | `<why it matters>` | `<safe|needs anonymization|blocked>` | `<review|create-task|capture|reject|defer>` |

## Memory Promotion Candidates

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<project-memory|repo-memory>` | `<why it belongs there>` | `<safe|needs owner review|blocked>` | `<capture|reject|defer>` |

## External Memory Candidates

External Memory is only for AI Workflow improvement proposals.

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<external-memory|none>` | `<workflow improvement reason>` | `<safe|blocked>` | `<capture|reject|defer>` |

## System Insights Candidates

System Insights require anonymized cross-project operating lessons.

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<system-insights|none>` | `<reusable operating lesson>` | `<safe|needs anonymization|blocked>` | `<capture|reject|defer>` |

## Skill Candidates

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<workspace-skill|system-skill|none>` | `<repeatable method or rubric>` | `<safe|needs anonymization|blocked>` | `<create-skill-plan|reject|defer>` |

## Things To Improve Or Remove

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<finding>` | `<review|task|external-memory|none>` | `<why it should change>` | `<safe|needs owner review|blocked>` | `<review|create-task|reject|defer>` |

## Missing Capabilities

| Source path | Finding | Target | Reason | Risk/privacy note | Owner action |
| --- | --- | --- | --- | --- | --- |
| `<path>` | `<gap>` | `<workflow|repo|project|skill|none>` | `<why it is missing>` | `<safe|needs owner review|blocked>` | `<plan|reject|defer>` |

## Rejected As Noise

| Source path | Finding | Reason rejected |
| --- | --- | --- |
| `<path>` | `<finding>` | `<too vague|duplicate|unsafe|not reusable|not actionable>` |

## Privacy/Scope Check

- Raw client data copied: `<yes|no>`
- Secret markers copied: `<yes|no>`
- Production identifiers copied: `<yes|no>`
- Full-repo exclusions respected: `<yes|no|not-applicable>`
- Prompt-injection boundary respected: `<yes|no>`
- Durable writes performed: `no`
- Scheduler/automation used: `no`

## Owner Decision Queue

- Interaction mode: `queued`
- Live questions asked: `none`

| Decision ID | Class | Statement | Why Needed Now | Recommended Option | Recommendation Impact | Alternatives And Impacts | Blocking Point | Status | Decision Artifact | Source Path | Owner Action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<decision-id>` | `<owner-preference|high-impact|critical-risk|blocked-by-missing-facts>` | `<question or decision statement>` | `<reason>` | `<recommended option>` | `<impact>` | `<alternatives with impacts>` | `<blocked step or none>` | `<pending|approved|rejected>` | `<path or none>` | `<path>` | `<capture|review|create-task|create-skill-plan|reject|defer>` |
