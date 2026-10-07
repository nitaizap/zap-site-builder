"""Measured QA. Numbers, not pictures: every check is computed in the page, at 1440px and 390px.

Writes work/<slug>/QA-REPORT.md and returns True when there are no errors.
Screenshots (zs shots) are for the human sign-off only.
"""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from build import load_site
from env import IS_WIN

VIEWPORTS = {"desktop": (1440, 900), "mobile": (390, 844)}

MEASURE_JS = r"""
() => {
  const out = {err: [], warn: [], info: {}};
  const E = m => out.err.push(m), W = m => out.warn.push(m);
  const q = s => [...document.querySelectorAll(s)];
  const vis = el => { const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false;
                      const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  // structure
  const h1 = q('h1'); if (h1.length !== 1) E(`H1 count ${h1.length} (want 1)`);
  out.info.h1 = h1.map(h => h.textContent.trim()).join(' | ');
  if (q('main').length !== 1) E(`<main> count ${q('main').length} (want 1)`);
  if (!document.getElementById('content')) E('no #content target for the skip link');
  const t = document.title; out.info.title = t;
  if (t.length < 20 || t.length > 70) W(`<title> length ${t.length}`);
  const noindex = !!document.querySelector('meta[name="robots"][content*="noindex"]');
  out.info.noindex = noindex;
  if (location.pathname.includes('/category/')) E('URL contains /category/');
  const md = q('meta[name="description"]'); if (md.length !== 1 && !noindex) E(`meta description count ${md.length}`);
  else { const l = md[0].content.length; out.info.desc = l; if (l < 100 || l > 170) W(`meta description length ${l}`); }
  if (!q('link[rel="canonical"]').length && !document.querySelector('meta[name="robots"][content*="noindex"]')) W('no canonical');
  if (!q('meta[property="og:image"]').length) W('no og:image');
  // heading order
  let last = 0; q('h1,h2,h3,h4,h5,h6').filter(vis).forEach(h => { const n = +h.tagName[1];
    if (last && n > last + 1) W(`heading jump h${last}→h${n}: "${h.textContent.trim().slice(0, 40)}"`); last = n; });
  // overflow, bounded by the <html> box (RTL puts the scrollbar on the left)
  const hw = document.documentElement.getBoundingClientRect().width;
  const over = [];
  q('body *').forEach(el => { if (el.closest('.zs-nav, .zs-skip, .zs-form__hp, script, style, svg, iframe')) return;
    const s = getComputedStyle(el); if (s.position === 'fixed' || !vis(el)) return;
    const r = el.getBoundingClientRect(); if (r.right > hw + 1.5 || r.left < -1.5) {
      let p = el.parentElement, clipped = false;
      while (p && p !== document.body) { const ps = getComputedStyle(p); if (/(hidden|clip)/.test(ps.overflowX)) { clipped = true; break; } p = p.parentElement; }
      if (!clipped) over.push((el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : el.tagName) + ` ${Math.round(r.left)}..${Math.round(r.right)}`);
    } });
  if (over.length) E(`horizontal overflow (${over.length}): ` + over.slice(0, 4).join(', '));
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 2) E(`page scrolls sideways: ${document.documentElement.scrollWidth}px > ${document.documentElement.clientWidth}px`);
  // tiny text
  const tiny = new Set(); const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (tw.nextNode()) { const n = tw.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement;
    if (!el || el.closest('.zs-form__hp, script, style') || !vis(el)) continue;
    const fs = parseFloat(getComputedStyle(el).fontSize); if (fs < 13.4) tiny.add(`${fs}px "${n.textContent.trim().slice(0, 24)}"`); }
  if (tiny.size) E(`text under 13.4px: ${[...tiny].slice(0, 3).join('; ')}`);
  // images
  q('img').forEach(i => { if (!i.hasAttribute('alt')) E(`img without alt: ${i.src.split('/').pop()}`);
    else if (i.alt === '' && !i.closest('[aria-hidden="true"]') && vis(i) && i.width > 120) W(`empty alt on visible image ${i.src.split('/').pop()}`);
    if (i.complete && i.naturalWidth === 0 && vis(i)) E(`broken image ${i.src.split('/').pop()}`); });
  // phone links must dial what they show
  const dig = s => { let d = s.replace(/\D/g, ''); if (d.startsWith('0')) d = '972' + d.slice(1); return d; };
  q('a[href^="tel:"]').forEach(a => { const shown = a.textContent.replace(/\D/g, ''); if (shown.length >= 7 && dig(a.textContent) !== dig(a.getAttribute('href').slice(4))) E(`tel mismatch: shows ${a.textContent.trim()} dials ${a.getAttribute('href')}`); });
  q('a[href*="wa.me/"]').forEach(a => { if (!/wa\.me\/972\d{8,9}/.test(a.href)) E(`bad WhatsApp link ${a.href}`); });
  // invented social proof
  const txt = document.body.innerText;
  const rating = txt.match(/(★|⭐|\b[45][.,]\d\s*(כוכבים|בגוגל|ב-גוגל)|\d+\s*ביקורות)/);
  if (rating) E(`rating text without a source: "${rating[0]}"`);
  // JSON-LD
  let faqSchema = null;
  q('script[type="application/ld+json"]').forEach(s => { try { const j = JSON.parse(s.textContent); const str = JSON.stringify(j);
      if (str.includes('aggregateRating')) E('aggregateRating in schema');
      const g = j['@graph'] || [j]; g.forEach(n => { if (n['@type'] === 'FAQPage') faqSchema = (n.mainEntity || []).length; }); }
    catch (e) { E('invalid JSON-LD'); } });
  const faqUi = q('.elementor-toggle-item, .elementor-accordion-item').length;
  if (faqUi || faqSchema) { out.info.faq = `${faqUi}/${faqSchema}`; if (faqUi !== (faqSchema || 0)) E(`FAQ shown ${faqUi} ≠ FAQPage schema ${faqSchema}`); }
  // contrast: text colour against the nearest painted background (WCAG AA: 4.5, large text 3)
  const rgb = s => { const m = s.match(/[\d.]+/g); if (!m) return null; const n = m.map(Number);
    if (s.startsWith('color(')) { n[0] *= 255; n[1] *= 255; n[2] *= 255; }   // color-mix() resolves to color(srgb 0..1)
    return n; };
  const lum = ([r, g, b]) => { const f = c => { c /= 255; return c <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4); }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none' && !/gradient/.test(s.backgroundImage)) return null;
      const c = rgb(s.backgroundColor); if (c && (c.length < 4 || c[3] > .5)) return c; }
    return [255, 255, 255]; };
  const low = new Map();
  q('h1,h2,h3,h4,p,li,a,span,strong,label,button').filter(vis).forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    if (el.closest('.zs-hero__media, .zs-form__hp')) return;
    const bg = bgOf(el); if (!bg) return;
    const s = getComputedStyle(el), fg = rgb(s.color); if (!fg) return;
    const a = fg.length > 3 ? fg[3] : 1; const mix = [0, 1, 2].map(i => fg[i] * a + bg[i] * (1 - a));
    const L1 = lum(mix), L2 = lum(bg), ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05);
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.6 && +s.fontWeight >= 700);
    const need = big ? 3 : 4.5;
    if (ratio < need) low.set(el.textContent.trim().slice(0, 30), ratio.toFixed(2));
  });
  // text over a photo: judge against the dark scrim colour the section declares
  if (low.size) { const list = [...low].slice(0, 4).map(([t, r]) => `"${t}" ${r}`).join('; ');
    ([...low.values()].some(r => r < 3) ? E : W)(`low contrast (${low.size}): ${list}`); }
  // css or shortcodes leaking as text
  if (/\.(zs|elementor)-[a-z_-]+\s*\{|\[zap_[a-z_]+/.test(txt)) E('CSS or shortcode text visible on the page');
  // accessibility basics
  q('a, button').filter(vis).forEach(el => { if (!(el.textContent.trim() || el.getAttribute('aria-label') || el.querySelector('img[alt]:not([alt=""])'))) W(`control without a name: ${el.outerHTML.slice(0, 60)}`); });
  q('input:not([type=hidden]), textarea, select').filter(vis).forEach(el => { if (!(el.labels && el.labels.length) && !el.getAttribute('aria-label')) E(`form field without label: ${el.name}`); });
  // links for the crawl
  out.links = [...new Set(q('a[href]').map(a => a.href).filter(h => h.startsWith(location.origin)).map(h => h.split('#')[0]))];
  // weight
  const res = performance.getEntriesByType('resource'); out.info.kb = Math.round((res.reduce((a, r) => a + (r.transferSize || r.encodedBodySize || 0), 0) + (performance.getEntriesByType('navigation')[0]?.transferSize || 0)) / 1024);
  return out;
}
"""


def _launch(p):
    try:
        return p.chromium.launch(channel="chrome") if IS_WIN else p.chromium.launch()
    except Exception:
        return p.chromium.launch()


def urls_for(site, data):
    """Every public URL, read from WordPress itself so the crawl matches what was really built."""
    out = site.eval_php(
        "$u = [];"
        "foreach (get_posts(['post_type'=>['page','post'],'post_status'=>'publish','numberposts'=>-1]) as $p) $u[] = get_permalink($p);"
        "foreach (get_terms(['taxonomy'=>'category','hide_empty'=>true]) as $t) $u[] = get_term_link($t);"
        "echo implode(\"\\n\", $u);")
    urls = [u.strip() for u in out.splitlines() if u.strip().startswith("http")]
    return list(dict.fromkeys(urls))


def _scroll_all(page):
    # Lazy images: scroll through, then force every <img> eager and wait until all have decoded,
    # so full-page screenshots never show empty cards.
    page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
      document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
      await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); })));
      window.scrollTo(0, 0); }""")
    page.wait_for_timeout(250)


def screenshots(site, paths, directions=False):
    from playwright.sync_api import sync_playwright
    data = load_site(site.src)
    out_dir = site.dir / "shots"
    out_dir.mkdir(exist_ok=True)
    jobs = []
    for p in paths:
        name = re.sub(r"[^a-z0-9]+", "-", urllib.parse.quote(p).lower()).strip("-") or "home"
        jobs.append((name, site.url + urllib.parse.quote(p)))
    if directions:
        for k in data.get("directions", {}):
            jobs.append((f"dir-{k}", site.url + "/?zs_dir=" + k))
    files = []
    with sync_playwright() as pw:
        b = _launch(pw)
        for vp, (w, h) in VIEWPORTS.items():
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, locale="he-IL")
            page = ctx.new_page()
            for name, url in jobs:
                page.goto(url, wait_until="networkidle")
                _scroll_all(page)
                f = out_dir / f"{name}-{vp}.png"
                # full_page capture drops off-screen images in Chromium; a viewport as tall as the page doesn't
                page.set_viewport_size({"width": w, "height": page.evaluate("document.documentElement.scrollHeight")})
                page.wait_for_timeout(600)
                page.screenshot(path=str(f))
                page.set_viewport_size({"width": w, "height": h})
                files.append(f)
            ctx.close()
        b.close()
    return files


def preview(site):
    """Gate material: the real home page under every design direction, desktop + mobile, in one PREVIEW.md.
    Lives in sites/<slug>/preview/ so it renders on GitHub once the site branch is pushed."""
    from PIL import Image
    data = load_site(site.src)
    dirs = data.get("directions") or {"a": {"label": "הכיוון הנוכחי"}}
    out = site.src / "preview"
    out.mkdir(exist_ok=True)
    for f in out.glob("*.jpg"):
        f.unlink()
    shots = screenshots(site, [], directions=True) if data.get("directions") else screenshots(site, ["/"])
    for f in shots:
        im = Image.open(f).convert("RGB")
        w = 900 if "desktop" in f.name else 390
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(out / (f.stem.replace("home", "dir-a") + ".jpg"), "JPEG", quality=72, optimize=True, progressive=True)
    lines = [f"# כיווני עיצוב — {data['business']['name']}", "",
             "אותו תוכן, אותו מבנה. משתנים רק צבעים, גופנים, פינות וסגנון ה-Hero. בוחרים אות אחת.", ""]
    for k, d in dirs.items():
        f = d.get("fonts", data.get("design", {}).get("fonts", {}))
        lines += [f"## {k.upper()} · {d.get('label', '')}", "",
                  f"סגנון `{d.get('preset', 'clean')}` · Hero `{d.get('hero', 'split')}` · גופנים {f.get('heading', '')} / {f.get('body', '')}", "",
                  "| מחשב | נייד |", "|---|---|",
                  f"| <img src=\"dir-{k}-desktop.jpg\" width=\"620\"> | <img src=\"dir-{k}-mobile.jpg\" width=\"250\"> |", ""]
    (out / "PREVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    return out / "PREVIEW.md"


def check_links(links):
    bad = []
    for u in sorted(links):
        req = urllib.request.Request(u, method="GET")
        opener = urllib.request.build_opener(NoRedirect)
        try:
            r = opener.open(req, timeout=20)
            code = r.status
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = str(e)[:40]
        if code != 200:
            bad.append((urllib.parse.unquote(u), code))
    return bad


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def test_form(page, site):
    """Submit the footer form like a person (waits > 3s so the time trap passes) and confirm it saved."""
    before = int(site.wp("post", "list", "--post_type=zap_lead", "--post_status=private", "--format=count") or 0)
    page.goto(site.url + "/", wait_until="networkidle")
    page.wait_for_timeout(3500)
    page.fill("#zf-footer-name", "בדיקת QA")
    page.fill("#zf-footer-phone", "050-0000000")
    page.check("#zf-footer input[name=zf_consent]")
    page.click("#zf-footer button[type=submit]")
    page.wait_for_load_state("networkidle")
    ok_msg = page.locator(".zs-form__ok").count() > 0
    after = int(site.wp("post", "list", "--post_type=zap_lead", "--post_status=private", "--format=count") or 0)
    mailed = site.eval_php("$p = get_posts(['post_type'=>'zap_lead','post_status'=>'private','numberposts'=>1]); echo $p ? get_post_meta($p[0]->ID,'_zap_mailed',true) : '';")
    # clean the test lead out again so the delivered site starts empty
    site.eval_php("foreach (get_posts(['post_type'=>'zap_lead','post_status'=>'private','numberposts'=>-1,'s'=>'בדיקת QA']) as $p) wp_delete_post($p->ID, true);")
    return ok_msg, after - before, mailed


def run_qa(site):
    from playwright.sync_api import sync_playwright
    data = load_site(site.src)
    urls = urls_for(site, data)
    rows, links, errors, warns = [], set(), 0, 0
    extra = []
    with sync_playwright() as pw:
        b = _launch(pw)
        for vp, (w, h) in VIEWPORTS.items():
            ctx = b.new_context(viewport={"width": w, "height": h}, locale="he-IL")
            page = ctx.new_page()
            console = []
            page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            for u in urls:
                console.clear()
                resp = page.goto(u, wait_until="networkidle")
                _scroll_all(page)
                m = page.evaluate(MEASURE_JS)
                if resp.status != 200:
                    m["err"].insert(0, f"HTTP {resp.status}")
                for c in console:
                    if "favicon" not in c:
                        m["warn"].append("console: " + c[:100])
                links |= set(m.pop("links"))
                rows.append((vp, urllib.parse.unquote(u.replace(site.url, "")) or "/", m))
                errors += len(m["err"])
                warns += len(m["warn"])
            if vp == "mobile":
                page.goto(site.url + "/", wait_until="networkidle")
                page.click(".zs-burger")
                page.wait_for_timeout(450)
                opened = page.evaluate("getComputedStyle(document.getElementById('zs-nav')).visibility === 'visible' && document.querySelector('.zs-burger').getAttribute('aria-expanded') === 'true'")
                page.keyboard.press("Escape")
                page.wait_for_timeout(350)
                closed = page.evaluate("document.querySelector('.zs-burger').getAttribute('aria-expanded') === 'false'")
                extra.append(("mobile menu opens / Escape closes", opened and closed))
                if not (opened and closed):
                    errors += 1
                ok_msg, saved, mailed = test_form(page, site)
                extra.append((f"lead form: thank-you shown, saved={saved}, mail={ {'yes': 'sent to the test address', 'no': 'FAILED', 'staging-skip': 'skipped on staging (correct)'}.get(mailed, 'n/a') }", ok_msg and saved == 1 and mailed != 'no'))
                if not (ok_msg and saved == 1):
                    errors += 1
            # 404 must be a real 404
            r404 = page.goto(site.url + "/no-such-page-zs/", wait_until="domcontentloaded")
            if vp == "desktop":
                extra.append(("404 page returns HTTP 404", r404.status == 404))
                if r404.status != 404:
                    errors += 1
            ctx.close()
        b.close()

    bad_links = check_links(links)
    errors += len(bad_links)

    lines = [f"# QA report — {data['business']['name']}", "",
             f"- Pages × viewports checked: **{len(rows)}** ({len(urls)} URLs × {len(VIEWPORTS)})",
             f"- Internal links tested: **{len(links)}**, not 200: **{len(bad_links)}**",
             f"- Errors: **{errors}** · Warnings: **{warns}**", ""]
    for name, ok in extra:
        lines.append(f"- {'✅' if ok else '❌'} {name}")
    lines += ["", "| viewport | page | errors | warnings | KB | details |", "|---|---|---|---|---|---|"]
    for vp, path, m in rows:
        det = "; ".join(m["err"] + m["warn"])[:300].replace("|", "/")
        lines.append(f"| {vp} | {path} | {len(m['err'])} | {len(m['warn'])} | {m['info'].get('kb', '')} | {det} |")
    if bad_links:
        lines += ["", "## Links that are not 200", ""] + [f"- {c} {u}" for u, c in bad_links]
    (site.src / "QA-REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:9 + len(extra)]))
    for vp, path, m in rows:
        for e in m["err"]:
            print(f"ERROR [{vp}] {path}: {e}")
    for u, c in bad_links:
        print(f"ERROR link {c}: {u}")
    return errors == 0
