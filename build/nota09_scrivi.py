"""Scrive sorgenti/nota-09-perche-numeri-complessi.html con formule KaTeX pre-generate."""
import json
import re
import subprocess
from pathlib import Path

FUORI = Path('sorgenti/nota-09-perche-numeri-complessi.html')

TESTA = '''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://laquantistica.com/nota-09-perche-numeri-complessi.html">
<title>Nota 09 · Perché scegliamo i numeri complessi? — La Quantistica</title>
<meta name="description" content="Perché usiamo i numeri complessi: che cosa chiediamo a un'algebra, le quattro sole possibilità, ampiezza e fase delle onde, il campo di Riemann-Silberstein, il problema agli autovalori e il ritorno alle soluzioni reali.">
<link rel="stylesheet" href="assets/lang.css?v=7">
<link rel="stylesheet" href="assets/note.css?v=6">
<script src="assets/lang.js?v=8"></script>
<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">
<style id="note-math">
html,body{overflow-x:clip;}
.choice-table{width:100%;border-collapse:collapse;margin:1.25rem 0 1.5rem;}
.choice-table th,.choice-table td{padding:.55rem .65rem;border-bottom:1px solid var(--n-line);text-align:left;vertical-align:top;}
.choice-table th{font-family:var(--n-mono);font-size:.78rem;text-transform:uppercase;}
@media(max-width:620px){.choice-table{font-size:.88rem}.choice-table th,.choice-table td{padding:.45rem .35rem;}}
</style>
<script src="assets/note-back.js?v=1" defer></script>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">

    <div class="doc-meta">
      <span class="tag"><span class="it">Nota 09</span><span class="en">Note 09</span></span>
      <a class="doc-back-crumb" id="backCrumb" href="04-diffrazione.html"><span class="crumb-arrow" aria-hidden="true">&larr;</span><span class="vh"><span class="it">Torna al </span><span class="en">Back to </span></span><span class="cap it">Cap. 04 · Diffrazione degli Elettroni</span><span class="cap en">Ch. 04 · Electron Diffraction</span></a>
      <div class="langsw" role="group" aria-label="Lingua / Language">
        <button class="langbtn" type="button" data-l="it" aria-pressed="false">Italiano</button>
        <button class="langbtn" type="button" data-l="en" aria-pressed="true">English</button>
      </div>
    </div>

    <h1 class="doc-title">
      <span class="lead"><span class="it">Una scelta</span><span class="en">A choice</span></span>
      <span class="it">Perché scegliamo i numeri complessi?</span><span class="en">Why do we choose complex numbers?</span>
    </h1>

'''

CORPO = r'''
<P class="lede">Per trascrivere le leggi della natura abbiamo bisogno di un’algebra: dobbiamo decidere quali numeri usare e quali operazioni ammettere. Non stiamo chiedendo di che cosa sia fatta la natura. Stiamo scegliendo un linguaggio, e lo vogliamo abbastanza ampio da esprimere quello che osserviamo e abbastanza semplice da permetterci di calcolare.
|To transcribe the laws of nature we need an algebra: we must decide which numbers to use and which operations to allow. We are not asking what nature is made of. We are choosing a language, and we want it broad enough to express what we observe and simple enough to let us calculate.</P>

<H2>Che cosa chiediamo a un’algebra|What we ask of an algebra</H2>

<P>Conviene dire subito che cosa pretendiamo, perché da qui discende tutto il resto.
|It is worth stating at once what we require, because everything else follows from it.</P>

<P>Chiediamo di poter <strong>sommare</strong>, perché gli stati si sovrappongono: la somma di due stati possibili deve essere ancora uno stato possibile. Chiediamo di poter <strong>moltiplicare</strong>, perché i processi si compongono: quando un sistema attraversa due stadi successivi, le due descrizioni vanno combinate in una sola. Chiediamo di poter <strong>dividere</strong> per un numero non nullo, perché vogliamo risolvere le equazioni, e perché l’evoluzione temporale si deve poter percorrere anche all’indietro.
|We ask to be able to <strong>add</strong>, because states superpose: the sum of two possible states must still be a possible state. We ask to be able to <strong>multiply</strong>, because processes compose: when a system goes through two successive stages, the two descriptions must be combined into one. We ask to be able to <strong>divide</strong> by any nonzero number, because we want to solve equations, and because time evolution must also be traversable backwards.</P>

<P>Chiediamo infine che il <strong>modulo di un prodotto</strong> sia il prodotto dei moduli. È la richiesta meno evidente ed è quella che restringe di più il campo. La facciamo perché le probabilità si ottengono dai moduli quadrati delle ampiezze: se due stadi successivi sono indipendenti le probabilità si moltiplicano, e questo accade soltanto se si moltiplicano anche i moduli.
|Finally, we ask that the <strong>modulus of a product</strong> be the product of the moduli. This is the least obvious requirement, and it is the one that narrows the field the most. We make it because probabilities are obtained from the squared moduli of the amplitudes: if two successive stages are independent the probabilities multiply, and this happens only if the moduli multiply as well.</P>

<P>Nessuna di queste richieste ci è imposta dall’esperienza: le imponiamo noi, perché senza di esse non sapremmo calcolare. Vale la pena tenerlo presente, perché la conclusione che segue vale quanto valgono le premesse.
|None of these requirements is imposed on us by experience: we impose them ourselves, because without them we would not know how to calculate. It is worth keeping this in mind, because the conclusion that follows is worth exactly as much as the premises.</P>

<H2>Quante possibilità abbiamo?|How many possibilities do we have?</H2>

<P>Con queste richieste le possibilità non sono infinite. Un teorema di Hurwitz dimostra che le algebre di divisione normate sui numeri reali esistono soltanto in dimensione 1, 2, 4 e 8. I quattro casi sono i numeri reali, i numeri complessi, i quaternioni e gli ottonioni. Non c’è altro.
|With these requirements the possibilities are not infinite. A theorem of Hurwitz proves that normed division algebras over the real numbers exist only in dimensions 1, 2, 4 and 8. The four cases are the real numbers, the complex numbers, the quaternions and the octonions. There is nothing else.</P>

<TABLE>
<table class="choice-table">
<thead><tr><th><span class="it">Algebra</span><span class="en">Algebra</span></th><th><span class="it">Dimensione</span><span class="en">Dimension</span></th><th><span class="it">Proprietà che si perde rispetto alla riga precedente</span><span class="en">Property lost with respect to the previous row</span></th></tr></thead>
<tbody>
<tr><td>{{\mathbb R}}</td><td>1</td><td><span class="it">—</span><span class="en">—</span></td></tr>
<tr><td>{{\mathbb C}}</td><td>2</td><td><span class="it">ordinamento compatibile con le operazioni</span><span class="en">an ordering compatible with the operations</span></td></tr>
<tr><td>{{\mathbb H}}</td><td>4</td><td><span class="it">commutatività del prodotto</span><span class="en">commutativity of multiplication</span></td></tr>
<tr><td>{{\mathbb O}}</td><td>8</td><td><span class="it">associatività del prodotto</span><span class="en">associativity of multiplication</span></td></tr>
</tbody>
</table>
</TABLE>

<P>Le perdite si sommano: i quaternioni non sono ordinabili e non sono commutativi, gli ottonioni non sono ordinabili, non sono commutativi e non sono associativi. I numeri complessi sono quindi l’algebra più ampia in cui il prodotto resta commutativo e associativo. Perdiamo l’ordinamento — di due numeri complessi non ha senso dire quale sia il maggiore — ma di un ordinamento non abbiamo bisogno: i numeri che leggiamo sugli strumenti restano reali, e quelli si ordinano ancora.
|The losses accumulate: the quaternions are neither orderable nor commutative; the octonions are neither orderable, nor commutative, nor associative. The complex numbers are therefore the largest algebra in which multiplication remains commutative and associative. We lose the ordering — of two complex numbers it makes no sense to say which is the greater — but an ordering is not something we need: the numbers we read off our instruments remain real, and those can still be ordered.</P>

<P>Resta una domanda naturale: viviamo in uno spazio a tre dimensioni, perché non un’algebra a tre dimensioni? Hamilton ci provò per anni prima di arrendersi e passare a quattro. Il motivo è topologico. Se in dimensione tre esistesse un’algebra come quella che chiediamo, potremmo prendere una base di direzioni nel punto 1 della sfera unitaria e trasportarla in ogni altro punto moltiplicandola per il punto stesso: otterremmo su tutta la sfera un campo di direzioni tangenti continuo e mai nullo. Il teorema della palla pelosa dice che questo è impossibile: una sfera ordinaria non si può pettinare. Dunque quell’algebra non esiste.
|A natural question remains: we live in a three-dimensional space, so why not a three-dimensional algebra? Hamilton tried for years before giving up and moving to four. The reason is topological. If in dimension three an algebra such as the one we are asking for existed, we could take a basis of directions at the point 1 of the unit sphere and carry it to every other point by multiplying it by that point: we would obtain, over the whole sphere, a continuous and nowhere-vanishing field of tangent directions. The hairy ball theorem says that this is impossible: an ordinary sphere cannot be combed. Hence that algebra does not exist.</P>

<P>Lo stesso argomento, portato fino in fondo, dà l’elenco completo: le sole sfere che si lasciano pettinare per intero sono quelle di dimensione 0, 1, 3 e 7, e sono precisamente le sfere unitarie delle quattro algebre. Aggiungendo la dimensione dell’asse reale si ritrovano 1, 2, 4 e 8.
|The same argument, carried through to the end, gives the complete list: the only spheres that can be combed entirely are those of dimension 0, 1, 3 and 7, and they are precisely the unit spheres of the four algebras. Adding the dimension of the real axis gives back 1, 2, 4 and 8.</P>

<H2>Le onde ci indicano i complessi|Waves point us towards complex numbers</H2>

<P>Nella scheda abbiamo visto che a un fascio di elettroni dobbiamo associare un’onda. Per descrivere un’onda l’ampiezza non basta: due onde della stessa ampiezza possono rinforzarsi o cancellarsi a seconda di come sono sfasate, e sono proprio queste cancellazioni a formare gli anelli sullo schermo. Ogni onda porta dunque due informazioni, l’ampiezza e la fase, e la seconda conta quanto la prima.
|In the chapter we saw that a beam of electrons must be associated with a wave. To describe a wave the amplitude is not enough: two waves of the same amplitude can reinforce or cancel each other depending on their relative phase, and it is precisely these cancellations that form the rings on the screen. Every wave therefore carries two pieces of information, the amplitude and the phase, and the second counts as much as the first.</P>

<P>Un numero complesso porta esattamente due informazioni: il modulo e l’argomento. Scriviamo l’onda reale
|A complex number carries exactly two pieces of information: the modulus and the argument. Let us write the real wave</P>

<EQ>A\cos(kx-\omega t+\phi)</EQ>

<P>come parte reale di
|as the real part of</P>

<EQ>Ae^{i\phi}e^{i(kx-\omega t)}.</EQ>

<P>Il solo fattore {{Ae^{i\phi}}} tiene insieme ampiezza e fase. E le operazioni che ci servono diventano prodotti: sfasare significa moltiplicare per un numero di modulo uno; derivare rispetto al tempo, per un’onda di frequenza definita, significa moltiplicare per {{-i\omega}}. Soprattutto, sommare due onde diventa sommare due numeri complessi, e la somma tiene conto da sé della fase relativa.
|The single factor {{Ae^{i\phi}}} keeps amplitude and phase together. And the operations we need become products: shifting the phase means multiplying by a number of modulus one; differentiating with respect to time, for a wave of definite frequency, means multiplying by {{-i\omega}}. Above all, adding two waves becomes adding two complex numbers, and the sum takes the relative phase into account by itself.</P>

<P>Il passaggio alla parte reale è lecito perché le equazioni che scriviamo sono lineari e a coefficienti reali; torneremo su questo punto alla fine. Aggiungiamo che tutto ciò non riguarda soltanto le onde quantistiche: vale per il suono, per la luce, per le correnti alternate. Dovunque ci sia un’onda, il numero complesso è il modo più breve di scriverla.
|Taking the real part is legitimate because the equations we write are linear and have real coefficients; we shall return to this point at the end. Let us add that none of this concerns quantum waves only: it holds for sound, for light, for alternating currents. Wherever there is a wave, the complex number is the shortest way of writing it.</P>

<H2>Un solo campo elettromagnetico|A single electromagnetic field</H2>

<P>I numeri complessi non sono indispensabili per l’elettromagnetismo classico. Mostrano però la loro utilità anche lì. Nel vuoto e in assenza di cariche e correnti, le equazioni di Maxwell sono
|Complex numbers are not indispensable to classical electromagnetism. Yet they show their usefulness there too. In vacuum and in the absence of charges and currents, Maxwell’s equations are</P>

<EQ>\begin{aligned}
\nabla\!\cdot\!\mathbf E&=0, & \nabla\!\cdot\!\mathbf B&=0,\\
\nabla\!\times\!\mathbf E&=-\frac{\partial\mathbf B}{\partial t}, &
\nabla\!\times\!\mathbf B&=\frac{1}{c^2}\frac{\partial\mathbf E}{\partial t}.
\end{aligned}</EQ>

<P>Poniamo
|Let us set</P>

<EQ>\mathbf F=\mathbf E+ic\mathbf B.</EQ>

<P>Il fattore {{c}} dà a {{\mathbf E}} e {{c\mathbf B}} le stesse dimensioni. La parte reale di {{\mathbf F}} è il campo elettrico, la parte immaginaria divisa per {{c}} è il campo magnetico. Le due equazioni di divergenza diventano una sola equazione complessa,
|The factor {{c}} gives {{\mathbf E}} and {{c\mathbf B}} the same dimensions. The real part of {{\mathbf F}} is the electric field, the imaginary part divided by {{c}} is the magnetic field. The two divergence equations become a single complex equation,</P>

<EQ>\nabla\!\cdot\!\mathbf F=0,</EQ>

<P>mentre le due equazioni che descrivono l’evoluzione dei campi diventano
|while the two equations describing the evolution of the fields become</P>

<EQ>i\frac{\partial\mathbf F}{\partial t}=c\,\nabla\!\times\!\mathbf F.</EQ>

<P>Per verificarlo basta sostituire la definizione di {{\mathbf F}} e separare le due parti: la parte reale dà la legge di Faraday, la parte immaginaria la legge di Ampère-Maxwell. Il vettore complesso {{\mathbf F}} è detto vettore di Riemann-Silberstein. In presenza di cariche e correnti al secondo membro si aggiungono i termini di sorgente, ma l’elettrico e il magnetico restano raccolti in un solo campo.
|To verify this, it is enough to substitute the definition of {{\mathbf F}} and separate the two parts: the real part gives Faraday’s law, the imaginary part the Ampère-Maxwell law. The complex vector {{\mathbf F}} is called the Riemann-Silberstein vector. In the presence of charges and currents, source terms are added on the right-hand side, but the electric and the magnetic field remain gathered into a single field.</P>

<P>Anche le due grandezze invarianti del campo escono insieme: il prodotto {{\mathbf F\cdot\mathbf F}} ha per parte reale {{E^2-c^2B^2}} e per parte immaginaria {{2c\,\mathbf E\cdot\mathbf B}}. Qui i campi misurabili restano reali: il numero complesso non cambia l’elettromagnetismo, ne accorcia la scrittura. Lo stesso vantaggio si ritrova nei circuiti in corrente alternata, dove resistenza e reattanza formano l’impedenza complessa {{Z=R+iX}}.
|The two invariant quantities of the field also come out together: the product {{\mathbf F\cdot\mathbf F}} has real part {{E^2-c^2B^2}} and imaginary part {{2c\,\mathbf E\cdot\mathbf B}}. Here the measurable fields remain real: the complex number does not change electromagnetism, it shortens the way we write it. The same advantage is found in alternating-current circuits, where resistance and reactance form the complex impedance {{Z=R+iX}}.</P>

<H2>Una coppia di numeri reali non basta|A pair of real numbers is not enough</H2>

<P>Si può obiettare che un numero complesso è soltanto una coppia di numeri reali, e che quindi non abbiamo introdotto nulla di nuovo. La coppia da sola non basta: quello che conta è la regola con cui le coppie si moltiplicano,
|One might object that a complex number is merely a pair of real numbers, and that we have therefore introduced nothing new. The pair alone is not enough: what matters is the rule by which pairs are multiplied,</P>

<EQ>(a,b)\,(c,d)=(ac-bd,\;ad+bc).</EQ>

<P>È questa regola a comporre le fasi e a produrre l’interferenza; una moltiplicazione fatta componente per componente non lo farebbe. Il contenuto dei numeri complessi sta nel prodotto, non nel numero delle componenti.
|It is this rule that composes phases and produces interference; a multiplication carried out component by component would not do so. The content of the complex numbers lies in the product, not in the number of components.</P>

<P>Lo si vede anche dall’altro verso. Ogni numero complesso si può rappresentare con una matrice reale,
|The same thing can be seen from the other side. Every complex number can be represented by a real matrix,</P>

<EQ>a+ib\;\longleftrightarrow\;\begin{pmatrix}a & -b\\ b & a\end{pmatrix},</EQ>

<P>e la moltiplicazione fra numeri complessi diventa il prodotto fra queste matrici. Possiamo dunque riscrivere con soli numeri reali qualunque calcolo complesso: nulla ce lo vieta. Il prezzo è raddoppiare le componenti e portarsi dietro in ogni passaggio, scritta per esteso, la struttura che {{i}} esprime in un simbolo solo. Per questo non diciamo che la natura «è complessa»: diciamo che i numeri complessi sono il modo più breve di scrivere quello che osserviamo.
|and multiplication of complex numbers becomes the product of these matrices. We can therefore rewrite any complex calculation using real numbers alone: nothing forbids it. The price is doubling the components and carrying along at every step, written out in full, the structure that {{i}} expresses in a single symbol. This is why we do not say that nature “is complex”: we say that complex numbers are the shortest way of writing what we observe.</P>

<H2>Il problema agli autovalori|The eigenvalue problem</H2>

<P>C’è un’ultima ragione, e nella nostra trattazione è la più concreta. Vedremo che a ogni grandezza osservabile corrisponde una matrice, e che i valori che quella grandezza può assumere sono gli autovalori della matrice. Gli autovalori si trovano risolvendo un’equazione polinomiale.
|There is one last reason, and in our treatment it is the most concrete. We shall see that to every observable quantity there corresponds a matrix, and that the values that quantity can take are the eigenvalues of the matrix. Eigenvalues are found by solving a polynomial equation.</P>

<P>Nel campo reale un’equazione polinomiale può non avere soluzioni. La matrice che ruota il piano di un angolo retto non ha alcun autovalore reale, perché non lascia ferma nessuna direzione. Se lavorassimo con i soli numeri reali dovremmo accettare che certe grandezze non abbiano alcun valore possibile.
|Over the real field a polynomial equation may have no solutions. The matrix that rotates the plane by a right angle has no real eigenvalue, because it leaves no direction fixed. If we worked with real numbers alone we would have to accept that certain quantities have no possible value at all.</P>

<P>Nel campo complesso questo non accade mai: ogni polinomio non costante ha almeno una radice. È il teorema fondamentale dell’algebra, e i numeri complessi sono la più piccola estensione dei reali che lo rende vero. Scegliendoli ci assicuriamo che il problema agli autovalori abbia sempre soluzione.
|Over the complex field this never happens: every nonconstant polynomial has at least one root. This is the fundamental theorem of algebra, and the complex numbers are the smallest extension of the reals that makes it true. By choosing them we make sure that the eigenvalue problem always has a solution.</P>

<P>Resta da chiedersi se quei valori siano numeri reali, come devono essere i risultati di una misura. Lo sono, purché la matrice sia hermitiana, e vedremo che le matrici delle grandezze fisiche lo sono: lavoriamo nel campo complesso e otteniamo risultati reali. Aggiungiamo che l’unità immaginaria non la stiamo introducendo per comodità di scrittura. Nella scheda comparirà da sé, quando ricaveremo l’equazione di evoluzione temporale.
|It remains to ask whether those values are real numbers, as the results of a measurement must be. They are, provided the matrix is Hermitian, and we shall see that the matrices of physical quantities are: we work over the complex field and obtain real results. Let us add that we are not introducing the imaginary unit for convenience of notation. In the chapter it will appear by itself, when we derive the time-evolution equation.</P>

<H2>Una scelta che non ci vincola|A choice that does not bind us</H2>

<P>Allargare il campo dai reali ai complessi non ci impedisce di ritrovare i reali quando servono. Se un’equazione lineare omogenea ha coefficienti reali e {{f}} ne è una soluzione complessa, allora {{\operatorname{Re}f}} e {{\operatorname{Im}f}} sono soluzioni anch’esse: è il motivo per cui poco fa abbiamo potuto prendere la parte reale dell’onda.
|Extending the field from the reals to the complex numbers does not prevent us from recovering the reals when we need them. If a homogeneous linear equation has real coefficients and {{f}} is a complex solution of it, then {{\operatorname{Re}f}} and {{\operatorname{Im}f}} are solutions as well: this is the reason why we could take the real part of the wave a moment ago.</P>

<P>Se poi il problema ha dati reali e ammette una sola soluzione, anche il coniugato {{f^*}} lo soddisfa; per unicità {{f=f^*}}, e la soluzione è reale da sé. Non dobbiamo fare nulla per riportarla nel campo reale: ci si trova già.
|If moreover the problem has real data and admits only one solution, the conjugate {{f^*}} satisfies it too; by uniqueness {{f=f^*}}, and the solution is real of its own accord. We need do nothing to bring it back to the real field: it is already there.</P>

<P>Possiamo dunque esplorare il campo complesso senza decidere in anticipo che ogni grandezza fisica debba essere complessa. Dove la fase non ha conseguenze osservabili le soluzioni verranno reali; dove le ha, come nell’interferenza, l’informazione che serve è già scritta.
|We can therefore explore the complex field without deciding in advance that every physical quantity must be complex. Where phase has no observable consequences the solutions will come out real; where it has, as in interference, the information we need is already written down.</P>

<P>Ricapitolando: fra le quattro algebre possibili i numeri complessi sono la più ampia con prodotto commutativo e associativo; tengono in una sola quantità l’ampiezza e la fase di un’onda; raccolgono in un solo campo l’elettrico e il magnetico; garantiscono che il problema agli autovalori abbia soluzione; e non ci fanno perdere i numeri reali, che restano quelli con cui leggiamo gli strumenti. Non sappiamo ancora se siano indispensabili. Sappiamo che sono l’algebra con cui conviene proseguire.
|To sum up: among the four possible algebras the complex numbers are the largest with commutative and associative multiplication; they hold the amplitude and the phase of a wave in a single quantity; they gather the electric and the magnetic field into one; they guarantee that the eigenvalue problem has a solution; and they do not make us lose the real numbers, which remain the ones we read off our instruments. We do not yet know whether they are indispensable. We do know that they are the algebra with which it is best to proceed.</P>

<H2>Riferimenti essenziali|Essential references</H2>

<P>Il risultato sulle algebre di divisione normate è il teorema di Hurwitz; l’elenco delle sfere pettinabili è dovuto a Bott, Milnor e Kervaire (1958). Per il campo elettromagnetico complesso abbiamo seguito la forma {{\mathbf F=\mathbf E+ic\mathbf B}}, introdotta nella teoria elettromagnetica da H. M. Weber e L. Silberstein e oggi nota come vettore di Riemann-Silberstein; una trattazione moderna si trova in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.
|The result on normed division algebras is Hurwitz’s theorem; the list of combable spheres is due to Bott, Milnor and Kervaire (1958). For the complex electromagnetic field we followed the form {{\mathbf F=\mathbf E+ic\mathbf B}}, introduced into electromagnetic theory by H. M. Weber and L. Silberstein and now known as the Riemann-Silberstein vector; a modern treatment can be found in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.</P>
'''

CODA = '''
    <div class="doc-return">
      <a id="backBottom" href="04-diffrazione.html"><span class="it">← Torna al Capitolo 4</span><span class="en">← Back to Chapter 4</span></a>
    </div>

    <div class="doc-foot">
      <span class="it">La Quantistica · Nota N.09 · Rev. 2026</span><span class="en">La Quantistica · Note No. 09 · Rev. 2026</span>
      <span>F. Palma</span>
    </div>

  </div>
</main>
</body>
</html>
'''


def marcatori(testo):
    """Posizioni dei {{tex}}, contando le graffe annidate del LaTeX."""
    risultati = []
    posizione = 0
    while True:
        inizio = testo.find('{{', posizione)
        if inizio < 0:
            return risultati
        indice = inizio + 2
        profondita = 0
        while indice < len(testo):
            if profondita == 0 and testo.startswith('}}', indice):
                risultati.append((inizio, indice + 2, testo[inizio + 2:indice]))
                posizione = indice + 2
                break
            if testo[indice] == '{':
                profondita += 1
            elif testo[indice] == '}':
                profondita -= 1
            indice += 1
        else:
            raise ValueError('Marcatore di formula non chiuso')


inline = [tex for _, _, tex in marcatori(CORPO)]
blocchi = re.findall(r'<EQ>(.+?)</EQ>', CORPO, re.S)
tutte = [(t, False) for t in dict.fromkeys(inline)] + [(t.strip(), True) for t in blocchi]

proc = subprocess.run(
    ['node', 'tools/katexgen/tex2katex.js'],
    input=json.dumps([{'i': i, 'tex': tex, 'display': display}
                      for i, (tex, display) in enumerate(tutte)]),
    capture_output=True, text=True, encoding='utf-8')
if proc.returncode:
    raise SystemExit(proc.stderr)

reso = {}
for risultato in json.loads(proc.stdout):
    if 'err' in risultato:
        raise SystemExit('%s\n%s' % (tutte[risultato['i']][0], risultato['err']))
    reso[tutte[risultato['i']][0]] = risultato['html']


def esc(testo):
    return (testo.replace('&', '&amp;').replace("'", '&#x27;')
            .replace('<', '&lt;').replace('>', '&gt;'))


def span_inline(tex):
    return '<span class="eq-inline eq-mml" data-tex="%s">%s</span>' % (esc(tex), reso[tex])


def div_blocco(tex):
    return ('<div class="equation"><span class="eq-mml eq-mml-block" data-tex="%s">%s</span></div>'
            % (esc(tex), reso[tex]))


def formule(testo):
    parti = []
    posizione = 0
    for inizio, fine, tex in marcatori(testo):
        parti.extend((testo[posizione:inizio], span_inline(tex)))
        posizione = fine
    parti.append(testo[posizione:])
    return ''.join(parti)


pezzi = []
for blocco in re.split(r'(<EQ>.+?</EQ>|<TABLE>.+?</TABLE>)', CORPO, flags=re.S):
    parte = blocco.strip()
    if not parte:
        continue
    if parte.startswith('<EQ>'):
        pezzi.append('    ' + div_blocco(parte[4:-5].strip()))
        continue
    if parte.startswith('<TABLE>'):
        pezzi.append('    ' + formule(parte[7:-8].strip()))
        continue
    for tag, attr, testo in re.findall(r'<(P|H2)(\s[^>]*)?>(.+?)</\1>', parte, re.S):
        italiano, inglese = testo.split('\n|') if '\n|' in testo else testo.split('|')
        italiano, inglese = ' '.join(italiano.split()), ' '.join(inglese.split())
        elemento = 'p' if tag == 'P' else 'h2'
        pezzi.append('    <%s%s><span class="it">%s</span><span class="en">%s</span></%s>'
                     % (elemento, attr or '', formule(italiano), formule(inglese), elemento))

FUORI.write_text(TESTA + '\n'.join(pezzi) + '\n' + CODA, encoding='utf-8', newline='')
print('scritta', FUORI, len(FUORI.read_text(encoding='utf-8')), 'caratteri')
print('formule:', len(tutte))
