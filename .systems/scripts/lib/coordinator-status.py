#!/usr/bin/env python3
"""Read-only coordinator contract. Verified evidence is not execution permission."""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


scope, qa, capture = load('validation-scope'), load('qa-evidence'), load('capture-state')


def baseline(repo):
    head = scope.git(repo, 'rev-parse', 'HEAD').decode().strip()
    state = scope.git(repo, 'status', '--porcelain=v1', '-z')
    diff = scope.git(repo, 'diff', '--binary', 'HEAD')
    return {'head': head, 'worktree_sha256': hashlib.sha256(state + b'\0' + diff).hexdigest(), 'dirty': bool(state)}


def status(workflow, workspace, repo, project):
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
            if assessment['assessed_source_head'] != before['head']:
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
    if verified and qa.assess(scope.contained(owner, evidence[-1]), workflow, workspace, project, repo) != verified:
        raise ValueError('QA inputs changed during coordinator read')
    if capture.inventory(workspace, workflow, repo, project) != captures:
        raise ValueError('capture evidence changed during coordinator read')
    return {'schema_version': 1, 'repository': str(repo), 'project': project,
            'workflow_version': workflow_head,
            'baseline': before, 'declared_status': declared, 'verified_qa': verified,
            'gate': 'verified-' + verified['verdict'].lower() if verified and not blockers else 'unknown',
            'blockers': blockers, 'evidence_paths': evidence, 'capture_inventory': captures,
            'freshness': 'current' if verified and not blockers else 'unknown', 'execution_authorized': False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--workflow', type=Path, required=True)
    p.add_argument('--workspace', type=Path, required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--project', required=True)
    p.add_argument('--schema-version', type=int, choices=[1], default=1)
    p.add_argument('--format', choices=['json', 'human'], default='json')
    a = p.parse_args()
    try:
        out = status(a.workflow, a.workspace, a.repo, a.project)
        if a.format == 'json':
            print(json.dumps(out, sort_keys=True))
        else:
            print('Project: ' + out['project'] + '\nGate: ' + out['gate'] + '\nFreshness: ' + out['freshness'])
            print('Execution authorized: no\nBlockers: ' + ('; '.join(out['blockers']) or 'none'))
        return 0 if out['freshness'] == 'current' else 1
    except (ValueError, OSError, UnicodeError, subprocess.CalledProcessError) as error:
        print(json.dumps({'schema_version': 1, 'gate': 'unknown', 'freshness': 'unknown',
                          'error': str(error), 'execution_authorized': False}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
