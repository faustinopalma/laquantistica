# -*- coding: utf-8 -*-
"""Reconstructed content for Chapter 3 (Esperimenti con gli Elettroni).
Prose recovered from the OCR-converted document; formulas transcribed from the
original PDF scan (build/pdf_pages). Formulas typeset for MathJax.
"""

def _fig(name, cap):
    return (f'<figure><img loading="lazy" src="img/03_elettroni/{name}" alt="{cap}">'
            f'<figcaption>{cap}</figcaption></figure>')

CH3_BODY = r'''
<p>Ogni oggetto materiale, come sappiamo, è costituito da un aggregato di particelle
elementari; una delle particelle più importanti è l'elettrone perché determina molte
caratteristiche della materia. In questa scheda descriveremo alcuni esperimenti con i
quali è possibile isolare l'elettrone e studiarne le proprietà fondamentali.</p>

<h2>Primo esperimento: conduzione di corrente nel vuoto</h2>
''' + _fig('FIG1.png', 'Fig. 1 — Ampolla di vetro con i due elettrodi A e B.') + r'''
<p>La fig. 1 mostra un'ampolla di vetro nella quale è fatto il vuoto. All'interno
dell'ampolla sono disposti due elettrodi A e B; l'elettrodo A può essere riscaldato
mediante effetto Joule. Se si applica una tensione tra i punti A e B (fig. 2), si osserva
una circolazione di corrente che può essere rilevata con un amperometro inserito in serie
al circuito. Se l'elettrodo A viene riscaldato si osserva che la corrente aumenta
sensibilmente.</p>
''' + _fig('FIG2.png', 'Fig. 2 — Circuito per rilevare la corrente nel vuoto.') + r'''
<p><em>Come è possibile che ci sia conduzione di corrente tra due punti separati nel
vuoto?</em></p>
<p>Il fenomeno si può interpretare pensando che esistano delle particelle cariche che si
possono trasferire nello spazio tra i due elettrodi. Quando viene applicata una differenza
di potenziale, l'elettrodo A emette queste particelle cariche che, trasferendosi all'altro
elettrodo, formano la corrente nel vuoto. Quando l'elettrodo A viene riscaldato, questo
libera un numero maggiore di particelle e quindi permette un maggior flusso di corrente.</p>

<h2>Cannone di particelle cariche (cannone elettronico)</h2>
''' + _fig('FIG3.png', 'Fig. 3 — Schema del cannone elettronico.') + r'''
<p>Il dispositivo rappresentato in figura 3 è un ingegnoso sistema che ci permette di
realizzare un fascio focalizzato di particelle cariche negative.</p>
<p>Consideriamo una particella carica negativa emessa dal filamento caldo A. Nel percorso
A&rarr;B la particella viene rallentata da una differenza di potenziale di circa 10&nbsp;V;
questo stadio serve a regolare il flusso di particelle: più è alta la tensione e meno
particelle passano nello stadio successivo. Nel percorso B&rarr;C le particelle vengono
accelerate notevolmente da una differenza di potenziale dell'ordine di 5000&nbsp;V; questo
stadio serve a dare energia alle particelle del fascio. Nei percorsi C&rarr;D e D&rarr;E le
particelle vengono prima rallentate e poi accelerate da una differenza di potenziale
dell'ordine di 100&nbsp;V. Questi due stadi costituiscono due lenti elettrostatiche, la
prima convergente e la seconda divergente, che permettono di focalizzare il fascio ad una
certa distanza fissata.</p>
<p>In uscita da questo sistema si ottiene un fascio di particelle cariche negative veloci,
ben focalizzato.</p>
<p>È chiaro che un cannone di particelle cariche può essere realizzato in molti modi
diversi, e che può avere una tensione di accelerazione anche molto più alta o più bassa di
5000&nbsp;V; tuttavia lo schema semplice che abbiamo mostrato è sufficiente per gli
esperimenti che descriveremo in questa scheda.</p>
<p>È interessante provare ad alimentare il sistema con tensioni di segno opposto. In linea
di principio dovremmo ottenere un cannone di particelle cariche positive, ma si osserva che
non viene proiettata nessuna particella. Questo si può spiegare pensando che un filamento
riscaldato emette solo particelle cariche negative.</p>

<h2>Schermo ai fosfori</h2>
''' + _fig('FIG4.png', 'Fig. 4 — Schermo ai fosfori.') + r'''
<p>Il fascio di particelle cariche non è direttamente visibile. Per poter rilevare il
fascio si usa uno schermo ai fosfori (fig. 4).</p>
<p>Lo schermo ai fosfori è sostanzialmente una lastra di vetro sulla quale è depositata una
particolare sostanza chimica che, quando viene colpita dalle particelle cariche accelerate,
emette luce visibile, rendendo luminoso il punto di incidenza.</p>
<p>Per ora non ci preoccuperemo di spiegare questo fenomeno di fosforescenza, ma lo useremo
solo come fatto empirico che ci permette di realizzare i nostri esperimenti.</p>

<h2>Deflessione del fascio dovuta a campi elettrici e magnetici</h2>
''' + _fig('FIG5.png', 'Fig. 5 — Apparato per la deflessione mediante campo elettrico.') + r'''
<p>L'apparato di figura 5 è costituito da un cannone elettronico, da una coppia di piastre
che ci permettono di realizzare un campo elettrico uniforme, e da uno schermo ai fosfori.
Il tutto è chiuso in una camera di vetro nella quale è fatto il vuoto. Se si alimentano le
piastre con una differenza di potenziale si osserva una deflessione dovuta al campo
elettrico, esattamente come ci aspettavamo pensando che il fascio fosse formato da un
insieme di particelle cariche negative. Quindi questo esperimento costituisce una conferma
all'ipotesi che un filamento conduttore riscaldato emette particelle cariche negative.</p>
''' + _fig('FIG6.png', 'Fig. 6 — Deflessione del fascio mediante campo magnetico.') + r'''
<p>Nel sistema di figura 6 le due piastre conduttrici sono state sostituite da due bobine.
Facendo attraversare queste bobine da una corrente, si genera un campo magnetico che
provoca una deflessione del fascio. Anche in questo caso la deflessione è esattamente come
ce l'aspettavamo in base all'ipotesi che il fascio è composto da un insieme di particelle
cariche.</p>
<p>Ora calcoliamo gli angoli di deflessione \(\delta_E\) e \(\delta_B\) relativi al campo
elettrico e al campo magnetico, in base all'ipotesi di validità delle leggi di Newton.</p>

<p><strong>Deflessione dovuta al campo elettrico</strong></p>
<div class="equation">\[ \delta_E=\frac{v_y}{v_x}=\frac{a_y\,t}{v_x}
=\frac{\left(\dfrac{qE}{m}\right)\dfrac{l}{v_x}}{v_x}
=\frac{qE\,l}{m\,v_x^{2}}=\frac{E\,l}{v_x^{2}}\cdot\frac{q}{m} \]</div>

<p><strong>Deflessione dovuta al campo magnetico</strong></p>
<div class="equation">\[ \delta_B=\frac{v_y}{v_x}=\frac{a_y\,t}{v_x}
=\frac{\left(\dfrac{q\,v_x B}{m}\right)\dfrac{l}{v_x}}{v_x}
=\frac{q\,B\,l}{m\,v_x}=\frac{B\,l}{v_x}\cdot\frac{q}{m} \]</div>

<p>Come si vede dalle formule, gli angoli di deflessione dipendono direttamente dal rapporto
\(\dfrac{q}{m}\) tra la carica e la massa delle particelle cariche. Se il fascio fosse
composto da diversi tipi di particella, con diversi rapporti \(\dfrac{q}{m}\), allora
avremmo ottenuto diversi angoli di deflessione per le diverse particelle, ed avremmo
osservato più di un punto luminoso sullo schermo ai fosfori. Il fatto che otteniamo un solo
angolo di deflessione è una prova che le particelle emesse dal filamento incandescente hanno
tutte lo stesso rapporto tra carica e massa. È molto ragionevole pensare che in realtà si
tratti di un solo tipo di particella, con una determinata massa ed una determinata carica.
Quest'ipotesi è confermata da molte altre esperienze e le particelle in questione vengono
chiamate <strong>elettroni</strong>.</p>

<h2>Esperimento di Thomson</h2>
<p>Il dispositivo per l'esperimento di Thomson contiene entrambi i sistemi di deflessione:
le piastre per il campo elettrico e le bobine per il campo magnetico.</p>
<p>Lo scopo dell'esperimento è di determinare il rapporto \(\dfrac{q}{m}\) tra la carica e
la massa dell'elettrone, e si esegue in due passi.</p>
<p>Prima si alimentano i due sistemi in opposizione, regolando l'intensità dei campi
elettrico e magnetico in modo da osservare una deflessione nulla. In questo modo si ha un
bilanciamento tra la forza magnetica e la forza elettrica e, dalla relativa relazione di
equilibrio, è possibile ricavare la velocità degli elettroni:</p>
<div class="equation">\[ q\,v_x B=qE \;\Rightarrow\; v_x B=E \;\Rightarrow\; v_x=\frac{E}{B} \]</div>
<p>Poi si misura la deflessione dovuta ad uno solo dei due sistemi e, conoscendo la velocità
\(v_x\), si determina il rapporto \(\dfrac{q}{m}\). Ad esempio, misurando \(\delta_B\):</p>
<div class="equation">\[ \delta_B=\frac{B\,l}{v_x}\cdot\frac{q}{m}
\;\Rightarrow\; \frac{q}{m}=\frac{v_x\,\delta_B}{B\,l} \]</div>
<p>Con questi esperimenti abbiamo individuato un'importante particella con carica negativa,
l'elettrone. Tuttavia non abbiamo ancora osservato nessuna particella positiva: questo
perché un filamento incandescente emette solo elettroni e quindi il cannone elettronico non
può sparare particelle con carica positiva. Noi però sappiamo che la materia è
sostanzialmente neutra, quindi per ogni carica negativa ci deve essere una corrispondente
carica positiva. Nel prossimo esperimento mostreremo che un atomo neutro è formato da un
certo numero di elettroni e da una particella positiva. Le particelle positive ottenute
togliendo uno o più elettroni ad un atomo neutro vengono chiamate <strong>ioni
positivi</strong>.</p>

<h2>Separazione dell'atomo in ioni positivi ed elettroni</h2>
''' + _fig('FIG7.png', 'Fig. 7 — Apparato per la separazione dell\'atomo in ioni ed elettroni.') + r'''
<p>La figura 7 mostra l'apparato sperimentale. Abbiamo un tubo di vetro e, alle estremità
destra e sinistra, due schermi ai fosfori. Nella parte centrale sono disposti due elettrodi
forati. All'interno del tubo è presente un determinato gas a bassa pressione (circa
\(10^{-2}\) atmosfere).</p>
<p>Se alimentiamo i due elettrodi con una tensione di circa 1000&nbsp;V, sui due schermi
appaiono due punti luminosi (fig. 8): a destra otteniamo un fascio di particelle negative,
a sinistra un fascio di particelle positive.</p>
''' + _fig('FIG8.png', 'Fig. 8 — I due punti luminosi sugli schermi.') + r'''
<p>Possiamo inserire dei sistemi di deflessione per studiare il tipo di particelle che
vengono proiettate, misurandone il rapporto \(\dfrac{q}{m}\) tra carica e massa (fig. 9).</p>
''' + _fig('FIG9.png', 'Fig. 9 — Deflessione dei fasci di ioni ed elettroni.') + r'''
<p>Eseguendo queste misure si osserva che le particelle negative non dipendono dal tipo di
gas immesso nell'apparato, e sono le stesse che abbiamo trovato con il cannone elettronico:
quindi sono elettroni. Le particelle positive, invece, dipendono dal tipo di gas. Si osserva
inoltre che le particelle positive subiscono una deflessione molto minore di quella subita
dagli elettroni sotto lo stesso campo elettrico. Questo vuol dire che il rapporto
\(\dfrac{q}{m}\) delle particelle positive è molto minore di quello degli elettroni.</p>
''' + _fig('FIG10.png', 'Fig. 10 — Gli ioni positivi possono generare più punti luminosi.') + r'''
<p>In alcuni casi, come mostra la figura 10, le particelle positive generano due o anche più
punti luminosi. I punti aggiuntivi corrispondono ad un rapporto \(\dfrac{q}{m}\) multiplo di
quello principale: \(2\dfrac{q}{m}\), \(3\dfrac{q}{m}\), ecc.</p>
<p>Questo esperimento può essere interpretato pensando che gli atomi siano formati da una
particella positiva, che chiameremo ione, e da un certo numero di elettroni. La maggior
parte degli atomi sono uniti e formano una struttura neutra. In alcuni casi però ci possono
essere anche atomi divisi e, quando si applica una tensione agli elettrodi, lo ione e gli
elettroni vengono accelerati in direzioni opposte. In questo modo, al di là dei fori
praticati sugli elettrodi, si generano dei fasci di particelle cariche.</p>
<p>Le particelle positive subiscono una deflessione molto inferiore a quella degli
elettroni, quindi, dovendo avere la stessa carica \(q\), vuol dire che hanno una massa \(m\)
molto maggiore. Il rapporto tra la massa dell'elettrone e quella dello ione dipende
dall'atomo considerato ed è dell'ordine di \(1/1000\).</p>
<p>Il fatto che gli ioni possano generare anche più di un punto luminoso si spiega pensando
che uno ione può essere ottenuto anche togliendo più di un elettrone ad un atomo neutro. In
questo modo la carica dello ione diviene multipla di quella dell'elettrone, mentre la massa
rimane praticamente invariata (perché l'elettrone è molto leggero rispetto all'atomo neutro,
quindi la sottrazione di un elettrone non cambia molto la massa); ne risulta un rapporto
\(\dfrac{q}{m}\) multiplo di quello fondamentale ed una deflessione multipla.</p>
<p><em>A questo punto può sorgere una domanda: quanti elettroni si possono togliere da un
atomo neutro?</em></p>
<p>Alcuni esperimenti, che non discuteremo in questa scheda, mostrano che gli atomi sono
formati da un numero finito di elettroni. Questo numero dipende dal tipo di atomo, può
essere solo uno, come nel caso dell'idrogeno, e può arrivare oltre a cento. La particella
positiva che rimane togliendo ad un atomo tutti i suoi elettroni è chiamata
<strong>nucleo</strong>.</p>
<p>Fino ad ora abbiamo misurato i rapporti \(\dfrac{q}{m}\) degli elettroni e degli ioni, ma
non abbiamo ancora misurato la carica \(q\) e la massa \(m\) separatamente. Per concludere
questa scheda descriviamo un esperimento molto ingegnoso ed elegante che ci permette di
misurare la carica \(q\) dell'elettrone.</p>

<h2>Esperimento di Millikan</h2>
<div class="gallery">
''' + _fig('APPARATO.jpg', 'Fig. 11 — Foto dell\'apparecchiatura di Millikan.') + \
     _fig('APPARA~1.jpg', 'Fig. 12 — Microscopio (a sinistra) e lampada (a destra).') + r'''
</div>
<p>Le figure 11 e 12 mostrano due foto dell'apparecchiatura.</p>
''' + _fig('FIG13.png', 'Fig. 13 — Nebulizzatore per l\'olio ad effetto Venturi.') + r'''
<p>Il primo elemento da osservare è il nebulizzatore per l'olio ad effetto Venturi,
rappresentato schematicamente in figura 13. Le goccioline spruzzate dal nebulizzatore
entrano attraverso due forellini tra le piastre conduttrici di un condensatore racchiuso
sotto una camera di plastica trasparente; la figura 14 mostra uno schema del nebulizzatore,
del condensatore e delle goccioline.</p>
''' + _fig('FIG14.png', 'Fig. 14 — Schema del nebulizzatore, del condensatore e delle goccioline.') + r'''
''' + _fig('PIASTRE.jpg', 'Fig. 15 — Foto del condensatore e della camera che lo racchiude.') + r'''
<p>La figura 15 mostra una foto del condensatore e della camera che lo racchiude. Le
goccioline spruzzate all'interno del condensatore sono visibili mediante un microscopio,
rappresentato a sinistra nella figura 12; l'illuminazione della parte interna del
condensatore è ottenuta da una lampada rappresentata a destra nella stessa figura 12. La
foto di figura 16 mostra quello che si vede guardando attraverso il microscopio.</p>
''' + _fig('GOCCIO~1.jpg', 'Fig. 16 — Vista delle goccioline attraverso il microscopio.') + r'''
<p>Osservando le goccioline si vede che queste cadono sotto l'azione del campo gravitazionale
(in realtà si vedono salire perché il microscopio capovolge l'immagine).</p>
''' + _fig('IMG19.jpg', 'Fig. 17 — Le piastre del condensatore alimentate con la tensione V.') + r'''
<p>Se si alimentano le piastre con una certa tensione \(V\) (fig. 17), si osserva che il moto
di alcune goccioline cambia: certe scendono più velocemente, certe scendono meno
velocemente, certe altre iniziano a salire. Questo vuol dire che alcune goccioline portano
una carica elettrica diversa da zero, e quindi subiscono una forza sotto l'azione del campo
elettrico.</p>
<p>Lo scopo dell'esperimento è di misurare la carica di una delle goccioline. Regolando la
tensione \(V\) si può fare in modo che la gocciolina scelta resti ferma in equilibrio. In
questa condizione abbiamo un bilanciamento tra le varie forze: la forza peso, la spinta di
Archimede dovuta all'aria e la forza elettrica:</p>
<div class="equation">\[ -g\,\rho_{Olio}\,\frac{4}{3}\pi R^{3}
+ g\,\rho_{Aria}\,\frac{4}{3}\pi R^{3} + qE = 0 \]</div>
<p>In questa equazione \(g\) è l'accelerazione di gravità, \(\rho_{Olio}\) e \(\rho_{Aria}\)
sono le densità dell'olio e dell'aria, \(R\) è il raggio della gocciolina ed \(E\) è il campo
elettrico presente tra le piastre del condensatore. Queste grandezze sono tutte note,
eccetto il raggio \(R\) della gocciolina; quindi, per derivare la carica \(q\), dobbiamo
trovare il modo di misurare questo raggio. Il metodo escogitato da Millikan è molto
intelligente.</p>
<p>Si spegne il campo elettrico e la gocciolina inizia a cadere. La velocità di caduta della
gocciolina aumenta fino a raggiungere una velocità limite alla quale le forze dovute al peso,
alla spinta di Archimede e all'attrito viscoso con l'aria si bilanciano:</p>
<div class="equation">\[ -g\,\rho_{Olio}\,\frac{4}{3}\pi R^{3}
+ g\,\rho_{Aria}\,\frac{4}{3}\pi R^{3} + 6\pi R\,\eta\,v = 0 \]</div>
<p>In questa equazione abbiamo usato la formula di Stokes per la forza viscosa,
\(F = 6\pi R\,\eta\,v\), dove \(\eta\) è la viscosità dell'aria e \(v\) è la velocità della
gocciolina.</p>
<p>Dalla seconda equazione possiamo ricavare il raggio \(R\) della gocciolina:</p>
<div class="equation">\[ R = \sqrt{\dfrac{9\,\eta\,v}{2g\,(\rho_{Olio}-\rho_{Aria})}} \]</div>
<p>Ora possiamo ricavare la carica \(q\) dalla prima equazione:</p>
<div class="equation">\[ q = \frac{4g\,(\rho_{Olio}-\rho_{Aria})\,\pi R^{3}}{3E} \]</div>
<p>sostituendo la formula trovata per \(R\):</p>
<div class="equation">\[ q = \frac{4g\,(\rho_{Olio}-\rho_{Aria})\,\pi}{3E}
\left(\dfrac{9\,\eta\,v}{2g\,(\rho_{Olio}-\rho_{Aria})}\right)^{\!3/2}
= \frac{9\pi\sqrt{2}\,(\eta\,v)^{3/2}}{E\,\sqrt{g\,(\rho_{Olio}-\rho_{Aria})}} \]</div>
<p>La formula definitiva per la carica \(q\) è</p>
<div class="equation">\[ q = \frac{9\pi\sqrt{2}\,(\eta\,v)^{3/2}}{E\,\sqrt{g\,(\rho_{Olio}-\rho_{Aria})}}
= \frac{9\pi\sqrt{2}\,\big(\eta\,\Delta x/\Delta t\big)^{3/2}}
{\dfrac{V}{d}\,\sqrt{g\,(\rho_{Olio}-\rho_{Aria})}} \]</div>
<p>Le grandezze da misurare nell'esecuzione dell'esperimento sono il campo elettrico \(E\) e
la velocità di caduta della gocciolina \(v\). Il campo \(E\) è dato dal rapporto \(V/d\) tra
la tensione \(V\) applicata e la distanza \(d\) tra le piastre del condensatore. La velocità
\(v\) si ottiene dal rapporto \(\Delta x/\Delta t\) tra lo spazio \(\Delta x\) ed il tempo
\(\Delta t\). Lo spazio \(\Delta x\) si misura mediante una scala graduata visibile
all'interno dell'oculare; il tempo \(\Delta t\) si misura con un cronometro manuale.</p>

<h2>Risultati sperimentali</h2>
<p>Le costanti da utilizzare nella formula per la carica \(q\) sono:</p>
<div class="equation">\[ \begin{aligned}
g &= 9{,}81\ \mathrm{m/s^{2}} \\
\rho_{Olio} &= 875{,}3\ \mathrm{kg/m^{3}} \\
\rho_{Aria} &= 1{,}3\ \mathrm{kg/m^{3}} \\
\eta &= 1{,}81\cdot10^{-5}\ \mathrm{Ns/m^{2}} \\
d &= 6\cdot10^{-3}\ \mathrm{m}
\end{aligned} \]</div>
<p>Sostituendo questi valori otteniamo la formula</p>
<div class="equation">\[ q = 2\cdot10^{-10}\,\frac{(\Delta x/\Delta t)^{3/2}}{V} \]</div>
<p>La seguente tabella mostra alcune misure di esempio.</p>
<div style="overflow-x:auto">
<table class="data">
<thead><tr><th>V (Volt)</th><th>&Delta;x (10<sup>-3</sup> m)</th><th>&Delta;t (s)</th><th>q (10<sup>-19</sup> C)</th></tr></thead>
<tbody>
<tr><td>140</td><td>3,2</td><td>45,4</td><td>8,3</td></tr>
<tr><td>50</td><td>3,2</td><td>125,5</td><td>5,1</td></tr>
<tr><td>250</td><td>3,2</td><td>59,1</td><td>3,2</td></tr>
<tr><td>480</td><td>3,7</td><td>24,1</td><td>8,0</td></tr>
<tr><td>400</td><td>3,7</td><td>49,5</td><td>3,3</td></tr>
<tr><td>510</td><td>3,7</td><td>41,7</td><td>3,3</td></tr>
<tr><td>270</td><td>3,2</td><td>88,1</td><td>1,6</td></tr>
<tr><td>380</td><td>3,2</td><td>44,1</td><td>3,2</td></tr>
<tr><td>400</td><td>3,2</td><td>66,1</td><td>1,7</td></tr>
</tbody>
</table>
</div>
<p>La cosa importante da osservare in questi risultati è che i valori della carica \(q\) non
sono casuali. Compare ripetutamente il valore di circa \(1{,}6\cdot10^{-19}\) C, e poi
compaiono altri valori che sono multipli di \(1{,}6\cdot10^{-19}\) C, cioè
\(3{,}2\cdot10^{-19}\) C, \(4{,}8\cdot10^{-19}\) C e \(6{,}4\cdot10^{-19}\) C. Inoltre non ci
sono valori inferiori a \(1{,}6\cdot10^{-19}\) C.</p>
<p>Questi risultati provano che la carica accumulata sulle goccioline di olio è corpuscolare,
cioè è formata da un certo numero di particelle elementari ognuna delle quali porta una
carica costante di \(1{,}6\cdot10^{-19}\) C.</p>
<p>È ragionevole pensare che queste particelle siano elettroni. Quindi con questo esperimento
abbiamo determinato la carica dell'elettrone.</p>

<h2>Ricapitolazione</h2>
<p>In questa scheda abbiamo preso familiarità con un'importante particella elementare,
l'elettrone. Abbiamo descritto degli esperimenti nei quali l'elettrone si comporta come una
particella materiale della meccanica classica. Tramite questi esperimenti abbiamo visto come
si può misurare il rapporto \(\dfrac{q}{m}\) tra la carica e la massa ed infine, grazie
all'esperimento di Millikan, abbiamo misurato la carica \(q = 1{,}6\cdot10^{-19}\) C. Inoltre
abbiamo descritto un esperimento che ci permette di raccogliere le prime informazioni sulla
struttura dell'atomo: abbiamo visto che un atomo è un sistema neutro formato da un nucleo
positivo e da un certo numero di elettroni, e abbiamo osservato che un nucleo è molto più
pesante di un elettrone, quindi contiene quasi tutta la massa dell'atomo.</p>
'''
