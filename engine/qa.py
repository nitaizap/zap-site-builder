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
  // --- design conformance: one scale, real pixels, one type system ---------------------
  // Correctness checks pass on a page that is merely ugly. These are the measurable half of
  // design.md: they catch drift (a second H2 size), softness (a photo blown past its pixels)
  // and a type system that grew a third family, none of which any other check can see.
  const a11yChrome = '[id^="pojo-a11y"], [class*="pojo-a11y"], #ea11y-root';
  const r2 = n => Math.round(n * 2) / 2;
  const scale = [];
  ['h1', 'h2', 'h3'].forEach(tag => {
    const sizes = new Set(q(tag).filter(vis)
      .filter(e => e.textContent.trim() && !e.closest(a11yChrome))
      .map(e => r2(parseFloat(getComputedStyle(e).fontSize))));
    if (!sizes.size) return;
    const list = [...sizes].sort((a, b) => b - a);
    scale.push(tag + ':' + list.join('/'));
    // design.md: "Boldness never touches the heading scale". A warning, not an error: a card title and a
    // section title legitimately share a tag, and the theme sizes them fluidly. Four sizes for one level is
    // drift worth looking at; it is not a reason to stop a handover.
    if (list.length > 2) W(`${tag} renders at ${list.length} sizes on one page: ${list.join('/')}px (design.md wants one)`);
  });
  out.info.scale = scale.join(' ');
  // An image shown wider than its own pixels is visibly soft; object-fit:fill distorts faces and logos.
  const upscaled = [], stretched = [];
  q('img').forEach(i => {
    if (!vis(i) || !i.naturalWidth || /\.svg($|\?)/i.test(i.currentSrc || i.src)) return;
    const b = i.getBoundingClientRect(), cs = getComputedStyle(i);
    if (b.width > i.naturalWidth * 1.02) upscaled.push(`${i.src.split('/').pop()} ${Math.round(b.width)}>${i.naturalWidth}`);
    const want = i.naturalWidth / i.naturalHeight;
    if (cs.objectFit === 'fill' && Math.abs(b.width / b.height - want) > want * 0.05) stretched.push(i.src.split('/').pop());
  });
  if (upscaled.length) E(`image shown larger than its own pixels (${upscaled.length}): ` + upscaled.slice(0, 3).join(', '));
  if (stretched.length) E(`image stretched out of ratio (${stretched.length}): ` + stretched.slice(0, 3).join(', '));
  // One type system: a heading family and a body family. A third is a widget that escaped the kit.
  const fams = new Set();
  q('body *').forEach(el => {
    if (!vis(el) || el.closest(a11yChrome + ', svg, script, style')) return;
    if (![...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) return;
    const f = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g, '').trim();
    if (/^(font ?awesome|eicons|icomoon|material)/i.test(f)) return;   // icon fonts are not type
    fams.add(f);
  });
  out.info.fonts = [...fams].join('/');
  // Two is the design (headings + body). A third is usually a host plugin or a widget that escaped the kit,
  // which is worth seeing but not always ours to fix; a fourth is the kit not being applied at all.
  if (fams.size > 3) E(`${fams.size} font families on one page: ${[...fams].join(', ')} (want 2: headings + body)`);
  else if (fams.size === 3) W(`3 font families: ${[...fams].join(', ')} (want 2: headings + body)`);
  // Icons on conversion buttons are a choice, not a rule, so this fires once per page and only when the page
  // uses none at all - the case where nobody decided, rather than the case where somebody decided no.
  // An icon is not always an element: the theme draws some with a ::before glyph or a background image,
  // and counting only child nodes reported "no icons" on a site whose buttons all had one (c80362823, 04/11).
  const drawsIcon = el => {
    for (const pseudo of ['::before', '::after']) {
      const s = getComputedStyle(el, pseudo);
      if (!s) continue;
      const c = s.content;
      if (c && c !== 'none' && c !== 'normal' && c !== '""' && c !== "''") return true;
      if (s.backgroundImage && s.backgroundImage !== 'none') return true;
    }
    return false;
  };
  const hasIcon = e => !!e.querySelector('svg, i, .elementor-button-icon') || drawsIcon(e)
    || [...e.children].some(drawsIcon);
  const btns = q('.elementor-button').filter(vis);
  // hasIcon covers the general case (child element, ::before/::after content, background image); the
  // zs-b-tel/zs-b-wa test from #91 stays as a named safety net for the two theme buttons it was written for.
  const iconic = e => hasIcon(e) || /zs-b-(tel|wa)/.test(e.closest('.zs-b')?.className || e.className);
  if (btns.length >= 3 && !btns.some(iconic))
    W(`no button on this page carries an icon (${btns.length} buttons)`);
  if (window.innerWidth < 768) {
    const docBox = document.documentElement.getBoundingClientRect();
    const tight = q('h1,h2,h3,p,li,label,.elementor-button').filter(e => vis(e) && e.textContent.trim()
        && !e.closest('.zs-nav, .zs-skip, ' + a11yChrome) && getComputedStyle(e).position !== 'fixed')
      .filter(e => { const b = e.getBoundingClientRect(); return b.left < docBox.left + 11 || b.right > docBox.right - 11; })
      .map(e => e.tagName + ':' + e.textContent.trim().slice(0, 14));
    if (tight.length) W(`mobile gutter under 12px (${tight.length}): ` + tight.slice(0, 3).join(', '));
    const smallTap = q('.elementor-button, button:not(.zs-vnote-btn)').filter(e => vis(e) && !e.closest(a11yChrome))
      .filter(e => e.getBoundingClientRect().height < 44).length;
    if (smallTap) W(`${smallTap} tap targets under 44px high`);
  }
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
    // icon-only controls (the phones' header call icon) are judged by their icon (svg, icon font or a CSS-mask icon);
    // a borderless text/icon button by its own colour (WCAG 1.4.11)
    const bare = !(el.innerText || '').trim(), ico = bare && el.querySelector('svg, i'), pb = getComputedStyle(el, '::before');
    const ic = ico ? rgb(getComputedStyle(ico).color) : (bare && pb.maskImage && pb.maskImage !== 'none' ? rgb(pb.backgroundColor) : null);
    const ir = ic ? cr(flat(ic, bg), bg) : 1;
    const fg = rgb(s.color), tr = (!fill || (fill.length > 3 && fill[3] <= .05)) && !(bw >= 1) && fg ? cr(flat(fg, bg), bg) : 1;
    if (Math.max(fr, br, tr, ir) < 3) faint.set((el.textContent || el.getAttribute('aria-label') || el.name || el.tagName).trim().slice(0, 24), Math.max(fr, br).toFixed(2));
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
  // house rule: no Elementor shortcode widgets (dynamic parts are zap-* widgets)
  if (q('.elementor-widget-shortcode').length) E(`shortcode widget on the page (${q('.elementor-widget-shortcode').length}): use a zap-* Elementor widget`);
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


def _count_images(node):
    """Every image a composition asks for, at any depth: `image`, `images`, `bg`, `photo`, `logo`.
    Counts what was composed rather than what rendered, because a thin direction is fixed in site.json."""
    n = 0
    if isinstance(node, dict):
        for k, v in node.items():
            if k in ("image", "bg", "photo", "logo") and isinstance(v, str) and v.strip():
                n += 1
            elif k in ("image", "bg", "photo", "logo") and isinstance(v, dict) and v:
                n += 1
            elif k == "images" and isinstance(v, list):
                n += len([x for x in v if x])
            else:
                n += _count_images(v)
    elif isinstance(node, list):
        for v in node:
            n += _count_images(v)
    return n


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
    # The floor a direction has to clear before the user sees it (references/gallery.md). A direction
    # under it reads as a wireframe and cannot be judged; the user is then choosing between sketches.
    # Counted from the composition, not the render: it is the composition that has to be fixed.
    # A BasiX site is a smaller site by design (portfolio.md), so its floor is lower, not waived.
    basic = data.get("tier") in (None, "basic")
    min_sections, min_images = (6, 4) if basic else (8, 6)
    thin = []
    for k, d in dirs.items():
        secs = d.get("home") or home
        imgs = _count_images(secs)
        if len(secs) < min_sections or imgs < min_images:
            thin.append((k, len(secs), imgs))
            print(f"ERROR direction {k} is under the floor: {len(secs)} sections (want {min_sections}+), "
                  f"{imgs} images (want {min_images}+). Compose more of the page, or say at the gate that the "
                  f"client's photography cannot carry it (references/gallery.md)")
    site._preview_thin = thin
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


# The link check used to open 8 connections at once with a flat 20s timeout. The dev server is PHP's built-in
# one with 4 workers and it serialises under contention, so 8 in flight is already a queue: pages that answer in
# 1.4-4.4s on their own took 7-19s while other builds ran on the same box, and the check reported the machine's
# load as a page of site errors. Three agents hit that in one day; one nearly accepted a false 11-error run.
# Hence: fewer connections than the server has workers, a timeout derived from how slow this box is right now,
# and a report that never calls "did not answer" an error status.
LINK_WORKERS = 3            # < the server's 4 workers: the check queues behind itself otherwise
LINK_TIMEOUT_MIN = 20       # never stricter than the old flat timeout
LINK_TIMEOUT_MAX = 180


def _probe(url):
    """Seconds for one page, fetched alone, best of two. None if it cannot be fetched at all."""
    best = None
    for _ in range(2):
        t0 = time.monotonic()
        try:
            urllib.request.build_opener(NoRedirect).open(urllib.request.Request(url, method="GET"), timeout=LINK_TIMEOUT_MAX)
        except urllib.error.HTTPError:
            pass                                    # a 404 still tells us how fast the box is
        except Exception:
            continue
        d = time.monotonic() - t0
        best = d if best is None else min(best, d)
    return best


def _timed_out(e):
    return isinstance(e, TimeoutError) or isinstance(getattr(e, "reason", None), TimeoutError) or "timed out" in str(e).lower()


def check_links(links):
    """-> [(url, status, kind)] for every link that did not answer 200.

    `kind` is "status" when the server answered with something other than 200 (a real finding) or "timeout" when
    it did not answer in time (almost always this machine, not the site). The caller must not add the second to
    the error count."""
    from concurrent.futures import ThreadPoolExecutor
    links = sorted(links)
    if not links:
        return []
    # How slow is this box right now? A quiet machine probes at ~1s and keeps the old 20s; a loaded one probes at
    # 15s and gets a budget that matches, instead of a page of invented errors.
    probe = _probe(links[0])
    budget = LINK_TIMEOUT_MIN if probe is None else min(LINK_TIMEOUT_MAX, max(LINK_TIMEOUT_MIN, probe * LINK_WORKERS * 4))
    if budget > LINK_TIMEOUT_MIN:
        print(f"note: this machine answers a page in {probe:.1f}s right now, so the link check allows "
              f"{budget:.0f}s per request instead of {LINK_TIMEOUT_MIN}s (load, not the site)")

    def one(u):
        code, kind = None, "timeout"
        for attempt in range(3):   # retries for dropped connections (remote hosts / proxies) and for load
            if attempt:
                time.sleep(2 * attempt)
            try:
                code = urllib.request.build_opener(NoRedirect).open(urllib.request.Request(u, method="GET"),
                                                                    timeout=budget * (1 + attempt)).status
                kind = "status"
                break
            except urllib.error.HTTPError as e:
                code, kind = e.code, "status"
                break
            except Exception as e:                  # a slow box gets more room on the next try, not another failure
                code, kind = (f"no answer in {budget * (1 + attempt):.0f}s", "timeout") if _timed_out(e) else (str(e)[:40], "timeout")
        return u, code, kind

    with ThreadPoolExecutor(LINK_WORKERS) as ex:
        res = list(ex.map(one, links))
    return [(urllib.parse.unquote(u), c, k) for u, c, k in res if not (k == "status" and c == 200)]


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def test_form(page, site):
    """Submit the visible lead form like a person (waits > 3s so the time trap passes) and confirm it saved."""
    before = int(site.wp("post", "list", "--post_type=zap_lead", "--post_status=private", "--format=count") or 0)
    page.goto(site.url + "/", wait_until="networkidle")
    page.wait_for_timeout(3500)
    # the footer band is hidden on pages with a contact section (one form per page): submit the form a visitor sees
    f = "footer" if page.locator("#zf-footer-name").is_visible() else "contact"
    page.fill(f"#zf-{f}-name", "בדיקת QA")
    page.fill(f"#zf-{f}-phone", "050-0000000")
    page.check(f"#zf-{f} input[name=zf_consent]")
    page.click(f"#zf-{f} button[type=submit]")
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
    # A run that dies half way must not leave the previous run's report behind: a stale file reads exactly like
    # a pass. Remove it first; it is written again only when the whole sweep completes.
    (site.src / getattr(site, "qa_report", "QA-REPORT.md")).unlink(missing_ok=True)
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
                for _try in range(3):      # the machine sleeping or the network dropping mid-run (net::ERR_NETWORK_IO_SUSPENDED, ERR_NETWORK_CHANGED) is retried, not fatal
                    try:
                        resp = page.goto(u, wait_until="networkidle")
                        break
                    except Exception as e:
                        if _try == 2 or "net::ERR_" not in str(e):
                            raise
                        page.wait_for_timeout(4000)
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
                el_menu = page.locator(".elementor-menu-toggle").count() > 0   # Elementor Pro Nav Menu in the header
                if el_menu:
                    page.click(".elementor-menu-toggle")
                    page.wait_for_timeout(450)
                    opened = page.evaluate("(() => { const d = document.querySelector('.elementor-nav-menu--dropdown'); if (!d) return false;"
                                           " const r = d.getBoundingClientRect(); return getComputedStyle(d).display !== 'none' && r.height > 150"
                                           " && document.querySelector('.elementor-menu-toggle').getAttribute('aria-expanded') === 'true'; })()")
                    page.click(".elementor-menu-toggle")
                    page.wait_for_timeout(350)
                    closed = page.evaluate("document.querySelector('.elementor-menu-toggle').getAttribute('aria-expanded') === 'false'")
                    extra.append(("mobile menu (Elementor Nav Menu) opens / closes", opened and closed))
                    if not (opened and closed):
                        errors += 1
                else:
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

    checked = check_links(links)
    bad_links = [(u, c) for u, c, k in checked if k == "status"]       # the server answered, and not with 200
    no_answer = [(u, c) for u, c, k in checked if k == "timeout"]      # it did not answer: this box, not the site
    errors += len(bad_links)
    warns += len(no_answer)

    lines = [f"# QA report — {data['business']['name']}", "",
             f"- Pages × viewports checked: **{len(rows)}** ({len(urls)} URLs × {len(VIEWPORTS)})",
             f"- Internal links tested: **{len(links)}**, answered with a non-200 status: **{len(bad_links)}**, "
             f"did not answer in time: **{len(no_answer)}**",
             f"- Errors: **{errors}** · Warnings: **{warns}**", ""]
    for name, ok in extra:
        lines.append(f"- {'✅' if ok else '❌'} {name}")
    lines += ["", "| viewport | page | errors | warnings | KB | type scale | fonts | details |",
              "|---|---|---|---|---|---|---|---|"]
    for vp, path, m in rows:
        det = "; ".join(m["err"] + m["warn"])[:300].replace("|", "/")
        lines.append(f"| {vp} | {path} | {len(m['err'])} | {len(m['warn'])} | {m['info'].get('kb', '')} | "
                     f"{m['info'].get('scale', '')} | {m['info'].get('fonts', '')} | {det} |")
    if bad_links:
        lines += ["", "## Links the server answered with a non-200 status", ""] + [f"- {c} {u}" for u, c in bad_links]
    if no_answer:
        lines += ["", "## Links that did not answer (timed out or refused the connection) - NOT an error status", "",
                  "These are almost always this machine, not the site: the dev server serialises, and another build "
                  "running beside this one pushes a 1.4s page past the timeout. Rerun the QA in a quiet window "
                  "before treating any of them as a finding.", ""] + [f"- {c} {u}" for u, c in no_answer]
    (site.src / getattr(site, "qa_report", "QA-REPORT.md")).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:9 + len(extra)]))
    for vp, path, m in rows:
        for e in m["err"]:
            print(f"ERROR [{vp}] {path}: {e}")
    for u, c in bad_links:
        print(f"ERROR link {c}: {u}")
    return errors == 0
