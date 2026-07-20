// Navigation: mobile toggle + highlight current page
(function () {
  var body = document.body;
  var toggle = document.querySelector('.menu-toggle');
  if (toggle) {
    toggle.addEventListener('click', function () {
      body.classList.toggle('nav-open');
    });
  }
  var scrim = document.querySelector('.scrim');
  if (scrim) {
    scrim.addEventListener('click', function () { body.classList.remove('nav-open'); });
  }
  // Mark active nav link based on current file name
  var current = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.sidebar nav a').forEach(function (a) {
    var href = a.getAttribute('href');
    if (href === current) { a.classList.add('active'); }
  });
})();

// Hover previews for references only; click jumps and offers a "return" button.
(function () {
  var pop = document.createElement('div');
  pop.className = 'ref-pop';
  document.body.appendChild(pop);

  var backBtn = document.createElement('button');
  backBtn.className = 'ref-return';
  backBtn.type = 'button';
  backBtn.innerHTML = '↩ Torna al punto di lettura';
  document.body.appendChild(backBtn);
  var returnY = null;

  function position(x, y) {
    var r = pop.getBoundingClientRect();
    var px = x + 18, py = y + 18;
    if (px + r.width > window.innerWidth - 8) px = x - r.width - 18;
    if (py + r.height > window.innerHeight - 8) py = y - r.height - 18;
    if (px < 8) px = 8;
    if (py < 8) py = 8;
    pop.style.left = px + 'px';
    pop.style.top = py + 'px';
  }
  function hide() { pop.classList.remove('show'); pop.innerHTML = ''; }

  // References -> preview on hover, jump + return button on click
  document.querySelectorAll('a.ref[data-ref]').forEach(function (a) {
    a.addEventListener('mouseenter', function (e) {
      var t = document.getElementById(a.getAttribute('data-ref'));
      if (!t) return;
      var media = t.querySelector('img, math, svg');
      var capEl = t.querySelector('figcaption');
      var inner = media ? media.outerHTML : t.innerHTML;
      var cap = capEl ? '<div class="cap">' + capEl.textContent + '</div>' : '';
      pop.innerHTML = '<div class="pv">' + inner + '</div>' + cap;
      pop.classList.add('show');
      position(e.clientX, e.clientY);
    });
    a.addEventListener('mousemove', function (e) { position(e.clientX, e.clientY); });
    a.addEventListener('mouseleave', hide);
    a.addEventListener('click', function (e) {
      var t = document.getElementById(a.getAttribute('data-ref'));
      if (!t) return;
      e.preventDefault();
      hide();
      returnY = window.pageYOffset;
      t.scrollIntoView({ behavior: 'smooth', block: 'center' });
      t.classList.remove('flash');
      void t.offsetWidth;
      t.classList.add('flash');
      backBtn.classList.add('show');
    });
  });

  backBtn.addEventListener('click', function () {
    if (returnY !== null) {
      window.scrollTo({ top: returnY, behavior: 'smooth' });
    }
    backBtn.classList.remove('show');
  });
})();
