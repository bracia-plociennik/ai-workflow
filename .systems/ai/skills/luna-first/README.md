# Luna-first

Native task-model routing for an explicitly activated source-pinned local component. See [SKILL.md](SKILL.md) for use and [the core contract](../../core/luna-first.md) for scope and lifecycle.

The global installer assembles the matching Workflow consumer, System adapter and skill in an immutable private local bundle. The bundled scripts/manage.py verifies that active bundle before delegation. The source skill alone does not activate or launch agents. No root-chat model switching, recursive agents, command executor, background service or automatic Phase8.

Verification: check-luna-first, check-system-skills and skill quick validation; native model/handle evidence is separate from synthetic tests. Explicit read-only is inspect-only.
