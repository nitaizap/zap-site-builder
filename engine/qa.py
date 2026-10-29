"""Measured QA. Numbers, not pictures: every check is computed in the page, at 1440px and 390px.

Writes work/<slug>/QA-REPORT.md and returns True when there are no errors.
Screenshots (zs shots) are for the human sign-off only.
"""
import html
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
  else if (md.length) { const l = md[0].content.length; out.info.desc = l; if (l < 100 || l > 170) W(`meta description length ${l}`); }
  if (!q('link[rel="canonical"]').length && !document.querySelector('meta[name="robots"][content*="noindex"]')) W('no canonical');
  if (!q('meta[property="og:image"]').length) W('no og:image');
  // heading order
  let last = 0; q('h1,h2,h3,h4,h5,h6').filter(vis).forEach(h => { const n = +h.tagName[1];
    if (last && n > last + 1) W(`heading jump h${last}→h${n}: "${h.textContent.trim().slice(0, 40)}"`); last = n; });
  // overflow, bounded by the <html> box (RTL puts the scrollbar on the left)
  const hw = document.documentElement.getBoundingClientRect().width;
  const over = [];
  q('body *').forEach(el => { if (el.closest('.zs-nav, .zs-skip, .zs-form__hp, script, style, svg, iframe, [id^="pojo-a11y"], [class*="pojo-a11y"], #ea11y-root')) return;   // Zap's accessibility toolbar: closed panel off-screen by design
    const s = getComputedStyle(el); if (s.position === 'fixed' || !vis(el)) return;
    const r = el.getBoundingClientRect(); if (r.right > hw + 1.5 || r.left < -1.5) {
      let p = el.parentElement, clipped = false;
      while (p && p !== document.body) { const ps = getComputedStyle(p); if (/(hidden|clip|auto|scroll)/.test(ps.overflowX)) { clipped = true; break; } p = p.parentElement; }
      if (!clipped) over.push((el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : el.tagName) + ` ${Math.round(r.left)}..${Math.round(r.right)}`);
    } });
  if (over.length) E(`horizontal overflow (${over.length}): ` + over.slice(0, 4).join(', '));
  if (document.documentElement.scrollWidth > document.documentElement.clientWidth + 2) E(`page scrolls sideways: ${document.documentElement.scrollWidth}px > ${document.documentElement.clientWidth}px`);
  // tiny text
  const tiny = new Set(); const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (tw.nextNode()) { const n = tw.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement;
    if (!el || el.closest('.zs-form__hp, script, style, [id^="pojo-a11y"], [class*="pojo-a11y"], #ea11y-root') || !vis(el)) continue;
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
  const faqUi = q('.elementor-toggle-item, .elementor-accordion-item, details.zs-faq__item').length;
  if (faqUi || faqSchema) { out.info.faq = `${faqUi}/${faqSchema}`; if (faqUi !== (faqSchema || 0)) E(`FAQ shown ${faqUi} ≠ FAQPage schema ${faqSchema}`); }
  // contrast: text colour against the nearest painted background (WCAG AA: 4.5, large text 3)
  const rgb = s => { const m = s.match(/[\d.]+/g); if (!m) return null; const n = m.map(Number);
    if (s.startsWith('color(')) { n[0] *= 255; n[1] *= 255; n[2] *= 255; }   // color-mix() resolves to color(srgb 0..1)
    return n; };
  const lum = ([r, g, b]) => { const f = c => { c /= 255; return c <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4); }; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const bgOf = el => { for (let e = el; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (e.classList && e.classList.contains('zs-card--img')) {   // text over a photo tile: judge against the tile's shade
        for (const ps of ['::after', '::before']) { const pb = getComputedStyle(e, ps);
          const g = pb.display !== 'none' && pb.content !== 'none' ? pb.backgroundImage : '', m = g && /gradient/.test(g) && g.match(/rgba?\([^)]+\)/);
          if (m) return rgb(m[0]).slice(0, 3); } }
      if (s.backgroundImage !== 'none' && !/gradient/.test(s.backgroundImage)) return null;
      const c = rgb(s.backgroundColor); if (c && (c.length < 4 || c[3] > .5)) return c; }
    return [255, 255, 255]; };
  const flat = (fg, bg) => { const a = fg.length > 3 ? fg[3] : 1; return [0, 1, 2].map(i => fg[i] * a + bg[i] * (1 - a)); };
  const cr = (x, y) => { const L1 = lum(x), L2 = lum(y); return (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05); };
  const behind = el => { for (let e = el.parentElement; e; e = e.parentElement) { const s = getComputedStyle(e);
      if (s.backgroundImage !== 'none' && !/gradient/.test(s.backgroundImage)) return null;
      if (e.matches('.zs-hero__media, .zs-card__img, .zs-split__media, picture')) return null;
      const c = rgb(s.backgroundColor); if (c && (c.length < 4 || c[3] > .5)) return c.slice(0, 3); }
    return [255, 255, 255]; };
  const skip = '.zs-hero__media, .zs-form__hp, [aria-hidden="true"], #pojo-a11y-toolbar, script, style, noscript';
  // every element that carries its own text must meet WCAG AA (4.5, large text 3): below it is an error
  const low = new Map(), grey = new Map(), small = new Map();
  q('body *').filter(vis).forEach(el => {
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    if (el.closest(skip)) return;   // decorative text (marquee, wordmark) is hidden from AT
    const bg = bgOf(el); if (!bg) return;
    const s = getComputedStyle(el), fg = rgb(s.color); if (!fg) return;
    const ratio = cr(flat(fg, bg.slice(0, 3)), bg.slice(0, 3));
    const big = parseFloat(s.fontSize) >= 24 || (parseFloat(s.fontSize) >= 18.6 && +s.fontWeight >= 700);
    if (ratio < 4.5) low.set(el.textContent.trim().slice(0, 30), ratio.toFixed(2));   // Zap QA: 4.5 for every size (red titles on navy passed WCAG's 3 for large text and were rejected)
    // body copy in grey reads as faded (Zap QA): paragraphs and list items need 6:1
    else if (el.matches('main p, main li') && parseFloat(s.fontSize) < 22 && ratio < 6 && lum(bg.slice(0, 3)) > .5)   // grey copy on a light ground grey.set(el.textContent.trim().slice(0, 30), ratio.toFixed(2));
    // nothing under 16px (Zap QA: top bar, labels, form fields, consent, footer, copyright)
    if (parseFloat(s.fontSize) < 15.5 && !el.closest('.screen-reader-text, .sr-only, .elementor-screen-only')) small.set(el.textContent.trim().slice(0, 30), parseFloat(s.fontSize).toFixed(1) + 'px');
  });
  if (low.size) E(`low text contrast (${low.size}): ${[...low].slice(0, 4).map(([t, r]) => `"${t}" ${r}`).join('; ')}`);
  if (grey.size) E(`body text too grey (${grey.size}, needs 6:1): ${[...grey].slice(0, 4).map(([t, r]) => `"${t}" ${r}`).join('; ')}`);
  if (small.size) E(`text under 16px (${small.size}): ${[...small].slice(0, 5).map(([t, r]) => `"${t}" ${r}`).join('; ')}`);
  // Zap QA checklist items, measured on every page
  if (q('.zs-leadband h2, .zs-footer h2, footer h2').length) E('repeated blocks (lead form, footer columns) use <h2>; they must not be headings');
  const ico = document.querySelector('link[rel~="icon"]');
  if (!ico) E('no favicon'); else if (!/favicon|cropped/i.test(ico.href)) W(`favicon may be the base site's: ${ico.href.split('/').pop()}`);
  const flogo = document.querySelector('.zs-footer a[href$="/"] img, footer a[href$="/"] img, .zs-footer__logo img');
  if (!flogo) E('no client logo in the footer (linking home)');
  const hlogo = document.querySelector('.zs-brand img');
  if (hlogo && vis(hlogo) && hlogo.getBoundingClientRect().height < (innerWidth < 768 ? 40 : 46)) E(`header logo too small: ${Math.round(hlogo.getBoundingClientRect().height)}px tall`);
  const pv = [...document.querySelectorAll('footer a, .zs-footer a')].find(a => /פרטיות/.test(a.textContent));
  if (pv && pv.target !== '_blank') E('footer privacy link must open in a new tab');
  const addr = [...document.querySelectorAll('.zs-footer__contact li, .zs-nap li')].find(li => li.querySelector('.zs-ico') && /\d/.test(li.textContent) && !/[@:]|^\s*0\d/.test(li.textContent.trim()) && /[א-ת]{3,}/.test(li.textContent) && !/[א-ת]׳?[–-]/.test(li.textContent));
  if (addr && !addr.querySelector('a[href*="waze.com"]')) E(`address is not a Waze link: "${addr.textContent.trim().slice(0, 30)}"`);
  if (innerWidth < 768) {
    const cta = document.querySelector('.zs-header__cta');
    if (cta && !document.body.classList.contains('zs-no-mcall') && (!vis(cta) || getComputedStyle(cta).visibility === 'hidden')) E('no phone icon in the mobile header');
    const hm = document.querySelector('.zs-hero--home .zs-hero__media'), hh = document.querySelector('.zs-hero--home h1');
    if (hm && hh && vis(hm)) { const g = hh.getBoundingClientRect().top - hm.getBoundingClientRect().bottom; if (g > 90) E(`empty band between the hero photo and the H1 on phones: ${Math.round(g)}px`); }
    const tb = document.querySelector('#pojo-a11y-toolbar .pojo-a11y-toolbar-toggle') || document.querySelector('#pojo-a11y-toolbar');
    const hit = (a, b) => a && b && !(a.right <= b.left || a.left >= b.right || a.bottom <= b.top || a.top >= b.bottom);
    if (tb && vis(tb)) { const r = tb.getBoundingClientRect(); if ([...document.querySelectorAll('.zs-hero h1, .zs-hero .elementor-button')].some(e => hit(r, e.getBoundingClientRect()))) E('accessibility button covers the hero title or buttons'); }
  }
  // controls and outlines (WCAG 1.4.11): fill or border at least 3:1 against what is behind them
  const faint = new Map();
  q('.elementor-button, .zs-btn, button:not(.zs-burger):not(.zs-vnote-btn), .zs-pause, .zs-social a, input:not([type=hidden]):not([type=checkbox]), textarea, select').filter(vis).forEach(el => {
    if (el.closest(skip)) return;
    const bg = behind(el); if (!bg) return;
    const s = getComputedStyle(el), fill = rgb(s.backgroundColor), bc = rgb(s.borderTopColor), bw = parseFloat(s.borderTopWidth);
    const fr = fill && (fill.length < 4 || fill[3] > .05) ? cr(flat(fill, bg), bg) : 1;
    const br = bw >= 1 && bc ? cr(flat(bc, bg), bg) : 1;
    if (Math.max(fr, br) < 3) faint.set((el.textContent || el.getAttribute('aria-label') || el.name || el.tagName).trim().slice(0, 24), Math.max(fr, br).toFixed(2));
  });
  if (faint.size) E(`control blends into its background (${faint.size}): ${[...faint].slice(0, 4).map(([t, r]) => `"${t}" ${r}`).join('; ')}`);
  // icons (svg / icon font / check bullets) at least 3:1
  const dim = new Map();
  q('svg.zs-ico, .elementor-icon, .zs-svg, .zs-checks li').filter(vis).forEach(el => {
    if (el.closest('.zs-hero__media, #pojo-a11y-toolbar')) return;
    const bg = bgOf(el); if (!bg) return;
    let c = rgb(getComputedStyle(el).color);
    if (el.matches('.zs-checks li')) { const pb = getComputedStyle(el, '::before'); if (pb.backgroundImage !== 'none') return;   // the bullet draws its own dark tick
      const b = rgb(pb.backgroundColor); if (b && (b.length < 4 || b[3] > .05)) c = b; }
    if (!c) return; const r = cr(flat(c, bg.slice(0, 3)), bg.slice(0, 3));
    if (r < 3) dim.set(el.className.toString().split(' ').find(x => x.startsWith('zs-') || x.startsWith('elementor')) || el.tagName, r.toFixed(2));
  });

  // decorative display text (wordmark, ticker) is hidden from screen readers but must still be visible: 3:1,
  // judged on its outline colour when the fill is transparent
  q('.zs-footer__mark, .zs-mq__i').filter(vis).forEach(el => {
    const bg = bgOf(el); if (!bg) return;
    const s = getComputedStyle(el); let c = rgb(s.color);
    if (!c || (c.length > 3 && c[3] < .05)) c = parseFloat(s.webkitTextStrokeWidth) > 0 ? rgb(s.webkitTextStrokeColor) : null;
    if (!c) return; const r = cr(flat(c, bg.slice(0, 3)), bg.slice(0, 3));
    if (r < 3) dim.set(el.className.toString().split(' ')[0], r.toFixed(2));
  });
  if (dim.size) E(`decorative text or icon too faint (${dim.size}): ${[...dim].slice(0, 4).map(([t, r]) => `${t} ${r}`).join('; ')}`);
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
        "foreach (get_posts(['post_type'=>['page','post'],'post_status'=>'publish','numberposts'=>-1,'meta_key'=>'_zs_key']) as $p) $u[] = get_permalink($p);"   # only what the build owns (not plugin pages on a client server)
        "foreach (get_terms(['taxonomy'=>'category','hide_empty'=>true]) as $t) $u[] = get_term_link($t);"
        "echo implode(\"\\n\", $u);")
    # /zs-dir-<k>/ are gate previews of other home layouts (local only), not part of the site
    urls = [u.strip() for u in out.splitlines() if u.strip().startswith("http") and "/zs-dir-" not in u]
    return list(dict.fromkeys(urls))


def _scroll_all(page):
    # Lazy images: scroll through, then force every <img> eager and wait until all have decoded,
    # so full-page screenshots never show empty cards.
    page.evaluate("""async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 40)); }
      document.querySelectorAll('img[loading="lazy"]').forEach(i => { i.loading = 'eager'; });
      await Promise.all([...document.images].map(i => i.complete ? null : new Promise(r => { i.onload = i.onerror = r; setTimeout(r, 4000); })));
      // one re-fetch for images that failed on a network drop; a truly broken image stays broken
      await Promise.all([...document.images].filter(i => i.complete && i.currentSrc && !i.naturalWidth).map(i => new Promise(r => {
        i.onload = i.onerror = r; setTimeout(r, 5000); i.removeAttribute('srcset'); i.src = i.currentSrc + (i.currentSrc.includes('?') ? '&' : '?') + 'zsretry=1'; })));
      window.scrollTo(0, 0); }""")
    page.wait_for_timeout(250)


def screenshots(site, paths, directions=False, mobile_only=False):
    """Full-page shots, desktop + mobile (or mobile only). paths ["all"] = every page the build owns.
    Works on the local build and on a pushed site (zs shots --site): the server can render differently
    (icon font vs SVG, caching, plugins), so look at the pushed site too, not only at the local one."""
    from playwright.sync_api import sync_playwright
    data = load_site(site.src)
    out_dir = site.dir / "shots"
    out_dir.mkdir(exist_ok=True)
    jobs = []
    if paths == ["all"]:
        paths = [urllib.parse.unquote(urllib.parse.urlsplit(u).path) or "/" for u in urls_for(site, data)]
    for i, p in enumerate(paths):
        # Hebrew paths percent-encode to unreadable names: number them, keep any latin part
        tail = re.sub(r"[^a-z0-9]+", "-", p.lower()).strip("-")
        name = "home" if p.strip("/") == "" else f"p{i:02d}" + (f"-{tail[:30]}" if tail else "")
        jobs.append((name, site.url + urllib.parse.quote(p)))
    if directions:
        for k, dv in data.get("directions", {}).items():   # a direction with its own home layout has its own page
            jobs.append((f"dir-{k}", site.url + (f"/zs-dir-{k}/" if dv.get("home") else "/?zs_dir=" + k)))
    files = []
    with sync_playwright() as pw:
        b = _launch(pw)
        for vp, (w, h) in VIEWPORTS.items():
            if mobile_only and vp != "mobile":
                continue
            ctx = b.new_context(viewport={"width": w, "height": h}, device_scale_factor=1, locale="he-IL")
            page = ctx.new_page()
            for name, url in jobs:
                page.goto(url, wait_until="networkidle")
                _scroll_all(page)
                f = out_dir / f"{name}-{vp}.png"
                # full_page capture drops off-screen images in Chromium; a viewport as tall as the page doesn't
                page.set_viewport_size({"width": w, "height": page.evaluate("document.documentElement.scrollHeight")})
                # finish scroll reveals / entrances so the shot shows the settled page
                page.evaluate("document.querySelectorAll('.zs-reveal').forEach(e => e.classList.add('is-in'))")
                page.wait_for_timeout(1600)
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
    from fingerprint import take, similarity, TOO_CLOSE
    import itertools
    urls = {k: site.url + (f"/zs-dir-{k}/" if d.get("home") else f"/?zs_dir={k}") for k, d in dirs.items()} if data.get("directions") else {"a": site.url + "/"}
    fps = take(urls)
    (out / "fingerprints.json").write_text(json.dumps(fps, ensure_ascii=False), encoding="utf-8")
    sims = {(a, b): similarity(fps[a], fps[b]) for a, b in itertools.combinations(fps, 2)}
    close = [f"{a.upper()}–{b.upper()} {v:.0%}" for (a, b), v in sims.items() if v >= TOO_CLOSE]
    for (a, b), v in sims.items():
        if v >= TOO_CLOSE:
            print(f"ERROR directions {a} and {b} look {v:.0%} alike (measured layout): change the kit, hero or section order of one")
    lines = [f"# כיווני עיצוב — {data['business']['name']}", "",
             "כל כיוון הוא דף בית שלם משלו: מבנה, סדר הבלוקים, צבעים וגופנים. בוחרים אות אחת.", "",
             "דמיון בין הכיוונים (מדוד מהדף עצמו): " + ", ".join(f"{a.upper()}–{b.upper()} {v:.0%}" for (a, b), v in sims.items()), ""]
    base = data.get("design", {})
    home = next((p.get("sections", []) for p in data.get("pages", []) if p.get("type") == "home"), [])
    for k, d in dirs.items():
        f = d.get("fonts", base.get("fonts", {}))
        recipe = " → ".join(s.get("type", "") + (":" + s["variant"] if s.get("variant") else "") for s in (d.get("home") or home))
        lines += [f"## {k.upper()} · {d.get('label', '')}", "",
                  f"ערכה `{d.get('kit', base.get('kit', '-'))}` · סגנון `{d.get('preset', base.get('preset', 'clean'))}` · Hero `{d.get('hero', base.get('hero', 'split'))}` · גופנים {f.get('heading', '')} / {f.get('body', '')}", "",
                  f"מבנה: {recipe}", "",
                  "| מחשב | נייד |", "|---|---|",
                  f"| <img src=\"dir-{k}-desktop.jpg\" width=\"620\"> | <img src=\"dir-{k}-mobile.jpg\" width=\"250\"> |", ""]
    (out / "PREVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    site._preview_close = close
    return out / "PREVIEW.md"


def check_links(links):
    from concurrent.futures import ThreadPoolExecutor

    def one(u):
        code = None
        for attempt in range(3):   # retries for dropped connections (remote hosts / proxies)
            if attempt:
                time.sleep(2 * attempt)
            try:
                code = urllib.request.build_opener(NoRedirect).open(urllib.request.Request(u, method="GET"), timeout=20).status
                break
            except urllib.error.HTTPError as e:
                code = e.code
                break
            except Exception as e:
                code = str(e)[:40]
        return u, code

    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(one, sorted(links)))
    return [(urllib.parse.unquote(u), c) for u, c in res if c != 200]


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
    def one_viewport(vp, w, h):
        rows, links, extra, errors, warns = [], set(), [], 0, 0
        with sync_playwright() as pw:
            b = _launch(pw)
            ctx = b.new_context(viewport={"width": w, "height": h}, locale="he-IL")
            page = ctx.new_page()
            console = []
            page.on("console", lambda m: console.append(m.text) if m.type == "error" else None)
            for u in urls:
                console.clear()
                resp = page.goto(u, wait_until="networkidle")
                for _ in range(2):     # a gateway hiccup (proxy / host) is retried, a real error stays
                    if resp is None or resp.status not in (502, 503, 504):
                        break
                    page.wait_for_timeout(3000)
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
                opened = page.evaluate("getComputedStyle(document.getElementById('zs-nav')).visibility === 'visible' && document.querySelector('.zs-burger').getAttribute('aria-expanded') === 'true'"
                                       # and it really covers the screen on top of the page (a filter/backdrop-filter on an ancestor clips a fixed menu)
                                       " && document.getElementById('zs-nav').getBoundingClientRect().height > innerHeight * 0.5"
                                       " && !!(document.elementFromPoint(innerWidth / 2, innerHeight * 0.6) || document.body).closest('#zs-nav')")
                page.keyboard.press("Escape")
                page.wait_for_timeout(350)
                closed = page.evaluate("document.querySelector('.zs-burger').getAttribute('aria-expanded') === 'false'")
                extra.append(("mobile menu opens full-screen on top / Escape closes", opened and closed))
                if not (opened and closed):
                    errors += 1
                if not data["business"].get("email_leads"):
                    no_form = page.locator("form.zs-form").count() == 0
                    extra.append(("calls-only site (no leads e-mail): no lead form rendered", no_form))
                    errors += 0 if no_form else 1
                else:
                    ok_msg, saved, mailed = test_form(page, site)
                    extra.append((f"lead form: thank-you shown, saved={saved}, mail={ {'yes': 'sent to the test address', 'no': 'FAILED', 'staging-skip': 'skipped on staging (correct)'}.get(mailed, 'n/a') }", ok_msg and saved == 1 and mailed != 'no'))
                    if not (ok_msg and saved == 1):
                        errors += 1
            # above the fold: the home hero's buttons are visible without scrolling on a short laptop / small phone
            # (browser bars deducted; on phones the fixed call bar too)
            fw, fh = (1280, 620) if vp == "desktop" else (360, 640)
            page.set_viewport_size({"width": fw, "height": fh})
            page.goto(site.url + "/", wait_until="networkidle")
            page.wait_for_timeout(400)
            fold = page.evaluate("""() => { const bs = [...document.querySelectorAll('.zs-hero--home .zs-btns .elementor-button')].slice(0, 2);
                const bar = document.querySelector('.zs-fab'); const br = bar && getComputedStyle(bar).display !== 'none' ? bar.getBoundingClientRect() : null;
                const lim = br && br.width > innerWidth * .6 ? br.top : innerHeight;   /* only a full-width call bar (phones), not the desktop floating WhatsApp button */
                return bs.length ? Math.max(...bs.map(b => b.getBoundingClientRect().bottom)) - lim : null; }""")
            if fold is not None:
                extra.append((f"hero buttons above the fold at {fw}×{fh}" + ("" if fold <= 0 else f" — {round(fold)}px below"), fold <= 0))
                if fold > 0:
                    errors += 1
            # Dapei Zahav reviews widget: when it shows reviews, the theme's styling must hold (Zap's own widget CSS
            # is a 404): stars in one row, the review in regular body text
            if vp == "desktop":
                page.set_viewport_size({"width": w, "height": h})
                page.goto(site.url + "/", wait_until="networkidle")
                try:
                    page.wait_for_function("document.querySelector('.zs-reviews-sec.zs-has-reviews')", timeout=8000)
                    rv = page.evaluate("""() => { const tops = new Set([...document.querySelectorAll('.zs-reviews .stars_over img')].map(i => Math.round(i.getBoundingClientRect().top)));
                        const t = document.querySelector('.zs-reviews .review_text'); return {rows: tops.size, bold: t ? +getComputedStyle(t).fontWeight >= 600 : false}; }""")
                    ok_rv = rv["rows"] <= 1 and not rv["bold"]
                    extra.append(("reviews widget styled (stars in one row, review in body text)", ok_rv))
                    if not ok_rv:
                        errors += 1
                except Exception:
                    pass        # no reviews shown (no customer-id, or the widget's API is unreachable from here)
            # 404 must be a real 404
            r404 = page.goto(site.url + "/no-such-page-zs/", wait_until="domcontentloaded")
            if vp == "desktop":
                extra.append(("404 page returns HTTP 404", r404.status == 404))
                if r404.status != 404:
                    errors += 1
            ctx.close()
            b.close()
        return rows, links, extra, errors, warns

    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(len(VIEWPORTS)) as ex:
        parts = list(ex.map(lambda kv: one_viewport(kv[0], *kv[1]), VIEWPORTS.items()))
    for r_, l_, x_, e_, w_ in parts:      # desktop first, then mobile, as before
        rows += r_; links |= l_; extra += x_; errors += e_; warns += w_

    # every social profile in site.json must be a visible link on the site (the footer renders them)
    home_html = None
    for attempt in range(4):        # network drops happen; the check must not be skipped silently
        try:
            home_html = urllib.request.urlopen(site.url + "/", timeout=30).read().decode("utf-8", "replace")
            break
        except Exception:
            time.sleep(3)
    if home_html is None and any((data["business"].get(n) or "").strip() for n in ("facebook", "instagram", "linkedin", "youtube", "tiktok")):
        extra.append(("social links: home page could not be fetched to check them", False))
        errors += 1
    if home_html is not None:
        for net in ("facebook", "instagram", "linkedin", "youtube", "tiktok"):
            u = (data["business"].get(net) or "").strip()
            if not u:
                continue
            forms = {u, urllib.parse.quote(u, safe=":/?=&%#"), html.escape(u), html.escape(urllib.parse.quote(u, safe=":/?=&%#"))}
            shown = any(f'href="{f}"' in home_html for f in forms)
            extra.append((f"{net} link shown on the site", shown))
            if not shown:
                errors += 1

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
    (site.src / getattr(site, "qa_report", "QA-REPORT.md")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:9 + len(extra)]))
    for vp, path, m in rows:
        for e in m["err"]:
            print(f"ERROR [{vp}] {path}: {e}")
    for u, c in bad_links:
        print(f"ERROR link {c}: {u}")
    return errors == 0
