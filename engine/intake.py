"""zs intake: turn a sites-team email (Word spec sheets + body) into ready-to-build site folders.

Runs on the machine that can see the client images (Windows with the F: drive). Stdlib only, so it
works without extra installs; Pillow, when present, shrinks oversized photos.

One email may carry several clients (one spec sheet per client). Spec sheets come as Word
(.docx, the "בייסיק" template) or Excel (.xlsx, the "וויקנד" template). For each spec:
  * client id   = the 8-digit Zap customer id (file name first, then the document text)
  * slug        = c<id>  (stable, Latin, the same id that names the F: folder)
  * writes      sites/<slug>/brief/<spec>         the original (.docx or .xlsx)
                sites/<slug>/brief/brief.md      the spec as text (paragraphs + tables), + the email body
                sites/<slug>/intake.json         id, name, package, sender, subject, links, staging URL, status
                sites/<slug>/assets/client/*     images copied from <images-root>/**/<id>*/
Nothing is invented: what is not found stays empty and is listed under "missing".
"""
import json
import re
import shutil
import sys
import urllib.parse
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
SPEC_EXT = (".docx", ".xlsx")
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


# ---------- Excel ----------

def _col(ref):
    """"B12" -> 1 (0-based column index)."""
    n = 0
    for ch in ref:
        if not ch.isalpha():
            break
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def _shared_strings(z):
    if "xl/sharedStrings.xml" not in z.namelist():
        return []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    return ["".join(t.text or "" for t in si.iter(S + "t")) for si in root.findall(S + "si")]


def _cell_text(c, shared):
    t = c.get("t")
    if t == "inlineStr":
        is_ = c.find(S + "is")
        return "".join(x.text or "" for x in is_.iter(S + "t")) if is_ is not None else ""
    v = c.find(S + "v")
    if v is None or v.text is None:
        return ""
    if t == "s":
        i = int(v.text)
        return shared[i] if 0 <= i < len(shared) else ""
    if t == "b":
        return "TRUE" if v.text.strip() == "1" else "FALSE"
    return v.text


def xlsx_text(path):
    """Same shape as docx_text: the sheets as `a | b | c` rows, plus the hyperlink targets.

    The "וויקנד" template is a two-sheet workbook ("כללי" + "איפיון עמודים") of label/value rows,
    so every row becomes one `label | value` line, exactly what spec_fields() already reads.
    The site tree ("עץ אתר") is the one field written across the row *below* its label, so it is
    re-emitted as a single `עץ אתר | page | page | ...` line.
    """
    lines, links = [], []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        shared = _shared_strings(z)
        order = []
        if "xl/workbook.xml" in names:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            rels = {}
            if "xl/_rels/workbook.xml.rels" in names:
                for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")):
                    rels[r.get("Id")] = r.get("Target")
            for sh in wb.iter(S + "sheet"):
                tgt = rels.get(sh.get(R + "id"), "")
                tgt = tgt[1:] if tgt.startswith("/") else "xl/" + tgt.lstrip("/")
                if tgt in names:
                    order.append((sh.get("name") or "", tgt))
        if not order:
            order = [("", n) for n in sorted(n for n in names
                                             if n.startswith("xl/worksheets/") and n.endswith(".xml"))]
        for sheet_name, target in order:
            root = ET.fromstring(z.read(target))
            head, tail = target.rsplit("/", 1)
            rel_path = head + "/_rels/" + tail + ".rels"
            ext = {}
            if rel_path in names:
                for r in ET.fromstring(z.read(rel_path)):
                    if r.get("TargetMode") == "External":
                        ext[r.get("Id")] = r.get("Target")
            for h in root.iter(S + "hyperlink"):
                u = ext.get(h.get(R + "id")) or h.get("location") or ""
                if u.startswith("http"):
                    links.append(u)
            rows = []                                    # one entry per non-empty row: [(column, text)]
            for row in root.iter(S + "row"):
                cells = [(_col(c.get("r") or "A"), t)
                         for c in row.findall(S + "c") for t in [_cell_text(c, shared).strip()] if t]
                if cells:
                    rows.append(cells)
            if sheet_name:
                lines.append("## " + sheet_name)
            for cells in rows:                           # a wide gap starts a second label/value pair
                group, prev = [], None
                for col, txt in cells:
                    if prev is not None and col - prev >= 3:
                        lines.append(" | ".join(group))
                        group = []
                    group.append(txt)
                    prev = col
                if group:
                    lines.append(" | ".join(group))
            for i, cells in enumerate(rows[:-1]):        # the site tree sits one row below its label
                for col, txt in cells:
                    if txt.startswith("עץ אתר"):
                        tree = [t for c2, t in rows[i + 1] if c2 >= col]
                        if tree:
                            lines.append("עץ אתר | " + " | ".join(tree))
            lines.append("")
    return "\n".join(lines).strip(), sorted(set(links))


def spec_text(path):
    """(text, links) for a spec sheet, Word or Excel."""
    return xlsx_text(path) if Path(path).suffix.lower() == ".xlsx" else docx_text(path)


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
    for p in PACKAGES[:4]:   # a whole word only: "פרו" must not match inside "פרויקט"
        if re.search(r"(?<![֐-ת])" + p + r"(?![֐-ת])", text[:400]):
            return p
    return ""


SAFELINK_RE = re.compile(r"https?://[\w.-]*safelinks\.protection\.outlook\.com/\S*", re.I)


def unwrap_safelinks(text):
    """Replace every Outlook safelink wrapper with the real URL it hides.

    Outlook rewrites links as
    `https://eur04.safelinks.protection.outlook.com/?url=<percent-encoded url>&data=...`.
    Storing that is storing garbage, so the `url=` parameter is decoded and the wrapper dropped.
    A wrapper with no readable `url=` is removed entirely rather than left behind.
    """
    def one(m):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(m.group(0)).query)
        return (q.get("url") or [""])[0]
    return SAFELINK_RE.sub(one, text or "")


def is_staging_host(url):
    return (".ussl.co.il" in url or "staging" in url or ".1wp.site" in url or "clicksite.co.il" in url)


BARE_STAGING_RE = re.compile(r"(?<![\w.@/:-])((?:[\w-]+\.)+(?:ussl\.co\.il|1wp\.site|clicksite\.co\.il))")


def staging_urls(text):
    """[(client id or "", url), ...] for every staging URL in the text, in order, de-duplicated.

    Staging hosts are not uniformly named - `80392936.ussl.co.il`, `80392210kisos.ussl.co.il`
    and `erezbread80049225.ussl.co.il` are all real - but the 8-digit client id is embedded in
    the host, so the id in the host is what says whose site it is.
    """
    text = unwrap_safelinks(text)
    found = URL_RE.findall(text) + ["https://" + h for h in BARE_STAGING_RE.findall(text)]
    out, seen = [], set()
    for u in found:
        if not is_staging_host(u):
            continue
        parts = urllib.parse.urlparse(u.rstrip(".,"))
        host = parts.netloc.lower()
        if not host or host in seen:
            continue
        u = parts.scheme + "://" + host + "/"        # the site itself, not the /wp-login.php someone sent
        seen.add(host)
        ids = ID_RE.findall(host)
        out.append((ids[0] if len(ids) == 1 else "", u))
    return out


def staging_from(text, cid=""):
    """The staging URL for this client, or "".

    One email can carry several clients and name all of their staging sites, so a host
    holding a different 8-digit id belongs to somebody else and is skipped.
    """
    for found, u in staging_urls(text):
        if cid and found and found != cid:
            continue
        return u
    return ""


def body_lines_for(body, cid, name):
    """The email-body lines that mention this client (by id or name)."""
    return [l for l in (body or "").splitlines()
            if cid in l or (name and name.split()[0] in l)]


def body_links_for(body, cid, name):
    """Links on the email-body line that mentions this client (by id or name)."""
    out = []
    for line in body_lines_for(body, cid, name):
        out += [u.rstrip(".,") for u in URL_RE.findall(line)]
    return sorted(set(out))


SPEC_FIELDS = {   # label in Zap's spec template -> intake.json key
    "שם הלקוח": "contact_name", "שם העסק": "name", "מספר לקוח": "client_id", "עץ אתר": "sitemap", "דומיין": "domain",
    "אתר קיים": "old_site", "טלפון מסקיו": "phone_tracking", "טלפון ישיר לעסק": "phone_direct",
    "וואטסאפ": "whatsapp", "שעות פעילות": "hours", "כתובת": "address", "אימייל": "email", "GMB": "gmb",
    "פייסבוק": "facebook", "אינסטגרם": "instagram", "יוטיוב": "youtube", "לינקדין": "linkedin",
    "טוויטר": "twitter", "עמוד משלוחים / תפריט": "menu_url", "לוגו": "logo", "חומר גרפי גולמי": "raw_graphics",
    "צבעים": "colors", "רפרנסים": "references", "תבנית נבחרת": "template", "רסט": "rest", "דפי זהב": "dapei_zahav",
    # the "וויקנד" Excel template spells the same fields out in full
    "מס' לקוח": "client_id", "שם הלקוח בפרסום": "name", "מס' לקוח בוויקנד": "weekend_client_id",
    "ורטיקל": "vertical", "קישור לתבנית": "template",
    "טלפון ישיר לעסק (אליו מחובר המסקיו)": "phone_direct", "נייד לכפתור וואטסאפ": "whatsapp",
    "כתובת עסק": "address", "טיק טוק": "tiktok",
    "לוגו (קישור לסייט)": "logo", "חומר גרפי גולמי (קישור לסייט)": "raw_graphics",
    "צבעים מועדפים על הלקוח": "colors", "אתר כרפרנס 1": "reference_1", "אתר כרפרנס 2": "reference_2",
    "מה הלקוח אהב / לא אהב ברפרנסים?": "references_notes",
    "אם כן, איזו כתובת דומיין? האם הכתובת תקינה?": "domain_requested",
    "כמה עמודים האתר הקיים": "old_site_pages", "סיכום שיחה עם מת\"ל": "call_summary",
    "קישור לסרטון 360": "video_360", "האם להציג חוות דעת באתר?": "reviews",
    "הנחיות כלליות לעורך": "content_notes", "הנחיות כלליות למעצב": "design_notes",
    "סגנון עריכה": "writing_style", "פנייה לגולשי האתר": "audience_address",
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
        docs += sorted(f for e in SPEC_EXT for f in p.glob("*" + e)) if p.is_dir() else [p]
    docs = [d for d in docs if d.suffix.lower() in SPEC_EXT and not d.name.startswith("~$")]
    if not docs:
        raise SystemExit("intake: no .docx/.xlsx spec sheets found in " + ", ".join(map(str, inputs)))
    results = []
    for doc in docs:
        text, doc_links = spec_text(doc)
        m = ID_RE.search(doc.stem) or ID_RE.search(text)
        cid = m.group(1) if m else ""
        if not cid:
            results.append({"file": doc.name, "error": "no 8-digit client id in file name or text"})
            continue
        slug = "c" + cid
        spec = spec_fields(text)
        name = spec.get("name") or spec.get("contact_name") or name_from_filename(doc.stem, cid)
        links = sorted(set(doc_links + [u.rstrip(".,") for u in URL_RE.findall(text)] + body_links_for(body, cid, name)))
        info = {
            "client_id": cid, "slug": slug, "branch": "site/" + slug, "name": name,
            "package": package_from(doc.stem, text),
            "spec_file": doc.name, "sender": sender, "subject": subject,
            "received": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "staging_url": staging or staging_from(text, cid)
                           or staging_from("\n".join(body_lines_for(body, cid, name)), cid),
            "links": links,
            "zap_pages": {"dapei_zahav": f"https://www.d.co.il/{cid}/"},
            "spec": spec,
            "image_sources": sorted({u for u in links if "wetransfer" in u or "drive.google" in u or "dropbox" in u
                                     or "rest.co.il" in u or "instagram" in u
                                     or "sharepoint.com" in u}),
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
        other = sorted({i for i in ID_RE.findall(subject or "") if i != cid})
        if other:
            info["missing"].append(
                "client id: the spec sheet says %s, the email subject says %s - %s used (the file wins)"
                % (cid, ", ".join(other), cid))
        if not info["package"]:
            info["missing"].append("package: no package named in the file name or the spec sheet")
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
    x = sub.add_parser("intake", help="sites-team email (.docx/.xlsx specs + body) -> sites/c<id>/ with brief + images")
    x.add_argument("inputs", nargs="+", help=".docx/.xlsx spec sheets, or a folder holding them")
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
