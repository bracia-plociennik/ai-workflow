import sys,unittest,tempfile,subprocess,json,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import dreaming_evidence_reader as r
import dreaming_evidence as d

class NativeCompatibility(unittest.TestCase):
    def test_standalone_and_legacy_source_gate(self):
        with tempfile.TemporaryDirectory() as td:
            import os
            out=subprocess.run(['bash',str(r.ROOT/'.systems/scripts/check-dreaming-mode')],env={**os.environ,'AI_WORKFLOW_WORKSPACE_HOME':td},capture_output=True,text=True)
            self.assertEqual(out.returncode,0,out.stdout+out.stderr)
            cap=d.local_capabilities(r.ROOT);self.assertEqual(cap['interface_version'],1)
            for path,expected in cap['source_fingerprints'].items():self.assertEqual(hashlib.sha256((r.ROOT/path).read_bytes()).hexdigest(),expected)
    def test_transport_native_meaning(self):
        value=json.loads((r.ROOT/'.systems/ai/templates/dreaming/evidence/v1/provider-fixture.json').read_text())
        d.envelope(value);self.assertEqual(value['evidence'][0]['native_state'],'promoted');self.assertEqual(value['evidence'][0]['native_quality'],'unknown')

if __name__=='__main__':unittest.main()
