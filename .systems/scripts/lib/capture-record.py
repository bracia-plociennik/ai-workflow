"""Shared capture semantics; callers select populations and provide trusted adapters."""
import hashlib
import re


STATES = {'pending-quality', 'ready', 'completed', 'deferred', 'owner-skipped', 'blocked', 'not-applicable'}
REQUIRED = {'Work ID', 'Work mode', 'Project/repo scope', 'Source artifact', 'Quality artifact',
            'State', 'Distillation artifact', 'Last reminder', 'Owner disposition', 'Privacy/scope check', 'Residual risk'}


def pairs(text):
    return [(key.strip('` '), value.replace('`', '').strip())
            for key, value in re.findall(r'^- ([^:\n]+):\s*([^\n]+)$', text, re.M)]


def references(workspace, owner, raw, scope, legacy=False):
    if raw == 'none':
        return None
    raw = raw.strip('` ').split(';', 1)[0].strip('` ')
    if legacy and raw.startswith('ai-workflow-workspace/'):
        raw = raw[len('ai-workflow-workspace/'):]
        path = scope.contained(workspace, raw)
        if not path.is_relative_to(owner) and not (raw.startswith('micro-projects/') and path.name == 'micro-project.md'):
            raise ValueError('capture evidence outside owning namespace')
    else:
        path = scope.contained(owner, raw)
    boundary = workspace if legacy else owner
    for parent in (path.parent, *path.parents):
        if parent == boundary.parent:
            break
        if (parent / '.git').exists() or (parent / '.git').is_symlink():
            raise ValueError('foreign repository in capture evidence')
        if parent == boundary:
            break
    return path


def accepted_distillation(text, legacy):
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line == '## Distillation Gate']
    if starts:
        if len(starts) != 1:
            raise ValueError('duplicate distillation gate')
        start = starts[0] + 1
        end = next((i for i in range(start, len(lines)) if lines[i].startswith('## ')), len(lines))
        values = re.findall(r'^- Ready for checkpoint processing:\s*([^\n]+)$',
                            '\n'.join(lines[start:end]), re.M)
        return len(values) == 1 and re.fullmatch(r'`?yes`?(?:[;,][^\n]*)?', values[0].strip()) is not None
    values = re.findall(r'^- State after accepted distillation:\s*([^\n]+)$', text, re.M)
    return legacy and len(values) == 1 and values[0].strip('` ') == 'completed'


def record(file, workspace, owner, workflow, repo, project, scope, qa):
    values = {}
    for key, value in pairs(file.read_text()):
        if key in values:
            raise ValueError('duplicate capture field')
        values[key] = value
    if not REQUIRED <= values.keys() or any(re.search(r'<[^>]+>|\b(?:TODO|TBD)\b', values[k]) for k in REQUIRED):
        raise ValueError('incomplete capture record')
    state = values['State']
    if state not in STATES:
        raise ValueError('invalid capture state')
    version = values.get('Capture schema', '1')
    if version not in {'1', '2', '3'}:
        raise ValueError('unsupported capture schema')
    derived = values.get('is_distilled` derived value', values.get('is_distilled derived value'))
    if (derived is not None or version in {'2', '3'}) and derived != ('true' if state == 'completed' else 'false'):
        raise ValueError('capture derived boolean mismatch')
    sources = {key: references(workspace, owner, values[key], scope, version == '1')
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
        quality_text = sources['Quality artifact'].read_text()
        try:
            v3 = qa.wire_version(quality_text.splitlines()) == 3
        except ValueError:
            v3 = False
        if v3 != (version == '3'):
            raise ValueError('mixed capture/QA wire versions')
        if project and ('full-qa-verification-v2' in quality_text or v3):
            try:
                historical = version == '2' and qa.history_entry(sources['Quality artifact'], owner) is not None
                assessed = qa.assess(sources['Quality artifact'], workflow, workspace, project, repo,
                                     'implementation-quality', project + ':' + values['Work ID'],
                                     require_pass=not historical, history_integrity=historical)
                if assessed['verdict'] != 'PASS':
                    raise ValueError('capture requires passing QA')
                if not historical and not assessed.get('source_equivalence_verified') and assessed['assessed_source_head'] != scope.git(repo, 'rev-parse', 'HEAD').decode().strip():
                    raise ValueError('capture QA HEAD is stale')
                _, sections = qa.read_current(sources['Quality artifact'].read_text().splitlines())
                bound_sources = {scope.contained(owner, relative): checksum for kind, relative, checksum in
                                 qa.input_rows(sections['Input Artifacts']) if kind == 'owning-project-evidence'
                                 and relative == values['Source artifact']}
                if sources['Source artifact'] not in bound_sources:
                    raise ValueError('capture source is not bound to current QA')
                if historical and hashlib.sha256(sources['Source artifact'].read_bytes()).hexdigest() != bound_sources[sources['Source artifact']]:
                    raise ValueError('historical capture source integrity mismatch')
                verification = 'verified-historical' if historical else 'verified-current'
            except (ValueError, OSError):
                if version in {'2', '3'}:
                    raise ValueError('capture current QA invalid')
        elif version in {'2', '3'}:
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
        if not accepted_distillation(text, version == '1'):
            raise ValueError('capture distillation not accepted')
    return {'path': str(file.relative_to(workspace)), 'owner': str(owner.relative_to(workspace)),
            'work_id': values['Work ID'], 'state': state, 'is_distilled': state == 'completed',
            'quality_verification': verification, 'schema_version': int(version)}



def collection(files, workspace, owner, workflow, repo, project, scope, qa):
    """Validate all selected claims, including identities on invalid records."""
    result = {'records': [], 'invalid': [], 'total': len(files), 'unresolved': 0}
    claims, distillations = {}, {}
    for file in files:
        try:
            file = scope.contained(owner, str(file.relative_to(owner)))
            if file.suffix != '.md':
                raise ValueError('unknown capture record type')
            text = file.read_text()
            parsed = pairs(text)
            ids = [value for key, value in parsed if key == 'Work ID']
            for identity in set(ids):
                claims.setdefault(identity, []).append(file)
            # Resolve reuse claims even when another field makes a row invalid.
            refs = [value for key, value in parsed if key == 'Distillation artifact' and value != 'none']
            schemas = [value for key, value in parsed if key == 'Capture schema']
            legacy = not schemas or schemas == ['1']
            for raw in refs:
                path = references(workspace, owner, raw, scope, legacy)
                distillations.setdefault(path, []).append(file)
            result['records'].append(record(file, workspace, owner, workflow, repo, project, scope, qa))
        except (ValueError, OSError, UnicodeError) as error:
            result['invalid'].append({'path': str(file.relative_to(workspace)), 'reason': str(error)})
    duplicate_files = set()
    for label, groups in [('duplicate capture work ID', claims),
                          ('distillation artifact reused by multiple records', distillations)]:
        for paths in groups.values():
            if len(set(paths)) > 1:
                for file in set(paths):
                    duplicate_files.add(file)
                    result['invalid'].append({'path': str(file.relative_to(workspace)), 'reason': label})
    duplicate_names = {str(file.relative_to(workspace)) for file in duplicate_files}
    result['records'] = [row for row in result['records'] if row['path'] not in duplicate_names]
    result['unresolved'] = sum(row['state'] not in {'completed', 'owner-skipped', 'not-applicable'}
                              or row['quality_verification'].startswith('unknown')
                              for row in result['records'])
    return result
