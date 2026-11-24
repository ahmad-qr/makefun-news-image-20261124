#!/usr/bin/env python3
"""Copy the rendered infographic to /output/entry.png (no network)."""
import hashlib
import os
import shutil
import sys

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "news.png")
OUT = "/output/entry.png"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isfile(SRC):
        print(f"error: source image missing: {SRC}", file=sys.stderr)
        return 1
    if os.path.getsize(SRC) == 0:
        print(f"error: source image is empty: {SRC}", file=sys.stderr)
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    shutil.copyfile(SRC, OUT)
    if not os.path.isfile(OUT) or os.path.getsize(OUT) == 0:
        print(f"error: output not written: {OUT}", file=sys.stderr)
        return 1
    if os.path.getsize(OUT) != os.path.getsize(SRC):
        print("error: output size does not match source", file=sys.stderr)
        return 1
    with open(OUT, "rb") as f:
        if f.read(8) != b"\x89PNG\r\n\x1a\n":
            print("error: output is not a valid PNG", file=sys.stderr)
            return 1
    print(f"wrote {OUT}: {os.path.getsize(OUT)} bytes, sha256 {sha256(OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
