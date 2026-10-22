"""Image preparation before WordPress sees a file: cap width, convert to WebP, keep it light.

Logos keep their format (PNG/SVG transparency matters) but are still capped in size.
"""
from pathlib import Path

from PIL import Image, ImageOps

TARGET_KB = 100      # photos: step quality down until under this (Zap SEO checklist: every image < 100 KB, WebP)
MIN_QUALITY = 60


def prepare_image(src: Path, out_dir: Path, keep_format=False, max_width=1600):
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = src.stem.lower().replace(" ", "-")
    if src.suffix.lower() == ".svg":
        dst = out_dir / (stem + ".svg")
        dst.write_bytes(src.read_bytes())
        return dst, 0, 0
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.width > max_width:
        im = im.resize((max_width, round(im.height * max_width / im.width)), Image.LANCZOS)
    if keep_format:
        dst = out_dir / (stem + ".png")
        if im.mode not in ("RGBA", "LA", "P"):
            im = im.convert("RGB")
        im.save(dst, "PNG", optimize=True)
        return dst, im.width, im.height
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA" if "transparency" in im.info else "RGB")
    dst = out_dir / (stem + ".webp")
    q = 82
    while True:
        im.save(dst, "WEBP", quality=q, method=6)
        if dst.stat().st_size <= TARGET_KB * 1024 or q <= MIN_QUALITY:
            break
        q -= 6
    for w in (1400, 1200, 1000):          # still heavy: shrink until it fits
        if dst.stat().st_size <= TARGET_KB * 1024 or im.width <= w:
            continue
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, "WEBP", quality=MIN_QUALITY + 8, method=6)
    return dst, im.width, im.height
