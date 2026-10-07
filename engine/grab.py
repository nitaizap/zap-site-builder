"""Research a client's existing web presence in one command (a real headless browser, so JS sites work).

  zs grab <slug> <url> [--pages 25]

- Crawls the site (same host), falling back to the newest Wayback Machine snapshot when the live site
  is down, blocked or gone (403/404/5xx/timeouts) - old client sites are often exactly that.
- Writes sites/<slug>/research/<host>.md: per page the title, headings, main text (trimmed), and across
  the site every phone, email, WhatsApp, address-looking line, social link, opening-hours line.
- Downloads the logo candidates (og:image, <img> with "logo" in src/alt/class, apple-touch-icon) and
  every content image >= 500px wide into sites/<slug>/research/img/ with a manifest (src, alt, size).

Facts found here still need judgement: the brief wins over the old site, and anything used on the new
site is recorded in NOTES.md with its source URL.
"""
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"

PAGE_JS = r"""
() => {
  const clean = s => (s || '').replace(/\s+/g, ' ').trim();
  const main = document.querySelector('main, article, #content, .content') || document.body;
  const heads = [...document.querySelectorAll('h1,h2,h3')].map(h => h.tagName + ': ' + clean(h.innerText)).filter(x => x.length > 4).slice(0, 40);
  const text = clean(main.innerText).slice(0, 6000);
  const links = [...document.querySelectorAll('a[href]')].map(a => a.href);
  const imgs = [...document.images].map(i => ({src: i.currentSrc || i.src, alt: i.alt || '', w: i.naturalWidth, h: i.naturalHeight,
      logo: /logo/i.test((i.src || '') + ' ' + (i.alt || '') + ' ' + (i.className || '') + ' ' + (i.closest('header') ? 'header' : ''))}));
  const bg = [...document.querySelectorAll('[style*="background"]')].map(e => (getComputedStyle(e).backgroundImage.match(/url\("?(.*?)"?\)/) || [])[1]).filter(Boolean);
  const meta = n => (document.querySelector(`meta[property="${n}"], meta[name="${n}"]`) || {}).content || '';
  const icon = (document.querySelector('link[rel="apple-touch-icon"], link[rel="icon"][sizes]') || {}).href || '';
  return {title: document.title, heads, text, links, imgs, bg, og: meta('og:image'), desc: meta('description'), icon};
}
"""


def _wayback(url):
    """Newest good snapshot of the home page (www / non-www, http / https), else of any page on the domain.
    The CDX index is used because the 'available' API misses www/http variants."""
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    def cdx(q):
        api = ("https://web.archive.org/cdx/search/cdx?" + q +
               "&output=json&limit=-3&filter=statuscode:200&filter=mimetype:text/html&fl=timestamp,original")
        for _ in range(3):                       # the CDX index is slow and flaky: retry before giving up
            try:
                req = urllib.request.Request(api, headers={"User-Agent": UA})
                rows = json.loads(urllib.request.urlopen(req, timeout=90).read() or b"[]")[1:]
                return rows[-1] if rows else None
            except Exception:
                continue
        return None
    for q in (f"url=www.{host}/", f"url={host}/", f"url={host}&matchType=domain"):
        hit = cdx(q)
        if hit:
            return f"https://web.archive.org/web/{hit[0]}/{hit[1]}"
    return None


def _download(url, dest):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": url})
        data = urllib.request.urlopen(req, timeout=40).read()
        if len(data) < 2000:
            return 0
        dest.write_bytes(data)
        return len(data)
    except Exception:
        return 0


def grab(site, url, max_pages=25):
    from playwright.sync_api import sync_playwright
    from qa import _launch
    if not url.startswith("http"):
        url = "https://" + url
    out = site.src / "research"
    (out / "img").mkdir(parents=True, exist_ok=True)
    host = urllib.parse.urlparse(url).netloc.replace("www.", "")
    pages, seen, queue, images, source = [], set(), [url], {}, "live"
    ids, gmb, socials = set(), set(), set()
    with sync_playwright() as pw:
        b = _launch(pw)
        ctx = b.new_context(user_agent=UA, locale="he-IL", viewport={"width": 1366, "height": 900})
        pg = ctx.new_page()
        first = True
        while queue and len(pages) < max_pages:
            u = queue.pop(0)
            key = re.sub(r"[#?].*$", "", u).rstrip("/")
            if key in seen:
                continue
            seen.add(key)
            try:
                r = pg.goto(u, wait_until="domcontentloaded", timeout=40000)
                pg.wait_for_timeout(1500)
                status = r.status if r else 0
            except Exception:
                status = 0
            if first and (status == 0 or status >= 400):
                wb = _wayback(url)
                if not wb:
                    b.close()
                    return f"{url} answered {status or 'nothing'} and has no Wayback snapshot. Ask the user for the material."
                source, first = f"wayback ({wb})", False
                queue = [wb]
                seen.clear()
                continue
            first = False
            if status >= 400:
                continue
            d = pg.evaluate(PAGE_JS)
            raw = pg.content()
            for m in re.findall(r"customer-id=[\"']?(\d{5,})", raw) + re.findall(r"d\.co\.il/(\d{6,})", raw):
                ids.add(m)
            for m in re.findall(r'https?://(?:maps\.app\.goo\.gl|g\.page|share\.google|goo\.gl/maps)/[\w/?=&.-]+', raw):
                gmb.add(m)
            for m in re.findall(r"https?://(?:www\.)?(?:facebook|instagram|linkedin|youtube|tiktok)\.com/[^\s\"'<>)]+", raw):
                if "sharer" not in m and "/plugins/" not in m:
                    socials.add(re.sub(r"^https?://web\.archive\.org/web/\d+[a-z_]*/", "", m))
            pages.append({"url": u, **{k: d[k] for k in ("title", "heads", "text", "desc")}})
            for im in d["imgs"]:
                if im["src"].startswith("http") and (im["w"] >= 500 or im["logo"]):
                    images.setdefault(im["src"], im)
            for extra in [d["og"], d["icon"], *d["bg"]]:
                if extra and extra.startswith("http"):
                    images.setdefault(extra, {"src": extra, "alt": "", "w": 0, "h": 0, "logo": extra in (d["og"], d["icon"])})
            for l in d["links"]:
                lu = urllib.parse.urlparse(l)
                same = host in lu.netloc or ("web.archive.org" in lu.netloc and host in lu.path)
                if same and not re.search(r"\.(pdf|jpe?g|png|webp|gif|zip|docx?)$", lu.path, re.I) and len(queue) < 200:
                    queue.append(l)
        b.close()

    blob = "\n".join(p["text"] for p in pages)
    phones = sorted(set(re.findall(r"(?<!\d)(0\d{1,2}-?\d{7}|\+972[\d-]{8,12}|\*\d{4})(?!\d)", blob)))
    emails = sorted(set(re.findall(r"[\w.+-]+@[\w-]+\.[\w.]+", blob)))
    hours = sorted(set(l.strip() for l in re.findall(r"[^\n.]*(?:א['׳]|ב['׳]|ראשון|שישי|ו['׳])[^\n.]*\d{1,2}:\d{2}[^\n.]*", blob)))[:8]
    addr = sorted(set(re.findall(r"(?:רח(?:וב|')?\s)?[א-ת\"' ]{2,25}\s\d{1,3}(?:[,،]\s?[א-ת ]{2,20})", blob)))[:10]
    social = sorted(set(l for p in pages for l in re.findall(r"https?://(?:www\.)?(?:facebook|instagram|linkedin|youtube|tiktok)\.com/[^\s\"')]+", p["text"])))

    manifest = []
    for i, (src, im) in enumerate(images.items()):
        ext = (re.search(r"\.(jpe?g|png|webp|gif|svg)", src, re.I) or [None, "jpg"])[1].lower()
        name = f"{'logo-' if im['logo'] else ''}{i:02d}.{ext}"
        size = _download(src, out / "img" / name)
        if size:
            manifest.append({"file": f"research/img/{name}", "src": src, "alt": im.get("alt", ""), "w": im.get("w"), "logo": im["logo"], "kb": size // 1024})
    (out / "img" / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    md = [f"# Research — {host}", "", f"source: {source} · pages read: {len(pages)} · images saved: {len(manifest)}", "",
          "## Contact details found (verify before use; the brief wins)", "",
          f"- phones: {', '.join(phones) or '—'}", f"- emails: {', '.join(emails) or '—'}",
          f"- address-like lines: {' | '.join(addr) or '—'}", f"- hours-like lines: {' | '.join(hours) or '—'}",
          f"- social: {', '.join(sorted(set(social) | socials)) or '—'}",
          f"- Dapei Zahav customer-id candidates (verify name+address+phone on d.co.il before use): {', '.join(sorted(ids)) or '—'}",
          f"- Google Business links: {', '.join(sorted(gmb)) or '—'}", "", "## Pages", ""]
    for p in pages:
        md += [f"### {p['title']}", p["url"], "", f"_meta description:_ {p['desc']}", "", *[f"- {h}" for h in p["heads"]], "",
               p["text"][:2500], ""]
    f = out / f"{host}.md"
    f.write_text("\n".join(md), encoding="utf-8")
    return f"{f}\n{len(pages)} pages from {source}; {len(manifest)} images in research/img (logo candidates: {sum(1 for m in manifest if m['logo'])})"
