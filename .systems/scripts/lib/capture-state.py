#!/usr/bin/env python3
"""Canonical capture inventory; historical completion is not current QA approval."""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope = load('validation-scope')
qa = load('qa-evidence')
shared = load('capture-record')


def references(workspace, owner, raw, legacy=False):
    return shared.references(workspace, owner, raw, scope, legacy)


def record(file, workspace, owner, workflow, repo, project):
    """Structural single-record API; gates must validate the owning collection."""
    return shared.record(file, workspace, owner, workflow, repo, project, scope, qa)


def collection(files, workspace, owner, workflow, repo, project):
    return shared.collection(files, workspace, owner, workflow, repo, project, scope, qa)
def inventory(workspace, workflow, repo, project=None):
    result = {'schema_version': 1, 'records': [], 'invalid': [], 'skipped': [], 'total': 0, 'unresolved': 0}
    if not workspace.exists():
        result['skipped'].append('workspace-absent')
        return result
    if workspace.is_symlink():
        raise ValueError('symlink workspace')
    workspace = workspace.resolve()
    if (workspace / '.git').exists() or (workspace / '.git').is_symlink():
        raise ValueError('foreign repository at workspace root')
    owners = []
    if project is not None:
        if not scope.SLUG.fullmatch(project):
            raise ValueError('unsafe project slug')
        owners = [('projects/' + project, project)]
    else:
        if (workspace / 'repo').exists():
            owners.append(('repo', None))
        projects = workspace / 'projects'
        if projects.is_symlink():
            raise ValueError('symlink projects namespace')
        if projects.exists():
            owners += [('projects/' + p.name, p.name) for p in sorted(projects.iterdir()) if p.is_dir() or p.is_symlink()]
    for raw, slug in owners:
        owner = scope.contained(workspace, raw, False)
        if (owner / '.git').exists() or (owner / '.git').is_symlink():
            result['skipped'].append(raw + ':foreign-repository')
            continue
        namespace = scope.contained(owner, 'capture-state', False)
        if not namespace.exists():
            continue
        if not namespace.is_dir():
            raise ValueError('invalid capture namespace')
        selected = collection(sorted(namespace.iterdir()), workspace, owner, workflow, repo, slug)
        for key in ('records', 'invalid'):
            result[key].extend(selected[key])
        for key in ('total', 'unresolved'):
            result[key] += selected[key]
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--workflow', type=Path, required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--project')
    a = p.parse_args()
    try:
        out = inventory(a.workspace, a.workflow, a.repo, a.project)
        print(json.dumps(out, sort_keys=True))
        return bool(out['invalid'])
    except (ValueError, OSError, UnicodeError) as error:
        print('Invalid canonical capture inventory: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
