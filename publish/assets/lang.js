// Lingua IT/EN — la scelta esplicita (localStorage 'site-lang') vince sempre;
// solo in sua assenza si segue la lingua del browser. Gira prima che la pagina si dipinga.
(function () {
  var KEY = 'site-lang';
  var root = document.documentElement;

  function scelta() {
    try {
      var s = localStorage.getItem(KEY);
      if (s === 'it' || s === 'en') return s;
    } catch (e) {}
    return null;
  }

  // Prima delle lingue dichiarate dall'utente, in ordine, che il sito parla (RFC 4647); poi inglese.
  function dalBrowser() {
    var l = (navigator.languages && navigator.languages.length)
      ? navigator.languages
      : (navigator.language ? [navigator.language] : []);
    for (var i = 0; i < l.length; i++) {
      var t = String(l[i]).toLowerCase().split('-')[0];
      if (t === 'it') return 'it';
      if (t === 'en') return 'en';
    }
    return 'en';
  }

  function sincronizzaBottoni(l) {
    document.querySelectorAll('.langbtn').forEach(function (b) {
      b.setAttribute('aria-pressed', b.getAttribute('data-l') === l ? 'true' : 'false');
    });
  }

  function apply(l) {
    root.setAttribute('data-lang', l);
    root.setAttribute('lang', l);
    sincronizzaBottoni(l);
  }

  apply(scelta() || dalBrowser());

  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.langbtn') : null;
    if (!b) return;
    var l = b.getAttribute('data-l');
    try { localStorage.setItem(KEY, l); } catch (e2) {}
    apply(l);
  });

  // Bottoni e barra laterale non esistono ancora: il resto aspetta il documento.
  document.addEventListener('DOMContentLoaded', function () {
    sincronizzaBottoni(root.getAttribute('data-lang'));

    // Su mobile il selettore vive solo nel menù laterale: aggiungiamo una pillola fissa.
    if (document.querySelector('.sidebar .langsw') && !document.querySelector('.langsw-mobile')) {
      var m = document.createElement('div');
      m.className = 'langsw-mobile';
      m.setAttribute('role', 'group');
      m.setAttribute('aria-label', 'Lingua / Language');
      m.innerHTML = '<span class="lg" aria-hidden="true">\uD83C\uDF10</span>' +
        '<button class="langbtn" type="button" data-l="it">Italiano</button>' +
        '<button class="langbtn" type="button" data-l="en">English</button>';
      document.body.appendChild(m);
      sincronizzaBottoni(root.getAttribute('data-lang'));
    }
  });
})();
