# 7. Checkpoint

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Scope:
- Workflow phase: `7. CHECKPOINT PROJEKTU`
- Result: `<PASS|FAIL|completed|blocked>`

## Inputs

- Repo memory: `docs/repo/memory.md`
- External workflow memory: `docs/ai/external-memory.md`
- Project memory: `docs/projects/<project>/project-memory.md`
- Distillations processed:
- Architecture: `docs/projects/<project>/architecture/phase-1-architecture.md`
- Project plan: `docs/projects/<project>/planning/phase-2-project-plan.md`
- Repo state checked:

## Distillations Processed

| Distillation | memory-in-repo-memory Before | Processed? | memory-in-repo-memory After |
| --- | --- | --- | --- |
| | `<true|false>` | `<yes|no>` | `<true|false>` |

## Memory Updates

| Memory File | Update Summary |
| --- | --- |
| `docs/repo/memory.md` | |
| `docs/ai/external-memory.md` | |
| `docs/projects/<project>/project-memory.md` | |

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
