#!/usr/bin/env bash
set -euo pipefail
fail=0
source .systems/scripts/lib/policy-boundaries.sh
for file in .systems/ai/core/validation-observability.md .systems/scripts/validate-workflow .systems/scripts/check-validator-smoke-tests .systems/scripts/lib/validation-timing.py .systems/scripts/report-validation-comparison .systems/scripts/smoke/manifest.json .systems/scripts/smoke/common.sh; do
  [[ -f "$file" ]] || { echo "Missing validation observability artifact: $file"; fail=1; }
done
for text in '--timing-output' 'median' 'three' 'group' 'all' 'equivalence' 'supporting evidence' 'monotonic' 'run_id' 'record_kind' 'parent_id' 'incomplete'; do
  rg -qi -- "$text" .systems/ai/core/validation-observability.md .systems/scripts/validate-workflow .systems/scripts/check-validator-smoke-tests || { echo "Validation observability missing: $text"; fail=1; }
done
policy_reject_unsafe_pattern \
  'green[^.;:]*scripts[^.;:]*PASS|skip[^.;:]*coverage|group[^.;:]*replace[^.;:]*all' \
  "Validation observability weakens coverage or PASS integrity" \
  .systems/ai/core/validation-observability.md
if ! bash .systems/scripts/check-validator-smoke-tests --verify-manifest; then
  echo "Validation observability smoke manifest invalid"
  fail=1
fi
exit "$fail"
