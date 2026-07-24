# validation-routing.md

## Purpose

Separate semantic and product QA from AI Workflow script validation. Workflow scripts are applicable supporting evidence, never the source of a quality verdict.

## Required Order

For every QA or quality closure:

1. compare the work with owner intent, DoD, accepted plan/spec, and scope;
2. perform findings-first code, diff, or artifact review;
3. inspect edge cases, regression, failure paths, skipped checks, and residual risk;
4. run target-product tests, builds, and manual checks that are safe and applicable;
5. run only applicable `.systems/scripts/**` checks as supporting evidence;
6. issue the final artifact-appropriate verdict.

Green scripts do not equal `PASS`. A semantic mismatch, unresolved blocker, material finding, incomplete DoD, or missing required product evidence cannot be overridden by script output.

## Routing Matrix

| Work | Semantic/Product QA | Workflow Scripts |
| --- | --- | --- |
| Working phases and phase 4 implementation | required according to the current artifact or code | no broad AI Workflow validation |
| Architecture, Plan, Packaging, and Spec QA | artifact-semantic QA first | targeted artifact validators only when applicable |
| Product phase 5 | product tests and full implementation QA | only when workflow contracts or runtime artifacts changed |
| Phase 6 distillation | capture, privacy, source, and state review | only required capture/privacy/state checks |
| Phase 7 checkpoint | checkpoint semantic review first | explicit `full` profile when required by checkpoint policy |
| CI, final system verification, high-impact workflow maintenance | full semantic current-diff review first | explicit `full` profile |

Ordinary product implementation, PDF generation, document work, design work, and other non-workflow implementation must not run broad AI Workflow validation solely because AI Workflow governs the task.

## Required Evidence

QA artifacts and substantive closures record:

```text
Validation Execution Record
- Semantic QA result:
- Findings/blockers:
- Product checks:
- Workflow script applicability:
- Targeted workflow commands:
- Script evidence role: supporting-only
- Final verdict:
```

`Workflow script applicability` is `applicable` or `not-applicable` with a reason. `Final verdict` must be derived from the complete semantic/product evidence, not script status.

## Authority Boundary

Validation routing does not weaken DoD, PASS Integrity, findings-first review, risk, permissions, owner approvals, phase gates, or required evidence. A skipped inapplicable workflow script is not a skipped product check.
