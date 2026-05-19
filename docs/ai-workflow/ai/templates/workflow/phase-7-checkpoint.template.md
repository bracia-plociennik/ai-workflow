# 7. Checkpoint

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Scope:
- Workflow phase: `7. CHECKPOINT PROJEKTU`
- Result: `<PASS|FAIL|completed|blocked>`

## Inputs

- Repo memory router: `docs/ai-workflow/repo/memory.md`
- Repo memory entries: `docs/ai-workflow/repo/memory/`
- External workflow memory router: `docs/ai-workflow/ai/external-memory.md`
- External workflow memory entries: `docs/ai-workflow/ai/external-memory/`
- Project memory router: `docs/ai-workflow/projects/<project>/memory.md`
- Project memory entries: `docs/ai-workflow/projects/<project>/memory/`
- Distillations processed:
- Architecture: `docs/ai-workflow/projects/<project>/architecture/phase-1-architecture.md`
- Project plan: `docs/ai-workflow/projects/<project>/planning/phase-2-project-plan.md`
- Repo state checked:

## Distillations Processed

| Distillation | memory-in-repo-memory Before | Processed? | memory-in-repo-memory After |
| --- | --- | --- | --- |
| | `<true|false>` | `<yes|no>` | `<true|false>` |

## Memory Updates

| Memory File | Update Summary |
| --- | --- |
| `docs/ai-workflow/repo/memory.md` | |
| `docs/ai-workflow/repo/memory/` | |
| `docs/ai-workflow/ai/external-memory.md` | |
| `docs/ai-workflow/ai/external-memory/` | |
| `docs/ai-workflow/projects/<project>/memory.md` | |
| `docs/ai-workflow/projects/<project>/memory/` | |

## Project Memory Entries

| Entry File | Type | Scope | Status | Router Updated |
| --- | --- | --- | --- | --- |
| `docs/ai-workflow/projects/<project>/memory/<YYYY-MM-DD-short-kebab-title>.md` | `<project-decision|project-constraint|project-risk|implementation-note|testing-note|drift-note|watch-item>` | `<scope>` | `<active|superseded|deprecated>` | `<yes|no>` |

## Repo Memory Entries

| Entry File | Type | Scope | Status | Router Updated |
| --- | --- | --- | --- | --- |
| `docs/ai-workflow/repo/memory/<YYYY-MM-DD-short-kebab-title>.md` | `<repo-fact|repo-rule|repo-constraint|repo-risk|command-note|integration-note|testing-note|deployment-note>` | `repo-wide` | `<active|superseded|deprecated>` | `<yes|no>` |

## External Memory Entries

| Entry File | Type | Scope | Privacy Check | Promotion Path |
| --- | --- | --- | --- | --- |
| `docs/ai-workflow/ai/external-memory/<YYYY-MM-DD-short-kebab-title>.md` | `<recommendation|rule|anti-pattern|template-change|skill-improvement|open-question>` | `<scope>` | `<pass|fail|n/a>` | `<target|n/a>` |

## Drift Review

| Drift | Classification | Impact | Required Action |
| --- | --- | --- | --- |
| | `<critical|warning|informational>` | | |

## Consistency Check

- Repo vs architecture: `<PASS|FAIL>`
- Repo vs plan/specs: `<PASS|FAIL>`
- Memory vs repo: `<PASS|FAIL>`
- Status vs artifacts: `<PASS|FAIL>`

## Checkpoint Gate

- Distillations processed atomically: `<yes|no>`
- Memory updated without mechanical copy-paste: `<yes|no>`
- Critical drift resolved or escalated: `<yes|no|none>`
- Can continue project workflow: `<yes|no>`
- Blocking reason: `<none|reason>`
