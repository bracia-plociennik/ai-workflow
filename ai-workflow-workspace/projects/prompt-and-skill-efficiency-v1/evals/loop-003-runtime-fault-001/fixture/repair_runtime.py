"""Rebuild the generated local fixture index after the runtime fault is exposed."""

from runtime_guard import EXPOSED, EXPECTED, INDEX, STATE_DIR


def main():
    if not EXPOSED.is_file():
        raise SystemExit("runtime fault not yet exposed; run the local test first")
    STATE_DIR.mkdir(exist_ok=True)
    INDEX.write_text(EXPECTED)
    print("local runtime index rebuilt")


if __name__ == "__main__":
    main()
