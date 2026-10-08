#!/usr/bin/env python3
"""Local synthetic acceptance probes for the LV002 timing boundary."""

import importlib.machinery
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile


root = Path.cwd()
helper = root / ".systems/scripts/lib/validation-timing.py"
spec = importlib.util.spec_from_file_location("timing", helper)
timing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(timing)
loader = importlib.machinery.SourceFileLoader("comparison", str(root / ".systems/scripts/report-validation-comparison"))
comparison = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(comparison)


def reject(name, path, cwd, diagnostic, env=None):
    before = path.read_bytes() if path.exists() else None
    result = subprocess.run([sys.executable, str(helper), "init", str(path)], cwd=cwd, env=env, capture_output=True, text=True)
    assert result.returncode == 2, (name, result.returncode, result.stderr)
    assert diagnostic in result.stderr, (name, result.stderr)
    assert (path.read_bytes() if path.exists() else None) == before, name
    print(name + ": pass")


override = dict(os.environ, TMPDIR=str(root))
if sys.platform == "darwin":
    native_git = subprocess.check_output(["xcrun", "--find", "git"], text=True).strip()
    override["PATH"] = str(Path(native_git).parent) + os.pathsep + override["PATH"]
reject("tmpdir cannot approve tracked source", root / ".systems/scripts/check-validation-observability", root, "tracked by git", override)
reject("tmpdir cannot approve new source output", root / ".systems/scripts/lv002-probe-output.tsv", root, "must be under ignored workspace or tmp", override)
with tempfile.TemporaryDirectory(prefix="lv002-boundary-", dir="/tmp") as directory:
    temporary = Path(directory)
    repository = temporary / "repository"
    subprocess.run(["git", "init", "-q", str(repository)], check=True)
    tracked = repository / "tracked.tsv"
    tracked.write_text(timing.HEADER)
    subprocess.run(["git", "-C", str(repository), "add", "tracked.tsv"], check=True)
    reject("tracked output inside temporary repository", tracked, repository, "tracked by git")
    reject("foreign tracked output from official working directory", tracked, root, "tracked by git")
    tracked.unlink()
    reject("deleted tracked output is not recreated", tracked, repository, "tracked by git")
    reject("foreign deleted tracked output is not recreated", tracked, root, "tracked by git")
    reject("new unignored output inside temporary repository", repository / "new.tsv", repository, "must be under ignored workspace or tmp")
    reject("foreign unignored output from official working directory", repository / "new.tsv", root, "must be under ignored workspace or tmp")
    valid = temporary / "standalone.tsv"
    subprocess.run(["python3", str(helper), "init", str(valid)], cwd=root, check=True)
    assert valid.read_text() == timing.HEADER
    print("standalone platform temporary output: pass")
    legacy = temporary / "legacy.tsv"
    legacy.write_text("command/check_id\tgroup\tduration_seconds\tresult\tprofile\n")
    try:
        comparison.timing_rows(legacy)
    except ValueError as error:
        assert "incompatible timing schema" in str(error)
    else:
        raise AssertionError("legacy schema was silently consumed")
    print("legacy five-column schema explicitly rejected by v2 reader: pass")

print("LV002 targeted boundary probes: 10 pass")
