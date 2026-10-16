import sys,tempfile,unittest,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_dreaming_evidence_reader_guard import policy
import dreaming_native as n
import dreaming_evidence_reader as r

def qa_text(checksum):
    import subprocess
    head=subprocess.check_output(['git','--no-optional-locks','-C',str(r.ROOT),'rev-parse','HEAD'],text=True).strip()
    digest=hashlib.sha256(f'owning-project-evidence:subject.md={checksum}\n'.encode()).hexdigest()
    return f'''# Synthetic architecture assessment

- QA verification contract: `full-qa-verification-v2`

## Current QA Run

- Run ID: fixture-native-current
- Artifact kind: architecture-qa
- Project/task identity: project-a
- Assessed source HEAD: {head}
- Assessed worktree digest: {digest}
- Input artifacts: see table
- Verdict: PASS
- Gate Decision: PASS

### Input Artifacts

| Root kind | Relative path | SHA-256 |
| --- | --- | --- |
| owning-project-evidence | subject.md | {checksum} |

### Findings

- Blockers: none
- Unresolved findings: none
- Scope: synthetic transport/reader fixture, no actual work approval.

### Evidence

| Check | Result | Evidence |
| --- | --- | --- |
| Fixture input binding | PASS | synthetic subject bytes |

### Review Completeness Gate

- Status: complete
- Reviewed baseline: exact synthetic subject digest
- Closure freshness: current
- Post-fix full re-review: not-required
- Policy-boundary adversarial matrix: completed
- Producer-consumer field audit: completed
- Required-field mapping: complete

### QA Verification Scope

Synthetic artifact reader semantics only; never WEP authority.

### Artifact QA Completeness Gate

- Owner intent and governing sources reviewed: synthetic fixture contract
- DoD / phase acceptance criteria reviewed: yes
- Scope and out-of-scope consistency: aligned
- Artifact / relevant diff review: completed
- Findings-first review: completed
- Failure / rework / dependency scenarios: completed
- Repository and source compatibility: aligned
- Post-fix full artifact re-review: not-required
- Evidence reviewed: current synthetic subject bytes
- Skipped or unreadable sources: none
- Residual risk: fixture only, no semantic delivery/permission proof
- Closure freshness: current

### Gate Decision

- Architecture QA result: PASS
- Required next phase: phase-2-planning
'''

class NativeReader(unittest.TestCase):
    def test_current_guarded_qa_then_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);project=root/'projects/project-a';(project/'quality').mkdir(parents=True)
            subject=project/'subject.md';subject.write_text('Synthetic plan only')
            report=project/'quality/phase-1-architecture-qa.md';report.write_text(qa_text(hashlib.sha256(subject.read_bytes()).hexdigest()))
            value=r.provide(policy(root));self.assertEqual(value['native_metadata'][0]['quality'],'verified-current');self.assertEqual(value['envelope']['result'],'partial')
            subject.write_text('Changed source');value=r.provide(policy(root));self.assertEqual(value['native_metadata'][0]['quality'],'unknown')
    def test_reference_outside_bounded_inventory_never_read(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);project=root/'projects/project-a';(project/'quality').mkdir(parents=True)
            report=project/'quality/phase-1-architecture-qa.md';report.write_text(qa_text('a'*64).replace('subject.md','../../outside.md'))
            value=r.provide(policy(root));self.assertEqual(value['native_metadata'][0]['quality'],'unknown')
    def test_metadata_cache_has_no_extra_reads(self):
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);p=policy(root)
            with patch.object(n,'read_file',side_effect=AssertionError('extra body read')):
                with self.assertRaises(ValueError):n.permitted(p,root/'outside.md',{})
    def test_capture_uses_native_reader_and_owned_refs(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td);root=base/'workspace';root.mkdir();repo=base/'repo';repo.mkdir()
            project=root/'projects/project-a';(project/'capture-state').mkdir(parents=True);(project/'subject.md').write_text('Synthetic source')
            capture=project/'capture-state/task-a.md'
            capture.write_text('''# Synthetic capture

- Capture schema: 2
- Work ID: TASK-A
- Work mode: full-project
- Project/repo scope: project-a
- Source artifact: subject.md
- Quality artifact: none
- State: pending-quality
- Distillation artifact: none
- Last reminder: 2026-10-12
- Owner disposition: not-requested
- Privacy/scope check: pass
- Residual risk: synthetic only
- is_distilled derived value: false
''')
            p=policy(root);p['roots'].append(dict(source_root_id='repo-a',locator=str(repo),kind='repository',bindings=[dict(prefix='',project_id='project-a',owner_workspace_id='workspace-a',source_class='source')]))
            value=r.provide(p);self.assertEqual(value['native_metadata'][0]['native_state'],'pending-quality');self.assertEqual(value['native_metadata'][0]['quality'],'unknown')
            capture.write_text(capture.read_text().replace('subject.md','../../outside.md'))
            value=r.provide(p);self.assertEqual(value['native_metadata'][0]['native_state'],'unknown')

if __name__=='__main__':unittest.main()
