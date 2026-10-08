# Static Baseline Preflight

Observed on 2026-09-24 before tracked source changes. This is not a behavioral evaluation and does not satisfy the stage 0 baseline gate.

## Repository Baseline

- Official upstream `main` and `origin/main`: `7a904f736eaf029bea750c3a735cd53fa61ef4c0`.
- Tracked worktree: clean at observation; `ai-workflow-workspace/**` remains ignored/untracked.
- `AGENTS.md`: 417 lines, 3917 words. `Always Read First` lists a broad policy set before workflow-governed work.
- `.systems/ai/core/command-routing.md`: 1350 lines, 9299 words.
- Active system skills: frontend, backend-laravel, blockchain, skill-creator. Their `SKILL.md` files contain 69, 67, 102, and 267 lines respectively.
- Only frontend-skill has an active `evals/evals.json` in this checkout.
- The skill-creator eval script scaffolds runs and grading files; it does not execute Codex or prove trigger behavior.

## Frozen Instruction Hashes (SHA-256)

| File | Hash |
| --- | --- |
| `AGENTS.md` | `e5dd2ff9b32022dab2d964a78d086e03d774a600e43db8c69cb7af4bbde03ccc` |
| `.systems/ai/core/command-routing.md` | `b155e80e3f3b4b6d61d23ff6a6b67aac5c216a0742e8b8f5e8a5d918908640da` |
| `.systems/ai/skills/frontend-skill/SKILL.md` | `a6411e67b4c0a61b138848b39a2aaf4b54e35533dc0adf980566f8834e51cee6` |
| `.systems/ai/skills/backend-laravel-skill/SKILL.md` | `ed3105a2853f3736502d7ebbfa61bca20f08966699b031eba3aae9141f4259cf` |
| `.systems/ai/skills/blockchain-skill/SKILL.md` | `cbe204f5900c6de99b8842e13ad0d49db760376fe6ece66569497b2a7b034a82` |
| `.systems/ai/skills/skill-creator/SKILL.md` | `645c67b7ae48994e1b337d6eec637e7510dd30b0d80d91f57288419ffa8284fd` |

## Interpretation Boundary

These counts and hashes make later comparisons reproducible, but they do not show which files an agent actually loads, model token usage, trigger precision, latency, task completion, or QA quality. Those require controlled paired runs and grading against `evals/evals.json`.

## Next Gate

PE-001 owner decision on isolated subagent execution is pending. No tracked source edit or behavioral baseline PASS is allowed before controlled runs are completed and reviewed.
