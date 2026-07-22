# Revisione delle schede dalla scansione cartacea (1999)

**Fonte di verità:** `scansioni/NN-*.pdf` — la tesi cartacea stampata del 1999.

**Regole di lavoro (nessuna scorciatoia):**
- Ogni scheda si controlla **una pagina alla volta**, confrontando la scansione con l'HTML.
- **Correzioni strutturali** (posizione/numerazione figure, figure mancanti, formule sbagliate,
  refusi OCR che non corrispondono al cartaceo) → applicate **sia** all'originale digitale
  (`site/mathml/`, e `site/svg/` dove presente lo stesso errore) **sia** a `publish/leggi/`,
  perché servono a rendere il digitale fedele al cartaceo.
- **Correzioni editoriali** (editing "livello B" di lingua, struttura bilingue IT/EN, note) →
  **SOLO** in `publish/leggi/` (differiscono volutamente dall'originale del 1999).
- Si controlla tutto: testo, posizionamento immagini, didascalie, formule, numerazione.

**Legenda:** `[ ]` da fare · `[~]` in corso · `[x]` fatto

---

## 00 — Introduzione — 5 pagine — `leggi/index.html`
- [ ] Scansione letta pagina per pagina (1→5)
- [ ] Originale (`site/mathml/index.html`, `site/svg/index.html`) verificato/corretto
- [ ] Publish (`publish/leggi/index.html`) verificato/corretto
- **Errori trovati / correzioni:** _(da compilare)_

## 01 — Esperimento di Stern-Gerlach — 9 pagine — `01-stern-gerlach.html`
- [~] Scansione letta pagina per pagina (1→9) — lette 1,2,3,4,5
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto (già bilingue)
- **Osservazioni dalla scansione:**
  - p1 = copertina «PRIMA SCHEDA»; p2 e p3 = STESSA pagina stampata «2» (doppia scansione, nessun contenuto perso).
  - Testo **fedele** al cartaceo: nel cartaceo c'è davvero «al di la» (senza accento), «(fig.1). se la calamita»,
    «accelera, dipende», «operazioni che descrivono l'esperienza». → le mie correzioni in publish sono **editoriali**
    (restano solo in publish; l'originale site/ resta fedele).
  - Sul cartaceo (pag. stampata 2) compaiono **Fig.1, Fig.2, Fig.3, Fig.4** come piccoli disegni a destra del testo.
    Nell'HTML sono immagini inline senza numero/didascalia (solo Fig.4 ha didascalia). → **DA SISTEMARE** numerazione/didascalie.
  - p5 = pag. stampata «3» = disegno tecnico completo (camera vaporizzazione + «Tubo in quarzo» + fenditura).
    Nell'HTML c'è solo il frammento image5.svg (tubo stretto). **Il disegno completo dell'apparato MANCA.**
  - Pagine stampate 4,5,6 (scan p6,p7,p8) = altri disegni tecnici a piena pagina — verosimilmente **assenti dal web**.
- **DECISIONE NECESSARIA (apparato):** come rendere i disegni tecnici a piena pagina mancanti?
  - A) lasciare il web con le sole figure fisiche (Fig.1–4), senza i disegni CAD dell'apparato;
  - B) **[consigliata]** inserire le pagine scansionate dell'apparato come immagini (fedele al cartaceo).
- **RISOLTO:** i DWG originali convertiti in SVG vettoriale (diagrammi-dwg/01/). Mappatura VERIFICATA con la scansione:
  - Figure fisiche (pag. stampata 2): **Fig.1 = FIG2** (calamita nel campo) · **Fig.2 = FIG1** (circuito magnetico) ·
    **Fig.3 = FIG3** (traferro sagomato + fascio) · **Fig.4 = FIG4** (fornetto→fenditure→vetrino).
  - Apparato: **pag.3 = PROGET~2** (camera vaporizz.+tubo quarzo+1ª fenditura) · **pag.4 = PROGETTO** (espansioni polari+2ª fenditura+vetrino, 600mm) ·
    **pag.5 = PROGET~1** (circuito magnetico completo, acciaio inox, spire) · **pag.6 = FIG5** (assemblaggio verticale completo) · **SEZIONE** = sezione polo (dettaglio).
  - NB: i nomi file DWG NON coincidono coi numeri figura (FIG1↔Fig.2, FIG2↔Fig.1 scambiati).
- **FATTO (figure Cap.1):** inseriti gli 8 SVG DWG (fig1–4 + app3–6) in TUTTE e 3 le edizioni
  (publish/leggi/01, site/mathml/01, site/svg/01) come figure numerate con didascalia bilingue (publish)/IT (site) e link hover;
  rimossi i vecchi image1–5.svg. Verificato: 8 figure, SVG caricati (fig1.svg 633×412px), 0 riferimenti residui.
  SVG sorgenti copiati in img/pandoc_ch1/ di ciascuna edizione.

## 02 — Esperimenti di Stern-Gerlach in cascata — 17 pagine — `02-stern-gerlach-cascata.html`
- [ ] Scansione letta pagina per pagina (1→17)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(figure orfane note: Fig.1/2/4/5 da collocare)_

## 03 — Esperimenti con gli Elettroni — 10 pagine — `03-elettroni.html`
- [ ] Scansione letta pagina per pagina (1→10)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(da compilare)_

## 04 — Diffrazione degli Elettroni — 20 pagine — `04-diffrazione.html`
- [ ] Scansione letta pagina per pagina (1→20)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(contiene la deduzione di Schrödinger)_

## 05 — Esperimento di Rutherford — 21 pagine — `05-rutherford.html`
- [ ] Scansione letta pagina per pagina (1→21)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(da compilare)_

## 06 — Ulteriori sviluppi della Teoria — 11 pagine — `06-ulteriori-sviluppi.html`
- [ ] Scansione letta pagina per pagina (1→11)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(teoria, poche/nessuna figura)_

## 07 — Esperimento di Franck-Hertz — 5 pagine — `07-franck-hertz.html`
- [ ] Scansione letta pagina per pagina (1→5)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto (già bilingue)
- **Errori trovati / correzioni:** _(sospetto "decima scheda" → "nona scheda" da verificare sul cartaceo)_

## 08 — Effetto Fotoelettrico — 7 pagine — `08-effetto-fotoelettrico.html`
- [ ] Scansione letta pagina per pagina (1→7)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto
- **Errori trovati / correzioni:** _(da compilare)_

## 09 — Spettri atomici di emissione — 6 pagine — `09-spettri-atomici.html`
- [ ] Scansione letta pagina per pagina (1→6)
- [ ] Originale verificato/corretto
- [ ] Publish verificato/corretto (già bilingue)
- **Errori trovati / correzioni:** _(da compilare)_
