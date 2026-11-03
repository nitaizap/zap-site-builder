"""Measure a home-page hero: how much of the first screen is used. Read-only, informational, NOT a gate.

    py tools/hero-space.py URL [URL ...] [--out report.txt] [--shots DIR]

Renders each URL at 1440x900, 1280x720 and 390x844 (headless Chrome via Playwright) and prints, per viewport, the
numbers behind the hero-space rule in `.claude/skills/zap-site/references/hero-space.md`: the hero's height against
the screen, the share of the hero box with nothing in it, the largest empty rectangle, the text block against the
hero and against the photo, and where the first button ends against the fold.

Why it is not a check: measured on the three sites the user rejected and three he did not, no metric separated the
two groups (hero-space.md has the table). The numbers are for you to read next to the screenshot, and to append
to that table when the user next says a hero wastes space, so a threshold can be earned from data instead of invented.

Output is ASCII-safe (Hebrew in the Windows console is mangled): pass --out to also get a UTF-8 file with the H1.
"""
import argparse
import io
import json
import sys
from pathlib import Path

VIEWPORTS = {"d1440": (1440, 900), "d1280": (1280, 720), "m390": (390, 844)}

JS = r"""
() => {
  const vw = innerWidth, vh = innerHeight;
  const vis = el => { const s = getComputedStyle(el); if (s.display === 'none' || s.visibility === 'hidden' || +s.opacity === 0) return false; const r = el.getBoundingClientRect(); return r.width > 1 && r.height > 1; };
  const h1 = [...document.querySelectorAll('h1')].find(vis);
  if (!h1) return {error: 'no h1'};
  let hero = document.querySelector('.zs-hero--home');
  let how = 'zs-hero';
  if (!hero) {
    how = 'climb';
    let el = h1;
    while (el.parentElement && !el.parentElement.matches('main, body, [data-elementor-type], .elementor, #content, .site-main')) el = el.parentElement;
    hero = el;
  }
  const hr = hero.getBoundingClientRect();
  const top = hr.top + scrollY, H = hr.height, W = hr.width;
  const textRects = [];
  const tw = document.createTreeWalker(hero, NodeFilter.SHOW_TEXT);
  while (tw.nextNode()) {
    const n = tw.currentNode; if (!n.textContent.trim()) continue; const el = n.parentElement;
    if (!vis(el) || el.closest('script,style,noscript,[aria-hidden="true"],.zs-pause,#pojo-a11y-toolbar')) continue;
    const rg = document.createRange(); rg.selectNodeContents(n);
    for (const r of rg.getClientRects()) if (r.width > 2 && r.height > 2) textRects.push({l: r.left, t: r.top, r: r.right, b: r.bottom, el});
  }
  const blocks = []; let bg = null;
  hero.querySelectorAll('img, video, picture, svg, .elementor-button, .zs-btn, form, input, textarea, button, .zs-hero__media, .zs-hero__form').forEach(el => {
    if (!vis(el)) return;
    const r = el.getBoundingClientRect();
    const area = r.width * r.height;
    const isMedia = el.matches('img, video, picture, .zs-hero__media') || (el.matches('svg') && area > 20000);
    if (isMedia && area >= 0.8 * W * H) { bg = bg || {l: r.left, t: r.top, r: r.right, b: r.bottom}; return; }
    blocks.push({l: r.left, t: r.top, r: r.right, b: r.bottom, kind: el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : ''), media: isMedia});
  });
  let cssBg = false;
  [hero, ...hero.querySelectorAll('*')].forEach(e => {
    const s = getComputedStyle(e);
    if (s.backgroundImage !== 'none' && /url\(/.test(s.backgroundImage)) {
      const r = e.getBoundingClientRect();
      if (r.width * r.height >= .8 * W * H) cssBg = true;
      else if (r.width * r.height > 4000) blocks.push({l: r.left, t: r.top, r: r.right, b: r.bottom, kind: 'cssbg', media: true});
    }
  });
  const hasBg = !!bg || cssBg;
  const C = 8, gx = Math.ceil(W / C), gy = Math.ceil(H / C);
  const mk = () => new Uint8Array(gx * gy);
  const paint = (g, r) => {
    const x0 = Math.max(0, Math.floor((r.l - hr.left) / C)), x1 = Math.min(gx, Math.ceil((r.r - hr.left) / C)), y0 = Math.max(0, Math.floor((r.t - hr.top) / C)), y1 = Math.min(gy, Math.ceil((r.b - hr.top) / C));
    for (let y = y0; y < y1; y++) for (let x = x0; x < x1; x++) g[y * gx + x] = 1;
  };
  const count = g => { let c = 0; for (const v of g) c += v; return c; };
  const gAll = mk(), gTxt = mk();
  textRects.forEach(r => { paint(gAll, r); paint(gTxt, r); });
  blocks.forEach(r => paint(gAll, r));
  const cells = gx * gy;
  const allr = [...textRects, ...blocks];
  const bb = allr.length ? {l: Math.min(...allr.map(r => r.l)), t: Math.min(...allr.map(r => r.t)), r: Math.max(...allr.map(r => r.r)), b: Math.max(...allr.map(r => r.b))} : null;
  const rowEmpty = [], colEmpty = [];
  for (let y = 0; y < gy; y++) { let any = 0; for (let x = 0; x < gx; x++) if (gAll[y * gx + x]) { any = 1; break; } rowEmpty.push(!any); }
  for (let x = 0; x < gx; x++) { let any = 0; for (let y = 0; y < gy; y++) if (gAll[y * gx + x]) { any = 1; break; } colEmpty.push(!any); }
  const run = a => { let best = 0, cur = 0; a.forEach(v => { cur = v ? cur + 1 : 0; best = Math.max(best, cur); }); return best; };
  let maxRect = 0, maxRectBox = null; const hgt = new Int32Array(gx);
  for (let y = 0; y < gy; y++) {
    for (let x = 0; x < gx; x++) hgt[x] = gAll[y * gx + x] ? 0 : hgt[x] + 1;
    const st = [];
    for (let x = 0; x <= gx; x++) {
      const h = x < gx ? hgt[x] : 0; let s = x;
      while (st.length && st[st.length - 1].h >= h) { const t = st.pop(); const a = t.h * (x - t.s); if (a > maxRect) { maxRect = a; maxRectBox = {w: (x - t.s) * C, h: t.h * C}; } s = t.s; }
      st.push({h, s});
    }
  }
  const tr = textRects.filter(r => !r.el.closest('.elementor-button, .zs-btn, button, a.elementor-button'));
  const tb = tr.length ? {l: Math.min(...tr.map(r => r.l)), t: Math.min(...tr.map(r => r.t)), r: Math.max(...tr.map(r => r.r)), b: Math.max(...tr.map(r => r.b))} : null;
  const colr = h1.parentElement.getBoundingClientRect();
  const h1s = getComputedStyle(h1);
  const h1lines = (() => { const rg = document.createRange(); rg.selectNodeContents(h1); const ys = new Set([...rg.getClientRects()].map(r => Math.round(r.top / 4))); return ys.size; })();
  const lead = [...hero.querySelectorAll('p')].find(p => vis(p) && p.textContent.trim().length > 20 && !p.closest('form,.zs-hero__form'));
  const leadS = lead ? getComputedStyle(lead) : null;
  const btns = [...hero.querySelectorAll('.elementor-button, .zs-btn, a.btn, a[class*="button"]')].filter(vis);
  const btn = btns[0] ? btns[0].getBoundingClientRect() : null;
  const media = blocks.filter(b => b.media).sort((a, b) => (b.r - b.l) * (b.b - b.t) - (a.r - a.l) * (a.b - a.t))[0];
  const mediaShare = media ? ((media.r - media.l) * (media.b - media.t)) / (W * H) : 0;
  const hdr = document.querySelector('header, .zs-header');
  const hdrH = hdr ? hdr.getBoundingClientRect().height : 0;
  return {
    how, cls: (hero.className || '').toString().slice(0, 60), vw, vh,
    heroTop: Math.round(top), heroH: Math.round(H), heroVh: +(H / vh).toFixed(2), heroBottomVsVh: Math.round(top + H - vh), hdrH: Math.round(hdrH),
    hasBgMedia: hasBg, mediaShare: +mediaShare.toFixed(2),
    inkShare: +(count(gAll) / cells).toFixed(3), txtShare: +(count(gTxt) / cells).toFixed(3),
    emptyShare: +(1 - count(gAll) / cells).toFixed(3),
    inkBboxShare: bb ? +(((Math.min(bb.r, hr.right) - Math.max(bb.l, hr.left)) * (Math.min(bb.b, hr.bottom) - Math.max(bb.t, hr.top))) / (W * H)).toFixed(3) : null,
    topGap: bb ? Math.round(bb.t - hr.top) : null, botGap: bb ? Math.round(hr.bottom - bb.b) : null,
    longestEmptyRow: run(rowEmpty) * C, longestEmptyCol: run(colEmpty) * C,
    maxEmptyRect: +(maxRect / cells).toFixed(3), maxEmptyRectBox: maxRectBox,
    textBlock: tb ? {w: Math.round(tb.r - tb.l), h: Math.round(tb.b - tb.t), widthVsHero: +((tb.r - tb.l) / W).toFixed(2), heightVsHero: +((tb.b - tb.t) / H).toFixed(2), l: Math.round(tb.l - hr.left), r: Math.round(hr.right - tb.r)} : null,
    col: {w: Math.round(colr.width), widthVsHero: +(colr.width / W).toFixed(2), inkVsCol: tb ? +((tb.r - tb.l) / colr.width).toFixed(2) : null},
    h1: {fs: parseFloat(h1s.fontSize), lines: h1lines, chars: h1.textContent.trim().length, w: Math.round(h1.getBoundingClientRect().width), text: h1.textContent.trim().slice(0, 40)},
    lead: lead ? {fs: parseFloat(leadS.fontSize), chars: lead.textContent.trim().length, w: Math.round(lead.getBoundingClientRect().width)} : null,
    cta: btn ? {text: btns[0].textContent.trim().slice(0, 20), bottom: Math.round(btn.bottom + scrollY), aboveFold: btn.bottom <= vh, bottomVsVh: Math.round(btn.bottom - vh), n: btns.length} : null,
    mediaBox: media ? {w: Math.round(media.r - media.l), h: Math.round(media.b - media.t)} : null, leadLines: lead ? Math.round(lead.getBoundingClientRect().height / (parseFloat(leadS.lineHeight) || parseFloat(leadS.fontSize) * 1.5)) : null, nblocks: blocks.length, mediaKinds: blocks.filter(b => b.media).map(b => b.kind).slice(0, 4),
  };
}
"""


def measure(urls, shots=None):
    from playwright.sync_api import sync_playwright
    out = {}
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome")
        except Exception:
            b = p.chromium.launch()
        for url in urls:
            out[url] = {}
            for vp, (w, h) in VIEWPORTS.items():
                ctx = b.new_context(viewport={"width": w, "height": h}, locale="he-IL", reduced_motion="reduce")
                pg = ctx.new_page()
                try:
                    pg.goto(url, wait_until="networkidle", timeout=60000)
                except Exception:
                    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
                pg.wait_for_timeout(2500)
                pg.evaluate("document.querySelectorAll('.zs-reveal').forEach(e => e.classList.add('is-in'))")
                pg.wait_for_timeout(1200)
                out[url][vp] = pg.evaluate(JS)
                if shots:
                    Path(shots).mkdir(parents=True, exist_ok=True)
                    host = url.split("//")[-1].split("/")[0].replace(":", "_")
                    pg.screenshot(path=str(Path(shots) / f"{host}-{vp}.png"))
                ctx.close()
        b.close()
    return out


def line(vp, m):
    if "error" in m:
        return f"  {vp:6} {m['error']}"
    tb, cta, mb = m.get("textBlock") or {}, m.get("cta") or {}, m.get("mediaBox") or {}
    txt_vs_media = round(tb["h"] / mb["h"], 2) if tb and mb.get("h") and not m["hasBgMedia"] and m["vw"] >= 768 else None
    return (f"  {vp:6} hero {m['heroH']}px = {m['heroVh']}vh | bg photo {'yes' if m['hasBgMedia'] else 'no'} | empty {m['emptyShare']:.0%} of box "
            f"| biggest empty rect {m['maxEmptyRect']:.0%} ({m['maxEmptyRectBox']['w']}x{m['maxEmptyRectBox']['h']}) "
            f"| text block {tb.get('widthVsHero')}w x {tb.get('heightVsHero')}h of hero, vs photo height {txt_vs_media} "
            f"| h1 {m['h1']['fs']}px/{m['h1']['lines']} line(s), lead {(m['lead'] or {}).get('fs')}px "
            f"| first button {'above' if cta.get('aboveFold') else 'BELOW'} the fold ({cta.get('bottomVsVh')}px)")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split(chr(10))[0])
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--out", help="also write the report (with the H1 text) as UTF-8 here")
    ap.add_argument("--shots", help="save a screenshot per viewport into this folder")
    ap.add_argument("--json", help="write the raw measurements as JSON here")
    a = ap.parse_args()
    res = measure(a.urls, a.shots)
    lines = []
    for url, v in res.items():
        lines.append(url)
        for vp, m in v.items():
            lines.append(line(vp, m))
            if a.out and "error" not in m:
                lines.append(f"         h1: {m['h1']['text']}")
    text = chr(10).join(lines)
    print(text.encode("ascii", "replace").decode())
    if a.out:
        io.open(a.out, "w", encoding="utf-8").write(text + chr(10))
    if a.json:
        io.open(a.json, "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
