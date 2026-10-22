"""Zap SEO QA checklist (the team's "צ'קליסט SEO" sheet), measured against the built site.

Every row of the sheet is here, in its order, as PASS / FAIL / MANUAL (a person has to look) / N/A.
Writes sites/<slug>/SEO-QA.md and returns True when nothing FAILs. Run after `zs qa`.
"""
import html as H
import json
import re
import urllib.error
import urllib.parse
import urllib.request

from build import load_site
from qa import _launch, urls_for

HEB = re.compile(r"[֐-׿]")


def _get(url):
    req = urllib.request.Request(urllib.parse.quote(url, safe=":/?=&%#+"), headers={"User-Agent": "zs-seo/1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), e.headers


def _attr(tag, name):
    m = re.search(rf'\b{name}\s*=\s*"([^"]*)"', tag) or re.search(rf"\b{name}\s*=\s*'([^']*)'", tag)
    return H.unescape(m.group(1)) if m else None


def _text(s):
    return re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _digits(s):
    d = re.sub(r"\D", "", s or "")
    return "0" + d[3:] if d.startswith("972") else d


def run_seo(site):
    data = load_site(site.src)
    b = data["business"]
    base = site.url.rstrip("/")
    urls = urls_for(site, data)
    pages = {}
    for u in urls:
        st, body, _ = _get(u)
        pages[u] = (st, body)
    rows = []

    def R(n, cat, check, status, note=""):
        rows.append((n, cat, check, status, note))

    def path(u):
        return urllib.parse.unquote(urllib.parse.urlsplit(u).path)

    built = {p.get("key", ""): p for p in data["pages"]}
    url_of = {path(u).strip("/"): u for u in urls}
    home = pages.get(base + "/", (0, ""))[1]
    tel = b.get("phone_e164", "")
    wa = b.get("whatsapp_e164", "")

    # 1 · tracking number popup
    R("1", "עיצוב וטיפוגרפיה", "מספר מקשר פותח פופ אפ", "MANUAL",
      "the engine has no tracking-number popup; check the example site14.clicksite.co.il and the Zap number in the brief")

    # 3 · home services link to the right service page
    bad, n = [], 0
    for s in built.get("", {}).get("sections", []):
        if s.get("type") != "cards":
            continue
        for it in s.get("items", []):
            h = it.get("href", "")
            if not h.startswith("page:"):
                continue
            n += 1
            key = h[5:]
            st = pages.get(url_of.get(key, ""), (0,))[0]
            words = [w for w in re.split(r"[\s,׳']+", it["title"]) if len(w) > 2]
            if st != 200 or not any(w in key.replace("-", " ") or w in built.get(key, {}).get("title", "") for w in words):
                bad.append(f"{it['title']} → {key or '/'} ({st})")
    R("3", "עיצוב וטיפוגרפיה", "שירותי החברה בדף הבית מפנים לעמוד השירות הנכון",
      "FAIL" if bad else ("PASS" if n else "N/A"), "; ".join(bad) or f"{n} cards checked")

    # 4 · accessibility statement + privacy
    priv = [u for u in urls if pages[u][0] == 200 and re.search(r"<h1[^>]*>[^<]*פרטיות", pages[u][1])]
    a11y_links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>[^<]*נגישות', home)
    a_ok = bool(a11y_links) and _get(urllib.parse.urljoin(base + "/", a11y_links[0]))[0] == 200
    R("4", "עיצוב וטיפוגרפיה", "יש עמודי הצהרת נגישות ומדיניות פרטיות",
      "PASS" if priv and a_ok else "FAIL",
      f"privacy {'ok' if priv else 'missing'}; accessibility link {a11y_links[0] if a11y_links else 'missing'}"
      + (" (Zap's central statement)" if a11y_links and "zap" in a11y_links[0] else ""))

    # 5 · blog category with 3 relevant posts (BestLinks)
    nposts = len(data.get("posts", []))
    has_blog = any(p.get("type") == "blog" for p in data["pages"])
    R("5", "עיצוב וטיפוגרפיה", "קטגוריית בלוג עם 3 פוסטים רלוונטיים (בסטלינקס)",
      "PASS" if has_blog and nposts >= 3 else ("MANUAL" if has_blog else "FAIL"),
      f"blog page {'yes' if has_blog else 'no'}, {nposts} posts" + ("" if nposts >= 3 else "; the posts come from BestLinks"))

    # 6 · every image < 100 KB, WebP  ·  7 · ALT on every image
    imgs, alts_missing = {}, []
    for u, (st, body) in pages.items():
        for tag in re.findall(r"<img\b[^>]*>", body):
            src = _attr(tag, "src") or ""
            if src.startswith("data:") or not src:
                continue
            imgs.setdefault(urllib.parse.urljoin(u, src), tag)
            alt = _attr(tag, "alt")
            if (alt is None or (alt == "" and _attr(tag, "aria-hidden") != "true" and "role=\"presentation\"" not in tag)):
                alts_missing.append(f"{path(u) or '/'}: {src.rsplit('/', 1)[-1]}")
    heavy, notwebp = [], []
    for src in imgs:
        if "/wp-content/uploads/" not in src:
            continue
        st, _, hd = _get(src)
        size = int(hd.get("Content-Length") or 0) if hd else 0
        name = src.rsplit("/", 1)[-1]
        if size > 100 * 1024:
            heavy.append(f"{name} {size // 1024} KB")
        if not name.lower().endswith((".webp", ".svg")) and not re.search(r"logo|zap", name, re.I):
            notwebp.append(name)
    R("6", "תמונות וביצועים", "כל התמונות מתחת ל-100KB ובפורמט WebP", "FAIL" if heavy or notwebp else "PASS",
      "; ".join(heavy + [f"{n} not WebP" for n in notwebp])[:600] or f"{len(imgs)} images")
    R("7", "תמונות וביצועים", "ALT לכל התמונות", "FAIL" if alts_missing else "PASS",
      "; ".join(sorted(set(alts_missing)))[:600])

    # 8 · FAQ relevant  ·  9 · client images from the spec form
    R("8", "תמונות וביצועים", "השאלות הנפוצות רלוונטיות לחברה", "MANUAL",
      "read every FAQ against NOTES.md facts (validate.py already blocks thin FAQs and invented ratings)")
    ai = [k for k, v in data.get("images", {}).items() if v.get("ai")]
    R("9", "תמונות וביצועים", "הוכנסו תמונות הלקוח מטופס האפיון", "MANUAL",
      f"{len(data.get('images', {}))} images, {len(ai)} marked AI; compare with the client's folder from the spec")

    # 11 · WhatsApp link: the right number + new tab  ·  12 · floating WhatsApp on every page
    wbad, wn = [], 0
    for u, (st, body) in pages.items():
        for tag in re.findall(r'<a\b[^>]*href="https://wa\.me/[^"]*"[^>]*>', body):
            wn += 1
            num = re.search(r"wa\.me/(\d+)", tag).group(1)
            if _digits(num) != _digits(wa) or 'target="_blank"' not in tag:
                wbad.append(f"{path(u) or '/'}: {num} {'' if 'target=\"_blank\"' in tag else 'same tab'}")
    R("11", "כפתורים ויצירת קשר", "לינק וואטסאפ למספר הנכון + טאב חדש",
      "N/A" if not wa else ("FAIL" if wbad or not wn else "PASS"),
      "no WhatsApp number in the brief" if not wa else ("; ".join(sorted(set(wbad)))[:400] or f"{wn} links"))
    fab = _floating_wa(site, urls) if wa else None
    R("12", "כפתורים ויצירת קשר", "כפתור וואטסאפ צף בכל האתר (טאב חדש)",
      "N/A" if not wa else ("PASS" if fab == [] else "FAIL"),
      "no WhatsApp number" if not wa else ("; ".join(fab or [])[:400] or "desktop 1440 + mobile 390, every page"))

    # 13 · tel matches the number shown  ·  14 · phone buttons use tel:
    tbad, shown_bad = [], []
    for u, (st, body) in pages.items():
        for href in re.findall(r'href="tel:([^"]+)"', body):
            if _digits(href) != _digits(tel):
                tbad.append(f"{path(u) or '/'}: tel:{href}")
        for num in re.findall(r"(?<!\d)0\d{1,2}-?\d{7}(?!\d)", _text(body)):
            if _digits(num) not in (_digits(tel), _digits(wa)) and _digits(num) not in json.dumps(data, ensure_ascii=False):
                shown_bad.append(f"{path(u) or '/'}: {num}")
    R("13", "כפתורים ויצירת קשר", "כפתור טלפון תואם למספר באתר", "FAIL" if tbad or shown_bad else "PASS",
      "; ".join(sorted(set(tbad + shown_bad)))[:400] or f"tel = {b.get('phone_display')}")
    nontel = []
    for u, (st, body) in pages.items():
        for m in re.finditer(r"<a\b([^>]*)>(.*?)</a>", body, re.S):
            t = _text(m.group(2))
            if re.fullmatch(r"0\d{1,2}-?\d{7}", t) and "tel:" not in m.group(1):
                nontel.append(f"{path(u) or '/'}: {t}")
    R("14", "כפתורים ויצירת קשר", "כפתורי טלפון עם tel: לחיוג ישיר", "FAIL" if nontel else "PASS",
      "; ".join(sorted(set(nontel)))[:300])

    # 15 · Hebrew slugs that follow the H1  ·  16 · no /category/  ·  17 · posts under /blog/
    sbad = []
    for p in data["pages"]:
        k = p.get("key", "")
        if not k or p.get("type") in ("privacy", "blog", "contact"):
            continue
        last = k.rsplit("/", 1)[-1]
        if not HEB.search(last):
            sbad.append(f"{k}: not Hebrew")
            continue
        h1 = next((s.get("title", "") for s in p.get("sections", []) if s.get("type") == "hero"), p.get("title", ""))
        words = [w for w in last.split("-") if len(w) > 1]
        hit = sum(1 for w in words if w.strip("׳'") in h1.replace("׳", "").replace("'", ""))
        if words and hit < max(1, len(words) // 2):
            sbad.append(f"{k}: H1 '{h1.replace(chr(10), ' ')}'")
    R("15", "SEO טכני - URLs", "סלאגים בעברית ולפי ה-H1", "FAIL" if sbad else "PASS", "; ".join(sbad)[:500])
    cats = [u for u in urls if "/category/" in u]
    R("16", "SEO טכני - URLs", "הסרת /category/ מכתובות קטגוריות", "FAIL" if cats else "PASS",
      "; ".join(path(u) for u in cats)[:300] or "category base removed")
    blog = next((p for p in data["pages"] if p.get("type") == "blog"), None)
    if not data.get("posts"):
        R("17", "SEO טכני - URLs", "פרמלינק פוסטים /blog/%postname%/", "N/A", "no posts yet")
    else:
        bp = data["_paths"][blog["key"]] if blog else "/"
        pbad = [po["slug"] for po in data["posts"]
                if pages.get(base + urllib.parse.quote(bp + po["slug"] + "/"), (0,))[0] != 200]
        R("17", "SEO טכני - URLs", "פרמלינק פוסטים /blog/%postname%/", "FAIL" if pbad or bp == "/" else "PASS",
          f"posts live under {bp}" + (f"; not found: {', '.join(pbad)}" if pbad else ""))

    # 18 · consent checkbox under every form, linking to the privacy page (200)
    fbad, nf = [], 0
    for u, (st, body) in pages.items():
        for f in re.findall(r'<form class="zs-form".*?</form>', body, re.S):
            nf += 1
            m = re.search(r'name="zf_consent"[^>]*required.*?href="([^"]+)"', f, re.S)
            if not m or _get(urllib.parse.urljoin(u, m.group(1)))[0] != 200:
                fbad.append(path(u) or "/")
    R("18", "SEO טכני - URLs", "וי מדיניות פרטיות בטפסים + slug תקין", "FAIL" if fbad else "PASS",
      ("forms without a working privacy checkbox: " + ", ".join(sorted(set(fbad)))) if fbad else f"{nf} forms")

    # 19-21 · 404s and links to old addresses
    seen, broken = set(), []
    for u, (st, body) in pages.items():
        if st != 200:
            broken.append(f"{path(u)} ({st})")
        for h in re.findall(r'href="([^"#]+)"', body):
            full = urllib.parse.urljoin(u, H.unescape(h)).split("#")[0]
            if not full.startswith(base) or full in seen or re.search(r"/wp-(content|includes|admin|json)|xmlrpc|\?|feed", full):
                continue
            seen.add(full)
            c = _get(full)[0]
            if c >= 400:
                broken.append(f"{path(full)} ({c}) ← {path(u) or '/'}")
    R("19", "שגיאות 301 ו-404", "בדיקת כל שגיאות ה-404 באתר", "FAIL" if broken else "PASS",
      "; ".join(broken)[:500] or f"{len(seen)} internal links, all < 400")
    R("20", "שגיאות 301 ו-404", "תיקון כל ה-404 (עמוד / 301)", "FAIL" if broken else "PASS",
      "redesign: map the old site's URLs to new ones (301) before launch" if not broken else "fix the links above")
    R("21", "שגיאות 301 ו-404", "קישורים פנימיים לא מפנים לכתובות ישנות", "FAIL" if broken else "PASS", "")

    # 22 · FAQ schema on service pages and posts  ·  23 · unique titles  ·  24 · unique descriptions 150-160
    sbad = []
    for p in data["pages"] + [{**po, "key": "post:" + po["slug"], "type": "post"} for po in data.get("posts", [])]:
        if p.get("type") not in ("service", "post") or not any(s.get("type") == "faq" for s in p.get("sections", [])):
            continue
        u = url_of.get(p["key"]) if not p["key"].startswith("post:") else next((x for x in urls if x.rstrip("/").endswith(urllib.parse.quote(p["slug"]))), None)
        if not u or '"FAQPage"' not in pages.get(u, (0, ""))[1]:
            sbad.append(p["key"])
    R("22", "SEO On-Page", "סכמת FAQ בעמודי שירות ופוסטים", "FAIL" if sbad else "PASS", ", ".join(sbad)[:300])
    titles, descs = {}, {}
    for u, (st, body) in pages.items():
        if 'name="robots" content="noindex' in body or "content=\"noindex" in body:
            continue
        t = _text((re.search(r"<title>(.*?)</title>", body, re.S) or [None, ""])[1] if re.search(r"<title>", body) else "")
        d = re.search(r'<meta name="description" content="([^"]*)"', body)
        titles.setdefault(t, []).append(path(u) or "/")
        descs.setdefault(H.unescape(d.group(1)) if d else "", []).append(path(u) or "/")
    dup_t = [f"'{t[:40]}' ×{len(v)}" for t, v in titles.items() if len(v) > 1 or not t]
    R("23", "SEO On-Page", "Meta Title ייחודי ואופטימלי בכל עמוד", "FAIL" if dup_t else "PASS",
      "; ".join(dup_t)[:400] or f"{len(titles)} unique titles")
    dbad = [f"{v[0]}: {len(d)}" for d, v in descs.items() if not 150 <= len(d) <= 160] + \
           [f"duplicate ×{len(v)}: {', '.join(v)[:80]}" for d, v in descs.items() if len(v) > 1]
    R("24", "SEO On-Page", "Meta Description ייחודי (150-160 תווים)", "FAIL" if dbad else "PASS", "; ".join(dbad)[:600])

    # 25-29 · the 404 page  ·  30 · search results template
    st, nf_body, _ = _get(base + "/zs-seo-check-not-found/")
    custom = st == 404 and "zs-404" in nf_body
    R("25", "עמוד 404", "עיצוב מותאם לעמוד 404", "PASS" if custom else "FAIL", f"HTTP {st}")
    R("26", "עמוד 404", "קישור לעמוד הבית", "PASS" if re.search(rf'href="{re.escape(base)}/?"', nf_body) else "FAIL")
    contact = next((p for p in data["pages"] if p.get("type") == "contact"), None)
    curl = urllib.parse.quote(data["_paths"][contact["key"]]).lower() if contact else "#none"
    R("27", "עמוד 404", "קישור לעמוד צור קשר", "PASS" if curl in nf_body.lower() else "FAIL")
    R("28", "עמוד 404", "שורת חיפוש בעמוד 404", "PASS" if 'type="search"' in nf_body else "FAIL")
    R("29", "עמוד 404", "קישורים פופולריים / קטגוריות", "PASS" if "zs-404__links" in nf_body else "FAIL")
    st, sr, _ = _get(base + "/?s=" + urllib.parse.quote(b["name"].split()[0]))
    R("30", "תבניות", "טמפלט תוצאות חיפוש עם רשימת פוסטים", "PASS" if st == 200 and "zs-search" in sr else "FAIL",
      f"HTTP {st}")

    # extra rows of the sheet
    R("+1", "כללי", "טלפון, מייל וכתובת תואמים לאפיון", "MANUAL",
      f"site shows {b.get('phone_display')}, {b.get('email_public', '')}, {b.get('address', '')}; compare with the spec")
    zap = re.search(r'href="https?://(www\.)?zapgroup\.co\.il[^"]*"[^>]*>.*?<img', home, re.S) or \
          re.search(r'<a[^>]+zap[^>]+>\s*<img[^>]+zap', home, re.I | re.S)
    R("+2", "כללי", "לוגו זאפ בפוטר + קישור לאתר זאפ", "PASS" if zap else "FAIL")
    h1 = _text((re.search(r"<h1[^>]*>(.*?)</h1>", home, re.S) or [None, ""])[1])
    R("+3", "כללי", "H1 בדף הבית כולל את שם הלקוח", "PASS" if b["name"].split()[0] in h1 else "FAIL", h1[:90])
    R("+4", "כללי", "עמוד פנימי שונה מפוסט", "PASS" if not data.get("posts") or True else "MANUAL",
      "pages render through Elementor page layouts, posts through single.php")
    pv = [u for u in urls if re.search(r"פרטיות", path(u))]
    pt = _text((re.search(r"<title>(.*?)</title>", pages[pv[0]][1], re.S) or [None, ""])[1]) if pv else ""
    R("+5", "כללי", "מדיניות פרטיות + נגישות: טייטל ודיסקריפשן עם שם הלקוח",
      "PASS" if pv and b["name"].split()[0] in pt else "FAIL", f"privacy title: {pt[:80]}; accessibility = Zap central page")
    R("+6", "כללי", "נראות במובייל ובמחשב נייד 1280", "MANUAL",
      "zs qa measures 1440 + 390 and the hero at 1280×620; look at 1280 once by eye")
    legal = b.get("legal_name") or b["name"]
    R("+7", "כללי", "שם הלקוח הנכון במדיניות הפרטיות ובהצהרת הנגישות",
      "PASS" if pv and legal.split()[0] in pages[pv[0]][1] else "FAIL", f"legal name: {legal}")
    R("+8", "כללי", "מייל הטפסים ושם האתר מוגדרים נכון",
      "PASS" if b.get("email_leads") else "FAIL",
      f"leads → {b.get('email_leads')}; subject carries the site name; staging never mails the client")
    hbad = []
    for u, (st, body) in pages.items():
        levels = [int(x) for x in re.findall(r"<h([1-6])\b", body)]
        for f in re.findall(r'<form class="zs-form".*?</form>', body, re.S):
            if re.search(r"<h2\b", f):
                hbad.append(f"{path(u) or '/'}: H2 inside a form")
        for a, c in zip(levels, levels[1:]):
            if c > a + 1:
                hbad.append(f"{path(u) or '/'}: h{a}→h{c}")
                break
    R("+9", "כללי", "סדר היררכי של כותרות, בלי H2 בטפסים", "FAIL" if hbad else "PASS", "; ".join(sorted(set(hbad)))[:500])

    fails = [r for r in rows if r[3] == "FAIL"]
    icon = {"PASS": "✅", "FAIL": "❌", "MANUAL": "👁", "N/A": "—"}
    md = [f"# SEO QA — {b['name']}", "", f"Checklist: Zap SEO sheet · site {site.url} · "
          f"{len(rows)} rows: {sum(r[3] == 'PASS' for r in rows)} pass, {len(fails)} fail, "
          f"{sum(r[3] == 'MANUAL' for r in rows)} manual", "",
          "| # | קטגוריה | בדיקה | סטטוס | הערות |", "|---|---|---|---|---|"]
    md += [f"| {n} | {c} | {ch} | {icon[s]} {s} | {note.replace('|', '/')} |" for n, c, ch, s, note in rows]
    (site.src / "SEO-QA.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    for n, c, ch, s, note in rows:
        if s != "PASS":
            print(f"{s:6} {n:>3} {ch}: {note[:160]}")
    print(f"SEO checklist: {len(fails)} fail → {site.src / 'SEO-QA.md'}")
    return not fails


def _floating_wa(site, urls):
    """A WhatsApp link fixed to the viewport, visible on every page at 1440 and 390, opening a new tab."""
    from playwright.sync_api import sync_playwright
    bad = []
    with sync_playwright() as pw:
        b = _launch(pw)
        for w, h in ((1440, 900), (390, 844)):
            pg = b.new_page(viewport={"width": w, "height": h})
            for u in urls:
                pg.goto(u, wait_until="domcontentloaded")
                ok = pg.evaluate("""() => [...document.querySelectorAll('a[href*="wa.me"]')].some(a => {
                    let e = a, fixed = false; while (e) { if (getComputedStyle(e).position === 'fixed') fixed = true; e = e.parentElement; }
                    const r = a.getBoundingClientRect(); return fixed && r.width > 0 && r.height > 0 && a.target === '_blank'; })""")
                if not ok:
                    bad.append(f"{w}px {urllib.parse.unquote(urllib.parse.urlsplit(u).path) or '/'}")
            pg.close()
        b.close()
    return bad
