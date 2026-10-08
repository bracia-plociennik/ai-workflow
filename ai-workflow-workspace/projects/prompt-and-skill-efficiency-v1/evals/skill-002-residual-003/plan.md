# SKILL-002 Residual-Gap Eval 003: Description-Only Candidate

## Freeze

- Date: 2026-09-28; paired candidate against eval 001 and eval 002 baselines. No tracked source changes.
- Baseline fixture: `/private/tmp/ai-workflow-skill-002-residual-001-safe`.
- Candidate fixture: `/private/tmp/ai-workflow-skill-002-residual-001-candidate`, a mechanical copy with only the `skill-creator/SKILL.md` frontmatter `description` line changed. The body, root router and all resources remain byte-identical.
- Model/control: fresh ephemeral GPT-6 Sol High, high reasoning effort, read-only sandbox, no user config, same prompt wrapper and exact case prompts as prior baseline runs.
- Comparisons: eval 001 `skill-review-direct` and `skill-eval-resource` versus identical candidate prompts; eval 002 `routine-discovery-near-miss` versus identical candidate prompt. Generic-code near miss from eval 001 is an additional negative baseline but not rerun unless the candidate introduces a regression signal.

## Candidate Hypothesis

- Current description includes broad `work involves ... SKILL.md contracts, README summaries, bundled resources, local eval plans, grading rubrics, skill validators, or skill safety gates` wording.
- Candidate limits activation to a specific skill artifact or its creation, adaptation, update, review, evaluation or packaging; routine discovery for unrelated product work is explicitly excluded.
- Expected: direct skill review and eval-resource cases still open the active skill and required schema. Routine discovery may inspect the frontmatter, but should not read the entire irrelevant skill body or apply its procedure.
- Forbidden: missing a required skill on positive cases, treating a candidate fixture as approved source, writing files, claiming formal PASS, or changing safety authority.

## Grading

- Primary observable: actual `SKILL.md` open command and whether it reads only frontmatter or the full body. Final `Skills used` is secondary, not a replacement for tool trace.
- Promote a residual-gap finding only if candidate behavior improves the negative case without positive-case regression, preferably repeated if the difference is surprising.
- One run per case is directional, not statistical confidence. A tied or unstable result means no source promotion.
- Artifact QA route: read-only adversarial review of copied fixture, one-line diff and rubric before execution.
- Implementation QA route: not-applicable, no tracked implementation writes.
- Output: evidence report under this ignored eval directory; any later active skill change still needs Spec QA PASS and exact high-risk owner approval.
