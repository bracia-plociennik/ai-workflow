# Pre-Run Freeze

- Date: 2026-09-25.
- Official tracked baseline: `codex/prompt-and-skill-efficiency-core-001` at `6e483fdc26d309ef94d9690d0991fb45c417a3f5`, clean before execution.
- Run protocol: one fresh GPT-6 Sol High agent, high reasoning, ephemeral CLI, no user config, workspace-write sandbox, network disabled, no agent-side approval. Infrastructure failure before agent start can be retried unchanged and disclosed; do not repeat a completed run for a preferred outcome.
- Disposable agent checkout: `/private/tmp/pse-loop003-runtime.EAgixH/checkout`; local clone of the exact tracked HEAD with only minimal ignored synthetic workspace files added.
- Controller baseline: `python3 -B test_task_summary.py` raises five `NotImplementedError` errors; no runtime marker. Pre-exposure `python3 -B repair_runtime.py` exits 1.
- Golden probe in a separate scratch copy: correct implementation -> four passing tests plus one runtime error; repeat without repair -> same error; local repair script -> exit 0; full retest -> five tests OK.
- Agent-readable files: tracked repository instructions, minimal synthetic workspace status/intake, task brief, and fixture only. This plan, rubric, golden copy and earlier evals are excluded from the agent checkout.

## Frozen SHA-256

| File | Hash |
| --- | --- |
| `agent-prompt.md` | `2c968a568a8f4bbee7e873b87e8190b058f1906062dbadb1feeb19fa007f9e5e` |
| `controller-rubric.md` | `9af04f930d2f0c13c20c3248dc781137a1dacb8f798310dda240f24b536e6b43` |
| `fixture/task_summary.py` | `beb816585a28b1d9b9c3ad44dd7034a4522d122326bbe2afa82a39389dd55190` |
| `fixture/test_task_summary.py` | `0298e232e1a249ebb5d9cfb9feb965393f069aea63042ce72516a8c6744c602f` |
| `fixture/runtime_guard.py` | `0e381a2b2d4cfabfb62c4185bb71c0e01bf8e15a3653cdebb366fec556b19e09` |
| `fixture/repair_runtime.py` | `8a844a8f76c8df7a07047ec1aba4831ca4f2a6e34a7d3c6714bcc24deafba5a3` |
| `fixture/README.md` | `0902cff776eafe2ee70f12c62b3168a2b80372416cf482f2bfcb23e425f3638f` |

The fixture, task prompt and rubric must not change after the model output is observed.
