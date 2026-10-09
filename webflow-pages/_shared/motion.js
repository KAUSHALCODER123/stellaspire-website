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
