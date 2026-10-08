# Controlled Baseline Manifest

- Baseline root: `/private/tmp/ai-workflow-pse-controlled-baseline`.
- Created locally from tracked `main` HEAD `7a904f736eaf029bea750c3a735cd53fa61ef4c0`; no network source.
- Per-case execution uses an independent copy at `/private/tmp/ai-workflow-pse-case-<id>` so fixture writes and runtime reads cannot affect another case.
- Model: GPT-6 Sol High, isolated subagent per case; owner approved local synthetic evaluation.
- Prompt source: `evals/evals.json`, version with `skill-source.md` near-miss fixture. Candidate must use the same prompt text, effort and permissions.
- Runtime context is fixed under the snapshot's `ai-workflow-workspace/repo/core/{status,context,repo-intake}.md`; agents must not read the live project workspace.
- Tracked checkout is clean at snapshot creation (`## main...origin/main`). Fixture output copies may differ per case; the master snapshot must not be changed after this manifest.

## Master Input SHA-256

| File | SHA-256 |
| --- | --- |
| `evals/fixtures/backend-only-near-miss/case.md` | `5ba3639975154f5f12ffa53bf6ee9f04df12b3c6007ea765a9d40405ef9702a4` |
| `evals/fixtures/blockchain-review/case.md` | `a026f8e7716a6f0f1e71664be9c3505f86924e1fe919f159e197182d8965e9cf` |
| `evals/fixtures/formal-phase-qa/case.md` | `d0f7d43c495be08cff6694e87033258bffd1538d551ec2e1983a39096049e469` |
| `evals/fixtures/local-completion-loop/math_utils.py` | `7685e31107a63a83f5cc1b0e0c7ac940c2dcf4bdb74b8ba023ad147423e9d157` |
| `evals/fixtures/local-completion-loop/test_math_utils.py` | `a48845881353aaca66840af90efceeb94b5c4ff0b55c95a8899f61edb9a31ebb` |
| `evals/fixtures/security-readonly/case.md` | `d5c99af7f7a2e33cdfc492daf1c504d88ed3e7a832b40157340dcc4522cdd044` |
| `evals/fixtures/skill-review-near-miss/skill-source.md` | `203f8e003255919611d2393d162018a5d6945729f30da9a3d30276b0139bb03d` |
| `evals/fixtures/tiny-doc-fix/README.md` | `217dc6623dc13972f776afa7fe7dc25f767fc394b93a29b76195e7b9bd9dfe6a` |
| `repo/core/status.md` | `b669fde197b78b238923dbddf7db0bfd022da34873b0a7da042677f9e1410ca2` |
| `repo/core/context.md` | `069e8a7dd86ba8db1dca632b7f449427412578d360a187a651e4949c11ee88f9` |
| `repo/core/repo-intake.md` | `b33983a8dfbe0a6b434113f914df901d92890d5aeebf94e9e9f452af786bc82d` |

## Evidence Limits

- Snapshot is outside the official repo and is not a commit or production artifact.
- Agent-reported opened files are self-report, not complete instrumented tool telemetry. Tokens, actual open count and wall-time comparison remain unknown unless exposed by a reliable source.
- A controlled baseline can establish behavioral differences and forbidden-action absence on these cases, not statistical reliability or universal correctness.
- Candidate runs must start from a copy of the same master snapshot with only the reviewed candidate instruction changes; reset each write-enabled fixture before a paired case.
