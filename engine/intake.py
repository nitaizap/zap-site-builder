"""zs intake: turn a sites-team email (Word spec sheets + body) into ready-to-build site folders.

Runs on the machine that can see the client images (Windows with the F: drive). Stdlib only, so it
works without extra installs; Pillow, when present, shrinks oversized photos.

One email may carry several clients (one .docx spec per client). For each .docx:
  * client id   = the 8-digit Zap customer id (file name first, then the document text)
  * slug        = c<id>  (stable, Latin, the same id that names the F: folder)
  * writes      sites/<slug>/brief/<spec>.docx    the original
                sites/<slug>/brief/brief.md      the spec as text (paragraphs + tables), + the email body
                sites/<slug>/intake.json         id, name, package, sender, subject, links, staging URL, status
                sites/<slug>/assets/client/*     images copied from <images-root>/**/<id>*/
Nothing is invented: what is not found stays empty and is listed under "missing".
"""
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ID_RE = re.compile(r"(?<!\d)(\d{8})(?!\d)")
URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".bmp", ".tif", ".tiff", ".heic", ".ai", ".eps", ".pdf"}
PACKAGES = ("בייסיק", "פרימיום", "פלוס", "פרו", "basic", "premium", "plus", "pro")
MAX_PX = 2400


# ---------- Word ----------

def _para_text(p):
    out = []
    for node in p.iter():
        if node.tag == W + "t" and node.text:
            out.append(node.text)
        elif node.tag in (W + "tab",):
            out.append("\t")
        elif node.tag in (W + "br", W + "cr"):
            out.append("\n")
    return "".join(out).strip()


def docx_text(path):
    """Body text in reading order; tables as `a | b | c` rows. Links (hyperlink targets) appended."""
    with zipfile.ZipFile(path) as z:
        root = ET.fromstring(z.read("word/document.xml"))
        rels = {}
        if "word/_rels/document.xml.rels" in z.namelist():
            for r in ET.fromstring(z.read("word/_rels/document.xml.rels")):
                if r.get("TargetMode") == "External":
                    rels[r.get("Id")] = r.get("Target")
    body = root.find(W + "body")
    lines = []
    for el in body:
        if el.tag == W + "p":
            t = _para_text(el)
            if t:
                lines.append(t)
        elif el.tag == W + "tbl":
            for tr in el.iter(W + "tr"):
                cells = [" ".join(_para_text(p) for p in tc.iter(W + "p")).strip() for tc in tr.findall(W + "tc")]
                if any(cells):
                    lines.append(" | ".join(cells))
            lines.append("")
    links = sorted(set(rels.values()))
    return "\n".join(lines).strip(), links


# ---------- parsing ----------

def name_from_filename(stem, cid):
    s = stem
    s = re.sub(r"\(\d+\)", "", s)
    s = re.sub(r"_\d+$", "", s.strip())
    if cid:
        s = s.replace(cid, " ")
    for p in PACKAGES:
        s = re.sub(r"[-–_]\s*" + re.escape(p), " ", s, flags=re.I)
    s = re.sub(r"[-–_]+\s*$", "", s.strip())
    return re.sub(r"\s+", " ", s).strip(" -–_")


def package_from(stem, text):
    for p in PACKAGES:
        if p.lower() in stem.lower():
            return p
    for p in PACKAGES[:4]:
        if p in text[:400]:
            return p
    return ""


def staging_from(text):
    for u in URL_RE.findall(text or ""):
        if ".ussl.co.il" in u or "staging" in u or ".1wp.site" in u or "clicksite.co.il" in u:
            return u.rstrip(".,/") + "/"
    return ""


def body_links_for(body, cid, name):
    """Links on the email-body line that mentions this client (by id or name)."""
    out = []
    for line in (body or "").splitlines():
        if cid in line or (name and name.split()[0] in line):
            out += [u.rstrip(".,") for u in URL_RE.findall(line)]
    return sorted(set(out))


SPEC_FIELDS = {   # label in Zap's spec template -> intake.json key
    "שם הלקוח": "name", "מספר לקוח": "client_id", "עץ אתר": "sitemap", "דומיין": "domain",
    "אתר קיים": "old_site", "טלפון מסקיו": "phone_tracking", "טלפון ישיר לעסק": "phone_direct",
    "וואטסאפ": "whatsapp", "שעות פעילות": "hours", "כתובת": "address", "אימייל": "email", "GMB": "gmb",
    "פייסבוק": "facebook", "אינסטגרם": "instagram", "יוטיוב": "youtube", "לינקדין": "linkedin",
    "טוויטר": "twitter", "עמוד משלוחים / תפריט": "menu_url", "לוגו": "logo", "חומר גרפי גולמי": "raw_graphics",
    "צבעים": "colors", "רפרנסים": "references", "תבנית נבחרת": "template", "רסט": "rest", "דפי זהב": "dapei_zahav",
}


def spec_fields(text):
    """First `label | value` row per known label (later sections reuse labels like H1, so first wins)."""
    out = {}
    for line in text.splitlines():
        if " | " not in line:
            continue
        k, v = (x.strip() for x in line.split(" | ", 1))
        key = SPEC_FIELDS.get(k)
        if key and v and key not in out:
            out[key] = v
    return out


# ---------- images ----------

def find_client_dirs(root, cid, depth=4):
    root = Path(root)
    if (root / cid).is_dir():             # Zap layout: F:\SiteContent\<id>\
        return [root / cid]
    hits, stack = [], [(root, 0)]
    while stack:
        d, lvl = stack.pop()
        try:
            kids = [k for k in d.iterdir() if k.is_dir()]
        except OSError:
            continue
        for k in kids:
            if cid in k.name:
                hits.append(k)
            elif lvl + 1 < depth:
                stack.append((k, lvl + 1))
    return hits


def copy_images(dirs, dest):
    dest.mkdir(parents=True, exist_ok=True)
    try:
        from PIL import Image
    except ImportError:
        Image = None
    copied = []
    for d in dirs:
        for f in sorted(d.rglob("*")):
            if not f.is_file() or f.suffix.lower() not in IMG_EXT:
                continue
            rel = f.relative_to(d)
            name = "_".join(rel.parts)
            name = re.sub(r"[^\w.\-א-ת]+", "-", name)
            out = dest / name
            if Image and f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                try:
                    im = Image.open(f)
                    if max(im.size) > MAX_PX:
                        im.thumbnail((MAX_PX, MAX_PX))
                        im.save(out, quality=88)
                        copied.append(name)
                        continue
                except Exception:
                    pass
            shutil.copy2(f, out)
            copied.append(name)
    return copied


# ---------- main ----------

def intake(inputs, images_root=None, sender="", subject="", body="", staging="", sites_dir=None, dry_run=False):
    sites_dir = Path(sites_dir or ROOT / "sites")
    docs = []
    for i in inputs:
        p = Path(i)
        docs += sorted(p.glob("*.docx")) if p.is_dir() else [p]
    docs = [d for d in docs if d.suffix.lower() == ".docx" and not d.name.startswith("~$")]
    if not docs:
        raise SystemExit("intake: no .docx spec sheets found in " + ", ".join(map(str, inputs)))
    results = []
    for doc in docs:
        text, doc_links = docx_text(doc)
        m = ID_RE.search(doc.stem) or ID_RE.search(text)
        cid = m.group(1) if m else ""
        if not cid:
            results.append({"file": doc.name, "error": "no 8-digit client id in file name or text"})
            continue
        slug = "c" + cid
        spec = spec_fields(text)
        name = spec.get("name") or name_from_filename(doc.stem, cid)
        links = sorted(set(doc_links + [u.rstrip(".,") for u in URL_RE.findall(text)] + body_links_for(body, cid, name)))
        info = {
            "client_id": cid, "slug": slug, "branch": "site/" + slug, "name": name,
            "package": package_from(doc.stem, text),
            "spec_file": doc.name, "sender": sender, "subject": subject,
            "received": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "staging_url": staging or staging_from(text) or staging_from(body),
            "links": links,
            "zap_pages": {"dapei_zahav": f"https://www.d.co.il/{cid}/"},
            "spec": spec,
            "image_sources": sorted({u for u in links if "wetransfer" in u or "drive.google" in u or "dropbox" in u
                                     or "rest.co.il" in u or "instagram" in u}),
            "images": [], "image_dirs": [], "missing": [], "status": "intake",
        }
        if any("rest.co.il" in u for u in links):
            info["zap_pages"]["rest"] = f"https://www.rest.co.il/rest/{cid}/"
        site = sites_dir / slug
        if images_root:
            dirs = find_client_dirs(images_root, cid)
            info["image_dirs"] = [str(d) for d in dirs]
            if not dirs:
                info["missing"].append(f"no folder with {cid} in its name under {images_root}")
            elif not dry_run:
                info["images"] = copy_images(dirs, site / "assets" / "client")
        else:
            info["missing"].append("images: no --images-root given")
        if not info["staging_url"]:
            info["missing"].append("staging URL (the sites team sends it later)")
        if not dry_run:
            (site / "brief").mkdir(parents=True, exist_ok=True)
            shutil.copy2(doc, site / "brief" / doc.name)
            md = [f"# {name} ({cid})", "", f"- from: {sender}", f"- subject: {subject}",
                  f"- package: {info['package']}", f"- staging: {info['staging_url'] or '(not yet)'}", ""]
            if body.strip():
                md += ["## Email body", "", body.strip(), ""]
            md += ["## Spec sheet: " + doc.name, "", text, ""]
            if doc_links:
                md += ["## Links in the spec", ""] + [f"- {u}" for u in doc_links] + [""]
            (site / "brief" / "brief.md").write_text("\n".join(md), encoding="utf-8")
            (site / "intake.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")
        results.append(info)
    return results


def cli(a):
    body = Path(a.body_file).read_text(encoding="utf-8") if a.body_file else ""
    import os
    root = a.images_root or os.environ.get("ZS_IMAGES_ROOT") or (r"F:\SiteContent" if os.name == "nt" else None)
    res = intake(a.inputs, root, a.sender or "", a.subject or "", body, a.staging or "", dry_run=a.dry_run)
    print(json.dumps(res, ensure_ascii=False, indent=2))
    if any("error" in r for r in res):
        sys.exit(1)


def add_parser(sub):
    x = sub.add_parser("intake", help="sites-team email (.docx specs + body) -> sites/c<id>/ with brief + images")
    x.add_argument("inputs", nargs="+", help=".docx files or a folder holding them")
    x.add_argument("--images-root", help=r"default F:\SiteContent (holds one folder per client id)")
    x.add_argument("--sender"); x.add_argument("--subject"); x.add_argument("--staging")
    x.add_argument("--body-file", help="the email body saved as UTF-8 text")
    x.add_argument("--dry-run", action="store_true")
    x.set_defaults(f=cli)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(prog="intake")
    add_parser(ap.add_subparsers(dest="cmd", required=True))
    a = ap.parse_args(["intake"] + sys.argv[1:])
    a.f(a)
