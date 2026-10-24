#!/usr/bin/env python3
"""Shrink and convert images for the website (needs Pillow: pip install pillow).

    python3 scripts/compress-images.py                    # everything in images/workshops/
    python3 scripts/compress-images.py path/to/folder photo.png ...

For every image found it
  - turns the camera rotation into real pixels and strips EXIF (GPS position, camera serial),
  - scales it down to at most --max pixels on the long side (default 2400),
  - saves JPEG photos at --quality (default 82), PNGs with transparency as optimised PNG,
  - converts PNG/TIFF/BMP/HEIC photos without transparency to .jpg (and removes the original),
  - leaves a file alone when the result would not be smaller.
Safe to run again: files that are already small stay as they are. HEIC needs: pip install pillow-heif."""
import argparse, os, sys
from PIL import Image, ImageOps

try:
    import pillow_heif
    pillow_heif.register_heif_opener()
except ImportError:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXT = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".heic", ".heif"}


def files(paths):
    for p in paths:
        if os.path.isdir(p):
            for d, _, fs in os.walk(p):
                for f in sorted(fs):
                    if os.path.splitext(f)[1].lower() in EXT:
                        yield os.path.join(d, f)
        elif os.path.splitext(p)[1].lower() in EXT:
            yield p


def shrink(path, mx, q):
    before = os.path.getsize(path)
    im = ImageOps.exif_transpose(Image.open(path))
    im.load()
    alpha = im.mode in ("RGBA", "LA") or "transparency" in im.info
    ext = os.path.splitext(path)[1].lower()
    if max(im.size) > mx:
        im.thumbnail((mx, mx), Image.LANCZOS)
    if alpha:
        out, fmt, kw = os.path.splitext(path)[0] + (".webp" if ext == ".webp" else ".png"), None, {}
        if out.endswith(".webp"):
            fmt, kw = "WEBP", {"quality": q, "method": 6}
        else:
            fmt, kw = "PNG", {"optimize": True}
    elif ext == ".webp":
        out, fmt, kw = path, "WEBP", {"quality": q, "method": 6}
        im = im.convert("RGB")
    else:
        out, fmt, kw = os.path.splitext(path)[0] + ".jpg", "JPEG", {"quality": q, "optimize": True, "progressive": True}
        im = im.convert("RGB")
    tmp = out + ".tmp"
    im.save(tmp, fmt, **kw)
    after = os.path.getsize(tmp)
    if out == path and after >= before:  # already small: keep the original
        os.remove(tmp)
        return before, before, path
    os.replace(tmp, out)
    if out != path:
        os.remove(path)
    return before, after, out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="*", default=[os.path.join(ROOT, "images", "workshops")])
    ap.add_argument("--max", type=int, default=2400, help="longest side in pixels")
    ap.add_argument("--quality", type=int, default=82)
    a = ap.parse_args()
    tb = ta = n = 0
    for f in files(a.paths):
        try:
            b, af, out = shrink(f, a.max, a.quality)
        except Exception as e:
            print("skip %s: %s" % (f, e), file=sys.stderr)
            continue
        tb, ta, n = tb + b, ta + af, n + 1
        print("%s  %d KB -> %d KB%s" % (os.path.relpath(out), b // 1024, af // 1024, "" if out == f else "  (was %s)" % os.path.basename(f)))
    print("%d file(s), %.1f MB -> %.1f MB" % (n, tb / 1e6, ta / 1e6))


if __name__ == "__main__":
    main()
