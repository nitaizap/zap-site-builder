/* Zap Base: mobile menu, header state, motion layer, hero video. No dependencies.
   Motion is progressive enhancement: content is never hidden unless this script runs (html.zs-js),
   and everything is revealed after a safety timeout even if the observer never fires. */
(function () {
  var root = document.documentElement;
  var body = document.body;

  /* ---------- mobile menu ---------- */
  var b = document.querySelector('.zs-burger');
  var nav = document.getElementById('zs-nav');
  function setOpen(open) {
    if (!b) return;
    b.setAttribute('aria-expanded', open ? 'true' : 'false');
    b.setAttribute('aria-label', open ? 'סגירת תפריט' : 'פתיחת תפריט');
    root.classList.toggle('zs-nav-open', open);
  }
  if (b && nav) {
    b.addEventListener('click', function () { setOpen(b.getAttribute('aria-expanded') !== 'true'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setOpen(false); });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) setOpen(false); });
    window.matchMedia('(min-width: 1025px)').addEventListener('change', function () { setOpen(false); });
    // while the menu is open the page behind it must not scroll; touch/wheel outside the menu is ignored
    var block = function (e) { if (root.classList.contains('zs-nav-open') && !e.target.closest('#zs-nav')) e.preventDefault(); };
    document.addEventListener('touchmove', block, { passive: false });
    document.addEventListener('wheel', block, { passive: false });
  }

  /* ---------- header state ---------- */
  var h = document.querySelector('.zs-header');
  var hero = document.querySelector('.zs-hero__img img');
  var lively = body.classList.contains('zs-m-lively');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ticking = false, scrolled = false;
  function onScroll() {
    var y = window.scrollY;
    var s = y > 8;
    if (h && s !== scrolled) { scrolled = s; h.classList.toggle('is-scrolled', s); }
    if (hero && lively && !reduce && y < 900) hero.style.transform = 'translate3d(0,' + Math.round(y * 0.08) + 'px,0) scale(1.06)';
    ticking = false;
  }
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  var motion = !reduce && !body.classList.contains('zs-m-none') && 'IntersectionObserver' in window;

  /* ---------- scroll reveal ---------- */
  var sel = '.zs-sec__title, .zs-sec__intro, .zs-card, .zs-feature, .zs-step, .zs-split__text, .zs-split__media,'
          + ' .zs-faq__list, .zs-postcard, .zs-trust__list li, .zs-cta__text, .zs-cta .zs-btns, .zs-gallery__img,'
          + ' .zs-contact__info, .zs-contact__map, .zs-prose-sec .zs-prose, .zs-layers__stack, .zs-layers__item';
  if (motion) {
    var items = [].slice.call(document.querySelectorAll(sel)).filter(function (el) { return !el.closest('.zs-hero'); });
    items.forEach(function (el) {
      var p = el.parentElement, i = p ? [].indexOf.call(p.children, el) : 0;
      el.style.setProperty('--zs-i', Math.min(i, 6));
      el.classList.add('zs-reveal');
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); count(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
    setTimeout(function () { items.forEach(function (el) { el.classList.add('is-in'); }); }, 4000);
    root.classList.add('zs-motion');
  }

  /* ---------- H1 words: wrapped for a staggered entrance (text and order unchanged) ---------- */
  if (motion) {
    var h1 = document.querySelector('.zs-hero__title .elementor-heading-title');
    if (h1 && !h1.querySelector('.zs-w')) {
      var wi = 0, walker = document.createTreeWalker(h1, NodeFilter.SHOW_TEXT), nodes = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach(function (n) {
        if (n.parentElement.closest('.zs-h1__sep')) return;
        var frag = document.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(function (part) {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
          var sp = document.createElement('span'); sp.className = 'zs-w'; sp.style.setProperty('--w', wi++); sp.textContent = part; frag.appendChild(sp);
        });
        n.parentNode.replaceChild(frag, n);
      });
    }
  }

  /* ---------- reviews: show the section only while the widget shows real reviews ----------
     The Dapei Zahav widget first paints a "טוען חוות דעת..." frame and empties itself if its API fails
     (it does on staging hosts), so judge the settled content, not the first paint. */
  var rv = document.querySelector('.zs-reviews-sec');
  if (rv) {
    var tries = 0, t = setInterval(function () {
      var w = rv.querySelector('zap-reviews');
      var txt = w ? ((w.shadowRoot ? w.shadowRoot.textContent : '') + ' ' + w.textContent).replace(/\s+/g, ' ').trim() : '';
      var real = txt.length > 80 && !/טוען/.test(txt);
      rv.classList.toggle('zs-has-reviews', real);
      if (++tries > 50) clearInterval(t);
    }, 300);
  }

  /* ---------- trust-strip counters: pure numbers only (15+, 98%, 1,200), never years ---------- */
  function count(el) {
    if (!motion || !el.matches('.zs-trust__list li')) return;
    var s = el.querySelector('strong');
    if (!s) return;
    var m = s.textContent.trim().match(/^(\d{1,3}(?:,\d{3})*|\d{1,4})(\+|%)?$/);
    if (!m) return;
    var target = parseInt(m[1].replace(/,/g, ''), 10);
    if (target >= 1900 && target <= 2100 && !m[2]) return;
    var suffix = m[2] || '', start = null, dur = 1100, fmt = m[1].indexOf(',') > -1;
    s.setAttribute('aria-label', s.textContent);
    function step(t) {
      if (!start) start = t;
      var k = Math.min(1, (t - start) / dur), v = Math.round(target * (1 - Math.pow(1 - k, 3)));
      s.textContent = (fmt ? v.toLocaleString('en-US') : v) + suffix;
      if (k < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------- route: the rider follows the scroll, each stop lights up when the rider reaches it ---------- */
  var routes = [].slice.call(document.querySelectorAll('.zs-route__list'));
  if (routes.length && motion) {
    routes.forEach(function (l) { l.classList.add('is-live'); });
    var rTick = false, idleT = null;
    var updRoutes = function () {
      rTick = false;
      var vh = window.innerHeight, ltr = root.getAttribute('dir') === 'ltr';
      routes.forEach(function (l) {
        var r = l.getBoundingClientRect();
        if (r.bottom < -200 || r.top > vh + 200) return;
        var p = Math.max(0, Math.min(1, (vh * 0.78 - r.top) / (r.height + vh * 0.18)));
        l.style.setProperty('--p', p.toFixed(4));
        var tr = l.querySelector('.zs-route__track');
        if (!tr) return;
        var t = tr.getBoundingClientRect(), vertical = t.height > t.width;
        if (vertical) {
          // phones: the rider parks just above the last stop instead of on top of it
          var ics = l.querySelectorAll('.zs-route__step .elementor-icon'), last = ics[ics.length - 1];
          var rh = (l.querySelector('.zs-route__rider') || tr).offsetHeight;
          var stop = last ? (last.getBoundingClientRect().top - rh / 2 - 6 - t.top) / t.height : 1;
          l.style.setProperty('--pr', Math.min(p, Math.max(0, stop)).toFixed(4));
        }
        l.querySelectorAll('.zs-route__step').forEach(function (st) {
          var ic = (st.querySelector('.elementor-icon') || st).getBoundingClientRect();
          var f = vertical ? (ic.top + ic.height / 2 - t.top) / t.height
                : ltr ? (ic.left + ic.width / 2 - t.left) / t.width : (t.right - ic.left - ic.width / 2) / t.width;
          st.classList.toggle('is-on', p >= Math.min(1, Math.max(0, f)) - 0.01);
        });
        l.classList.remove('is-idle');
      });
      clearTimeout(idleT);
      idleT = setTimeout(function () { routes.forEach(function (l) { l.classList.add('is-idle'); }); }, 260);
    };
    window.addEventListener('scroll', function () { if (!rTick) { rTick = true; requestAnimationFrame(updRoutes); } }, { passive: true });
    window.addEventListener('resize', updRoutes);
    updRoutes();
  }

  /* ---------- scroll progress vehicle ---------- */
  var pg = document.querySelector('.zs-progress');
  if (pg && !reduce) {
    root.classList.add('zs-js');
    var pTick = false, pIdle = null;
    var updProgress = function () {
      pTick = false;
      var max = document.documentElement.scrollHeight - window.innerHeight;
      pg.style.setProperty('--sp', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : 0);
    };
    window.addEventListener('scroll', function () {
      if (!pTick) { pTick = true; requestAnimationFrame(updProgress); }
      if (window.scrollY > 40) pg.classList.add('is-moving');
      clearTimeout(pIdle); pIdle = setTimeout(function () { pg.classList.remove('is-moving'); }, 900);
    }, { passive: true });
    updProgress();
  }

  /* ---------- bento tiles: pointer tilt (fine pointers only) ---------- */
  if (motion && lively && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    [].forEach.call(document.querySelectorAll('.zs-cards--bento .zs-card--img'), function (c) {
      c.addEventListener('pointermove', function (e) {
        var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
        c.classList.add('is-tilting');
        c.style.setProperty('--ry', ((x - 0.5) * 7).toFixed(2) + 'deg');
        c.style.setProperty('--rx', ((0.5 - y) * 6).toFixed(2) + 'deg');
        c.style.setProperty('--mx', (x * 100).toFixed(1) + '%');
        c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      });
      c.addEventListener('pointerleave', function () {
        c.classList.remove('is-tilting');
        c.style.setProperty('--rx', '0deg'); c.style.setProperty('--ry', '0deg');
      });
    });
  }

  /* ---------- pause button for everything that moves on its own for more than 5 s (WCAG 2.2.2) ---------- */
  function addPause(el) {
    if (el.querySelector('.zs-pause')) return;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'zs-pause';
      btn.setAttribute('aria-pressed', 'false');
      btn.setAttribute('aria-label', 'עצירת התנועה');
      btn.innerHTML = '<svg viewBox="0 0 24 24" width="14" height="14" aria-hidden="true" focusable="false"><path class="zs-pause__p" d="M7 5h3v14H7zM14 5h3v14h-3z"/><path class="zs-pause__r" d="M8 5l11 7-11 7z"/></svg>';
      btn.addEventListener('click', function () {
        var on = !el.classList.contains('is-paused');
        el.classList.toggle('is-paused', on);
        btn.setAttribute('aria-pressed', on ? 'true' : 'false');
        btn.setAttribute('aria-label', on ? 'הפעלת התנועה' : 'עצירת התנועה');
      });
      (el.querySelector('.zs-hero__media') || el).appendChild(btn);
  }
  if (motion) [].forEach.call(document.querySelectorAll('.zs-pausable'), addPause);

  /* ---------- whole card clickable: a click anywhere on a card with a title link follows that link
     (keyboard users still tab to the title link: one focus stop per card) ---------- */
  function cardLink(e) {
    var c = e.target.closest && e.target.closest('.zs-card');
    if (!c || e.target.closest('a, button, input, textarea, select, label')) return null;
    if (window.getSelection && String(window.getSelection()).length) return null;   // selecting text, not clicking
    return c.querySelector('.zs-card__title a[href]');
  }
  document.addEventListener('click', function (e) {
    var a = cardLink(e);
    if (!a || e.button !== 0) return;
    if (e.ctrlKey || e.metaKey || e.shiftKey) window.open(a.href, '_blank', 'noopener');
    else a.click();
  });
  document.addEventListener('auxclick', function (e) {
    var a = cardLink(e);
    if (a && e.button === 1) { e.preventDefault(); window.open(a.href, '_blank', 'noopener'); }
  });

  /* ---------- hero slider: 2-3 photos crossfade every hero.interval s (default 4); reduced motion keeps the fade, drops the zoom ---------- */
  [].forEach.call(document.querySelectorAll('.zs-hero__slider'), function (sl) {
    var slides = [].slice.call(sl.querySelectorAll('.zs-hero__slide'));
    if (slides.length < 2) return;
    slides[0].classList.add('is-on');
    sl.classList.add('is-ready');
    // the client asked for rotating photos: they rotate under "reduce motion" too (a crossfade without the
    // zoom); only motion:"none" keeps the first photo
    if (body.classList.contains('zs-m-none')) return;
    var i = 0, host = sl.closest('.zs-hero') || sl;
    if (!motion) addPause(host);
    var iv = (parseInt((sl.className.match(/zs-int-(\d+)/) || [])[1], 10) || 4) * 1000, prev = null, t = 0;
    sl.style.setProperty('--zs-iv', iv + 'ms');
    setInterval(function () {
      if (host.classList.contains('is-paused') || document.hidden) return;
      // the outgoing photo stays opaque underneath (.is-prev) while the next one fades in over it
      clearTimeout(t);
      if (prev) prev.classList.remove('is-prev');
      prev = slides[i];
      prev.classList.add('is-prev');
      prev.classList.remove('is-on');
      i = (i + 1) % slides.length;
      slides[i].classList.add('is-on');
      var done = prev;
      t = setTimeout(function () { done.classList.remove('is-prev'); }, 2000);
    }, iv);
  });


  /* ---------- hero video: desktop only, after load, never on data-saver ---------- */
  var v = document.querySelector('video.zs-hero__video[data-src]');
  if (v) {
    var conn = navigator.connection || {};
    var ok = !reduce && !conn.saveData && window.matchMedia('(min-width: 900px)').matches;
    if (ok) {
      var go = function () {
        v.src = v.getAttribute('data-src');
        v.addEventListener('playing', function () { v.classList.add('is-playing'); }, { once: true });
        var p = v.play(); if (p && p.catch) p.catch(function () {});
      };
      if (document.readyState === 'complete') setTimeout(go, 300); else window.addEventListener('load', function () { setTimeout(go, 300); });
    }
  }
})();

/* layers: highlight a layer and its list item together (hover / tap / focus); auto-tour once when it comes into view */
(function () {
  document.querySelectorAll('.zs-layers').forEach(function (sec) {
    var draw = sec.querySelector('.zs-layers__draw'); if (!draw) return;
    var gs = [].slice.call(draw.querySelectorAll('.zs-lx'));
    var rows = [].slice.call(sec.querySelectorAll('.zs-layers__item'));
    var user = false, timer = null;
    function hl(i) {
      draw.classList.toggle('has-hl', i >= 0);
      gs.forEach(function (g, k) { g.classList.toggle('is-hl', k === i); });
      rows.forEach(function (r, k) { r.classList.toggle('is-hl', k === i); });
    }
    function take(i) { user = true; clearInterval(timer); hl(i); }
    rows.forEach(function (r, i) {
      r.setAttribute('tabindex', '0');
      r.addEventListener('mouseenter', function () { take(i); });
      r.addEventListener('focus', function () { take(i); });
      r.addEventListener('click', function () { take(i); });
    });
    gs.forEach(function (g, i) {
      g.addEventListener('mouseenter', function () { take(i); });
      g.addEventListener('click', function () { take(i); });
    });
    sec.addEventListener('mouseleave', function () { if (user) hl(-1); });
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduce || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (es) {
      if (!es[0].isIntersecting) return; io.disconnect();
      var i = 0;
      setTimeout(function () {
        if (user) return;
        hl(0);
        timer = setInterval(function () {      /* one tour, then rest: no endless motion */
          if (user) return clearInterval(timer);
          i++; if (i >= gs.length) { clearInterval(timer); hl(-1); return; }
          hl(i);
        }, 1800);
      }, gs.length * 220 + 900);
    }, { threshold: 0.35 });
    io.observe(draw);
  });
})();
