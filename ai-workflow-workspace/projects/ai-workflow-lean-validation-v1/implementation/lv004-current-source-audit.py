"""Bind structural/ownership evidence to the current thirteen-path ceiling."""
import collections
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
smoke = root / ".systems/scripts/smoke"
manifest = json.loads((smoke / "manifest.json").read_text())
paths = [".systems/scripts/check-validator-smoke-tests", ".systems/scripts/smoke/manifest.json",
         ".systems/scripts/smoke/common.sh"] + [f".systems/scripts/smoke/{g}.sh" for g in manifest["groups"]]
paths += [".systems/scripts/check-validation-observability", ".systems/scripts/check-validation-completion",
          ".systems/ai/core/validation-observability.md", ".systems/ai/core/commands.md", "README.md"]
changed = set(subprocess.check_output(["git", "diff", "--name-only"], text=True).splitlines())
changed |= set(subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"], text=True).splitlines())
assert changed == set(paths), (changed-set(paths), set(paths)-changed)
inventory = json.loads((project / "implementation/lv004-reference/inventory.json").read_text())
assert manifest["reference_test_ids"] == inventory["reference_test_ids"]
subprocess.run(["bash", ".systems/scripts/check-validator-smoke-tests", "--verify-manifest"], check=True)
for relative in paths:
    if relative.endswith(".sh") or Path(relative).name in ("check-validator-smoke-tests", "check-validation-observability", "check-validation-completion"):
        subprocess.run(["bash", "-n", relative], check=True)
with tempfile.TemporaryDirectory(prefix="lv004-pure-import-") as temporary:
    result = subprocess.run(["bash", "-eu", "-c", 'source "$1"; printf pure-import', "probe", str(smoke / "common.sh")],
                            cwd=temporary, text=True, capture_output=True)
    assert result.returncode == 0 and result.stdout == "pure-import" and not list(Path(temporary).iterdir()), result
hashes = {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in sorted(paths)}
doc = {"source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
       "paths_sha256": hashes, "source_digest": hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
       "approved_paths": len(paths), "reference_ids": len(manifest["reference_test_ids"]),
       "supplemental_ids": len(manifest["supplemental_test_ids"]), "ownership": dict(collections.Counter(manifest["test_groups"].values())),
       "outside_point_classification": dict(collections.Counter(r["classification"] for r in manifest["external_assertion_audit"])),
       "nested_python_assertions": len(manifest["nested_python_assertions"]), "frozen_regions": len(manifest["regions"]),
       "pure_import": "verified", "ci_updater_and_full_runner": "unchanged",
       "limits": "Structural supporting evidence; behavior, current source review and formal quality are separate."}
(project / "implementation/lv004-current-source-audit.json").write_text(json.dumps(doc, indent=2) + "\n")
print(json.dumps({k:v for k,v in doc.items() if k != "paths_sha256"}))
