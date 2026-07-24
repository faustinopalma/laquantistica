// Toggle di lingua IT/EN — condivide la scelta con la landing (localStorage 'site-lang')
(function () {
  var KEY = 'site-lang';
  var root = document.documentElement;

  function detect() {
    var s = null;
    try { s = localStorage.getItem(KEY); } catch (e) {}
    if (s === 'it' || s === 'en') return s;
    var n = (navigator.language || navigator.userLanguage || 'it').toLowerCase();
    return n.indexOf('it') === 0 ? 'it' : 'en';
  }

  function apply(l) {
    root.setAttribute('data-lang', l);
    root.setAttribute('lang', l);
    document.querySelectorAll('.langbtn').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-l') === l ? 'true' : 'false');
    });
  }

  // Su mobile il selettore di lingua è nascosto nel menù laterale: se il controllo
  // vive solo nella sidebar, aggiungiamo una piccola pillola IT/EN fissa e sempre visibile.
  if (document.querySelector('.sidebar .langsw') && !document.querySelector('.langsw-mobile')) {
    var m = document.createElement('div');
    m.className = 'langsw-mobile';
    m.setAttribute('role', 'group');
    m.setAttribute('aria-label', 'Lingua / Language');
    m.innerHTML = '<span class="lg" aria-hidden="true">\uD83C\uDF10</span>' +
      '<button class="langbtn" type="button" data-l="it">IT</button>' +
      '<button class="langbtn" type="button" data-l="en">EN</button>';
    document.body.appendChild(m);
  }

  apply(detect());

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.langbtn') : null;
    if (!b) return;
    var l = b.getAttribute('data-l');
    try { localStorage.setItem(KEY, l); } catch (e2) {}
    apply(l);
  });
})();
