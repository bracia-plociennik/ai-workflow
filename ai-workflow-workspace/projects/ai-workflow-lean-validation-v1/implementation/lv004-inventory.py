"""Freeze and inspect the exact predecessor runner before source partition."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

root = Path.cwd()
project = root / "ai-workflow-workspace/projects/ai-workflow-lean-validation-v1"
dest = project / "implementation/lv004-reference"
dest.mkdir(exist_ok=True)
source = root / ".systems/scripts/check-validator-smoke-tests"
data = source.read_bytes()
frozen = dest / "check-validator-smoke-tests.sh"
if frozen.exists() and frozen.read_bytes() != data:
    raise SystemExit("Refusing to replace a frozen reference")
frozen.write_bytes(data)
log = (project / "implementation/lv003-owner-approved-full.log").read_text()
ids = re.findall(r"AI_WORKFLOW_SMOKE_PROGRESS test=(\S+) status=started", log)
if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate reference smoke identity")
lines = data.decode().splitlines()
consumer_refs = []
for check in sorted((root / ".systems/scripts").glob("check-*")):
    if check.name == source.name or not check.is_file():
        continue
    for n, line in enumerate(check.read_text().splitlines(), 1):
        if "check-validator-smoke-tests" in line:
            consumer_refs.append({"file": str(check.relative_to(root)), "line": n, "text": line})
outside_assertions = [
    {"id": f"mono-line-{n:04d}", "source_line": n, "sha256": hashlib.sha256(line.encode()).hexdigest(), "text": line}
    for n, line in enumerate(lines, 1)
    if n >= 701 and (
        re.match(r"\s*(?:grep|test |if (?:kill|grep)|\[\[|if ! rg|if ! grep)", line)
        or ('exit 1' in line and not line.lstrip().startswith('#'))
    )
]
document = {
    "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "source_sha256": hashlib.sha256(data).hexdigest(),
    "reference_log_sha256": hashlib.sha256(log.encode()).hexdigest(),
    "reference_test_ids": ids,
    "consumer_references": consumer_refs,
    "candidate_external_assertion_lines": outside_assertions,
    "limits": [
        "Lexical assertion candidates require semantic classification; this is not an equivalence certificate.",
        "Dynamic IDs are taken from actual complete execution, not inferred from source text.",
        "No tracked source writes or split promotion are performed by this inventory.",
    ],
}
(dest / "inventory.json").write_text(json.dumps(document, indent=2) + "\n")
print(json.dumps({"reference_ids": len(ids), "assertion_candidates": len(outside_assertions), "consumer_refs": len(consumer_refs)}))
