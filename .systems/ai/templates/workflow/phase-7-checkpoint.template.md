# 7. Checkpoint

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Scope:
- Workflow phase: `7. CHECKPOINT PROJEKTU`
- Result: `<PASS|FAIL|completed|blocked>`

## Inputs

- Repo memory router: `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md`
- Repo memory entries: `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/`
- External workflow memory router: `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md`
- External workflow memory entries: `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/`
- System insights router: `AI_WORKFLOW_WORKSPACE_HOME/system-insights/system-insights.md`
- System insight entries: `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/`
- Project memory router: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory.md`
- Project memory entries: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory/`
- Distillations processed:
- Architecture: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/architecture/phase-1-architecture.md`
- Project plan: `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/planning/phase-2-project-plan.md`
- Repo state checked:

## Distillations Processed

| Distillation | memory-in-repo-memory Before | Processed? | memory-in-repo-memory After |
| --- | --- | --- | --- |
| | `<true|false>` | `<yes|no>` | `<true|false>` |

## Memory Updates

| Memory File | Update Summary |
| --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/core/memory.md` | |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/` | |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/external-memory.md` | |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/` | |
| `AI_WORKFLOW_WORKSPACE_HOME/system-insights/system-insights.md` | |
| `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/` | |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory.md` | |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory/` | |

## Project Memory Entries

| Entry File | Type | Scope | Status | Router Updated |
| --- | --- | --- | --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/projects/<project>/memory/<YYYY-MM-DD-short-kebab-title>.md` | `<project-decision|project-constraint|project-risk|implementation-note|testing-note|drift-note|watch-item>` | `<scope>` | `<active|superseded|deprecated>` | `<yes|no>` |

## Repo Memory Entries

| Entry File | Type | Scope | Status | Router Updated |
| --- | --- | --- | --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/repo/memory/<YYYY-MM-DD-short-kebab-title>.md` | `<repo-fact|repo-rule|repo-constraint|repo-risk|command-note|integration-note|testing-note|deployment-note>` | `repo-wide` | `<active|superseded|deprecated>` | `<yes|no>` |

## External Memory Entries

| Entry File | Type | Scope | Privacy Check | Promotion Path |
| --- | --- | --- | --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/<YYYY-MM-DD-short-kebab-title>.md` | `<recommendation|rule|anti-pattern|template-change|skill-improvement|open-question>` | `<scope>` | `<pass|fail|n/a>` | `<target|n/a>` |

## System Insight Entries

| Entry File | Category | Status | Privacy Check | Skill Candidate |
| --- | --- | --- | --- | --- |
| `AI_WORKFLOW_WORKSPACE_HOME/system-insights/insights/<YYYY-MM-DD-short-kebab-title>.md` | `<frontend|backend|smart-contracts|seo|ads|offer|process|quality|client-work|product|skills>` | `<proposed|accepted|promoted-to-skill|superseded|rejected>` | `<pass|fail>` | `<yes|no>` |

## Drift Review

| Drift | Classification | Impact | Required Action |
| --- | --- | --- | --- |
| | `<critical|warning|informational>` | | |

## Consistency Check

- Repo vs architecture: `<PASS|FAIL>`
- Repo vs plan/specs: `<PASS|FAIL>`
- Memory vs repo: `<PASS|FAIL>`
- System insights privacy/scope, if used: `<PASS|FAIL|n/a>`
- Status vs artifacts: `<PASS|FAIL>`

## Checkpoint Gate

- Distillations processed atomically: `<yes|no>`
- Memory updated without mechanical copy-paste: `<yes|no>`
- Critical drift resolved or escalated: `<yes|no|none>`
- Can continue project workflow: `<yes|no>`
- Blocking reason: `<none|reason>`

## Owner Decision Checkpoint

- Interaction mode: `<interactive|queued|suppressed-owner-opt-out|none>`
- Decision state: `<clear|awaiting-owner|blocked|queued>`
- Material decisions: `<decision IDs|none>`
- Questions asked: `<decision IDs|none>`
- Auto-resolved reversible decisions: `<decision IDs|none>`
- Optional owner refinements: `<list|none>`
- Decision artifacts: `<paths|none>`
- Next route:

## Optional Knowledge Capture

- Capture recommended: `<yes|no>`
- Target: `<project-memory|repo-memory|external-memory|system-insights|decision-artifact|status|none>`
- Reason:
- Owner decision required: `<yes|no>`
- Owner decision: `<capture-now|defer-to-distillation|defer-to-checkpoint|reject|not-requested>`
- Privacy/scope check: `<pass|fail|n/a>`
- Suggested entry title:
- Suggested entry summary:
