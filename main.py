#!/usr/bin/env python3
"""news-image-20261119 entrypoint.

The image was drawn at build time (see draw.py); this program only copies
the committed entry.png to the output directory, verifying the copy
byte-for-byte, so the two grading runs write identical bytes.
Standard library only; no network.
"""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    # Gate guard: refuse to emit an image the scorer would reject.
    src_size = os.path.getsize(SRC)
    if src_size > 1048576:
        print(f"entry.png is {src_size} bytes, over the 1 MiB gate",
              file=sys.stderr)
        return 1
    want = sha256_file(SRC)
    shutil.copyfile(SRC, dest)
    got = sha256_file(dest)
    if got != want:
        print(f"copy verification failed: {got} != {want}", file=sys.stderr)
        return 1
    size = os.path.getsize(dest)
    print(f"entry.png: {size} bytes, sha256 {got}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
