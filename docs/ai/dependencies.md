# dependencies.md

## Default Rule

Do not add production dependencies without an approved task scope and the required risk review.

## Approval Requirements

Human approval is required when a dependency:

- is production runtime code;
- affects auth, billing, security, data, or external integrations;
- introduces a paid vendor or lock-in;
- has unclear license terms;
- is unmaintained or has known security advisories;
- materially increases bundle size or runtime cost.

## Evaluation Checklist

Before adding a dependency, record:

- purpose;
- alternatives considered;
- license;
- maintenance status;
- security advisory status;
- package size/performance impact;
- transitive dependency risk;
- removal/rollback path.

## Dev Dependencies

Low-risk local developer tooling may be auto-resolvable when it is scoped to tests, linting, or workflow validation and does not affect production runtime.
