#!/usr/bin/env python3
"""Copy selected tracked current-worktree product files into an empty fixture."""
import argparse
import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

spec = importlib.util.spec_from_file_location('scope', Path(__file__).with_name('validation-scope.py'))
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)
TOP = {'.systems', '.github', 'AGENTS.md', 'HUMANS.md', 'README.md', '.gitignore'}


def selected(raw):
    if raw.split('/')[0] not in TOP:
        return False
    scope.relative(raw)
    if '.git' in Path(raw).parts or Path(raw).suffix.lower() in {'.key', '.pem', '.p12', '.pfx'}:
        raise ValueError('sensitive fixture input')
    return not (raw.startswith('.systems/ai/skills/') and 'context' in Path(raw).parts)


def build(repo, destination, extras=()):
    repo = repo.resolve(strict=True)
    if Path(os.fsdecode(scope.git(repo, 'rev-parse', '--show-toplevel').strip())).resolve() != repo:
        raise ValueError('fixture source must be canonical Git root')
    if destination.is_symlink():
        raise ValueError('symlink fixture destination')
    destination = destination.resolve()
    if destination.is_relative_to(repo) or repo.is_relative_to(destination):
        raise ValueError('fixture destination overlaps source')
    if destination.exists() and (not destination.is_dir() or any(destination.iterdir())):
        raise ValueError('fixture destination must be empty')
    names = {os.fsdecode(x) for x in scope.git(repo, 'ls-files', '-z').split(b'\0') if x}
    for raw in extras:
        if not selected(raw) or raw.split('/')[0] not in {'.systems', '.github'}:
            raise ValueError('unsafe explicit fixture extra')
        scope.contained(repo, raw)
        if subprocess.run(['git', '-C', str(repo), 'check-ignore', '--quiet', '--', raw]).returncode == 0:
            raise ValueError('ignored fixture extra is not product source')
        names.add(raw)
    files = []
    for raw in sorted(names):
        if not selected(raw):
            continue
        path = scope.contained(repo, raw, False)
        if not path.exists():
            continue  # Preserve current tracked deletions instead of resurrecting HEAD blobs.
        if not path.is_file():
            raise ValueError('fixture input is not a regular file')
        scope.digest(path)
        files.append((raw, path))
    destination.mkdir(parents=True, exist_ok=True)
    for raw, path in files:
        target = destination / raw
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    return [raw for raw, _ in files]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--extra', action='append', default=[])
    a = p.parse_args()
    extras = a.extra + [x for x in os.environ.get('AI_WORKFLOW_SMOKE_EXTRA_FILES', '').split(':') if x]
    try:
        copied = build(a.repo, a.output, extras)
        print('Smoke fixture: selected current-worktree files=' + str(len(copied)))
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        p.exit(1, 'Invalid smoke fixture: ' + str(error) + '\n')


if __name__ == '__main__':
    main()
