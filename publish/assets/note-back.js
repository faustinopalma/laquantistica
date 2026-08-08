/* note-back.js — ritorno al punto di lettura nelle note.
   La stessa nota è richiamata da capitoli diversi: la destinazione arriva da
   ?ret=<pagina.html%23ancora> e viene applicata al richiamo in testata, alla
   pillola sempre visibile e al pulsante di fine nota. Senza ?ret= vale la
   destinazione già scritta nel documento. */
(function () {
  var CAPITOLI = {
    '03-elettroni.html':                ['Cap. 01 \u00b7 Esperimenti con gli Elettroni', 'Ch. 01 \u00b7 Experiments with Electrons'],
    '04-diffrazione.html':              ['Cap. 02 \u00b7 Diffrazione degli Elettroni', 'Ch. 02 \u00b7 Electron Diffraction'],
    '04b-forma-evoluzione.html':        ['Cap. 03 \u00b7 La forma dell’equazione di evoluzione', 'Ch. 03 \u00b7 The Form of the Evolution Equation'],
    '04c-hamiltoniana.html':            ['Cap. 04 \u00b7 L’hamiltoniana e l’equazione di Schrödinger', 'Ch. 04 \u00b7 The Hamiltonian and the Schrödinger Equation'],
    '05-rutherford.html':               ['Cap. 05 \u00b7 Esperimento di Rutherford', 'Ch. 05 \u00b7 The Rutherford Experiment'],
    '05b-diffusione.html':              ['Cap. 06 \u00b7 La formula di diffusione di Rutherford', 'Ch. 06 \u00b7 Rutherford’s Scattering Formula'],
    '07-franck-hertz.html':             ['Cap. 07 \u00b7 Esperimento di Franck-Hertz', 'Ch. 07 \u00b7 The Franck–Hertz Experiment'],
    '08-effetto-fotoelettrico.html':    ['Cap. 08 \u00b7 Effetto Fotoelettrico', 'Ch. 08 \u00b7 The Photoelectric Effect'],
    '01-stern-gerlach.html':            ['Cap. 09 \u00b7 Esperimento di Stern-Gerlach', 'Ch. 09 \u00b7 The Stern–Gerlach Experiment'],
    '02-stern-gerlach-cascata.html':    ['Cap. 10 \u00b7 Esperimenti di Stern-Gerlach in cascata', 'Ch. 10 \u00b7 Cascaded Stern–Gerlach Experiments'],
    '06-ulteriori-sviluppi.html':       ['Cap. 11 \u00b7 Ulteriori sviluppi della Teoria', 'Ch. 11 \u00b7 Further Developments of the Theory'],
    '09-spettri-atomici.html':          ['Cap. 12 \u00b7 Spettri atomici di emissione', 'Ch. 12 \u00b7 Atomic Emission Spectra']
  };

  function destinazioneValida(v) {
    if (!v) return null;
    try { v = decodeURIComponent(v); } catch (e) { return null; }
    if (v.indexOf('..') !== -1 || v.indexOf('//') !== -1) return null;
    if (/^[A-Za-z0-9._\/-]+\.html(#[A-Za-z0-9._-]+)?$/.test(v)) return v;
    return null;
  }

  function nomePagina(u) {
    return u.split('#')[0].split('?')[0].split('/').pop().replace(/\.html$/, '');
  }

  var crumb = document.getElementById('backCrumb');
  var fondo = document.getElementById('backBottom');
  var predefinita = (crumb && crumb.getAttribute('href')) || (fondo && fondo.getAttribute('href'));
  if (!predefinita) return;

  var richiesta = new URLSearchParams(location.search).get('ret');
  var ret = destinazioneValida(richiesta) || predefinita;
  var etichette = CAPITOLI[ret.split('#')[0].split('/').pop()];

  function testo(el, i) {
    if (el) el.textContent = etichette[i];
  }
  if (crumb) {
    crumb.setAttribute('href', ret);
    if (etichette) {
      testo(crumb.querySelector('.cap.it'), 0);
      testo(crumb.querySelector('.cap.en'), 1);
    }
  }
  if (fondo) fondo.setAttribute('href', ret);

  /* Pillola sempre visibile: il ritorno non deve dipendere da dove si è arrivati a leggere. */
  var breve = etichette
    ? [etichette[0].split('\u00b7')[0].trim(), etichette[1].split('\u00b7')[0].trim()]
    : null;
  var pillola = document.createElement('a');
  pillola.className = 'note-back-fab';
  pillola.setAttribute('href', ret);
  var freccia = document.createElement('span');
  freccia.className = 'nb-arrow';
  freccia.setAttribute('aria-hidden', 'true');
  freccia.textContent = '\u2190';
  pillola.appendChild(freccia);
  [['it', breve ? 'Torna al ' + breve[0] : 'Torna al capitolo'],
   ['en', breve ? 'Back to ' + breve[1] : 'Back to the chapter']].forEach(function (v) {
    var s = document.createElement('span');
    s.className = v[0];
    s.textContent = v[1];
    pillola.appendChild(s);
  });
  document.body.appendChild(pillola);

  /* In fondo alla nota c'è già il pulsante grande: lì la pillola sparisce. */
  var fine = document.querySelector('.doc-return');
  if (fine && 'IntersectionObserver' in window) {
    new IntersectionObserver(function (voci) {
      pillola.classList.toggle('is-hidden', voci[0].isIntersecting);
    }).observe(fine);
  }

  /* Su schermo stretto la pillola coprirebbe il testo: si ritira mentre si legge
     (scorrimento in avanti) e ricompare appena si torna indietro. */
  var stretta = window.matchMedia('(max-width:860px)');
  var precedente = window.pageYOffset;
  window.addEventListener('scroll', function () {
    var y = window.pageYOffset;
    if (!stretta.matches) pillola.classList.remove('is-away');
    else if (y > precedente + 8 && y > 140) pillola.classList.add('is-away');
    else if (y < precedente - 8) pillola.classList.remove('is-away');
    precedente = y;
  }, { passive: true });

  /* Se si è arrivati proprio da quella pagina, si torna con la cronologia:
     così si ritrova la posizione esatta invece dell'ancora del richiamo. */
  var cronologiaIniziale = history.length;
  function daQuellaPagina() {
    if (!document.referrer) return false;
    var r;
    try { r = new URL(document.referrer); } catch (e) { return false; }
    return r.origin === location.origin && nomePagina(r.pathname) === nomePagina(ret);
  }
  [crumb, fondo, pillola].forEach(function (a) {
    if (!a) return;
    a.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if (history.length !== cronologiaIniziale || !daQuellaPagina()) return;
      e.preventDefault();
      history.back();
    });
  });

  /* Il cambio di lingua ricarica la nota: senza questo si perderebbe il punto di ritorno. */
  if (richiesta) {
    document.querySelectorAll('a.langbtn[href]').forEach(function (a) {
      if (a.getAttribute('href').indexOf('?') === -1) {
        a.setAttribute('href', a.getAttribute('href') + '?ret=' + encodeURIComponent(ret));
      }
    });
  }
})();
