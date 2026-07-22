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

  apply(detect());

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.langbtn') : null;
    if (!b) return;
    var l = b.getAttribute('data-l');
    try { localStorage.setItem(KEY, l); } catch (e2) {}
    apply(l);
  });
})();
