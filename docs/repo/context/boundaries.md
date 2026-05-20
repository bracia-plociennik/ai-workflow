# Repository Boundaries

- In scope for this repository: workflow docs, templates, example artifacts, repo-local runtime artifacts, and human runbook docs.
- Out of scope for this repository: application code, real product architecture, production deployment, secrets, customer data, paid vendor commitments, and target-repository domain facts outside `docs/repo/` examples.
- Target install boundary: in target repositories, AI Workflow is workflow-owned only as the nested clone directory `ai-workflow/` plus the root `AGENTS.md` shim copied or merged from `ai-workflow/docs/ai/templates/root-agents.template.md`.
- Target-owned roots: target repository `README.md`, existing `AGENTS.md`, `HUMANS.md`, `docs/`, `scripts/`, `.github/`, product code, app config, CI, and deployment files must not be overwritten by AI Workflow.
