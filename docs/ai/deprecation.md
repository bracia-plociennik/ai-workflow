# deprecation.md

## Archive Policy

Old project artifacts are archived or superseded, not silently deleted.

## Superseded Artifacts

When an artifact is replaced:

- mark the old artifact as `superseded`;
- link to the replacement;
- keep historical decisions immutable;
- create a new decision to supersede an old decision by reference.

## Active Artifact Rule

Only one active spec is allowed per task/package.

If duplicates exist:

- choose a canonical artifact;
- record duplicate paths;
- stop when duplicates conflict on scope, risk, or acceptance criteria.

## Deprecated Workflow Files

Workflow file migrations must be recorded in `docs/ai/changelog.md`.
