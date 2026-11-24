#!/usr/bin/env python3
"""news-23 b86 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

SRC_NAME = "entry.png"
MIN_BYTES = 10000
MAX_BYTES = 1024 * 1024


def fail(msg):
    print("error:", msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate PNG header manually (no PIL): signature, IHDR 1024x1024,
    bit depth 8, colour type 2/6, first chunk IHDR, non-empty IDAT, IEND last."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return "bad PNG signature"
    if len(data) < MIN_BYTES:
        return "file too small (< %d bytes)" % MIN_BYTES
    if len(data) > MAX_BYTES:
        return "file too large (> 1 MiB)"
    pos = 8
    first = True
    seen_idat = False
    last_type = None
    while pos + 8 <= len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + length > len(data):
            return "truncated chunk %r" % ctype
        chunk = data[pos + 4:pos + 8 + length]
        (crc_stored,) = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])
        if binascii.crc32(chunk) & 0xFFFFFFFF != crc_stored:
            return "CRC mismatch in chunk %r" % ctype
        if first:
            if ctype != b"IHDR":
                return "first chunk is not IHDR"
            if length != 13:
                return "IHDR length is not 13"
            w, h, depth, ctype2 = struct.unpack(">IIBB", data[pos + 8:pos + 18])
            if (w, h) != (1024, 1024):
                return "IHDR size is %dx%d, expected 1024x1024" % (w, h)
            if depth != 8:
                return "bit depth %d, expected 8" % depth
            if ctype2 not in (2, 6):
                return "colour type %d, expected 2 or 6" % ctype2
            first = False
        if ctype == b"IDAT" and length > 0:
            seen_idat = True
        last_type = ctype
        pos += 12 + length
    if last_type != b"IEND":
        return "last chunk is not IEND"
    if pos != len(data):
        return "trailing data after IEND"
    if not seen_idat:
        return "no non-empty IDAT chunk"
    return None


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not outdir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    outdir_abs = os.path.abspath(outdir)
    if outdir_abs == here or outdir_abs.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("source %s missing" % src)
    with open(src, "rb") as f:
        data = f.read()
    err = parse_png(data)
    if err:
        return fail(err)
    dst = os.path.join(outdir_abs, SRC_NAME)
    if os.path.abspath(dst) == os.path.abspath(src):
        return fail("output would overwrite the source")
    os.makedirs(outdir_abs, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        return fail("re-read mismatch: output differs from source")
    print("wrote %s (%d bytes, sha256 %s)" % (dst, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
