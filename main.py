"""Write one short family scene to the entry output path.

Resolves the output path from ENTRY_OUTPUT, then OUTPUT_DIR /
MAKEFUN_OUTPUT_DIR, then /output/entry.txt, then this script's own
directory. Stdlib only.
"""

import os


ENTRY = (
    "Mom keeps Dad's first burnt pancake in the freezer, labelled "
    "'Exhibit A' \u2014 and every anniversary he thaws it, takes one bite, "
    "and says, 'Still the best thing I ever made.'"
)


def resolve_output_path():
    explicit = os.environ.get("ENTRY_OUTPUT")
    if explicit:
        return explicit
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    if os.path.isdir("/output"):
        return "/output/entry.txt"
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    if not ENTRY.strip():
        raise ValueError("entry text must not be empty")
    if len(ENTRY) > 280:
        raise ValueError("entry text exceeds 280 characters")
    if ENTRY.count("\n") > 1:
        raise ValueError("entry text must be one or two lines")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(ENTRY)
    os.chmod(path, 0o644)
    with open(path, "r", encoding="utf-8") as handle:
        if handle.read() != ENTRY:
            raise ValueError("read-back check failed: output differs from entry")


if __name__ == "__main__":
    main()
