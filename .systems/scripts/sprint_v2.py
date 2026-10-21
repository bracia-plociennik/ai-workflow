#!/usr/bin/env python3
"""Default Sprint: bounded targeted confidence, separate explicit full verification.

The caller verifies actual owner scope; state/CLI flags never authenticate consent.
"""
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import shutil
import subprocess
import time

import durable_runtime as runtime
import task_resource_cleanup as resources
import sprint_iteration as legacy

BUDGET = 300
STATES = {'iterating', 'paused', 'targeted', 'targeted-checked', 'targeted-incomplete',
          'targeted-failed', 'verifying', 'verified'}
FIELDS = legacy.FIELDS | {'cycles', 'full_request'}
FULL = {'uruchom phase 8', 'phase 8', 'run phase 8', 'uruchom pełną weryfikację',
        'run full verification', 'sprawdź całość'}


def now():
    return time.time()


def remaining(cycle):
    elapsed = now() - cycle['started_at']
    if elapsed < 0:
        raise ValueError('QA clock moved backwards; inspect budget before continuing')
    return max(0, BUDGET - elapsed)


def evidence(sprint, raw):
    path = runtime.unlinked(raw)
    owner = Path(sprint['workspace']) / 'projects' / sprint['project']
    if not path.is_relative_to(owner / 'reviews') or not path.is_file() or not path.read_text().strip():
        raise ValueError('nonempty current owning reviews evidence required')
    return {'path': str(path), 'sha256': legacy.digest(path)}


def validate(sprint, policy, record):
    legacy.fields(sprint, FIELDS, 'Sprint V2 state')
    if type(sprint['schema']) is not int or sprint['schema'] != 2 or sprint['state'] not in STATES:
        raise ValueError('unsupported Sprint V2 schema/state')
    # Reuse V1 path, source identity, acceptance and QA evidence validation.
    old = {k: v for k, v in sprint.items() if k in legacy.FIELDS}
    old['schema'] = 1
    old['state'] = sprint['state'] if sprint['state'] in legacy.STATES else 'iterating'
    legacy.validate_v1(old, policy, record)
    cycles = sprint['cycles']
    if not isinstance(cycles, list):
        raise ValueError('invalid Sprint cycles')
    seen = set()
    for cycle in cycles:
        legacy.fields(cycle, {'digest', 'started_at', 'finished_at', 'result', 'report', 'checks'}, 'targeted cycle')
        if not isinstance(cycle['digest'], str) or len(cycle['digest']) != 64 or cycle['digest'] in seen:
            raise ValueError('duplicate or invalid accepted source cycle')
        seen.add(cycle['digest'])
        if type(cycle['started_at']) not in {int, float} or not math.isfinite(cycle['started_at']) or cycle['started_at'] <= 0:
            raise ValueError('invalid QA budget start')
        if cycle['result'] not in {None, 'passed', 'failed', 'incomplete'} or not isinstance(cycle['checks'], list):
            raise ValueError('invalid targeted result')
        if cycle['finished_at'] is not None and (type(cycle['finished_at']) not in {int, float} or not math.isfinite(cycle['finished_at']) or cycle['finished_at'] < cycle['started_at']):
            raise ValueError('invalid QA completion time')
        if (cycle['result'] is None) != (cycle['finished_at'] is None):
            raise ValueError('incomplete targeted completion record')
        if cycle['report'] is not None:
            legacy.fields(cycle['report'], {'path', 'sha256'}, 'targeted report')
        for check in cycle['checks']:
            legacy.fields(check, {'exit_code', 'timed_out', 'log', 'sha256'}, 'targeted check')
            if type(check['exit_code']) is not int or type(check['timed_out']) is not bool:
                raise ValueError('invalid targeted check result')
            log = runtime.unlinked(check['log'])
            if not log.is_relative_to(Path(sprint['workspace'])/'projects'/sprint['project']/'evidence') or (check['exit_code'] != 125 and legacy.digest(log) != check['sha256']):
                raise ValueError('changed or foreign targeted check evidence')
    if sprint['state'].startswith('targeted'):
        if not cycles or sprint['verification_request'] is None:
            raise ValueError('targeted QA needs owner request and cycle')
        expected = {'targeted': None, 'targeted-checked': 'passed', 'targeted-incomplete': 'incomplete', 'targeted-failed': 'failed'}[sprint['state']]
        if cycles[-1]['result'] != expected:
            raise ValueError('targeted state/result mismatch')
        if expected is not None and cycles[-1]['report'] is None:
            raise ValueError('targeted result requires evidence')
    full = sprint['full_request']
    if full is not None:
        legacy.fields(full, {'message', 'owner_reference'}, 'full verification request')
        if full['message'].strip().casefold() not in FULL or not full['owner_reference']:
            raise ValueError('explicit scoped owner full-verification request required')
    if sprint['state'] in {'verifying', 'verified'} and full is None:
        raise ValueError('full QA cannot follow preview acceptance alone')


def inspect(record, workflow=None):
    _, _, sprint = legacy.read(record)
    current = legacy.population(sprint)
    stale = current != (sprint['verification_digest'] or (sprint['preview'] or {}).get('digest'))
    valid = False
    if sprint['state'] == 'verified' and not stale and workflow is not None:
        try:
            legacy.quality(sprint, workflow)
            valid = True
        except (ValueError, OSError, KeyError, subprocess.SubprocessError):
            pass
    cycle = sprint['cycles'][-1] if sprint['cycles'] else None
    report_valid = False
    if cycle and cycle['report']:
        try:
            report_valid = evidence(sprint, cycle['report']['path']) == cycle['report']
        except (ValueError, OSError):
            pass
    safe = (not stale and sprint['state'] == 'targeted-checked' and report_valid
            and cycle['result'] == 'passed' and all(c['exit_code'] == 0 and not c['timed_out'] for c in cycle['checks']))
    state = sprint['state']
    if stale and state != 'paused':
        state = 'iterating'
    elif state == 'verified' and not valid:
        state = 'verifying'
    return {'schema': 2, 'state': state, 'revision': sprint['revision'], 'preview': sprint['preview'],
            'source_changed': stale, 'deferred': not valid, 'closure_allowed': valid,
            'continuation_allowed': safe or valid, 'targeted_result': cycle['result'] if cycle else None,
            'remaining_seconds': remaining(cycle) if cycle and cycle['result'] is None else 0,
            'full_verification_requested': sprint['full_request'] is not None,
            'checks': legacy.CHECKS if state == 'verifying' else [], 'authority': 'none'}


def mutate(record, action, args):
    _, policy, _ = legacy.read(record)
    with resources.lock(policy):
        value, policy, sprint = legacy.read(record)
        revision = -1 if sprint is None else sprint['revision']
        if args.expected_revision != revision:
            raise ValueError('Sprint revision changed; inspect before retry')
        if action == 'start':
            if sprint is not None:
                raise ValueError('Sprint already exists')
            root = runtime.identity(args.source)
            if root['git_common'] != policy['canonical']['git_common']:
                raise ValueError('foreign source repository')
            production = None
            if args.environment == 'production':
                if not args.production_approval:
                    raise ValueError('production needs separate exact owner approval')
                production = runtime.read_json(args.production_approval)
            sprint = {'schema': 2, 'project': args.project, 'task': args.task, 'revision': 0,
                      'state': 'iterating', 'source': root, 'scope': args.scope, 'workspace': policy['workspace'],
                      'preview': None, 'verification_request': None, 'verification_digest': None,
                      'correction_review': None, 'quality': None, 'deferred_checks': legacy.CHECKS,
                      'production_approval': production, 'cycles': [], 'full_request': None}
            value['sprint_iteration'] = sprint
        elif sprint is None:
            raise ValueError('Sprint not active')
        elif action == 'preview':
            if sprint['state'] == 'paused' or not args.reference or not args.preview_id:
                raise ValueError('resume first; preview needs shown reference and ID')
            sprint.update(state='iterating', preview={'id': args.preview_id, 'digest': legacy.population(sprint), 'reference': args.reference},
                          verification_request=None, verification_digest=None, correction_review=None, quality=None, full_request=None)
        elif action in {'pause', 'resume'}:
            # Budget/requests/history survive; resume cannot trigger checks or renew allowance.
            sprint['state'] = ('paused' if action == 'pause' else
                               ('targeted' if sprint['cycles'] and sprint['cycles'][-1]['result'] is None
                                and sprint['verification_request'] is not None else 'iterating'))
        elif action in {'accept', 'request-verification'}:
            kind = 'accept' if action == 'accept' else 'verify'
            if sprint['state'] != 'iterating' or legacy.classify(args.message, args.origin) != kind or not args.owner_reference:
                raise ValueError('genuine current owner acceptance/request required')
            preview = sprint['preview']
            if preview is None or args.preview_id != preview['id'] or legacy.population(sprint) != preview['digest']:
                raise ValueError('current actually shown preview required')
            # A fingerprint can never create a second budget, even after a new preview ID or session.
            matching = next((c for c in sprint['cycles'] if c['digest'] == preview['digest']), None)
            if matching is not None:
                raise ValueError('accepted source already has a QA cycle; resume it without resetting budget')
            sprint['cycles'].append({'digest': preview['digest'], 'started_at': now(), 'finished_at': None,
                                     'result': None, 'report': None, 'checks': []})
            sprint.update(state='targeted', verification_request={'preview_id': preview['id'], 'digest': preview['digest'],
                          'kind': kind, 'message': args.message, 'owner_reference': args.owner_reference},
                          verification_digest=preview['digest'], correction_review=None, quality=None, full_request=None)
        elif action == 'qa-run':
            if sprint['state'] != 'targeted' or not args.command or legacy.population(sprint) != sprint['verification_digest']:
                raise ValueError('active current targeted cycle and reviewed command required')
            cycle = sprint['cycles'][-1]
            if any(c['exit_code'] == 125 for c in cycle['checks']):
                raise ValueError('interrupted check is unverified; preserve logs and record incomplete before further work')
            seconds = remaining(cycle)
            if seconds <= 0:
                raise ValueError('targeted QA budget exhausted; record incomplete, do not retry')
            folder = Path(sprint['workspace'])/'projects'/sprint['project']/'evidence'/'targeted'
            runtime.unlinked(folder, exists=False);folder.mkdir(parents=True, exist_ok=True)
            path = folder / ('cycle-' + str(len(sprint['cycles'])) + '-check-' + str(len(cycle['checks']) + 1) + '.log')
            timed_out = False
            with path.open('x') as output:
                # Reserve durable negative evidence BEFORE spawning. A killed parent cannot lose the attempt.
                cycle['checks'].append({'exit_code':125, 'timed_out':False, 'log':str(path), 'sha256':legacy.digest(path)})
                sprint['revision'] += 1
                resources.save(record, value)
                watchdog = shutil.which('timeout')
                if watchdog is None:
                    raise ValueError('independent timeout watchdog unavailable; targeted command not started')
                process = subprocess.Popen([watchdog, '--signal=TERM', '--kill-after=2s', str(max(.001, remaining(cycle)))+'s', *args.command], cwd=sprint['source']['root'], stdin=subprocess.DEVNULL,
                                           stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
                try:
                    exit_code = process.wait(timeout=max(.001, remaining(cycle)) + 3)
                    timed_out = exit_code in {124, 137}
                except (subprocess.TimeoutExpired, KeyboardInterrupt):
                    timed_out = True
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL);process.wait()
                    exit_code = 124
            cycle['checks'][-1] = {'exit_code': exit_code, 'timed_out': timed_out, 'log': str(path), 'sha256': legacy.digest(path)}
        elif action == 'complete-targeted':
            if sprint['state'] != 'targeted' or legacy.population(sprint) != sprint['verification_digest']:
                raise ValueError('current targeted verification required')
            cycle = sprint['cycles'][-1]
            result = args.result
            if result not in {'passed', 'failed', 'incomplete'}:
                raise ValueError('explicit targeted outcome required')
            if result == 'passed' and (remaining(cycle) <= 0 or any(c['exit_code'] != 0 or c['timed_out'] for c in cycle['checks'])):
                raise ValueError('exhausted/failed QA cannot be reported as passed')
            cycle.update(result=result, finished_at=now(), report=evidence(sprint, args.report))
            sprint['state'] = {'passed': 'targeted-checked', 'failed': 'targeted-failed', 'incomplete': 'targeted-incomplete'}[result]
        elif action == 'request-full-verification':
            if args.origin != 'owner' or not args.owner_reference or args.message.strip().casefold() not in FULL:
                raise ValueError('explicit scoped owner Phase 8/full verification request required')
            if sprint['verification_request'] is None or legacy.population(sprint) != sprint['verification_digest']:
                raise ValueError('current accepted/explicitly requested source required before full verification')
            sprint.update(state='verifying', full_request={'message': args.message, 'owner_reference': args.owner_reference}, quality=None)
        elif action == 'refresh-verification':
            if sprint['state'] not in {'targeted', 'verifying'} or sprint['verification_request'] is None:
                raise ValueError('prior verification request required')
            review = evidence(sprint, args.correction_review)
            sprint.update(verification_digest=legacy.population(sprint), correction_review=review, quality=None)
        elif action == 'complete':
            if sprint['state'] != 'verifying' or sprint['full_request'] is None or legacy.population(sprint) != sprint['verification_digest']:
                raise ValueError('explicit full verification with fresh QA required')
            report = runtime.unlinked(args.report)
            if not report.is_relative_to(Path(sprint['workspace'])/'projects'/sprint['project']/'quality'):
                raise ValueError('full QA must come from owning quality reports, not targeted reviews')
            sprint['quality'] = {'report': str(report), 'sha256': legacy.digest(args.report), 'digest': legacy.population(sprint)}
            legacy.quality(sprint, args.workflow_root)
            sprint['state'] = 'verified'
        else:
            raise ValueError('unsupported Sprint V2 operation')
        if action != 'start':
            sprint['revision'] += 1
        validate(sprint, policy, record)
        resources.save(record, value)
    return inspect(record, args.workflow_root)
