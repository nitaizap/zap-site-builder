"""zs static: a browsable offline copy of the built site (open index.html, no server).

For looking, not for launch: every page, link, image, font, animation and the hero video work from
file://; the lead form only shows a notice and the Dapei Zahav reviews need the live domain.
Windows-safe: no '?' or other reserved characters in file names (WordPress adds ?ver= to assets).
"""
import base64
import re
import shutil
import subprocess
import urllib.parse
import zipfile
from pathlib import Path

RESERVED = re.compile(r'[?:*"<>|\\]')
NOTE = ('<script>document.addEventListener("submit",function(e){e.preventDefault();'
        'alert("עותק תצוגה מקומי: הטופס פעיל רק באתר החי.");},true);</script>')


def export(site, out_zip=None):
    base = site.url.rstrip("/")
    tmp = site.dir / "static"
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    subprocess.run(["wget", "--no-proxy", "-q", "-e", "robots=off", "--recursive", "--level=5", "--page-requisites",
                    "--convert-links", "--adjust-extension", "--restrict-file-names=nocontrol", "--no-host-directories",
                    "--reject-regex", r"(wp-json|xmlrpc|wp-login|/feed/|\?p=|comments|wp-admin|oembed|replytocom)",
                    base + "/"], cwd=tmp, check=False)
    if not (tmp / "index.html").exists():
        raise SystemExit(f"static export failed: is {base} running? (zs serve {site.slug})")

    # media the crawler cannot see: hero videos (data-src) and Elementor's lazily loaded JS chunks
    for f in tmp.rglob("*.html"):
        for src in re.findall(r'data-src="' + re.escape(base) + r'/([^"]+)"', f.read_text(encoding="utf-8")):
            src = urllib.parse.unquote(src)
            dst = tmp / src
            if not dst.exists() and (site.dir / "wp" / src).exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(site.dir / "wp" / src, dst)
    chunks = site.dir / "wp/wp-content/plugins/elementor/assets/js/chunks"
    if chunks.exists():
        d = tmp / "wp-content/plugins/elementor/assets/js/chunks"
        d.mkdir(parents=True, exist_ok=True)
        for c in chunks.glob("*.js"):
            shutil.copy2(c, d / c.name)

    # Windows-safe names: main.css?ver=1.2.css -> main.css
    renamed = {}
    for f in sorted(tmp.rglob("*"), key=lambda p: -len(p.parts)):
        if f.is_file() and RESERVED.search(f.name):
            new = f.with_name(RESERVED.split(f.name, 1)[0] if "?" in f.name else RESERVED.sub("-", f.name))
            if new.exists():
                new.unlink()
            f.rename(new)
            renamed[f.name] = new.name

    # fonts embedded (browsers block font files from file:// in some setups)
    for css in (tmp / "wp-content/themes/zap-base/fonts").glob("*.css"):
        t = css.read_text(encoding="utf-8")
        t = re.sub(r"url\(([^)]+?\.woff2)\)",
                   lambda m: "url(data:font/woff2;base64," + base64.b64encode((css.parent / m.group(1)).read_bytes()).decode() + ")", t)
        css.write_text(t, encoding="utf-8")

    for f in [*tmp.rglob("*.html"), *tmp.rglob("*.css"), *tmp.rglob("*.js")]:
        t = f.read_text(encoding="utf-8", errors="surrogateescape")
        o = t
        for old, new in renamed.items():
            for form in (old, old.replace("?", "%3F"), urllib.parse.quote(old, safe="=-._~")):
                t = t.replace(form, new)
        if f.suffix == ".html":
            pre = "../" * (len(f.relative_to(tmp).parts) - 1)
            t = re.sub(r'<link[^>]+(wp-json|oembed|xmlrpc|EditURI)[^>]*>\s*', "", t)
            t = re.sub(r'<link rel="preload"[^>]+as="font"[^>]*>\s*', "", t)
            t = t.replace(base + "/", pre).replace(base.replace("/", "\\/") + "\\/", pre.replace("/", "\\/"))
            t = t.replace(base, pre or "./")
            if NOTE not in t:
                t = t.replace("</body>", NOTE + "</body>", 1)
        if t != o:
            f.write_text(t, encoding="utf-8", errors="surrogateescape")

    (tmp / "README.txt").write_text(
        "עותק תצוגה מקומי\n\n1. מחלצים את כל התיקייה (Extract all) - לא לפתוח מתוך ה-zip.\n"
        "2. פותחים את index.html בדפדפן.\n\nלא פעיל בעותק המקומי: שליחת הטופס וביקורות דפי זהב (רק באתר החי).\n",
        encoding="utf-8")
    out_zip = Path(out_zip or site.src.parent.parent / "dist" / f"{site.slug}-preview.zip")
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(tmp.rglob("*")):
            if f.is_file():
                rel = f.relative_to(tmp).as_posix()
                assert not RESERVED.search(rel), rel
                z.write(f, f"{site.slug}-preview/{rel}")
    return out_zip, len(list(tmp.rglob("index.html")))
