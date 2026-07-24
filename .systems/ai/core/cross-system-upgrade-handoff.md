# cross-system-upgrade-handoff.md

## Purpose

Keep substantive AI Workflow and AI System upgrades intentionally aligned without creating automatic cross-repository writes.

This contract applies to workflow-maintenance upgrades that may be useful in the counterpart system. It does not apply to ordinary product work, client work, or domain lessons.

## Required Decision

Before commit or handoff, record:

```text
Cross-system impact:
- Owner decision: <yes|no|pending>
- Counterpart: <ai-workflow|ai-system|none>
- Handoff artifact: <path|not-required|pending>
```

- `yes`: create one privacy-safe External Memory handoff for the complete accepted scope.
- `no`: use `Counterpart: none` and `Handoff artifact: not-required`, with a short reason.
- `pending`: stop before commit and handoff.

The owner decides shared impact for every substantive system upgrade. A no-question opt-out cannot infer or auto-resolve shared impact.

## Producer And Consumer Contract

Producers:

- workflow-maintenance plan or micro-project artifact;
- substantive pre-commit or handoff response;
- active autopilot decision queue when the decision appears during `running`.

Consumers:

- contract compliance before commit or handoff;
- External Memory handoff creation when the decision is `yes`;
- counterpart adaptation work.

Active autopilot does not interrupt mid-run. It queues the shared-impact decision and stops at `awaiting-owner` before commit or handoff.

## Handoff Requirements

The handoff lives in:

```text
AI_WORKFLOW_WORKSPACE_HOME/external-memory/memory/<date>-<topic>-<counterpart>-handoff.md
```

It must contain:

- concept and intended outcome;
- owner decisions;
- safety and authority boundaries;
- source-system reference paths;
- validators and smoke-test expectations;
- counterpart adaptation checklist;
- privacy/scope check;
- residual risk.

Do not include raw client data, client names, secrets, credentials, production identifiers, project-specific runtime, or copied private repository content.

## Authority Boundary

The decision and handoff are advisory for the counterpart. They do not:

- grant write, commit, push, deployment, or approval authority;
- change source-of-truth order, risk, permissions, DoD, QA, phase gates, or owner approvals;
- automatically modify the counterpart system;
- turn External Memory into project, client, or product-domain memory.
