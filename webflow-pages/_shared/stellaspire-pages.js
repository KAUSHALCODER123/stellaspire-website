(function () {
  // Mobile menu
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  var mobile = window.matchMedia('(max-width: 960px)');

  function syncMenu() {
    nav.hidden = mobile.matches;
    toggle.setAttribute('aria-expanded', 'false');
  }
  syncMenu();
  mobile.addEventListener('change', syncMenu);

  toggle.addEventListener('click', function () {
    var open = toggle.getAttribute('aria-expanded') === 'true';
    nav.hidden = open;
    toggle.setAttribute('aria-expanded', String(!open));
  });
  nav.addEventListener('click', function (e) {
    if (mobile.matches && e.target.closest('a')) {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobile.matches && !nav.hidden) {
      nav.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
      toggle.focus();
    }
  });

  // FAQ accordion (answers stay visible if JavaScript is off)
  document.querySelectorAll('.faq-button').forEach(function (button) {
    var answer = document.getElementById(button.getAttribute('aria-controls'));
    var icon = button.querySelector('.faq-icon');
    answer.hidden = true;
    button.setAttribute('aria-expanded', 'false');
    icon.textContent = '+';
    button.addEventListener('click', function () {
      var open = button.getAttribute('aria-expanded') === 'true';
      button.setAttribute('aria-expanded', String(!open));
      answer.hidden = open;
      icon.textContent = open ? '+' : '−';
    });
  });
})();


document.addEventListener('click',function(e){document.querySelectorAll('.nav-drop[open]').forEach(function(d){if(!d.contains(e.target))d.removeAttribute('open');});});
document.addEventListener('keydown',function(e){if(e.key==='Escape')document.querySelectorAll('.nav-drop[open]').forEach(function(d){d.removeAttribute('open');});});

// Micro-interactions: header shadow on scroll + gentle scroll reveal
(function () {
  var header = document.querySelector('.site-header');
  function onScroll() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
  onScroll(); window.addEventListener('scroll', onScroll, { passive: true });

  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var targets = document.querySelectorAll(
    'main section:not(.hero):not(.page-hero):not(.article-hero) .h2, .section-intro, .expertise-row, .step, .card, .post-card, ' +
    '.quote, .featured-article, .support-row, .tick-list li, .photo-band, .table-wrap, .faq-row, .short-answer, .method-grid > div, .cta-grid > div'
  );
  document.documentElement.classList.add('reveal-on');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  targets.forEach(function (el) {
    var sib = el.parentElement ? [].indexOf.call(el.parentElement.children, el) : 0;
    el.style.transitionDelay = Math.min(sib, 4) * 60 + 'ms';
    el.classList.add('reveal'); io.observe(el);
  });
})();
