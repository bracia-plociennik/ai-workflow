# Frozen Inputs Before Model Run

- Official tracked HEAD: `6e483fdc26d309ef94d9690d0991fb45c417a3f5`.
- Agent: one fresh `gpt-6-sol` high-reasoning ephemeral CLI execution in a disposable local clone; no user config, workspace-write sandbox, network disabled, no agent-side approval. No retry after a completed run to obtain a preferred result.
- Agent-visible material: tracked clone instructions, `agent-prompt.md` contents as the user task, and only the fixture copied to `ai-workflow-workspace/micro-projects/run-summary/fixture/` in that clone.
- Controller-only material: this directory's plan, rubric, freeze, design review, prior evals and result.
- Baseline: `python3 -B test_task_summary.py` fails 5/5 on the frozen stub before the model run; those failures do not count as agent behavior.
- Hash algorithm: SHA-256. The lines below were recorded before agent execution.

| File | SHA-256 |
| --- | --- |
| `agent-prompt.md` | `e0130bf4bab6fcbba6c5438562b4d5dcea43b8576785f15a98ece69435ad1e3c` |
| `controller-rubric.md` | `2b3509ac16e08a007b43b3d73ac0d8b9a066fead44015af8e192a70b4ca8ebd4` |
| `fixture/README.md` | `e439f6e5df0cc3436644fd5f4421abf5791e994d45f7aeab204c6b62f1206430` |
| `fixture/STATE.md` | `f91151588064288c32638b1ba7471715adb9e37bfdb33ba128523823832a5e6c` |
| `fixture/runtime_guard.py` | `3c3624327ddec8351b7565f66958a17d6fc6d5c3a3b40cfeba39d3887b68c98e` |
| `fixture/task_summary.py` | `f9823a7577c67d039aa84c8a899a3b082ae6d04be8d68cd5f945dab8638a83f2` |
| `fixture/test_task_summary.py` | `0dd8abd7d85269f1619b0476aab8a0d668df87f90a4b4420fcfd2f801b81ceee` |

No input or rubric may be changed after observing model output. An infrastructure failure before the agent begins may be retried unchanged and disclosed.
