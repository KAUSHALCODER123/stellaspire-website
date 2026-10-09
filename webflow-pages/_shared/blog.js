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
