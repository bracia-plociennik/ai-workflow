#!/usr/bin/env python3
"""Read-only coordinator contract. Verified evidence is not execution permission."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import stat
import subprocess
import sys
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope, qa, capture = load('validation-scope'), load('qa-evidence'), load('capture-state')

CAPABILITY = '.systems/ai/capabilities/parallel-task-orchestration-v1.json'
PARALLEL_FILES = ('.systems/scripts/lib/parallel-orchestration.py',
                  '.systems/scripts/plan-parallel-work', '.systems/scripts/manage-parallel-run',
                  '.systems/ai/templates/orchestration/run.template.json',
                  '.systems/ai/templates/orchestration/unit.template.json',
                  '.systems/ai/templates/orchestration/result.template.json')
PARALLEL_MODES = ['serial', 'parallel-read-only', 'parallel-implementation']


def bounded_bytes(root, relative, limit):
    path = scope.contained(root, relative)
    fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        before = os.fstat(stream.fileno())
        if (not stat.S_ISREG(before.st_mode) or before.st_nlink != 1
                or not before.st_mode & 0o444 or before.st_size > limit):
            raise ValueError('unsafe capability input')
        raw = stream.read(limit + 1)
        after = os.fstat(stream.fileno())
        signature = lambda info: (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)
        if path.is_symlink() or len(raw) > limit or signature(before) != signature(after) or signature(after) != signature(path.stat()):
            raise ValueError('capability changed during read')
        return raw


def parallel_capability(workflow):
    """Installed protocol metadata never authenticates a worker backend."""
    unknown = {'state': 'unknown', 'reason': 'missing-invalid-or-unsupported-capability',
               'installed_protocol': None, 'native_backend_verification': 'unverified',
               'operational_support': False, 'owner_permission': 'not-assessed',
               'fallback': 'serial', 'execution_authorized': False, 'source_sha256': None}
    try:
        workflow = Path(workflow)
        if any(path.is_symlink() for path in (workflow, *workflow.parents)):
            raise ValueError('linked workflow')
        workflow = workflow.resolve(strict=True)
        raw = bounded_bytes(workflow, CAPABILITY, 32768)
        value = scope.strict_json(raw.decode('utf-8'))
        scope.fields(value, {'schema_version', 'feature', 'protocol_version', 'manifest_schema',
                            'unit_schema', 'result_schema', 'installed_modes', 'native_backend',
                            'fallback', 'execution_authorized', 'installed_sources_sha256'}, 'parallel capability')
        for key in ('schema_version', 'protocol_version', 'manifest_schema', 'unit_schema', 'result_schema'):
            if type(value[key]) is not int or value[key] != 1:
                raise ValueError('unsupported capability version')
        if (value['feature'] != 'parallel-task-orchestration-v1'
                or value['installed_modes'] != PARALLEL_MODES
                or value['fallback'] != 'serial' or value['execution_authorized'] is not False):
            raise ValueError('unsupported capability or authority')
        native = value['native_backend']
        scope.fields(native, {'verification', 'isolation', 'capacity', 'tested_backends'}, 'native backend')
        if native != {'verification': 'unverified', 'isolation': 'unknown', 'capacity': None, 'tested_backends': []}:
            raise ValueError('installed metadata cannot verify native backend')
        expected = value['installed_sources_sha256']
        scope.fields(expected, set(PARALLEL_FILES), 'installed source hashes')
        hashes = {}
        for path in PARALLEL_FILES:
            source = bounded_bytes(workflow, path, 2 * 1024 * 1024)
            digest = hashlib.sha256(source).hexdigest()
            if not isinstance(expected[path], str) or not re.fullmatch(r'[0-9a-f]{64}', expected[path]) or digest != expected[path]:
                raise ValueError('incompatible installed source')
            if path.endswith('.json'):
                template = scope.strict_json(source.decode('utf-8'))
                if not isinstance(template, dict) or type(template.get('schema')) is not int or template['schema'] != 1:
                    raise ValueError('incompatible installed template schema')
                if path.endswith('run.template.json'):
                    units = template.get('units')
                    if not isinstance(units, list) or not units or any(
                            not isinstance(unit, dict) or type(unit.get('schema')) is not int or unit['schema'] != 1 for unit in units):
                        raise ValueError('incompatible installed unit schema')
            hashes[path] = digest
        hashes[CAPABILITY] = hashlib.sha256(raw).hexdigest()
        return {**unknown, 'state': 'installed', 'reason': 'protocol-only-native-verification-deferred',
                'installed_protocol': {key: value[key] for key in
                                       ('protocol_version', 'manifest_schema', 'unit_schema', 'result_schema', 'installed_modes')},
                'source_sha256': hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()}
    except (ValueError, OSError, UnicodeError, TypeError, RecursionError):
        return unknown


def baseline(repo):
    head = scope.git(repo, 'rev-parse', 'HEAD').decode().strip()
    state = scope.git(repo, 'status', '--porcelain=v1', '-z')
    diff = scope.git(repo, 'diff', '--binary', 'HEAD')
    return {'head': head, 'worktree_sha256': hashlib.sha256(state + b'\0' + diff).hexdigest(), 'dirty': bool(state)}


def status(workflow, workspace, repo, project, schema_version=1):
    if type(schema_version) is not int or schema_version not in (1, 2):
        raise ValueError('unsupported coordinator schema')
    if workflow.is_symlink() or repo.is_symlink():
        raise ValueError('symlink repository identity')
    workflow, repo = workflow.resolve(strict=True), repo.resolve(strict=True)
    if Path(scope.git(repo, 'rev-parse', '--show-toplevel').decode().strip()).resolve() != repo:
        raise ValueError('ambiguous repository identity')
    if workspace.is_symlink():
        raise ValueError('symlink workspace')
    workspace = workspace.resolve(strict=True)
    owner = scope.owned_root(workspace, 'projects/' + project)
    before = baseline(repo)
    workflow_head = scope.git(workflow, 'rev-parse', 'HEAD').decode().strip()
    capability = parallel_capability(workflow) if schema_version == 2 else None
    source = scope.contained(owner, 'status.md')
    text = source.read_text()
    declared = {}
    for key, value in re.findall(r'^\|\s*`?([a-z-]+)`?\s*\|\s*([^|]+)\|', text, re.M):
        if key in declared:
            raise ValueError('duplicate project status field')
        declared[key] = value.strip('` ')
    if not declared:
        raise ValueError('missing declared project status')
    if declared.get('project', project) != project:
        raise ValueError('project status identity mismatch')
    phase = declared.get('current-phase', 'unknown')
    task = declared.get('current-task', '')
    names = {'phase-1-architecture-qa': 'phase-1-architecture-qa.md', 'phase-2-plan-qa': 'phase-2-plan-qa.md',
             'phase-8-final-check': 'phase-8-final-check.md'}
    if phase in {'phase-3-spec-qa', 'phase-5-quality'} and re.fullmatch(r'[A-Za-z0-9-]+', task):
        names[phase] = ('phase-3-' + task.lower() + '-spec-qa.md') if phase == 'phase-3-spec-qa' else ('phase-5-' + task.lower() + '-quality.md')
    verified, evidence, blockers = None, ['status.md'], []
    if phase in names:
        raw = 'quality/' + names[phase]
        evidence.append(raw)
        try:
            assessment = qa.assess(scope.contained(owner, raw), workflow, workspace, project, repo)
            if not assessment.get('source_equivalence_verified') and assessment['assessed_source_head'] != before['head']:
                raise ValueError('QA assessed source HEAD is stale')
            verified = assessment
        except (ValueError, OSError) as error:
            blockers.append('QA evidence unavailable or stale: ' + str(error))
    else:
        blockers.append('No recognized current formal QA route; declaration is not verified')
    captures = capture.inventory(workspace, workflow, repo, project)
    if captures['invalid']:
        blockers.append('Invalid capture evidence')
    after = baseline(repo)
    if before != after or source.read_text() != text:
        raise ValueError('baseline changed during coordinator read')
    if scope.git(workflow, 'rev-parse', 'HEAD').decode().strip() != workflow_head:
        raise ValueError('workflow version changed during coordinator read')
    if verified:
        reread = qa.assess(scope.contained(owner, evidence[-1]), workflow, workspace, project, repo)
        def stable_assessment(value):
            proof = dict(value)
            if 'binding' in proof:
                proof['binding'] = {k: v for k, v in proof['binding'].items() if k != 'checked_at'}
            return proof
        if stable_assessment(reread) != stable_assessment(verified):
            raise ValueError('QA inputs changed during coordinator read')
    if capture.inventory(workspace, workflow, repo, project) != captures:
        raise ValueError('capture evidence changed during coordinator read')
    if schema_version == 2 and parallel_capability(workflow) != capability:
        raise ValueError('capability changed during coordinator read')
    out = {'schema_version': 1, 'repository': str(repo), 'project': project,
            'workflow_version': workflow_head,
            'baseline': before, 'declared_status': declared, 'verified_qa': verified,
            'gate': 'verified-' + verified['verdict'].lower() if verified and not blockers else 'unknown',
            'blockers': blockers, 'evidence_paths': evidence, 'capture_inventory': captures,
            'freshness': 'current' if verified and not blockers else 'unknown', 'execution_authorized': False}
    if schema_version == 2:
        out.update(schema_version=2, parallel_capability=capability)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workflow', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--project', required=True)
    p.add_argument('--schema-version', type=int, choices=[1, 2], default=1)
    p.add_argument('--format', choices=['json', 'human'], default='json')
    a = p.parse_args()
    try:
        out = status(a.workflow, a.workspace, a.repo, a.project, a.schema_version)
        if a.format == 'json':
            print(json.dumps(out, sort_keys=True))
        else:
            print('Project: ' + out['project'] + '\nGate: ' + out['gate'] + '\nFreshness: ' + out['freshness'])
            print('Execution authorized: no\nBlockers: ' + ('; '.join(out['blockers']) or 'none'))
            if a.schema_version == 2:
                print('Parallel protocol: ' + out['parallel_capability']['state'] +
                      '\nNative backend: unverified; operational support: no; fallback: serial')
        return 0 if out['freshness'] == 'current' else 1
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'schema_version': a.schema_version, 'gate': 'unknown', 'freshness': 'unknown',
                          'error': str(error), 'execution_authorized': False}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
