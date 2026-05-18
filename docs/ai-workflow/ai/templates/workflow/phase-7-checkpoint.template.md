# 7. Checkpoint

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Scope:
- Workflow phase: `7. CHECKPOINT PROJEKTU`
- Result: `<PASS|FAIL|completed|blocked>`

## Inputs

- Repo memory: `docs/ai-workflow/repo/memory.md`
- External workflow memory: `docs/ai-workflow/ai/external-memory.md`
- Project memory: `docs/ai-workflow/projects/<project>/project-memory.md`
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
| `docs/ai-workflow/ai/external-memory.md` | |
| `docs/ai-workflow/projects/<project>/project-memory.md` | |

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
