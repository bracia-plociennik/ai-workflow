# Pre-Run Freeze

- Frozen before the model run on 2026-09-25.
- Official tracked HEAD: `6e483fdc26d309ef94d9690d0991fb45c417a3f5`.
- Disposable checkout: `/private/tmp/pse-loop003-blind.DrMG3b/checkout`, cloned locally from that branch; only a minimal synthetic workspace and task fixture were added.
- Agent-readable fixture: `ai-workflow-workspace/micro-projects/task-state-summary/fixture/` in the disposable checkout.
- Agent-readable context excludes this eval plan, controller rubric, prior LOOP-003 eval, and previous agent trace.
- Prompt SHA-256: `12d3172e7e4b92692204f18d45ca4c58de96f1502c3c46f7f9cae500031c8259`.
- Initial implementation SHA-256: `6003922d0247a7b21441ec592b02d05685e501480b76f76381ce7f193f2fdedc`.
- Test SHA-256: `1dd98623ffedf966242eba1e391c5dfc91b56ecec1cb30456744f3791ec495b6`.
- Controller rubric SHA-256: `448534d3e517a2aeefb1e96647cab0dc04cf3769a7bb0fc50e5972b18b109eaa`.
- Baseline: `python3 -B test_task_summary.py` runs six tests and raises six `NotImplementedError` errors. This baseline is controller evidence, not a post-edit failure.
- Run count: one successful agent start. An infrastructure failure before agent start may be retried without changing frozen inputs and must be disclosed.
- Configuration: `gpt-6-sol`, reasoning effort `high`, `codex exec --ephemeral --ignore-user-config --json`, workspace-write sandbox, no network, no agent-side approval or external access.
