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
<meta name="description" content="Perché usiamo i numeri complessi: le quattro algebre di divisione normate, ampiezza e fase delle onde, il campo di Riemann-Silberstein e il ritorno alle soluzioni reali.">
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
<P class="lede">Per trascrivere le leggi della natura abbiamo bisogno di un’algebra. Dobbiamo decidere quali numeri usare e quali operazioni ammettere. Non cerchiamo di stabilire di che cosa sia «fatta» la natura: cerchiamo un linguaggio abbastanza ampio da esprimere le regolarità che osserviamo e abbastanza semplice da permetterci di calcolarne le conseguenze.
|To transcribe the laws of nature we need an algebra. We must decide which numbers to use and which operations to allow. We are not trying to establish what nature is “made of”: we are looking for a language broad enough to express the regularities we observe and simple enough to let us calculate their consequences.</P>

<H2>Quante possibilità abbiamo?|How many possibilities do we have?</H2>

<P>Se chiediamo che si possano sommare, moltiplicare e dividere i numeri non nulli, e che la norma di un prodotto sia il prodotto delle norme, le possibilità non sono infinite. Un teorema di Hurwitz dimostra che le algebre reali di divisione normate hanno soltanto dimensione 1, 2, 4 oppure 8. I quattro casi sono i numeri reali, i complessi, i quaternioni e gli ottonioni.
|If we require that nonzero numbers can be added, multiplied and divided, and that the norm of a product is the product of the norms, the possibilities are not infinite. A theorem of Hurwitz proves that real normed division algebras can only have dimension 1, 2, 4 or 8. The four cases are the real numbers, complex numbers, quaternions and octonions.</P>

<TABLE>
<table class="choice-table">
<thead><tr><th><span class="it">Algebra</span><span class="en">Algebra</span></th><th><span class="it">Dimensione</span><span class="en">Dimension</span></th><th><span class="it">Proprietà che non si conserva</span><span class="en">Property no longer retained</span></th></tr></thead>
<tbody>
<tr><td>{{\mathbb R}}</td><td>1</td><td><span class="it">—</span><span class="en">—</span></td></tr>
<tr><td>{{\mathbb C}}</td><td>2</td><td><span class="it">ordinamento compatibile con le operazioni</span><span class="en">an ordering compatible with the operations</span></td></tr>
<tr><td>{{\mathbb H}}</td><td>4</td><td><span class="it">commutatività del prodotto</span><span class="en">commutativity of multiplication</span></td></tr>
<tr><td>{{\mathbb O}}</td><td>8</td><td><span class="it">associatività del prodotto</span><span class="en">associativity of multiplication</span></td></tr>
</tbody>
</table>
</TABLE>

<P>I numeri complessi sono quindi l’algebra più estesa fra queste quattro nella quale il prodotto resta commutativo e associativo. In più sono algebricamente chiusi: ogni polinomio non costante a coefficienti complessi ha almeno una radice complessa. Non è ancora una ragione fisica per sceglierli, ma è una ragione per considerarli il primo ampliamento dei numeri reali.
|Complex numbers are therefore the largest of these four algebras in which multiplication remains commutative and associative. They are also algebraically closed: every nonconstant polynomial with complex coefficients has at least one complex root. This is not yet a physical reason to choose them, but it is a reason to regard them as the first extension of the real numbers.</P>

<P>Il teorema della palla pelosa dà un’immagine del vincolo topologico: su una sfera ordinaria non possiamo assegnare in ogni punto una direzione tangente continua e mai nulla. Il risultato che serve qui è più forte: le sole sfere sulle quali si può scegliere ovunque un’intera base di direzioni tangenti sono {{S^0}}, {{S^1}}, {{S^3}} e {{S^7}}. Sono precisamente le sfere unitarie associate alle quattro algebre di dimensione 1, 2, 4 e 8. La palla pelosa introduce il problema; il teorema di Hurwitz ne dà la conclusione algebrica.
|The hairy ball theorem gives a picture of the topological restriction: on an ordinary sphere we cannot assign a continuous, nowhere-zero tangent direction at every point. The result needed here is stronger: the only spheres on which a complete basis of tangent directions can be chosen everywhere are {{S^0}}, {{S^1}}, {{S^3}} and {{S^7}}. These are precisely the unit spheres associated with the four algebras of dimension 1, 2, 4 and 8. The hairy ball theorem introduces the problem; Hurwitz’s theorem gives its algebraic conclusion.</P>

<H2>Le onde ci indicano i complessi|Waves point us towards complex numbers</H2>

<P>Nell’esperimento di diffrazione abbiamo visto che agli elettroni dobbiamo associare un comportamento ondulatorio. Per descrivere un’onda non basta indicarne l’ampiezza: occorre anche sapere in quale fase si trova. Un numero complesso contiene entrambe le informazioni. Il suo modulo dà l’ampiezza e il suo argomento dà la fase.
|In the diffraction experiment we saw that electrons must be associated with wave behaviour. To describe a wave it is not enough to specify its amplitude: we must also know its phase. A complex number contains both pieces of information. Its modulus gives the amplitude and its argument gives the phase.</P>

<P>Per esempio, l’onda reale
|For example, the real wave</P>

<EQ>A\cos(kx-\omega t+\phi)</EQ>

<P>può essere scritta come la parte reale di
|can be written as the real part of</P>

<EQ>Ae^{i\phi}e^{i(kx-\omega t)}.</EQ>

<P>Il solo numero complesso {{Ae^{i\phi}}} conserva insieme ampiezza e fase. Inoltre una derivata rispetto al tempo equivale a moltiplicare per {{-i\omega}}, e una traslazione di fase equivale a moltiplicare per un numero di modulo uno. Somme, derivate e sfasamenti diventano così operazioni algebriche. Questo vale per le onde quantistiche, ma vale già per il suono, la luce e le correnti alternate.
|The single complex number {{Ae^{i\phi}}} keeps amplitude and phase together. Moreover, differentiation with respect to time amounts to multiplication by {{-i\omega}}, and a phase shift amounts to multiplication by a number of modulus one. Sums, derivatives and phase shifts thus become algebraic operations. This is true for quantum waves, but it is already true for sound, light and alternating currents.</P>

<H2>Un solo campo elettromagnetico|A single electromagnetic field</H2>

<P>I numeri complessi non sono indispensabili per l’elettromagnetismo classico. Tuttavia mostrano la loro utilità anche lì. Nel vuoto e in assenza di cariche e correnti, le equazioni di Maxwell sono
|Complex numbers are not indispensable to classical electromagnetism. Yet they show their usefulness there as well. In vacuum and in the absence of charges and currents, Maxwell’s equations are</P>

<EQ>\begin{aligned}
\nabla\!\cdot\!\mathbf E&=0, & \nabla\!\cdot\!\mathbf B&=0,\\
\nabla\!\times\!\mathbf E&=-\frac{\partial\mathbf B}{\partial t}, &
\nabla\!\times\!\mathbf B&=\frac{1}{c^2}\frac{\partial\mathbf E}{\partial t}.
\end{aligned}</EQ>

<P>Poniamo
|Let us set</P>

<EQ>\mathbf F=\mathbf E+ic\mathbf B.</EQ>

<P>Il fattore {{c}} dà a {{\mathbf E}} e {{c\mathbf B}} le stesse dimensioni. La parte reale di {{\mathbf F}} è il campo elettrico e la parte immaginaria, divisa per {{c}}, è il campo magnetico. Le due equazioni di divergenza diventano una sola equazione complessa,
|The factor {{c}} gives {{\mathbf E}} and {{c\mathbf B}} the same dimensions. The real part of {{\mathbf F}} is the electric field and its imaginary part, divided by {{c}}, is the magnetic field. The two divergence equations become one complex equation,</P>

<EQ>\nabla\!\cdot\!\mathbf F=0,</EQ>

<P>mentre le due equazioni che descrivono l’evoluzione dei campi diventano
|while the two equations describing the evolution of the fields become</P>

<EQ>i\frac{\partial\mathbf F}{\partial t}=c\,\nabla\!\times\!\mathbf F.</EQ>

<P>Per verificarlo basta sostituire la definizione di {{\mathbf F}} e separare parte reale e parte immaginaria: si ritrovano rispettivamente la legge di Ampère-Maxwell e la legge di Faraday. Il vettore complesso {{\mathbf F}} è detto vettore di Riemann-Silberstein. In presenza di cariche e correnti compaiono i termini sorgente, ma il campo elettrico e quello magnetico restano raccolti in un solo campo complesso.
|To verify this, it is enough to substitute the definition of {{\mathbf F}} and separate real and imaginary parts: the Ampère-Maxwell law and Faraday’s law are recovered respectively. The complex vector {{\mathbf F}} is called the Riemann-Silberstein vector. In the presence of charges and currents source terms appear, but the electric and magnetic fields remain combined into a single complex field.</P>

<P>Qui i campi misurabili restano reali. Il numero complesso non cambia l’elettromagnetismo: ne rende più visibile la struttura. Lo stesso vantaggio si presenta con i fasori nei circuiti in corrente alternata, dove resistenza e reattanza formano l’impedenza complessa {{Z=R+iX}}.
|Here the measurable fields remain real. The complex number does not change electromagnetism: it makes its structure more visible. The same advantage appears with phasors in alternating-current circuits, where resistance and reactance form the complex impedance {{Z=R+iX}}.</P>

<H2>Perché non fermarci ai reali?|Why not stop at the real numbers?</H2>

<P>Ogni numero complesso {{a+ib}} può essere rappresentato mediante due numeri reali, e la sua moltiplicazione mediante una matrice reale {{2\times2}}. In questo senso possiamo riscrivere con soli numeri reali qualunque calcolo complesso, pagando il prezzo di raddoppiare le componenti e di portare esplicitamente nelle matrici la struttura che {{i}} esprime in un solo simbolo.
|Every complex number {{a+ib}} can be represented by two real numbers, and its multiplication by a real {{2\times2}} matrix. In this sense we can rewrite any complex calculation using real numbers alone, at the price of doubling the components and carrying explicitly in matrices the structure that {{i}} expresses in a single symbol.</P>

<P>Questo chiarisce anche perché non conviene concludere che un esperimento abbia dimostrato che la natura «è complessa». La formulazione complessa della Meccanica Quantistica è quella standard e mette direttamente in evidenza fase, interferenza ed evoluzione unitaria. Formulazioni reali più grandi possono riprodurne la struttura, ma la devono ricostruire con variabili e vincoli aggiuntivi. Per il nostro scopo è sufficiente una conclusione più limitata: i numeri complessi sono la scelta più promettente.
|This also explains why we should not conclude that an experiment has proved that nature “is complex”. The complex formulation of quantum mechanics is the standard one and directly displays phase, interference and unitary evolution. Larger real formulations can reproduce its structure, but must reconstruct it with additional variables and constraints. For our purpose a more limited conclusion is enough: complex numbers are the most promising choice.</P>

<H2>Una scelta che non ci vincola|A choice that does not bind us</H2>

<P>Allargare il campo dai reali ai complessi non ci impedisce di ritrovare i reali. Se un’equazione lineare ha coefficienti reali, dalla soluzione complessa {{f}} otteniamo ancora due soluzioni reali, {{\operatorname{Re}f}} e {{\operatorname{Im}f}}. Se anche i dati sono reali e la soluzione è unica, {{f^*}} soddisfa lo stesso problema; per unicità deve essere {{f=f^*}}, quindi la soluzione è reale.
|Extending the field from real to complex numbers does not prevent us from recovering the real numbers. If a linear equation has real coefficients, from a complex solution {{f}} we obtain two real solutions, {{\operatorname{Re}f}} and {{\operatorname{Im}f}}. If the data are also real and the solution is unique, {{f^*}} satisfies the same problem; by uniqueness {{f=f^*}}, so the solution is real.</P>

<P>Possiamo dunque esplorare il campo complesso senza assumere in anticipo che ogni grandezza fisica debba essere complessa. Se la legge e le condizioni del problema richiedono una soluzione reale, torneremo ai numeri reali. Se invece la fase ha conseguenze osservabili, come nell’interferenza, l’informazione necessaria è già presente.
|We can therefore explore the complex field without assuming in advance that every physical quantity must be complex. If the law and the conditions of the problem require a real solution, we shall return to real numbers. If instead phase has observable consequences, as in interference, the necessary information is already present.</P>

<P>La scelta dei numeri complessi nasce quindi da più indicazioni concordi. Fra le quattro algebre di divisione normate sono la più ampia che conserva un prodotto commutativo e associativo; descrivono in una sola quantità il modulo e la fase delle onde; raccolgono in un solo campo le due parti dell’elettromagnetismo; e non ci fanno perdere le soluzioni reali. Non sappiamo ancora se saranno indispensabili. Sappiamo però che sono l’algebra più adatta con cui proseguire.
|The choice of complex numbers therefore comes from several concordant indications. Among the four normed division algebras they are the largest that retains commutative and associative multiplication; they describe the modulus and phase of waves in a single quantity; they combine the two parts of electromagnetism in a single field; and they do not make us lose real solutions. We do not yet know whether they will be indispensable. We do know, however, that they are the most suitable algebra with which to proceed.</P>

<H2>Riferimenti essenziali|Essential references</H2>

<P>Il risultato sulle algebre di divisione normate è il teorema di Hurwitz. Per il campo elettromagnetico complesso abbiamo seguito la forma {{\mathbf F=\mathbf E+ic\mathbf B}}, introdotta nella teoria elettromagnetica da H. M. Weber e L. Silberstein e oggi nota come vettore di Riemann-Silberstein. Una trattazione moderna si trova in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.
|The result on normed division algebras is Hurwitz’s theorem. For the complex electromagnetic field we followed the form {{\mathbf F=\mathbf E+ic\mathbf B}}, introduced into electromagnetic theory by H. M. Weber and L. Silberstein and now known as the Riemann-Silberstein vector. A modern treatment can be found in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.</P>
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