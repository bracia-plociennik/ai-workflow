import sys,unittest,tempfile,subprocess,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_dreaming_evidence_reader_guard import policy
import dreaming_evidence_reader as r

class Reader(unittest.TestCase):
    def test_actual_cli_and_utf8(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);(root/'notes.md').write_text('Zażółć. Plan, time unknown.');v=policy(root);v['limits']['chunk_bytes']=5
            request=root.parent/(root.name+'-request.json')
            try:
                request.write_text(json.dumps(v));out=subprocess.run([sys.executable,'-B',str(r.ROOT/'.systems/scripts/dreaming-evidence'),'inspect','--request',str(request)],capture_output=True,text=True)
                self.assertEqual(out.returncode,0,out.stderr);value=json.loads(out.stdout)
                self.assertEqual(''.join(x['text'] for x in value['chunks']),'Zażółć. Plan, time unknown.')
                self.assertEqual(value['envelope']['result'],'partial');self.assertEqual(value['envelope']['coverage']['counts']['reviewed'],0)
            finally:request.unlink(missing_ok=True)
    def test_ignored_change_without_head(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td);file=root/'notes.md';file.write_text('first');a=r.provide(policy(root));file.write_text('second');b=r.provide(policy(root))
            self.assertNotEqual(a['chunks'][0]['source_ref']['sha256'],b['chunks'][0]['source_ref']['sha256'])
    def test_safe_invalid_cli(self):
        out=subprocess.run([sys.executable,'-B',str(r.ROOT/'.systems/scripts/dreaming-evidence'),'inspect','--request','/home/private/no.json'],capture_output=True,text=True)
        self.assertEqual(out.returncode,2);self.assertNotIn('/home/private',out.stderr)

if __name__=='__main__':unittest.main()
