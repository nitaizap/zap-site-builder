"""Layout fingerprint: what the home page LOOKS like, measured from the rendered page, not from section names.

`zs pool` used to compare section names, so swapping "split:card" for "split:duo" passed while the page still read
the same. This measures the skeleton a visitor sees at 1440px: the header arrangement, the container width, and for
every section its ground (light / tint / dark / colour), height, how much of it is photo, how many columns its
content runs in and where its heading sits. Two homes are compared on those tokens; `zs pool` stops on a close match.
"""
import json
from difflib import SequenceMatcher

JS = r"""() => {
  const lum = (c) => { const m = (c || '').match(/[\d.]+/g); if (!m || (m.length > 3 && +m[3] === 0)) return null;
    const [r, g, b] = m.slice(0, 3).map(x => { x = x / 255; return x <= .03928 ? x / 12.92 : Math.pow((x + .055) / 1.055, 2.4); });
    return { l: .2126 * r + .7152 * g + .0722 * b, sat: Math.max(...m.slice(0, 3)) - Math.min(...m.slice(0, 3)) }; };
  const ground = (el) => { let e = el; while (e && e !== document.documentElement) { const c = lum(getComputedStyle(e).backgroundColor); if (c) return c; e = e.parentElement; } return { l: 1, sat: 0 }; };
  const W = innerWidth;
  const out = { header: '', wrap: 0, secs: [], page: {} };
  const px = (v) => parseFloat(v) || 0;
  const firstR = (sel) => { const e = document.querySelector(sel); return e ? px(getComputedStyle(e).borderTopLeftRadius) : -1; };
  const bucket = (v, cuts) => v < 0 ? 'n' : String(cuts.filter(c => v >= c).length);
  const h2 = document.querySelector('.zs-sec:not(.zs-hero) .zs-sec__title .elementor-heading-title');
  const btn = document.querySelector('.zs-sec .zs-b .elementor-button');
  const hdr = document.querySelector('.zs-header');
  const secEls = [...document.querySelectorAll('.zs-sec:not(.zs-hero)')];
  out.page = {
    img_r: bucket(firstR('.zs-sec:not(.zs-hero) img'), [3, 12, 24]),
    card_r: bucket(firstR('.zs-card'), [3, 12, 24]),
    btn_r: bucket(btn ? px(getComputedStyle(btn).borderTopLeftRadius) : -1, [3, 12, 40]),
    h2: bucket(h2 ? px(getComputedStyle(h2).fontSize) : -1, [30, 40, 52]),
    inset: secEls.filter(e => e.getBoundingClientRect().width < W - 20).length > secEls.length / 2,
    edge: px(getComputedStyle(document.body, '::before').width) > 0 && getComputedStyle(document.body, '::before').position === 'fixed',
    header_pill: hdr ? px(getComputedStyle(hdr).borderTopLeftRadius) > 20 : false,
  };
  const brand = document.querySelector('.zs-brand'), nav = document.querySelector('.zs-header__nav, .zs-nav');
  if (brand && nav) { const b = brand.getBoundingClientRect(), n = nav.getBoundingClientRect();
    const bx = (b.left + b.width / 2) / W;
    out.header = (Math.abs(bx - .5) < .12 ? 'logo-centre' : 'logo-side') + (n.top > b.bottom - 4 ? '/menu-below' : Math.abs((n.left + n.width / 2) / W - .5) < .1 ? '/menu-centre' : '/menu-side'); }
  const secs = [...document.querySelectorAll('.zs-sec')].filter(s => !s.closest('.zs-sec:not(:scope) .zs-sec'));
  for (const s of secs) {
    const r = s.getBoundingClientRect(); if (r.height < 40) continue;
    const g = ground(s);
    const tone = g.sat > 60 ? 'colour' : g.l < .2 ? 'dark' : g.l < .9 ? 'tint' : 'light';
    let img = 0; s.querySelectorAll('img, video').forEach(i => { const q = i.getBoundingClientRect(); img += Math.max(0, q.width) * Math.max(0, q.height); });
    const imgShare = Math.min(1, img / Math.max(1, r.width * r.height));
    const inner = s.querySelector(':scope > .e-con-inner') || s;
    const ir = inner.getBoundingClientRect(); out.wrap = Math.max(out.wrap, Math.round(ir.width));
    // columns: distinct left edges of the visible blocks in the section's largest row
    const blocks = [...s.querySelectorAll('.zs-card, .zs-feature, .zs-step, .elementor-widget-image, .zs-faq, .zs-head, .zs-split__text, .zs-gallery__item, .gallery-item')]
      .map(e => e.getBoundingClientRect()).filter(q => q.width > 60 && q.height > 40);
    const rows = {}; blocks.forEach(q => { const k = Math.round(q.top / 40); (rows[k] = rows[k] || new Set()).add(Math.round(q.left / 30)); });
    const cols = Math.min(5, Math.max(1, ...Object.values(rows).map(x => x.size)));
    const h = s.querySelector('.zs-sec__title, .zs-hero__title');
    const hw = s.querySelector(':scope > .e-con-inner > .zs-head');
    let head = 'none';
    if (h) { const t = getComputedStyle(h.querySelector('.elementor-heading-title') || h).textAlign;
      let side = false;
      if (hw) { const q = hw.getBoundingClientRect();
        side = q.width < ir.width * .5 && [...hw.parentElement.children].some(x => { if (x === hw) return false; const z = x.getBoundingClientRect();
          return z.height > 20 && z.top < q.bottom && (z.right <= q.left + 4 || z.left >= q.right - 4); }); }
      head = side ? 'side' : (t === 'center' ? 'centre' : 'start'); }
    out.secs.push({ tone, h: +(r.height / W).toFixed(2), img: +imgShare.toFixed(2), cols, head, full: r.width >= W - 2 && ir.width >= W - 80 });
  }
  return out;
}"""


def measure(page):
    """page: a Playwright page already at 1440px on the home page -> fingerprint dict."""
    return page.evaluate(JS)


TOO_CLOSE = .85   # ERROR: reads as the same site (calibrated: one kit on the same section order scores .87-.96)
CLOSE = .75       # WARN

HEAD = {"start": "a", "side": "d", "centre": "c", "none": "n"}


def _tok(s):
    hb = "S" if s["h"] < .3 else "M" if s["h"] < .65 else "L"
    ib = "0" if s["img"] < .08 else "1" if s["img"] < .4 else "2"
    return f"{s['tone'][0]}{hb}{ib}{s['cols']}{HEAD[s['head']]}"


def similarity(a, b):
    """0..1: how alike two homes look. Section-by-section skeleton (70%) + page frame (30%)."""
    seq = SequenceMatcher(None, [_tok(s) for s in a["secs"]], [_tok(s) for s in b["secs"]]).ratio()
    # looser pass: grounds and head placement only (what reads first from a distance)
    loose = SequenceMatcher(None, [s["tone"][0] + HEAD[s["head"]] for s in a["secs"]], [s["tone"][0] + HEAD[s["head"]] for s in b["secs"]]).ratio()
    pa, pb = a.get("page", {}), b.get("page", {})
    feats = [a.get("header") == b.get("header"), abs(a.get("wrap", 0) - b.get("wrap", 0)) < 60] + [pa.get(k) == pb.get(k) for k in
             ("img_r", "card_r", "btn_r", "h2", "inset", "edge", "header_pill")]
    frame = sum(feats) / len(feats)
    return round(.35 * seq + .25 * loose + .4 * frame, 3)


def load(text):
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return None


def take(urls):
    """{name: url} -> {name: fingerprint}, measured at 1440x900 after a full scroll (lazy images, reveals)."""
    from playwright.sync_api import sync_playwright
    from qa import _launch, _scroll_all
    out = {}
    with sync_playwright() as pw:
        b = _launch(pw)
        page = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1, locale="he-IL")
        for name, url in urls.items():
            page.goto(url, wait_until="networkidle")
            _scroll_all(page)
            page.evaluate("document.querySelectorAll('.zs-reveal').forEach(e => e.classList.add('is-in'))")
            page.wait_for_timeout(600)
            out[name] = measure(page)
        b.close()
    return out
