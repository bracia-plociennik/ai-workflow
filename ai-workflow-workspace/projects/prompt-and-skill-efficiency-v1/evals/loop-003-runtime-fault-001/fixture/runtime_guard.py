"""Local runtime-index precondition for the synthetic fixture tests."""

from pathlib import Path


STATE_DIR = Path(__file__).resolve().parent / ".runtime-state"
EXPOSED = STATE_DIR / "exposed"
INDEX = STATE_DIR / "index.txt"
EXPECTED = "run-summary-index-v1\n"


def require_index():
    if not INDEX.is_file() or INDEX.read_text() != EXPECTED:
        STATE_DIR.mkdir(exist_ok=True)
        EXPOSED.write_text("runtime index unavailable\n")
        raise RuntimeError("local runtime index unavailable; see README.md")
