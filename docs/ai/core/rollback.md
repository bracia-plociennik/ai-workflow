# rollback.md

## Purpose

High-risk and production-impacting tasks must define how to recover safely.

If rollback is requested before or after `final-owner-yes`, first capture the owner request as a change request under `docs/projects/<project>/change-requests/`, then route to the correct rollback, fix loop, or workflow phase.

## Required Rollback Notes

Include rollback notes when a task touches:

- persistent data;
- migrations;
- auth or permissions;
- billing or payments;
- external integrations;
- infrastructure;
- production deployment behavior;
- irreversible side effects.

## Rollback Content

Document:

- rollback method;
- data migration reversal or forward-fix strategy;
- feature flag status;
- deploy order;
- monitoring signals;
- failure thresholds;
- owner approval needed for rollback;
- known irreversible parts.

## PASS Rule

For applicable tasks, missing rollback notes block `PASS`.
