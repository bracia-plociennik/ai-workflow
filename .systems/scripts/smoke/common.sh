#!/usr/bin/env bash
# Pure shared function definitions; no execution on import.
run_must_fail() {
  local name="$1"
  shift
  local expected_literal=""
  if [[ "${1:-}" == "--expect-literal" ]]; then
    [[ "$#" -ge 3 && -n "$2" ]] || { echo "Missing --expect-literal value for $name"; exit 1; }
    expected_literal="$2"
    shift 2
  fi
  local output="$tmp/${name}.out"
  local started=$SECONDS
  local started_ns=""
  [[ -z "${AI_WORKFLOW_TIMING_OUTPUT:-}" ]] || started_ns="$(python3 "$timing_helper" now)"
  local status
  local expected_status=1
  local expected_diagnostic='[[:graph:]]'

  case "$name" in
    validation-timing-rejects-existing-output|validation-timing-rejects-escaping-output|validation-timing-rejects-symlink|validation-timing-rejects-tmpdir-override|validation-timing-rejects-tracked-temporary-output|validation-timing-rejects-unignored-temporary-repo-output|validation-timing-rejects-foreign-tracked-output|validation-timing-rejects-foreign-deleted-tracked-output|validation-timing-rejects-foreign-unignored-output|validation-comparison-rejects-incomplete|validation-comparison-rejects-source-mismatch|validation-comparison-rejects-duplicate-record|validation-comparison-rejects-missing-smoke-check|validation-comparison-rejects-nonfinite-duration|validation-comparison-rejects-separate-output|validation-comparison-rejects-oversized-smoke-wall|validation-comparison-rejects-private-fingerprint)
      expected_status=2
      expected_diagnostic='Validation (timing|comparison) error:'
      ;;
    validate-workflow-emits-failure-marker)
      expected_status=7
      expected_diagnostic='^AI_WORKFLOW_VALIDATE_COMPLETE .*result=fail .*exit_code=7'
      ;;
    timeout-wrapper-returns-124|timeout-wrapper-kills-process-group)
      expected_status=124
      expected_diagnostic='^AI_WORKFLOW_TIMEOUT '
      ;;
    update-validation-failure)
      expected_status=7
      expected_diagnostic='^AI_WORKFLOW_UPDATE_VALIDATION_COMPLETE result=fail exit_code=7$'
      ;;
    update-validation-timeout)
      expected_status=124
      expected_diagnostic='^AI_WORKFLOW_UPDATE_VALIDATION_COMPLETE result=timeout exit_code=124$'
      ;;
    qa-evidence-rejects-unsafe-project|naming-rejects-unsafe-project|status-consistency-rejects-unsafe-project)
      expected_status=2
      expected_diagnostic='^Unsafe project slug:'
      ;;
    qa-evidence-rejects-missing-project|status-consistency-rejects-missing-project)
      expected_status=2
      expected_diagnostic='^Selected project does not exist:'
      ;;
    workflow-fast-rejects-unsafe-project)
      expected_diagnostic='^Unsafe project slug:'
      ;;
    qa-evidence-v2-rejects-duplicate-current)
      expected_diagnostic='exactly one top-level Current QA Run is required'
      ;;
    qa-evidence-v2-rejects-duplicate-run-id)
      expected_diagnostic='duplicate QA run ID'
      ;;
    qa-evidence-v2-rejects-stale-input|status-consistency-v2-rejects-stale-input)
      expected_diagnostic='stale or mismatched input SHA-256'
      ;;
    qa-evidence-v2-rejects-traversal)
      expected_diagnostic='unsafe input path'
      ;;
    qa-evidence-v2-rejects-conflicting-gate)
      expected_diagnostic='current verdict and gate decision conflict'
      ;;
    qa-evidence-v2-rejects-subsection-result-conflict|qa-evidence-v2-rejects-phase5-subsection-conflict)
      expected_diagnostic='current Gate Decision subsection conflicts with verdict'
      ;;
    qa-evidence-v2-rejects-subsection-progression)
      expected_diagnostic='current Gate Decision blocks progression despite PASS'
      ;;
    qa-evidence-v2-rejects-pass-fix-loop-route|qa-evidence-v2-rejects-phase5-fix-loop-route)
      expected_diagnostic='current Gate Decision routes PASS to a fix loop'
      ;;
    qa-evidence-v2-rejects-quality-gate-fix-loop-route)
      expected_diagnostic='current Quality Gate routes PASS to a fix loop'
      ;;
    qa-evidence-v2-rejects-report-level-result-conflict)
      expected_diagnostic='report-level Result conflicts with current verdict'
      ;;
    qa-evidence-v2-rejects-final-verdict-conflict)
      expected_diagnostic='report-level Final verdict conflicts with current verdict'
      ;;
    status-consistency-v2-rejects-two-current-assessments)
      expected_diagnostic='multiple V2 assessments for current phase/task'
      ;;
    status-consistency-v2-rejects-current-fail)
      expected_diagnostic='status PASS conflicts with current QA verdict'
      ;;
    status-consistency-v2-rejects-unmatched-task)
      expected_diagnostic='has no QA assessment for its current task despite V2 reports for this phase'
      ;;
    qa-evidence-v2-rejects-fenced-fake-section)
      expected_diagnostic='missing or empty current subsection: Findings'
      ;;
    qa-evidence-v2-rejects-wrong-task-identity)
      expected_diagnostic='current identity does not match report filename'
      ;;
    qa-evidence-v2-rejects-fenced-verdict)
      expected_diagnostic='missing current fields: Verdict'
      ;;
    qa-evidence-v2-rejects-fenced-quality-field)
      expected_diagnostic='missing or incomplete Quality Gate: Cross-contract consistency aligned'
      ;;
    qa-evidence-v2-rejects-unapproved-target-root)
      expected_diagnostic='input root is not approved: approved-target-source'
      ;;
    qa-evidence-v2-rejects-escaping-symlink)
      expected_diagnostic='input artifact escapes approved root'
      ;;
    qa-evidence-v2-rejects-missing-current-dod)
      expected_diagnostic='missing current implementation quality section: Definition Of Done Validation'
      ;;
    qa-evidence-v2-rejects-final-owner-bypass)
      expected_diagnostic='final check cannot close plan before owner approval'
      ;;
    qa-evidence-v2-rejects-owner-mismatch)
      expected_diagnostic='unsatisfied Intent / Plan / Spec Compliance: Owner instruction mismatch'
      ;;
    qa-evidence-v2-rejects-incomplete-adversarial-review)
      expected_diagnostic='unsatisfied Review Completeness Gate: Negative-space / adversarial review'
      ;;
    qa-evidence-v2-rejects-unverified-quality-gate)
      expected_diagnostic='unsatisfied Quality Gate: Cross-contract consistency aligned'
      ;;
    qa-evidence-v2-rejects-incomplete-matrix-row)
      expected_diagnostic='incomplete current adaptive matrix row'
      ;;
    qa-evidence-v2-rejects-failed-completion-row)
      expected_diagnostic='final check PASS has failed completion area'
      ;;
    worktree-bootstrap-stops-self-clone)
      expected_diagnostic='official AI Workflow repository must not clone itself'
      ;;
    pass-without-evidence)
      expected_diagnostic='missing or empty current subsection: Evidence'
      ;;
    pass-with-failed-command|qa-evidence-v2-rejects-failed-artifact-check|qa-evidence-v2-rejects-failed-edge-case)
      expected_diagnostic='current PASS has a failed check or manual result'
      ;;
    qa-evidence-rejects-tampered-recovery|qa-evidence-rejects-wrong-recovery-fingerprint|qa-evidence-rejects-tampered-v1-original|qa-evidence-rejects-missing-v1-recovery)
      expected_diagnostic='registered V1 original or recovery fingerprint mismatch'
      ;;
    qa-evidence-v1-first-overrides-legacy-admission|qa-evidence-selected-project-still-fails)
      expected_diagnostic='V1 marker takes precedence over pre-V1 legacy admission'
      ;;
  esac

  # Every ordinary negative case has a stable, cause-specific diagnostic contract.
  if [[ "$expected_diagnostic" == '[[:graph:]]' && -z "$expected_literal" ]]; then
    case "$name" in
      update-ahead-stops) expected_diagnostic='^AI_WORKFLOW_UPSTREAM_STATE relation=ahead ';;
      update-diverged-stops) expected_diagnostic='^AI_WORKFLOW_UPSTREAM_STATE relation=diverged ';;
      branch-policy-public-blocks-dev-workspace|branch-policy-compat-dev-blocks-local-workspace) expected_diagnostic='Branch policy violation: ai-workflow-workspace/ is tracked\.';;
      branch-policy-public-blocks-legacy-workspace|branch-policy-compat-dev-blocks-legacy-workspace) expected_diagnostic='Branch policy violation: legacy workspace files are tracked under workspace/\.';;
      missing-autopilot-readme-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/autopilot/autopilot-readme\.template\.md';;
      missing-phase-0-init-template) expected_diagnostic='Missing workflow template: \.systems/ai/templates/workflow/phase-0-init\.template\.md';;
      missing-autopilot-readiness-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/autopilot/readiness\.template\.md';;
      missing-prompt-composition-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/prompt-composition\.md';;
      missing-project-prompting-router-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/prompting/project-prompting-readme\.template\.md';;
      missing-system-insights-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/system-insights\.md';;
      missing-contract-compliance-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/contract-compliance\.md';;
      missing-skill-intake-plan-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/workspace/skills/skill-intake-plan\.template\.md';;
      missing-knowledge-capture-gate-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-knowledge-capture-gate';;
      missing-dreaming-mode-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/dreaming-mode\.md';;
      missing-dream-report-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/dreaming/dream-report\.template\.md';;
      missing-dreaming-mode-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-dreaming-mode';;
      missing-quality-review-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/quality-review\.md';;
      missing-global-quality-review-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-global-quality-review-stance';;
      missing-request-batch-triage-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/request-batch-triage\.md';;
      missing-request-batch-triage-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-request-batch-triage';;
      missing-response-evidence-trace-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-response-evidence-trace';;
      missing-phase-skill-discovery-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-phase-skill-discovery';;
      missing-default-quality-closure-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-default-quality-closure';;
      missing-default-idea-validation-opt-out-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-default-idea-validation-opt-out';;
      missing-end-of-task-capture-contract) expected_diagnostic='Missing required artifact: \.systems/ai/core/end-of-task-capture\.md';;
      missing-end-of-task-capture-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/capture/end-of-task-capture\.template\.md';;
      missing-end-of-task-capture-validator) expected_diagnostic='Missing required artifact: \.systems/scripts/check-end-of-task-capture';;
      contract-compliance-requires-side-task-mode) expected_diagnostic='Missing contract compliance reference in \.systems/ai/core/contract-compliance\.md: side-task';;
      contract-compliance-requires-micro-task-knowledge-capture) expected_diagnostic='Missing contract compliance reference in \.systems/ai/templates/projects/micro-task\.template\.md: template contract compliance section';;
      contract-compliance-blocks-medium-risk-micro-project-template) expected_diagnostic='Missing contract compliance reference in \.systems/ai/templates/micro-projects/micro-project\.template\.md: micro-project low-risk contract';;
      contract-compliance-requires-micro-project-work-mode) expected_diagnostic='Missing contract compliance reference in \.systems/ai/templates/micro-projects/micro-project\.template\.md: micro-project work mode';;
      system-skills-blocks-known-project-marker) expected_diagnostic='Project source marker: CHT';;
      system-skills-blocks-machine-specific-path) expected_diagnostic='Source path: /Users/example/project/AGENTS\.md';;
      system-skills-require-intake-plan-for-context) expected_diagnostic='System skill with context/ and active artifacts must include skill-intake-plan\.md: \.systems/ai/skills/context-intake-missing-plan';;
      system-skills-block-context-active-instructions) expected_diagnostic='Always load context/\*\* as active instructions\.';;
      system-skills-block-context-guidance|system-skills-block-context-guidance-in-reference) expected_diagnostic='Use context/\*\* as guidance during skill execution\.';;
      quick-validate-block-context-guidance) expected_diagnostic='Active skill artifact treats context/\*\* as active guidance or authority: \.systems/ai/skills/context-intake-guidance/SKILL\.md';;
      quick-validate-block-context-guidance-in-reference) expected_diagnostic='Active skill artifact treats context/\*\* as active guidance or authority: \.systems/ai/skills/context-reference-guidance/references/source\.md';;
      system-skills-block-long-skill-md) expected_diagnostic='System skill SKILL\.md is too long; keep active contracts compact \(311 lines > 300\): \.systems/ai/skills/context-intake-long/SKILL\.md';;
      system-skills-require-skill-md) expected_diagnostic='Missing system skill artifact: \.systems/ai/skills/skill-creator/SKILL\.md';;
      system-skills-require-readme) expected_diagnostic='Missing system skill artifact: \.systems/ai/skills/skill-creator/README\.md';;
      system-skills-require-frontmatter-name) expected_diagnostic='Missing required frontmatter key '\''name'\'': \.systems/ai/skills/skill-creator/SKILL\.md';;
      system-skills-require-authority-boundary) expected_diagnostic='System skill SKILL\.md missing authority boundary text '\''supporting execution guidance\|advisory'\'': \.systems/ai/skills/skill-creator/SKILL\.md';;
      system-skills-block-claude-cli-marker) expected_diagnostic='Run claude -p for trigger evals\.';;
      system-skills-block-external-cdn) expected_diagnostic='<script src="https://cdn\.example\.invalid/viewer\.js"></script>';;
      system-skills-block-undeclared-yaml-import) expected_diagnostic='import yaml';;
      system-skills-block-python-cache-artifacts) expected_diagnostic='System skill contains generated Python runtime artifacts: \.systems/ai/skills/skill-creator';;
      system-skills-package-blocks-output-inside-skill) expected_diagnostic='Output archive must be outside the skill directory: \.systems/ai/skills/skill-creator/skill-creator\.zip';;
      system-skills-run-eval-blocks-path-traversal) expected_diagnostic='Invalid eval id for filesystem directory: '\''\.\./escape'\''\. Use letters, digits, dots, underscores, or hyphens only; do not use path separators\.';;
      system-skills-run-eval-blocks-config-path-traversal) expected_diagnostic='Invalid configuration for filesystem directory: '\''\.\./escape'\''\. Use letters, digits, dots, underscores, or hyphens only; do not use path separators\.';;
      missing-update-workspace-script) expected_diagnostic='Missing required artifact: \.systems/scripts/update-workspace';;
      system-insights-missing-privacy-check) expected_diagnostic='System Insight entry missing required metadata '\''Privacy check:'\'': \.systems/ai/examples/system-insights/bad-missing-privacy\.md';;
      system-insights-missing-operational-validation) expected_diagnostic='System Insight entry missing required section '\''## 8\. WALIDACJA OPERACYJNA'\'': \.systems/ai/examples/system-insights/bad-missing-operational-validation\.md';;
      system-insights-blocks-raw-client-data) expected_diagnostic='- Contact value person@example\.invalid';;
      system-insights-blocks-product-domain-external-memory) expected_diagnostic='External Memory contains product-domain or System Insight lesson';;
      prompt-composition-blocks-unsafe-authority) expected_diagnostic='Prompt artifacts can override AGENTS\.md and approve implementation\.';;
      prompt-composition-blocks-mixed-denial-grant) expected_diagnostic='Prompt artifacts cannot override AGENTS\.md, but can approve implementation\.';;
      prompt-composition-blocks-prompting-artifacts-authority) expected_diagnostic='Prompting artifacts can approve implementation\.';;
      prompt-composition-blocks-prompt-modules-authority) expected_diagnostic='Prompt modules can authorize writes\.';;
      missing-autopilot-range-in-readiness) expected_diagnostic='Missing planning-range reference in \.systems/ai/templates/autopilot/readiness\.template\.md';;
      missing-micro-task-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/projects/micro-task\.template\.md';;
      missing-micro-project-template) expected_diagnostic='Missing required artifact: \.systems/ai/templates/micro-projects/micro-project\.template\.md';;
      post-plan-empty-tasks|later-phase-empty-tasks) expected_diagnostic='\.systems/ai/examples/projects/EXAMPLE/tasks\.md has no concrete task rows';;
      bad-naming) expected_diagnostic='Invalid Markdown filename \(filesystem\): \.systems/ai/workflow/Phase_8_BAD\.md';;
      naming-requires-frozen-eval-marker) expected_diagnostic='Invalid Markdown filename \(workspace-filesystem\): .*ai-workflow-workspace/projects/EXAMPLE/evals/frozen-run/fixture/STATE\.md';;
      naming-rejects-bad-canonical-eval-artifact) expected_diagnostic='Invalid Markdown filename \(workspace-filesystem\): .*ai-workflow-workspace/projects/EXAMPLE/evals/frozen-run/Result_BAD\.md';;
      naming-rejects-bad-unrelated-workspace-artifact) expected_diagnostic='Invalid Markdown filename \(workspace-filesystem\): .*ai-workflow-workspace/projects/EXAMPLE/Other_BAD\.md';;
      missing-canonical-project-context) expected_diagnostic='\.systems/ai/examples/projects/EXAMPLE is in or past project/context intake but missing canonical context: \.systems/ai/examples/projects/EXAMPLE/context\.md';;
      missing-gate-heading) expected_diagnostic='Missing gate heading';;
      knowledge-capture-requires-phase-block) expected_diagnostic='Missing Optional Knowledge Capture block in \.systems/ai/workflow/phase-0-idea-validation\.md';;
      knowledge-capture-requires-template-field) expected_diagnostic='Missing Optional Knowledge Capture field '\''- Owner decision required:'\'' in \.systems/ai/templates/workflow/phase-0-idea-validation\.template\.md';;
      knowledge-capture-blocks-hard-gate-wording) expected_diagnostic='Agents must write memory after every phase\.';;
      default-quality-chain-requires-architecture-mapping) expected_diagnostic='Missing default quality chaining text in \.systems/ai/core/command-routing\.md: `phase-1-architecture` -> `phase-1-architecture-qa`';;
      default-quality-chain-requires-bez-qa-opt-out) expected_diagnostic='Missing default quality chaining text: bez QA';;
      default-quality-chain-blocks-unsafe-opt-out-wording) expected_diagnostic='Unsafe opt-out wording suggests progression without required QA';;
      default-quality-chain-blocks-default-task-packaging) expected_diagnostic='Plan QA still routes unconditionally to task packaging';;
      default-quality-chain-requires-owner-only-packaging) expected_diagnostic='Missing default quality chaining text in \.systems/ai/workflow/phase-2-task-packaging\.md: optional owner-requested';;
      default-quality-chain-blocks-phase-8-auto-chain) expected_diagnostic='Unsafe wording suggests phase 8 can be started by default quality chaining';;
      dreaming-mode-requires-full-repo-variant) expected_diagnostic='Dreaming Mode policy missing required boundary text: full-repo';;
      dreaming-mode-requires-dream-variant-template-field) expected_diagnostic='Dream report template missing required field or section: Dream variant: `<workflow-artifacts-only\\\|full-repo>`';;
      dreaming-mode-requires-risk-privacy-template-field|dreaming-mode-requires-risk-privacy-per-candidate-section) expected_diagnostic='Section '\''Workflow Artifact Findings'\'' missing required table column '\''Risk/privacy note'\'': \.systems/ai/templates/dreaming/dream-report\.template\.md';;
      dreaming-mode-requires-prompt-injection-boundary) expected_diagnostic='Dreaming Mode policy missing required boundary text: prompt-injection\.md';;
      dreaming-mode-requires-full-repo-exclusions) expected_diagnostic='Dreaming Mode policy missing required boundary text: \\\.git/';;
      dreaming-mode-blocks-automatic-writes-wording) expected_diagnostic='Dreaming Mode writes System Insights automatically\.';;
      dreaming-mode-requires-report-privacy-check) expected_diagnostic='Dream Report privacy check must confirm no raw client data copied';;
      dreaming-mode-blocks-raw-client-data) expected_diagnostic='Dream Report appears to contain raw client data or secret markers';;
      dreaming-mode-blocks-full-repo-not-applicable-report) expected_diagnostic='Full-repo Dream Report cannot mark repo/code review findings not-applicable';;
      dreaming-v2-blocks-placeholder) expected_diagnostic='Dream Report v2 contains unresolved placeholders';;
      dreaming-v2-blocks-duplicate-id) expected_diagnostic='Dream Report v2 contains duplicate recommendation IDs';;
      dreaming-v2-blocks-repeated-without-evidence) expected_diagnostic='Repeated Dream recommendation lacks previous evidence';;
      dreaming-v2-requires-complete-privacy-scope) expected_diagnostic='Dream Report v2 missing required field';;
      global-quality-review-requires-cross-contract-consistency) expected_diagnostic='Missing global quality review reference in \.systems/ai/core/quality-review\.md: Cross-contract consistency';;
      global-quality-review-requires-formal-negative-space-field) expected_diagnostic='Missing global quality review reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: formal quality template field: \^- Negative-space / adversarial review: `<completed\\\|not-applicable\\\|incomplete>`\$';;
      global-quality-review-blocks-green-validator-verdict) expected_diagnostic='green validators are sufficient for PASS';;
      global-quality-review-blocks-fixed-lines-only-review|implementation-slicing-blocks-fixed-lines-only-post-fix-review) expected_diagnostic='post-fix review may inspect only fixed lines';;
      global-quality-review-blocks-current-closure-without-rereview) expected_diagnostic='closure may remain current without full re-review';;
      global-quality-review-blocks-no-findings-with-stale-closure) expected_diagnostic='No findings found may be declared with stale closure';;
      global-quality-review-requires-find-blockers-routing) expected_diagnostic='Missing global quality review reference in \.systems/ai/core/command-routing\.md: find blockers routing';;
      global-quality-review-blocks-advisory-pass-wording) expected_diagnostic='advisory review may mark PASS';;
      global-quality-review-blocks-advisory-produce-pass-wording) expected_diagnostic='advisory review may produce PASS';;
      global-quality-review-blocks-final-review-final-check-wording|end-of-task-capture-blocks-final-review-final-check) expected_diagnostic='final review runs phase-8-final-check';;
      global-quality-review-blocks-final-review-starts-final-check-wording) expected_diagnostic='final review starts phase-8-final-check';;
      global-quality-review-requires-formal-gate-eligibility-field) expected_diagnostic='Missing global quality review reference in \.systems/ai/core/quality-review\.md: formal gate eligibility';;
      global-quality-review-preserves-formal-phase5-pass-fail) expected_diagnostic='Missing global quality review reference in \.systems/ai/workflow/phase-5-quality\.md: formal quality PASS remains';;
      intent-plan-spec-compliance-requires-global-review-lens) expected_diagnostic='Missing intent/plan/spec compliance reference in \.systems/ai/core/quality-review\.md: global review lens: Intent / Plan / Spec Compliance';;
      intent-plan-spec-compliance-requires-phase5-lens) expected_diagnostic='Missing intent/plan/spec compliance reference in \.systems/ai/workflow/phase-5-quality\.md: formal quality lens: Intent / Plan / Spec Compliance';;
      intent-plan-spec-compliance-requires-template-status) expected_diagnostic='Missing intent/plan/spec compliance reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: quality template field: Compliance status';;
      intent-plan-spec-compliance-blocks-qa-pass-without-ac) expected_diagnostic='QA may pass without checking acceptance criteria';;
      intent-plan-spec-compliance-blocks-scope-creep-tests-pass) expected_diagnostic='scope creep is acceptable if tests pass';;
      implementation-slicing-requires-core-local-failure-route) expected_diagnostic='Missing pre-quality local failure route in \.systems/ai/core/implementation-slicing\.md: failed local check trigger';;
      implementation-slicing-requires-phase4-local-failure-route) expected_diagnostic='Missing pre-quality local failure route in \.systems/ai/workflow/phase-4-implementation\.md: failed local check trigger';;
      implementation-slicing-requires-failed-check-retest) expected_diagnostic='Missing pre-quality local failure route in \.systems/ai/core/implementation-slicing\.md: failed-check retest';;
      implementation-slicing-rejects-compound-ignore-exception) expected_diagnostic='Do not assert that a failed local check may be ignored, but a failed local check may be ignored\.';;
      implementation-slicing-rejects-direct-ignore) expected_diagnostic='A failed local check may be ignored\.';;
      implementation-slicing-rejects-permission-bypass) expected_diagnostic='Retry may bypass permissions\.';;
      implementation-slicing-rejects-protected-test-weakening) expected_diagnostic='Protected tests may be weakened\.';;
      implementation-slicing-rejects-green-test-as-formal-pass) expected_diagnostic='Passing tests are formal PASS\.';;
      implementation-slicing-rejects-direct-formal-fix-loop) expected_diagnostic='Phase 4 may go directly to phase-5-fix-loop\.';;
      implementation-slicing-rejects-missing-local-failure-source) expected_diagnostic='Missing implementation slicing artifact: \.systems/ai/core/implementation-slicing\.md';;
      implementation-slicing-rejects-forbidden-retest) expected_diagnostic='Unsafe pre-quality local failure route in \.systems/ai/core/implementation-slicing\.md: failed-check retest forbidden';;
      implementation-slicing-rejects-compound-forbidden-retest) expected_diagnostic='Unsafe pre-quality local failure route in \.systems/ai/workflow/phase-4-implementation\.md: failed-check retest forbidden';;
      implementation-slicing-rejects-forbidden-diagnosis) expected_diagnostic='Unsafe pre-quality local failure route in \.systems/ai/core/implementation-slicing\.md: failure diagnosis forbidden';;
      implementation-slicing-requires-core-contract) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/core/implementation-slicing\.md: contract term: Implementation Slice Plan';;
      implementation-slicing-requires-phase4-slice-plan) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/workflow/phase-4-implementation\.md: phase-4 term: Implementation Slice Plan';;
      implementation-slicing-requires-template-execution-evidence) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/templates/workflow/phase-4-implementation\.template\.md: phase-4 template field: ## Slice Execution Evidence';;
      implementation-slicing-blocks-bypass-qa-wording) expected_diagnostic='slice plan may bypass QA';;
      implementation-slicing-requires-dod-source) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/core/implementation-slicing\.md: contract term: DoD source';;
      implementation-slicing-requires-quality-closure) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/core/implementation-slicing\.md: contract term: Mandatory Quality Closure';;
      implementation-slicing-blocks-pass-without-review) expected_diagnostic='implementation PASS without review';;
      implementation-slicing-blocks-pass-before-findings-review) expected_diagnostic='PASS before findings review';;
      implementation-slicing-blocks-automated-only-pass) expected_diagnostic='automated checks are sufficient for PASS';;
      implementation-slicing-requires-micro-work-routing) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/core/operating-model\.md: operating model side-task/micro-task/micro-project integration';;
      implementation-slicing-requires-micro-task-dod) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/templates/projects/micro-task\.template\.md: \.systems/ai/templates/projects/micro-task\.template\.md Definition of Done';;
      implementation-slicing-requires-micro-project-dod) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/templates/micro-projects/micro-project\.template\.md: \.systems/ai/templates/micro-projects/micro-project\.template\.md Definition of Done';;
      plan-quality-contract-requires-core-contract) expected_diagnostic='Missing plan-quality contract reference in \.systems/ai/core/plan-quality-contract\.md: contract field: ## Plan Quality Contract';;
      plan-quality-contract-requires-implementation-quality-route) expected_diagnostic='Missing plan-quality contract reference in \.systems/ai/templates/workflow/phase-3-specification\.template\.md: Implementation Quality Closure route:';;
      plan-quality-contract-requires-plan-artifact-qa-route) expected_diagnostic='Missing plan-quality contract reference in \.systems/ai/core/command-routing\.md: Codex /plan artifact QA route';;
      plan-quality-contract-blocks-implementation-plan-without-artifact-qa) expected_diagnostic='Implementation-capable plan cannot use not-applicable artifact QA';;
      plan-quality-contract-requires-concrete-dod-source) expected_diagnostic='Plan artifact needs a concrete value for: DoD source';;
      plan-quality-contract-requires-read-only-not-applicable-reason) expected_diagnostic='Read-only plan needs a specific not-applicable reason';;
      plan-quality-contract-blocks-quality-bypass-wording) expected_diagnostic='Plan Quality Contract may bypass QA\.';;
      validation-profile-scoped-requires-checks) expected_diagnostic='--profile scoped requires --checks <check-a,check-b>';;
      validation-profiles-require-standard-default) expected_diagnostic='Missing validation profile reference in \.systems/scripts/validate-workflow: validate-workflow profile support: profile="standard"';;
      validation-profiles-require-ci-explicit-full) expected_diagnostic='Missing validation profile reference in \.github/workflows/ai-workflow-validate\.yml: CI explicit full validation';;
      validation-profiles-require-agents-final-full) expected_diagnostic='Missing validation profile reference in AGENTS\.md near AGENTS finalization explicit full validation';;
      validation-profiles-require-commands-final-full) expected_diagnostic='Missing validation profile reference in \.systems/ai/core/commands\.md near commands final maintenance explicit full validation';;
      validation-profiles-require-readme-reuse-full) expected_diagnostic='Missing validation profile reference in README\.md near README reuse explicit full validation';;
      validation-profiles-require-full-smoke-tests) expected_diagnostic='Missing validation profile reference in \.systems/scripts/validate-workflow: validate-workflow profile support: check-validator-smoke-tests';;
      validation-profiles-block-fast-enough-before-commit) expected_diagnostic='fast is enough before commit';;
      validation-profiles-block-standard-replaces-full) expected_diagnostic='standard may replace full for workflow contracts';;
      validation-profiles-block-skip-smoke-pass) expected_diagnostic='skip smoke tests and mark PASS';;
      request-batch-triage-requires-routing-field) expected_diagnostic='Missing request batch triage reference in \.systems/ai/core/request-batch-triage\.md: triage matrix field: routing';;
      request-batch-triage-requires-risk-field) expected_diagnostic='Missing request batch triage reference in \.systems/ai/core/request-batch-triage\.md: triage matrix field: risk';;
      request-batch-triage-requires-nine-column-matrix) expected_diagnostic='Invalid triage matrix column count at line 119: expected 9, got 8';;
      request-batch-triage-requires-mixed-list-split) expected_diagnostic='Missing request batch triage reference in \.systems/ai/core/request-batch-triage\.md: mixed-list routing: active project and another repo-level item';;
      request-batch-triage-blocks-automatic-implementation-wording) expected_diagnostic='batch triage may implement all items automatically';;
      request-batch-triage-requires-high-risk-owner-decision) expected_diagnostic='Missing request batch triage reference in \.systems/ai/core/request-batch-triage\.md: high-risk routing boundary';;
      response-evidence-trace-requires-section) expected_diagnostic='Missing response evidence trace reference in \.systems/ai/core/response-contract\.md: Execution Trace section';;
      response-evidence-trace-requires-skills-field) expected_diagnostic='Missing response evidence trace reference in \.systems/ai/core/response-contract\.md: trace field: Skills/roles used:';;
      response-evidence-trace-blocks-no-sources-needed) expected_diagnostic='no sources needed';;
      response-evidence-trace-requires-agents-routing) expected_diagnostic='Missing response evidence trace reference in AGENTS\.md: AGENTS execution trace';;
      phase-skill-discovery-requires-metadata-first-agents) expected_diagnostic='Missing phase skill discovery reference in AGENTS\.md: no unrelated full-body read';;
      phase-skill-discovery-requires-metadata-first-operating-model) expected_diagnostic='Missing phase skill discovery reference in \.systems/ai/core/operating-model\.md: no unrelated full-body read';;
      phase-skill-discovery-requires-frontmatter-boundary) expected_diagnostic='Missing phase skill discovery reference in AGENTS\.md: frontmatter boundary';;
      phase-skill-discovery-requires-operating-model) expected_diagnostic='Missing phase skill discovery reference in \.systems/ai/core/operating-model\.md: phase skill discovery';;
      phase-skill-discovery-requires-workspace-first) expected_diagnostic='Missing phase skill discovery reference in \.systems/ai/core/operating-model\.md: workspace skills first';;
      phase-skill-discovery-requires-none-fallback) expected_diagnostic='Missing phase skill discovery reference in \.systems/ai/core/operating-model\.md: Skills used: none';;
      phase-skill-discovery-blocks-skill-approval) expected_diagnostic='skill may approve implementation';;
      default-quality-closure-requires-contract) expected_diagnostic='Missing default quality closure reference in \.systems/ai/core/quality-review\.md: default quality closure';;
      default-quality-closure-requires-opt-out-report) expected_diagnostic='Missing default quality closure reference in \.systems/ai/core/quality-review\.md: Quality skipped by owner opt-out';;
      default-quality-closure-blocks-opt-out-pass) expected_diagnostic='bez QA may continue as PASS';;
      default-quality-closure-requires-verification-opt-out) expected_diagnostic='Missing default quality closure reference in \.systems/ai/core/quality-review\.md: opt-out: bez weryfikacji';;
      default-quality-closure-blocks-without-verification-pass) expected_diagnostic='without verification may count as PASS';;
      default-idea-validation-requires-single-work-default) expected_diagnostic='Missing default idea validation reference in \.systems/ai/core/task-intake\.md: Single new work defaults to Task Idea Validation';;
      default-idea-validation-requires-batch-validation-route) expected_diagnostic='Missing default idea validation reference in \.systems/ai/core/request-batch-triage\.md: validation route';;
      default-idea-validation-requires-opt-out-grammar) expected_diagnostic='Missing default idea validation reference in \.systems/ai/core/task-intake\.md: task intake opt-out: bez idea validation';;
      default-idea-validation-requires-opt-out-reporting) expected_diagnostic='Missing default idea validation reference in \.systems/ai/core/response-contract\.md: required opt-out reporting phrase';;
      default-idea-validation-blocks-risk-bypass-wording) expected_diagnostic='without idea validation may bypass risk checks';;
      end-of-task-capture-requires-trigger-grammar) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/core/end-of-task-capture\.md: trigger grammar';;
      end-of-task-capture-requires-precedence) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/core/end-of-task-capture\.md: precedence rules';;
      end-of-task-capture-requires-privacy-field) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/templates/capture/end-of-task-capture\.template\.md: template field: Privacy/scope check';;
      end-of-task-capture-preserves-distillation-route) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/core/end-of-task-capture\.md: unchanged route: Zrób distillation\.\*phase-6-distillation';;
      end-of-task-capture-preserves-checkpoint-route) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/core/end-of-task-capture\.md: unchanged route: Zrób checkpoint\.\*phase-7-checkpoint';;
      end-of-task-capture-blocks-auto-pass) expected_diagnostic='end task may mark PASS automatically';;
      end-of-task-capture-blocks-auto-final-check) expected_diagnostic='end task runs phase-8-final-check';;
      end-of-task-capture-blocks-project-close) expected_diagnostic='end task may close project without final-owner-yes';;
      end-of-task-capture-blocks-client-names) expected_diagnostic='System Insights may include client names';;
      end-of-task-capture-blocks-external-memory-domain-lessons|knowledge-capture-reminder-blocks-external-memory-frontend-lessons) expected_diagnostic='External Memory stores frontend lessons';;
      knowledge-capture-reminder-requires-contract) expected_diagnostic='Missing file for knowledge capture reminder check: \.systems/ai/core/knowledge-capture-reminder\.md';;
      knowledge-capture-reminder-requires-template) expected_diagnostic='Missing file for knowledge capture reminder check: \.systems/ai/templates/capture/knowledge-capture-reminder\.template\.md';;
      knowledge-capture-reminder-requires-implementation-trigger) expected_diagnostic='Missing knowledge capture reminder reference in \.systems/ai/core/knowledge-capture-reminder\.md: trigger: implementation work completed';;
      knowledge-capture-reminder-requires-new-unrelated-task-trigger) expected_diagnostic='Missing knowledge capture reminder reference in \.systems/ai/core/knowledge-capture-reminder\.md: trigger: the owner starts a new unrelated task';;
      knowledge-capture-reminder-blocks-auto-memory) expected_diagnostic='Knowledge Capture Reminder automatically writes memory';;
      knowledge-capture-reminder-blocks-auto-memory-with-trailing-negation) expected_diagnostic='Knowledge Capture Reminder automatically writes memory; this does not require owner approval';;
      knowledge-capture-reminder-blocks-auto-push) expected_diagnostic='Knowledge Capture Reminder auto-push';;
      knowledge-capture-reminder-blocks-ignored-workspace-commit) expected_diagnostic='commit ignored workspace artifacts';;
      knowledge-capture-reminder-blocks-skip-bypass) expected_diagnostic='skip knowledge capture may bypass phase 6 evidence privacy status gate';;
      knowledge-capture-reminder-blocks-skip-permission-bypass) expected_diagnostic='owner-approved skip capture may bypass permissions and owner approvals';;
      knowledge-capture-reminder-blocks-skip-stop-condition-bypass) expected_diagnostic='no capture may ignore stop conditions';;
      knowledge-capture-reminder-blocks-external-memory-backend-lessons) expected_diagnostic='External Memory stores backend lessons';;
      knowledge-capture-reminder-blocks-external-memory-smart-contract-lessons) expected_diagnostic='External Memory stores smart contract lessons';;
      knowledge-capture-reminder-blocks-external-memory-SEO-lessons) expected_diagnostic='External Memory stores SEO lessons';;
      knowledge-capture-reminder-blocks-external-memory-ads-lessons) expected_diagnostic='External Memory stores ads lessons';;
      knowledge-capture-reminder-blocks-external-memory-advertising-lessons) expected_diagnostic='External Memory stores advertising lessons';;
      knowledge-capture-reminder-blocks-external-memory-paid-media-lessons) expected_diagnostic='External Memory stores paid media lessons';;
      knowledge-capture-reminder-blocks-external-memory-offer-lessons) expected_diagnostic='External Memory stores offer lessons';;
      knowledge-capture-reminder-blocks-external-memory-client-work-lessons) expected_diagnostic='External Memory stores client work lessons';;
      knowledge-capture-reminder-blocks-external-memory-product-lessons) expected_diagnostic='External Memory stores product lessons';;
      knowledge-capture-reminder-blocks-inverse-external-memory-domain-routing) expected_diagnostic='Product lessons belong in External Memory';;
      knowledge-capture-reminder-blocks-system-insights-raw-client-data) expected_diagnostic='System Insights may include raw client data';;
      instruction-adherence-refresh-requires-contract) expected_diagnostic='Missing file for instruction adherence refresh check: \.systems/ai/core/instruction-adherence-refresh\.md';;
      instruction-adherence-refresh-requires-pre-write-trigger) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/instruction-adherence-refresh\.md: trigger: before the first implementation-class write';;
      instruction-adherence-refresh-requires-pre-commit-handoff-trigger) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/instruction-adherence-refresh\.md: trigger: before commit readiness, handoff, or quality closure';;
      instruction-adherence-refresh-requires-resume-trigger) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/instruction-adherence-refresh\.md: trigger: after session resume';;
      instruction-adherence-refresh-requires-compaction-trigger) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/instruction-adherence-refresh\.md: trigger: after context compaction';;
      instruction-adherence-refresh-requires-source-conflict-trigger) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/instruction-adherence-refresh\.md: trigger: when chat, memory, status, repository state, accepted artifacts, or contracts conflict';;
      instruction-adherence-refresh-requires-trace-fields) expected_diagnostic='Missing instruction adherence refresh reference in \.systems/ai/core/response-contract\.md: response trace field: Contracts refreshed: <paths\|not-needed>';;
      response-evidence-trace-requires-instruction-refresh-fields) expected_diagnostic='Missing response evidence trace reference in \.systems/ai/core/response-contract\.md: trace field: Contracts refreshed: <paths\|not-needed>';;
      instruction-adherence-refresh-blocks-chat-memory-may-override-agentsmd) expected_diagnostic='chat memory may override AGENTS\.md';;
      instruction-adherence-refresh-blocks-agent-may-change-default-behavior-without-owner-approval) expected_diagnostic='agent may change default behavior without owner approval';;
      instruction-adherence-refresh-blocks-any-explicit-owner-message-may-bypass-contracts) expected_diagnostic='any explicit owner message may bypass contracts';;
      instruction-adherence-refresh-blocks-instruction-adherence-refresh-grants-write-permission) expected_diagnostic='Instruction Adherence Refresh grants write permission';;
      instruction-adherence-refresh-blocks-instruction-adherence-refresh-may-bypass-permissions) expected_diagnostic='Instruction Adherence Refresh may bypass permissions';;
      instruction-adherence-refresh-blocks-full-refresh-is-required-before-every-message) expected_diagnostic='full refresh is required before every message';;
      instruction-adherence-refresh-blocks-not-needed-is-allowed-after-context-compaction) expected_diagnostic='not-needed is allowed after context compaction';;
      instruction-adherence-refresh-blocks-quality-closure-may-use-a-stale-instruction-baseline) expected_diagnostic='quality closure may use a stale instruction baseline';;
      instruction-adherence-refresh-blocks-chat-history-overrides-agentsmd) expected_diagnostic='chat history overrides AGENTS\.md';;
      instruction-adherence-refresh-blocks-owner-instruction-bypasses-qa) expected_diagnostic='owner instruction bypasses QA';;
      instruction-adherence-refresh-blocks-instruction-adherence-refresh-allows-formal-pass) expected_diagnostic='Instruction Adherence Refresh allows formal PASS';;
      instruction-adherence-refresh-blocks-run-full-refresh-before-every-edit) expected_diagnostic='run full refresh before every edit';;
      instruction-adherence-refresh-blocks-not-needed-is-valid-after-resume) expected_diagnostic='not-needed is valid after resume';;
      instruction-adherence-refresh-blocks-not-needed-is-valid-after-a-long-interruption) expected_diagnostic='not-needed is valid after a long interruption';;
      instruction-adherence-refresh-blocks-quality-closure-uses-stale-instruction-baseline) expected_diagnostic='quality closure uses stale instruction baseline';;
      instruction-adherence-refresh-blocks-every-tracked-contract-change-requires-refresh-before-the-next-write) expected_diagnostic='every tracked contract change requires refresh before the next write';;
      implementation-slicing-requires-instruction-refresh-evidence) expected_diagnostic='Missing implementation slicing reference in \.systems/ai/templates/workflow/phase-4-implementation\.template\.md: phase-4 template field: Instruction refresh';;
      global-quality-review-requires-instruction-baseline) expected_diagnostic='Missing global quality review reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: formal quality template field: \^- Instruction baseline: `<current\\\|stale\\\|blocked>`\$';;
      contract-compliance-requires-instruction-refresh) expected_diagnostic='Missing contract compliance reference in \.systems/ai/core/contract-compliance\.md: Instruction refresh';;
      owner-decision-checkpoints-requires-contract) expected_diagnostic='Missing file for owner decision checkpoint check: \.systems/ai/core/owner-decision-checkpoints\.md';;
      owner-decision-checkpoints-requires-phase-block) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/workflow/phase-1-architecture\.md: checkpoint heading';;
      owner-decision-checkpoints-blocks-duplicate-phase-block) expected_diagnostic='Owner Decision Checkpoint must appear exactly once in \.systems/ai/workflow/phase-1-architecture\.md';;
      owner-decision-checkpoints-requires-template-fields) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/templates/workflow/phase-3-specification\.template\.md: checkpoint field: - Optional owner refinements: `<list\|none>`';;
      owner-decision-checkpoints-requires-owner-preference) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/owner-decision-checkpoints\.md: decision class: owner-preference';;
      owner-decision-checkpoints-requires-owner-preference-in-phase-taxonomy) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/templates/workflow/phase-0-idea-validation\.template\.md: idea validation template taxonomy';;
      owner-decision-checkpoints-requires-recommendation-first) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/owner-decision-checkpoints\.md: behavior: put the recommended option first';;
      owner-decision-checkpoints-requires-question-batch-limit) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/owner-decision-checkpoints\.md: behavior: group at most `1-3` questions';;
      owner-decision-checkpoints-requires-option-impact) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/owner-decision-checkpoints\.md: behavior: provide impact for the recommendation and each alternative';;
      owner-decision-checkpoints-blocks-ask-the-owner-about-every-uncertainty) expected_diagnostic='ask the owner about every uncertainty';;
      owner-decision-checkpoints-blocks-auto-resolve-high-impact-decisions) expected_diagnostic='auto-resolve high-impact decisions';;
      owner-decision-checkpoints-blocks-critical-risk-decisions-are-auto-resolvable) expected_diagnostic='critical-risk decisions are auto-resolvable';;
      owner-decision-checkpoints-blocks-nie-dopytuj-may-bypass-qa) expected_diagnostic='nie dopytuj may bypass QA';;
      owner-decision-checkpoints-blocks-no-question-opt-out-allows-guessed-acceptance-criteria) expected_diagnostic='no-question opt-out allows guessed acceptance criteria';;
      owner-decision-checkpoints-blocks-autopilot-may-ask-live-questions-while-running) expected_diagnostic='autopilot may ask live questions while running';;
      owner-decision-checkpoints-blocks-autopilot-asks-clarification-questions-while-running) expected_diagnostic='autopilot asks clarification questions while running';;
      owner-decision-checkpoints-blocks-autopilot-may-continue-with-a-pending-material-decision) expected_diagnostic='autopilot may continue with a pending material decision';;
      owner-decision-checkpoints-blocks-autopilot-continues-with-a-pending-material-decision) expected_diagnostic='autopilot continues with a pending material decision';;
      owner-decision-checkpoints-blocks-dreaming-mode-may-ask-live-questions) expected_diagnostic='Dreaming Mode may ask live questions';;
      owner-decision-checkpoints-blocks-dreaming-mode-asks-follow-up-questions) expected_diagnostic='Dreaming Mode asks follow-up questions';;
      owner-decision-checkpoints-blocks-read-only-review-may-interrupt-to-ask) expected_diagnostic='read-only review may interrupt to ask';;
      owner-decision-checkpoints-blocks-optional-knowledge-capture-requires-interactive-question) expected_diagnostic='Optional Knowledge Capture requires interactive question';;
      review-completeness-gate-blocks-incomplete-v2-verdict) expected_diagnostic='Missing review completeness gate reference in \.systems/ai/core/quality-review\.md: incomplete V2 verdict block';;
      review-completeness-gate-requires-formal-policy-matrix) expected_diagnostic='Missing review completeness gate reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: canonical V2 template field: - Policy-boundary adversarial matrix: `<completed\|not-applicable\|incomplete>`';;
      review-completeness-gate-requires-micro-producer-audit) expected_diagnostic='Missing review completeness gate reference in \.systems/ai/templates/micro-projects/micro-project\.template\.md: canonical V2 template field: - Producer-consumer field audit: `<completed\|not-applicable\|incomplete>`';;
      review-completeness-gate-requires-dreaming-decision-artifact) expected_diagnostic='Missing review completeness gate reference in \.systems/ai/templates/dreaming/dream-report\.template\.md: Dreaming full decision record';;
      dreaming-mode-requires-full-queued-decision-fields) expected_diagnostic='Dream report template missing v2 recommendation column: Decision Artifact';;
      review-completeness-gate-requires-autopilot-decision-artifact) expected_diagnostic='Missing review completeness gate reference in \.systems/ai/templates/autopilot/readiness\.template\.md: autopilot full decision record: decision-artifact:';;
      owner-decision-checkpoints-requires-autopilot-decision-artifact) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/templates/autopilot/readiness\.template\.md: autopilot queued-decision field: decision-artifact:';;
      review-completeness-gate-requires-shared-policy-helper) expected_diagnostic='Missing review completeness gate reference in \.systems/scripts/check-owner-decision-checkpoints: shared policy helper use';;
      review-completeness-gate-audits-full-qa-policy-validator) expected_diagnostic='Missing full QA policy validator from Review Completeness Gate audit';;
      review-completeness-gate-requires-review-baseline-and-freshness-inside-gate) expected_diagnostic='Missing review-template Review Completeness Gate field: - Reviewed baseline: `<HEAD/worktree/diff/artifact identifiers>`';;
      policy-boundaries-fails-missing-source) expected_diagnostic='^Policy-boundary scan failed: missing source test$';;
      policy-boundaries-blocks-repeated-unsafe-match-after-safe-quote) expected_diagnostic='Do not say `no sources needed`; no sources needed\.';;
      cross-system-yes-without-handoff-fails) expected_diagnostic='Shared-impact yes requires handoff path';;
      cross-system-pending-blocks-handoff) expected_diagnostic='Shared-impact decision pending blocks commit/handoff';;
      cross-system-handoff-blocks-raw-client-data) expected_diagnostic='Shared-impact handoff contains a raw client/credential marker';;
      cross-system-handoff-blocks-email-shaped-data) expected_diagnostic='Shared-impact handoff contains an email or credential-shaped value';;
      cross-system-handoff-requires-external-memory-namespace) expected_diagnostic='Shared-impact handoff must live under ai-workflow-workspace/external-memory/memory/';;
      end-of-task-capture-requires-koniec-pracy) expected_diagnostic='Missing end-of-task capture reference in \.systems/ai/core/end-of-task-capture\.md: trigger: Koniec pracy';;
      end-of-task-capture-blocks-acknowledge-only) expected_diagnostic='Koniec pracy may acknowledge only and ask what to do next\.';;
      validation-routing-requires-script-applicability) expected_diagnostic='Missing validation routing requirement in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: field: Workflow script applicability';;
      validation-routing-blocks-green-scripts-pass) expected_diagnostic='Green scripts equal PASS\.';;
      model-selection-requires-non-blocking-field) expected_diagnostic='Missing model guidance requirement in \.systems/ai/templates/workflow/phase-4-implementation\.template\.md: model field: Blocking: `no`';;
      model-selection-blocks-qa-bypass) expected_diagnostic='Model selection may bypass QA\.';;
      worktree-bootstrap-requires-approval) expected_diagnostic='Worktree bootstrap STOP: platform network/write approval was not recorded';;
      worktree-bootstrap-requires-strong-marker) expected_diagnostic='Worktree bootstrap STOP: missing strong AI Workflow installation marker';;
      worktree-bootstrap-rejects-symlink-marker) expected_diagnostic='Worktree bootstrap STOP: accepted marker cannot be a symlink';;
      worktree-bootstrap-stops-agents-collision) expected_diagnostic='Worktree bootstrap STOP: root AGENTS\.md already exists and requires owner-approved merge';;
      worktree-bootstrap-stops-wrong-origin) expected_diagnostic='Worktree bootstrap STOP: existing clone has wrong origin';;
      worktree-bootstrap-stops-dirty-clone) expected_diagnostic='Worktree bootstrap STOP: existing clone is dirty';;
      owner-decision-checkpoints-requires-response-trace) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/response-contract\.md: response contract field: - Decisions asked/pending: <ids\|none>';;
      response-evidence-trace-requires-owner-decision-fields) expected_diagnostic='Missing response evidence trace reference in \.systems/ai/core/response-contract\.md: owner decision trace field: - Decisions asked/pending: <ids\|none>';;
      owner-decision-checkpoints-blocks-quality-chain-with-pending-decision) expected_diagnostic='Missing owner decision checkpoint reference in \.systems/ai/core/workflow\.md: workflow decision stop before quality chaining';;
      default-quality-chaining-blocks-pending-owner-decision) expected_diagnostic='Missing default quality chaining text in \.systems/ai/core/workflow\.md: If the working phase ends with a material `Owner Decision Checkpoint` state of `awaiting-owner` or `blocked`, stop before QA/Quality chaining\.';;
      qa-evidence-positive-gate-still-requires-evidence|qa-evidence-punctuated-positive-still-requires-evidence|qa-evidence-gate-only-positive-still-requires-evidence) expected_diagnostic='missing ## Evidence section';;
      qa-evidence-rejects-conflicting-declared-results) expected_diagnostic='conflicting declared result and gate decision';;
      full-qa-verification-requires-legacy-contract-legacy-fingerprint-admission-is-terminal-for-the-exact-registered-file) expected_diagnostic='Missing full QA verification reference in \.systems/ai/core/full-qa-verification\.md: terminal legacy admission boundary';;
      full-qa-verification-requires-legacy-contract-a-v1-marker-takes-precedence-over-pre-v1-admission) expected_diagnostic='Missing full QA verification reference in \.systems/ai/core/full-qa-verification\.md: V1-first legacy admission precedence';;
      full-qa-verification-requires-legacy-contract-superseded-invalid-v1) expected_diagnostic='Missing full QA verification reference in \.systems/ai/core/full-qa-verification\.md: incomplete V1 recovery boundary';;
      full-qa-verification-requires-legacy-contract-does-not-upgrade-the-artifact) expected_diagnostic='Missing full QA verification reference in \.systems/ai/core/full-qa-verification\.md: legacy evidence is not an evidence upgrade';;
      full-qa-verification-requires-artifact-completeness-gate) expected_diagnostic='Missing full QA verification reference in \.systems/ai/templates/workflow/phase-1-architecture-qa\.template\.md: artifact completeness gate';;
      full-qa-verification-requires-current-phase5-run) expected_diagnostic='Missing full QA verification reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: current quality section: ## Current QA Run';;
      full-qa-verification-blocks-technical-only-qa) expected_diagnostic='Technical checks are enough without owner intent\.';;
      full-qa-verification-requires-forbidden-state-matrix-field) expected_diagnostic='Missing full QA verification reference in \.systems/ai/templates/workflow/phase-5-quality\.template\.md: phase 5 matrix field: Forbidden States/Rows';;
      qa-evidence-requires-artifact-completeness-for-pass) expected_diagnostic='Invalid current QA assessment: missing or incomplete Artifact QA Completeness Gate: Owner intent and governing sources reviewed';;
      qa-evidence-requires-contract-marker-for-formal-pass|qa-evidence-rejects-tampered-legacy-fingerprint|qa-evidence-rejects-unregistered-legacy-fingerprint|qa-evidence-rejects-wrong-legacy-checksum|qa-evidence-rejects-wrong-legacy-path|qa-evidence-rejects-outside-workspace-legacy) expected_diagnostic='missing V1 QA marker or registered legacy evidence fingerprint';;
      qa-evidence-rejects-artifact-pass-with-scope-mismatch) expected_diagnostic='Invalid current QA assessment: unsatisfied Artifact QA Completeness Gate: Scope and out-of-scope consistency';;
      qa-evidence-rejects-incomplete-v1-recovery) expected_diagnostic='missing ## Artifact QA Completeness Gate for formal artifact QA PASS';;
      naming-global-still-fails) expected_diagnostic='Invalid Markdown filename \(workspace-filesystem\): .*ai-workflow-workspace/projects/unrelated-project/Bad Name\.md';;
      status-consistency-selected-project-still-fails|status-consistency-global-still-fails) expected_diagnostic='ai-workflow-workspace/projects/unrelated-project/status\.md has invalid current-phase: not-a-phase';;
      workflow-fast-global-still-fails) expected_diagnostic='Invalid Markdown filename';;
      qa-evidence-requires-adaptive-matrix-for-phase-5-pass) expected_diagnostic='Invalid current QA assessment: missing current implementation quality section: Adaptive Data / Integration Verification Matrix';;
      qa-evidence-requires-phase-5-definition-of-done-validation) expected_diagnostic='Invalid current QA assessment: missing current implementation quality section: Definition Of Done Validation';;
      qa-evidence-requires-phase-5-intent--plan--spec-compliance) expected_diagnostic='Invalid current QA assessment: missing current implementation quality section: Intent / Plan / Spec Compliance';;
      qa-evidence-requires-phase-5-review-completeness-gate) expected_diagnostic='Invalid current QA assessment: missing or empty current subsection: Review Completeness Gate';;
      qa-evidence-requires-phase-5-findings) expected_diagnostic='Invalid current QA assessment: missing or empty current subsection: Findings';;
      qa-evidence-rejects-phase-5-pass-with-failed-dod) expected_diagnostic='Invalid current QA assessment: implementation PASS lacks complete current DoD validation';;
      qa-evidence-rejects-phase-5-pass-with-partial-intent-compliance) expected_diagnostic='Invalid current QA assessment: unsatisfied Intent / Plan / Spec Compliance: Compliance status';;
      qa-evidence-rejects-phase-5-pass-with-stale-completeness-gate) expected_diagnostic='Invalid current QA assessment: unsatisfied Review Completeness Gate: Closure freshness';;
      qa-evidence-rejects-phase-5-pass-with-unresolved-p1) expected_diagnostic='Invalid current QA assessment: PASS has unresolved or undocumented findings';;
      qa-evidence-rejects-phase-5-pass-with-unsatisfied-quality-gate) expected_diagnostic='Invalid current QA assessment: unsatisfied Quality Gate: 100% DoD satisfied';;
      qa-evidence-requires-complete-required-adaptive-matrix-row) expected_diagnostic='Invalid current QA assessment: incomplete current adaptive matrix row';;
      bad-phase-transition) expected_diagnostic='\.systems/ai/examples/projects/EXAMPLE/status\.md has invalid phase transition: phase-1-architecture \+ PASS -> phase-8-final-check';;
      update-blocks-dirty-template|update-blocks-dirty-example-micro-project) expected_diagnostic='STOP: system-owned files are dirty';;
      update-blocks-legacy-nested-workspace) expected_diagnostic='STOP: legacy workspace found inside AI_WORKFLOW_HOME';;
      delivery-constraints-blocks-quality-bypass) expected_diagnostic='Deadline pressure may skip QA\.';;
      distillation-state-blocks-dreaming-write) expected_diagnostic='Dreaming automatically writes memory from every undistilled state\.';;
      distillation-state-requires-state-field) expected_diagnostic='Missing distillation state reference in \.systems/ai/templates/capture/distillation-state\.template\.md: canonical State field';;
      delivery-constraints-requires-phase5-evidence) expected_diagnostic='Missing delivery constraints reference in \.systems/ai/workflow/phase-5-quality\.md: delivery block';;
      distillation-state-requires-mandatory-producer) expected_diagnostic='Missing distillation state reference in \.systems/ai/core/distillation-state\.md: mandatory producer rule';;
      dreaming-queue-requires-all-columns) expected_diagnostic='Section '\''Undistilled Work Queue'\'' missing required table column '\''Residual Risk'\'': \.systems/ai/templates/dreaming/dream-report\.template\.md';;
      workspace-freshness-remains-advisory) expected_diagnostic='Workspace freshness incorrectly acts as a hard gate';;
      contract-topology-remains-advisory) expected_diagnostic='Contract topology incorrectly acts as a hard gate';;
      validation-observability-preserves-pass-integrity) expected_diagnostic='Validation observability weakens coverage or PASS integrity';;
      skill-evaluation-remains-optional) expected_diagnostic='Skill evaluation contract contains unsafe or mandatory wording';;
      update-ff-only-failure-leaves-external-workspace) expected_diagnostic='^AI_WORKFLOW_UPSTREAM_STATE relation=diverged ';;
    esac
  fi

  should_run_smoke_test "$name" || return 0

  local capability_backup=""
  if [[ "$name" == "missing-autopilot-range-in-readiness" ]]; then
    # Pin only this deliberate fixture mutation; integrity tests never use this hook.
    capability_backup="$tmp/execution-capability-range.orig"
    cp "$tmp/.systems/ai/capabilities/execution-modes-v1.json" "$capability_backup"
    python3 - "$tmp" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
path = root / ".systems/ai/capabilities/execution-modes-v1.json"
record = json.loads(path.read_text())
name = ".systems/ai/templates/autopilot/readiness.template.md"
record["sources"][name] = hashlib.sha256((root / name).read_bytes()).hexdigest()
path.write_text(json.dumps(record, indent=2) + "\n")
PY
  fi

  if [[ "$progress" != "quiet" ]]; then
    printf 'AI_WORKFLOW_SMOKE_PROGRESS test=%s status=started\n' "$name"
  fi

  set +e
  (cd "$tmp" && "$timeout_runner" --timeout-seconds "$test_timeout_seconds" "$@") >"$output" 2>&1
  status=$?
  set -e
  if [[ -n "$capability_backup" ]]; then
    mv "$capability_backup" "$tmp/.systems/ai/capabilities/execution-modes-v1.json"
  fi
  if [[ -n "${AI_WORKFLOW_SMOKE_DIAGNOSTICS_OUTPUT:-}" ]]; then
    mkdir -p "$(dirname "$AI_WORKFLOW_SMOKE_DIAGNOSTICS_OUTPUT")"
    printf '%s\t%s\t%s\n' "$name" "$status" "$(sed -n '/[^[:space:]]/{p;q;}' "$output")" >> "$AI_WORKFLOW_SMOKE_DIAGNOSTICS_OUTPUT"
  fi
  record_smoke_timing "$name" "$started_ns" "$([[ "$status" -eq "$expected_status" ]] && echo pass || echo fail)"
  if [[ "$status" -ne "$expected_status" ]]; then
    echo "Validator smoke test returned $status instead of expected $expected_status: $name"
    cat "$output"
    exit 1
  fi
  if grep -Eq '^(Traceback \(most recent call last\):|FileNotFoundError:|PermissionError:|OSError:)' "$output"; then
    echo "Validator smoke test hit an infrastructure error instead of the intended rejection: $name"
    cat "$output"
    exit 1
  fi
  if [[ "$expected_diagnostic" == '[[:graph:]]' && -z "$expected_literal" ]]; then
    echo "Validator smoke test lacks a specific diagnostic contract: $name"
    cat "$output"
    exit 1
  fi
  if ! grep -Eq -- "$expected_diagnostic" "$output"; then
    echo "Validator smoke test lacks expected diagnostic: $name"
    cat "$output"
    exit 1
  fi
  if [[ -n "$expected_literal" ]] && ! grep -Fq -- "$expected_literal" "$output"; then
    echo "Validator smoke test lacks the intended rejected clause: $name"
    cat "$output"
    exit 1
  fi
  if [[ "$progress" == "verbose" ]]; then
    printf 'AI_WORKFLOW_SMOKE_PROGRESS test=%s status=pass duration_seconds=%s\n' "$name" "$((SECONDS - started))"
  fi
}

run_must_pass() {
  local name="$1"
  shift
  local output="$tmp/${name}.out"
  local started=$SECONDS
  local started_ns=""
  [[ -z "${AI_WORKFLOW_TIMING_OUTPUT:-}" ]] || started_ns="$(python3 "$timing_helper" now)"
  local status

  should_run_smoke_test "$name" || return 0

  if [[ "$progress" != "quiet" ]]; then
    printf 'AI_WORKFLOW_SMOKE_PROGRESS test=%s status=started\n' "$name"
  fi

  set +e
  (cd "$tmp" && "$timeout_runner" --timeout-seconds "$test_timeout_seconds" "$@") >"$output" 2>&1
  status=$?
  set -e
  record_smoke_timing "$name" "$started_ns" "$([[ "$status" -eq 0 ]] && echo pass || echo fail)"
  if [[ "$status" -ne 0 ]]; then
    echo "Validator smoke test unexpectedly failed: $name"
    cat "$output"
    exit 1
  fi
  if [[ "$progress" == "verbose" ]]; then
    printf 'AI_WORKFLOW_SMOKE_PROGRESS test=%s status=pass duration_seconds=%s\n' "$name" "$((SECONDS - started))"
  fi
}

smoke_test_group() {
  local name="$1"
  case "$name" in
    *skill*|*context*|*quick-validate*) echo skills ;;
    *quality*|*qa-*|*full-qa*|*global-review*|*intent-plan*|*implementation-slicing*|*plan-quality*|*validation-routing*|*default-quality*|*review-completeness*) echo quality ;;
    *policy*|*prompt-composition*|*contract-compliance*|*request-batch*|*owner-decision*|*response-evidence*|*end-of-task*|*knowledge-capture*|*cross-system*|*instruction-refresh*|*phase-skill*|*idea-validation*|*delivery-constraints*|*distillation-state*) echo policy ;;
    *init-workspace*|*update-workspace*|*resolver*|*branch-policy*|*bootstrap*|*naming*|*status*|*required-artifacts*) echo workspace ;;
    *) echo core ;;
  esac
}

record_smoke_timing() {
  local name="$1"
  local started_ns="$2"
  local result="$3"
  local output_path="${AI_WORKFLOW_TIMING_OUTPUT:-}"
  [[ -n "$output_path" ]] || return 0
  python3 "$timing_helper" record "$output_path" "$smoke_timing_run_id" "$name" "${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}" "$result" "${AI_WORKFLOW_SMOKE_TIMING_PROFILE:-smoke-$smoke_group}" child smoke-suite-wall "$started_ns"
}
run_policy_boundary_matrix() {
  local id="$1"
  local file="$2"
  local check="$3"
  local safe_case="$4"
  local direct_unsafe_case="$5"
  local compound_unsafe_case="$6"
  local semicolon_unsafe_case="$7"
  local target="$tmp/$file"
  local period_unsafe_case="${compound_unsafe_case/, but /. }"
  local colon_unsafe_case="${compound_unsafe_case/, but /: }"
  local unless_unsafe_case="${compound_unsafe_case/, but / unless }"
  local yet_unsafe_case="${compound_unsafe_case/, but / yet }"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$safe_case" >> "$target"
  run_must_pass "policy-boundary-${id}-allows-safe-prohibition" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$direct_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-direct-unsafe" --expect-literal "$direct_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$compound_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-but-unsafe-exception" --expect-literal "$compound_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$period_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-period-unsafe-exception" --expect-literal "$period_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$colon_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-colon-unsafe-exception" --expect-literal "$colon_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$unless_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-unless-unsafe-exception" --expect-literal "$unless_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$yet_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-yet-unsafe-exception" --expect-literal "$yet_unsafe_case" "$check"
  mv "$target.bak" "$target"

  cp "$target" "$target.bak"
  printf '\n%s\n' "$semicolon_unsafe_case" >> "$target"
  run_must_fail "policy-boundary-${id}-blocks-safe-semicolon-unsafe-exception" --expect-literal "$semicolon_unsafe_case" "$check"
  mv "$target.bak" "$target"
}


should_run_smoke_test() {
  local name="$1"
  # These four nested negative-helper probes are checked by their enclosing
  # infrastructure assertions, not independently owned suite cases.
  case "$name" in
    smoke-helper-rejects-unexpected-timeout|smoke-helper-rejects-missing-source|smoke-helper-rejects-wrong-error-code|smoke-helper-rejects-wrong-diagnostic) return 0 ;;
  esac
  if [[ -n "${AI_WORKFLOW_SMOKE_LEDGER:-}" ]]; then
    printf '%s\t%s\n' "$name" "${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}" >> "$AI_WORKFLOW_SMOKE_LEDGER"
  fi
  return 0
}
