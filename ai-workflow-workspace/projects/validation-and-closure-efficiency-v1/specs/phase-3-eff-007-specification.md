# EFF-007 Specification

## Owner Intent

Fingerprint actual opened contracts and scope/stage; selective full refresh checks current authority; environment checked early.

## Scope

instruction-adherence-refresh.md; validation-observability.md; lib/execution-efficiency.py. Approved source writes are restricted to this upstream project, supporting docs/integrations and meaningful tests. Unknown dependent effects stop or execute fresh. No AI System edit.

## Definition of Done

Resume with changed scope/source cannot silently continue; ps/tools/writable output fail before expensive checks.

## Implementation Slice Plan

Source: accepted owner plan/context, this spec and current contracts. DoD source: this specification. Slice 1 implements the owned behavior; slice 2 adds adversarial cases and integrations; slice 3 performs current-diff findings-first QA and records execution evidence. Stop on changed scope, missing permissions, invalid inputs or unknown dependencies. Quality is required after fixes.

## Plan Quality Contract

- Plan classification: implementation-capable
- DoD source: context.md and the accepted owner plan in this conversation.
- Testable DoD / acceptance conditions: seven capabilities work; current/history separation preserves bytes; producer validates supplied review; reuse rejects changed, incomplete or forged evidence; coverage preserved.
- Artifact QA route: phase-3-spec-qa
- Artifact QA trigger: before the first write of each task.
- Implementation Quality Closure route: phase-5-quality
- Required verification: adversarial Python tests, producer-consumer audit, three comparable synthetic samples per scenario, existing smoke suite, explicit full validation.
- Quality-ready criteria: no unresolved P0/P1/material P2; all seven scope checks and regression evidence complete.
- Owner opt-out: none
- Not-applicable reason: none
- Blocking decision: none
- Next route: specification QA, approved implementation slices, phase 5, phase 6, phase 7, owner-triggered phase 8 awaiting final-owner-yes.
