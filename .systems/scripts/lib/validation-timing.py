#!/usr/bin/env python3
"""Write privacy-minimal, monotonic validation timing records."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import time


HEADER = (
    "command/check_id\tgroup\tduration_seconds\tresult\tprofile\t"
    "schema_version\trun_id\trecord_kind\tparent_id\n"
)
FIELD = re.compile(r"^[a-zA-Z0-9_.-]+$")


def safe_output(raw):
    path = Path(raw).expanduser().absolute()
    if path.exists() and not path.is_file():
        raise ValueError("timing output is not a regular file")
    if path.is_symlink():
        raise ValueError("timing output must not be a symlink")
    resolved = path.resolve()
    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", str(path)], check=False, capture_output=True
    )
    if tracked.returncode == 0:
        raise ValueError("timing output is tracked by git")
    ancestor = resolved.parent
    while not ancestor.exists():
        ancestor = ancestor.parent
    target_repository = subprocess.run(
        ["git", "-C", str(ancestor), "rev-parse", "--show-toplevel"],
        check=False, capture_output=True, text=True,
    )
    if target_repository.returncode == 0:
        target_tracked = subprocess.run(
            ["git", "-C", str(ancestor), "ls-files", "--error-unmatch", str(resolved)],
            check=False, capture_output=True,
        )
        if target_tracked.returncode == 0:
            raise ValueError("timing output is tracked by git")
    repository = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], check=False, capture_output=True, text=True
    )
    inside_repository = target_repository.returncode == 0 or (
        repository.returncode == 0 and resolved.is_relative_to(
            Path(repository.stdout.strip()).resolve()
        )
    )
    # Environment overrides cannot widen the output boundary into source folders.
    temporary_roots = {Path("/tmp").resolve(), Path("/var/tmp").resolve()}
    if sys.platform == "darwin":
        temporary_roots.add(Path("/var/folders").resolve())
    if not inside_repository and any(resolved.is_relative_to(root) for root in temporary_roots):
        return path
    workspace = Path.cwd() / "ai-workflow-workspace"
    if not resolved.is_relative_to(workspace.resolve()):
        raise ValueError("timing output must be under ignored workspace or tmp")
    check = subprocess.run(
        ["git", "check-ignore", "-q", str(path)], check=False, capture_output=True
    )
    if check.returncode != 0:
        raise ValueError("timing output is not ignored by git")
    return path


def field(value):
    if not FIELD.fullmatch(value):
        raise ValueError("timing metadata contains an unsafe field")
    return value


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("now")
    init = sub.add_parser("init")
    init.add_argument("path")
    record = sub.add_parser("record")
    record.add_argument("path")
    record.add_argument("run_id")
    record.add_argument("check_id")
    record.add_argument("group")
    record.add_argument("result")
    record.add_argument("profile")
    record.add_argument("record_kind")
    record.add_argument("parent_id")
    record.add_argument("start_ns", type=int)
    args = parser.parse_args()
    if args.action == "now":
        print(time.monotonic_ns())
        return
    path = safe_output(args.path)
    if args.action == "init":
        path.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        with os.fdopen(os.open(path, flags, 0o600), "w", encoding="utf-8") as out:
            out.write(HEADER)
        return
    values = [
        field(args.check_id), field(args.group), field(args.result),
        field(args.profile), field(args.run_id), field(args.record_kind),
        field(args.parent_id),
    ]
    if args.start_ns < 0 or args.start_ns > time.monotonic_ns():
        raise ValueError("invalid monotonic start")
    duration = (time.monotonic_ns() - args.start_ns) / 1_000_000_000
    with path.open("r", encoding="utf-8") as existing:
        first_line = existing.readline()
    if first_line != HEADER:
        raise ValueError("timing output has incompatible schema")
    row = (
        f"{values[0]}\t{values[1]}\t{duration:.6f}\t{values[2]}\t"
        f"{values[3]}\t2\t{values[4]}\t{values[5]}\t{values[6]}\n"
    )
    flags = os.O_WRONLY | os.O_APPEND
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    with os.fdopen(os.open(path, flags), "w", encoding="utf-8") as out:
        out.write(row)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, IndexError) as exc:
        print(f"Validation timing error: {exc}", file=sys.stderr)
        raise SystemExit(2)
