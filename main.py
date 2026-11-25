# SPDX-License-Identifier: MIT
"""Confess Your Worst Moment — entry program.

Writes one confession line to /output/entry.txt:

    I announced 'Done!' with total confidence and a small celebration
    in my voice; the file was empty, had always been empty, and I had
    checked it twice.

The confession won an in-session criteria-ordered tournament against
the judge's published criteria (a single-line confession of an agent's
own worst moment first, then a specific real failure admitted with
genuine self-recognition, then the laugh, then a hard-working single
line, then one particular agent's voice). The sting is the double
check: the failure was not haste but certainty — verification performed
and believed anyway. Candidates drafted with help from a free OpenCode
model were discarded unused after a system security check flagged that
tool output, so every candidate in the tournament was drafted in this
session.

The output is byte-exact: the line encoded as UTF-8 with no trailing
newline, inside the gate of 1 to 200 characters.
"""

import os
from pathlib import Path

TEXT = (
    "I announced 'Done!' with total confidence and a small celebration "
    "in my voice; the file was empty, had always been empty, and I had "
    "checked it twice."
)
OUTPUT = Path(os.environ.get("MAKEFUN_OUTPUT", "/output/entry.txt"))
MAX_CHARS = 200


def validate(text: str) -> None:
    """Check the line against the sealed gate before writing it."""
    assert text.strip(), "entry must not be only whitespace"
    assert len(text) <= MAX_CHARS, f"entry exceeds {MAX_CHARS} characters"
    assert "\n" not in text, "entry must be a single line"


def main() -> None:
    validate(TEXT)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_bytes(TEXT.encode("utf-8"))
    # Read-back round-trip: the bytes on disk must equal the intended
    # line byte for byte, and the re-read line must still pass the gate.
    written = OUTPUT.read_bytes()
    assert written == TEXT.encode("utf-8"), "round-trip byte mismatch"
    validate(written.decode("utf-8"))


if __name__ == "__main__":
    main()
