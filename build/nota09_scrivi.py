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
<meta name="description" content="Perché usiamo i numeri complessi: che cosa deve avere un'algebra, le quattro sole possibilità, ampiezza e fase delle onde, il campo di Riemann-Silberstein, il problema agli autovalori e il ritorno alle soluzioni reali.">
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
<P class="lede">Per trascrivere le leggi della natura abbiamo bisogno di un’algebra: dobbiamo decidere quali numeri usare e quali operazioni ammettere. Non è una domanda su che cosa sia fatta la natura: è la scelta di uno strumento di calcolo.
|To transcribe the laws of nature we need an algebra: we must decide which numbers to use and which operations to allow. This is not a question about what nature is made of: it is the choice of a tool for calculation.</P>

<H2>Che cosa deve avere un’algebra|What an algebra must have</H2>

<P>Queste sono le proprietà che ci servono. Da qui discende tutto il resto.
|These are the properties we need. Everything else follows from them.</P>

<P><strong>Somma e prodotto.</strong> I numeri si devono poter sommare e moltiplicare. Della somma vogliamo quello che vale per i numeri reali: l’ordine degli addendi non conta, esiste lo zero, ogni numero ha il suo opposto. Del prodotto vogliamo soltanto che si distribuisca sulla somma. Non pretendiamo che l’ordine dei fattori sia indifferente, né che le parentesi si possano spostare: chiediamo il meno possibile, per vedere quante possibilità restano.
|<strong>Addition and multiplication.</strong> Numbers must be able to be added and multiplied. Of addition we want what holds for the real numbers: the order of the terms does not matter, there is a zero, every number has its opposite. Of multiplication we want only that it distribute over addition. We do not require the order of the factors to be immaterial, nor brackets to be movable: we ask for as little as possible, to see how many possibilities remain.</P>

<P><strong>La divisione.</strong> Si deve poter dividere per qualunque numero diverso da zero. Risolvere {{ax=b}} vuol dire moltiplicare i due membri per l’inverso di {{a}}: se qualche numero diverso da zero non ha inverso, quell’equazione resta senza soluzione. Non è un caso di scuola. Nell’aritmetica dell’orologio a dodici ore {{2\cdot 6}} fa {{12}}, che sull’orologio è lo zero, pur non essendo zero né {{2}} né {{6}}; e l’equazione {{2x=1}} non ha alcuna soluzione, perché {{2x}} è sempre pari mentre {{1}} non lo è. Chiedere che si possa sempre dividere è chiedere che questo non succeda.
|<strong>Division.</strong> It must be possible to divide by any number other than zero. Solving {{ax=b}} means multiplying both sides by the inverse of {{a}}: if some nonzero number has no inverse, that equation is left with no solution. This is not a textbook curiosity. In the arithmetic of the twelve-hour clock {{2\cdot 6}} makes {{12}}, which on the clock is zero, although neither {{2}} nor {{6}} is zero; and the equation {{2x=1}} has no solution at all, because {{2x}} is always even while {{1}} is not. To require that division always be possible is to require that this not happen.</P>

<P><strong>Il modulo.</strong> Ogni numero ha un modulo, un numero reale non negativo, e il modulo di un prodotto è il prodotto dei moduli. Fra i numeri reali il modulo è il valore assoluto e la regola vale già: {{|ab|=|a|\,|b|}}. Quando un numero è fatto di più componenti reali prendiamo come modulo la distanza ordinaria dall’origine, {{\sqrt{a_1^2+\cdots+a_n^2}}}: è quello che si fa già con i complessi, dove {{|a+ib|=\sqrt{a^2+b^2}}}. È la proprietà che restringe di più il campo: senza, la grandezza di un prodotto non sarebbe determinata da quelle dei fattori.
|<strong>The modulus.</strong> Every number has a modulus, a non-negative real number, and the modulus of a product is the product of the moduli. Among the real numbers the modulus is the absolute value and the rule already holds: {{|ab|=|a|\,|b|}}. When a number is made of several real components we take as its modulus the ordinary distance from the origin, {{\sqrt{a_1^2+\cdots+a_n^2}}}: this is what is already done with the complex numbers, where {{|a+ib|=\sqrt{a^2+b^2}}}. It is the property that narrows the field the most: without it, the size of a product would not be determined by the sizes of the factors.</P>

<P>Un insieme di numeri che possiede tutte queste proprietà ha un nome: si chiama <em>algebra di divisione normata sui numeri reali</em>. Il nome è lungo ma non dice nulla di più di quello che abbiamo appena elencato. <em>Algebra</em> perché ci sono la somma e il prodotto; <em>di divisione</em> perché si può dividere per qualunque numero diverso da zero; <em>normata</em> perché c’è un modulo — i matematici lo chiamano norma — che si moltiplica insieme ai numeri; <em>sui numeri reali</em> perché ogni numero dell’insieme è costruito a partire da numeri reali.
|A set of numbers possessing all these properties has a name: it is called a <em>normed division algebra over the real numbers</em>. The name is long but says nothing more than what we have just listed. <em>Algebra</em> because addition and multiplication are there; <em>division</em> because one can divide by any number other than zero; <em>normed</em> because there is a modulus — mathematicians call it a norm — that multiplies along with the numbers; <em>over the real numbers</em> because every number in the set is built out of real numbers.</P>

<P>Queste quattro proprietà sono utili per scrivere una teoria fisica. Le grandezze si sommano quando più contributi si mettono insieme. Si moltiplicano quando una grandezza ne scala un’altra, o quando due operazioni si applicano una dopo l’altra. Si divide ogni volta che da una legge si ricava un’incognita: risolvere per {{x}} è dividere. E il modulo serve perché i conti vanno confrontati con numeri letti su uno strumento, che sono reali e hanno una grandezza; se il modulo non si moltiplicasse insieme ai numeri, dopo un calcolo lungo non sapremmo stimare nemmeno l’ordine di grandezza del risultato.
|These four properties are useful for writing a physical theory. Quantities are added when several contributions are put together. They are multiplied when one quantity scales another, or when two operations are applied one after the other. One divides whenever an unknown is drawn out of a law: solving for {{x}} is dividing. And the modulus is needed because calculations have to be compared with numbers read off an instrument, which are real and have a size; if the modulus did not multiply along with the numbers, after a long calculation we could not even estimate the order of magnitude of the result.</P>

<P>Utili non vuol dire obbligatorie. Nulla ci assicura che la natura si lasci descrivere così. Su un orologio con un numero primo di ore, per dire, somma, prodotto e divisione funzionano tutti — lì ogni numero diverso da zero ha il suo inverso — e di numeri reali non ce n’è nessuno: un mondo fatto in quel modo non lo possiamo escludere. Queste proprietà non sono imposte dall’esperienza, le scegliamo noi, e la conclusione che segue vale quanto valgono le premesse.
|Useful does not mean compulsory. Nothing assures us that nature lets itself be described this way. On a clock with a prime number of hours, say, addition, multiplication and division all work — there every number other than zero has its inverse — and there are no real numbers in it at all: a world made that way we cannot rule out. These properties are not imposed by experience, we choose them, and the conclusion that follows is worth as much as the premises are.</P>

<H2>Quante possibilità abbiamo?|How many possibilities do we have?</H2>

<P>Quanti numeri reali servono per scrivere un numero di un’algebra di divisione normata: è questo che chiamiamo <strong>dimensione</strong> dell’algebra. Un numero reale ha dimensione 1. Un numero complesso {{a+ib}} ha dimensione 2, perché per darlo occorrono i due reali {{a}} e {{b}}. Se esistessero numeri fatti di tre reali, la loro algebra avrebbe dimensione 3.
|How many real numbers it takes to write down a number of a normed division algebra: this is what we call the <strong>dimension</strong> of the algebra. A real number has dimension 1. A complex number {{a+ib}} has dimension 2, because giving it requires the two reals {{a}} and {{b}}. If there were numbers made of three reals, their algebra would have dimension 3.</P>

<P>Ci si aspetterebbe di poterne costruire una per ogni dimensione. Non è così. Un teorema di Hurwitz dimostra che ne esistono soltanto quattro, e sono queste:
|One would expect to be able to build one in every dimension. It is not so. A theorem of Hurwitz proves that only four of them exist, and they are these:</P>

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

<P>Conviene vedere che cosa significano quelle perdite, perché è su di esse che decideremo.
|It is worth seeing what those losses mean, because it is on them that we shall decide.</P>

<P><strong>L’ordinamento.</strong> Fra due numeri reali possiamo sempre dire quale sia il maggiore, e la relazione va d’accordo con le operazioni: se sommiamo la stessa quantità a due numeri il loro ordine non cambia, e il prodotto di due numeri positivi è positivo. Fra i numeri complessi un ordinamento con queste proprietà non esiste: chiedersi se {{2+3i}} sia maggiore o minore di {{3+2i}} non ha senso. È una perdita che possiamo permetterci, perché i numeri che leggiamo sugli strumenti restano reali, e quelli si ordinano ancora.
|<strong>The ordering.</strong> Of two real numbers we can always say which is the greater, and the relation agrees with the operations: adding the same quantity to two numbers does not change their order, and the product of two positive numbers is positive. Among complex numbers no ordering with these properties exists: asking whether {{2+3i}} is greater or smaller than {{3+2i}} makes no sense. This is a loss we can afford, because the numbers we read off our instruments remain real, and those can still be ordered.</P>

<P><strong>La commutatività.</strong> I quaternioni sono numeri con una parte reale e tre unità immaginarie, {{i}}, {{j}}, {{k}}: si scrivono {{a+bi+cj+dk}}, e Hamilton li trovò nel 1843. Il loro prodotto dipende dall’ordine dei fattori: {{ij=k}}, ma {{ji=-k}}. Chi li adopera deve dire ogni volta da quale parte moltiplica, e ogni regola si sdoppia in una versione destra e una sinistra. Non sono una curiosità: sono il modo consueto di rappresentare le rotazioni nello spazio, e si usano nella grafica al calcolatore, nella robotica e nel controllo d’assetto dei satelliti. Lì la non commutatività è un pregio, perché nemmeno le rotazioni commutano: due rotazioni eseguite in ordine diverso portano in posizioni diverse.
|<strong>Commutativity.</strong> Quaternions are numbers with one real part and three imaginary units, {{i}}, {{j}}, {{k}}: they are written {{a+bi+cj+dk}}, and Hamilton found them in 1843. Their product depends on the order of the factors: {{ij=k}}, but {{ji=-k}}. Anyone using them must state each time from which side they multiply, and every rule splits into a right-hand and a left-hand version. They are no curiosity: they are the usual way of representing rotations in space, and they are used in computer graphics, in robotics and in the attitude control of satellites. There, non-commutativity is a virtue, because rotations do not commute either: two rotations performed in a different order lead to different positions.</P>

<P><strong>L’associatività.</strong> Gli ottonioni hanno otto componenti: una reale e sette immaginarie. In essi cambia anche il modo di raggruppare i fattori: {{(ab)c}} e {{a(bc)}} possono essere diversi. Le parentesi non si possono più spostare, e passaggi che di solito facciamo senza pensarci vanno rifatti da capo. Fuori dalla matematica non hanno un impiego consolidato: compaiono in alcuni tentativi di fisica teorica, ma nulla di stabilito.
|<strong>Associativity.</strong> Octonions have eight components: one real and seven imaginary. In them even the grouping of factors matters: {{(ab)c}} and {{a(bc)}} may differ. Brackets can no longer be moved around, and steps we usually take without thinking must be redone from scratch. Outside mathematics they have no established use: they turn up in some attempts at theoretical physics, but nothing settled.</P>

<P>Le perdite si sommano scendendo: i quaternioni non sono ordinabili e non sono commutativi; gli ottonioni non sono ordinabili, non sono commutativi e non sono associativi. I numeri complessi sono dunque l’ultima algebra in cui il prodotto è commutativo e associativo, e l’unica proprietà che perdiamo è l’ordinamento, di cui non abbiamo bisogno.
|The losses accumulate as we go down: the quaternions are neither orderable nor commutative; the octonions are neither orderable, nor commutative, nor associative. The complex numbers are therefore the last algebra in which multiplication is commutative and associative, and the only property we lose is the ordering, which we do not need.</P>

<H2>Perché non un’algebra a tre dimensioni?|Why not a three-dimensional algebra?</H2>

<P>A un fisico la domanda viene per prima: viviamo in uno spazio a tre dimensioni, perché nell’elenco il 3 non c’è? Non è una curiosità. Hamilton passò anni a cercare numeri fatti di tre componenti, e si arrese soltanto quando provò con quattro.
|To a physicist this is the first question: we live in a three-dimensional space, so why is 3 missing from the list? It is not idle curiosity. Hamilton spent years looking for numbers made of three components, and gave up only when he tried with four.</P>

<P>Il motivo è geometrico. In un’algebra prendiamo tutti i numeri di modulo 1. Nei numeri complessi sono i punti a distanza 1 dall’origine del piano, cioè una circonferenza. In un’algebra di dimensione 3 sarebbero i punti a distanza 1 dall’origine dello spazio, cioè la superficie di una sfera ordinaria.
|The reason is geometric. In an algebra, take all the numbers of modulus 1. Among the complex numbers these are the points at distance 1 from the origin of the plane, that is, a circle. In an algebra of dimension 3 they would be the points at distance 1 from the origin of space, that is, the surface of an ordinary sphere.</P>

<P>Diciamo prima che cosa vuol dire pettinare. Piantiamo un pelo in ogni punto della superficie e chiediamo tre cose: che ogni pelo sia aderente, cioè punti in una direzione tangente alla superficie; che passando da un punto a quelli vicini la direzione cambi con continuità, senza scatti; e che in nessun punto il pelo manchi o si rizzi. Pettinare la superficie vuol dire riuscire a disporre i peli così.
|Let us first say what combing means. We plant a hair at every point of the surface and require three things: that every hair lie flat, that is, point along a direction tangent to the surface; that in passing from a point to its neighbours the direction change continuously, without jumps; and that at no point the hair be missing or stand up. To comb the surface means to succeed in laying the hairs out in this way.</P>

<P>Ora facciamo vedere che se l’algebra a tre dimensioni esiste, la sfera si pettina. Intanto il numero 1 sta sulla sfera: da {{|1|=|1\cdot 1|=|1|^2}} e {{|1|\neq 0}} segue {{|1|=1}}. In quel punto scegliamo una direzione tangente qualunque e chiamiamola {{v}}.
|Now let us show that if the three-dimensional algebra exists, the sphere can be combed. First of all the number 1 lies on the sphere: from {{|1|=|1\cdot 1|=|1|^2}} and {{|1|\neq 0}} it follows that {{|1|=1}}. At that point we choose any tangent direction and call it {{v}}.</P>

<P>Prendiamo poi un punto qualunque della sfera, cioè un numero {{u}} di modulo 1, e consideriamo l’operazione che a ogni {{x}} associa {{xu}}. È lineare, perché il prodotto si distribuisce sulla somma; e non cambia i moduli, perché {{|xu|=|x|\,|u|=|x|}}. Avendo preso il modulo uguale alla distanza dall’origine, questo vuol dire che l’operazione conserva tutte le distanze: è dunque una rotazione dello spazio, al più composta con una riflessione. Porta la sfera in sé stessa, porta il punto 1 nel punto {{u}}, e porta rigidamente il piano tangente in 1 sul piano tangente in {{u}}.
|Then take any point of the sphere, that is, a number {{u}} of modulus 1, and consider the operation sending each {{x}} to {{xu}}. It is linear, because multiplication distributes over addition; and it does not change moduli, since {{|xu|=|x|\,|u|=|x|}}. Having taken the modulus to be the distance from the origin, this means the operation preserves all distances: it is therefore a rotation of space, at most combined with a reflection. It carries the sphere onto itself, it carries the point 1 to the point {{u}}, and it carries the tangent plane at 1 rigidly onto the tangent plane at {{u}}.</P>

<P>Nel punto {{u}} piantiamo allora il pelo {{vu}}, cioè l’immagine di {{v}}. È aderente, perché la rotazione manda il piano tangente sul piano tangente. Non manca mai, perché una rotazione non schiaccia nulla a zero. E cambia con continuità, perché {{vu}} dipende da {{u}} in modo lineare. Al variare di {{u}} su tutta la sfera abbiamo un pelo in ogni punto, aderente, continuo e mai mancante: la sfera è pettinata. Resta così dimostrato che se l’algebra a tre dimensioni esiste, allora la sfera si lascia pettinare.
|At the point {{u}} we then plant the hair {{vu}}, that is, the image of {{v}}. It lies flat, because the rotation sends the tangent plane onto the tangent plane. It is never missing, because a rotation crushes nothing to zero. And it changes continuously, because {{vu}} depends linearly on {{u}}. Letting {{u}} range over the whole sphere we have a hair at every point, lying flat, continuous and never missing: the sphere is combed. It is thus proved that if the three-dimensional algebra exists, then the sphere can be combed.</P>

<P>Il teorema della palla pelosa dice che la sfera non si lascia pettinare: comunque si dispongano i peli, resta sempre almeno un punto in cui il pelo manca o si rizza. Non lo dimostriamo, lo prendiamo per acquisito. Mettendolo insieme a quanto precede il conto è chiuso: se l’algebra ci fosse la sfera si pettinerebbe; la sfera non si pettina; dunque l’algebra a tre dimensioni non esiste. Hamilton stava cercando una cosa che non c’era.
|The hairy ball theorem says that the sphere cannot be combed: however the hairs are laid out, there always remains at least one point where the hair is missing or stands up. We do not prove it, we take it as given. Putting it together with what precedes, the matter is settled: if the algebra existed the sphere could be combed; the sphere cannot be combed; therefore the three-dimensional algebra does not exist. Hamilton was looking for something that was not there.</P>

<P>Sulla circonferenza invece i peli si dispongono, mandandoli tutti nello stesso verso di percorrenza. Attenzione però: questo non dimostra che l’algebra di dimensione 2 esista. L’implicazione va in un senso solo, e quando la superficie si pettina non conclude nulla. Dice soltanto che in dimensione 2 non c’è questo ostacolo; che l’algebra ci sia lo sappiamo perché i numeri complessi li abbiamo davanti, non perché il ragionamento lo imponga.
|On the circle, by contrast, the hairs can be laid out, by sending them all the same way round. Note however: this does not prove that the algebra of dimension 2 exists. The implication runs one way only, and when the surface can be combed it concludes nothing. It says merely that in dimension 2 this obstacle is absent; that the algebra is there we know because the complex numbers are in front of us, not because the argument requires it.</P>

<P>Qui va tolto di mezzo un equivoco di parole. In matematica la sfera è la sola superficie, e la sua dimensione è quella della superficie, non dello spazio che la contiene: per dire dove ci troviamo su una sfera bastano due numeri, come la latitudine e la longitudine, quindi la sfera ordinaria ha dimensione 2 e vive nello spazio a tre dimensioni. Allo stesso modo si parla di una sfera di dimensione 3, che vive in uno spazio a quattro dimensioni, e di una di dimensione 7, che vive in uno spazio a otto. Disegnarle non possiamo, ma le formule le trattano come le altre.
|A verbal misunderstanding must be cleared away here. In mathematics the sphere is the surface alone, and its dimension is that of the surface, not of the space containing it: to say where we are on a sphere two numbers suffice, such as latitude and longitude, so the ordinary sphere has dimension 2 and lives in three-dimensional space. In the same way one speaks of a sphere of dimension 3, which lives in a four-dimensional space, and of one of dimension 7, which lives in an eight-dimensional space. We cannot draw them, but the formulas treat them like the others.</P>

<P>Lo stesso ragionamento si può fare con più direzioni alla volta. Invece di un pelo solo ne trasportiamo un fascio: in un’algebra di dimensione {{n}} scegliamo nel punto 1 un sistema di {{n-1}} direzioni tangenti indipendenti — tante quante sono le dimensioni della sfera — e lo portiamo in ogni punto moltiplicando per {{u}}. Essendo una rotazione, l’operazione mantiene le direzioni indipendenti fra loro. Diciamo allora che la sfera si lascia <strong>pettinare per intero</strong>. È una richiesta più forte del pelo singolo: la sfera di dimensione 5, per esempio, un pelo lo accetta, un sistema completo no.
|The same argument can be made with several directions at once. Instead of a single hair we carry a whole bundle: in an algebra of dimension {{n}} we choose at the point 1 a system of {{n-1}} independent tangent directions — as many as the dimensions of the sphere — and we carry it to every point by multiplying by {{u}}. Being a rotation, the operation keeps the directions independent of one another. We then say that the sphere can be <strong>combed entirely</strong>. This is a stronger requirement than the single hair: the sphere of dimension 5, for instance, accepts one hair, but not a complete system.</P>

<P>Le sole sfere che si lasciano pettinare per intero sono quelle di dimensione 0, 1, 3 e 7, e sono esattamente quelle formate dai numeri di modulo 1 delle quattro algebre. Conviene guardarle una per una.
|The only spheres that can be combed entirely are those of dimension 0, 1, 3 and 7, and they are exactly those formed by the numbers of modulus 1 of the four algebras. It is worth looking at them one at a time.</P>

<P><strong>Dimensione 0.</strong> I numeri reali di modulo 1 sono due soltanto, {{-1}} e {{+1}}: due punti staccati, e nient’altro. Su un punto non ci si può muovere, quindi non ci sono direzioni tangenti da sistemare e non c’è nulla da pettinare. Il caso è banale, ed è proprio per questo che funziona.
|<strong>Dimension 0.</strong> There are only two real numbers of modulus 1, {{-1}} and {{+1}}: two separate points, and nothing else. On a point one cannot move, so there are no tangent directions to arrange and there is nothing to comb. The case is trivial, and that is exactly why it works.</P>

<P><strong>Dimensione 1.</strong> I numeri complessi di modulo 1 formano una circonferenza, e per dire dove ci troviamo basta un numero, l’angolo. Si pettina mandando tutti i peli nello stesso verso di percorrenza.
|<strong>Dimension 1.</strong> The complex numbers of modulus 1 form a circle, and to say where we are one number suffices, the angle. It is combed by sending all the hairs the same way round.</P>

<P><strong>Dimensione 3.</strong> I quaternioni di modulo 1 formano una sfera che vive nello spazio a quattro dimensioni: per dire dove ci troviamo servono tre numeri, come su una sfera ordinaria ne servono due. Disegnarla non possiamo, ma i conti dicono che si lascia pettinare per intero: in ogni punto si possono disporre tre direzioni indipendenti.
|<strong>Dimension 3.</strong> The quaternions of modulus 1 form a sphere living in four-dimensional space: to say where we are, three numbers are needed, just as two are needed on an ordinary sphere. We cannot draw it, but the calculations say it can be combed entirely: at every point three independent directions can be laid out.</P>

<P><strong>Dimensione 7.</strong> Gli ottonioni di modulo 1 formano una sfera in uno spazio a otto dimensioni. Immaginarla non è possibile; che si lasci pettinare lo dicono soltanto i conti.
|<strong>Dimension 7.</strong> The octonions of modulus 1 form a sphere in an eight-dimensional space. Picturing it is not possible; that it can be combed is something only the calculations tell us.</P>

<P>La sfera ordinaria, quella di dimensione 2, in questo elenco non c’è: è per questo che manca l’algebra di dimensione 3.
|The ordinary sphere, the one of dimension 2, is not on this list: this is why the algebra of dimension 3 is missing.</P>

<P>Devo però dire fin dove arrivo io. Dietro a questi risultati c’è una matematica vasta — topologia algebrica, teoria dei fibrati, i lavori di Bott, Milnor e Kervaire — che non si impara in qualche settimana: sono cose che si studiano per anni. Io non le conosco. Mi limito a riportare le conclusioni di chi le ha costruite: le strade percorribili sono quattro, e per la scelta che dobbiamo fare questo basta. Spero di poterle studiare, un giorno.
|I must say, though, how far I myself get. Behind these results lies a vast body of mathematics — algebraic topology, the theory of fibre bundles, the work of Bott, Milnor and Kervaire — which is not learned in a few weeks: these are things one studies for years. I do not know them. I merely report the conclusions of those who built them: the practicable roads are four, and for the choice we have to make this is enough. I hope to be able to study them one day.</P>

<H2>Le onde ci indicano i complessi|Waves point us towards complex numbers</H2>

<P>Nella scheda sulla diffrazione degli elettroni abbiamo visto che a un fascio di elettroni dobbiamo associare un’onda. Per descrivere un’onda l’ampiezza non basta: due onde della stessa ampiezza possono rinforzarsi o cancellarsi a seconda di come sono sfasate, e sono proprio queste cancellazioni a formare gli anelli sullo schermo. Ogni onda porta dunque due informazioni, l’ampiezza e la fase, e la seconda conta quanto la prima.
|In the card on the diffraction of electrons we saw that a beam of electrons must be associated with a wave. To describe a wave the amplitude is not enough: two waves of the same amplitude can reinforce or cancel each other depending on their relative phase, and it is precisely these cancellations that form the rings on the screen. Every wave therefore carries two pieces of information, the amplitude and the phase, and the second counts as much as the first.</P>

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

<P>Qui i campi misurabili restano reali: il numero complesso non cambia l’elettromagnetismo, ne accorcia la scrittura. Lo stesso vantaggio si ritrova nei circuiti in corrente alternata, dove resistenza e reattanza formano l’impedenza complessa {{Z=R+iX}}.
|Here the measurable fields remain real: the complex number does not change electromagnetism, it shortens the way we write it. The same advantage is found in alternating-current circuits, where resistance and reactance form the complex impedance {{Z=R+iX}}.</P>

<H2>Una coppia di numeri reali non basta|A pair of real numbers is not enough</H2>

<P>Si può obiettare che un numero complesso è soltanto una coppia di numeri reali, e che quindi non abbiamo introdotto nulla di nuovo. La coppia da sola non basta: quello che conta è la regola con cui le coppie si moltiplicano,
|One might object that a complex number is merely a pair of real numbers, and that we have therefore introduced nothing new. The pair alone is not enough: what matters is the rule by which pairs are multiplied,</P>

<EQ>(a,b)\,(c,d)=(ac-bd,\;ad+bc).</EQ>

<P>È questa regola a comporre le fasi e a produrre l’interferenza; una moltiplicazione fatta componente per componente non lo farebbe. Il contenuto dei numeri complessi sta nel prodotto, non nel numero delle componenti.
|It is this rule that composes phases and produces interference; a multiplication carried out component by component would not do so. The content of the complex numbers lies in the product, not in the number of components.</P>

<P>Lo si vede anche dall’altro verso. Ogni numero complesso si può rappresentare con una matrice reale,
|The same thing can be seen from the other side. Every complex number can be represented by a real matrix,</P>

<EQ>a+ib\;\longleftrightarrow\;\begin{pmatrix}a & -b\\ b & a\end{pmatrix},</EQ>

<P>e la moltiplicazione fra numeri complessi diventa il prodotto fra queste matrici. Possiamo dunque riscrivere con soli numeri reali qualunque calcolo complesso: nulla ce lo vieta. Il prezzo è raddoppiare le componenti e portarsi dietro in ogni passaggio, scritta per esteso, la struttura che {{i}} esprime in un simbolo solo. Per questo non diciamo che la natura «è complessa»: i numeri complessi sono soltanto il modo più breve di scrivere quello che osserviamo.
|and multiplication of complex numbers becomes the product of these matrices. We can therefore rewrite any complex calculation using real numbers alone: nothing forbids it. The price is doubling the components and carrying along at every step, written out in full, the structure that {{i}} expresses in a single symbol. This is why we do not say that nature “is complex”: complex numbers are simply the shortest way of writing what we observe.</P>

<H2>Il problema agli autovalori|The eigenvalue problem</H2>

<P>C’è un’ultima ragione, e nella nostra trattazione è la più concreta. Vedremo che a ogni grandezza osservabile corrisponde una matrice, e che i valori che quella grandezza può assumere sono gli autovalori di quella matrice. Un autovalore è un numero {{\lambda}} per cui esiste un vettore non nullo che la matrice si limita a moltiplicare per {{\lambda}}, senza cambiarne la direzione; per trovarli si risolve un’equazione polinomiale.
|There is one last reason, and in our treatment it is the most concrete. We shall see that to every observable quantity there corresponds a matrix, and that the values that quantity can take are the eigenvalues of that matrix. An eigenvalue is a number {{\lambda}} for which there exists a nonzero vector that the matrix merely multiplies by {{\lambda}}, without changing its direction; to find them one solves a polynomial equation.</P>

<P>Nel campo reale un’equazione polinomiale può non avere soluzioni. La matrice che ruota il piano di un angolo retto non ha alcun autovalore reale, e si capisce perché: ruotando di novanta gradi nessuna direzione resta al suo posto. Se lavorassimo con i soli numeri reali dovremmo accettare che certe grandezze non abbiano alcun valore possibile.
|Over the real field a polynomial equation may have no solutions. The matrix that rotates the plane by a right angle has no real eigenvalue, and it is clear why: under a rotation of ninety degrees no direction stays where it was. If we worked with real numbers alone we would have to accept that certain quantities have no possible value at all.</P>

<P>Nel campo complesso questo non accade mai: ogni polinomio non costante ha almeno una radice. È il teorema fondamentale dell’algebra, e i numeri complessi sono la più piccola estensione dei reali che lo rende vero. Scegliendoli ci assicuriamo che il problema agli autovalori abbia sempre soluzione.
|Over the complex field this never happens: every nonconstant polynomial has at least one root. This is the fundamental theorem of algebra, and the complex numbers are the smallest extension of the reals that makes it true. By choosing them we make sure that the eigenvalue problem always has a solution.</P>

<P>Resta da chiedersi se quei valori siano numeri reali, come devono essere i risultati di una misura. Lo sono, purché la matrice sia hermitiana, cioè uguale alla propria aggiunta, e vedremo che le matrici delle grandezze fisiche lo sono: lavoriamo nel campo complesso e otteniamo risultati reali. Aggiungiamo che l’unità immaginaria non la stiamo introducendo per comodità di scrittura. Nella scheda sulla forma dell’equazione di evoluzione comparirà da sé, quando ricaveremo l’equazione dell’evoluzione temporale.
|It remains to ask whether those values are real numbers, as the results of a measurement must be. They are, provided the matrix is Hermitian, that is, equal to its own adjoint, and we shall see that the matrices of physical quantities are: we work over the complex field and obtain real results. Let us add that we are not introducing the imaginary unit for convenience of notation. In the card on the form of the evolution equation it will appear by itself, when we derive the equation of time evolution.</P>

<H2>Una scelta che non ci vincola|A choice that does not bind us</H2>

<P>Allargare il campo dai reali ai complessi non ci impedisce di ritrovare i reali quando servono. Se un’equazione lineare omogenea ha coefficienti reali e {{f}} ne è una soluzione complessa, allora {{\operatorname{Re}f}} e {{\operatorname{Im}f}} sono soluzioni anch’esse: è il motivo per cui poco fa abbiamo potuto prendere la parte reale dell’onda.
|Extending the field from the reals to the complex numbers does not prevent us from recovering the reals when we need them. If a homogeneous linear equation has real coefficients and {{f}} is a complex solution of it, then {{\operatorname{Re}f}} and {{\operatorname{Im}f}} are solutions as well: this is the reason why we could take the real part of the wave a moment ago.</P>

<P>Se poi il problema ha dati reali e ammette una sola soluzione, anche il coniugato {{f^*}} lo soddisfa; per unicità {{f=f^*}}, e la soluzione è reale da sé. Non dobbiamo fare nulla per riportarla nel campo reale: ci si trova già.
|If moreover the problem has real data and admits only one solution, the conjugate {{f^*}} satisfies it too; by uniqueness {{f=f^*}}, and the solution is real of its own accord. We need do nothing to bring it back to the real field: it is already there.</P>

<P>Possiamo dunque esplorare il campo complesso senza decidere in anticipo che ogni grandezza fisica debba essere complessa. Dove la fase non ha conseguenze osservabili le soluzioni verranno reali; dove le ha, come nell’interferenza, l’informazione che serve è già scritta.
|We can therefore explore the complex field without deciding in advance that every physical quantity must be complex. Where phase has no observable consequences the solutions will come out real; where it has, as in interference, the information we need is already written down.</P>

<P>Ricapitolando: fra le quattro algebre possibili i numeri complessi sono l’ultima in cui il prodotto resta commutativo e associativo; tengono in una sola quantità l’ampiezza e la fase di un’onda; raccolgono in un solo campo l’elettrico e il magnetico; garantiscono che il problema agli autovalori abbia soluzione; e non ci fanno perdere i numeri reali, che restano quelli con cui leggiamo gli strumenti. Non sappiamo ancora se siano indispensabili. Sappiamo che sono l’algebra con cui conviene proseguire.
|To sum up: among the four possible algebras the complex numbers are the last in which multiplication remains commutative and associative; they hold the amplitude and the phase of a wave in a single quantity; they gather the electric and the magnetic field into one; they guarantee that the eigenvalue problem has a solution; and they do not make us lose the real numbers, which remain the ones we read off our instruments. We do not yet know whether they are indispensable. We do know that they are the algebra with which it is best to proceed.</P>

<H2>Riferimenti essenziali|Essential references</H2>

<P>Il risultato sulle quattro algebre è il teorema di Hurwitz (1898); l’elenco delle sfere che si lasciano pettinare per intero è dovuto a Bott e Milnor e, indipendentemente, a Kervaire (1958). Per il campo elettromagnetico complesso abbiamo seguito la forma {{\mathbf F=\mathbf E+ic\mathbf B}}, introdotta nella teoria elettromagnetica da H. M. Weber e L. Silberstein e oggi nota come vettore di Riemann-Silberstein; una trattazione moderna si trova in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.
|The result on the four algebras is Hurwitz’s theorem (1898); the list of spheres that can be combed entirely is due to Bott and Milnor and, independently, to Kervaire (1958). For the complex electromagnetic field we followed the form {{\mathbf F=\mathbf E+ic\mathbf B}}, introduced into electromagnetic theory by H. M. Weber and L. Silberstein and now known as the Riemann-Silberstein vector; a modern treatment can be found in I. Bialynicki-Birula, <em>Photon wave function</em>, <em>Progress in Optics</em> 36 (1996), pp. 245–294.</P>
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
