#!/usr/bin/env python3
"""Verify reviewed workspace blobs without reading mutable worktree contents."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

PREFIX = "ai-workflow-workspace/"
REVIEW = PREFIX + "repo/publication-review.json"
SECRET = re.compile(
    rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|"
    rb"(?<![A-Za-z0-9_-])(?:ghp_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|"
    rb"sk-[A-Za-z0-9_-]{40,}|AKIA[A-Z0-9]{16})"
)
BLOCKED_PARTS = {".git", "node_modules", "__pycache__", ".pytest_cache", ".DS_Store"}
BLOCKED_SUFFIXES = {".pyc", ".pyo", ".key", ".pem", ".p12", ".pfx"}


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate review key")
        result[key] = value
    return result


def inventory(repo, ref=None):
    if ref:
        if ref.startswith("-"):
            raise ValueError("invalid committed-tree reference")
        ref = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{tree}").decode().strip()
    command = ("ls-tree", "-rz", ref, "--", "ai-workflow-workspace") if ref else (
        "ls-files", "--stage", "-z", "--", "ai-workflow-workspace")
    result = {}
    for row in git(repo, *command).split(b"\0"):
        if not row:
            continue
        meta, raw = row.split(b"\t", 1)
        if ref:
            mode, kind, object_id = meta.decode().split()
        else:
            mode, object_id, kind = meta.decode().split()
        path = raw.decode("utf-8", errors="strict")
        if (mode not in {"100644", "100755"} or (kind != "blob" if ref else kind != "0")
                or path in result):
            raise ValueError("non-regular, conflicted or duplicate workspace path: " + path)
        parts = PurePosixPath(path).parts
        if (not path.startswith(PREFIX) or ".." in parts or "\\" in path
                or any(part in BLOCKED_PARTS for part in parts)
                or PurePosixPath(path).suffix.lower() in BLOCKED_SUFFIXES
                or any(part == ".env" or part.startswith(".env.") for part in parts)
                or PurePosixPath(path).name in {"auth.json", "credentials.json"}):
            raise ValueError("forbidden workspace publication path: " + path)
        content = git(repo, "cat-file", "blob", object_id)
        if SECRET.search(content):
            raise ValueError("credential pattern in workspace blob: " + path)
        result[path] = content
    return result


def verify(repo, ref=None):
    files = inventory(repo, ref)
    if not files:
        print("Workspace publication: no tracked snapshot")
        return
    if REVIEW not in files:
        raise ValueError("missing workspace publication review")
    review = json.loads(files[REVIEW], object_pairs_hook=unique_keys)
    if (not isinstance(review, dict) or type(review.get("schema")) is not int or review.get("schema") != 1
            or review.get("privacy_review") != "completed"
            or not re.fullmatch(r"[0-9a-f]{40,64}", str(review.get("source_head", "")))
            or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(review.get("reviewed_at", "")))
            or review.get("quality_authority") != "supporting-only"):
        raise ValueError("invalid workspace publication review")
    expected = review.get("files")
    actual = {path: hashlib.sha256(body).hexdigest() for path, body in files.items() if path != REVIEW}
    if not isinstance(expected, dict) or expected != actual:
        raise ValueError("workspace publication inventory/hash mismatch; re-review changed files")
    print("Workspace publication: reviewed blobs=" + str(len(actual)) + "; supporting-only, not current QA PASS")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--ref", help="Verify a committed tree instead of the index")
    args = parser.parse_args()
    try:
        verify(args.repo.resolve(strict=True), args.ref)
    except (ValueError, OSError, subprocess.CalledProcessError, UnicodeError) as error:
        parser.exit(1, "Workspace publication violation: " + str(error) + "\n")


if __name__ == "__main__":
    main()
