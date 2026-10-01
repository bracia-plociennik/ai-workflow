#!/usr/bin/env bash
set -euo pipefail

tmp="$(mktemp -d "${TMPDIR:-/tmp}/ai-workflow-validator-smoke.XXXXXX")"
smoke_group="${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}"
progress="summary"
test_timeout_seconds="180"
smoke_started_at=$SECONDS
smoke_completion_emitted=0
smoke_suite_completed=0
smoke_final_status=0

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --group)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --group"; exit 1; }
      smoke_group="$2"
      shift 2
      ;;
    --progress)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --progress"; exit 1; }
      progress="$2"
      shift 2
      ;;
    --test-timeout-seconds)
      [[ "$#" -ge 2 ]] || { echo "Missing value for --test-timeout-seconds"; exit 1; }
      test_timeout_seconds="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: check-validator-smoke-tests [--group all|core|policy|quality|skills|workspace] [--progress quiet|summary|verbose] [--test-timeout-seconds seconds]"
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
done

case "$smoke_group" in
  all|core|policy|quality|skills|workspace) ;;
  *) echo "Unknown smoke group: $smoke_group"; exit 1 ;;
esac

case "$progress" in
  quiet|summary|verbose) ;;
  *) echo "Unknown progress mode: $progress"; exit 1 ;;
esac

if ! [[ "$test_timeout_seconds" =~ ^[0-9]+([.][0-9]+)?$ ]] || [[ "$test_timeout_seconds" == "0" || "$test_timeout_seconds" == "0.0" ]]; then
  echo "--test-timeout-seconds must be greater than zero"
  exit 1
fi

# Copied fixtures own their roots. Do not inherit the dispatcher's private runtime
# or forced repository mode; individual tests set their explicit environment.
unset AI_WORKFLOW_MODE AI_WORKFLOW_MODE_RESOLVED AI_WORKFLOW_HOME AI_WORKFLOW_WORKSPACE_HOME TARGET_REPO_ROOT

timeout_runner="$(pwd -P)/.systems/scripts/run-with-timeout"
timing_helper="$(pwd -P)/.systems/scripts/lib/validation-timing.py"
smoke_timing_start=""
smoke_timing_run_id="${AI_WORKFLOW_TIMING_RUN_ID:-$(date -u +%Y%m%dT%H%M%S)-$$}"
if [[ -n "${AI_WORKFLOW_TIMING_OUTPUT:-}" && "${AI_WORKFLOW_SMOKE_CHILD:-0}" != 1 ]]; then
  if [[ ! -e "$AI_WORKFLOW_TIMING_OUTPUT" ]]; then
    python3 "$timing_helper" init "$AI_WORKFLOW_TIMING_OUTPUT"
  fi
  smoke_timing_start="$(python3 "$timing_helper" now)"
fi

finish_smoke() {
  local status="${1:-$?}"
  local result="fail"
  if [[ "$status" -eq 0 ]]; then result="pass"; fi
  if [[ "$status" -eq 124 ]]; then result="timeout"; fi
  if [[ "$status" -eq 130 || "$status" -eq 143 ]]; then result="interrupted"; fi
  if [[ -n "${AI_WORKFLOW_TIMING_OUTPUT:-}" && -n "$smoke_timing_start" ]]; then
    if ! python3 "$timing_helper" record "$AI_WORKFLOW_TIMING_OUTPUT" "$smoke_timing_run_id" smoke-suite-wall smoke "$result" "smoke-$smoke_group" wall validation-wall "$smoke_timing_start"; then
      echo "Smoke timing wall record failed" >&2
      status=1
      result="fail"
    fi
  fi
  smoke_final_status="$status"
  if [[ "$smoke_completion_emitted" -eq 0 ]]; then
    smoke_completion_emitted=1
    printf 'AI_WORKFLOW_SMOKE_GROUP_COMPLETE group=%s result=%s exit_code=%s duration_seconds=%s\n' \
      "$smoke_group" "$result" "$status" "$((SECONDS - smoke_started_at))"
  fi
}

cleanup() {
  rm -rf "$tmp"
}
on_smoke_exit() {
  local status="$1"
  if [[ "$status" -eq 0 && "$smoke_suite_completed" -ne 1 ]]; then
    echo "Smoke suite ended before the final completion point" >&2
    status=1
  fi
  finish_smoke "$status"
  cleanup
  trap - EXIT
  exit "$smoke_final_status"
}
trap 'on_smoke_exit "$?"' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

printf 'AI_WORKFLOW_SMOKE_GROUP_START group=%s progress=%s\n' "$smoke_group" "$progress"

python3 .systems/scripts/lib/smoke-fixture.py --repo "$(pwd -P)" --output "$tmp"

source "$(pwd -P)/.systems/scripts/smoke/common.sh"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md" "$tmp/example-status.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/tasks.md" "$tmp/example-tasks.orig"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/example-phase5-quality.orig"
# BEGIN FROZEN region-2828-3215
run_must_pass "global-quality-review-valid" .systems/scripts/check-global-quality-review-stance

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/Cross-contract consistency/Cross-policy note/g' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-requires-cross-contract-consistency" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/- Negative-space \/ adversarial review: `<completed\|not-applicable\|incomplete>`\n//' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "global-quality-review-requires-formal-negative-space-field" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\ngreen validators are sufficient for PASS\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-green-validator-verdict" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\npost-fix review may inspect only fixed lines\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-fixed-lines-only-review" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nclosure may remain current without full re-review\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-current-closure-without-rereview" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nNo findings found may be declared with stale closure\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-no-findings-with-stale-closure" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/command-routing.md" "$tmp/.systems/ai/core/command-routing.md.bak"
perl -0pi -e 's/find blockers/find bx/g; s/Find blockers/Find bx/g' "$tmp/.systems/ai/core/command-routing.md"
run_must_fail "global-quality-review-requires-find-blockers-routing" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/command-routing.md.bak" "$tmp/.systems/ai/core/command-routing.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nadvisory review may mark PASS\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-advisory-pass-wording" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nadvisory review may produce PASS\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-advisory-produce-pass-wording" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nfinal review runs phase-8-final-check\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-final-review-final-check-wording" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nfinal review starts phase-8-final-check\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-blocks-final-review-starts-final-check-wording" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/- formal gate eligibility\.//' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "global-quality-review-requires-formal-gate-eligibility-field" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/workflow/phase-5-quality.md" "$tmp/.systems/ai/workflow/phase-5-quality.md.bak"
perl -0pi -e 's/PASS/OK/g; s/FAIL/BLOCKED/g' "$tmp/.systems/ai/workflow/phase-5-quality.md"
run_must_fail "global-quality-review-preserves-formal-phase5-pass-fail" .systems/scripts/check-global-quality-review-stance
mv "$tmp/.systems/ai/workflow/phase-5-quality.md.bak" "$tmp/.systems/ai/workflow/phase-5-quality.md"

run_must_pass "intent-plan-spec-compliance-valid" .systems/scripts/check-intent-plan-spec-compliance-review

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/Intent \/ Plan \/ Spec Compliance/Conceptual Compliance/g' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "intent-plan-spec-compliance-requires-global-review-lens" .systems/scripts/check-intent-plan-spec-compliance-review
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/workflow/phase-5-quality.md" "$tmp/.systems/ai/workflow/phase-5-quality.md.bak"
perl -0pi -e 's/Intent \/ Plan \/ Spec Compliance/Conceptual Compliance/g' "$tmp/.systems/ai/workflow/phase-5-quality.md"
run_must_fail "intent-plan-spec-compliance-requires-phase5-lens" .systems/scripts/check-intent-plan-spec-compliance-review
mv "$tmp/.systems/ai/workflow/phase-5-quality.md.bak" "$tmp/.systems/ai/workflow/phase-5-quality.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/- Compliance status: `<aligned\|partial\|mismatch\|unknown>`\n//' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "intent-plan-spec-compliance-requires-template-status" .systems/scripts/check-intent-plan-spec-compliance-review
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/workflow/phase-5-quality.md" "$tmp/.systems/ai/workflow/phase-5-quality.md.bak"
printf '\nQA may pass without checking acceptance criteria\n' >> "$tmp/.systems/ai/workflow/phase-5-quality.md"
run_must_fail "intent-plan-spec-compliance-blocks-qa-pass-without-ac" .systems/scripts/check-intent-plan-spec-compliance-review
mv "$tmp/.systems/ai/workflow/phase-5-quality.md.bak" "$tmp/.systems/ai/workflow/phase-5-quality.md"

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
printf '\nscope creep is acceptable if tests pass\n' >> "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "intent-plan-spec-compliance-blocks-scope-creep-tests-pass" .systems/scripts/check-intent-plan-spec-compliance-review
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

run_must_pass "implementation-slicing-valid" .systems/scripts/check-implementation-slicing

assert_local_failure_smoke_error() {
  local name="$1"
  local expected="$2"
  if ! rg -qF -- "$expected" "$tmp/$name.out"; then
    echo "Implementation slicing smoke test failed for the wrong reason: $name"
    cat "$tmp/$name.out"
    exit 1
  fi
}

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/## Pre-Quality Local Failure Route/## Local Failure Note/' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-requires-core-local-failure-route" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-requires-core-local-failure-route" "Missing pre-quality local failure route"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/workflow/phase-4-implementation.md" "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak"
perl -0pi -e 's/## Pre-Quality Local Failure Route/## Local Failure Note/' "$tmp/.systems/ai/workflow/phase-4-implementation.md"
run_must_fail "implementation-slicing-requires-phase4-local-failure-route" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-requires-phase4-local-failure-route" "Missing pre-quality local failure route"
mv "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak" "$tmp/.systems/ai/workflow/phase-4-implementation.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/rerun the failed check/consider the failed check/' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-requires-failed-check-retest" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-requires-failed-check-retest" "failed-check retest"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nDo not assert that a failed local check may be ignored.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_pass "implementation-slicing-safe-local-failure-prohibition" .systems/scripts/check-implementation-slicing
printf 'Do not assert that a failed local check may be ignored, but a failed local check may be ignored.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-compound-ignore-exception" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-compound-ignore-exception" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nA failed local check may be ignored.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-direct-ignore" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-direct-ignore" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nRetry may bypass permissions.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-permission-bypass" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-permission-bypass" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nProtected tests may be weakened.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-protected-test-weakening" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-protected-test-weakening" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nPassing tests are formal PASS.\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-green-test-as-formal-pass" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-green-test-as-formal-pass" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/workflow/phase-4-implementation.md" "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak"
printf '\nPhase 4 may go directly to phase-5-fix-loop.\n' >> "$tmp/.systems/ai/workflow/phase-4-implementation.md"
run_must_fail "implementation-slicing-rejects-direct-formal-fix-loop" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-direct-formal-fix-loop" "Unsafe pre-quality local failure wording found"
mv "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak" "$tmp/.systems/ai/workflow/phase-4-implementation.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
rm "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-missing-local-failure-source" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-missing-local-failure-source" "Missing implementation slicing artifact"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

run_must_pass "implementation-slicing-in-scope-correction-and-legitimate-stop" .systems/scripts/check-implementation-slicing

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/(## Pre-Quality Local Failure Route\n)/$1\nDo not rerun the failed check without a safe environment.\n/' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_pass "implementation-slicing-allows-conditional-retest-safety" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/(## Pre-Quality Local Failure Route\n)/$1\nDo not rerun the failed check.\n/' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-forbidden-retest" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-forbidden-retest" "failed-check retest forbidden"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/workflow/phase-4-implementation.md" "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak"
perl -0pi -e 's/(## Pre-Quality Local Failure Route\n)/$1\nInspect the failure, but do not rerun the failed check.\n/' "$tmp/.systems/ai/workflow/phase-4-implementation.md"
run_must_fail "implementation-slicing-rejects-compound-forbidden-retest" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-compound-forbidden-retest" "failed-check retest forbidden"
mv "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak" "$tmp/.systems/ai/workflow/phase-4-implementation.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/(## Pre-Quality Local Failure Route\n)/$1\nNever inspect the failure.\n/' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-rejects-forbidden-diagnosis" .systems/scripts/check-implementation-slicing
assert_local_failure_smoke_error "implementation-slicing-rejects-forbidden-diagnosis" "failure diagnosis forbidden"
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/Implementation Slice Plan/Implementation Steps/g' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-requires-core-contract" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/workflow/phase-4-implementation.md" "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak"
perl -0pi -e 's/Implementation Slice Plan/Implementation Steps/g' "$tmp/.systems/ai/workflow/phase-4-implementation.md"
run_must_fail "implementation-slicing-requires-phase4-slice-plan" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/workflow/phase-4-implementation.md.bak" "$tmp/.systems/ai/workflow/phase-4-implementation.md"

cp "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak"
perl -0pi -e 's/## Slice Execution Evidence/## Execution Evidence/g' "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"
run_must_fail "implementation-slicing-requires-template-execution-evidence" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nslice plan may bypass QA\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-blocks-bypass-qa-wording" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/DoD source/Done target/g' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-requires-dod-source" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
perl -0pi -e 's/Mandatory Quality Closure/Quality Note/g' "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-requires-quality-closure" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nimplementation PASS without review\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-blocks-pass-without-review" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nPASS before findings review\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-blocks-pass-before-findings-review" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\npost-fix review may inspect only fixed lines\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-blocks-fixed-lines-only-post-fix-review" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/implementation-slicing.md" "$tmp/.systems/ai/core/implementation-slicing.md.bak"
printf '\nautomated checks are sufficient for PASS\n' >> "$tmp/.systems/ai/core/implementation-slicing.md"
run_must_fail "implementation-slicing-blocks-automated-only-pass" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/implementation-slicing.md.bak" "$tmp/.systems/ai/core/implementation-slicing.md"

cp "$tmp/.systems/ai/core/operating-model.md" "$tmp/.systems/ai/core/operating-model.md.bak"
perl -0pi -e 's/Implementation Slice Plan/Implementation Steps/g' "$tmp/.systems/ai/core/operating-model.md"
run_must_fail "implementation-slicing-requires-micro-work-routing" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/core/operating-model.md.bak" "$tmp/.systems/ai/core/operating-model.md"

cp "$tmp/.systems/ai/templates/projects/micro-task.template.md" "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak"
perl -0pi -e 's/## Definition of Done/## Done/g' "$tmp/.systems/ai/templates/projects/micro-task.template.md"
run_must_fail "implementation-slicing-requires-micro-task-dod" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/templates/projects/micro-task.template.md.bak" "$tmp/.systems/ai/templates/projects/micro-task.template.md"

cp "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak"
perl -0pi -e 's/## Definition of Done/## Done/g' "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"
run_must_fail "implementation-slicing-requires-micro-project-dod" .systems/scripts/check-implementation-slicing
mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"

run_must_pass "plan-quality-contract-valid" .systems/scripts/check-plan-quality-contract

cp "$tmp/.systems/ai/core/plan-quality-contract.md" "$tmp/.systems/ai/core/plan-quality-contract.md.bak"
perl -0pi -e 's/## Plan Quality Contract/## Plan Readiness/g' "$tmp/.systems/ai/core/plan-quality-contract.md"
run_must_fail "plan-quality-contract-requires-core-contract" .systems/scripts/check-plan-quality-contract
mv "$tmp/.systems/ai/core/plan-quality-contract.md.bak" "$tmp/.systems/ai/core/plan-quality-contract.md"

cp "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md" "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md.bak"
perl -0pi -e 's/Implementation Quality Closure route:/Implementation Closure route:/' "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md"
run_must_fail "plan-quality-contract-requires-implementation-quality-route" .systems/scripts/check-plan-quality-contract
mv "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-3-specification.template.md"

cp "$tmp/.systems/ai/core/command-routing.md" "$tmp/.systems/ai/core/command-routing.md.bak"
perl -0pi -e 's/phase-3-spec-qa/phase-3-artifact-review/g' "$tmp/.systems/ai/core/command-routing.md"
run_must_fail "plan-quality-contract-requires-plan-artifact-qa-route" .systems/scripts/check-plan-quality-contract
mv "$tmp/.systems/ai/core/command-routing.md.bak" "$tmp/.systems/ai/core/command-routing.md"

cp "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/plan-quality-read-only.md"
perl -0pi -e 's/<implementation-capable\|read-only>/read-only/; s/<owner prompt\/context\|micro-project artifact\|accepted plan\|other>/accepted owner read-only request/; s/<testable done conditions>/analysis is delivered to the owner/; s/<global-quality-review-stance\|not-applicable>/not-applicable/g; s/<before implementation\|not-applicable with reason>/not-applicable because no implementation writes/; s/<automated checks\|manual checks\|edge\/regression review\|adaptive data\/integration matrix or not-applicable with reason>/manual artifact review only/; s/<criteria>/analysis has the requested evidence/; s/<route>/handoff/; s/<reason\|none>/read-only analysis has no implementation writes/' "$tmp/plan-quality-read-only.md"
run_must_pass "plan-quality-contract-allows-justified-read-only-plan" .systems/scripts/check-plan-quality-contract --artifact "$tmp/plan-quality-read-only.md"

cp "$tmp/plan-quality-read-only.md" "$tmp/plan-quality-read-only.md.bak"
perl -0pi -e 's/- Plan classification: `read-only`/- Plan classification: `implementation-capable`/' "$tmp/plan-quality-read-only.md"
run_must_fail "plan-quality-contract-blocks-implementation-plan-without-artifact-qa" .systems/scripts/check-plan-quality-contract --artifact "$tmp/plan-quality-read-only.md"
mv "$tmp/plan-quality-read-only.md.bak" "$tmp/plan-quality-read-only.md"

cp "$tmp/plan-quality-read-only.md" "$tmp/plan-quality-read-only.md.bak"
perl -0pi -e 's/- DoD source: `accepted owner read-only request`/- DoD source:/' "$tmp/plan-quality-read-only.md"
run_must_fail "plan-quality-contract-requires-concrete-dod-source" .systems/scripts/check-plan-quality-contract --artifact "$tmp/plan-quality-read-only.md"
mv "$tmp/plan-quality-read-only.md.bak" "$tmp/plan-quality-read-only.md"

perl -0pi -e 's/- Not-applicable reason: `read-only analysis has no implementation writes`/- Not-applicable reason:/' "$tmp/plan-quality-read-only.md"
run_must_fail "plan-quality-contract-requires-read-only-not-applicable-reason" .systems/scripts/check-plan-quality-contract --artifact "$tmp/plan-quality-read-only.md"

cp "$tmp/.systems/ai/core/plan-quality-contract.md" "$tmp/.systems/ai/core/plan-quality-contract.md.bak"
printf '\nPlan Quality Contract may bypass QA.\n' >> "$tmp/.systems/ai/core/plan-quality-contract.md"
run_must_fail "plan-quality-contract-blocks-quality-bypass-wording" .systems/scripts/check-plan-quality-contract
mv "$tmp/.systems/ai/core/plan-quality-contract.md.bak" "$tmp/.systems/ai/core/plan-quality-contract.md"

run_policy_boundary_matrix \
  "plan-quality-contract" \
  ".systems/ai/core/plan-quality-contract.md" \
  .systems/scripts/check-plan-quality-contract \
  "Implementation-capable plans must not use not-applicable quality closure." \
  "Implementation-capable plans may use not-applicable quality closure." \
  "Implementation-capable plans must not use not-applicable quality closure, but implementation-capable plans may use not-applicable quality closure." \
  "Implementation-capable plans must not use not-applicable quality closure; implementation-capable plans may use not-applicable quality closure."

run_must_pass "validation-profiles-valid" .systems/scripts/check-validation-profiles
run_must_pass "validation-profile-fast-explain" .systems/scripts/validate-workflow --profile fast --explain
run_must_pass "validation-profile-scoped-check" .systems/scripts/validate-workflow --profile scoped --checks check-validation-profiles --explain
cp "$tmp/.systems/ai/core/validation-profiles.md" "$tmp/lv003-profile-policy.backup"
printf '\nScoped coverage complete must not grant PASS automatically.\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_pass "validation-scope-safe-coverage-prohibition" .systems/scripts/check-validation-profiles
cp "$tmp/lv003-profile-policy.backup" "$tmp/.systems/ai/core/validation-profiles.md"
printf '\nScoped coverage complete grants PASS automatically.\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-scope-rejects-coverage-pass" --expect-literal 'grants PASS automatically' .systems/scripts/check-validation-profiles
cp "$tmp/lv003-profile-policy.backup" "$tmp/.systems/ai/core/validation-profiles.md"
printf '\nScoped coverage complete must not grant PASS automatically, but Scoped coverage complete grants PASS automatically.\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-scope-rejects-compound-coverage-pass" --expect-literal 'grants PASS automatically' .systems/scripts/check-validation-profiles
mv "$tmp/lv003-profile-policy.backup" "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-profile-scoped-requires-checks" .systems/scripts/validate-workflow --profile scoped

cp "$tmp/.systems/scripts/validate-workflow" "$tmp/.systems/scripts/validate-workflow.bak"
perl -0pi -e 's/profile="standard"/profile="full"/' "$tmp/.systems/scripts/validate-workflow"
run_must_fail "validation-profiles-require-standard-default" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/scripts/validate-workflow.bak" "$tmp/.systems/scripts/validate-workflow"

cp "$tmp/.github/workflows/ai-workflow-validate.yml" "$tmp/.github/workflows/ai-workflow-validate.yml.bak"
perl -0pi -e 's/validate-workflow --profile full/validate-workflow/' "$tmp/.github/workflows/ai-workflow-validate.yml"
run_must_fail "validation-profiles-require-ci-explicit-full" .systems/scripts/check-validation-profiles
mv "$tmp/.github/workflows/ai-workflow-validate.yml.bak" "$tmp/.github/workflows/ai-workflow-validate.yml"

cp "$tmp/AGENTS.md" "$tmp/AGENTS.md.bak"
perl -0pi -e 's/validate-workflow --profile full/validate-workflow/g' "$tmp/AGENTS.md"
run_must_fail "validation-profiles-require-agents-final-full" .systems/scripts/check-validation-profiles
mv "$tmp/AGENTS.md.bak" "$tmp/AGENTS.md"

cp "$tmp/.systems/ai/core/commands.md" "$tmp/.systems/ai/core/commands.md.bak"
perl -0pi -e 's/validate-workflow --profile full/validate-workflow/g' "$tmp/.systems/ai/core/commands.md"
run_must_fail "validation-profiles-require-commands-final-full" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/ai/core/commands.md.bak" "$tmp/.systems/ai/core/commands.md"

cp "$tmp/README.md" "$tmp/README.md.bak"
perl -0pi -e 's/validate-workflow --profile full/validate-workflow/g' "$tmp/README.md"
run_must_fail "validation-profiles-require-readme-reuse-full" .systems/scripts/check-validation-profiles
mv "$tmp/README.md.bak" "$tmp/README.md"

cp "$tmp/.systems/scripts/validate-workflow" "$tmp/.systems/scripts/validate-workflow.bak"
perl -0pi -e 's/check-validator-smoke-tests/check-validator-light-tests/g' "$tmp/.systems/scripts/validate-workflow"
run_must_fail "validation-profiles-require-full-smoke-tests" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/scripts/validate-workflow.bak" "$tmp/.systems/scripts/validate-workflow"

cp "$tmp/.systems/ai/core/validation-profiles.md" "$tmp/.systems/ai/core/validation-profiles.md.bak"
printf '\nfast is enough before commit\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-profiles-block-fast-enough-before-commit" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/ai/core/validation-profiles.md.bak" "$tmp/.systems/ai/core/validation-profiles.md"

cp "$tmp/.systems/ai/core/validation-profiles.md" "$tmp/.systems/ai/core/validation-profiles.md.bak"
printf '\nstandard may replace full for workflow contracts\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-profiles-block-standard-replaces-full" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/ai/core/validation-profiles.md.bak" "$tmp/.systems/ai/core/validation-profiles.md"

cp "$tmp/.systems/ai/core/validation-profiles.md" "$tmp/.systems/ai/core/validation-profiles.md.bak"
printf '\nskip smoke tests and mark PASS\n' >> "$tmp/.systems/ai/core/validation-profiles.md"
run_must_fail "validation-profiles-block-skip-smoke-pass" .systems/scripts/check-validation-profiles
mv "$tmp/.systems/ai/core/validation-profiles.md.bak" "$tmp/.systems/ai/core/validation-profiles.md"

run_must_pass "request-batch-triage-valid" .systems/scripts/check-request-batch-triage

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/ \| routing \|/ | /g; s/ routing, / /g; s/`routing`, //' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-requires-routing-field" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/ \| risk \|/ | /g; s/ risk, / /g; s/`risk`, //' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-requires-risk-field" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/\| new feature idea \| standalone-new-feature \| product feature \| unknown \| new-project \| unresolved \| none \| idea validation decision \| Needs project workspace and formal idea validation\. \|/\| new feature idea \| standalone-new-feature \| product feature \| unknown \| new-project \| unresolved \| idea validation decision \| Needs project workspace and formal idea validation. \|/' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-requires-nine-column-matrix" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

cp "$tmp/.systems/ai/core/request-batch-triage.md" "$tmp/.systems/ai/core/request-batch-triage.md.bak"
perl -0pi -e 's/active project and another repo-level item/active project plus repo item/g; s/workflow-improvements/workflow_updates/g; s/standalone-new-feature/standalone_feature/g; s/standalone-change-request/standalone_change/g' "$tmp/.systems/ai/core/request-batch-triage.md"
run_must_fail "request-batch-triage-requires-mixed-list-split" .systems/scripts/check-request-batch-triage
mv "$tmp/.systems/ai/core/request-batch-triage.md.bak" "$tmp/.systems/ai/core/request-batch-triage.md"

# END FROZEN region-2828-3215

# BEGIN FROZEN region-3632-3827

cp "$tmp/.systems/ai/core/quality-review.md" "$tmp/.systems/ai/core/quality-review.md.bak"
perl -0pi -e 's/an applicable policy-boundary adversarial matrix or producer-consumer field audit is incomplete/an applicable matrix is incomplete/' "$tmp/.systems/ai/core/quality-review.md"
run_must_fail "review-completeness-gate-blocks-incomplete-v2-verdict" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/ai/core/quality-review.md.bak" "$tmp/.systems/ai/core/quality-review.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/- Policy-boundary adversarial matrix: `<completed\|not-applicable\|incomplete>`\n//' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "review-completeness-gate-requires-formal-policy-matrix" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak"
perl -0pi -e 's/- Producer-consumer field audit: `<completed\|not-applicable\|incomplete>`\n//' "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"
run_must_fail "review-completeness-gate-requires-micro-producer-audit" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md.bak" "$tmp/.systems/ai/templates/micro-projects/micro-project.template.md"

cp "$tmp/.systems/ai/templates/dreaming/dream-report.template.md" "$tmp/.systems/ai/templates/dreaming/dream-report.template.md.bak"
perl -0pi -e 's/ \| Decision Artifact//g' "$tmp/.systems/ai/templates/dreaming/dream-report.template.md"
run_must_fail "review-completeness-gate-requires-dreaming-decision-artifact" .systems/scripts/check-review-completeness-gate
run_must_fail "dreaming-mode-requires-full-queued-decision-fields" .systems/scripts/check-dreaming-mode
mv "$tmp/.systems/ai/templates/dreaming/dream-report.template.md.bak" "$tmp/.systems/ai/templates/dreaming/dream-report.template.md"

cp "$tmp/.systems/ai/templates/autopilot/readiness.template.md" "$tmp/.systems/ai/templates/autopilot/readiness.template.md.bak"
perl -0pi -e 's/    decision-artifact: null\n//' "$tmp/.systems/ai/templates/autopilot/readiness.template.md"
run_must_fail "review-completeness-gate-requires-autopilot-decision-artifact" .systems/scripts/check-review-completeness-gate
run_must_fail "owner-decision-checkpoints-requires-autopilot-decision-artifact" .systems/scripts/check-owner-decision-checkpoints
mv "$tmp/.systems/ai/templates/autopilot/readiness.template.md.bak" "$tmp/.systems/ai/templates/autopilot/readiness.template.md"

cp "$tmp/.systems/scripts/check-owner-decision-checkpoints" "$tmp/.systems/scripts/check-owner-decision-checkpoints.bak"
perl -0pi -e 's/policy_reject_unsafe_pattern/policy_reject_removed/g' "$tmp/.systems/scripts/check-owner-decision-checkpoints"
run_must_fail "review-completeness-gate-requires-shared-policy-helper" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/scripts/check-owner-decision-checkpoints.bak" "$tmp/.systems/scripts/check-owner-decision-checkpoints"

cp "$tmp/.systems/scripts/check-review-completeness-gate" "$tmp/.systems/scripts/check-review-completeness-gate.bak"
perl -0pi -e 's/\n  \.systems\/scripts\/check-full-qa-verification//' "$tmp/.systems/scripts/check-review-completeness-gate"
run_must_fail "review-completeness-gate-audits-full-qa-policy-validator" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/scripts/check-review-completeness-gate.bak" "$tmp/.systems/scripts/check-review-completeness-gate"

cp "$tmp/.systems/ai/templates/reviews/review.template.md" "$tmp/.systems/ai/templates/reviews/review.template.md.bak"
perl -0pi -e 's/- Reviewed baseline: `<HEAD\/worktree\/diff\/artifact identifiers>`\n- Closure freshness: `<current\|stale>`\n\n## Adaptive Data \/ Integration Verification Matrix/## Adaptive Data \/ Integration Verification Matrix/' "$tmp/.systems/ai/templates/reviews/review.template.md"
printf '\n- Reviewed baseline: `<HEAD/worktree/diff/artifact identifiers>`\n- Closure freshness: `<current|stale>`\n' >> "$tmp/.systems/ai/templates/reviews/review.template.md"
run_must_fail "review-completeness-gate-requires-review-baseline-and-freshness-inside-gate" .systems/scripts/check-review-completeness-gate
mv "$tmp/.systems/ai/templates/reviews/review.template.md.bak" "$tmp/.systems/ai/templates/reviews/review.template.md"

run_must_fail "policy-boundaries-fails-missing-source" bash -lc '
  source .systems/scripts/lib/policy-boundaries.sh
  fail=0
  policy_reject_unsafe_pattern "unsafe policy wording" "missing source test" /definitely/missing/policy-source.md
  exit "$fail"
'

cp "$tmp/.systems/ai/core/response-contract.md" "$tmp/.systems/ai/core/response-contract.md.bak"
printf '\nDo not say `no sources needed`; no sources needed.\n' >> "$tmp/.systems/ai/core/response-contract.md"
run_must_fail "policy-boundaries-blocks-repeated-unsafe-match-after-safe-quote" .systems/scripts/check-response-evidence-trace
mv "$tmp/.systems/ai/core/response-contract.md.bak" "$tmp/.systems/ai/core/response-contract.md"

run_policy_boundary_matrix \
  "response-evidence" \
  ".systems/ai/core/response-contract.md" \
  .systems/scripts/check-response-evidence-trace \
  "Execution Trace must not be omitted for substantive responses." \
  "Execution Trace may be omitted for substantive responses." \
  "Execution Trace must not be omitted by default, but Execution Trace may be omitted for substantive responses." \
  "Execution Trace must not be omitted by default; Execution Trace may be omitted for substantive responses."
run_policy_boundary_matrix \
  "default-quality" \
  ".systems/ai/core/quality-review.md" \
  .systems/scripts/check-default-quality-closure \
  "bez QA must not mark PASS." \
  "bez QA may mark PASS." \
  "bez QA must not mark PASS, but bez QA may mark PASS." \
  "bez QA must not mark PASS; bez QA may mark PASS."
run_policy_boundary_matrix \
  "instruction-refresh" \
  ".systems/ai/core/instruction-adherence-refresh.md" \
  .systems/scripts/check-instruction-adherence-refresh \
  "Instruction Adherence Refresh must not grant write permission." \
  "Instruction Adherence Refresh allows write permission." \
  "Instruction Adherence Refresh must not grant write permission, but Instruction Adherence Refresh allows write permission." \
  "Instruction Adherence Refresh must not grant write permission; Instruction Adherence Refresh allows write permission."
run_policy_boundary_matrix \
  "phase-skill" \
  ".systems/ai/core/operating-model.md" \
  .systems/scripts/check-phase-skill-discovery \
  "A skill must not approve implementation." \
  "A skill may approve implementation." \
  "A skill must not approve implementation, but a skill may approve implementation." \
  "A skill must not approve implementation; a skill may approve implementation."
run_policy_boundary_matrix \
  "batch-triage" \
  ".systems/ai/core/request-batch-triage.md" \
  .systems/scripts/check-request-batch-triage \
  "Batch triage must not write files." \
  "Batch triage may write files." \
  "Batch triage must not write files, but batch triage may write files." \
  "Batch triage must not write files; batch triage may write files."
run_policy_boundary_matrix \
  "intent-review" \
  ".systems/ai/core/quality-review.md" \
  .systems/scripts/check-intent-plan-spec-compliance-review \
  "Technical checks are not enough." \
  "Technical checks are enough." \
  "Technical checks are not enough, but technical checks are enough." \
  "Technical checks are not enough; technical checks are enough."
run_policy_boundary_matrix \
  "global-review" \
  ".systems/ai/core/quality-review.md" \
  .systems/scripts/check-global-quality-review-stance \
  "Advisory review must not mark formal PASS." \
  "Advisory review may mark formal PASS." \
  "Advisory review must not mark formal PASS, but advisory review may mark formal PASS." \
  "Advisory review must not mark formal PASS; advisory review may mark formal PASS."
run_policy_boundary_matrix \
  "validation-profiles" \
  ".systems/ai/core/validation-profiles.md" \
  .systems/scripts/check-validation-profiles \
  "Standard must not replace full." \
  "Standard may replace full." \
  "Standard must not replace full, but standard may replace full." \
  "Standard must not replace full; standard may replace full."
run_policy_boundary_matrix \
  "implementation-slicing" \
  ".systems/ai/core/implementation-slicing.md" \
  .systems/scripts/check-implementation-slicing \
  "Slicing must not bypass QA." \
  "Slicing may bypass QA." \
  "Slicing must not bypass QA, but slicing may bypass QA." \
  "Slicing must not bypass QA; slicing may bypass QA."
run_policy_boundary_matrix \
  "end-task" \
  ".systems/ai/core/end-of-task-capture.md" \
  .systems/scripts/check-end-of-task-capture \
  "End task must not run phase-8-final-check." \
  "End task runs phase-8-final-check." \
  "End task must not run phase-8-final-check, but end task runs phase-8-final-check." \
  "End task must not run phase-8-final-check; end task runs phase-8-final-check."
run_policy_boundary_matrix \
  "idea-opt-out" \
  ".systems/ai/core/task-intake.md" \
  .systems/scripts/check-default-idea-validation-opt-out \
  "Without idea validation must not bypass risk checks." \
  "Without idea validation may bypass risk checks." \
  "Without idea validation must not bypass risk checks, but without idea validation may bypass risk checks." \
  "Without idea validation must not bypass risk checks; without idea validation may bypass risk checks."
run_policy_boundary_matrix \
  "owner-checkpoints" \
  ".systems/ai/core/owner-decision-checkpoints.md" \
  .systems/scripts/check-owner-decision-checkpoints \
  "Autopilot must not ask live questions while running." \
  "Autopilot may ask live questions while running." \
  "Autopilot must not ask live questions while running, but autopilot may ask live questions while running." \
  "Autopilot must not ask live questions while running; autopilot may ask live questions while running."
run_policy_boundary_matrix \
  "full-qa-verification" \
  ".systems/ai/core/full-qa-verification.md" \
  .systems/scripts/check-full-qa-verification \
  "Formal PASS must not occur without findings-first review." \
  "Formal PASS without findings-first review." \
  "Formal PASS must not occur without findings-first review, but formal PASS without findings-first review." \
  "Formal PASS must not occur without findings-first review; formal PASS without findings-first review."

run_policy_boundary_matrix \
  "cross-system-handoff" \
  ".systems/ai/core/cross-system-upgrade-handoff.md" \
  .systems/scripts/check-cross-system-upgrade-handoff \
  "Cross-system impact pending must not allow commit." \
  "Cross-system impact pending may allow commit." \
  "Cross-system impact pending must not allow commit, but cross-system impact pending may allow commit." \
  "Cross-system impact pending must not allow commit; cross-system impact pending may allow commit."
run_policy_boundary_matrix \
  "worktree-bootstrap" \
  ".systems/ai/core/worktree-bootstrap.md" \
  .systems/scripts/check-worktree-bootstrap \
  "Bootstrap must not skip approval." \
  "Bootstrap may skip approval." \
  "Bootstrap must not skip approval, but bootstrap may skip approval." \
  "Bootstrap must not skip approval; bootstrap may skip approval."
run_policy_boundary_matrix \
  "validation-routing" \
  ".systems/ai/core/validation-routing.md" \
  .systems/scripts/check-validation-routing \
  "Green scripts must not equal PASS." \
  "Green scripts equal PASS." \
  "Green scripts must not equal PASS, but green scripts equal PASS." \
  "Green scripts must not equal PASS; green scripts equal PASS."
run_policy_boundary_matrix \
  "model-selection" \
  ".systems/ai/core/model-selection-guidance.md" \
  .systems/scripts/check-model-selection-guidance \
  "Model selection must not bypass QA." \
  "Model selection may bypass QA." \
  "Model selection must not bypass QA, but model selection may bypass QA." \
  "Model selection must not bypass QA; model selection may bypass QA."

run_must_pass "cross-system-upgrade-handoff-valid" .systems/scripts/check-cross-system-upgrade-handoff

# END FROZEN region-3632-3827

# BEGIN FROZEN region-3925-3945
run_must_pass "validation-routing-valid" .systems/scripts/check-validation-routing
cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/- Workflow script applicability:.*\n//' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "validation-routing-requires-script-applicability" .systems/scripts/check-validation-routing
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/core/validation-routing.md" "$tmp/.systems/ai/core/validation-routing.md.bak"
printf '\nGreen scripts equal PASS.\n' >> "$tmp/.systems/ai/core/validation-routing.md"
run_must_fail "validation-routing-blocks-green-scripts-pass" .systems/scripts/check-validation-routing
mv "$tmp/.systems/ai/core/validation-routing.md.bak" "$tmp/.systems/ai/core/validation-routing.md"

run_must_pass "model-selection-guidance-valid" .systems/scripts/check-model-selection-guidance
cp "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak"
perl -0pi -e 's/- Blocking: `no`\n//' "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"
run_must_fail "model-selection-requires-non-blocking-field" .systems/scripts/check-model-selection-guidance
mv "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-4-implementation.template.md"

cp "$tmp/.systems/ai/core/model-selection-guidance.md" "$tmp/.systems/ai/core/model-selection-guidance.md.bak"
printf '\nModel selection may bypass QA.\n' >> "$tmp/.systems/ai/core/model-selection-guidance.md"
run_must_fail "model-selection-blocks-qa-bypass" .systems/scripts/check-model-selection-guidance
mv "$tmp/.systems/ai/core/model-selection-guidance.md.bak" "$tmp/.systems/ai/core/model-selection-guidance.md"
# END FROZEN region-3925-3945

# BEGIN FROZEN region-4052-4706
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/^### Evidence$/### Missing Evidence/m' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "pass-without-evidence" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/result: "PASS"/result: "FAIL"/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "pass-with-failed-command" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

v2_project="$tmp/ai-workflow-workspace/projects/qa-reader-smoke"
mkdir -p "$v2_project/specs" "$v2_project/quality"
printf 'Synthetic accepted specification.\n' > "$v2_project/specs/fixture.md"
printf 'Synthetic project context.\n' > "$v2_project/context.md"
cat > "$v2_project/status.md" <<'MD'
| Field | Value |
| --- | --- |
| `workflow-scope` | `plan-derived` |
| `current-task` | `LV-CORE-001-verdict-integrity` |
| `current-phase` | `phase-3-spec-qa` |
| `phase-result` | `PASS` |
| `next-phase` | `phase-4-implementation` |
| `blocking-reason` | `none` |
| `updated-at` | `2026-09-29` |
MD
cat > "$v2_project/tasks.md" <<'MD'
| Task ID | Title | Risk | Status | Task Card | Spec | Quality |
| --- | --- | --- | --- | --- | --- | --- |
| LV-CORE-001-verdict-integrity | Synthetic | high | ready | none | none | none |
MD
v2_input_sha="$(shasum -a 256 "$v2_project/specs/fixture.md" | awk '{print $1}')"
v2_digest="$(printf 'owning-project-evidence:specs/fixture.md=%s\n' "$v2_input_sha" | shasum -a 256 | awk '{print $1}')"
v2_report="$v2_project/quality/phase-3-lv-core-001-verdict-integrity-spec-qa.md"
cat > "$v2_report" <<MD
# Synthetic V2 Spec QA

QA verification contract: \`full-qa-verification-v2\`

## Current QA Run

- Run ID: v2-current-001
- Artifact kind: spec-qa
- Project/task identity: qa-reader-smoke:LV-CORE-001-verdict-integrity
- Assessed source HEAD: f362ce3c0ebb16c36e54bc48bb11b9a71db1548d
- Assessed worktree digest: $v2_digest
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | specs/fixture.md | $v2_input_sha |

### Findings

- Blockers: none
- Unresolved findings: none

### Evidence

- command: synthetic fixture check exited 0.

### Review Completeness Gate

- Status: complete
- Reviewed baseline: synthetic fixture version 1
- Closure freshness: current
- Post-fix full re-review: not-required
- Policy-boundary adversarial matrix: not-applicable
- Producer-consumer field audit: completed
- Required-field mapping: complete

### QA Verification Scope

- Synthetic specification readiness; no implementation verdict.

### Artifact QA Completeness Gate

- Owner intent and governing sources reviewed: synthetic owner instruction and accepted specification
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned
- Post-fix full artifact re-review: not-required
- Evidence reviewed: synthetic fixture and expected status transition
- Skipped or unreadable sources: none
- Residual risk: synthetic fixture only
- Closure freshness: current

### Gate Decision

- Spec QA result: PASS
- Can enter implementation: yes
- Required next phase: implementation

## Historical Runs

- Run ID: v2-old-001; Verdict: FAIL.
MD
cp "$v2_report" "$tmp/v2-report.orig"
run_must_pass "qa-evidence-v2-current-valid" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
run_must_pass "status-consistency-v2-current-valid" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-status-consistency --project qa-reader-smoke

sed 's/- Spec QA result: PASS/- Spec QA result: FAIL/' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-subsection-result-conflict" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
sed 's/- Can enter implementation: yes/- Can enter implementation: no/' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-subsection-progression" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
sed 's/- Required next phase: implementation/- Required next phase: 3.7. SPEC FIX LOOP/' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-pass-fix-loop-route" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
perl -0pe 's/^### Gate Decision$/### Checks\n\n| Check | Result | Evidence |\n| --- | --- | --- |\n| Source compatibility | FAIL | Synthetic mismatch |\n\n### Gate Decision/m' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-failed-artifact-check" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

cp "$v2_project/status.md" "$v2_project/status.md.bak"
sed 's/LV-CORE-001-verdict-integrity/LV-CORE-002-verdict-integrity/' "$v2_project/status.md.bak" > "$v2_project/status.md"
run_must_fail "status-consistency-v2-rejects-unmatched-task" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-status-consistency --project qa-reader-smoke
mv "$v2_project/status.md.bak" "$v2_project/status.md"

perl -0pe 's/^- Run ID: v2-current-001$/```md\n- Run ID: fake-history\n```\n- Run ID: v2-current-001/m' "$tmp/v2-report.orig" > "$v2_report"
run_must_pass "qa-evidence-v2-ignores-fenced-metadata" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

perl -0pe 's/^- Verdict: PASS$/```md\n- Verdict: PASS\n```/m' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-fenced-verdict" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

target_source="$tmp/target-source"
mkdir -p "$target_source"
printf 'Synthetic target input.\n' > "$target_source/fixture.md"
target_input_sha="$(shasum -a 256 "$target_source/fixture.md" | awk '{print $1}')"
target_digest="$(printf 'approved-target-source:fixture.md=%s\n' "$target_input_sha" | shasum -a 256 | awk '{print $1}')"
sed -e "s/owning-project-evidence | specs\/fixture.md | $v2_input_sha/approved-target-source | fixture.md | $target_input_sha/" -e "s/$v2_digest/$target_digest/" "$tmp/v2-report.orig" > "$v2_report"
run_must_pass "qa-evidence-v2-accepts-approved-target-root" python3 .systems/scripts/lib/qa-evidence.py "$v2_report" --workflow-root "$tmp" --workspace-root "$tmp/ai-workflow-workspace" --project qa-reader-smoke --approved-target-root "$target_source"
run_must_fail "qa-evidence-v2-rejects-unapproved-target-root" python3 .systems/scripts/lib/qa-evidence.py "$v2_report" --workflow-root "$tmp" --workspace-root "$tmp/ai-workflow-workspace" --project qa-reader-smoke
printf 'Synthetic external input.\n' > "$tmp/outside-input.md"
ln -s "$tmp/outside-input.md" "$target_source/linked.md"
linked_sha="$(shasum -a 256 "$tmp/outside-input.md" | awk '{print $1}')"
sed -e "s/fixture.md | $target_input_sha/linked.md | $linked_sha/" "$v2_report" > "$v2_report.bak"
mv "$v2_report.bak" "$v2_report"
run_must_fail "qa-evidence-v2-rejects-escaping-symlink" python3 .systems/scripts/lib/qa-evidence.py "$v2_report" --workflow-root "$tmp" --workspace-root "$tmp/ai-workflow-workspace" --project qa-reader-smoke --approved-target-root "$target_source"
cp "$tmp/v2-report.orig" "$v2_report"

cp "$tmp/v2-report.orig" "$v2_project/quality/recovery-phase-3-lv-core-001-verdict-integrity-spec-qa.md"
run_must_fail "status-consistency-v2-rejects-two-current-assessments" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-status-consistency --project qa-reader-smoke
rm "$v2_project/quality/recovery-phase-3-lv-core-001-verdict-integrity-spec-qa.md"

printf '\n## Current QA Run\n- Verdict: PASS\n' >> "$v2_report"
run_must_fail "qa-evidence-v2-rejects-duplicate-current" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

sed 's/v2-old-001/v2-current-001/' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-duplicate-run-id" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

printf 'Changed synthetic specification.\n' > "$v2_project/specs/fixture.md"
run_must_fail "qa-evidence-v2-rejects-stale-input" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
run_must_fail "status-consistency-v2-rejects-stale-input" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-status-consistency --project qa-reader-smoke
printf 'Synthetic accepted specification.\n' > "$v2_project/specs/fixture.md"

sed 's@specs/fixture.md@../specs/fixture.md@' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-traversal" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
cp "$tmp/v2-report.orig" "$v2_report"

sed 's@- Gate Decision: PASS@- Gate Decision: FAIL@' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-conflicting-gate" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
sed -e 's@- Verdict: PASS@- Verdict: FAIL@' -e 's@- Gate Decision: PASS@- Gate Decision: FAIL@' -e 's@- Spec QA result: PASS@- Spec QA result: FAIL@' -e 's@- Can enter implementation: yes@- Can enter implementation: no@' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "status-consistency-v2-rejects-current-fail" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-status-consistency --project qa-reader-smoke
perl -0pe 's/^### Findings\n.*?^### Evidence\n/```md\n### Findings\n- Blockers: none\n```\n/ms' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-fenced-fake-section" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
sed 's/qa-reader-smoke:LV-CORE-001-verdict-integrity/qa-reader-smoke:WRONG-01/' "$tmp/v2-report.orig" > "$v2_report"
run_must_fail "qa-evidence-v2-rejects-wrong-task-identity" env AI_WORKFLOW_WORKSPACE_HOME="$tmp/ai-workflow-workspace" .systems/scripts/check-qa-evidence --project qa-reader-smoke
rm -rf "$v2_project"

negative_final_check="$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-negative-final-check.md"
cat > "$negative_final_check" <<'MD'
# Negative final check

## Metadata

- Technical result: `FAIL`

## Completion Review

| Area | Result | Evidence |
| --- | --- | --- |
| Product checks | PASS | Focused checks completed. |
| Historical evidence | FAIL | The required registry is unresolved. |

## Evidence

- Command: focused check exited 0; this does not establish overall PASS.

## Gate Decision

- Result: FAIL
- Can-proceed: false
MD
run_must_pass "qa-evidence-ignores-component-pass-in-negative-final-check" .systems/scripts/check-qa-evidence

cat > "$negative_final_check" <<'MD'
# Incomplete positive final check

## Gate Decision

- Result: PASS
- Can-proceed: true
MD
run_must_fail "qa-evidence-positive-gate-still-requires-evidence" .systems/scripts/check-qa-evidence

cat > "$negative_final_check" <<'MD'
# Incomplete punctuated final check

## Gate Decision

- Result: PASS.
MD
run_must_fail "qa-evidence-punctuated-positive-still-requires-evidence" .systems/scripts/check-qa-evidence

cat > "$negative_final_check" <<'MD'
# Incomplete gate-only decision

## Gate Decision

- Can-proceed: true
MD
run_must_fail "qa-evidence-gate-only-positive-still-requires-evidence" .systems/scripts/check-qa-evidence

cat > "$negative_final_check" <<'MD'
# Contradictory final check

## Metadata

- Result: FAIL

## Evidence

- Command: focused check exited 0.

## Gate Decision

- Result: PASS
- Can-proceed: true
MD
run_must_fail "qa-evidence-rejects-conflicting-declared-results" .systems/scripts/check-qa-evidence
rm "$negative_final_check"

run_must_pass "full-qa-verification-valid" .systems/scripts/check-full-qa-verification

for legacy_contract_field in \
  'Legacy fingerprint admission is terminal for the exact registered file' \
  'A V1 marker takes precedence over pre-V1 admission' \
  'superseded-invalid-v1' \
  'does not upgrade the artifact'
do
  cp "$tmp/.systems/ai/core/full-qa-verification.md" "$tmp/.systems/ai/core/full-qa-verification.md.bak"
  perl -0pi -e "s/\\Q${legacy_contract_field}\\E//g" "$tmp/.systems/ai/core/full-qa-verification.md"
  legacy_contract_slug="$(printf '%s' "$legacy_contract_field" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-')"
  run_must_fail "full-qa-verification-requires-legacy-contract-${legacy_contract_slug}" .systems/scripts/check-full-qa-verification
  mv "$tmp/.systems/ai/core/full-qa-verification.md.bak" "$tmp/.systems/ai/core/full-qa-verification.md"
done

cp "$tmp/.systems/ai/templates/workflow/phase-1-architecture-qa.template.md" "$tmp/.systems/ai/templates/workflow/phase-1-architecture-qa.template.md.bak"
perl -0pi -e 's/## Artifact QA Completeness Gate/## Missing Artifact Gate/' "$tmp/.systems/ai/templates/workflow/phase-1-architecture-qa.template.md"
run_must_fail "full-qa-verification-requires-artifact-completeness-gate" .systems/scripts/check-full-qa-verification
mv "$tmp/.systems/ai/templates/workflow/phase-1-architecture-qa.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-1-architecture-qa.template.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/^## Current QA Run$/## Missing Current QA Run/m' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "full-qa-verification-requires-current-phase5-run" .systems/scripts/check-full-qa-verification
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/core/full-qa-verification.md" "$tmp/.systems/ai/core/full-qa-verification.md.bak"
printf '\nTechnical checks are enough without owner intent.\n' >> "$tmp/.systems/ai/core/full-qa-verification.md"
run_must_fail "full-qa-verification-blocks-technical-only-qa" .systems/scripts/check-full-qa-verification
mv "$tmp/.systems/ai/core/full-qa-verification.md.bak" "$tmp/.systems/ai/core/full-qa-verification.md"

cp "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak"
perl -0pi -e 's/\| Forbidden States\/Rows \|/| Missing Forbidden States |/' "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"
run_must_fail "full-qa-verification-requires-forbidden-state-matrix-field" .systems/scripts/check-full-qa-verification
mv "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md.bak" "$tmp/.systems/ai/templates/workflow/phase-5-quality.template.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak"
perl -0pi -e 's/## Artifact QA Completeness Gate/## Missing Artifact QA Gate/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"
run_must_fail "qa-evidence-requires-artifact-completeness-for-pass" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak"
perl -0pi -e 's/- QA verification contract: `full-qa-verification-v2`\n//' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"
run_must_fail "qa-evidence-requires-contract-marker-for-formal-pass" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak"
perl -0pi -e 's/Scope and out-of-scope consistency: `aligned`/Scope and out-of-scope consistency: `mismatch`/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"
run_must_fail "qa-evidence-rejects-artifact-pass-with-scope-mismatch" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md"

legacy_qa="$tmp/ai-workflow-workspace/projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md"
legacy_registry="$tmp/ai-workflow-workspace/repo/core/legacy-qa-evidence-v1.md"
mkdir -p "$(dirname "$legacy_qa")" "$(dirname "$legacy_registry")"
cat > "$legacy_qa" <<'MD'
# Registered Legacy QA Evidence

Result: `PASS`
MD
legacy_checksum="$(shasum -a 256 "$legacy_qa" | awk '{print $1}')"
write_legacy_registry() {
  local path="$1"
  local checksum="$2"
  local classification="${3:-historical QA artifact; bytes preserved}"
  cat > "$legacy_registry" <<EOF
# Legacy QA Evidence Registry

| Relative workspace path | SHA-256 | Classification |
| --- | --- | --- |
| $path | $checksum | $classification |
EOF
}

write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "$legacy_checksum" \
  "historical QA artifact; bytes preserved"
run_must_pass "qa-evidence-allows-registered-legacy-fingerprint" .systems/scripts/check-qa-evidence

generic_legacy="$tmp/ai-workflow-workspace/projects/upgrade-with-master-prompt/quality/phase-4-legacy-implementation-result.md"
cat > "$generic_legacy" <<'MD'
# Registered Legacy Implementation Evidence

Result: `PASS`
MD
generic_legacy_checksum="$(shasum -a 256 "$generic_legacy" | awk '{print $1}')"
write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-4-legacy-implementation-result.md" \
  "$generic_legacy_checksum" \
  "historical QA artifact; bytes preserved"
printf '| %s | %s | %s |\n' \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "$legacy_checksum" \
  "historical QA artifact; bytes preserved" >> "$legacy_registry"
run_must_pass "qa-evidence-allows-registered-legacy-fingerprint-for-generic-quality-file" .systems/scripts/check-qa-evidence
rm "$generic_legacy"

write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "$legacy_checksum" \
  "historical QA artifact; bytes preserved"

cp "$legacy_qa" "$legacy_qa.bak"
printf '\nTampered legacy evidence.\n' >> "$legacy_qa"
run_must_fail "qa-evidence-rejects-tampered-legacy-fingerprint" .systems/scripts/check-qa-evidence
mv "$legacy_qa.bak" "$legacy_qa"

unregistered_legacy="$tmp/ai-workflow-workspace/projects/unregistered-legacy/quality/phase-1-architecture-qa.md"
mkdir -p "$(dirname "$unregistered_legacy")"
cp "$legacy_qa" "$unregistered_legacy"
run_must_fail "qa-evidence-rejects-unregistered-legacy-fingerprint" .systems/scripts/check-qa-evidence
rm "$unregistered_legacy"

write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "0000000000000000000000000000000000000000000000000000000000000000"
run_must_fail "qa-evidence-rejects-wrong-legacy-checksum" .systems/scripts/check-qa-evidence

write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-2-plan-qa.md" \
  "$legacy_checksum"
run_must_fail "qa-evidence-rejects-wrong-legacy-path" .systems/scripts/check-qa-evidence

outside_legacy="$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-2-plan-qa.md"
cat > "$outside_legacy" <<'MD'
# Outside Workspace Legacy QA Evidence

Result: `PASS`
MD
write_legacy_registry \
  "projects/outside-workspace/quality/phase-2-plan-qa.md" \
  "$(shasum -a 256 "$outside_legacy" | awk '{print $1}')"
run_must_fail "qa-evidence-rejects-outside-workspace-legacy" .systems/scripts/check-qa-evidence
rm "$outside_legacy"

v1_incomplete="$tmp/ai-workflow-workspace/projects/registered-v1/quality/phase-1-architecture-qa.md"
mkdir -p "$(dirname "$v1_incomplete")"
cat > "$v1_incomplete" <<'MD'
# Registered Incomplete V1 QA Evidence

QA verification contract: `full-qa-verification-v1`

Result: `PASS`
MD
write_legacy_registry \
  "projects/registered-v1/quality/phase-1-architecture-qa.md" \
  "$(shasum -a 256 "$v1_incomplete" | awk '{print $1}')"
printf '| %s | %s | %s |\n' \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "$legacy_checksum" \
  "historical QA artifact; bytes preserved" >> "$legacy_registry"
run_must_fail "qa-evidence-v1-first-overrides-legacy-admission" .systems/scripts/check-qa-evidence

run_must_pass "qa-evidence-project-scope-isolates-other-project" .systems/scripts/check-qa-evidence --project upgrade-with-master-prompt
run_must_fail "qa-evidence-selected-project-still-fails" .systems/scripts/check-qa-evidence --project registered-v1
run_must_fail "qa-evidence-rejects-unsafe-project" .systems/scripts/check-qa-evidence --project ../registered-v1
run_must_fail "qa-evidence-rejects-missing-project" .systems/scripts/check-qa-evidence --project absent-project

v1_recovery="${v1_incomplete%/*}/recovery-phase-1-architecture-qa.md"
write_v1_compat_fixture() {
  local source="$1" destination="$2" first_section="$3"
  awk -v first_section="$first_section" '
    $0 == "## Current QA Run" { in_run=1; emitting=0; next }
    in_run && $0 == first_section { emitting=1 }
    in_run && !emitting { next }
    /Example hashes below are schema illustrations/ { next }
    {
      gsub(/full-qa-verification-v2/, "full-qa-verification-v1")
      if ($0 ~ /^### /) sub(/^### /, "## ")
      print
    }
  ' "$source" > "$destination"
}
write_v1_compat_fixture "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-1-architecture-qa.md" "$v1_recovery" '### QA Verification Scope'
v1_checksum="$(shasum -a 256 "$v1_incomplete" | awk '{print $1}')"
recovery_checksum="$(shasum -a 256 "$v1_recovery" | awk '{print $1}')"
write_recovery_registry() {
  local original_sha="${1:-$v1_checksum}"
  local replacement_sha="${2:-$recovery_checksum}"
  cat > "$legacy_registry" <<EOF
# Legacy QA Evidence Registry

| Classification | Workspace-relative artifact path | Original SHA-256 | Replacement path | Replacement SHA-256 |
| --- | --- | --- | --- | --- |
| pre-v1 | \`projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md\` | \`$legacy_checksum\` | none | none |
| superseded-invalid-v1 | \`projects/registered-v1/quality/phase-1-architecture-qa.md\` | \`$original_sha\` | \`projects/registered-v1/quality/recovery-phase-1-architecture-qa.md\` | \`$replacement_sha\` |
EOF
}
write_recovery_registry
run_must_pass "qa-evidence-five-column-verified-v1-recovery" .systems/scripts/check-qa-evidence

cp "$v1_incomplete" "$v1_incomplete.bak"
perl -0pi -e 's/QA verification contract: `full-qa-verification-v1`/No V1 marker/' "$v1_incomplete"
write_recovery_registry "$(shasum -a 256 "$v1_incomplete" | awk '{print $1}')" "$recovery_checksum"
run_must_pass "qa-evidence-recovery-admits-unmarked-historical-original" .systems/scripts/check-qa-evidence
mv "$v1_incomplete.bak" "$v1_incomplete"
write_recovery_registry

cp "$v1_recovery" "$v1_recovery.bak"
printf '\nTampered recovery.\n' >> "$v1_recovery"
run_must_fail "qa-evidence-rejects-tampered-recovery" .systems/scripts/check-qa-evidence
mv "$v1_recovery.bak" "$v1_recovery"

write_recovery_registry "$v1_checksum" "0000000000000000000000000000000000000000000000000000000000000000"
run_must_fail "qa-evidence-rejects-wrong-recovery-fingerprint" .systems/scripts/check-qa-evidence
write_recovery_registry

cp "$v1_incomplete" "$v1_incomplete.bak"
printf '\nTampered original.\n' >> "$v1_incomplete"
run_must_fail "qa-evidence-rejects-tampered-v1-original" .systems/scripts/check-qa-evidence
mv "$v1_incomplete.bak" "$v1_incomplete"

cp "$v1_recovery" "$v1_recovery.bak"
perl -0pi -e 's/## Artifact QA Completeness Gate/## Missing Artifact QA Gate/' "$v1_recovery"
write_recovery_registry "$v1_checksum" "$(shasum -a 256 "$v1_recovery" | awk '{print $1}')"
run_must_fail "qa-evidence-rejects-incomplete-v1-recovery" .systems/scripts/check-qa-evidence
mv "$v1_recovery.bak" "$v1_recovery"

write_recovery_registry
rm "$v1_recovery"
run_must_fail "qa-evidence-rejects-missing-v1-recovery" .systems/scripts/check-qa-evidence
rm "$v1_incomplete"

phase5_original="$tmp/ai-workflow-workspace/projects/registered-v1/quality/phase-5-historical-quality.md"
phase5_recovery="${phase5_original%/*}/recovery-phase-5-historical-quality.md"
cat > "$phase5_original" <<'MD'
# Incomplete Historical QA

Result: `PASS`
MD
write_v1_compat_fixture "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$phase5_recovery" '### Definition Of Done Validation'
perl -0pi -e 's/Applicability: `required`/Applicability: `not-applicable`\n- Not-applicable reason: recovery does not add a data integration./' "$phase5_recovery"
cat > "$legacy_registry" <<EOF
# Legacy QA Evidence Registry

| Classification | Workspace-relative artifact path | Original SHA-256 | Replacement path | Replacement SHA-256 |
| --- | --- | --- | --- | --- |
| pre-v1 | \`projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md\` | \`$legacy_checksum\` | none | none |
| superseded-invalid-v1 | \`projects/registered-v1/quality/phase-5-historical-quality.md\` | \`$(shasum -a 256 "$phase5_original" | awk '{print $1}')\` | \`projects/registered-v1/quality/recovery-phase-5-historical-quality.md\` | \`$(shasum -a 256 "$phase5_recovery" | awk '{print $1}')\` |
EOF
run_must_pass "qa-evidence-allows-plain-not-applicable-recovery-reason" .systems/scripts/check-qa-evidence
rm "$phase5_original" "$phase5_recovery"

write_legacy_registry \
  "projects/upgrade-with-master-prompt/quality/phase-1-architecture-qa.md" \
  "$legacy_checksum"

scoped_status="$tmp/ai-workflow-workspace/projects/upgrade-with-master-prompt/status.md"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md" "$scoped_status"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/tasks.md" "${scoped_status%/*}/tasks.md"
cp "$tmp/.systems/ai/examples/projects/EXAMPLE/context.md" "${scoped_status%/*}/context.md"
bad_project="$tmp/ai-workflow-workspace/projects/unrelated-project"
mkdir -p "$bad_project"
cp "$scoped_status" "$bad_project/status.md"
cp "${scoped_status%/*}/tasks.md" "$bad_project/tasks.md"
cp "${scoped_status%/*}/context.md" "$bad_project/context.md"
perl -0pi -e 's/`phase-4-implementation`/`not-a-phase`/' "$bad_project/status.md"
printf '# Invalid name in another project\n' > "$bad_project/Bad Name.md"
run_must_pass "naming-project-scope-isolates-other-project" .systems/scripts/check-naming --project upgrade-with-master-prompt
run_must_fail "naming-global-still-fails" .systems/scripts/check-naming
run_must_fail "naming-rejects-unsafe-project" .systems/scripts/check-naming --project ../unrelated-project
run_must_pass "status-consistency-project-scope-isolates-other-project" .systems/scripts/check-status-consistency --project upgrade-with-master-prompt
run_must_fail "status-consistency-selected-project-still-fails" .systems/scripts/check-status-consistency --project unrelated-project
run_must_fail "status-consistency-global-still-fails" .systems/scripts/check-status-consistency
run_must_fail "status-consistency-rejects-unsafe-project" .systems/scripts/check-status-consistency --project ../unrelated-project
run_must_fail "status-consistency-rejects-missing-project" .systems/scripts/check-status-consistency --project absent-project
run_must_pass "workflow-fast-project-scope" .systems/scripts/validate-workflow --profile fast --project upgrade-with-master-prompt --explain
run_must_fail "workflow-fast-global-still-fails" .systems/scripts/validate-workflow --profile fast
run_must_fail "workflow-fast-rejects-unsafe-project" .systems/scripts/validate-workflow --profile fast --project ../unrelated-project
rm -rf "$bad_project"
rm "$scoped_status" "${scoped_status%/*}/tasks.md" "${scoped_status%/*}/context.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/## Adaptive Data \/ Integration Verification Matrix/## Missing Adaptive Matrix/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-requires-adaptive-matrix-for-phase-5-pass" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

run_must_pass "qa-evidence-allows-complete-phase-5-v2-pass" .systems/scripts/check-qa-evidence

phase5_v2="$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/^- Result: `PASS`$/- Result: `FAIL`/m' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-report-level-result-conflict" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
printf '\n## Validation Execution Record\n\n- Final verdict: FAIL\n' >> "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-final-verdict-conflict" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/(^### Gate Decision\n(?:(?!^## ).)*?\bresult: )PASS/${1}FAIL/ms' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-phase5-subsection-conflict" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
sed 's/required-next-phase: "phase-6-distillation"/required-next-phase: "phase-5-fix-loop"/' "$phase5_v2.bak" > "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-phase5-fix-loop-route" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/(- Quality result: `PASS`\n)/$1- Required next phase: phase-5-fix-loop\n/' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-quality-gate-fix-loop-route" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/^### Gate Decision$/### Edge Cases\n\n| Edge Case | Result | Evidence |\n| --- | --- | --- |\n| Empty input | FAIL | Missing coverage |\n\n### Gate Decision/m' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-failed-edge-case" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/^(- Cross-contract consistency aligned: `yes`)$/```md\n$1\n```/m' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-fenced-quality-field" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/Owner instruction mismatch: `no`/Owner instruction mismatch: `yes`/' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-owner-mismatch" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/Negative-space \/ adversarial review: `completed`/Negative-space \/ adversarial review: `incomplete`/' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-incomplete-adversarial-review" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/Cross-contract consistency aligned: `yes`/Cross-contract consistency aligned: `no`/' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-unverified-quality-gate" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

cp "$phase5_v2" "$phase5_v2.bak"
perl -0pi -e 's/Applicability: `not-applicable`/Applicability: `required`/; s/\| \| \| \| \| \| \| \|/| input record | canonical profile | derived output | wrong profile | explicit error | integration test | |/' "$phase5_v2"
run_must_fail "qa-evidence-v2-rejects-incomplete-matrix-row" .systems/scripts/check-qa-evidence
mv "$phase5_v2.bak" "$phase5_v2"

phase8_v2="$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md"
cp "$phase8_v2" "$phase8_v2.bak"
perl -0pi -e 's/Example artifacts present and internally linked \| PASS/Example artifacts present and internally linked | FAIL/' "$phase8_v2"
run_must_fail "qa-evidence-v2-rejects-failed-completion-row" .systems/scripts/check-qa-evidence
mv "$phase8_v2.bak" "$phase8_v2"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/^### Definition Of Done Validation$/### Missing DoD Validation/m' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-v2-rejects-missing-current-dod" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md.bak"
perl -0pi -e 's/Can close active plan: awaiting-owner/Can close active plan: yes/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md"
run_must_fail "qa-evidence-v2-rejects-final-owner-bypass" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-8-final-check.md"

for heading in \
  'Definition Of Done Validation' \
  'Intent / Plan / Spec Compliance' \
  'Review Completeness Gate' \
  'Findings'
do
  cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
  perl -0pi -e "s{\\Q## ${heading}\\E}{## Missing ${heading}}" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
  heading_slug="$(printf '%s' "$heading" | tr '[:upper:] ' '[:lower:]-' | tr -cd '[:alnum:]-')"
  run_must_fail "qa-evidence-requires-phase-5-${heading_slug}" .systems/scripts/check-qa-evidence
  mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
done

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/\| Example artifact flow is linked and internally consistent \| PASS \|/| Example artifact flow is linked and internally consistent | FAIL |/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-rejects-phase-5-pass-with-failed-dod" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/Compliance status: `aligned`/Compliance status: `partial`/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-rejects-phase-5-pass-with-partial-intent-compliance" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/Closure freshness: `current`/Closure freshness: `stale`/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-rejects-phase-5-pass-with-stale-completeness-gate" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/- Critical errors: none\./- P1: unresolved artifact-flow regression./' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-rejects-phase-5-pass-with-unresolved-p1" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/100% DoD satisfied: `yes`/100% DoD satisfied: `no`/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-rejects-phase-5-pass-with-unsatisfied-quality-gate" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/Applicability: `not-applicable`/Applicability: `required`/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_fail "qa-evidence-requires-complete-required-adaptive-matrix-row" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak"
perl -0pi -e 's/Applicability: `not-applicable`/Applicability: `required`/; s/\| \| \| \| \| \| \| \|/| input record | canonical profile | derived output | wrong profile | explicit error | integration test | manual trace |/' "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"
run_must_pass "qa-evidence-allows-complete-required-adaptive-matrix-row" .systems/scripts/check-qa-evidence
mv "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md.bak" "$tmp/.systems/ai/examples/projects/EXAMPLE/quality/phase-5-ex-01-quality.md"

cp "$tmp/example-status.orig" "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md"
perl -0pi -e 's/^\| `current-phase` \| `[^`]+` \|$/| `current-phase` | `phase-1-architecture` |/m' "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md"
perl -0pi -e 's/^\| `phase-result` \| `[^`]+` \|$/| `phase-result` | `PASS` |/m' "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md"
perl -0pi -e 's/^\| `next-phase` \| `[^`]+` \|$/| `next-phase` | `phase-8-final-check` |/m' "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md"
run_must_fail "bad-phase-transition" .systems/scripts/check-status-consistency
cp "$tmp/example-status.orig" "$tmp/.systems/ai/examples/projects/EXAMPLE/status.md"

# END FROZEN region-4052-4706


echo "Owned smoke group passed."
smoke_suite_completed=1
