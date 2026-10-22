#!/usr/bin/env python3
"""Verify actual active immutable component before its fixed adapter command."""
from pathlib import Path
import hashlib,json,os,sys
bundle=Path(__file__).resolve().parents[2]
try:
    registration=Path.home()/'.config/ai-system/luna-first/active.json'
    value=json.loads(registration.read_text())
    if value['status']!='active' or Path(value['destination'])!=bundle:raise ValueError('Luna-first component inactive or wrong binding')
    actual={str(p.relative_to(bundle)):hashlib.sha256(p.read_bytes()).hexdigest() for p in bundle.rglob('*') if p.is_file() and not p.is_symlink()}
    if actual!=value['installed_files'] or any(p.is_symlink() for p in bundle.rglob('*')):raise ValueError('Luna-first component source changed')
except (OSError,ValueError,KeyError) as exc:
    raise SystemExit('Luna-first unavailable: '+str(exc))
os.execv(sys.executable,[sys.executable,'-B',str(bundle/'system/.systems/scripts/luna_first_adapter.py'),'--workflow-root',str(bundle/'workflow'),*sys.argv[1:]])
