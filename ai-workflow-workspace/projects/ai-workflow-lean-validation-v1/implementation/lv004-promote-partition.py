"""Mechanical promotion of the reviewed literal partition, not its verdict."""
import hashlib
import json
from pathlib import Path
import shutil

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
candidate = Path("/tmp/ai-workflow-lv004-cleanup-fixed/source")
inventory = json.loads((project / "implementation/lv004-reference/inventory.json").read_text())
current = root / ".systems/scripts/check-validator-smoke-tests"
if hashlib.sha256(current.read_bytes()).hexdigest() != inventory["source_sha256"]:
    raise SystemExit("Public source drifted since accepted frozen reference")
proof = json.loads((project / "implementation/lv004-equivalence-retest/equivalence-results.json").read_text())
mutations = json.loads((project / "implementation/lv004-protected-mutations/results.json").read_text())
if proof["result"] != "pass" or mutations["result"] != "pass":
    raise SystemExit("Equivalence/mutation proof missing")
manifest = json.loads((candidate / ".systems/scripts/smoke/manifest.json").read_text())
if manifest["reference_test_ids"] != inventory["reference_test_ids"]:
    raise SystemExit("Frozen ID inventory changed")
paths = [".systems/scripts/check-validator-smoke-tests", ".systems/scripts/smoke/manifest.json",
         ".systems/scripts/smoke/common.sh"] + [f".systems/scripts/smoke/{g}.sh" for g in manifest["groups"]]
for relative in paths:
    target = root / relative
    target.parent.mkdir(exist_ok=True)
    shutil.copy2(candidate / relative, target)
print(json.dumps({"promoted_paths": paths, "reference_ids": len(manifest["reference_test_ids"]),
                  "supplemental_ids": len(manifest["supplemental_test_ids"]),
                  "quality": "pending fresh current-diff semantic review and full verification"}))
