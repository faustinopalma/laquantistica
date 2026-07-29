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

## Sintesi della seconda lettura — uno o più lab per capitolo?
Rileggendo il corpo dei capitoli, **non sempre basta un solo lab**. In sintesi:
- **Un solo lab (o lab teorici):** Cap.1 (con un'opzione preparatoria), Cap.6 (concettuali), Cap.7, Cap.9.
- **Conviene una catena di lab intermedi:**
  - **Cap.3** — nel testo è già una *sequenza*: corrente nel vuoto → cannone elettronico → deflessione E
    → deflessione B (e/m) → separazione ioni/elettroni → Millikan.
  - **Cap.4** — previsione classica (campana) → anelli + de Broglie → *perché* si formano gli anelli (reticolo).
  - **Cap.5** — conteggio N(ϑ) → contrasto «sfera piena vs nucleo» → confronto con la formula 1/sin⁴.
  - **Cap.8** — caratteristica I–V / tensione d'arresto → tensione d'arresto vs frequenza (h, W).
Gli step intermedi possono diventare **piccoli lab separati** oppure **stadi (tab) di un unico banco**:
lo decidi tu nelle Indicazioni.

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

### [L1.0] (preparatorio) Forza su una calamita: campo uniforme vs disuniforme 💡
- **Concetto:** in un campo **uniforme** il dipolo sente solo una coppia (nessuna traslazione); serve un campo
  **disuniforme** (gradiente) per avere una forza netta, e quindi la deflessione.
- **Cosa fa l'utente:** commuta tra campo uniforme/disuniforme e orienta la calamita; vede la forza risultante.
- **Fisica mostrata:** F = ∇(μ·B); perché il traferro è sagomato.
- **Figure di riferimento:** Fig. 1–2 (atomo-calamita, traferro).
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto (opzionale, apre il Cap.1)
- > Indicazioni: _(da compilare)_

### [L1.1] Stern-Gerlach singolo — le due macchie 💡
- **Concetto:** quantizzazione — il fascio si divide in due sole macchie.
- **Cosa fa l'utente:** accende/spegne il gradiente, regola l'intensità del fascio e (opzionale)
  l'orientazione della macchina; osserva le due macchie sul vetrino.
- **Fisica mostrata:** previsione classica (banda continua) vs risultato reale (due punti);
  è il *prequel* naturale del Cap.2.
- **Figure di riferimento:** Fig. 1–4.
- **Priorità / Complessità:** 🔴 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 2 — Stern-Gerlach in cascata  ✅ (serie completa)
Introduzione a stati, sovrapposizione, ampiezze e interferenza tramite macchine SG in cascata.

### [L2.1] Esperimento 1 — due macchine, angolo relativo ✅
- **Concetto:** conta solo l'angolo *relativo*; probabilità cos²/sin²(ϑ/2). → `lab-02a-sg-angolo-relativo.html`

### [L2.2] Esperimento 2 — tre macchine ✅
- **Concetto:** lo stato dopo la 2ª macchina è indipendente dall'orientazione della 1ª. → `lab-02b-sg-tre-macchine.html`

### [L2.3] Esperimento 3 — scomposizione e ricombinazione ✅
- **Concetto:** ricombinando i rami le probabilità **non si sommano** (0,5+0,5=0). → `lab-02c-sg-ricombinazione.html`

### [L2.4] Esperimento 4 — sfasamento φ ✅
- **Concetto:** un cammino più lungo introduce uno sfasamento; P(m₀=−k)=sin²(φ/2); curva d'interferenza. → `lab-02d-sg-sfasamento.html`

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
Il capitolo è una **catena di esperimenti**: si isola l'elettrone e se ne studiano le proprietà. Ogni tappa
può diventare un piccolo lab a sé, oppure uno **stadio** di un unico «banco elettroni».

### [L3.1] Corrente nel vuoto (emissione termoionica) 💡
- **Concetto:** tra due elettrodi nel vuoto passa corrente → esistono particelle cariche emesse dal filamento caldo.
- **Cosa fa l'utente:** applica la tensione A–B e scalda il filamento; vede l'amperometro salire col riscaldamento.
- **Fisica mostrata:** emissione termoionica; aumento di corrente con la temperatura.
- **Figure di riferimento:** Fig. 1–2.
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.2] Cannone elettronico + schermo ai fosfori 💡
- **Concetto:** si forma un fascio focalizzato di cariche negative; invertendo la polarità **non** esce nulla
  (il filamento emette solo cariche negative).
- **Cosa fa l'utente:** regola le tensioni (flusso ~10 V, accelerazione ~5000 V, lenti ~100 V), vede il fascio
  focalizzarsi sullo schermo; prova a invertire la polarità (nessun fascio).
- **Fisica mostrata:** accelerazione, lenti elettrostatiche, segno della carica emessa.
- **Figure di riferimento:** Fig. 3–4.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.3] Deflessione con campo elettrico 💡
- **Concetto:** il fascio devia nel campo E → conferma che è fatto di cariche negative.
- **Cosa fa l'utente:** alimenta le piastre e osserva la deflessione (parabolica) della macchia.
- **Fisica mostrata:** moto di una carica in campo E uniforme; verso della deflessione.
- **Figure di riferimento:** Fig. 5.
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.4] Deflessione con campo magnetico (e/m) 💡
- **Concetto:** nel campo B il fascio percorre un arco; combinando E e B si ricava e/m.
- **Cosa fa l'utente:** regola la corrente nelle bobine (B) ed eventualmente E; misura la deflessione → e/m.
- **Fisica mostrata:** forza di Lorentz, raggio di curvatura, misura del rapporto carica/massa.
- **Figure di riferimento:** Fig. 6.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.5] Separazione in ioni ed elettroni (segno e massa) 💡
- **Concetto:** un atomo può essere separato in ioni (positivi, pesanti) ed elettroni (negativi, leggeri):
  le deflessioni hanno verso opposto e ampiezza molto diversa.
- **Cosa fa l'utente:** attiva la separazione e osserva i due punti sugli schermi e le rispettive deflessioni.
- **Fisica mostrata:** rapporto e/m molto diverso per ioni ed elettroni; segno delle cariche.
- **Figure di riferimento:** Fig. 7–10.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L3.6] Goccia di Millikan (quantizzazione della carica) 💡
- **Concetto:** la carica è un multiplo intero di *e*.
- **Cosa fa l'utente:** regola la tensione tra le piastre per **sospendere** una gocciolina (peso = forza elettrica);
  ripete su molte gocce e costruisce l'istogramma delle cariche → gradini multipli di *e*.
- **Fisica mostrata:** equilibrio mg = qE, legge di Stokes (caduta), quantizzazione di *e*.
- **Figure di riferimento:** Fig. 13–17.
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 4 — Diffrazione degli Elettroni
Tre momenti distinti: la **previsione classica**, il **risultato** (anelli / de Broglie) e il **perché**
si formano gli anelli. Possibili 2–3 lab (o stadi di uno solo).

### [L4.1] Previsione classica (macchia a campana) 💡
- **Concetto:** se gli elettroni fossero palline, urtando i nuclei darebbero una distribuzione a campana.
- **Cosa fa l'utente:** «spara» elettroni classici sul reticolo e vede accumularsi una macchia diffusa (gaussiana).
- **Fisica mostrata:** previsione classica da confrontare col risultato reale.
- **Figure di riferimento:** Fig. 2–4.
- **Priorità / Complessità:** ⚪ · ★
- **Stato:** 💡 proposto (contrasto, apre il capitolo)
- > Indicazioni: _(da compilare)_

### [L4.2] Anelli di diffrazione + de Broglie 💡
- **Concetto:** si ottengono **anelli** concentrici; λ = h/p, il raggio ∝ 1/√V.
- **Cosa fa l'utente:** regola la tensione acceleratrice V e vede i due anelli (d₁, d₂) restringersi/allargarsi.
- **Fisica mostrata:** λ = h/√(2meV), condizione di diffrazione, dualismo onda-particella.
- **Figure di riferimento:** Fig. 1, 11–13.
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto (lab principale)
- > Indicazioni: _(da compilare)_

### [L4.3] Perché gli anelli: reticolo → sottoreticoli → cerchi 💡
- **Concetto:** il reticolo si scompone in sottoreticoli a righe parallele (d₁, d₂); un singolo cristallo dà
  punti, tanti cristalli orientati a caso danno i cerchi.
- **Cosa fa l'utente:** mostra la scomposizione del reticolo e la sovrapposizione di cristalli → formazione degli anelli.
- **Fisica mostrata:** relazione reticolo ↔ figura di diffrazione.
- **Figure di riferimento:** Fig. 14–18.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Cap. 5 — Esperimento di Rutherford
Un lab principale (conteggi) con due tappe di **interpretazione** che possono essere stadi separati.

### [L5.1] Diffusione: traiettorie e conteggio N(ϑ) 💡
- **Concetto:** scattering coulombiano; poche particelle deviano molto.
- **Cosa fa l'utente:** «spara» particelle α (traiettorie iperboliche al variare di parametro d'urto/energia);
  ruota il rivelatore all'angolo ϑ e conta gli impulsi → costruisce N(ϑ).
- **Fisica mostrata:** traiettoria iperbolica, parametro d'urto, rate di conteggio vs angolo.
- **Figure di riferimento:** Fig. 2, 12, 15.
- **Priorità / Complessità:** 🔴 · ★★★
- **Stato:** 💡 proposto (lab principale)
- > Indicazioni: _(da compilare)_

### [L5.2] Sfera piena vs nucleo puntiforme (trasparenza) 💡
- **Concetto:** se gli atomi fossero sferette piene la lamina sarebbe «opaca»; con nuclei minuscoli è quasi trasparente.
- **Cosa fa l'utente:** commuta tra i due modelli e osserva quante particelle passano/deviano.
- **Fisica mostrata:** dimensione del nucleo, «vuoto» dell'atomo.
- **Figure di riferimento:** Fig. 13–14.
- **Priorità / Complessità:** 🟡 · ★
- **Stato:** 💡 proposto (contrasto, può essere uno stadio di L5.1)
- > Indicazioni: _(da compilare)_

### [L5.3] Confronto con la formula di Rutherford 💡
- **Concetto:** N(ϑ) ∝ 1/sin⁴(ϑ/2).
- **Cosa fa l'utente:** sovrappone i conteggi misurati alla curva teorica (scala lineare/logaritmica).
- **Fisica mostrata:** legge di Rutherford, accordo teoria/esperienza.
- **Figure di riferimento:** Fig. 18–22.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto (può essere il pannello destro di L5.1)
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
- **Cosa fa l'utente:** aumenta la tensione acceleratrice e traccia la curva I(V); sceglie **neon** o **mercurio**
  (cambia la spaziatura dei picchi).
- **Fisica mostrata:** energia di eccitazione ΔE = e·ΔV (distanza tra i picchi), quantizzazione dei livelli.
- **Figure di riferimento:** Fig. 1–2 (ampolla/elettrodi), 6 (curva I–V), 10 (mercurio, sei massimi).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto (lab principale)
- > Indicazioni: _(da compilare)_

### [L7.2] (vista secondaria) Zone luminose tra le griglie 💡
- **Concetto:** le zone in cui gli elettroni raggiungono l'energia di soglia si illuminano; il loro numero
  aumenta con la tensione, in sincrono coi picchi della curva I(V).
- **Cosa fa l'utente:** al variare della tensione vede comparire nuove bande luminose nel tubo.
- **Fisica mostrata:** localizzazione spaziale degli urti anelastici (legame diretto coi minimi di I).
- **Figure di riferimento:** Fig. 7 (zone luminose a 70 V).
- **Priorità / Complessità:** ⚪ · ★
- **Stato:** 💡 proposto (può essere un riquadro accanto a L7.1)
- > Indicazioni: _(da compilare)_

---

## Cap. 8 — Effetto Fotoelettrico
Conviene distinguere due momenti: la **misura della tensione d'arresto** per un colore e la **dipendenza
dalla frequenza** (che dà h e il lavoro di estrazione).

### [L8.1] Caratteristica I–V e tensione d'arresto 💡
- **Concetto:** la corrente fotoelettrica si annulla a una tensione d'arresto V₀ che misura l'energia degli elettroni;
  l'**intensità** cambia la corrente ma **non** V₀.
- **Cosa fa l'utente:** sceglie un colore e l'intensità, aumenta la tensione frenante fino ad annullare la corrente (V₀).
- **Fisica mostrata:** E_max = e·V₀; indipendenza di V₀ dall'intensità.
- **Figure di riferimento:** Fig. 2–3.
- **Priorità / Complessità:** 🟡 · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

### [L8.2] Tensione d'arresto vs frequenza (h, W) 💡
- **Concetto:** V₀ cresce linearmente con la frequenza ν; pendenza = h/e, intercetta = lavoro di estrazione W.
- **Cosa fa l'utente:** cambia il **filtro** (frequenza) e registra V₀ per ciascuno → traccia V₀(ν).
- **Fisica mostrata:** E = hν − W, costante di Planck, soglia di frequenza (fotoni).
- **Figure di riferimento:** Fig. 1, 7–9 (filtri).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto (lab principale)
- > Indicazioni: _(da compilare)_

---

## Cap. 9 — Spettri Atomici
Le righe spettrali corrispondono ai **salti** tra livelli energetici (E_i − E_f = hν); serie di Balmer per l'idrogeno.

### [L9.1] Spettri atomici e righe di Balmer 💡
- **Concetto:** ogni transizione tra livelli emette una riga di frequenza/colore precisi.
- **Cosa fa l'utente:** clic su una transizione nel diagramma dei livelli dell'idrogeno → vede comparire la
  **riga** corrispondente (colore/λ) sullo «schermo» dietro il reticolo.
- **Fisica mostrata:** E_i − E_f = hν, serie di Balmer, relazione livelli ↔ righe osservate.
- **Figure di riferimento:** Fig. 2 (livelli), 3 (salti), 7 (righe sullo schermo), 12 (lampada di Balmer).
- **Priorità / Complessità:** 🔴 · ★★
- **Stato:** 💡 proposto (lab principale)
- > Indicazioni: _(da compilare)_

### [L9.2] (opzionale) Confronto tra gas diversi 💡
- **Concetto:** gas diversi (idrogeno, neon, mercurio…) hanno spettri di righe caratteristici («impronta»).
- **Cosa fa l'utente:** seleziona il gas e confronta i pattern di righe.
- **Fisica mostrata:** unicità dello spettro per specie atomica.
- **Figure di riferimento:** Fig. 4 (tubi), 5 (neon), 8–11 (mercurio).
- **Priorità / Complessità:** ⚪ · ★★
- **Stato:** 💡 proposto
- > Indicazioni: _(da compilare)_

---

## Roadmap suggerita (modificabile)
Ordine proposto per l'implementazione (puoi riordinare):
1. **[L1.1] Stern-Gerlach singolo** — completa la coppia con il Cap.2, riuso quasi totale del core.
2. **[L7.1] Franck-Hertz** — curva I(V), riuso del registratore/oscilloscopio già pronto.
3. **[L8.2] Effetto fotoelettrico** (V₀ vs ν) — riuso plotter (preceduto da L8.1).
4. **[L4.2] Diffrazione elettronica** — anelli che si restringono con V (molto visivo).
5. **[L9.1] Spettri atomici** — righe da transizioni (si lega a L6.2).
6. **[L3.x] Banco elettroni** — catena L3.1→L3.5 (piccoli lab o stadi), poi **[L3.6] Millikan**.
7. **[L5.1] Rutherford** — traiettorie + conteggi (il più impegnativo), con L5.2/L5.3 come stadi.
8. **[L2.5] fasori**, **[L6.x] teorici**, viste secondarie (L1.0, L4.1, L4.3, L7.2, L9.2) — a seguire.

> Note generali / vincoli (da compilare da parte tua):
> _..._
