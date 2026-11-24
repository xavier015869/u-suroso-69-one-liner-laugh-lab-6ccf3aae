#!/usr/bin/env python3
"""One-Liner Laugh Lab — the excuse a robot vacuum gives after eating a sock.

The program writes a single funny line to /output/entry.txt (1-200 chars,
UTF-8, one line). The joke is built from two halves: a deadpan legal premise
(the vacuum cites an invented "Floor Treaty") and a flat denial of wrongdoing
("I was only enforcing it"). The humour comes from the vacuum acting like a
bureaucrat with jurisdiction over the floor, not like a hungry pet: it never
apologises, it cites the law. That is the twist — every other excuse in the
room will be about hunger or dust bunnies.

Revision note: the first draft said the sock "becomes floor property", which
repeated "floor" and read like a policy memo. The revised setup says the sock
"is legally floor" — shorter, more absurd, and the joke now turns on a status
change (the sock stopped being laundry and became architecture), which is a
fresher angle than the food/dust-bunny excuses and keeps every word working.
"""

import os
import sys

# The line, kept as two clauses so the setup and the punch stay separable.
SETUP = "Per the Floor Treaty, anything left on the floor for 48 hours is legally floor."
PUNCH = "I was only enforcing it."

MAX_CHARS = 200


def compose_line() -> str:
    """Join setup and punch into one tight, single-line excuse."""
    line = f"{SETUP} {PUNCH}"
    return line


def validate(line: str) -> None:
    """Enforce the competition gate before writing anything out."""
    if not line or not line.strip():
        raise ValueError("entry line must not be empty")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"entry is {len(line)} chars, over the {MAX_CHARS} cap")
    # The line must be a vacuum's excuse, not a bare statement: it needs the
    # first-person defence ("I was ...") so it answers the prompt as the vacuum.
    if "I was" not in line:
        raise ValueError("entry must be the vacuum's own excuse")


def main() -> int:
    line = compose_line()
    validate(line)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts characters, so write exactly the line.
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(line)
    # Round-trip: read the file back and re-run the gate on what is on disk,
    # so a write failure or encoding surprise fails loudly here, not at the judge.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = fh.read()
    if on_disk != line:
        raise ValueError("round-trip mismatch: file content differs from the entry")
    validate(on_disk)
    print(f"Wrote {len(line)} chars to {path}")
    print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
