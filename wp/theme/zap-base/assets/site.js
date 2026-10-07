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
          + ' .zs-contact__info, .zs-contact__map, .zs-prose-sec .zs-prose';
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
