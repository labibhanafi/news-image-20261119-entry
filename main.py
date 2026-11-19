#!/usr/bin/env python3
"""Runner for the news-image-20261119 entry.

Validates entry.png (PNG signature, IHDR dimensions 1024x1024, size at
most 1 MiB) and copies it into the output directory. The output directory
comes from the MAKEFUN_OUTPUT_DIR environment variable, defaulting to
/output. Use --check-only to validate without copying.

Standard library only.
"""
import argparse
import os
import shutil
import struct
import sys
from pathlib import Path

EXPECTED_W = 1024
EXPECTED_H = 1024
MAX_BYTES = 1024 * 1024
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def validate(path):
    """Return a list of problems with the image at path (empty = valid)."""
    problems = []
    if not path.is_file():
        return [f"entry image not found: {path}"]
    data = path.read_bytes()
    if len(data) > MAX_BYTES:
        problems.append(f"file too large: {len(data)} bytes > {MAX_BYTES}")
    if not data.startswith(PNG_SIGNATURE):
        problems.append("missing PNG signature")
        return problems
    # IHDR is the first chunk: length(4) + type(4) + width(4) + height(4)
    if len(data) < 24 or data[12:16] != b"IHDR":
        problems.append("missing IHDR chunk")
        return problems
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (EXPECTED_W, EXPECTED_H):
        problems.append(
            f"wrong dimensions: {width}x{height}, expected "
            f"{EXPECTED_W}x{EXPECTED_H}"
        )
    if b"IEND" not in data[-16:]:
        problems.append("missing IEND chunk (file looks truncated)")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate entry.png and exit without copying it",
    )
    args = parser.parse_args(argv)

    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    problems = validate(source)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print(f"entry.png OK: {EXPECTED_W}x{EXPECTED_H}, "
          f"{source.stat().st_size} bytes")
    if args.check_only:
        return 0

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    print(f"copied to {dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
