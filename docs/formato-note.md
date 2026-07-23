# Formato "Scheda Tecnica" per le Note

Formato editoriale, stile **industriale / ingegneristico**, usato per le note a lato
della tesi (onestà intellettuale, dietro le quinte, aneddoti storici, ecc.).
È volutamente diverso dalle pagine dei capitoli, così le note si distinguono a colpo d'occhio.

> Nota di lavoro: questo formato è una prima scelta grafica e potrà essere ritoccato.
> Tutte le note condividono lo stesso CSS, quindi una modifica di stile si propaga a tutte.

## File coinvolti
- `publish/assets/note.css` — stile completo della scheda (griglia tecnica di sfondo,
  foglio con cornice tratteggiata, barra metadati monospace, sezioni con prefisso `//`,
  pulsante di ritorno, footer tecnico). Riusabile da tutte le note.
- `publish/assets/style.css` — contiene la classe `.nota-link`, il **callout** che si
  inserisce nel corpo di un capitolo per rimandare a una nota.

## Convenzioni
- **Nome file nota**: `nota-NN-slug.html` (es. `nota-01-stern-gerlach.html`), nella
  cartella `publish/` (stessa dei capitoli, così i path `assets/...` restano relativi).
- **Lingua**: le note sono in italiano (pagina `<html lang="it">`, senza toggle IT/EN).
  Il *callout* nel capitolo invece usa gli span `.it`/`.en` per adattarsi alla lingua scelta.
- **Ritorno al punto di partenza**: nel capitolo il callout ha `id="nota-N"`; la nota
  rimanda indietro con `href="NN-....html#nota-N"` (àncora → torna esattamente al callout).
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
  <link rel="stylesheet" href="assets/note.css?v=1">
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">
    <div class="doc-meta">
      <span class="tag">Nota NN</span>
      <span>Cap. NN · Titolo capitolo</span>
      <span class="sep">|</span>
      <span class="tag amber">Etichetta tematica</span>
      <a class="doc-back-top" href="NN-....html#nota-N">← Cap. N</a>
    </div>
    <h1 class="doc-title"><span class="lead">Occhiello</span>Titolo della nota</h1>
    <p class="lede">Primo paragrafo (leggermente più grande).</p>
    <p>Paragrafi… usa <strong>grassetto</strong> (accento) ed <em>corsivo</em>.</p>
    <h2>Sezione</h2>   <!-- il prefisso "// " è aggiunto dal CSS -->
    <p>…</p>
    <div class="doc-return">
      <a href="NN-....html#nota-N">← Torna al Capitolo N: Titolo</a>
    </div>
    <div class="doc-foot">
      <span>La Quantistica · Nota tecnica N.NN · Rev. 2026</span>
      <span>F. Palma</span>
    </div>
  </div>
</main>
</body>
</html>
```

## Callout da inserire nel capitolo
Va messo nel punto desiderato del capitolo (tipicamente dopo un paragrafo). Porta l'`id`
usato dalla nota per il ritorno:
```html
<div class="nota-link" id="nota-N">
<span class="k">Nota NN</span>
<span class="it">Testo invito in italiano. <a href="nota-NN-slug.html">Leggi la nota →</a></span><span class="en">Invitation text in English. <a href="nota-NN-slug.html">Read the note → (in Italian)</a></span>
</div>
```

## Elementi di stile (per eventuali ritocchi)
- Sfondo pagina: griglia 24px (`--n-grid`).
- Foglio: `.sheet` con barra accento a sinistra (`::before`) e cornice tratteggiata (`::after`).
- Font: metadati/sezioni/pulsanti in **monospace** (`--n-mono`); corpo in **serif** (`--n-serif`).
- Colori: `--n-accent` mattone (#7b2d26), `--n-amber` ambra (#b06a12), `--n-blue` blueprint (#1a5276).
- Le variabili sono in cima a `note.css`.
