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
