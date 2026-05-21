# Change Requests

This directory stores project-local owner change request entries.

Use this directory for:

- owner comments before `final-owner-yes`;
- rejected final approval with required corrections;
- additions, removals, corrections, or decision rollbacks after `final-owner-yes`;
- triage records that decide whether a request is a micro-task, fix loop, new task, new project iteration, decision rollback, or new project.

## Naming

Use:

```text
YYYY-MM-DD-<project>-cr-<nnn>-<slug>.md
```

## Rules

- Do not treat a chat comment as complete until it has a change request entry or is explicitly rejected as non-material.
- Pre-final blocking change requests block `final-owner-yes`.
- Post-final change requests never rewrite old final approval evidence.
- Do not use change requests to bypass quality, approval, risk, permissions, or Definition of Done.
