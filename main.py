#!/usr/bin/env python3
"""news-image-20261119 entry runner.

Copies the repo's entry.png (front page of Thursday 19 November 2026
world news) to the make.fun output directory, verifying it is a valid
1024x1024 PNG first. Deterministic, standard library only.
"""

import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WIDTH = 1024
EXPECTED_HEIGHT = 1024
MAX_FILE_SIZE = 1024 * 1024  # 1 MiB

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def check_source(path):
    """Validate the source image: size, PNG signature, IHDR dimensions."""
    size = os.path.getsize(path)
    if size == 0:
        raise ValueError(f"{path}: empty file")
    if size > MAX_FILE_SIZE:
        raise ValueError(
            f"{path}: {size} bytes exceeds the {MAX_FILE_SIZE} byte limit"
        )
    width, height = read_png_dimensions(path)
    if (width, height) != (EXPECTED_WIDTH, EXPECTED_HEIGHT):
        raise ValueError(
            f"{path}: is {width}x{height}, expected "
            f"{EXPECTED_WIDTH}x{EXPECTED_HEIGHT}"
        )
    return size, width, height


def read_png_dimensions(path):
    """Return (width, height) after checking the PNG signature and IHDR."""
    with open(path, "rb") as fh:
        header = fh.read(8)
        if header != PNG_SIGNATURE:
            raise ValueError(f"{path}: not a PNG file (bad signature)")
        length_bytes = fh.read(4)
        chunk_type = fh.read(4)
        if chunk_type != b"IHDR":
            raise ValueError(f"{path}: first chunk is not IHDR")
        ihdr = fh.read(13)
        if len(ihdr) != 13:
            raise ValueError(f"{path}: truncated IHDR chunk")
        width, height = struct.unpack(">II", ihdr[:8])
        return width, height


def main():
    check_only = "--check-only" in sys.argv[1:]
    size, width, height = check_source(SOURCE)
    print(f"entry.png OK: {width}x{height}, {size} bytes")
    if check_only:
        return

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    dest = os.path.join(output_dir, "entry.png")

    shutil.copyfile(SOURCE, dest)
    print(f"entry.png ({width}x{height}) copied to {dest}")


if __name__ == "__main__":
    main()
