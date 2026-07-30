/* Modifica delle pagine direttamente nel browser — SOLO in locale.
 *
 * Viene iniettato da tools/edit_server.py quando l'indirizzo contiene ?edit=1.
 * Nelle pagine pubblicate non c'e' nulla di tutto questo.
 *
 * Si modifica la lingua principale (italiano) e le formule. Le altre lingue non
 * si toccano: il server annota ogni modifica nel registro, e l'allineamento
 * delle traduzioni si fa dopo, in un colpo solo.
 *
 * Le formule e i rimandi alle figure dentro un paragrafo restano BLOCCHI ATOMICI:
 * si possono spostare o cancellare, non corrompere. Al salvataggio vengono
 * rimessi esattamente come stanno nel sorgente, perche' nella pagina viva sono
 * stati trasformati (MathJax li rende in SVG, app.js sposta la parola "Fig.").
 */
(function () {
  'use strict';

  var FILE = document.currentScript.getAttribute('data-file');
  var TEXT_SEL = 'main .it';
  var EQ_SEL = '[data-tex]';
  var REF_SEL = 'a.ref';

  var src = null;          // porzioni di sorgente grezzo, dal server
  var pending = {};        // chiave "text:3" / "tex:7" -> modifica in sospeso
  var bar, status, saveBtn;

  /* ---------------------------------------------------------------- utilita' */

  function esc(s) { return s.replace(/[&<>]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]; }); }

  function post(path, body) {
    return fetch('/__edit/' + path, {
      method: 'POST', headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }).then(function (r) { return r.json(); });
  }

  function count() { return Object.keys(pending).length; }

  function refresh() {
    var n = count();
    status.textContent = n === 0 ? 'nessuna modifica'
      : n === 1 ? '1 modifica non salvata' : n + ' modifiche non salvate';
    bar.classList.toggle('dirty', n > 0);
    saveBtn.disabled = n === 0;
  }

  /* ------------------------------------------------- blocchi atomici nel testo */

  // Nel sorgente le formule e i rimandi sono queste stringhe; nella pagina viva
  // sono altro. Al salvataggio si rimettono al loro posto per indice.
  function rawParts(raw, kind) {
    var re = kind === 'eq'
      ? /<span[^>]*data-tex="[^"]*"[^>]*>[\s\S]*?<\/span>/g
      : /<a class="ref"[\s\S]*?<\/a>/g;
    return raw.match(re) || [];
  }

  function freeze(el) {
    el.querySelectorAll(EQ_SEL + ',' + REF_SEL).forEach(function (n) {
      n.setAttribute('contenteditable', 'false');
      n.classList.add('lq-atom');
    });
  }

  function serialize(el, raw) {
    var clone = el.cloneNode(true);
    [['eq', EQ_SEL], ['ref', REF_SEL]].forEach(function (p) {
      var parts = rawParts(raw, p[0]);
      var nodes = clone.querySelectorAll(p[1]);
      for (var i = 0; i < nodes.length; i++) {
        var ph = document.createElement('template');
        ph.innerHTML = '';
        var marker = document.createComment('lq' + p[0] + i);
        nodes[i].parentNode.replaceChild(marker, nodes[i]);
      }
      var out = clone.innerHTML;
      for (var j = 0; j < nodes.length; j++) {
        out = out.replace('<!--lq' + p[0] + j + '-->', parts[j] !== undefined ? parts[j] : '');
      }
      clone.innerHTML = out;
    });
    return clone.innerHTML.trim();
  }

  /* ------------------------------------------------------------ testo italiano */

  function setupText() {
    var live = Array.prototype.slice.call(document.querySelectorAll(TEXT_SEL));
    if (live.length !== src.lang[src.primary].length) {
      throw new Error('la pagina non corrisponde al file (' + live.length +
        ' frasi qui, ' + src.lang[src.primary].length + ' nel sorgente): ricarica');
    }
    live.forEach(function (el, i) {
      var raw = src.lang[src.primary][i].raw;
      el.classList.add('lq-editable');
      el.dataset.lqIndex = i;
      el.addEventListener('dblclick', function (ev) {
        if (ev.altKey) return;
        start(el, i, raw);
      });
    });
  }

  function commit(el, i, raw) {
    var now = serialize(el, raw);
    var key = 'text:' + i;
    if (now === raw.trim()) {
      delete pending[key];
      el.classList.remove('lq-changed');
    } else {
      pending[key] = { kind: 'text', index: i, old: raw, html: now };
      el.classList.add('lq-changed');
    }
    refresh();
  }

  function start(el, i, raw) {
    if (el.isContentEditable) return;
    freeze(el);
    el.setAttribute('contenteditable', 'true');
    el.classList.add('lq-editing');
    el.focus();
    // si annota mentre si scrive: cosi' premere "Salva" senza uscire dal
    // paragrafo non fa perdere nulla
    var timer = null;
    function onInput() {
      clearTimeout(timer);
      timer = setTimeout(function () { commit(el, i, raw); }, 350);
    }
    el.addEventListener('input', onInput);
    el.addEventListener('blur', function done() {
      el.removeEventListener('blur', done);
      el.removeEventListener('input', onInput);
      clearTimeout(timer);
      el.removeAttribute('contenteditable');
      el.classList.remove('lq-editing');
      commit(el, i, raw);
    });
  }

  /* -------------------------------------------------------------------- formule */

  function setupEq() {
    var live = Array.prototype.slice.call(document.querySelectorAll('main ' + EQ_SEL));
    if (live.length !== src.tex.length) {
      throw new Error('formule non allineate col file: ricarica');
    }
    live.forEach(function (el, i) {
      el.classList.add('lq-eq');
      el.addEventListener('dblclick', function (ev) {
        if (ev.altKey) return;
        ev.stopPropagation();
        openEq(el, i);
      });
    });
  }

  var dlg, dlgTa, dlgPrev, dlgErr, dlgTarget;

  function buildDialog() {
    dlg = document.createElement('div');
    dlg.className = 'lq-dlg';
    dlg.innerHTML =
      '<div class="lq-dlg-box">' +
      '  <div class="lq-dlg-head">Formula · LaTeX</div>' +
      '  <textarea spellcheck="false"></textarea>' +
      '  <div class="lq-dlg-prev"></div>' +
      '  <div class="lq-dlg-err"></div>' +
      '  <div class="lq-dlg-foot">' +
      '    <button data-a="cancel">Annulla</button>' +
      '    <button data-a="ok" class="go">Applica</button>' +
      '  </div>' +
      '</div>';
    document.body.appendChild(dlg);
    dlgTa = dlg.querySelector('textarea');
    dlgPrev = dlg.querySelector('.lq-dlg-prev');
    dlgErr = dlg.querySelector('.lq-dlg-err');
    dlgTa.addEventListener('input', preview);
    dlg.addEventListener('click', function (ev) {
      var a = ev.target.getAttribute && ev.target.getAttribute('data-a');
      if (a === 'cancel' || ev.target === dlg) close();
      if (a === 'ok') accept();
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape' && dlg.classList.contains('on')) close();
    });
  }

  var previewTimer = null;
  function preview() {
    clearTimeout(previewTimer);
    previewTimer = setTimeout(function () {
      var tex = dlgTa.value.trim();
      var display = dlgTarget.el.classList.contains('eq-mml-block');
      dlgErr.textContent = '';
      if (!window.MathJax || !MathJax.tex2svgPromise) return;
      MathJax.texReset();
      MathJax.tex2svgPromise(tex, { display: display }).then(function (node) {
        dlgPrev.innerHTML = '';
        dlgPrev.appendChild(node);
        var bad = dlgPrev.querySelector('[data-mml-node="merror"], [fill="red"]');
        dlgErr.textContent = bad ? 'MathJax non capisce questo LaTeX' : '';
      }).catch(function (e) { dlgErr.textContent = String(e.message || e); });
    }, 180);
  }

  function openEq(el, i) {
    if (!dlg) buildDialog();
    dlgTarget = { el: el, i: i };
    dlgTa.value = src.tex[i].tex;
    dlg.classList.add('on');
    preview();
    dlgTa.focus();
  }

  function close() { dlg.classList.remove('on'); }

  function accept() {
    var tex = dlgTa.value.trim();
    var i = dlgTarget.i, key = 'tex:' + i;
    if (tex === src.tex[i].tex) { delete pending[key]; dlgTarget.el.classList.remove('lq-changed'); }
    else {
      pending[key] = { kind: 'tex', index: i, old: src.tex[i].raw, tex: tex };
      dlgTarget.el.classList.add('lq-changed');
    }
    close();
    refresh();
  }

  /* ------------------------------------------------------- apertura in VS Code */

  function lineOf(node) {
    var el = node.closest ? node.closest('[data-lq-index],' + EQ_SEL) : null;
    if (!el) return 1;
    if (el.hasAttribute('data-lq-index')) return src.lang[src.primary][+el.dataset.lqIndex].line;
    var all = Array.prototype.slice.call(document.querySelectorAll('main ' + EQ_SEL));
    var k = all.indexOf(el);
    return k >= 0 && src.tex[k] ? src.tex[k].line : 1;
  }

  function setupAltClick() {
    document.addEventListener('click', function (ev) {
      if (!ev.altKey) return;
      ev.preventDefault();
      post('open', { file: FILE, line: lineOf(ev.target) }).then(function (r) {
        if (!r.ok) note(r.error || 'non riesco ad aprire VS Code', true);
      });
    }, true);
  }

  /* ------------------------------------------------------------------ barra */

  function note(msg, bad) {
    status.textContent = msg;
    bar.classList.toggle('bad', !!bad);
    if (!bad) setTimeout(refresh, 2500);
  }

  function save() {
    var active = document.querySelector('.lq-editing');
    if (active) active.blur();                 // chiude l'ultima modifica in corso
    var edits = Object.keys(pending).map(function (k) { return pending[k]; });
    if (!edits.length) return;
    saveBtn.disabled = true;
    post('save', { file: FILE, edits: edits }).then(function (r) {
      if (r.error) { note('NON salvato — ' + r.error, true); saveBtn.disabled = false; return; }
      pending = {};
      note('salvate ' + r.saved + ' modifiche · ricarico…');
      setTimeout(function () { location.reload(); }, 700);
    });
  }

  /* ----------------------------------------------------- spostare i blocchi */

  // Lo spostamento non passa dalla coda delle modifiche: scrive subito, uno
  // scambio alla volta. Riordinare si giudica guardando, e chi guarda vuole
  // vedere il risultato mentre decide, non dopo aver premuto Salva.
  function setupMove() {
    var main = document.querySelector('main article') || document.querySelector('main');
    if (!main) return;
    var blocchi = Array.prototype.filter.call(main.children, function (el) {
      return /^(P|FIGURE|DIV|UL|OL|TABLE|BLOCKQUOTE|PRE|H2|H3|H4|HR)$/.test(el.tagName);
    });
    blocchi.forEach(function (el, i) {
      el.classList.add('lq-blocco');
      var cmd = document.createElement('span');
      cmd.className = 'lq-move';
      cmd.innerHTML =
        '<button title="sposta sopra" data-verso="-1">↑</button>' +
        '<button title="sposta sotto" data-verso="1">↓</button>';
      if (i === 0) cmd.querySelector('[data-verso="-1"]').disabled = true;
      if (i === blocchi.length - 1) cmd.querySelector('[data-verso="1"]').disabled = true;
      cmd.addEventListener('click', function (ev) {
        var b = ev.target.closest('button');
        if (!b || b.disabled) return;
        ev.preventDefault();
        if (count()) { note('salva prima le modifiche al testo', true); return; }
        muovi(i, parseInt(b.getAttribute('data-verso'), 10));
      });
      el.appendChild(cmd);
    });
  }

  function muovi(indice, verso) {
    var y = window.scrollY;
    post('move', { file: FILE, index: indice, verso: verso }).then(function (r) {
      if (r.error) { note(r.error, true); return; }
      sessionStorage.setItem('lq-scroll', String(y));
      location.reload();
    });
  }

  function buildBar() {
    bar = document.createElement('div');
    bar.className = 'lq-bar';
    bar.innerHTML =
      '<span class="lq-tag">modifica locale</span>' +
      '<span class="lq-status"></span>' +
      '<span class="lq-help">doppio clic per modificare · ↑↓ per spostare · Alt+clic apre VS Code</span>' +
      '<button class="lq-save">Salva</button>';
    document.body.appendChild(bar);
    status = bar.querySelector('.lq-status');
    saveBtn = bar.querySelector('.lq-save');
    saveBtn.addEventListener('click', save);
    window.addEventListener('beforeunload', function (ev) {
      if (count()) { ev.preventDefault(); ev.returnValue = ''; }
    });
    var y = sessionStorage.getItem('lq-scroll');
    if (y !== null) { sessionStorage.removeItem('lq-scroll'); window.scrollTo(0, +y); }
  }

  /* -------------------------------------------------------------------- avvio */

  fetch('/__edit/spans?file=' + encodeURIComponent(FILE))
    .then(function (r) { return r.json(); })
    .then(function (data) {
      if (data.error) throw new Error(data.error);
      src = data;
      document.documentElement.setAttribute('data-lang', src.primary);
      buildBar();
      setupText();
      setupEq();
      setupMove();
      setupAltClick();
      refresh();
      document.body.classList.add('lq-edit-on');
    })
    .catch(function (e) {
      if (!bar) buildBar();
      note('modifica non attiva — ' + (e.message || e), true);
    });
})();
