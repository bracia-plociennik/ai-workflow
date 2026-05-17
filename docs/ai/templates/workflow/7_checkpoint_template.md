# 7. Checkpoint

## Metadata

- Project: `<project>`
- Date: `<YYYY-MM-DD>`
- Scope:
- Workflow phase: `7. CHECKPOINT PROJEKTU`
- Result: `<PASS|FAIL|completed|blocked>`

## Inputs

- Repo memory: `docs/ai/REPO-MEMORY.md`
- External workflow memory: `docs/ai/EXTERNAL-MEMORY.md`
- Project memory: `docs/projects/<project>/PROJECT-MEMORY.md`
- Distillations processed:
- Architecture: `docs/projects/<project>/architecture/1_architecture_phase.md`
- Project plan: `docs/projects/<project>/planning/2_project_plan.md`
- Repo state checked:

## Distillations Processed

| Distillation | memory_in_repo_memory Before | Processed? | memory_in_repo_memory After |
| --- | --- | --- | --- |
| | `<true|false>` | `<yes|no>` | `<true|false>` |

## Memory Updates

| Memory File | Update Summary |
| --- | --- |
| `docs/ai/REPO-MEMORY.md` | |
| `docs/ai/EXTERNAL-MEMORY.md` | |
| `docs/projects/<project>/PROJECT-MEMORY.md` | |

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
