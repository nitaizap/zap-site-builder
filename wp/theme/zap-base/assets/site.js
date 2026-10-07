/* Zap Base: mobile menu + header state. No dependencies. */
(function () {
  var b = document.querySelector('.zs-burger');
  var nav = document.getElementById('zs-nav');
  var root = document.documentElement;
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
  var h = document.querySelector('.zs-header');
  if (h) {
    var on = false;
    var tick = function () {
      var s = window.scrollY > 8;
      if (s !== on) { on = s; h.classList.toggle('is-scrolled', s); }
    };
    window.addEventListener('scroll', tick, { passive: true });
    tick();
  }
})();
