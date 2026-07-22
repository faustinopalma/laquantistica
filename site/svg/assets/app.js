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
  var scrollHideHandler = null;

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

  function hideBack() {
    backBtn.classList.remove('show');
    if (scrollHideHandler) {
      window.removeEventListener('scroll', scrollHideHandler);
      scrollHideHandler = null;
    }
  }

  // Semantic figure labels (Italian + English, singular/plural) that should be
  // absorbed into the reference link so the whole "figura 1" / "fig. 1" /
  // "Figure 1" is hoverable & clickable, not just the bare number.
  var LABEL = /(\b(?:figure|figura|figg|fig)\.?)([ \u00a0\t]*)$/i;

  // References -> preview on hover, jump + return button on click
  document.querySelectorAll('a.ref[data-ref]').forEach(function (a) {
    // Extend the interactive region to include the preceding label word.
    var prev = a.previousSibling;
    if (prev && prev.nodeType === 3) {
      var m = prev.nodeValue.match(LABEL);
      if (m) {
        prev.nodeValue = prev.nodeValue.slice(0, prev.nodeValue.length - m[0].length);
        a.insertBefore(document.createTextNode(m[1] + '\u00a0'), a.firstChild);
      }
    }

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

      // Auto-hide the "return" button once the reader has kept scrolling well
      // past the target: only arm hiding after the target first reaches center
      // (so the smooth-scroll itself never triggers it prematurely).
      if (scrollHideHandler) window.removeEventListener('scroll', scrollHideHandler);
      var reached = false;
      scrollHideHandler = function () {
        var rect = t.getBoundingClientRect();
        var offCenter = rect.top + rect.height / 2 - window.innerHeight / 2;
        if (!reached) {
          if (Math.abs(offCenter) < window.innerHeight * 0.5) reached = true;
          return;
        }
        if (Math.abs(offCenter) > window.innerHeight * 1.15) hideBack();
      };
      window.addEventListener('scroll', scrollHideHandler, { passive: true });
    });
  });

  backBtn.addEventListener('click', function () {
    if (returnY !== null) {
      window.scrollTo({ top: returnY, behavior: 'smooth' });
    }
    hideBack();
  });
})();

// Lightbox: click a figure image (or a ".zoom-link") to open it enlarged in an
// overlay. Click the overlay or press Esc to close. Gives a compact inline
// figure plus an on-demand large version.
(function () {
  var box = document.createElement('div');
  box.className = 'lightbox';
  box.innerHTML = '<button class="lightbox-close" type="button" aria-label="Chiudi">\u00d7</button><div class="lightbox-inner"></div>';
  document.body.appendChild(box);
  var inner = box.querySelector('.lightbox-inner');

  function open(src, alt) {
    inner.innerHTML = '';
    var img = document.createElement('img');
    img.src = src;
    if (alt) img.alt = alt;
    inner.appendChild(img);
    box.classList.add('show');
    document.body.classList.add('lightbox-open');
  }
  function close() {
    box.classList.remove('show');
    document.body.classList.remove('lightbox-open');
    inner.innerHTML = '';
  }

  // Any image inside a figure becomes zoomable.
  document.querySelectorAll('figure img').forEach(function (img) {
    img.classList.add('zoomable');
    img.addEventListener('click', function () { open(img.getAttribute('src'), img.getAttribute('alt')); });
  });

  // Explicit "enlarge" links: <a class="zoom-link" data-zoom="path.svg">.
  document.querySelectorAll('a.zoom-link[data-zoom]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      e.preventDefault();
      open(a.getAttribute('data-zoom'), a.getAttribute('data-alt'));
    });
  });

  box.addEventListener('click', function (e) {
    if (e.target === box || e.target.classList.contains('lightbox-close') || e.target === inner) close();
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && box.classList.contains('show')) close();
  });
})();
