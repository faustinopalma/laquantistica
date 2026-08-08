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
<meta name="description" content="Perché usiamo i numeri complessi: che cosa deve avere un'algebra, le quattro sole possibilità, ampiezza e fase delle onde, il campo di Riemann-Silberstein, perché manca l'algebra a tre dimensioni e il problema agli autovalori.">
<link rel="stylesheet" href="assets/lang.css?v=7">
<link rel="stylesheet" href="assets/note.css?v=6">
<script src="assets/lang.js?v=8"></script>
<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">
<style id="note-math">
html,body{overflow-x:clip;}
.choice-table{width:100%;border-collapse:collapse;margin:1.25rem 0 1.5rem;}
.choice-table th,.choice-table td{padding:.55rem .65rem;border-bottom:1px solid var(--n-line);text-align:left;vertical-align:top;}
.choice-table th{font-family:var(--n-mono);font-size:.78rem;text-transform:uppercase;}
@media(max-width:620px){.choice-table{font-size:.86rem}.choice-table th,.choice-table td{padding:.45rem .3rem;}}
</style>
<script src="assets/note-back.js?v=1" defer></script>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">

    <div class="doc-meta">
      <span class="tag"><span class="it">Nota 09</span><span class="en">Note 09</span></span>
      <a class="doc-back-crumb" id="backCrumb" href="04b-forma-evoluzione.html#nota-9"><span class="crumb-arrow" aria-hidden="true">&larr;</span><span class="vh"><span class="it">Torna al </span><span class="en">Back to </span></span><span class="cap it">Cap. 03 · La forma dell’equazione di evoluzione</span><span class="cap en">Ch. 03 · The Form of the Evolution Equation</span></a>
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
<P class="lede">Per trascrivere le leggi della natura abbiamo bisogno di un’algebra: dobbiamo decidere quali numeri usare e quali operazioni ammettere. La scelta la facciamo noi. Che poi i fenomeni si lascino davvero descrivere con l’algebra scelta non lo decidiamo noi: lo dice l’esperienza, ed è un fatto che riguarda la natura, non la nostra scrittura.
|To transcribe the laws of nature we need an algebra: we must decide which numbers to use and which operations to allow. The choice is ours to make. Whether the phenomena then really let themselves be described by the algebra we choose is not ours to decide: experience says that, and it is a fact about nature, not about the way we write.</P>

<H2>Che cosa deve avere un’algebra|What an algebra must have</H2>

<P>Queste sono le proprietà che chiediamo.
|These are the properties we ask for.</P>

<P><strong>Somma e prodotto.</strong> I numeri si devono poter sommare e moltiplicare. Della somma vogliamo quello che vale per i numeri reali: l’ordine degli addendi non conta, esiste lo zero, ogni numero ha il suo opposto. Del prodotto vogliamo che si distribuisca sulla somma e che i fattori reali si possano portare fuori: moltiplicare {{x}} per il doppio di {{u}} deve dare il doppio di {{xu}}. Vogliamo inoltre che esista il numero {{1}}: un numero che, moltiplicato per qualunque altro, lo lascia com’è. Non pretendiamo che l’ordine dei fattori sia indifferente, né che le parentesi si possano spostare: chiediamo il meno possibile, per vedere quante possibilità restano.
|<strong>Addition and multiplication.</strong> Numbers must be able to be added and multiplied. Of addition we want what holds for the real numbers: the order of the terms does not matter, there is a zero, every number has its opposite. Of multiplication we want it to distribute over addition, and real factors to be movable out of it: multiplying {{x}} by twice {{u}} must give twice {{xu}}. We also want the number {{1}} to exist: a number that, multiplied by any other, leaves it as it is. We do not require the order of the factors to be immaterial, nor brackets to be movable: we ask for as little as possible, to see how many possibilities remain.</P>

<P><strong>La divisione.</strong> Si deve poter dividere per qualunque numero diverso da zero. Risolvere {{ax=b}} vuol dire dividere i due membri per {{a}}: se per qualche numero diverso da zero la divisione non si potesse fare, quell’equazione resterebbe senza soluzione. Non è un caso di scuola. Nell’aritmetica dell’orologio a dodici ore {{2\cdot 6}} fa {{12}}, che sull’orologio è lo zero, pur non essendo zero né {{2}} né {{6}}. Chiedere che si possa sempre dividere è chiedere che questo non succeda.
|<strong>Division.</strong> It must be possible to divide by any number other than zero. Solving {{ax=b}} means dividing both sides by {{a}}: if for some number other than zero the division could not be carried out, that equation would be left without a solution. This is not a schoolroom case. In the arithmetic of the twelve-hour clock {{2\cdot 6}} makes {{12}}, which on the clock is zero, although neither {{2}} nor {{6}} is zero. To ask that division always be possible is to ask that this shall not happen.</P>

<P><strong>Il modulo.</strong> Ogni numero ha un modulo, un numero reale non negativo, e il modulo di un prodotto è il prodotto dei moduli. Fra i numeri reali il modulo è il valore assoluto e la regola vale già: {{|ab|=|a|\,|b|}}. Quando un numero è fatto di più componenti reali prendiamo come modulo la distanza ordinaria dall’origine, {{\sqrt{a_1^2+\cdots+a_n^2}}}: è quello che si fa già con i complessi, dove {{|a+ib|=\sqrt{a^2+b^2}}}. È la proprietà che restringe di più il campo.
|<strong>The modulus.</strong> Every number has a modulus, a non-negative real number, and the modulus of a product is the product of the moduli. Among the real numbers the modulus is the absolute value and the rule already holds: {{|ab|=|a|\,|b|}}. When a number is made of several real components we take as modulus the ordinary distance from the origin, {{\sqrt{a_1^2+\cdots+a_n^2}}}: this is what is already done with the complex numbers, where {{|a+ib|=\sqrt{a^2+b^2}}}. It is the property that narrows the field the most.</P>

<P>Un insieme di numeri con tutte queste proprietà si chiama <em>algebra di divisione normata sui numeri reali</em>: il nome è lungo, ma elenca esattamente quello che abbiamo chiesto, e «norma» è il nome che i matematici danno al modulo.
|A set of numbers with all these properties is called a <em>normed division algebra over the real numbers</em>: the name is long, but it lists exactly what we have asked for, and “norm” is the name mathematicians give to the modulus.</P>

<H2>Quante possibilità abbiamo?|How many possibilities do we have?</H2>

<P>Quanti numeri reali servono per scrivere un numero dell’algebra: è questo che chiamiamo <strong>dimensione</strong>. Un numero reale ha dimensione 1. Un numero complesso {{a+ib}} ha dimensione 2, perché per darlo occorrono i due reali {{a}} e {{b}}. Se esistessero numeri fatti di tre reali, la loro algebra avrebbe dimensione 3.
|How many real numbers it takes to write a number of the algebra: this is what we call the <strong>dimension</strong>. A real number has dimension 1. A complex number {{a+ib}} has dimension 2, because giving it requires the two reals {{a}} and {{b}}. If there were numbers made of three reals, their algebra would have dimension 3.</P>

<P>Ci si aspetterebbe di poterne costruire una per ogni dimensione. Non è così. Un teorema di Hurwitz dimostra che ne esistono soltanto quattro:
|One would expect to be able to build one in every dimension. It is not so. A theorem of Hurwitz proves that only four of them exist:</P>

<TABLE>
<table class="choice-table">
<thead><tr><th><span class="it">Algebra</span><span class="en">Algebra</span></th><th><span class="it">Dimensione</span><span class="en">Dimension</span></th><th><span class="it">Che cosa smette di valere</span><span class="en">What stops holding</span></th></tr></thead>
<tbody>
<tr><td><span class="it">numeri reali</span><span class="en">real numbers</span></td><td>1</td><td><span class="it">—</span><span class="en">—</span></td></tr>
<tr><td><span class="it">numeri complessi</span><span class="en">complex numbers</span></td><td>2</td><td><span class="it">l’ordinamento</span><span class="en">the ordering</span></td></tr>
<tr><td><span class="it">quaternioni</span><span class="en">quaternions</span></td><td>4</td><td><span class="it">la commutatività del prodotto</span><span class="en">commutativity of multiplication</span></td></tr>
<tr><td><span class="it">ottonioni</span><span class="en">octonions</span></td><td>8</td><td><span class="it">l’associatività del prodotto</span><span class="en">associativity of multiplication</span></td></tr>
</tbody>
</table>
</TABLE>

<P>La terza colonna va letta in modo cumulativo. Le quattro proprietà di partenza — somma, prodotto, divisione, modulo — valgono in tutte e quattro le algebre: è ciò che le rende algebre di divisione normate. Ma ogni volta che si sale di dimensione si perde una proprietà che nell’algebra precedente valeva ancora, e le perdite si trascinano dietro: i numeri reali hanno tutto; i complessi hanno tutto tranne l’ordinamento; i quaternioni hanno perso anche la commutatività; gli ottonioni anche l’associatività.
|The third column is to be read cumulatively. The four starting properties — addition, multiplication, division, modulus — hold in all four algebras: that is what makes them normed division algebras. But each time we go up in dimension a property that still held in the previous algebra is lost, and the losses carry over: the real numbers have everything; the complex numbers have everything except the ordering; the quaternions have lost commutativity as well; the octonions associativity too.</P>

<P>Vediamo ora che cosa significa ciascuna perdita.
|Let us now see what each loss means.</P>

<P><strong>L’ordinamento.</strong> Fra due numeri reali possiamo sempre dire quale sia il maggiore, e la relazione va d’accordo con le operazioni: sommare la stessa quantità a due numeri non ne cambia l’ordine, e il prodotto di due positivi è positivo. Fra i numeri complessi un ordinamento così non esiste: chiedersi se {{2+3i}} sia maggiore o minore di {{3+2i}} non ha senso. È una perdita che possiamo permetterci, perché i numeri che leggiamo sugli strumenti restano reali, e quelli si ordinano ancora.
|<strong>The ordering.</strong> Of two real numbers we can always say which is the greater, and the relation agrees with the operations: adding the same quantity to two numbers does not change their order, and the product of two positive numbers is positive. Among complex numbers no such ordering exists: asking whether {{2+3i}} is greater or smaller than {{3+2i}} makes no sense. This is a loss we can afford, because the numbers we read off our instruments remain real, and those can still be ordered.</P>

<P>In cambio della perdita c’è un guadagno, e conviene dirlo subito perché più avanti sarà decisivo: nel campo complesso ogni equazione polinomiale non costante ha almeno una soluzione. Nei reali non è così — {{x^2+1=0}} non ne ha — ed è proprio per risolverla che {{i}} è nato. Questa proprietà si chiama <em>chiusura algebrica</em>, i complessi sono la più piccola estensione dei reali che la possiede, e fra le quattro algebre sono i soli ad averla.
|In exchange for the loss there is a gain, and it is worth saying at once because further on it will be decisive: over the complex field every nonconstant polynomial equation has at least one solution. Over the reals this is not so — {{x^2+1=0}} has none — and it was precisely in order to solve it that {{i}} was born. This property is called <em>algebraic closure</em>, the complex numbers are the smallest extension of the reals that possesses it, and among the four algebras they are the only ones that have it.</P>

<P><strong>La commutatività.</strong> I quaternioni hanno una parte reale e tre unità immaginarie, {{i}}, {{j}}, {{k}}: si scrivono {{a+bi+cj+dk}}, e Hamilton li trovò nel 1843. Il loro prodotto dipende dall’ordine dei fattori: {{ij=k}}, ma {{ji=-k}}. Chi li adopera deve dire ogni volta da quale parte moltiplica, e ogni regola si sdoppia in una versione destra e una sinistra. Non sono una curiosità: sono il modo consueto di rappresentare le rotazioni nello spazio, e si usano nella grafica al calcolatore, nella robotica e nel controllo d’assetto dei satelliti. Lì la non commutatività è un pregio, perché nemmeno le rotazioni commutano: due rotazioni eseguite in ordine diverso portano in posizioni diverse.
|<strong>Commutativity.</strong> The quaternions have a real part and three imaginary units, {{i}}, {{j}}, {{k}}: they are written {{a+bi+cj+dk}}, and Hamilton found them in 1843. Their product depends on the order of the factors: {{ij=k}}, but {{ji=-k}}. Anyone using them must state each time from which side they multiply, and every rule splits into a right-hand and a left-hand version. They are not a curiosity: they are the usual way of representing rotations in space, and they are used in computer graphics, in robotics and in the attitude control of satellites. There non-commutativity is an advantage, because rotations do not commute either: two rotations performed in a different order lead to different positions.</P>

<P><strong>L’associatività.</strong> Gli ottonioni hanno otto componenti, una reale e sette immaginarie. In essi cambia anche il modo di raggruppare i fattori: {{(ab)c}} e {{a(bc)}} possono essere diversi, e passaggi che di solito facciamo senza pensarci vanno rifatti da capo. Fuori dalla matematica non hanno un impiego consolidato: compaiono in alcuni tentativi di fisica teorica, ma nulla di stabilito.
|<strong>Associativity.</strong> The octonions have eight components, one real and seven imaginary. In them even the grouping of factors changes: {{(ab)c}} and {{a(bc)}} may differ, and steps we usually take without thinking must be redone from scratch. Outside mathematics they have no established use: they appear in some attempts at theoretical physics, but nothing settled.</P>

<P>Tirando le somme: i numeri complessi sono l’ultima algebra in cui il prodotto resta commutativo e associativo, l’unica proprietà che vi perdiamo è l’ordinamento, di cui non abbiamo bisogno, e in cambio guadagniamo la chiusura algebrica.
|To sum up: the complex numbers are the last algebra in which multiplication remains commutative and associative, the only property we lose there is the ordering, which we do not need, and in exchange we gain algebraic closure.</P>

<H2>Le onde ci indicano i complessi|Waves point us towards complex numbers</H2>

<P>Nella scheda sulla diffrazione degli elettroni abbiamo visto che a un fascio di elettroni dobbiamo associare un’onda. Per descrivere un’onda l’ampiezza non basta: due onde della stessa ampiezza possono rinforzarsi o cancellarsi a seconda di come sono sfasate, e sono proprio queste cancellazioni a formare gli anelli sullo schermo. Ogni onda porta dunque due informazioni, l’ampiezza e la fase, e la seconda conta quanto la prima.
|In the chapter on the diffraction of electrons we saw that a beam of electrons must be associated with a wave. To describe a wave the amplitude is not enough: two waves of the same amplitude can reinforce or cancel each other depending on their relative phase, and it is precisely these cancellations that form the rings on the screen. Every wave therefore carries two pieces of information, the amplitude and the phase, and the second counts as much as the first.</P>

<P>Un numero complesso porta esattamente due informazioni: il modulo e l’argomento. Scriviamo l’onda reale
|A complex number carries exactly two pieces of information: the modulus and the argument. Let us write the real wave</P>

<EQ>A\cos(kx-\omega t+\phi)</EQ>

<P>come parte reale di
|as the real part of</P>

<EQ>Ae^{i\phi}e^{i(kx-\omega t)}.</EQ>

<P>Il solo fattore {{Ae^{i\phi}}} tiene insieme ampiezza e fase. E le operazioni che ci servono diventano prodotti: sfasare significa moltiplicare per un numero di modulo uno; derivare rispetto al tempo, per un’onda di frequenza definita, significa moltiplicare per {{-i\omega}}. Soprattutto, sommare due onde diventa sommare due numeri complessi, e la somma tiene conto da sé della fase relativa.
|The single factor {{Ae^{i\phi}}} keeps amplitude and phase together. And the operations we need become products: shifting the phase means multiplying by a number of modulus one; differentiating with respect to time, for a wave of definite frequency, means multiplying by {{-i\omega}}. Above all, adding two waves becomes adding two complex numbers, and the sum takes the relative phase into account by itself.</P>

<P>Il passaggio alla parte reale è lecito perché le equazioni che scriviamo sono lineari e a coefficienti reali; torneremo su questo punto alla fine. Tutto ciò non riguarda soltanto le onde quantistiche: vale per il suono, per la luce, per le correnti alternate.
|Taking the real part is legitimate because the equations we write are linear and have real coefficients; we shall return to this point at the end. None of this concerns quantum waves only: it holds for sound, for light, for alternating currents.</P>

<H2>Un solo campo elettromagnetico|A single electromagnetic field</H2>

<P>I numeri complessi non sono indispensabili per l’elettromagnetismo classico, ma mostrano la loro utilità anche lì. Le equazioni di Maxwell nel vuoto, con le cariche e le correnti al loro posto, sono
|Complex numbers are not indispensable to classical electromagnetism, but they show their usefulness there too. Maxwell’s equations in vacuum, with the charges and currents in place, are</P>

<EQ>\begin{aligned}
\nabla\!\cdot\!\mathbf E&=\frac{\rho}{\varepsilon_0}, & \nabla\!\cdot\!\mathbf B&=0,\\
\nabla\!\times\!\mathbf E&=-\frac{\partial\mathbf B}{\partial t}, &
\nabla\!\times\!\mathbf B&=\mu_0\mathbf J+\frac{1}{c^2}\frac{\partial\mathbf E}{\partial t}.
\end{aligned}</EQ>

<P>dove {{\rho}} è la densità di carica, {{\mathbf J}} la densità di corrente, {{c}} la velocità della luce nel vuoto, e le due costanti del vuoto sono legate dalla relazione {{\varepsilon_0\mu_0c^2=1}}.
|where {{\rho}} is the charge density, {{\mathbf J}} the current density, {{c}} the speed of light in vacuum, and the two constants of free space are related by {{\varepsilon_0\mu_0c^2=1}}.</P>

<P>Poniamo
|Let us set</P>

<EQ>\mathbf F=\mathbf E+ic\mathbf B.</EQ>

<P>Il fattore {{c}} dà a {{\mathbf E}} e {{c\mathbf B}} le stesse dimensioni. La parte reale di {{\mathbf F}} è il campo elettrico, la parte immaginaria divisa per {{c}} è il campo magnetico. Le due equazioni di divergenza diventano una sola equazione complessa,
|The factor {{c}} gives {{\mathbf E}} and {{c\mathbf B}} the same dimensions. The real part of {{\mathbf F}} is the electric field, the imaginary part divided by {{c}} is the magnetic field. The two divergence equations become a single complex equation,</P>

<EQ>\nabla\!\cdot\!\mathbf F=\frac{\rho}{\varepsilon_0},</EQ>

<P>mentre le due equazioni di evoluzione diventano
|while the two evolution equations become</P>

<EQ>i\frac{\partial\mathbf F}{\partial t}=c\,\nabla\!\times\!\mathbf F-\frac{i}{\varepsilon_0}\mathbf J.</EQ>

<P>Per verificarlo basta sostituire la definizione di {{\mathbf F}} e separare le due parti. Nella prima equazione la parte reale dà la legge di Gauss e la parte immaginaria dice che il campo magnetico non ha sorgenti; nella seconda la parte reale dà la legge di Faraday e la parte immaginaria la legge di Ampère-Maxwell. Il vettore complesso {{\mathbf F}} è detto vettore di Riemann-Silberstein. Le quattro equazioni sono diventate due, sorgenti comprese, e l’elettrico e il magnetico stanno in un solo campo.
|To verify this, it is enough to substitute the definition of {{\mathbf F}} and separate the two parts. In the first equation the real part gives Gauss’s law and the imaginary part says that the magnetic field has no sources; in the second the real part gives Faraday’s law and the imaginary part the Ampère-Maxwell law. The complex vector {{\mathbf F}} is called the Riemann-Silberstein vector. The four equations have become two, sources and all, and the electric and the magnetic field sit in a single field.</P>

<P>Qui i campi misurabili restano reali: il numero complesso non cambia l’elettromagnetismo, ne accorcia la scrittura. Lo stesso vantaggio si ritrova nei circuiti in corrente alternata, dove resistenza e reattanza formano l’impedenza complessa {{Z=R+iX}}.
|Here the measurable fields remain real: the complex number does not change electromagnetism, it shortens the way we write it. The same advantage is found in alternating-current circuits, where resistance and reactance form the complex impedance {{Z=R+iX}}.</P>

<H2>Perché non un’algebra a tre dimensioni?|Why not a three-dimensional algebra?</H2>

<P>Una domanda è rimasta in sospeso: viviamo in uno spazio a tre dimensioni, perché nell’elenco delle quattro algebre il 3 non c’è? Non è una curiosità. Hamilton passò anni a cercare numeri fatti di tre componenti, e si arrese soltanto quando provò con quattro.
|One question has been left hanging: we live in a three-dimensional space, so why is 3 absent from the list of the four algebras? It is not idle curiosity. Hamilton spent years looking for numbers made of three components, and gave up only when he tried with four.</P>

<P>La risposta viene da un teorema dal nome pittoresco, il teorema della palla pelosa, che di numeri non parla affatto: parla di peli su una sfera. Vediamo prima che cosa dice, poi che cosa c’entra.
|The answer comes from a theorem with a picturesque name, the hairy ball theorem, which does not speak of numbers at all: it speaks of hairs on a sphere. Let us first see what it says, then what it has to do with us.</P>

<P>Piantiamo un pelo in ogni punto della superficie di una sfera e chiediamo tre cose: che ogni pelo sia aderente, cioè punti in una direzione tangente alla superficie; che passando da un punto a quelli vicini la direzione cambi con continuità, senza scatti; e che in nessun punto il pelo manchi. Quello che stiamo descrivendo i matematici lo chiamano un campo vettoriale tangente, continuo e mai nullo; noi diremo che la sfera è pettinata. Il teorema afferma che sulla sfera una pettinatura così non esiste: comunque si dispongano i peli, resta almeno un punto calvo, una chierica.
|We plant a hair at every point of the surface of a sphere and ask three things: that every hair lie flat, that is, point in a direction tangent to the surface; that in passing from a point to its neighbours the direction change continuously, without jumps; and that at no point the hair be missing. What we are describing is what mathematicians call a tangent vector field, continuous and nowhere zero; we shall say that the sphere is combed. The theorem states that on the sphere no such combing exists: however the hairs are laid out, at least one bald point remains, a tonsure.</P>

<P>La dimostrazione non la diamo, ma il risultato si lascia intuire. Immaginiamo di pettinare la sfera lungo i meridiani, tutti i peli dal polo nord verso il polo sud: la pettinatura riesce ovunque, tranne che ai due poli, dove i meridiani convergono e la direzione da scegliere non c’è. Lì restano due chieriche. Spostiamo i peli come vogliamo e le chieriche si spostano con loro, ma non spariscono: si possono ridurre a una sola, mai a nessuna.
|We do not give the proof, but the result can be sensed. Imagine combing the sphere along the meridians, all the hairs from the north pole towards the south pole: the combing succeeds everywhere except at the two poles, where the meridians converge and there is no direction to choose. Two tonsures remain there. Move the hairs as we like and the tonsures move with them, but they do not disappear: they can be reduced to one, never to none.</P>

<P>Il legame con la nostra domanda passa per i numeri di modulo 1. Un numero di un’algebra di dimensione 3 è fatto di tre numeri reali, quindi lo possiamo vedere come un punto dello spazio, o come il vettore che va dall’origine a quel punto: da qui in avanti useremo le due parole per la stessa cosa, e il prodotto dell’algebra si applica a questi vettori come a qualunque altro numero. I numeri di modulo 1 sono allora i punti a distanza 1 dall’origine, cioè la superficie di una sfera ordinaria, e sono quelli per cui moltiplicare non cambia le grandezze. Osserviamo infine che la sfera è centrata nell’origine, e che su una sfera così essere tangente in un punto vuol dire essere perpendicolare a quel punto.
|The link with our question runs through the numbers of modulus 1. A number of an algebra of dimension 3 is made of three real numbers, so we can see it as a point of space, or as the vector running from the origin to that point: from here on we shall use the two words for the same thing, and the multiplication of the algebra applies to these vectors as to any other number. The numbers of modulus 1 are then the points at distance 1 from the origin, that is, the surface of an ordinary sphere, and they are the ones by which multiplying does not change sizes. Let us note finally that the sphere is centred at the origin, and that on such a sphere being tangent at a point means being perpendicular to that point.</P>

<P>Il ragionamento ha questa forma. Supponiamo che l’algebra a tre dimensioni esista. Faremo vedere che allora la sua sfera si lascia pettinare; ma il teorema dice che non si lascia pettinare. L’ipotesi porta a una conclusione falsa, dunque è falsa l’ipotesi: quell’algebra non esiste. Resta da dimostrare il primo passaggio, ed è quello che facciamo ora.
|The argument has this shape. Suppose the three-dimensional algebra exists. We shall show that its sphere can then be combed; but the theorem says that it cannot. The hypothesis leads to a false conclusion, so it is the hypothesis that is false: that algebra does not exist. What remains to be proved is the first step, and that is what we do now.</P>

<P>Il punto {{1}} sta sulla sfera. Lì piantiamo il primo pelo: scegliamo una direzione tangente qualunque, cioè un vettore {{v}} non nullo perpendicolare a {{1}}. È l’unica scelta che facciamo a mano; tutti gli altri peli verranno da questa.
|The point {{1}} lies on the sphere. There we plant the first hair: we choose any tangent direction, that is, a non-zero vector {{v}} perpendicular to {{1}}. It is the only choice we make by hand; all the other hairs will come from this one.</P>

<P>Prendiamo poi un punto qualunque della sfera, cioè un numero {{u}} di modulo 1, e consideriamo l’operazione che a ogni {{x}} associa {{xu}}. È lineare, perché il prodotto si distribuisce sulla somma e i fattori reali si portano fuori. E non cambia i moduli, perché {{|xu|=|x|\,|u|=|x|}}: avendo preso il modulo uguale alla distanza dall’origine, conserva tutte le distanze. È dunque una trasformazione rigida dello spazio, e come tale conserva anche gli angoli. Porta la sfera in sé stessa, e porta il punto {{1}} nel punto {{u}}.
|Now take any point of the sphere, that is, a number {{u}} of modulus 1, and consider the operation that to every {{x}} assigns {{xu}}. It is linear, because multiplication distributes over addition and real factors come out. And it does not change the moduli, because {{|xu|=|x|\,|u|=|x|}}: having taken the modulus equal to the distance from the origin, it preserves all distances. It is therefore a rigid transformation of space, and as such it preserves angles too. It carries the sphere into itself, and carries the point {{1}} to the point {{u}}.</P>

<P>Al punto {{u}} piantiamo allora il pelo {{vu}}, il prodotto di {{v}} per {{u}}, che è l’immagine di {{v}} in quella trasformazione. È aderente: {{v}} è perpendicolare a {{1}} e gli angoli si conservano, quindi {{vu}} è perpendicolare a {{u}}. Non manca mai: se {{vu}} fosse zero avrebbe modulo zero, ma {{|vu|=|v|\neq 0}}. E cambia con continuità, perché {{vu}} dipende da {{u}} in modo lineare. Al variare di {{u}} su tutta la sfera i peli ci sono tutti, aderenti e continui: la sfera è pettinata, senza chieriche.
|At the point {{u}} let us then plant the hair {{vu}}, the product of {{v}} by {{u}}, which is the image of {{v}} under that transformation. It lies flat: {{v}} is perpendicular to {{1}} and angles are preserved, hence {{vu}} is perpendicular to {{u}}. It is never missing: if {{vu}} were zero it would have modulus zero, but {{|vu|=|v|\neq 0}}. And it changes continuously, because {{vu}} depends on {{u}} linearly. As {{u}} runs over the whole sphere the hairs are all there, lying flat and continuous: the sphere is combed, with no tonsure.</P></P>

<P>Ma la sfera non si pettina, e l’ipotesi cade con lei: l’algebra a tre dimensioni non esiste. Hamilton stava cercando una cosa che non c’era.
|But the sphere cannot be combed, and the hypothesis falls with it: the three-dimensional algebra does not exist. Hamilton was looking for something that was not there.</P>

<P>Il ragionamento vale in un senso solo. Sulla circonferenza i peli si dispongono senza difficoltà, tutti nello stesso verso di percorrenza, ma questo non dimostra che l’algebra di dimensione 2 esista: dice soltanto che in dimensione 2 l’ostacolo non c’è. Che i numeri complessi esistano lo sappiamo perché li abbiamo davanti.
|The argument runs one way only. On the circle the hairs are laid out without difficulty, all of them the same way round, but this does not prove that the algebra of dimension 2 exists: it says merely that in dimension 2 the obstacle is absent. That the complex numbers exist we know because we have them before us.</P>

<P>Devo però dire fin dove arrivo io. Di questa sezione abbiamo dimostrato una cosa sola: che se l’algebra esiste, la sua sfera si pettina. Il teorema della palla pelosa lo abbiamo preso per acquisito, e lo stesso vale per il teorema di Hurwitz, da cui viene la tabella delle quattro algebre. Dietro a entrambi c’è una matematica vasta: topologia algebrica, teoria dei fibrati, cose che si studiano per anni e che io non conosco. Mi limito a riportare le conclusioni di chi le ha costruite: le strade percorribili sono quattro, e per la scelta che dobbiamo fare questo basta. Spero di poterle studiare, un giorno.
|I must say, though, how far I myself get. Of this section we have proved one thing only: that if the algebra exists, its sphere can be combed. The hairy ball theorem we have taken as given, and the same holds for Hurwitz’s theorem, from which the table of the four algebras comes. Behind both lies a vast body of mathematics: algebraic topology, the theory of fibre bundles, things one studies for years and that I do not know. I merely report the conclusions of those who built them: the practicable roads are four, and for the choice we have to make this is enough. I hope to be able to study them one day.</P>

<H2>Il problema agli autovalori|The eigenvalue problem</H2>

<P>C’è un’ultima ragione, e nella nostra trattazione è la più concreta. Vedremo che a ogni grandezza osservabile corrisponde una matrice, e che i valori che quella grandezza può assumere sono gli autovalori di quella matrice. Un autovalore è un numero {{\lambda}} per cui esiste un vettore non nullo che la matrice si limita a moltiplicare per {{\lambda}}, senza cambiarne la direzione; per trovarli si risolve un’equazione polinomiale.
|There is one last reason, and in our treatment it is the most concrete. We shall see that to every observable quantity there corresponds a matrix, and that the values that quantity can take are the eigenvalues of that matrix. An eigenvalue is a number {{\lambda}} for which there exists a non-zero vector that the matrix merely multiplies by {{\lambda}}, without changing its direction; to find them one solves a polynomial equation.</P>

<P>Nel campo reale un’equazione polinomiale può non avere soluzioni. La matrice che ruota il piano di un angolo retto non ha alcun autovalore reale, e si capisce perché: ruotando di novanta gradi nessuna direzione resta al suo posto. Se lavorassimo con i soli numeri reali dovremmo accettare che certe grandezze non abbiano alcun valore possibile.
|Over the real field a polynomial equation may have no solutions. The matrix that rotates the plane by a right angle has no real eigenvalue, and it is clear why: under a rotation of ninety degrees no direction stays where it was. If we worked with real numbers alone we would have to accept that certain quantities have no possible value at all.</P>

<P>Nel campo complesso questo non accade mai: è la chiusura algebrica che abbiamo anticipato, nota anche come teorema fondamentale dell’algebra — ogni polinomio non costante ha almeno una radice. È qui che quel guadagno si incassa: scegliendo i complessi ci assicuriamo che il problema agli autovalori abbia sempre soluzione.
|Over the complex field this never happens: it is the algebraic closure we anticipated, also known as the fundamental theorem of algebra — every nonconstant polynomial has at least one root. This is where that gain is collected: by choosing the complex numbers we make sure that the eigenvalue problem always has a solution.</P>

<P>Resta da chiedersi se quei valori siano numeri reali, come devono essere i risultati di una misura. Lo sono, purché la matrice sia hermitiana, cioè uguale alla propria aggiunta, e vedremo che le matrici delle grandezze fisiche lo sono: lavoriamo nel campo complesso e otteniamo risultati reali. Aggiungiamo che l’unità immaginaria non la stiamo introducendo per comodità di scrittura: nella scheda comparirà da sé, quando ricaveremo l’equazione dell’evoluzione temporale.
|It remains to ask whether those values are real numbers, as the results of a measurement must be. They are, provided the matrix is Hermitian, that is, equal to its own adjoint, and we shall see that the matrices of physical quantities are: we work over the complex field and obtain real results. Let us add that we are not introducing the imaginary unit for convenience of notation: in the chapter it will appear by itself, when we derive the equation of time evolution.</P>

<H2>Una scelta che non ci vincola|A choice that does not bind us</H2>

<P>Allargare il campo dai reali ai complessi non ci impedisce di ritrovare i reali quando servono. Se un’equazione lineare omogenea ha coefficienti reali e {{f}} ne è una soluzione complessa, allora {{\operatorname{Re}f}} e {{\operatorname{Im}f}} sono soluzioni anch’esse: è il motivo per cui poco fa abbiamo potuto prendere la parte reale dell’onda.
|Extending the field from the reals to the complex numbers does not prevent us from recovering the reals when we need them. If a homogeneous linear equation has real coefficients and {{f}} is a complex solution of it, then {{\operatorname{Re}f}} and {{\operatorname{Im}f}} are solutions as well: this is the reason why we could take the real part of the wave a moment ago.</P>

<P>Ricapitolando: fra le quattro algebre possibili i numeri complessi sono l’ultima in cui il prodotto resta commutativo e associativo; tengono in una sola quantità l’ampiezza e la fase di un’onda; raccolgono in un solo campo l’elettrico e il magnetico; garantiscono che il problema agli autovalori abbia soluzione; e non ci fanno perdere i numeri reali, che restano quelli con cui leggiamo gli strumenti. Non sappiamo ancora se siano indispensabili. Sappiamo che sono l’algebra con cui conviene proseguire.
|To sum up: among the four possible algebras the complex numbers are the last in which multiplication remains commutative and associative; they hold the amplitude and the phase of a wave in a single quantity; they gather the electric and the magnetic field into one; they guarantee that the eigenvalue problem has a solution; and they do not make us lose the real numbers, which remain the ones we read off our instruments. We do not yet know whether they are indispensable. We do know that they are the algebra with which it is best to proceed.</P>

<H2>Riferimenti essenziali|Essential references</H2>

<P>Il risultato sulle quattro algebre è il teorema di Hurwitz (1898). Il teorema della palla pelosa è di L. E. J. Brouwer (1912). Per il campo elettromagnetico complesso abbiamo seguito la forma {{\mathbf F=\mathbf E+ic\mathbf B}}, introdotta nella teoria elettromagnetica da H. M. Weber e L. Silberstein e oggi nota come vettore di Riemann-Silberstein; una trattazione moderna si trova in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.
|The result on the four algebras is Hurwitz’s theorem (1898). The hairy ball theorem is due to L. E. J. Brouwer (1912). For the complex electromagnetic field we followed the form {{\mathbf F=\mathbf E+ic\mathbf B}}, introduced into electromagnetic theory by H. M. Weber and L. Silberstein and now known as the Riemann-Silberstein vector; a modern treatment can be found in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.</P>
'''

CODA = '''
    <div class="doc-return">
      <a id="backBottom" href="04b-forma-evoluzione.html#nota-9"><span class="it">← Torna al punto di lettura</span><span class="en">← Back to where you were</span></a>
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
