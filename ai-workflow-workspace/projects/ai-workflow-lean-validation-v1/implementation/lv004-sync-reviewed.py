"""Copy only the reviewed source ceiling to the isolated source-only fixture."""
import hashlib
import json
from pathlib import Path
import shutil

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
audit = json.loads((project / "implementation/lv004-current-source-audit.json").read_text())
candidate = Path("/tmp/ai-workflow-lv004-cleanup-fixed/source")
for relative, expected in audit["paths_sha256"].items():
    assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected, relative
    shutil.copy2(root / relative, candidate / relative)
    assert hashlib.sha256((candidate / relative).read_bytes()).hexdigest() == expected, relative
print(json.dumps({"matched_paths": len(audit["paths_sha256"]), "source_digest": audit["source_digest"]}))
