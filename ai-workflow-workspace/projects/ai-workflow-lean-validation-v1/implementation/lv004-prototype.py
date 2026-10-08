"""Build an isolated, unpromoted literal partition for equivalence investigation."""
import hashlib
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
frozen = project / "implementation/lv004-reference"
inventory = json.loads((frozen / "inventory.json").read_text())
lines = (frozen / "check-validator-smoke-tests.sh").read_text().splitlines(keepends=True)
parser = argparse.ArgumentParser()
parser.add_argument("--candidate-root", type=Path, required=True)
args = parser.parse_args()
candidate = args.candidate_root.resolve()
if not candidate.is_relative_to(Path("/tmp").resolve()):
    raise SystemExit("Prototype output must be in the approved temporary root")
candidate.mkdir(exist_ok=True)
for name in (".systems", ".github"):
    shutil.copytree(root / name, candidate / name, dirs_exist_ok=True)
for name in ("AGENTS.md", "HUMANS.md", "README.md", ".gitignore"):
    shutil.copy2(root / name, candidate / name)

# Whole top-level intervals, including every mutation, check and restoration.
# bash -n below rejects intervals ending inside a function, control flow or heredoc.
regions = [
    ("core", 701, 1210),
    ("workspace", 1270, 1511),
    ("policy", 1512, 1544),
    ("skills", 1545, 1967),
    ("workspace", 1968, 1971),
    ("policy", 1972, 2310),
    ("workspace", 2311, 2827),
    ("quality", 2828, 3215),
    ("policy", 3216, 3631),
    ("quality", 3632, 3827),
    ("policy", 3828, 3924),
    ("quality", 3925, 3945),
    ("workspace", 3946, 4033),
    ("policy", 4034, 4051),
    ("quality", 4052, 4706),
    ("workspace", 4707, 4812),
    ("policy", 4813, 4845),
    ("workspace", 4846, 4866),
    ("core", 4867, 4872),
    ("skills", 4873, 4878),
    ("workspace", 4879, 4893),
]

covered = set()
for group, start, end in regions:
    for n in range(start, end + 1):
        if n in covered:
            raise SystemExit("Duplicate source ownership")
        covered.add(n)
for n in range(701, 4894):
    if n not in covered and n not in range(1211, 1270):
        raise SystemExit(f"Missing executable source line: {n}")

common = "".join(lines[113:686] + lines[692:700] + lines[1210:1265])
common = common.replace('"$(smoke_test_group "$name")"', '"${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}"')
common = common.replace('"smoke-$smoke_group" child', '"${AI_WORKFLOW_SMOKE_TIMING_PROFILE:-smoke-$smoke_group}" child')
common += '''
should_run_smoke_test() {
  local name="$1"
  # These four nested negative-helper probes are checked by their enclosing
  # infrastructure assertions, not independently owned suite cases.
  case "$name" in
    smoke-helper-rejects-unexpected-timeout|smoke-helper-rejects-missing-source|smoke-helper-rejects-wrong-error-code|smoke-helper-rejects-wrong-diagnostic) return 0 ;;
  esac
  if [[ -n "${AI_WORKFLOW_SMOKE_LEDGER:-}" ]]; then
    printf '%s\\t%s\\n' "$name" "${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}" >> "$AI_WORKFLOW_SMOKE_LEDGER"
  fi
  return 0
}
'''
common_path = candidate / ".systems/scripts/smoke/common.sh"
common_path.parent.mkdir(exist_ok=True)
common_path.write_text("#!/usr/bin/env bash\n# Pure shared function definitions; no execution on import.\n" + common)
header = "".join(lines[:113])
header = header.replace("smoke_group=\"all\"", 'smoke_group="${AI_WORKFLOW_SMOKE_OWNED_GROUP:?}"')
header = header.replace("if [[ -n \"${AI_WORKFLOW_TIMING_OUTPUT:-}\" ]]; then", "if [[ -n \"${AI_WORKFLOW_TIMING_OUTPUT:-}\" && \"${AI_WORKFLOW_SMOKE_CHILD:-0}\" != 1 ]]; then")
header = header.replace("AI_WORKFLOW_SMOKE_START", "AI_WORKFLOW_SMOKE_GROUP_START")
header = header.replace("AI_WORKFLOW_SMOKE_COMPLETE", "AI_WORKFLOW_SMOKE_GROUP_COMPLETE")
header += 'source "$(pwd -P)/.systems/scripts/smoke/common.sh"\n'
header += "".join(lines[1265:1268])
groups = ("core", "policy", "quality", "skills", "workspace")
entries = []
id_groups = {}
group_patterns = {}
calls = []
for group in groups:
    chunks = []
    patterns = []
    for assigned, start, end in regions:
        if assigned != group:
            continue
        chunk = "".join(lines[start - 1:end])
        result = subprocess.run(["bash", "-n"], input=chunk, text=True, capture_output=True)
        if result.returncode:
            raise SystemExit(f"Invalid boundary {group} {start}-{end}: {result.stderr}")
        chunks.append(f"# BEGIN FROZEN region-{start:04d}-{end:04d}\n" + chunk + f"# END FROZEN region-{start:04d}-{end:04d}\n")
        for match in re.finditer(r'(run_must_(?:pass|fail))\s+"([^"]+)"[^\n]*', chunk):
            helper, name = match.group(1, 2)
            pattern = re.sub(r"\$\{[^}]+\}|\$[a-zA-Z_][a-zA-Z_0-9]*", "*", name)
            patterns.append(pattern)
            calls.append((group, pattern, helper, match.group(0), f"region-{start:04d}-{end:04d}"))
        for match in re.finditer(r'run_policy_boundary_matrix\s+\\\n\s+"([^"]+)"\s+\\\n[^\n]+\n[^\n]+', chunk):
            scope = match.group(1)
            patterns.append("policy-boundary-" + scope + "-*")
            calls.append((group, "policy-boundary-" + scope + "-*", "matrix", match.group(0), f"region-{start:04d}-{end:04d}"))
        entries.append({
            "id": f"region-{start:04d}-{end:04d}", "group": group,
            "reference_lines": [start, end],
            "source_sha256": hashlib.sha256(chunk.encode()).hexdigest(),
            "assertion_ids": [a["id"] for a in inventory["candidate_external_assertion_lines"] if start <= a["source_line"] <= end],
            "setup_id": "isolated-source-copy-and-owned-region-setup",
            "cleanup_id": "exit-trap-removes-owned-fixture",
            "mutation_id": "literal-reference-region",
            "expected_outcome": "identical wrapper status/diagnostic and post-call assertions",
        })
    import fnmatch
    ids = [i for i in inventory["reference_test_ids"] if any(fnmatch.fnmatchcase(i, pat) for pat in patterns)]
    group_patterns[group] = patterns
    supplement = (project / "implementation/lv004-supplement.sh").read_text() if group == "core" else ""
    body = header + "\n".join(chunks) + "\n" + supplement + '\necho "Owned smoke group passed."\nsmoke_suite_completed=1\n'
    path = candidate / f".systems/scripts/smoke/{group}.sh"
    path.write_text(body)
    result = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    if result.returncode:
        raise SystemExit(result.stderr)
for identifier in inventory["reference_test_ids"]:
    literal = [g for g, patterns in group_patterns.items() if identifier in patterns]
    matching = literal or [g for g, patterns in group_patterns.items() if any(fnmatch.fnmatchcase(identifier, pat) for pat in patterns)]
    if len(matching) != 1:
        raise SystemExit(f"Ambiguous or absent wrapper ownership: {identifier}: {matching}")
    id_groups[identifier] = matching[0]
missing = set(inventory["reference_test_ids"]) - set(id_groups)
if missing:
    raise SystemExit("Unmapped executed identities: " + ", ".join(sorted(missing)))
supplemental_ids = ["smoke-partition-manifest-valid"] + ["smoke-partition-rejects-" + case for case in ("missing-id", "duplicate-id", "missing-region", "missing-audit", "missing-nested-audit", "wrong-assertion-line", "wrong-nested-owner", "wrong-test-region", "removed-post-call-assertion")]
supplemental_ids += ["smoke-observability-allows-safe-prohibition"] + ["smoke-observability-rejects-" + case for case in ("direct", "but", "however", "period", "colon", "unless", "yet", "semicolon", "missing-source")]
id_groups.update({identifier: "core" for identifier in supplemental_ids})
for match in re.finditer(r'(run_must_(?:pass|fail))\s+"([^"]+)"[^\n]*', (project / "implementation/lv004-supplement.sh").read_text()):
    helper, name = match.group(1, 2)
    pattern = re.sub(r"\$\{[^}]+\}|\$[a-zA-Z_][a-zA-Z_0-9]*", "*", name)
    calls.append(("core", pattern, helper, match.group(0), "supplemental-core"))
tests = []
for identifier, group in id_groups.items():
    possible = [row for row in calls if row[0] == group and fnmatch.fnmatchcase(identifier, row[1])]
    literal = [row for row in possible if row[1] == identifier]
    if not possible:
        raise SystemExit("Missing source outcome contract: " + identifier)
    _, pattern, helper, command, region_id = (literal or possible)[0]
    if helper == "matrix":
        helper = "run_must_pass" if identifier.endswith("allows-safe-prohibition") else "run_must_fail"
    tests.append({"id": identifier, "group": group, "region_id": region_id,
                  "helper": helper, "command_contract": command,
                  "setup_id": "owned-group-disposable-source-fixture",
                  "cleanup_id": "owned-group-exit-trap-and-supervisor-tree-cleanup",
                  "mutation_id": pattern,
                  "expected_outcome": "exit 0" if helper == "run_must_pass" else "exact typed nonzero status, specific diagnostic and expected literal when specified"})
audit = []
for point in inventory["candidate_external_assertion_lines"]:
    text = point["text"].strip()
    classification = "failure-fixture" if point["source_line"] == 938 else "failure-branch" if text == "exit 1" else "assertion"
    audit.append({"id": point["id"], "source_line": point["source_line"], "sha256": point["sha256"], "classification": classification,
                  "rationale": "Synthetic failure injection, not an independent assertion" if classification == "failure-fixture" else "Failure arm of preceding condition; preserved with complete control flow" if classification == "failure-branch" else "Executable post-call/structural invariant retained with its fixture transaction"})
nested = []
for number, line in enumerate(lines, 1):
    if re.match(r"\s*(assert\b|raise AssertionError)", line):
        owners = [(group, start, end) for group, start, end in regions if start <= number <= end]
        if len(owners) != 1:
            raise SystemExit("Unowned nested Python assertion")
        group, start, end = owners[0]
        nested.append({"id": f"mono-python-line-{number:04d}", "source_line": number,
                       "group": group, "region_id": f"region-{start:04d}-{end:04d}",
                       "sha256": hashlib.sha256(line.rstrip("\n").encode()).hexdigest(),
                       "rationale": "Preserved inside the owned synthetic scope probe, including assertion and failure branches; raw region digest binds complete Python control flow"})
manifest = {
    "schema": 2, "groups": list(groups),
    "reference_sha256": inventory["source_sha256"],
    "reference_test_ids": inventory["reference_test_ids"],
    "reference_ids_sha256": hashlib.sha256(("\n".join(inventory["reference_test_ids"]) + "\n").encode()).hexdigest(),
    "supplemental_test_ids": supplemental_ids,
    "external_assertion_audit": audit,
    "nested_python_assertions": nested,
    "external_assertion_ids": [a["id"] for a in inventory["candidate_external_assertion_lines"]],
    "regions": entries, "test_groups": id_groups,
    "tests": tests,
    "files_sha256": {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in common_path.parent.glob("*.sh")},
}
(candidate / ".systems/scripts/smoke/manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
shutil.copy2(project / "implementation/lv004-dispatcher.template.sh", candidate / ".systems/scripts/check-validator-smoke-tests")
(candidate / ".systems/scripts/check-validator-smoke-tests").chmod((root / ".systems/scripts/check-validator-smoke-tests").stat().st_mode & 0o777)
# Narrow consumer relocation: progress is produced by the imported helper,
# while top-level lifecycle remains in the public dispatcher.
completion = candidate / ".systems/scripts/check-validation-completion"
text = completion.read_text()
old = 'for marker in "AI_WORKFLOW_SMOKE_START" "AI_WORKFLOW_SMOKE_PROGRESS" "AI_WORKFLOW_SMOKE_COMPLETE"; do'
if old not in text:
    raise SystemExit("Completion source changed; re-review the relocation")
text = text.replace(old, 'for marker in "AI_WORKFLOW_SMOKE_START" "AI_WORKFLOW_SMOKE_COMPLETE"; do')
text = text.replace('require_text .systems/scripts/check-validator-smoke-tests "AI_WORKFLOW_SMOKE_PROGRESS" "smoke progress marker"', 'require_text .systems/scripts/smoke/common.sh "AI_WORKFLOW_SMOKE_PROGRESS" "smoke progress marker"')
text = text.replace('  ".systems/scripts/check-validator-smoke-tests"', '  ".systems/scripts/check-validator-smoke-tests"\n  ".systems/scripts/smoke/common.sh"\n  ".systems/scripts/smoke/manifest.json"')
text = text.replace('require_text .systems/scripts/validate-workflow "--progress"', '''for group in core policy quality skills workspace; do
  require_text ".systems/scripts/smoke/$group.sh" "AI_WORKFLOW_SMOKE_GROUP_START" "group start $group"
  require_text ".systems/scripts/smoke/$group.sh" "AI_WORKFLOW_SMOKE_GROUP_COMPLETE" "group completion $group"
done

require_text .systems/scripts/validate-workflow "--progress"''')
completion.write_text(text)
observability = candidate / ".systems/scripts/check-validation-observability"
shutil.copy2(project / "implementation/lv004-observability.template.sh", observability)
observability.chmod((root / ".systems/scripts/check-validation-observability").stat().st_mode & 0o777)
print(json.dumps({"candidate": str(candidate), "ids": len(id_groups), "regions": len(entries)}))
