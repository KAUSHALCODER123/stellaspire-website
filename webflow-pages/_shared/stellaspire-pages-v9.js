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

// Stellaspire v6 motion layer: hero depth, parallax, tilt, count-up, reels, reading progress.
// Transform/opacity only, one rAF loop, passive listeners. Skipped entirely for reduced motion
// except the video players, which always work.
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  var root = document.documentElement;

  // ---------- Founder reels: load the video only when someone taps play ----------
  function stopOthers(except) {
    document.querySelectorAll('.reel video, .reel-dialog video').forEach(function (v) { if (v !== except) v.pause(); });
  }
  function track(name, label) {
    if (window.gtag) window.gtag('event', name, { video_title: label });
  }
  document.querySelectorAll('.reel[data-video]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (btn.classList.contains('is-playing')) return;
      var title = btn.getAttribute('data-title');
      var v = document.createElement('video');
      v.src = btn.getAttribute('data-video');
      v.poster = (btn.querySelector('img') || {}).src || '';
      v.controls = true; v.playsInline = true; v.setAttribute('playsinline', '');
      v.addEventListener('play', function () { stopOthers(v); });
      v.addEventListener('ended', function () { track('video_complete', title); });
      btn.appendChild(v);
      btn.classList.add('is-playing');
      btn.removeAttribute('aria-label');
      v.play().catch(function () {});
      v.focus();
      track('video_start', title);
    });
  });

  // Hero "watch" button opens the same video in a dialog
  document.querySelectorAll('[data-open-reel]').forEach(function (btn) {
    var dlg = document.getElementById(btn.getAttribute('data-open-reel'));
    if (!dlg || !dlg.showModal) return;
    var v = dlg.querySelector('video');
    btn.addEventListener('click', function () {
      if (!v.src) v.src = v.getAttribute('data-src');
      dlg.showModal(); stopOthers(v); v.play().catch(function () {});
      track('video_start', btn.getAttribute('data-title'));
    });
    dlg.addEventListener('close', function () { v.pause(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.querySelector('.reel-dialog-close').addEventListener('click', function () { dlg.close(); });
  });

  if (reduce) return;

  // ---------- Count-up for result numbers ----------
  var counters = document.querySelectorAll('.result-number');
  if ('IntersectionObserver' in window && counters.length) {
    var cio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        cio.unobserve(e.target);
        var el = e.target, text = el.textContent, m = text.match(/[\d,]+/);
        if (!m) return;
        var end = parseInt(m[0].replace(/,/g, ''), 10), t0 = performance.now(), dur = 1400;
        (function step(t) {
          var k = Math.min(1, (t - t0) / dur), val = Math.round(end * (1 - Math.pow(1 - k, 3)));
          el.textContent = text.replace(m[0], val.toLocaleString('en-IN'));
          if (k < 1) requestAnimationFrame(step); else el.textContent = text;
        })(t0);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { cio.observe(c); });
  }

  // ---------- Scroll-linked: hero depth, image parallax, reading progress ----------
  var hero = document.querySelector('.hero--live');
  var frames = [].slice.call(document.querySelectorAll('.photo, .article-cover')).filter(function (f) { return f.querySelector('img'); });
  frames.forEach(function (f) { f.classList.add('has-parallax'); });
  var article = document.querySelector('.article-layout');
  var bar = null;
  if (article) { bar = document.createElement('div'); bar.className = 'read-progress'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar); }

  var ticking = false;
  function onFrame() {
    ticking = false;
    var vh = window.innerHeight;
    if (hero) {
      var h = hero.offsetHeight || 1;
      hero.style.setProperty('--sy', Math.min(1, Math.max(0, window.scrollY / h)).toFixed(3));
    }
    frames.forEach(function (f) {
      var r = f.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh) return;
      var k = (r.top + r.height / 2 - vh / 2) / vh; // -1..1 around centre
      f.style.setProperty('--py', (k * -36).toFixed(1) + 'px');
    });
    if (bar) {
      var a = article.getBoundingClientRect();
      var p = Math.min(1, Math.max(0, -a.top / Math.max(1, a.height - vh)));
      bar.style.setProperty('--p', p.toFixed(3));
    }
  }
  function req() { if (!ticking) { ticking = true; requestAnimationFrame(onFrame); } }
  window.addEventListener('scroll', req, { passive: true });
  window.addEventListener('resize', req, { passive: true });
  onFrame();

  if (!fine) return;

  // ---------- Hero: pointer drives the 3D mark and floating chips ----------
  if (hero) {
    var mx = 0, my = 0, pending = false;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      mx = ((e.clientX - r.left) / r.width - 0.5) * 2;
      my = ((e.clientY - r.top) / r.height - 0.5) * 2;
      if (!pending) { pending = true; requestAnimationFrame(function () {
        pending = false; hero.style.setProperty('--mx', mx.toFixed(3)); hero.style.setProperty('--my', my.toFixed(3));
      }); }
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { hero.style.setProperty('--mx', 0); hero.style.setProperty('--my', 0); });
  }

  // ---------- 3D tilt with glare ----------
  document.querySelectorAll('.card, .post-card, .reel-card, .result').forEach(function (el) {
    el.classList.add('tilt');
    var raf = 0;
    el.addEventListener('pointerenter', function () { el.style.transitionDelay = '0ms'; });
    el.addEventListener('pointermove', function (e) {
      var r = el.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        el.classList.add('is-tilting');
        el.style.setProperty('--ry', ((x - 0.5) * 8).toFixed(2) + 'deg');
        el.style.setProperty('--rx', ((0.5 - y) * 8).toFixed(2) + 'deg');
        el.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
        el.style.setProperty('--gy', (y * 100).toFixed(1) + '%');
      });
    }, { passive: true });
    el.addEventListener('pointerleave', function () {
      cancelAnimationFrame(raf); el.classList.remove('is-tilting');
      el.style.setProperty('--rx', '0deg'); el.style.setProperty('--ry', '0deg');
    });
  });

  // ---------- Magnetic primary buttons ----------
  document.querySelectorAll('.hero .button, .cta-band .button, .hero-watch').forEach(function (b) {
    b.classList.add('magnetic');
    b.addEventListener('pointermove', function (e) {
      var r = b.getBoundingClientRect();
      b.style.setProperty('--tx', ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px');
      b.style.setProperty('--ty', ((e.clientY - r.top - r.height / 2) * 0.3).toFixed(1) + 'px');
    }, { passive: true });
    b.addEventListener('pointerleave', function () { b.style.setProperty('--tx', '0px'); b.style.setProperty('--ty', '0px'); });
  });
})();

// Home hero motion graphic: a live Stellaspire search.
// Each mandate plays brief -> market map -> shortlist -> offer accepted, then the next mandate.
// Illustrative, anonymised profiles. DOM + CSS transitions only; pauses off-screen; static for reduced motion.
(function () {
  var hero = document.querySelector('.hero--live');
  if (!hero) return;
  var card = hero.querySelector('.ls-card');
  var rowsEl = hero.querySelector('.ls-rows');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var MANDATES = [
    { role: 'Chief Financial Officer', client: 'Series C fintech · Bengaluru', tags: ['Finance leadership', 'Confidential'],
      offer: 'CFO · Series C fintech',
      rows: [['AK', 'CA · 16 yrs · listed NBFC', 92, 1], ['RS', 'MBA · 12 yrs · consumer tech', 58, 0], ['PM', 'CA · 14 yrs · fintech, IPO prep', 88, 1],
             ['VJ', 'CPA · 18 yrs · manufacturing', 46, 0], ['NI', 'CA, CFA · 15 yrs · payments', 84, 1]] },
    { role: 'Head of Analytics', client: 'Global Capability Centre · Hyderabad', tags: ['Analytics leadership', 'GCC set-up'],
      offer: 'Head of Analytics · GCC',
      rows: [['SD', '15 yrs · BFSI analytics', 90, 1], ['KR', '9 yrs · BI, retail', 52, 0], ['AM', '13 yrs · data science, GCC', 87, 1],
             ['TB', '11 yrs · marketing analytics', 49, 0], ['LP', '14 yrs · risk analytics', 83, 1]] },
    { role: 'ML Engineering Lead', client: 'AI scale-up · Bengaluru', tags: ['AI & ML', 'Hands-on lead'],
      offer: 'ML Engineering Lead · AI scale-up',
      rows: [['RV', '10 yrs · NLP, production ML', 91, 1], ['HG', '6 yrs · research only', 55, 0], ['MS', '11 yrs · MLOps, platform', 86, 1],
             ['DK', '8 yrs · computer vision', 61, 0], ['AT', '12 yrs · recsys, team lead', 85, 1]] }
  ];

  var timers = [], idx = 0, visible = true, paused = false;
  function later(fn, ms) { timers.push(setTimeout(fn, ms)); }
  function clear() { timers.forEach(clearTimeout); timers = []; }
  function $(sel) { return hero.querySelector(sel); }

  function render(m, i) {
    $('.ls-count').textContent = '0' + (i + 1) + ' / 0' + MANDATES.length;
    $('.ls-role').textContent = m.role;
    $('.ls-client').textContent = m.client;
    $('.ls-tags').innerHTML = m.tags.map(function (t) { return '<span>' + t + '</span>'; }).join('');
    $('.ls-toast small').textContent = m.offer;
    rowsEl.innerHTML = m.rows.map(function (r, k) {
      return '<li class="ls-row" data-fit="' + r[3] + '" style="--d:' + (k * 140) + 'ms;--m:' + r[2] + '%">' +
        '<span class="ls-av">' + r[0] + '</span><span class="ls-who"><b>Candidate ' + r[0].charAt(0) + '.' + r[0].charAt(1) + '.</b><small>' + r[1] + '</small></span>' +
        '<span class="ls-match"><i></i></span><span class="ls-state"></span></li>';
    }).join('');
  }

  function stage(n) { hero.setAttribute('data-stage', n); }

  function play() {
    clear();
    var m = MANDATES[idx];
    card.classList.add('is-swapping');
    later(function () {
      render(m, idx); stage(1);
      card.classList.remove('is-swapping');
    }, 380);
    later(function () { stage(2); }, 1300);   // market map: profiles stream in
    later(function () { stage(3); }, 3400);   // shortlist: non-fits drop, fits get ticked
    later(function () { stage(4); }, 5200);   // offer accepted
    later(function () { idx = (idx + 1) % MANDATES.length; if (visible && !paused) play(); }, 8600);
  }

  if (reduce) { render(MANDATES[0], 0); stage(4); return; }

  // Pause when the hero is off-screen or the tab is hidden; resume from the next mandate
  if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
    var was = visible; visible = es[0].isIntersecting;
    if (visible && !was && !paused) play(); else if (!visible) clear();
  }).observe(hero);
  document.addEventListener('visibilitychange', function () {
    if (document.hidden) clear(); else if (visible && !paused) play();
  });

  // Gentle 3D depth that follows the pointer (fine pointers only)
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var scene = hero.querySelector('.scene-3d'), pending = false, mx = 0, my = 0;
    hero.addEventListener('pointermove', function (e) {
      var r = hero.getBoundingClientRect();
      mx = (e.clientX - r.left) / r.width - 0.5; my = (e.clientY - r.top) / r.height - 0.5;
      if (!pending) { pending = true; requestAnimationFrame(function () {
        pending = false; scene.style.setProperty('--rx', (my * -6).toFixed(2) + 'deg'); scene.style.setProperty('--ry', (mx * 8).toFixed(2) + 'deg');
      }); }
    }, { passive: true });
    hero.addEventListener('pointerleave', function () { scene.style.setProperty('--rx', '0deg'); scene.style.setProperty('--ry', '0deg'); });
  }

  render(MANDATES[0], 0); stage(1);
  play();
})();

// Blog articles: checklist (remembered per browser), active TOC link, timeline reveal, share buttons.
(function () {
  // ---------- Checklists ----------
  document.querySelectorAll('.checklist[data-checklist]').forEach(function (box) {
    var key = 'ss-checklist:' + box.getAttribute('data-checklist');
    var inputs = [].slice.call(box.querySelectorAll('input[type="checkbox"]'));
    var out = box.querySelector('.checklist-progress');
    var saved = [];
    try { saved = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
    inputs.forEach(function (inp, i) { inp.checked = saved.indexOf(i) > -1; });
    function update() {
      var done = inputs.filter(function (i) { return i.checked; }).length;
      if (out) {
        out.innerHTML = '<span>' + done + ' of ' + inputs.length + ' done</span><span class="checklist-bar" aria-hidden="true"><i></i></span>';
        out.style.setProperty('--done', Math.round(done / inputs.length * 100) + '%');
      }
      try { localStorage.setItem(key, JSON.stringify(inputs.map(function (inp, i) { return inp.checked ? i : -1; }).filter(function (i) { return i > -1; }))); } catch (e) {}
    }
    inputs.forEach(function (inp) {
      inp.addEventListener('change', function () {
        update();
        if (inp.checked && window.gtag) window.gtag('event', 'checklist_tick', { checklist: box.getAttribute('data-checklist') });
      });
    });
    update();
  });

  // ---------- Share ----------
  document.querySelectorAll('[data-share-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var done = function () { var t = btn.textContent; btn.textContent = 'Link copied'; setTimeout(function () { btn.textContent = t; }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(location.href.split('#')[0]).then(done, function () {});
    });
  });

  if (!('IntersectionObserver' in window)) return;

  // ---------- Active TOC link ----------
  var links = [].slice.call(document.querySelectorAll('.toc a[href^="#"]'));
  var map = {};
  links.forEach(function (a) { var el = document.getElementById(a.getAttribute('href').slice(1)); if (el) map[el.id] = a; });
  var ids = Object.keys(map);
  if (ids.length) {
    var current = null;
    var tio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) current = e.target.id; });
      if (current) links.forEach(function (a) { a.classList.toggle('is-active', a === map[current]); });
    }, { rootMargin: '-20% 0px -70% 0px' });
    ids.forEach(function (id) { tio.observe(document.getElementById(id)); });
  }

  // ---------- Timeline steps light up as they scroll in ----------
  var sio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); sio.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -30% 0px' });
  document.querySelectorAll('.step-timeline > li').forEach(function (li) { sio.observe(li); });
})();
