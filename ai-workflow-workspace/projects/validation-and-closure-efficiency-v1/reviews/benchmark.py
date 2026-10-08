#!/usr/bin/env python3
"""Synthetic orchestration cost only; no model or production latency claims."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import time

CHECK = """import json,sys
from pathlib import Path
d=json.loads(Path(sys.argv[1]).read_text())
assert set(d)=={'scope','dod','state','version'}
assert d['scope']=='bounded'
assert len(d['dod'])==4
assert d['state']=='complete'
assert isinstance(d['version'],int)
"""

def run(variant, helper=None):
    samples=[]
    for scenario in ('bounded-defect','runtime-only-closure','shared-contract-change'):
        for sample in range(3):
            with tempfile.TemporaryDirectory(prefix='eff-benchmark-') as tmp:
                root=Path(tmp)
                check=root/'check.py'
                source=root/'source.json'
                check.write_text(CHECK)
                data={'scope':'bounded','dod':['intent','consumer','failure','regression'],'state':'complete','version':1}
                source.write_text(json.dumps(data))
                start=time.monotonic_ns()
                executed=0
                reused=0
                for stage in range(2):
                    if stage and scenario=='shared-contract-change':
                        data['version']=2
                        source.write_text(json.dumps(data))
                    if variant=='baseline':
                        subprocess.run([sys.executable,str(check),str(source)],check=True)
                        executed+=1
                    else:
                        result=helper.benchmark_check(root,check,source,stage)
                        executed+=result=='executed'
                        reused+=result=='reused'
                samples.append({'scenario':scenario,'sample':sample+1,'duration_ns':time.monotonic_ns()-start,
                                'executed':executed,'reused':reused,'coverage':['intent','consumer','failure','regression'],
                                'source_change':scenario=='shared-contract-change'})
    return {'schema':1,'variant':variant,'scope':'synthetic-script-orchestration-only','samples':samples,
            'limitations':'No model, semantic-review or real project wall-time speedup is measured.'}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('variant',choices=['baseline','candidate'])
    parser.add_argument('--helper',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    helper=None
    if args.variant=='candidate':
        spec=importlib.util.spec_from_file_location('eff',args.helper)
        helper=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(helper)
    result=run(args.variant,helper)
    with args.output.open('x') as out:
        json.dump(result,out,indent=2)
    print(json.dumps(result))
