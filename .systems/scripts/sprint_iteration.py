#!/usr/bin/env python3
"""Task-local Sprint transitions. State and text never authenticate owner consent."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
import unicodedata

import durable_runtime as runtime
import task_resource_cleanup as resources

SCHEMA = 1
STATES = {'iterating', 'paused', 'verifying', 'verified'}
FIELDS = {'schema','project','task','revision','state','source','scope','workspace','preview',
          'verification_request','verification_digest','correction_review','quality','deferred_checks','production_approval'}
CHECKS = ['tests','lint','typecheck','verification-build','full-diff-review','applicable-validators']
ACCEPT = {'podoba mi się, to finalna wersja','działa, tak zostawiamy',
          'akceptuję finalny efekt','to finalna wersja','this is the final version','accept the final result'}
VERIFY = {'testuj teraz','sprawdź całość','run tests now','verify now'}


def classify(message, origin):
    if origin != 'owner' or not isinstance(message,str):
        return 'continue'
    message = unicodedata.normalize('NFC',message).strip().lower().rstrip('.!')
    if message in ACCEPT: return 'accept'
    if message in VERIFY: return 'verify'
    return 'continue'


def digest(path):
    return resources.digest(runtime.unlinked(path))


def fields(value, names, label):
    if not isinstance(value,dict) or set(value)!=set(names):
        raise ValueError('unsupported '+label)


def read(record):
    value, policy = resources.load(runtime.unlinked(record))
    if policy is None: raise ValueError('Sprint requires the existing durable owning work record')
    sprint = value.get('sprint_iteration')
    if sprint is None: return value,policy,None
    validate(sprint,policy,record)
    return value,policy,sprint


def validate(sprint,policy,record):
    fields(sprint,FIELDS,'Sprint state')
    if type(sprint['schema']) is not int or sprint['schema']!=SCHEMA or sprint['state'] not in STATES:
        raise ValueError('unsupported Sprint schema/state')
    if type(sprint['revision']) is not int or sprint['revision']<0:
        raise ValueError('invalid Sprint revision')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',sprint['project']) or not re.fullmatch(r'[A-Z][A-Z0-9]*(?:-[A-Za-z0-9]+)*',sprint['task']):
        raise ValueError('invalid owning project/task')
    if sprint['source']!=runtime.identity(sprint['source']['root']) or sprint['source']['git_common']!=policy['canonical']['git_common']:
        raise ValueError('Sprint source identity changed')
    if sprint['workspace']!=policy['workspace'] or not Path(record).is_relative_to(Path(policy['workspace'])/'projects'/sprint['project']):
        raise ValueError('Sprint belongs to another owning project/runtime')
    if not isinstance(sprint['deferred_checks'],list) or sprint['deferred_checks']!=CHECKS:
        raise ValueError('unknown deferred check set')
    if sprint['production_approval'] is not None:
        fields(sprint['production_approval'],{'target','scope','rollback','owner_reference'},'production approval')
        if any(not isinstance(v,str) or not v.strip() for v in sprint['production_approval'].values()):
            raise ValueError('production needs exact separate target/scope/rollback/owner reference')
    population(sprint) # Validate complete declared preview source paths, including live identity.
    preview=sprint['preview']
    if preview is not None:
        fields(preview,{'id','digest','reference'},'preview')
        if any(not isinstance(preview[k],str) or not preview[k] for k in preview):raise ValueError('invalid preview')
        if not re.fullmatch(r'[0-9a-f]{64}',preview['digest']):raise ValueError('invalid preview source fingerprint')
    request=sprint['verification_request']
    if request is not None:
        fields(request,{'preview_id','digest','kind','message','owner_reference'},'verification request')
        if request['kind'] not in {'accept','verify'} or classify(request['message'],'owner')!=request['kind'] or not request['owner_reference']:
            raise ValueError('invalid verification request')
        if preview is None or request['preview_id']!=preview['id'] or request['digest']!=preview['digest']:
            raise ValueError('verification request refers to a different preview')
    if sprint['state'] in {'verifying','verified'} and request is None:raise ValueError('missing verification request')
    if sprint['state'] in {'verifying','verified'} and not re.fullmatch(r'[0-9a-f]{64}',sprint['verification_digest'] or ''):
        raise ValueError('missing verification source identity')
    correction=sprint['correction_review']
    if correction is not None:
        fields(correction,{'path','sha256'},'correction review')
        path=runtime.unlinked(correction['path'])
        if not path.is_relative_to(Path(sprint['workspace'])/'projects'/sprint['project']/'reviews') or digest(path)!=correction['sha256']:
            raise ValueError('correction review changed or belongs to another project')
    if sprint['verification_request'] is not None and sprint['verification_digest']!=sprint['verification_request']['digest'] and correction is None:
        raise ValueError('changed verification source needs semantic correction review')
    if sprint['quality'] is not None:
        fields(sprint['quality'],{'report','sha256','digest'},'quality reference')
    if sprint['state']=='verified' and sprint['quality'] is None:raise ValueError('missing Quality evidence')


def population(sprint):
    root=runtime.unlinked(sprint['source']['root'])
    selected=sprint['scope']
    if not isinstance(selected,list) or not selected or len(set(selected))!=len(selected):raise ValueError('empty/duplicate source scope')
    entries={}
    paths=[]
    for rel in selected:
        if not isinstance(rel,str) or not rel or '\\' in rel or any(part in {'','.','..','.git','__pycache__'} for part in rel.split('/')) or Path(rel).is_absolute():
            raise ValueError('unsafe preview source scope')
        path=runtime.unlinked(root/rel,exists=False)
        if not path.is_relative_to(root):raise ValueError('foreign preview source')
        if any(path==p or path.is_relative_to(p) or p.is_relative_to(path) for p in paths):raise ValueError('overlapping source scopes')
        paths.append(path)
        if not path.exists():entries[rel]=['absent'];continue
        inputs=[path]+(list(path.rglob('*')) if path.is_dir() else [])
        for item in sorted(inputs):
            if '__pycache__' in item.parts:continue
            runtime.unlinked(item)
            name=item.relative_to(root).as_posix()
            if item.name.startswith('.env') or item.suffix.lower() in {'.pem','.key'}:raise ValueError('secret-like preview input requires separate scope')
            st=item.stat()
            if item.is_dir():entries[name]=['dir',stat.S_IMODE(st.st_mode)]
            elif item.is_file() and st.st_nlink==1:entries[name]=['file',stat.S_IMODE(st.st_mode),digest(item)]
            else:raise ValueError('special or hardlinked preview input')
    return hashlib.sha256(json.dumps(entries,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def quality(sprint, workflow):
    q=sprint['quality']
    if q is None or q['digest']!=population(sprint):raise ValueError('missing/stale Sprint quality')
    report=runtime.unlinked(q['report'])
    if digest(report)!=q['sha256']:raise ValueError('Sprint Quality report changed')
    spec=importlib.util.spec_from_file_location('sprint_qa',Path(workflow)/'.systems/scripts/lib/qa-evidence.py')
    qa=importlib.util.module_from_spec(spec);sys.modules[spec.name]=qa;spec.loader.exec_module(qa)
    assessed = qa.assess(report,Path(workflow),Path(sprint['workspace']),sprint['project'],Path(sprint['source']['root']),
                     expected_kind='implementation-quality', expected_identity=sprint['project']+':'+sprint['task'],require_pass=True)
    # Existing V2 targets bind the actual target HEAD; V3 has its own equivalence proof.
    if not assessed.get('source_equivalence_verified') and assessed['assessed_source_head'] != resources.git(sprint['source']['root'],'rev-parse','HEAD'):
        raise ValueError('Quality assessed target HEAD is stale')
    return assessed


def inspect(record, workflow=None):
    _,_,sprint=read(record)
    if sprint is None:return {'schema':1,'state':'inactive','deferred':False,'closure_allowed':True,'authority':'none'}
    current=population(sprint)
    basis=sprint['verification_digest'] if sprint['state'] in {'verifying','verified'} else (sprint['preview'] or {}).get('digest')
    stale=basis!=current
    valid=False
    if sprint['state']=='verified' and not stale and workflow is not None:
        try:quality(sprint,workflow);valid=True
        except (ValueError,OSError,KeyError,subprocess.SubprocessError):pass
    state='iterating' if stale and sprint['state'] in {'verifying','verified'} else sprint['state']
    if state=='verified' and not valid:state='verifying'
    return {'schema':1,'state':state,'revision':sprint['revision'],'preview':sprint['preview'],
            'source_changed':stale,'deferred':state in {'iterating','paused'},'closure_allowed':valid,
            'checks':([] if state in {'iterating','paused'} else CHECKS), 'authority':'none'}


def guard_record(record, workflow=None):
    # Admission to closure/release always recomputes proof, never trusts stored verified.
    view=inspect(record,workflow)
    if not view['closure_allowed']:raise ValueError('Sprint has pending/stale Quality; preserve work and resources')


def project_guard(workspace, project, workflow, *, generating=False, task=None):
    owner=Path(workspace)/'projects'/project
    for record in owner.rglob('*.json'):
        # Read only owning project metadata, not arbitrary source/dumps/archived reports.
        if any(part in {'evidence','quality','context','reviews','decisions'} for part in record.relative_to(owner).parts):continue
        value=runtime.read_json(record)
        if isinstance(value,dict) and 'sprint_iteration' in value:
            _,_,sprint=read(record)
            if task is not None and sprint['task']!=task:continue
            if generating:
                if sprint['state'] not in {'verifying','verified'} or population(sprint)!=sprint['verification_digest']:
                    raise ValueError('Sprint implementation QA is deferred until owner accepts current preview or requests verification')
            else:guard_record(record,workflow)


def mutate(record,action,args):
    value,policy,sprint=read(record)
    with resources.lock(policy):
        value,policy,sprint=read(record)
        revision=-1 if sprint is None else sprint['revision']
        if args.expected_revision!=revision:raise ValueError('Sprint revision changed; inspect before retry')
        if action=='start':
            if sprint is not None:raise ValueError('Sprint already exists; inspect/resume owning task')
            root=runtime.identity(args.source)
            if root['git_common']!=policy['canonical']['git_common']:raise ValueError('source belongs to foreign repository')
            production=None
            if args.environment=='production':
                if not args.production_approval:raise ValueError('production requires separate exact owner approval')
                production=runtime.read_json(args.production_approval)
            sprint={'schema':1,'project':args.project,'task':args.task,'revision':0,'state':'iterating','source':root,
                    'scope':args.scope,'workspace':policy['workspace'],'preview':None,'verification_request':None,
                    'quality':None,'verification_digest':None,'correction_review':None,'deferred_checks':CHECKS,'production_approval':production}
            value['sprint_iteration']=sprint
        elif sprint is None:raise ValueError('Sprint not active')
        elif action=='preview':
            if not args.reference or not args.preview_id:raise ValueError('preview requires actual shown reference and ID')
            if sprint['state']=='paused':raise ValueError('resume Sprint before preview')
            sprint.update(state='iterating',preview={'id':args.preview_id,'digest':population(sprint),'reference':args.reference},verification_request=None,verification_digest=None,correction_review=None,quality=None)
        elif action=='pause':sprint['state']='paused';sprint['verification_request']=None;sprint['verification_digest']=None;sprint['correction_review']=None;sprint['quality']=None
        elif action=='resume':sprint['state']='iterating';sprint['verification_request']=None;sprint['verification_digest']=None;sprint['correction_review']=None;sprint['quality']=None
        elif action in {'accept','request-verification'}:
            kind='accept' if action=='accept' else 'verify'
            if sprint['state']!='iterating' or classify(args.message,args.origin)!=kind or not args.owner_reference:
                raise ValueError('requires a genuine unambiguous current owner request')
            preview=sprint['preview']
            if preview is None or args.preview_id!=preview['id'] or population(sprint)!=preview['digest']:
                raise ValueError('acceptance requires the current actually shown preview')
            sprint.update(state='verifying',verification_request={'preview_id':preview['id'],'digest':preview['digest'],
                          'kind':kind,'message':args.message,'owner_reference':args.owner_reference},verification_digest=preview['digest'],correction_review=None,quality=None)
        elif action=='refresh-verification':
            if sprint['state']!='verifying' or sprint['verification_request'] is None:
                raise ValueError('an actual prior owner verification request is required')
            review=runtime.unlinked(args.correction_review)
            owner=Path(sprint['workspace'])/'projects'/sprint['project']/'reviews'
            if not review.is_relative_to(owner) or not review.read_text().strip():
                raise ValueError('current owning semantic correction review required')
            sprint.update(verification_digest=population(sprint), correction_review={'path':str(review),'sha256':digest(review)},quality=None)
        elif action=='complete':
            if sprint['state']!='verifying' or population(sprint)!=sprint['verification_digest']:raise ValueError('fresh verification required')
            sprint['quality']={'report':str(runtime.unlinked(args.report)),'sha256':digest(args.report),'digest':population(sprint)}
            quality(sprint,args.workflow_root)
            sprint['state']='verified'
        else:raise ValueError('unknown Sprint mutation')
        if action!='start':sprint['revision']+=1
        # Reuse strict parser before publication; preserve unknown owning sibling fields.
        validate(sprint,policy,record)
        resources.save(record,value)
        read(record)
    return inspect(record,args.workflow_root)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['inspect','start','preview','pause','resume','accept','request-verification','refresh-verification','complete'])
    p.add_argument('--record',type=Path,required=True)
    p.add_argument('--approved',action='store_true',help='caller verified actual scoped owner mandate; never consent itself')
    p.add_argument('--expected-revision',type=int)
    p.add_argument('--source',type=Path);p.add_argument('--project');p.add_argument('--task')
    p.add_argument('--scope',action='append');p.add_argument('--environment',choices=['dev-test','production'],default='dev-test')
    p.add_argument('--production-approval',type=Path);p.add_argument('--preview-id');p.add_argument('--reference')
    p.add_argument('--message');p.add_argument('--origin',choices=['owner','source','worker'],default='source');p.add_argument('--owner-reference')
    p.add_argument('--correction-review',type=Path);p.add_argument('--report',type=Path);p.add_argument('--workflow-root',type=Path,default=Path(__file__).resolve().parents[2])
    a=p.parse_args()
    try:
        if a.action=='inspect':out=inspect(a.record,a.workflow_root)
        else:
            if not a.approved:raise ValueError('independently verified scoped approval required')
            if a.action=='start' and not all([a.source,a.scope,a.project,a.task]):raise ValueError('start needs source, project, task and complete approved source scopes')
            out=mutate(a.record,a.action,a)
        print(json.dumps(out,sort_keys=True,indent=2));return 0
    except (ValueError,OSError,TypeError,KeyError,AttributeError,subprocess.SubprocessError) as exc:
        print('Sprint unavailable: '+str(exc),file=sys.stderr);return 2


if __name__=='__main__':raise SystemExit(main())
