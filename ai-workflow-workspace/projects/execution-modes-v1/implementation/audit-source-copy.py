"""Read-only source population comparison; not QA, approval or receipt authority."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

roots = [Path(value) for value in sys.argv[1:]]
if len(roots) != 2:
    raise SystemExit("Expected two source roots")

def inventory(root):
    names = subprocess.check_output(
        ["git", "-C", str(root), "ls-files", "-z"], text=True).split("\0")
    result = {}
    for name in filter(None, names):
        path = root / name
        if path.is_symlink() or not path.is_file():
            raise ValueError("Unsafe/missing source: " + name)
        result[name] = {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                       "mode": path.stat().st_mode & 0o777}
    return result

left, right = [inventory(root) for root in roots]
if left != right:
    raise SystemExit("Source populations differ")
print(json.dumps({"schema": 1, "result": "equal-bytes-modes-and-paths",
                  "authority": "supporting-only", "sources": left}, indent=2))
