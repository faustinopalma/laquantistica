# Canovaccio dei Laboratori Virtuali — *La Quantistica*

Mappa di tutti i possibili **lab virtuali** (simulatori interattivi) ricavabili dai 9 capitoli
della tesi. È un documento **di lavoro**: modificalo liberamente per dare indicazioni sulla
costruzione. Lo useremo come traccia per implementare i lab **uno alla volta**.

## Come usare questo documento
- Ogni lab ha un blocco con: **concetto**, **cosa fa l'utente**, **fisica mostrata**, **figure
  di riferimento**, **priorità/complessità**, **stato** e un campo **Indicazioni** da compilare tu.
- Scrivi le tue note nel campo `> Indicazioni:` di ciascun lab (cosa mostrare, cosa NON mostrare,
  controlli desiderati, testi, ecc.).
- Cambia **Priorità** e **Stato** per dirmi da quale partire.
- Quando un lab è pronto per l'implementazione, lo prendo e lo costruisco seguendo le tue indicazioni.

## Legenda
- **Stato:** ✅ fatto · 🔨 in corso · 💡 proposto · ⏸️ in attesa di indicazioni · ❌ scartato
- **Priorità:** 🔴 alta · 🟡 media · ⚪ bassa
- **Complessità:** ★ semplice · ★★ media · ★★★ impegnativa

## Convenzioni tecniche condivise (per tutti i lab)
- Pagine **separate** `publish/sim-*.html`, stile «laboratorio di elettronica / oscilloscopio»
  (indipendente dallo stile accademico del sito).
- Riuso del **nucleo condiviso** `publish/assets/sim-sg-core.js` + `publish/assets/sim-sg.css`
  (helper SVG, macchine, gauge a lancetta, registratore/plotter, ecc.). Se servono nuovi helper
  (es. traiettorie, istogrammi) si aggiungono al core e si riusano.
- **Bilingue** it/en (`<span class="it">` / `<span class="en">`, `assets/lang.js`).
- Layout tipo Cap.2: **diagramma SVG a sinistra** (a tutta altezza) + **pannello strumenti a destra**
  (slider, letture, formule, registratore).
- **Link** «Prova il simulatore» a valle della spiegazione teorica nel capitolo corrispondente
  (come già fatto nel Cap.2).
- **Deploy:** push su `main` → Azure Static Web Apps. Verifica con Playwright (attenzione: timer/rAF
  throttlati in headless → controllare lo stato via DOM, non solo screenshot).

---

## Cap. 1 — Esperimento di Stern-Gerlach
Un atomo si comporta come una piccola calamita; in un campo **disuniforme** il fascio si separa in
**due** macchie discrete (quantizzazione della proiezione del momento magnetico), non in una banda continua.

### [L1.1] Stern-Gerlach singolo 💡
- **Concetto:** quantizzazione — il fascio si divide in due sole macchie.
- **Cosa fa l'utente:** accende/spegne il gradiente di campo, regola l'intensità del fascio e
  (opzionale) l'orientazione della macchina; osserva le due macchie sul vetrino.
- **Fisica mostrata:** previsione classica (banda continua) vs risultato reale (due punti);
  è il *prequel* naturale del Cap.2.
- **Figure di riferimento:** Fig. 1–4 (atomo-calamita, traferro sagomato, percorso del fascio).
- **Priorità / Complessità:** 🔴 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 2 — Stern-Gerlach in cascata  ✅ (serie completa)
Introduzione a stati, sovrapposizione, ampiezze e interferenza tramite macchine SG in cascata.

### [L2.1] Esperimento 1 — due macchine, angolo relativo ✅
- **Concetto:** conta solo l'angolo *relativo*; probabilità cos²/sin²(ϑ/2). → `sim-esp1.html`

### [L2.2] Esperimento 2 — tre macchine ✅
- **Concetto:** lo stato dopo la 2ª macchina è indipendente dall'orientazione della 1ª. → `sim-esp2.html`

### [L2.3] Esperimento 3 — scomposizione e ricombinazione ✅
- **Concetto:** ricombinando i rami le probabilità **non si sommano** (0,5+0,5=0). → `sim-esp3.html`

### [L2.4] Esperimento 4 — sfasamento φ ✅
- **Concetto:** un cammino più lungo introduce uno sfasamento; P(m₀=−k)=sin²(φ/2); curva d'interferenza. → `sim-esp4.html`

### [L2.5] Ampiezze come fasori 💡
- **Concetto:** somma di ampiezze nel piano complesso (1 + e^{iφ}) → modulo quadro = probabilità.
- **Cosa fa l'utente:** ruota il fasore e^{iφ}, vede la somma vettoriale e |1+e^{iφ}|² = 4cos²(φ/2).
- **Fisica mostrata:** perché si sommano le **ampiezze** e non le probabilità (chiude il discorso Esp.3/4).
- **Figure di riferimento:** derivazione con i numeri complessi (dopo Fig. 11).
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 3 — Esperimenti con gli Elettroni
Deflessione di fasci di elettroni con campi E e B (rapporto e/m) e quantizzazione della **carica** (Millikan).

### [L3.1] Rapporto e/m (deflessione del fascio) 💡
- **Concetto:** un fascio di elettroni deflesso da campo elettrico e/o magnetico permette di ricavare e/m.
- **Cosa fa l'utente:** regola la tensione acceleratrice, la tensione deflettrice (E) e il campo B;
  osserva lo spostamento della macchia sullo schermo ai fosfori.
- **Fisica mostrata:** parabola nel campo E, arco di cerchio nel campo B; misura di e/m; segno della carica.
- **Figure di riferimento:** Fig. 3 (cannone), 4 (schermo), 5 (deflessione E), 6 (deflessione B), 7–9 (ioni/elettroni).
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.2] Goccia di Millikan (quantizzazione della carica) 💡
- **Concetto:** la carica è un multiplo intero di *e*.
- **Cosa fa l'utente:** regola la tensione tra le piastre per **sospendere** una gocciolina (peso = forza elettrica);
  ripete su molte gocce e costruisce l'istogramma delle cariche → gradini multipli di *e*.
- **Fisica mostrata:** equilibrio mg = qE, legge di Stokes (caduta), quantizzazione di *e*.
- **Figure di riferimento:** Fig. 13 (nebulizzatore), 14 (condensatore/goccioline), 17 (piastre con V).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 4 — Diffrazione degli Elettroni
Elettroni attraverso grafite → **anelli** di diffrazione: gli elettroni si comportano come onde (de Broglie).

### [L4.1] Diffrazione elettronica su grafite 💡
- **Concetto:** dualismo onda-particella; λ = h/p; gli anelli si restringono all'aumentare della tensione.
- **Cosa fa l'utente:** regola la tensione acceleratrice V; osserva i due anelli concentrici (d₁, d₂)
  cambiare raggio; (opzionale) confronto con la previsione classica (macchia a campana).
- **Fisica mostrata:** λ = h/√(2meV), condizione di diffrazione, raggio ∝ 1/√V; reticolo → sottoreticoli a righe.
- **Figure di riferimento:** Fig. 1 (schema), 4 (previsione classica), 11–12 (anelli), 14–18 (reticolo grafite).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 5 — Esperimento di Rutherford
Particelle α su lamina d'oro: la maggior parte passa, poche deviano molto → **nucleo** piccolo e massiccio.

### [L5.1] Diffusione di Rutherford 💡
- **Concetto:** scattering coulombiano; N(ϑ) ∝ 1/sin⁴(ϑ/2).
- **Cosa fa l'utente:** «spara» particelle α (traiettorie iperboliche al variare del parametro d'urto/energia);
  ruota il rivelatore all'angolo ϑ e conta gli impulsi; costruisce N(ϑ) e lo confronta con la formula.
- **Fisica mostrata:** traiettoria iperbolica, parametro d'urto, legge di Rutherford, «trasparenza» della lamina.
- **Figure di riferimento:** Fig. 2 (apparato), 12 (N/Δt vs ϑ), 13–14 (interpretazione), 15 (geometria), 18–22 (confronto).
- **Priorità / Complessità:** 🔴 · ★★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 6 — Ulteriori sviluppi della Teoria
Capitolo prevalentemente **teorico** (principi, ampiezze per la quantità di moto, grandezze
compatibili/incompatibili, momento angolare, energia, livelli dell'idrogeno). Lab possibili più «concettuali».

### [L6.1] Compatibili / incompatibili e indeterminazione 💡
- **Concetto:** grandezze incompatibili (posizione/quantità di moto) — coppia di Fourier.
- **Cosa fa l'utente:** stringe/allarga il pacchetto in posizione e vede allargarsi/stringersi quello in quantità di moto (Δx·Δp).
- **Fisica mostrata:** ampiezze di probabilità per x e per p, principio di indeterminazione.
- **Figure di riferimento:** §«Ampiezze di probabilità per la quantità di moto», §«Grandezze compatibili e incompatibili».
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L6.2] Livelli energetici dell'idrogeno 💡
- **Concetto:** Eₙ = −13,6 eV / n²; struttura dei livelli (base per Cap.9).
- **Cosa fa l'utente:** esplora i livelli, seleziona n, legge l'energia; ponte verso gli spettri (Cap.9).
- **Fisica mostrata:** quantizzazione dell'energia, spaziatura dei livelli.
- **Figure di riferimento:** §«Livelli energetici per l'atomo di idrogeno».
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L6.3] Momento angolare quantizzato 💡
- **Concetto:** proiezioni discrete del momento angolare.
- **Cosa fa l'utente:** sceglie ℓ e vede i possibili valori di m (proiezioni) sul cono/sfera.
- **Fisica mostrata:** quantizzazione di Lz.
- **Figure di riferimento:** §«Momento angolare».
- **Priorità / Complessità:** ⚪ · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 7 — Esperimento di Franck-Hertz
Corrente vs tensione acceleratrice con **massimi e minimi periodici**: prova diretta dei livelli energetici discreti.

### [L7.1] Franck-Hertz (I–V) 💡
- **Concetto:** urti anelastici a energia di soglia → dentellature periodiche nella curva I(V).
- **Cosa fa l'utente:** aumenta la tensione acceleratrice e traccia la curva I(V); vede comparire le
  «zone luminose» tra le griglie; sceglie **neon** o **mercurio** (cambia la spaziatura dei picchi).
- **Fisica mostrata:** energia di eccitazione ΔE = e·ΔV (distanza tra i picchi), quantizzazione dei livelli.
- **Figure di riferimento:** Fig. 1–2 (ampolla/elettrodi), 6 (curva I–V), 7 (zone luminose), 10 (mercurio, sei massimi).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 8 — Effetto Fotoelettrico
La luce estrae elettroni; l'energia degli elettroni dipende dalla **frequenza**, non dall'intensità → fotoni.

### [L8.1] Effetto fotoelettrico 💡
- **Concetto:** E = hν − W; tensione d'arresto vs frequenza; l'intensità cambia la corrente, non l'energia.
- **Cosa fa l'utente:** sceglie il **filtro** (colore/frequenza) e l'intensità; misura la **tensione d'arresto**;
  costruisce il grafico V_arresto vs ν → pendenza = h/e, intercetta = lavoro di estrazione W.
- **Fisica mostrata:** quantizzazione della luce (fotoni), costante di Planck, soglia di frequenza.
- **Figure di riferimento:** Fig. 1 (estrazione), 2 (catodo/anodo/I), 3 (misura energia), 7–9 (filtri).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 9 — Spettri Atomici
Le righe spettrali corrispondono ai **salti** tra livelli energetici (E_i − E_f = hν); serie di Balmer per l'idrogeno.

### [L9.1] Spettri atomici e righe di Balmer 💡
- **Concetto:** ogni transizione tra livelli emette una riga di frequenza/colore precisi.
- **Cosa fa l'utente:** clic su una transizione nel diagramma dei livelli dell'idrogeno → vede comparire la
  **riga** corrispondente (colore/λ) sullo «schermo» dietro il reticolo; (opzionale) sceglie il gas.
- **Fisica mostrata:** E_i − E_f = hν, serie di Balmer, relazione livelli ↔ righe osservate.
- **Figure di riferimento:** Fig. 2 (livelli), 3 (salti), 7 (righe sullo schermo), 12 (lampada di Balmer).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Roadmap suggerita (modificabile)
Ordine proposto per l'implementazione (puoi riordinare):
1. **[L1.1] Stern-Gerlach singolo** — completa la coppia con il Cap.2, riuso quasi totale del core.
2. **[L7.1] Franck-Hertz** — curva I(V), riuso del registratore/oscilloscopio già pronto.
3. **[L8.1] Effetto fotoelettrico** — grafico V_arresto vs ν, riuso plotter.
4. **[L4.1] Diffrazione elettronica** — anelli che si restringono con V (molto visivo).
5. **[L9.1] Spettri atomici** — righe da transizioni (si lega a L6.2).
6. **[L3.2] Millikan** — istogramma della carica.
7. **[L5.1] Rutherford** — traiettorie + conteggi (il più impegnativo).
8. **[L3.1] e/m**, **[L2.5] fasori**, **[L6.x] teorici** — a seguire.

> Note generali / vincoli (da compilare da parte tua):
> _..._
