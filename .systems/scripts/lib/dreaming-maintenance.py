"""Bounded Workflow artifact maintenance; never rewrite historical QA."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import tempfile
import sys


def need(value, reason):
    if not value:
        raise ValueError(reason)


def owned(root, relative):
    root = Path(root)
    need(root.is_absolute() and root.resolve() == root, 'unsafe-root')
    rel = Path(relative)
    need(not rel.is_absolute() and rel.parts and '..' not in rel.parts, 'unsafe-relative-path')
    current = root
    for part in rel.parts:
        current /= part
        need(not current.is_symlink(), 'linked-path')
    need(current.resolve().is_relative_to(root), 'outside-owner')
    return current


def fingerprint(path):
    need(path.is_file() and not path.is_symlink() and path.stat().st_nlink == 1, 'unsafe-file')
    need(path.stat().st_size <= 4 * 1024 * 1024, 'oversized-artifact')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root, project):
    project = owned(root, project)
    need(project.is_dir(), 'missing-project')
    findings = []
    tasks = project / 'tasks.md'
    if tasks.exists():
        text = tasks.read_text()
        prefix = 'AI_WORKFLOW_WORKSPACE_HOME/'
        for reference in sorted(set(re.findall(r'AI_WORKFLOW_WORKSPACE_HOME/[^\s|`)>]+', text))):
            target = owned(root, reference[len(prefix):])
            if not target.is_file():
                findings.append({'kind': 'missing-reference', 'source': str(tasks.relative_to(root)),
                                 'reference': reference, 'disposition': 'needs-existing-target-or-explicit-gap'})
    quality = project / 'quality'
    qa_results = []
    if quality.is_dir():
        script = Path(__file__).with_name('qa-evidence.py')
        spec = importlib.util.spec_from_file_location('dreaming_qa_consumer', script)
        qa = importlib.util.module_from_spec(spec); sys.modules[spec.name] = qa; spec.loader.exec_module(qa)
        reports = sorted(quality.glob('*.md'))
        need(len(reports) <= 200, 'artifact-audit-needs-smaller-batch')
        for report in reports:
            owned(root, str(report.relative_to(root))); fingerprint(report)
            # Approval documents have their own consumer; never call them broken
            # Quality simply because they do not use the assessment wire format.
            if 'QA verification contract:' not in report.read_text():
                qa_results.append({'report': str(report.relative_to(root)), 'state': 'not-an-assessment'})
                continue
            try:
                result = qa.assess(report, Path(__file__).parents[3], Path(root), project.name,
                                   target_root=Path(root).parent, history_integrity=True)
                qa_results.append({'report': str(report.relative_to(root)),
                                   'state': result['lifecycle'], 'verdict': result['verdict'],
                                   'current_gate_eligible': result['current_gate_eligible']})
            except (ValueError, OSError) as error:
                findings.append({'kind': 'qa-not-current-or-invalid',
                                 'source': str(report.relative_to(root)), 'reason': str(error)[:240],
                                 'disposition': 'fresh-assessment-required-no-hash-replacement'})
    status = project / 'status.md'
    if status.exists():
        values = dict(re.findall(r'^\|\s*`?([a-z-]+)`?\s*\|\s*`?([^|`]*?)`?\s*\|', status.read_text(), re.M))
        phase, result, next_phase = (values.get(k, '').strip() for k in ('current-phase', 'phase-result', 'next-phase'))
        if result in {'in-progress', 'blocked', 'not-started'} and next_phase not in {phase, 'none', 'not-applicable'}:
            findings.append({'kind': 'inconsistent-current-transition', 'source': str(status.relative_to(root)),
                             'disposition': 'review-current-evidence-before-status-correction'})
    return {'project': str(project.relative_to(root)), 'findings': findings, 'quality': qa_results,
            'historical_quality_revalidated': False, 'execution_authorized': False}


def repair(root, request):
    need(set(request) == {'file', 'sha256', 'old', 'new', 'target'}, 'invalid-repair')
    file = owned(root, request['file'])
    need(file.name in {'tasks.md', 'links.md'}, 'historical-or-semantic-artifact-protected')
    need(not any(p in {'quality', 'reviews', 'checkpoints', 'decisions', 'capture-state'}
                 for p in Path(request['file']).parts), 'historical-evidence-protected')
    target = owned(root, request['target'])
    need(target.is_file(), 'missing-replacement-target')
    prefix = 'AI_WORKFLOW_WORKSPACE_HOME/'
    need(request['new'] == prefix + request['target'], 'replacement-must-be-existing-reference')
    need(request['old'].startswith(prefix) and request['old'] != request['new'], 'invalid-old-reference')
    old_target = owned(root, request['old'][len(prefix):])
    need(not old_target.exists(), 'existing-reference-not-repairable')
    original = file.read_bytes()
    if request['old'].encode() not in original and request['new'].encode() in original:
        return {'status': 'no-change', 'sha256': fingerprint(file)}
    need(fingerprint(file) == request['sha256'], 'artifact-changed')
    # Replace one complete Markdown/table token, never a substring of another path.
    pattern = re.compile(r'(?<![\w/.-])' + re.escape(request['old']) + r'(?=$|[\s|`)>])')
    updated, count = pattern.subn(lambda _: request['new'], original.decode())
    need(count > 0, 'reference-not-found')
    fd, name = tempfile.mkstemp(prefix='.maintenance-', dir=file.parent)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(updated.encode()); stream.flush(); os.fsync(stream.fileno())
        os.chmod(name, file.stat().st_mode & 0o777)
        need(fingerprint(file) == request['sha256'], 'artifact-changed')
        os.replace(name, file)
    finally:
        if os.path.exists(name): os.unlink(name)
    return {'status': 'executed', 'before_sha256': request['sha256'],
            'sha256': fingerprint(file), 'replacements': count}


def reconcile(root, project):
    """Repair path moves only: same owner, artifact family and exact basename.

    Zero or multiple current candidates remain explicit gaps. No prose guessing,
    title matching, cross-project substitution or historical report alteration.
    """
    directory = owned(root, project); results = []
    for name in ('tasks.md', 'links.md'):
        file = directory / name
        if not file.exists(): continue
        owned(root, str(file.relative_to(root))); fingerprint(file)
        references = sorted(set(re.findall(r'AI_WORKFLOW_WORKSPACE_HOME/[^\s|`)>]+', file.read_text())))
        for old in references:
            relative = old.removeprefix('AI_WORKFLOW_WORKSPACE_HOME/')
            target = owned(root, relative)
            if target.exists(): continue
            local = Path(relative)
            expected_prefix = Path(project)
            if not local.is_relative_to(expected_prefix):
                results.append({'reference': old, 'status': 'blocked', 'reason': 'foreign-project-reference'})
                continue
            parts = local.relative_to(expected_prefix).parts
            if not parts or parts[0] not in {'specs', 'quality'}:
                results.append({'reference': old, 'status': 'blocked', 'reason': 'unknown-artifact-family'})
                continue
            family = owned(root, str(expected_prefix / parts[0]))
            if not family.is_dir():
                results.append({'reference': old, 'status': 'blocked', 'reason': 'missing-artifact-family'})
                continue
            # Never select snapshots or archived evidence as the current router.
            candidates = [p for p in family.rglob(local.name)
                          if p.is_file() and not any(x in {'reviews','archive','backups','snapshots'}
                                                     for x in p.relative_to(family).parts)]
            if len(candidates) != 1:
                results.append({'reference': old, 'status': 'blocked', 'reason': 'missing-or-ambiguous-current-target'})
                continue
            replacement = str(candidates[0].relative_to(root))
            result = repair(root, {'file': str(file.relative_to(root)), 'sha256': fingerprint(file),
                                  'old': old, 'new': 'AI_WORKFLOW_WORKSPACE_HOME/' + replacement,
                                  'target': replacement})
            results.append({'reference': old, **result})
    return {'status': 'executed' if any(x['status'] == 'executed' for x in results) else 'no-change',
            'repairs': results, 'remaining': audit(root, project)['findings'],
            'semantic_quality_pass_implied': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['audit', 'repair', 'reconcile'])
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--project')
    parser.add_argument('--request')
    args = parser.parse_args()
    try:
        result = (audit(args.workspace, args.project) if args.action == 'audit'
                  else reconcile(args.workspace, args.project) if args.action == 'reconcile'
                  else repair(args.workspace, json.loads(Path(args.request).read_text())))
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    except (ValueError, OSError, TypeError) as error:
        parser.exit(1, 'Maintenance blocked: ' + str(error) + '\n')


if __name__ == '__main__': main()
