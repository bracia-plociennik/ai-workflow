#!/usr/bin/env python3
"""Task-owned model routing metadata. Native dispatch and actual consent stay with the lead."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import tempfile
import time

LUNA='gpt-6-luna'
SOL='gpt-6.1-sol'
REQUEST={'schema','project','task','target_root','inputs','goal','mode','risk','clear','bounded','reversible','dod','checks','concerns','ready','owner_reference'}
STATE={'schema','revision','request','source_hashes','selection','state','attempts','hold_reason'}
ATTEMPT={'id','model','effort','handle','status','outcome','evidence','before','after'}
STRONG={'architecture','ambiguity','security','permissions','billing','migration','production','cross-system','policy','recovery','adversarial-review'}


def fields(value,expected):
    if not isinstance(value,dict) or set(value)!=set(expected):raise ValueError('unsupported fields')


def unlinked(path,exists=True):
    p=Path(os.path.abspath(os.path.expanduser(str(path))))
    if any(x.is_symlink() for x in (p,*p.parents)):raise ValueError('linked path')
    if exists and not p.exists():raise ValueError('missing path')
    return p


def read(path):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError('duplicate JSON key')
            d[k]=v
        return d
    p=unlinked(path)
    if not p.is_file():raise ValueError('regular JSON file required')
    return json.loads(p.read_text(),object_pairs_hook=unique)


def text(value):return isinstance(value,str) and bool(value.strip())


def validate_request(r):
    fields(r,REQUEST)
    if type(r['schema']) is not int or r['schema']!=1:raise ValueError('unknown request version')
    if r['mode'] not in {'implementation','read-only','planning','conversation'} or r['risk'] not in {'low','medium','high','critical','unknown'}:raise ValueError('unknown risk/mode')
    for k in ['clear','bounded','reversible']:
        if type(r[k]) is not bool:raise ValueError('explicit booleans required')
    fields(r['ready'],{'input','access','permission'})
    if any(type(v) is not bool for v in r['ready'].values()):raise ValueError('explicit readiness required')
    for k in ['project','task','goal','owner_reference','target_root']:
        if not text(r[k]):raise ValueError('missing request identity/scope')
    if not r['project'].replace('-','').isalnum() or '/' in r['task'] or '..' in r['task']:raise ValueError('unsafe work identity')
    for k in ['inputs','dod','checks','concerns']:
        if not isinstance(r[k],list) or any(not text(v) for v in r[k]) or len(r[k])!=len(set(r[k])):raise ValueError('invalid request list')
    if set(r['concerns'])-STRONG:raise ValueError('unknown concern')
    if not Path(r['target_root']).is_absolute():raise ValueError('absolute target required')
    unlinked(r['target_root'])
    return r


def choose(r,available=(LUNA,SOL)):
    validate_request(r)
    result={'model':None,'effort':'high','reason':None,'execution_authorized':False}
    if not all(r['ready'].values()):result['reason']='missing-input-access-or-permission'
    elif r['mode']=='conversation':result['reason']='keep-current-conversation'
    else:
        strong=r['risk'] not in {'low','medium'} or bool(r['concerns']) or not all(r[k] for k in ['clear','bounded','reversible']) or not r['dod'] or not r['checks']
        model=SOL if strong else LUNA
        if model not in available:result['reason']='selected-model-unavailable'
        else:result.update(model=model,reason='strong-reasoning' if strong else 'bounded-clear-task')
    return result


def snapshot(r):
    root=unlinked(r['target_root']);out={}
    for rel in r['inputs']:
        path=PurePosixPath(rel)
        if path.is_absolute() or '..' in path.parts or any(p in {'.git','.env','credentials','secrets'} for p in path.parts):raise ValueError('unsafe source input')
        p=unlinked(root/rel)
        if not p.is_relative_to(root) or not p.is_file() or p.stat().st_size>8*1024*1024:raise ValueError('invalid source input')
        out[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
    if not out and r['mode']=='implementation':raise ValueError('implementation needs declared source inputs')
    return out


def qa_remaining(record,now=None):
    """Conservatively share the actual existing Sprint cycle, never create one."""
    s=record.get('sprint_iteration')
    if s is None:return None
    if s.get('schema')!=2:raise ValueError('legacy Sprint needs its existing procedure')
    if s.get('state') not in {'targeted','targeted-checked','targeted-failed','targeted-incomplete'}:return None
    cycles=s.get('cycles')
    if not isinstance(cycles,list) or not cycles:raise ValueError('missing existing QA cycle')
    started=cycles[-1].get('started_at');current=time.time() if now is None else now
    if type(started) not in {int,float} or not math.isfinite(started) or not math.isfinite(current) or current<started:raise ValueError('unknown/backwards QA clock')
    return max(0,300-(current-started))


def validate_state(s):
    fields(s,STATE);validate_request(s['request'])
    if type(s['schema']) is not int or s['schema']!=1 or type(s['revision']) is not int or s['revision']<0:raise ValueError('invalid routing version/revision')
    if s['state'] not in {'ready','live','completed','held','blocked'} or not isinstance(s['attempts'],list):raise ValueError('invalid routing state')
    seen=set()
    for a in s['attempts']:
        fields(a,ATTEMPT)
        if not text(a['id']) or a['id'] in seen or a['model'] not in {LUNA,SOL} or a['effort']!='high':raise ValueError('invalid attempt identity/model')
        seen.add(a['id'])
        if a['status'] not in {'reserved','running','terminated'}:raise ValueError('invalid lifecycle')
        if a['status']!='reserved' and not text(a['handle']):raise ValueError('missing actual handle')
    if sum(a['status']!='terminated' for a in s['attempts'])>1:raise ValueError('multiple active executors')
    if sum(a['model']==LUNA for a in s['attempts'])>2 or sum(a['model']==SOL for a in s['attempts'])>1:raise ValueError('attempt ceiling exceeded')


def owner_path(record,request):
    p=unlinked(record)
    if not any(parent.name==request['project'] and parent.parent.name=='projects' for parent in p.parents):raise ValueError('record outside owning project')
    return p


@contextmanager
def lock(path,value):
    policy=value.get('task_resource_cleanup')
    base=unlinked(policy['canonical']['git_common'])/'task-resource-cleanup.lock' if policy else path.parent/'.luna-first.lock'
    fd=os.open(base,os.O_CREAT|os.O_RDWR|os.O_NOFOLLOW,0o600)
    try:
        fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);yield
    finally:os.close(fd)


def write(path,value):
    fd,temp=tempfile.mkstemp(prefix='.routing-',dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f:json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
        os.replace(temp,path)
    finally:
        if os.path.exists(temp):os.unlink(temp)


def transition(record,op,*,request=None,revision=None,handle=None,outcome=None,evidence=None,actual_model=None,terminated=False,available=(LUNA,SOL)):
    path=unlinked(record);initial=read(path)
    with lock(path,initial):
        value=read(path);s=value.get('model_routing')
        if op=='start':
            if s is not None:raise ValueError('routing already exists; inspect, do not reset')
            validate_request(request);owner_path(path,request)
            if request['mode']=='read-only':raise ValueError('read-only permits choose/inspect only; no routing state writes')
            if value.get('sprint_iteration') and (value['sprint_iteration'].get('project')!=request['project'] or value['sprint_iteration'].get('task')!=request['task']):raise ValueError('foreign Sprint identity')
            selection=choose(request,available)
            s={'schema':1,'revision':0,'request':request,'source_hashes':snapshot(request),'selection':selection,'state':'ready' if selection['model'] else 'held','attempts':[],'hold_reason':None if selection['model'] else selection['reason']}
        else:
            if s is None:raise ValueError('missing task-owned routing')
            validate_state(s);owner_path(path,s['request'])
            if revision!=s['revision']:raise ValueError('stale revision')
            if op=='reserve':
                if s['state']!='ready' or any(a['status']!='terminated' for a in s['attempts']):raise ValueError('active/unknown executor or task not ready')
                if snapshot(s['request'])!=s['source_hashes']:raise ValueError('source changed before dispatch')
                left=qa_remaining(value)
                if left is not None and left<=0:raise ValueError('shared QA budget exhausted')
                model=s['selection']['model']
                if model not in available:raise ValueError('selected model unavailable')
                s['attempts'].append({'id':f"{s['request']['task']}-{len(s['attempts'])+1}",'model':model,'effort':'high','handle':None,'status':'reserved','outcome':None,'evidence':None,'before':s['source_hashes'],'after':None});s['state']='live'
            elif op=='bind':
                a=s['attempts'][-1]
                if s['state']!='live' or a['status']!='reserved' or not text(handle):raise ValueError('reserved attempt and actual handle required')
                if any(x['handle']==handle for x in s['attempts'][:-1]):raise ValueError('native handle already retired')
                a.update(handle=handle,status='running')
            elif op=='report-preview':
                a=s['attempts'][-1]
                if s['state']!='live' or a['status']!='running' or a['handle']!=handle:raise ValueError('matching live native handle required')
                proof=unlinked(evidence)
                if not proof.is_file() or not proof.read_bytes() or not any(parent.name==s['request']['project'] and parent.parent.name=='projects' for parent in proof.parents):raise ValueError('owning preview evidence required')
                s['source_hashes']=snapshot(s['request']);a.update(outcome='preview-ready',evidence={'path':str(proof),'sha256':hashlib.sha256(proof.read_bytes()).hexdigest()})
            elif op=='finish':
                a=s['attempts'][-1]
                if a['status']!='running' or a['handle']!=handle or not terminated or actual_model!=a['model']:raise ValueError('matching actual model/handle and observed termination required')
                if outcome not in {'qa-passed','qa-failed','qa-incomplete','blocked-input','scope-drift'}:raise ValueError('unknown outcome')
                proof=unlinked(evidence)
                if not proof.is_file() or not proof.read_bytes() or not any(parent.name==s['request']['project'] and parent.parent.name=='projects' for parent in proof.parents):raise ValueError('current owning evidence required')
                if outcome.startswith('qa-') and value.get('sprint_iteration'):
                    sprint=value['sprint_iteration']
                    if sprint.get('state') not in {'targeted','targeted-checked','targeted-failed','targeted-incomplete','verifying','verified'}:raise ValueError('owner acceptance or verification required before QA')
                    left=qa_remaining(value)
                    if left is not None and left<=0:outcome='qa-incomplete'
                s['source_hashes']=snapshot(s['request'])
                a.update(status='terminated',outcome=outcome,evidence={'path':str(proof),'sha256':hashlib.sha256(proof.read_bytes()).hexdigest()},after=s['source_hashes'])
                if outcome=='qa-passed':s.update(state='completed',hold_reason=None)
                elif outcome in {'blocked-input','scope-drift','qa-incomplete'}:s.update(state='held',hold_reason=outcome)
                elif a['model']==SOL:s.update(state='blocked',hold_reason='strong-attempt-failed')
                else:
                    model=LUNA if sum(x['model']==LUNA for x in s['attempts'])<2 else SOL
                    if model not in available:s.update(state='held',hold_reason='selected-model-unavailable')
                    else:s.update(state='ready',hold_reason=None,selection={'model':model,'effort':'high','reason':'one-repair' if model==LUNA else 'luna-repair-failed','execution_authorized':False})
            else:raise ValueError('unknown transition')
            s['revision']+=1
        validate_state(s);value['model_routing']=s;write(path,value)
        return {'model_routing':s,'remaining_qa_seconds':qa_remaining(value),'execution_authorized':False}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('operation',choices=['choose','start','inspect','reserve','bind','report-preview','finish'])
    p.add_argument('--record');p.add_argument('--request');p.add_argument('--revision',type=int);p.add_argument('--handle');p.add_argument('--outcome');p.add_argument('--evidence');p.add_argument('--actual-model');p.add_argument('--terminated',action='store_true');a=p.parse_args()
    try:
        if a.operation=='choose':out=choose(read(a.request))
        elif a.operation=='inspect':
            value=read(a.record);s=value.get('model_routing')
            if s is not None:validate_state(s);owner_path(a.record,s['request'])
            out={'model_routing':s,'remaining_qa_seconds':qa_remaining(value),'execution_authorized':False}
        else:out=transition(a.record,a.operation,request=read(a.request) if a.request else None,revision=a.revision,handle=a.handle,outcome=a.outcome,evidence=a.evidence,actual_model=a.actual_model,terminated=a.terminated)
        print(json.dumps(out,indent=2));return 0
    except (ValueError,OSError,KeyError,IndexError,TypeError) as exc:print('Model routing unavailable: '+str(exc),file=__import__('sys').stderr);return 2


if __name__=='__main__':raise SystemExit(main())
