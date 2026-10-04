#!/usr/bin/env python3
"""Immutable pre-review source inventories; recompute equivalence, never permission."""
import argparse
from functools import lru_cache
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent
PRODUCT = ('.systems', '.github', 'AGENTS.md', 'HUMANS.md', 'README.md', '.gitignore')
ROLES = {'spec-dod', 'owner-approval', 'implementation', 'review'}
CAPABILITY = 'phase-commit-policy-v1'
MARKER = 'full-qa-verification-v3'


@lru_cache(maxsize=None)
def load(name):
    spec = importlib.util.spec_from_file_location('binding_' + name.replace('-', '_'), HERE / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def fields(value, required, label):
    if not isinstance(value, dict) or set(value) != set(required):
        raise ValueError('invalid ' + label + ' fields')


def read(path):
    return load('execution-efficiency').read_json(path)


def git(root, *args):
    return subprocess.check_output(['git', '--no-replace-objects', '-C', str(root), *args], stderr=subprocess.PIPE)


def root_path(raw):
    path = load('execution-efficiency').canonical_path(raw).resolve(strict=True)
    if git(path, 'rev-parse', '--show-toplevel').decode().strip() != str(path):
        raise ValueError('source must be an explicit Git root')
    return path


def identity(root):
    common = git(root, 'rev-parse', '--path-format=absolute', '--git-common-dir').decode().strip()
    return {'path': str(root), 'git_common': str(Path(common).resolve(strict=True))}


def product_path(path, kind, exclusions):
    if any(path == e or path.startswith(e + '/') for e in exclusions):
        return False
    return kind == 'approved-target-source' or any(path == p or path.startswith(p + '/') for p in PRODUCT)


def data_path(path):
    parts = Path(path).parts
    return path.startswith('.systems/ai/skills/legacy/') or (
        path.startswith('.systems/ai/skills/') and 'context' in parts[4:])


def source_path(path):
    load('validation-scope').relative(path)
    qa = load('qa-evidence')
    if any(part.lower() in qa.FORBIDDEN_PARTS or part.lower().endswith(('.pem', '.key'))
           for part in Path(path).parts):
        raise ValueError('sensitive source input is not authorized')
    return path


def blob_hashes(root, objects):
    objects = list(dict.fromkeys(objects))
    payload = ('\n'.join(objects) + '\n').encode() if objects else b''
    result = subprocess.run(['git', '--no-replace-objects', '-C', str(root), 'cat-file', '--batch'],
                            input=payload, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout
    hashes, offset = {}, 0
    for oid in objects:
        end = result.find(b'\n', offset)
        actual, kind, size = result[offset:end].decode().split()
        if actual != oid or kind != 'blob':
            raise ValueError('invalid batch source object')
        offset = end + 1
        length = int(size)
        blob = result[offset:offset + length]
        offset += length
        if len(blob) != length or result[offset:offset + 1] != b'\n':
            raise ValueError('truncated batch source object')
        hashes[oid] = hashlib.sha256(blob).hexdigest()
        offset += 1
    if offset != len(result):
        raise ValueError('unexpected batch source object')
    return hashes


def selected_tree(root, revision, kind, exclusions):
    entries, objects = {}, {}
    for raw in git(root, 'ls-tree', '-r', '-z', revision).split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        path = name.decode('utf-8')
        if not product_path(path, kind, exclusions):
            continue
        mode, typ, oid = meta.decode().split()
        source_path(path)
        if mode not in {'100644', '100755'} or typ != 'blob':
            raise ValueError('unsupported source tree type: ' + path)
        objects[path] = oid
        entries[path] = {'mode': mode, 'type': 'data' if data_path(path) else 'source'}
    hashes = blob_hashes(root, objects.values())
    for path, oid in objects.items():
        entries[path]['sha256'] = hashes[oid]
    return entries


def selected_index(root, kind, exclusions):
    entries, objects = {}, {}
    for raw in git(root, 'ls-files', '--stage', '-z').split(b'\0'):
        if not raw:
            continue
        meta, name = raw.split(b'\t', 1)
        path = name.decode('utf-8')
        if not product_path(path, kind, exclusions):
            continue
        mode, oid, stage = meta.decode().split()
        source_path(path)
        if stage != '0' or mode not in {'100644', '100755'} or path in entries:
            raise ValueError('unmerged or unsafe source index')
        objects[path] = oid
        entries[path] = {'mode': mode, 'type': 'data' if data_path(path) else 'source'}
    hashes = blob_hashes(root, objects.values())
    for path, oid in objects.items():
        entries[path]['sha256'] = hashes[oid]
    return entries


def inventory(root, kind, baseline, exclusions):
    scope = load('validation-scope')
    base = selected_tree(root, baseline, kind, exclusions)
    head = git(root, 'rev-parse', 'HEAD').decode().strip()
    current = selected_tree(root, head, kind, exclusions)
    index = selected_index(root, kind, exclusions)
    names = set(base) | set(current) | set(index)
    for path in git(root, 'ls-files', '--others', '--exclude-standard', '-z').split(b'\0'):
        if path and product_path(path.decode(), kind, exclusions):
            names.add(path.decode())
    for path in git(root, 'ls-files', '--others', '--ignored', '--exclude-standard', '-z').split(b'\0'):
        if not path:
            continue
        name = path.decode()
        if product_path(name, kind, exclusions) and not ('__pycache__' in Path(name).parts and name.endswith('.pyc')):
            raise ValueError('unknown ignored source input: ' + name)
    live = {}
    for name in sorted(names):
        source_path(name)
        path = scope.contained(root, name, False)
        for parent in (path.parent, *path.parents):
            if parent == root:
                break
            if (parent / '.git').exists() or (parent / '.git').is_symlink():
                raise ValueError('nested source repository')
        if not path.exists():
            live[name] = {'type': 'deleted', 'mode': None, 'sha256': None}
            continue
        info = path.stat()
        if not stat.S_ISREG(info.st_mode):
            raise ValueError('nonregular source input')
        live[name] = {'type': 'data' if data_path(name) else 'source', 'permissions': stat.S_IMODE(info.st_mode),
                      'mode': '100755' if info.st_mode & 0o111 else '100644',
                      'sha256': scope.digest(path)}
    return {'baseline': base, 'tree': current, 'index': index, 'live': live, 'head': head}


def runtime_evidence(owner, entries):
    if not isinstance(entries, list) or len(entries) != len(ROLES):
        raise ValueError('all stable evidence roles are required')
    result, seen = [], set()
    scope = load('validation-scope')
    for entry in entries:
        fields(entry, {'role', 'path'}, 'stable evidence')
        role, raw = entry['role'], entry['path']
        if role not in ROLES or role in seen:
            raise ValueError('invalid or duplicate evidence role')
        seen.add(role)
        prefix = {'spec-dod': 'specs/', 'owner-approval': 'decisions/',
                  'implementation': 'implementation/', 'review': 'reviews/'}[role]
        if not raw.startswith(prefix) or not raw.endswith('.md'):
            raise ValueError('evidence has wrong role namespace')
        path = scope.contained(owner, raw)
        for parent in (path.parent, *path.parents):
            if parent == owner:
                break
            if (parent / '.git').exists() or (parent / '.git').is_symlink():
                raise ValueError('foreign runtime evidence')
        result.append({'role': role, 'path': raw, 'sha256': scope.digest(path)})
    return sorted(result, key=lambda e: e['role'])


def owning_root(workspace, project):
    scope = load('validation-scope')
    owner = scope.owned_root(workspace, 'projects/' + project)
    current = owner
    while current != workspace.parent:
        if (current / '.git').exists() or (current / '.git').is_symlink():
            raise ValueError('foreign repository in owning evidence namespace')
        if current == workspace:
            break
        current = current.parent
    return owner


def snapshot(workflow, workspace, project, task, evidence, dependencies=None, target=None,
             target_workspace=None, installed_workflow=None):
    scope, eff = load('validation-scope'), load('execution-efficiency')
    if not scope.SLUG.fullmatch(project) or not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)*', task):
        raise ValueError('invalid snapshot identity')
    workflow, workspace = root_path(workflow), eff.canonical_path(workspace).resolve(strict=True)
    owner = owning_root(workspace, project)
    roots = [('workflow-source', workflow, [])]
    if target is not None:
        target = root_path(target)
        if target == workflow or target_workspace is None or installed_workflow is None:
            raise ValueError('target needs distinct explicit typed exclusions')
        exclusions = [scope.relative(target_workspace), scope.relative(installed_workflow)]
        if exclusions[0] == exclusions[1] or any(e in {'.systems', '.github'} for e in exclusions):
            raise ValueError('invalid target exclusions')
        roots.append(('approved-target-source', target, exclusions))
    dependencies = dependencies or []
    if len(set(dependencies)) != len(dependencies):
        raise ValueError('duplicate dependency')
    for name in dependencies:
        scope.relative(name)
        if not product_path(name, 'workflow-source', []) or data_path(name):
            raise ValueError('dependency outside active source population')
    source = []
    for kind, root, exclusions in roots:
        head = git(root, 'rev-parse', 'HEAD').decode().strip()
        items = inventory(root, kind, head, exclusions)
        source.append({'kind': kind, 'identity': identity(root), 'head': head,
                       'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                       'exclusions': exclusions, 'population': items['live']})
    for name in dependencies:
        if source[0]['population'].get(name, {}).get('type') != 'source':
            raise ValueError('missing active dependency')
    return {'schema': 1, 'capability': CAPABILITY, 'project': project, 'task': task,
            'owner_root': str(owner), 'sources': source, 'dependencies': sorted(dependencies),
            'stable_evidence': runtime_evidence(owner, evidence),
            'environment': eff.environment_identity(),
            'required_checks': sorted(eff.read_json(HERE / 'validation-checks.json')['checks'])}


def capability(workflow):
    value = read(workflow / '.systems/ai/capabilities/phase-commit-policy-v1.json')
    fields(value, {'schema', 'capability', 'snapshot_schema', 'qa_contract', 'capture_schema', 'authority'}, 'capability')
    if any(type(value[k]) is not int for k in ('schema', 'snapshot_schema', 'capture_schema')) or value != {'schema': 1, 'capability': CAPABILITY, 'snapshot_schema': 1,
                 'qa_contract': MARKER, 'capture_schema': 3, 'authority': 'none'}:
        raise ValueError('unsupported installed binding capability')


def verify_snapshot(path, checksum, workflow, workspace, project, task, target=None):
    eff, scope = load('execution-efficiency'), load('validation-scope')
    path = eff.canonical_path(path)
    if eff.file_hash(path) != checksum:
        raise ValueError('snapshot checksum mismatch')
    value = read(path)
    fields(value, {'schema', 'capability', 'project', 'task', 'owner_root', 'sources', 'dependencies',
                   'stable_evidence', 'environment', 'required_checks'}, 'snapshot')
    if type(value['schema']) is not int or value['schema'] != 1 or value['capability'] != CAPABILITY:
        raise ValueError('unsupported snapshot schema')
    if value['project'] != project or value['task'] != task:
        raise ValueError('snapshot belongs to another task')
    workflow = root_path(workflow)
    owner = owning_root(eff.canonical_path(workspace).resolve(strict=True), project)
    if value['owner_root'] != str(owner):
        raise ValueError('snapshot owning root changed')
    capability(workflow)
    evidence = runtime_evidence(owner, [{'role': e['role'], 'path': e['path']} for e in value['stable_evidence']])
    if evidence != value['stable_evidence']:
        raise ValueError('stable artifact evidence changed')
    if value['environment'] != eff.environment_identity() or value['required_checks'] != sorted(eff.read_json(HERE / 'validation-checks.json')['checks']):
        raise ValueError('verification environment or check coverage changed')
    expected_kinds = ['workflow-source'] + (['approved-target-source'] if target is not None and root_path(target) != workflow else [])
    if not isinstance(value['sources'], list) or [s.get('kind') for s in value['sources']] != expected_kinds:
        raise ValueError('source roots missing or unexpectedly added')
    actual = []
    for item in value['sources']:
        fields(item, {'kind', 'identity', 'head', 'tree', 'exclusions', 'population'}, 'source root')
        if not all(isinstance(item[k], str) and re.fullmatch('[0-9a-f]{40}', item[k]) for k in ('head', 'tree')):
            raise ValueError('invalid actual source baseline')
        root = workflow if item['kind'] == 'workflow-source' else root_path(target)
        if identity(root) != item['identity']:
            raise ValueError('repository identity changed')
        if item['kind'] == 'workflow-source' and item['exclusions']:
            raise ValueError('workflow source exclusions are forbidden')
        if item['kind'] != 'workflow-source':
            # Existing receipts do not attest target-product checks. Never claim reuse.
            raise ValueError('target-product verification coverage unsupported; fresh target QA required')
        if git(root, 'rev-parse', item['head'] + '^{tree}').decode().strip() != item['tree']:
            raise ValueError('snapshot baseline tree mismatch')
        observed = inventory(root, item['kind'], item['head'], item['exclusions'])
        if observed['live'] != item['population']:
            raise ValueError('source population/modes/content changed')
        staged = git(root, 'diff', '--cached', '--name-only', '--no-renames', '-z').split(b'\0')
        if any(not product_path(name.decode(), item['kind'], []) for name in staged if name):
            raise ValueError('unrelated staged content')
        committed = observed['head'] != item['head']
        if committed:
            chain = git(root, 'rev-list', '--reverse', item['head'] + '..HEAD').decode().splitlines()
            if not chain:
                raise ValueError('unexpected commit ancestry')
            previous = item['head']
            for n, commit in enumerate(chain):
                header = git(root, 'cat-file', 'commit', commit).split(b'\n\n', 1)[0]
                parents = [line.removeprefix(b'parent ').decode()
                           for line in header.splitlines() if line.startswith(b'parent ')]
                if parents != [previous]:
                    raise ValueError('unexpected merge/rebase history')
                changed = git(root, 'diff-tree', '--no-commit-id', '--name-only', '-r', '-z', commit).split(b'\0')
                for name in (x.decode() for x in changed if x):
                    # No ambient workspace prefix grants commit scope or fresh closure.
                    if not product_path(name, item['kind'], []) or n > 0 or name not in item['population']:
                        raise ValueError('unexpected commit path; runtime chain requires fresh owned closure/QA')
                previous = commit
            expected = {k: {f: v[f] for f in ('type', 'mode', 'sha256')}
                        for k, v in item['population'].items() if v['type'] != 'deleted'}
            if observed['tree'] != expected or observed['index'] != expected:
                raise ValueError('commit tree/index differs from reviewed sources')
        actual.append({'kind': item['kind'], 'identity': identity(root), 'head': observed['head'],
                       'tree': git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                       'population_digest': digest(observed['live']), 'post_commit': committed})
    deps = value['dependencies']
    if not isinstance(deps, list) or deps != sorted(set(deps)):
        raise ValueError('invalid dependency inventory')
    for name in deps:
        if data_path(name) or value['sources'][0]['population'].get(name, {}).get('type') != 'source':
            raise ValueError('unbound dependency')
    return {'repositories': actual, 'population_digest': digest([s['population'] for s in value['sources']]),
            'stable_evidence': evidence, 'snapshot': value}


def assess_v3(report, workflow, workspace, project, target, expected_kind, expected_identity,
              schema_only, require_pass, document, verify_inputs, history_integrity, qa):
    if schema_only or history_integrity or not verify_inputs:
        raise ValueError('bound V3 is current-only; no legacy/historical fallback')
    text = report.read_text() if document is None else document
    markers = re.findall(r'^- QA verification contract: \x60([^\x60]+)\x60$', text, re.M)
    if markers != [MARKER] or '## Historical Runs' in text:
        raise ValueError('mixed QA wire versions')
    meta, sections = qa.read_current(text.splitlines())
    fields(meta, qa.REQUIRED | {'Source snapshot', 'Source snapshot SHA-256', 'Binding capability',
                              'Full source receipt', 'Full source receipt SHA-256'}, 'bound current QA')
    kind = meta['Artifact kind']
    if not kind.startswith('bound:') or kind[6:] not in qa.KINDS or meta['Binding capability'] != CAPABILITY:
        raise ValueError('unsupported bound QA kind/capability')
    if kind[6:] != 'implementation-quality':
        raise ValueError('V1 binding supports implementation quality only')
    identity_text = meta['Project/task identity']
    task = identity_text.removeprefix(project + ':')
    owner = Path(workspace).resolve(strict=True) / 'projects' / project
    snapshot_path = qa.contained(owner, meta['Source snapshot'])
    actual = verify_snapshot(snapshot_path, meta['Source snapshot SHA-256'], workflow, workspace, project, task, target)
    if actual['snapshot']['sources'][0]['head'] != meta['Assessed source HEAD']:
        raise ValueError('QA and snapshot baselines conflict')
    # Reuse semantic V2 validation in memory only after explicit V3 discrimination.
    ordinary = text.replace('`' + MARKER + '`', '`full-qa-verification-v2`')
    ordinary = ordinary.replace('- Artifact kind: ' + kind, '- Artifact kind: ' + kind[6:])
    assessed = qa.assess(report, workflow, workspace, project, target, expected_kind, expected_identity,
                         require_pass=require_pass, document=ordinary, _v3_normalized=True)
    current_inputs = {(k, p, h) for k, p, h in qa.input_rows(sections['Input Artifacts'])}
    for item in actual['stable_evidence']:
        if ('owning-project-evidence', item['path'], item['sha256']) not in current_inputs:
            raise ValueError('QA omits required stable evidence role')
    key = os.environ.get('AI_WORKFLOW_QA_BINDING_KEY_FILE')
    if not key:
        raise ValueError('explicit authenticated receipt key unavailable')
    receipt_path = qa.contained(owner, meta['Full source receipt'])
    eff = load('execution-efficiency')
    if eff.file_hash(receipt_path) != meta['Full source receipt SHA-256']:
        raise ValueError('bound source receipt changed')
    receipt = eff.verify_source(receipt_path, Path(key))
    if receipt['environment'] != actual['snapshot']['environment']:
        raise ValueError('receipt and snapshot environment differ')
    refreshed = qa.assess(report, workflow, workspace, project, target, expected_kind, expected_identity,
                          require_pass=require_pass, document=ordinary, _v3_normalized=True)
    if refreshed != assessed:
        raise ValueError('QA inputs changed during binding read')
    closing = verify_snapshot(snapshot_path, meta['Source snapshot SHA-256'], workflow, workspace, project, task, target)
    if closing != actual or eff.file_hash(receipt_path) != meta['Full source receipt SHA-256']:
        raise ValueError('source proof changed during binding read')
    if document is None and report.read_text() != text:
        raise ValueError('QA changed during binding read')
    return {**assessed, 'wire_version': 3, 'source_equivalence_verified': True,
            'binding': {'schema': 1, 'status': 'eligible', 'qa_hash': hashlib.sha256(text.encode()).hexdigest(),
                        'snapshot_hash': meta['Source snapshot SHA-256'], 'repositories': actual['repositories'],
                        'population_digest': actual['population_digest'],
                        'artifact_evidence_freshness': 'current', 'checked_at': datetime.now(timezone.utc).isoformat(),
                        'reasons': ['current semantic QA and independently derived equivalent sources'],
                        'authority': 'none'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    snap = sub.add_parser('snapshot')
    snap.add_argument('--workflow-root', required=True, type=Path)
    snap.add_argument('--workspace-root', required=True, type=Path)
    snap.add_argument('--project', required=True)
    snap.add_argument('--task', required=True)
    snap.add_argument('--evidence', required=True, type=Path)
    snap.add_argument('--output', required=True, type=Path)
    snap.add_argument('--key-file', required=True, type=Path)
    check = sub.add_parser('verify')
    check.add_argument('--report', required=True, type=Path)
    check.add_argument('--workflow-root', required=True, type=Path)
    check.add_argument('--workspace-root', required=True, type=Path)
    check.add_argument('--project', required=True)
    check.add_argument('--key-file', required=True, type=Path)
    args = parser.parse_args()
    try:
        eff = load('execution-efficiency')
        eff.key_bytes(args.key_file)
        expected_key = str(eff.canonical_path(args.key_file))
        if os.environ.get('AI_WORKFLOW_QA_BINDING_KEY_FILE') != expected_key:
            raise ValueError('declare AI_WORKFLOW_QA_BINDING_KEY_FILE before snapshot, receipt and verification')
        if args.action == 'snapshot':
            value = snapshot(args.workflow_root, args.workspace_root, args.project, args.task, read(args.evidence))
            load('execution-efficiency').publish(args.output, value)
            print(json.dumps({'schema': 1, 'snapshot_sha256': load('execution-efficiency').file_hash(args.output),
                              'path': str(args.output), 'authority': 'none'}, sort_keys=True))
        else:
            value = load('qa-evidence').assess(args.report, args.workflow_root, args.workspace_root,
                                             args.project, require_pass=True)
            if (value.get('wire_version') != 3 or value.get('source_equivalence_verified') is not True
                    or value.get('binding', {}).get('status') != 'eligible'):
                raise ValueError('explicit current V3 source binding proof required')
            print(json.dumps(value, sort_keys=True))
        return 0
    except (ValueError, OSError, TypeError, KeyError, subprocess.SubprocessError) as error:
        print('QA binding ineligible: ' + str(error), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
