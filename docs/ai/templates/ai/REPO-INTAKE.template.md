# Repo Intake

## Metadata

| Field | Value |
| --- | --- |
| `repo_name` | `<fill in target repo>` |
| `repo_path` | `<fill in target repo>` |
| `date` | `<YYYY-MM-DD>` |
| `result` | `<PASS|BLOCKED>` |
| `active_project_workspace` | `<none|docs/projects/<project>>` |
| `workflow_ready` | `<yes|no>` |
| `autopilot_ready` | `<yes|no|not_applicable>` |
| `owner_action_required` | `<none|specific action>` |

## Command Map

| Command Type | Command | Status | Safety Notes |
| --- | --- | --- | --- |
| install | `not configured` | `<usable|missing|unsafe>` | |
| dev server | `not configured` | `<usable|missing|unsafe>` | |
| test | `not configured` | `<usable|missing|unsafe>` | |
| lint/style check | `not configured` | `<usable|missing|unsafe>` | |
| typecheck | `not configured` | `<usable|missing|unsafe>` | |
| build | `not configured` | `<usable|missing|unsafe>` | |
| migration/schema check | `not configured` | `<usable|missing|unsafe|not_applicable>` | |
| scheduler/queue | `not configured` | `<usable|missing|unsafe|not_applicable>` | |
| e2e/browser tests | `not configured` | `<usable|missing|unsafe|not_applicable>` | |

## Safe Environment

- Test database strategy:
- Fake/log/array/test service strategy:
- Mail/notification strategy:
- Queue/background job strategy:
- External API strategy:
- Commands that must never run against production:
- Dependency install policy:
- Migration policy:
- Secret/credential policy:

## Repo Risk Register

| Area | Risk | STOP Condition | Safe Default |
| --- | --- | --- | --- |
| secrets | plaintext credentials or production env | production/private secret access | fake/test references only |
| database | destructive migration or real data change | destructive or production DB operation | additive test migration only |
| external effects | emails, alerts, tickets, API writes | real customer/user side effect | fake/log/array/test adapters |
| legal/ToS | scraping, paid vendor, privacy | legal/ToS-sensitive action | STOP for owner approval |
| git/release | force-push, tag deletion, release | destructive git/release operation | branch + commit after PASS |

## Gate Decision

```text
result: <PASS|BLOCKED>
blocking_reason: <none|reason>
next_valid_step: <create project workspace|project intake|fix repo workflow docs|owner decision>
```
