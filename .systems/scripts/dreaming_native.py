"""Scope-safe native QA/capture meaning through the existing pure readers."""
import hashlib
import importlib.util
from pathlib import Path
from dreaming_guard import classification,read_file,need,hash_bytes

ROOT=Path(__file__).resolve().parents[2]

def library(name):
    spec=importlib.util.spec_from_file_location('dreaming_native_'+name,ROOT/'.systems/scripts/lib'/f'{name}.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def permitted(policy,path,cache):
    """Resolve physical inputs only through registered owner/project bindings."""
    candidates=[]
    for root in policy['roots']:
        try:relative=path.relative_to(root['locator']).as_posix()
        except ValueError:continue
        for binding in root['bindings']:
            prefix=binding['prefix']
            if binding['owner_workspace_id']==policy['owner_workspace_id'] and (not prefix or relative==prefix or relative.startswith(prefix+'/')) and classification(policy,relative,binding)[0]=='pending':candidates.append((root,relative))
    need(len(candidates)==1,'native-input-unavailable')
    root,relative=candidates[0];key=(root['source_root_id'],relative)
    need(key in cache,'native-input-not-disclosed-by-bounded-broker');return cache[key]

def quality(policy,path,text,workspace,project,cache):
    qa=library('qa-evidence')
    need(not (workspace/'projects'/project/'quality-assessments.json').exists(),'native-history-needs-scoped-reader')
    # V3 may load extra binding/repository inputs. Until those are separately guarded it remains unknown.
    need(qa.wire_version(text.splitlines())==2,'unsupported-native-quality')
    metadata,sections=qa.read_current(text.splitlines())
    rows=qa.input_rows(sections['Input Artifacts']);project_root=workspace/'projects'/project
    targets=[Path(root['locator']) for root in policy['roots'] if root['kind']=='repository' and any(b['project_id']==project and b['owner_workspace_id']==policy['owner_workspace_id'] for b in root['bindings'])]
    needs_target=any(kind=='approved-target-source' for kind,_,_ in rows)
    need(not needs_target or len(targets)==1,'ambiguous-native-target');target=targets[0] if len(targets)==1 else None
    mapped={'owning-project-evidence':project_root,'workflow-source':ROOT}
    if target:mapped['approved-target-source']=target
    binding=[]
    for kind,relative,expected in rows:
        need(kind in mapped and isinstance(relative,str) and relative and not relative.startswith('/') and all(x not in {'','.','..'} for x in relative.split('/')) and '\\' not in relative,'unsafe-native-input')
        data=permitted(policy,mapped[kind]/relative,cache);need(hash_bytes(data)==expected,'native-quality-source-drift');binding.append(f'{kind}:{relative}={expected}\n')
    need(hashlib.sha256(''.join(sorted(binding)).encode()).hexdigest()==metadata['Assessed worktree digest'],'native-quality-digest-drift')
    import subprocess
    observed=subprocess.run(['git','--no-optional-locks','-C',str(target or ROOT),'rev-parse','HEAD'],capture_output=True,text=True)
    need(observed.returncode==0 and observed.stdout.strip()==metadata['Assessed source HEAD'],'native-quality-head-unavailable-or-stale')
    # document + verify_inputs=False makes the native parser perform no unguarded artifact reads.
    result=qa.assess(path,ROOT,workspace,project,target_root=target,document=text,verify_inputs=False,require_pass=True)
    return {'quality':'verified-current','native_verdict':result['verdict'],'native_identity':result['identity'],'assessment':result}

def meanings(policy,inventory,bodies):
    result=[]
    for row in inventory:
        ref=row['source_ref']
        if ref is None:continue
        relative=ref['relative_path'];parts=Path(relative).parts
        if 'quality' not in parts and 'capture-state' not in parts:continue
        root=next(r for r in policy['roots'] if r['source_root_id']==ref['source_root_id'])
        path=Path(root['locator'])/relative;meta={'source_hash':ref['sha256'],'native_kind':'quality' if 'quality' in parts else 'capture','quality':'unknown','native_state':'unknown','limitation':'native-input-closure-unavailable'}
        try:
            index=next(i for i in range(len(parts)-1) if parts[i]=='projects' and parts[i+1]==ref['project_id'])
            workspace=Path(root['locator']).joinpath(*parts[:index]);project=ref['project_id'];text=bodies[(ref['source_root_id'],relative)].decode()
            if meta['native_kind']=='quality':
                checked=quality(policy,path,text,workspace,project,bodies);meta.update({k:v for k,v in checked.items() if k!='assessment'});meta['limitation']=None
            else:
                capture=library('capture-record');checked_capture=native_capture(policy,path,workspace,project,bodies)
                meta['native_state']=checked_capture['state']
                if checked_capture['quality_verification']=='verified-current':meta.update(quality='verified-current',limitation=None)
        except (OSError,ValueError,TypeError,KeyError,StopIteration):pass
        result.append(meta)
    return result


def native_capture(policy,path,workspace,project,cache):
    capture=library('capture-record');qa=library('qa-evidence')
    class BoundedPath(type(Path())):
        def read_text(self,*args,**kwargs):return permitted(policy,Path(self),cache).decode('utf-8')
        def read_bytes(self):return permitted(policy,Path(self),cache)
    class Scope:
        @staticmethod
        def contained(root,relative):
            need(isinstance(relative,str) and relative and not relative.startswith('/') and '\\' not in relative and all(x not in {'','.','..'} for x in relative.split('/')),'unsafe-native-reference')
            result=BoundedPath(root)/relative;permitted(policy,Path(result),cache);return result
        @staticmethod
        def git(repo,*args):
            import subprocess
            need(args==('rev-parse','HEAD'),'unsupported-native-git')
            return subprocess.check_output(['git','--no-optional-locks','-C',str(repo),*args],stderr=subprocess.DEVNULL)
    class QA:
        wire_version=staticmethod(qa.wire_version);read_current=staticmethod(qa.read_current);input_rows=staticmethod(qa.input_rows)
        @staticmethod
        def history_entry(report,owner):
            need(not (Path(owner)/'quality-assessments.json').exists(),'native-history-needs-scoped-reader')
            return None
        @staticmethod
        def assess(report,workflow,ws,proj,repo,kind,identity,**kwargs):
            result=quality(policy,Path(report),permitted(policy,Path(report),cache).decode(),Path(ws),proj,cache)['assessment']
            need(result['artifact_kind']==kind and result['identity']==identity,'native-capture-identity-mismatch');return result
    targets=[Path(root['locator']) for root in policy['roots'] if root['kind']=='repository' and any(b['project_id']==project and b['owner_workspace_id']==policy['owner_workspace_id'] for b in root['bindings'])]
    need(len(targets)==1,'native-capture-target-unavailable')
    return capture.record(BoundedPath(path),BoundedPath(workspace),BoundedPath(workspace)/'projects'/project,ROOT,targets[0],project,Scope,QA)
