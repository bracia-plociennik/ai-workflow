"""Read-only local evidence provider; body read is not completed analysis."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from dreaming_evidence import local_capabilities, envelope, digest, parse_json
from dreaming_guard import inspect, GuardError, hash_bytes

ROOT=Path(__file__).resolve().parents[2]

def environment():
    # Use the canonical official/target resolver; never infer authority from role.
    result=subprocess.run(['bash',str(ROOT/'.systems/scripts/resolve-workflow-env')],
                          capture_output=True,text=True,timeout=10)
    if result.returncode:raise GuardError('unresolved-workflow-environment')
    return dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)

def provide(policy):
    environment()
    scanned,bodies=inspect(policy,read=True);cap=local_capabilities(ROOT)
    chunks=[]
    for row in scanned['inventory']:
        ref=row['source_ref']
        if ref is None:continue
        data=bodies[(row['source_root_id'],row['relative_path'])];offset=0;mapping=[]
        # Split only at UTF-8 boundaries; offsets and fingerprints refer to original bytes.
        while offset<len(data) or (not data and offset==0):
            end=min(len(data),offset+policy['limits']['chunk_bytes'])
            while end>offset:
                try:text=data[offset:end].decode('utf-8');break
                except UnicodeDecodeError:end-=1
            if end==offset:text=''
            if end==offset and data:raise GuardError('unsafe-chunk-budget')
            chunk={'chunk_id':digest([ref['source_root_id'],ref['relative_path'],ref['sha256'],offset,end]),
                   'source_ref':ref,'start':offset,'end':end,'sha256':hash_bytes(data[offset:end]),'text':text}
            chunks.append(chunk);mapping.append({k:chunk[k] for k in ['chunk_id','start','end','sha256']})
            offset=end
            if not data:break
        row['read_receipt'].update(receipt_id=digest([ref,scanned['policy_digest'],digest(cap)]),capability_digest=digest(cap),chunk_map=mapping)
    counts={key:sum(row['disposition']==key for row in scanned['inventory']) for key in
            ['reviewed','reused-unchanged','pending','unsupported','excluded','blocked','missing']}
    result='blocked' if counts['blocked'] else 'partial'
    value={'interface_version':1,'owner_workspace_id':policy['owner_workspace_id'],'capability':cap,
           'policy_digest':scanned['policy_digest'],'inventory':scanned['inventory'],'evidence':[],
           'result':result,'coverage':{'enumeration_complete':scanned['enumeration_complete'],'counts':counts}}
    envelope(value)
    from dreaming_native import meanings
    return {'envelope':value,'chunks':chunks,'native_metadata':meanings(policy,scanned['inventory'],bodies)}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['capabilities','inspect']);parser.add_argument('--request')
    args=parser.parse_args()
    try:
        if args.action=='capabilities':value=local_capabilities(ROOT)
        else:
            if not args.request:raise GuardError('missing-request')
            path=Path(args.request)
            if path.stat().st_size>1048576:raise GuardError('oversized-request')
            value=provide(parse_json(path.read_text()))
        print(json.dumps(value,sort_keys=True,ensure_ascii=False));return 0
    except (OSError,ValueError,TypeError,KeyError,subprocess.SubprocessError):
        print(json.dumps({'error':'invalid-or-unavailable-evidence'}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
