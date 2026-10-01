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
STATES = {'pending-quality', 'ready', 'completed', 'deferred', 'owner-skipped', 'blocked', 'not-applicable'}
REQUIRED = {'Work ID', 'Work mode', 'Project/repo scope', 'Source artifact', 'Quality artifact',
            'State', 'Distillation artifact', 'Last reminder', 'Owner disposition', 'Privacy/scope check', 'Residual risk'}


def references(workspace, owner, raw, legacy=False):
    if raw == 'none':
        return None
    raw = raw.strip('` ').split(';', 1)[0].strip('` ')
    if legacy and raw.startswith('ai-workflow-workspace/'):
        raw = raw[len('ai-workflow-workspace/'):]
        path = scope.contained(workspace, raw)
        if not path.is_relative_to(owner) and not (raw.startswith('micro-projects/') and path.name == 'micro-project.md'):
            raise ValueError('capture evidence outside owning namespace')
        return path
    return scope.contained(owner, raw)


def record(file, workspace, owner, workflow, repo, project):
    values = {}
    for key, value in re.findall(r'^- ([^:\n]+):\s*([^\n]+)$', file.read_text(), re.M):
        key, value = key.strip('` '), value.replace('`', '').strip()
        if key in values:
            raise ValueError('duplicate capture field')
        values[key] = value
    if not REQUIRED <= values.keys() or any(re.search(r'<[^>]+>|\b(?:TODO|TBD)\b', values[k]) for k in REQUIRED):
        raise ValueError('incomplete capture record')
    state = values['State']
    if state not in STATES:
        raise ValueError('invalid capture state')
    version = values.get('Capture schema', '1')
    if version not in {'1', '2'}:
        raise ValueError('unsupported capture schema')
    derived = values.get('is_distilled` derived value', values.get('is_distilled derived value'))
    if (derived is not None or version == '2') and derived != ('true' if state == 'completed' else 'false'):
        raise ValueError('capture derived boolean mismatch')
    sources = {key: references(workspace, owner, values[key], version == '1')
               for key in ('Source artifact', 'Quality artifact', 'Distillation artifact')}
    verification = 'not-required'
    if state in {'ready', 'completed'}:
        if sources['Source artifact'] is None:
            raise ValueError('capture source missing')
        if not re.fullmatch(r'pass(?: for [^<>\n]+)?', values['Privacy/scope check']):
            raise ValueError('capture privacy not pass')
        if sources['Quality artifact'] is None:
            raise ValueError('capture quality missing')
        verification = 'unknown-historical-or-advisory'
        if project and 'full-qa-verification-v2' in sources['Quality artifact'].read_text():
            try:
                assessed = qa.assess(sources['Quality artifact'], workflow, workspace, project, repo,
                                     'implementation-quality', project + ':' + values['Work ID'], require_pass=True)
                if assessed['assessed_source_head'] != scope.git(repo, 'rev-parse', 'HEAD').decode().strip():
                    raise ValueError('capture QA HEAD is stale')
                verification = 'verified-current'
            except (ValueError, OSError):
                if version == '2':
                    raise ValueError('capture current QA invalid')
        elif version == '2':
            raise ValueError('capture schema 2 needs owning-project current QA')
    if state == 'completed':
        artifact = sources['Distillation artifact']
        if artifact is None or not artifact.is_relative_to(owner / 'distillations'):
            raise ValueError('completed capture lacks owned distillation')
        text = artifact.read_text()
        ids = [x.strip('` .') for x in re.findall(r'^- Task/package ID:\s*([^\n]+)$', text, re.M)]
        legacy_ids = [x.strip('` .') for x in re.findall(r'^- Work ID:\s*([^\n]+)$', text, re.M)]
        if ids != [values['Work ID']] and not (version == '1' and not ids and legacy_ids == [values['Work ID']]):
            raise ValueError('capture distillation identity mismatch')
        accepted = re.search(r'^## Distillation Gate\s*$', text, re.M) and re.search(r'^- Ready for checkpoint processing:\s*`?yes\b', text, re.M)
        legacy_accepted = version == '1' and re.search(r'^- State after accepted distillation:\s*`?completed\b', text, re.M)
        if not accepted and not legacy_accepted:
            raise ValueError('capture distillation not accepted')
    return {'path': str(file.relative_to(workspace)), 'owner': str(owner.relative_to(workspace)),
            'work_id': values['Work ID'], 'state': state, 'is_distilled': state == 'completed',
            'quality_verification': verification, 'schema_version': int(version)}


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
    identities, distilled_paths = set(), set()
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
        for file in sorted(namespace.iterdir()):
            result['total'] += 1
            try:
                file = scope.contained(owner, str(file.relative_to(owner)))
                if file.suffix != '.md':
                    raise ValueError('unknown capture record type')
                row = record(file, workspace, owner, workflow, repo, slug)
                identity = (raw, row['work_id'])
                if identity in identities:
                    raise ValueError('duplicate capture work ID')
                identities.add(identity)
                if row['state'] == 'completed':
                    vals = dict(re.findall(r'^- ([^:\n]+):\s*([^\n]+)$', file.read_text(), re.M))
                    path = references(workspace, owner, vals['Distillation artifact'], row['schema_version'] == 1)
                    if path in distilled_paths:
                        raise ValueError('distillation artifact reused by multiple records')
                    distilled_paths.add(path)
                result['records'].append(row)
                if row['state'] not in {'completed', 'owner-skipped', 'not-applicable'} or row['quality_verification'].startswith('unknown'):
                    result['unresolved'] += 1
            except (ValueError, OSError, UnicodeError) as error:
                result['invalid'].append({'path': str(file.relative_to(workspace)), 'reason': str(error)})
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
