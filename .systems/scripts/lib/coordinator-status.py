#!/usr/bin/env python3
"""Read-only coordinator contract. Verified evidence is not execution permission."""
import argparse
import hashlib
import importlib.util
import json
import datetime
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


LEAD_ACTIONS = {'inspect', 'planning-artifacts', 'implementation', 'quality-assessment',
                'local-commit', 'publish', 'install-activate', 'external-effect'}
LEAD_FIELDS = {'schema_version', 'lead_id', 'lead_kind', 'owner_id', 'parent_work_id',
               'mandate_ref', 'mandate_revision', 'allowed_actions', 'resource_roots',
               'phase_ceiling', 'reserved_actions', 'escalation_target'}


def lead_path(raw):
    if not isinstance(raw, str) or not raw or any(ord(c) < 32 for c in raw):
        raise ValueError('invalid lead resource')
    path = Path(raw)
    if (not path.is_absolute() or '..' in path.parts or any(c in raw for c in '*?[]')
            or any(p.is_symlink() for p in (path, *path.parents))):
        raise ValueError('lead resource must be concrete absolute and unlinked')
    return path


def lead_phase(value):
    match = re.fullmatch(r'phase-([0-8])-[a-z]+(?:-[a-z]+)*', value or '')
    if not match:
        raise ValueError('unsupported lead phase')
    return int(match.group(1))


def inspect_work_lead(record, action='inspect', resource=None, phase='phase-0-repo-intake'):
    """Compare declared scope, never authenticate original consent or execute work.

    The executing agent independently checks the actual owner instruction and live
    revocation disposition. A matching projection cannot supply that verification.
    """
    scope.fields(record, {'work_lead', 'mandate_state', 'valid_until', 'context_binding',
                          'evidence_refs'}, 'work-lead projection')
    lead = record['work_lead']
    scope.fields(lead, LEAD_FIELDS, 'work_lead')
    if type(lead['schema_version']) is not int or lead['schema_version'] != 1:
        raise ValueError('unsupported work-lead version')
    if lead['lead_kind'] not in {'human', 'ai-system'}:
        raise ValueError('unsupported lead kind')
    for name in ('lead_id', 'owner_id', 'parent_work_id', 'mandate_ref', 'escalation_target'):
        if (not isinstance(lead[name], str) or not lead[name].strip()
                or any(ord(c) < 32 for c in lead[name])):
            raise ValueError('missing lead identity/evidence pointer')
    if type(lead['mandate_revision']) is not int or lead['mandate_revision'] < 1:
        raise ValueError('invalid mandate revision')
    actions, roots, reserved = lead['allowed_actions'], lead['resource_roots'], lead['reserved_actions']
    for values in (actions, roots, reserved, record['evidence_refs']):
        if (not isinstance(values, list) or any(not isinstance(x, str) or not x for x in values)
                or len(values) != len(set(values))):
            raise ValueError('invalid or duplicate lead list')
    if not actions or not roots or not set(actions) <= LEAD_ACTIONS:
        raise ValueError('unknown/empty lead scope')
    if any(any(ord(c) < 32 for c in x) or '*' in x for x in reserved):
        raise ValueError('invalid reservations')
    paths = [lead_path(x) for x in roots]
    target = lead_path(resource) if resource is not None else None
    ceiling, requested = lead_phase(lead['phase_ceiling']), lead_phase(phase)
    state, binding = record['mandate_state'], record['context_binding']
    if state not in {'issued', 'revoked', 'superseded', 'unknown'}:
        raise ValueError('unknown mandate disposition')
    if binding not in {'resolved', 'unbound', 'unavailable', 'conflict'}:
        raise ValueError('unknown context binding')
    expires = record['valid_until']
    expired = False
    if expires is not None:
        if not isinstance(expires, str):
            raise ValueError('invalid mandate expiry')
        timestamp = datetime.datetime.fromisoformat(expires)
        if timestamp.tzinfo is None:
            raise ValueError('expiry must include timezone')
        expired = timestamp <= datetime.datetime.now(datetime.timezone.utc)
    out = dict(lead_contract_version=1, context_binding=binding, scope_check='matched',
               authority_check='unknown', provenance_verified=False, execution_authorized=False,
               evidence_refs=list(record['evidence_refs']), actionable_blockers=[],
               next_allowed_action=action)
    reason = None
    if state != 'issued':
        out['authority_check'] = 'revoked' if state in {'revoked', 'superseded'} else 'unknown'
        reason = 'Mandate is not currently issued'
    elif expired:
        out['authority_check'] = 'expired'
        reason = 'Mandate expired'
    elif not record['evidence_refs']:
        out['authority_check'] = 'missing'
        reason = 'Original owner evidence references missing'
    elif binding != 'resolved':
        reason = 'Bound System context unavailable/conflicting; inspect only'
    elif (action not in actions or action in reserved or requested > ceiling
          or target is None or not any(target.is_relative_to(root) for root in paths)):
        out['authority_check'] = 'out-of-scope'
        reason = 'Requested action/resource/phase exceeds declared scope'
    if reason:
        out.update(scope_check='blocked', next_allowed_action='inspect', actionable_blockers=[reason])
    else:
        out['actionable_blockers'] = ['Executing agent must independently verify actual owner provenance/current disposition and phase gates']
    return out


def status(workflow, workspace, repo, project, schema_version=1, lead_record=None, requested_action="inspect", resource=None, requested_phase=None):
    if type(schema_version) is not int or schema_version not in (1, 2, 3):
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
    capability = parallel_capability(workflow) if schema_version in (2, 3) else None
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
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        import sprint_iteration
        sprint_iteration.project_guard(workspace, project, workflow)
    except (ValueError, OSError, KeyError) as error:
        verified = None
        blockers.append('Sprint closure unavailable: ' + str(error))
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
    if schema_version in (2, 3) and parallel_capability(workflow) != capability:
        raise ValueError('capability changed during coordinator read')
    out = {'schema_version': 1, 'repository': str(repo), 'project': project,
            'workflow_version': workflow_head,
            'baseline': before, 'declared_status': declared, 'verified_qa': verified,
            'gate': 'verified-' + verified['verdict'].lower() if verified and not blockers else 'unknown',
            'blockers': blockers, 'evidence_paths': evidence, 'capture_inventory': captures,
            'freshness': 'current' if verified and not blockers else 'unknown', 'execution_authorized': False}
    if schema_version in (2, 3):
        out.update(schema_version=schema_version, parallel_capability=capability)
    if schema_version == 3:
        if lead_record is None:
            lead = {'lead_contract_version': 1, 'context_binding': 'unbound',
                    'authority_check': 'missing', 'scope_check': 'unknown',
                    'provenance_verified': False, 'execution_authorized': False,
                    'actionable_blockers': ['No work-lead record selected; standalone owner instructions still govern'],
                    'evidence_refs': [], 'next_allowed_action': 'inspect'}
        else:
            path = scope.contained(owner, str(lead_record))
            raw = bounded_bytes(owner, str(path.relative_to(owner)), 65536)
            lead = inspect_work_lead(scope.strict_json(raw.decode('utf-8')), requested_action,
                                     resource or str(repo), requested_phase or phase)
            if raw != bounded_bytes(owner, str(path.relative_to(owner)), 65536):
                raise ValueError('lead record changed during inspection')
        out.update(lead, actual_gate=out['gate'])
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workflow', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--project', required=True)
    p.add_argument('--schema-version', type=int, choices=[1, 2, 3], default=1)
    p.add_argument('--format', choices=['json', 'human'], default='json')
    p.add_argument('--lead-record', help='owning-project relative JSON projection, schema3 only; never authenticates consent')
    p.add_argument('--requested-action', default='inspect')
    p.add_argument('--resource', help='absolute concrete requested resource; schema3 only')
    p.add_argument('--requested-phase', help='explicit requested phase, schema3 only')
    a = p.parse_args()
    try:
        if a.schema_version != 3 and (a.lead_record or a.resource or a.requested_phase or a.requested_action != 'inspect'):
            raise ValueError('work-lead options require explicit schema3')
        out = status(a.workflow, a.workspace, a.repo, a.project, a.schema_version, a.lead_record, a.requested_action, a.resource, a.requested_phase)
        if a.format == 'json':
            print(json.dumps(out, sort_keys=True))
        else:
            print('Project: ' + out['project'] + '\nGate: ' + out['gate'] + '\nFreshness: ' + out['freshness'])
            print('Execution authorized: no\nBlockers: ' + ('; '.join(out['blockers']) or 'none'))
            if a.schema_version in (2, 3):
                print('Parallel protocol: ' + out['parallel_capability']['state'] +
                      '\nNative backend: unverified; operational support: no; fallback: serial')
        return 0 if out['freshness'] == 'current' else 1
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'schema_version': a.schema_version, 'gate': 'unknown', 'freshness': 'unknown',
                          'error': str(error), 'execution_authorized': False}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
