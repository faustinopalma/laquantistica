# Formato "Scheda Tecnica" per le Note

Formato editoriale, stile **industriale / ingegneristico**, usato per le note a lato
della tesi (onestà intellettuale, dietro le quinte, aneddoti storici, ecc.).
È volutamente diverso dalle pagine dei capitoli, così le note si distinguono a colpo d'occhio.

> Nota di lavoro: questo formato è una prima scelta grafica e potrà essere ritoccato.
> Tutte le note condividono lo stesso CSS, quindi una modifica di stile si propaga a tutte.

## File coinvolti
- `publish/assets/note.css` — stile completo della scheda (griglia tecnica di sfondo,
  foglio con cornice tratteggiata, barra metadati monospace, sezioni con prefisso `//`,
  toggle lingua, pulsante di ritorno, footer tecnico). Riusabile da tutte le note.
- `publish/assets/lang.css` + `publish/assets/lang.js` — meccanica bilingue IT/EN
  (condivisa con i capitoli): mostra/nasconde gli span `.it`/`.en` in base a
  `html[data-lang]`, gestisce i pulsanti `.langbtn`, ricorda la scelta in
  `localStorage` (`site-lang`).
- `publish/assets/style.css` — contiene la classe `.nota-link`, il **callout** che si
  inserisce nel corpo di un capitolo per rimandare a una nota.

## Convenzioni
- **Nome file nota**: `nota-NN-slug.html` (es. `nota-01-stern-gerlach.html`), nella
  cartella `publish/` (stessa dei capitoli, così i path `assets/...` restano relativi).
- **Lingua**: le note sono **bilingui IT/EN** come i capitoli — stessa meccanica
  (`lang.css` + `lang.js`, span `.it`/`.en`, toggle `.langbtn` nella barra metadati).
  La scelta di lingua è condivisa con tutto il sito (`localStorage` `site-lang`).
- **Ritorno al punto di partenza (dinamico)**: la stessa nota può essere linkata da
  punti diversi, quindi il link di ritorno **non è statico**. Il callout passa
  `?ret=<pagina.html%23ancora>`; uno script nella nota valida il parametro (accetta solo
  path interni `.html` + eventuale `#ancora`, per sicurezza — no `javascript:`, no URL
  esterni) e imposta i due link "indietro" (`#backTop` e `#backBottom`).
  Fallback se `ret` manca o non è valido: il capitolo di riferimento.
- **Canonical**: ogni nota ha `<link rel="canonical" href="https://laquantistica.com/nota-...html">`.

## Struttura minima di una pagina nota
```html
<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="canonical" href="https://laquantistica.com/nota-NN-slug.html">
  <title>Nota NN · Titolo · La Quantistica</title>
  <link rel="stylesheet" href="assets/lang.css?v=3">
  <link rel="stylesheet" href="assets/note.css?v=2">
  <script defer src="assets/lang.js?v=3"></script>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">
    <div class="doc-meta">
      <span class="tag">Nota NN</span>
      <span class="it">Cap. NN · Titolo</span><span class="en">Ch. NN · Title</span>
      <span class="sep">|</span>
      <span class="tag amber"><span class="it">Etichetta</span><span class="en">Label</span></span>
      <div class="langsw" role="group" aria-label="Lingua / Language">
        <button class="langbtn" type="button" data-l="it" aria-pressed="true">IT</button>
        <button class="langbtn" type="button" data-l="en" aria-pressed="false">EN</button>
      </div>
      <a class="doc-back-top" id="backTop" href="NN-....html#nota-N"><span class="it">← Indietro</span><span class="en">← Back</span></a>
    </div>

    <h1 class="doc-title">
      <span class="lead"><span class="it">Occhiello</span><span class="en">Eyebrow</span></span>
      <span class="it">Titolo della nota</span><span class="en">Note title</span>
    </h1>

    <p class="lede"><span class="it">Primo paragrafo…</span><span class="en">First paragraph…</span></p>
    <p><span class="it">…usa <strong>grassetto</strong> ed <em>corsivo</em>.</span><span class="en">…use <strong>bold</strong> and <em>italic</em>.</span></p>
    <h2><span class="it">Sezione</span><span class="en">Section</span></h2>   <!-- il prefisso "// " lo aggiunge il CSS -->

    <div class="doc-return">
      <a id="backBottom" href="NN-....html#nota-N"><span class="it">← Torna al punto di lettura</span><span class="en">← Back to where you were</span></a>
    </div>
    <div class="doc-foot">
      <span>La Quantistica · Nota tecnica N.NN · Rev. 2026</span>
      <span>F. Palma</span>
    </div>
  </div>
</main>

<script>
/* Ritorno dinamico: legge ?ret=<pagina.html%23ancora>, lo valida e lo applica ai due link. */
(function () {
  function safeRet(v){
    if(!v) return null;
    try{ v = decodeURIComponent(v); }catch(e){ return null; }
    if(v.indexOf('..')!==-1 || v.indexOf('//')!==-1) return null;
    if(/^[A-Za-z0-9._\/-]+\.html(#[A-Za-z0-9._-]+)?$/.test(v)) return v;
    return null;
  }
  var ret = safeRet(new URLSearchParams(location.search).get('ret')) || 'NN-....html#nota-N';
  ['backTop','backBottom'].forEach(function(id){ var a=document.getElementById(id); if(a) a.setAttribute('href', ret); });
})();
</script>
</body>
</html>
```

## Callout da inserire nel capitolo
Va messo nel punto desiderato del capitolo. Porta l'`id` usato come àncora di ritorno,
e passa quello stesso punto alla nota tramite `?ret=`:
```html
<div class="nota-link" id="nota-N">
<span class="k">Nota NN</span>
<span class="it">Breve invito sobrio. <a href="nota-NN-slug.html?ret=NN-....html%23nota-N">Leggi →</a></span><span class="en">Short, understated teaser. <a href="nota-NN-slug.html?ret=NN-....html%23nota-N">Read →</a></span>
</div>
```
Per linkare la **stessa** nota da un altro punto: usa un nuovo `id` (es. `nota-N-bis`) e
cambia solo il valore di `?ret=` — la nota tornerà automaticamente lì.

## Elementi di stile (per eventuali ritocchi)
- Sfondo pagina: griglia 24px (`--n-grid`).
- Foglio: `.sheet` con barra accento a sinistra (`::before`) e cornice tratteggiata (`::after`).
- Font: metadati/sezioni/pulsanti in **monospace** (`--n-mono`); corpo in **serif** (`--n-serif`).
- Colori: `--n-accent` mattone (#7b2d26), `--n-amber` ambra (#b06a12), `--n-blue` blueprint (#1a5276).
- Le variabili sono in cima a `note.css`.
