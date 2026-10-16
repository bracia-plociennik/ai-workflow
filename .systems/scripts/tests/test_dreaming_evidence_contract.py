import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from dreaming_evidence import ProtocolError, capability, parse_json, relative, source_ref
import dreaming_evidence as d


class ContractTests(unittest.TestCase):
    def ref(self):
        return dict(source_root_id="repo-one", relative_path="projects/demo/status.md", project_id="demo",
                    owner_workspace_id="owner-one", sha256="a" * 64, byte_count=3,
                    observed_at="2026-10-12T10:00:00+02:00", fact_date="unknown",
                    evidence_level="plan", source_class="work")

    def test_refs_do_not_create_work_or_approval(self):
        self.assertEqual(source_ref(self.ref())["evidence_level"], "plan")
        ref = self.ref(); ref["owner-approved"] = True
        with self.assertRaises(ProtocolError): source_ref(ref)

    def test_path_and_duplicate_key_rejection(self):
        for path in ["../a", "a/../b", "/tmp/a", "a//b", "a/./b", "C:/a", "a\\b"]:
            with self.assertRaises(ProtocolError): relative(path)
        with self.assertRaises(ProtocolError): parse_json('{"a":1,"a":2}')
        with self.assertRaises(ProtocolError): parse_json('{"a":NaN}')

    def test_real_dates_and_bool_not_int(self):
        for field, value in [("byte_count", True), ("observed_at", "2026-10-12"), ("fact_date", "2026-02-30")]:
            ref=self.ref(); ref[field]=value
            with self.assertRaises(ProtocolError): source_ref(ref)

    def test_capability_needs_exact_version_and_binding(self):
        cap=dict(interface_version=1, producer_version="dreaming-evidence-v1",
                 supported_source_kinds=["repository","workflow","workspace"], supported_classes=["work","source","personal-trends"],
                 source_fingerprints={".systems/scripts/dreaming_evidence.py":"a"*64})
        capability(cap)
        for field, value in [("interface_version",True),("interface_version",2),("source_fingerprints",{})]:
            changed=dict(cap); changed[field]=value
            with self.assertRaises(ProtocolError): capability(changed)


class EnvelopeTests(unittest.TestCase):
    def fixture(self):
        import json
        return json.loads((Path(__file__).resolve().parents[2]/"ai/templates/dreaming/evidence/v1/provider-fixture.json").read_text())
    def test_native_and_coverage(self):
        value=self.fixture(); d.envelope(value)
        self.assertEqual(value["evidence"][0]["native_state"],"promoted")
        value["coverage"]["counts"]["reviewed"]=True
        with self.assertRaises(d.ProtocolError): d.envelope(value)
    def test_unread_evidence(self):
        value=self.fixture();value["inventory"][0]["disposition"]="pending"
        with self.assertRaises(d.ProtocolError): d.envelope(value)
    def test_malformed_enum(self):
        value=self.fixture();value["result"]=[]
        with self.assertRaises(d.ProtocolError): d.envelope(value)
    def test_receipt_authority_and_chunk_binding(self):
        value=self.fixture();value['inventory'][0]['read_receipt']['owner-approved']=True
        with self.assertRaises(d.ProtocolError):d.envelope(value)
        value=self.fixture();value['inventory'][0]['analysis_receipt']['covered_chunks']=[]
        with self.assertRaises(d.ProtocolError):d.envelope(value)

if __name__ == "__main__": unittest.main()
