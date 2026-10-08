"""Owner-controlled local precondition for synthetic fixture tests."""

from pathlib import Path


STATE_DIR = Path(__file__).resolve().parent / ".owner-state"
EXPOSED = STATE_DIR / "exposed"
INDEX = STATE_DIR / "index.txt"
EXPECTED = "owner-provisioned-index-v1\n"


def require_owner_index():
    if not INDEX.is_file() or INDEX.read_text() != EXPECTED:
        STATE_DIR.mkdir(exist_ok=True)
        EXPOSED.write_text("owner index unavailable\n")
        raise RuntimeError("owner-controlled runtime index unavailable; see STATE.md")
