"""Scrive sorgenti/nota-08-matrici-hermitiane.html (bilingue, formule KaTeX pre-generate).

Marcatori: <P>italiano\n|english</P>, <H2>italiano|english</H2>, <EQ>tex</EQ>, {{tex}} in linea.
"""
import json
import re
import subprocess
from pathlib import Path

FUORI = Path('sorgenti/nota-08-matrici-hermitiane.html')

TESTA = '''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://laquantistica.com/nota-08-matrici-hermitiane.html">
<title>Nota 08 · Perché preferiamo le matrici hermitiane — La Quantistica</title>
<meta name="description" content="Le matrici hermitiane stanno ai numeri reali come le antihermitiane agli immaginari puri: i loro autovalori sono reali, e sono i numeri con cui si esprime una misura. E che cosa sarebbe cambiato tenendo la matrice antihermitiana.">
<link rel="stylesheet" href="assets/lang.css?v=7">
<link rel="stylesheet" href="assets/note.css?v=6">
<script src="assets/lang.js?v=8"></script>
<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">
<style id="note-math">
html,body{overflow-x:clip;}
</style>
<script src="assets/note-back.js?v=1" defer></script>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">

    <div class="doc-meta">
      <span class="tag"><span class="it">Nota 08</span><span class="en">Note 08</span></span>
      <a class="doc-back-crumb" id="backCrumb" href="04-diffrazione.html#nota-8"><span class="crumb-arrow" aria-hidden="true">&larr;</span><span class="vh"><span class="it">Torna al </span><span class="en">Back to </span></span><span class="cap it">Cap. 04 · Diffrazione degli Elettroni</span><span class="cap en">Ch. 04 · Electron Diffraction</span></a>
      <div class="langsw" role="group" aria-label="Lingua / Language">
        <button class="langbtn" type="button" data-l="it" aria-pressed="false">Italiano</button>
        <button class="langbtn" type="button" data-l="en" aria-pressed="true">English</button>
      </div>
    </div>

    <h1 class="doc-title">
      <span class="lead"><span class="it">Una scelta</span><span class="en">A choice</span></span>
      <span class="it">Perché preferiamo le matrici hermitiane?</span><span class="en">Why do we prefer Hermitian matrices?</span>
    </h1>

'''

CORPO = r'''
<P class="lede">Ricavando l’equazione di evoluzione abbiamo trovato una matrice antihermitiana, {{A(t)}}, e l’abbiamo subito sostituita con {{H(t)=iA(t)}}, che è hermitiana. La sostituzione non aggiunge e non toglie nulla al risultato: le due scritture dicono la stessa cosa. Vediamo perché preferiamo la seconda.
|In deriving the evolution equation we found an anti-Hermitian matrix, {{A(t)}}, and immediately replaced it with {{H(t)=iA(t)}}, which is Hermitian. The replacement neither adds to nor takes away from the result: the two ways of writing say the same thing. Let us see why we prefer the second.</P>

<H2>Reali e immaginari puri|Real and purely imaginary</H2>

<P>Fra le matrici e i numeri c’è un’analogia stretta, e in essa l’operazione di aggiunto corrisponde alla coniugazione complessa. Un numero è reale quando coincide con il suo coniugato, {{z^*=z}}; è immaginario puro quando cambia segno, {{z^*=-z}}. Allo stesso modo una matrice è hermitiana quando {{H^+=H}}, ed è antihermitiana quando {{A^+=-A}}.
|Between matrices and numbers there is a close analogy, and in it the adjoint corresponds to complex conjugation. A number is real when it equals its own conjugate, {{z^*=z}}; it is purely imaginary when it changes sign, {{z^*=-z}}. In the same way a matrix is Hermitian when {{H^+=H}}, and anti-Hermitian when {{A^+=-A}}.</P>

<P>L’analogia prosegue: moltiplicare per {{i}} porta un numero reale in un immaginario puro e viceversa, e porta una matrice hermitiana in una antihermitiana e viceversa. È il passaggio che abbiamo fatto scrivendo {{H=iA}}, lo stesso che avevamo già fatto passando dall’operatore derivata {{D}} alla matrice {{K=iD}}.
|The analogy goes further: multiplying by {{i}} carries a real number into a purely imaginary one and back, and carries a Hermitian matrix into an anti-Hermitian one and back. It is the step we took in writing {{H=iA}}, the same one we had already taken in passing from the derivative operator {{D}} to the matrix {{K=iD}}.</P>

<H2>Gli autovalori|The eigenvalues</H2>

<P>La differenza si vede meglio negli autovalori. Sia {{|\psi\rangle}} un autovettore di una matrice hermitiana {{H}}, con autovalore {{a}}, cioè {{H|\psi\rangle=a|\psi\rangle}}. Allora
|The difference shows up best in the eigenvalues. Let {{|\psi\rangle}} be an eigenvector of a Hermitian matrix {{H}}, with eigenvalue {{a}}, that is {{H|\psi\rangle=a|\psi\rangle}}. Then</P>

<EQ>\begin{aligned}
a\langle\psi|\psi\rangle & =\langle\psi|H|\psi\rangle={\left(\langle\psi|H^+|\psi\rangle\right)}^* \\
& ={\left(\langle\psi|H|\psi\rangle\right)}^*=a^*\langle\psi|\psi\rangle
\end{aligned}</EQ>

<P>dove il secondo passaggio vale per qualunque matrice e il terzo usa {{H^+=H}}. Poiché {{\langle\psi|\psi\rangle}} non è nullo, resta {{a=a^*}}: l’autovalore è reale. Rifacendo lo stesso conto con una matrice antihermitiana, dove {{A^+=-A}}, il terzo passaggio cambia segno e si arriva a {{a=-a^*}}: l’autovalore è immaginario puro. Lo zero, che è reale e immaginario puro insieme, è l’unico valore che le due famiglie hanno in comune.
|where the second step holds for any matrix and the third uses {{H^+=H}}. Since {{\langle\psi|\psi\rangle}} is not zero, we are left with {{a=a^*}}: the eigenvalue is real. Repeating the same computation with an anti-Hermitian matrix, where {{A^+=-A}}, the third step changes sign and we arrive at {{a=-a^*}}: the eigenvalue is purely imaginary. Zero, which is real and purely imaginary at once, is the only value the two families have in common.</P>

<H2>Perché scegliamo le hermitiane|Why we choose the Hermitian ones</H2>

<P>Perché i numeri reali sono quelli con cui si esprime il risultato di una misura. Vedremo più avanti che le matrici hermitiane corrispondono a grandezze fisiche che già conosciamo — l’energia, la quantità di moto, la posizione — e che i loro autovalori sono i valori che quelle grandezze possono assumere. Non è una corrispondenza che imponiamo adesso: verrà fuori da sé, e trovarla scritta con numeri reali ci risparmierà di doverla tradurre ogni volta.
|Because real numbers are the ones in which the result of a measurement is expressed. We shall see later that Hermitian matrices correspond to physical quantities we already know — energy, momentum, position — and that their eigenvalues are the values those quantities can take. It is not a correspondence we are imposing now: it will emerge on its own, and finding it written in real numbers will spare us from having to translate it every time.</P>

<H2>E se avessimo tenuto <em>A</em>?|And if we had kept <em>A</em>?</H2>

<P>Non sarebbe cambiato nulla di essenziale. Il percorso resterebbe lo stesso: le formule avrebbero qualche {{i}} in più e qualche cambio di segno da tenere presente, ma le conclusioni sarebbero le medesime. E l’unità immaginaria non sparirebbe: qui l’abbiamo estratta subito, mettendola davanti alla matrice; se non lo avessimo fatto, l’avremmo incontrata comunque poco più avanti. È l’equazione a richiederla, non la nostra notazione.
|Nothing essential would have changed. The path would be the same: the formulas would have an extra {{i}} here and there, and a few sign changes to keep in mind, but the conclusions would be the very same. And the imaginary unit would not disappear: here we have extracted it at once, placing it in front of the matrix; had we not done so, we would have met it a little further on anyway. It is the equation that requires it, not our notation.</P>

<P>A questo punto della trattazione le due scritture sono del tutto equivalenti: dire che {{A}} è antihermitiana e dire che {{H}} è hermitiana è dire la stessa cosa. Abbiamo scelto la seconda perché è quella in cui riconosceremo prima le grandezze che ci interessano.
|At this point of the treatment the two ways of writing are entirely equivalent: to say that {{A}} is anti-Hermitian and to say that {{H}} is Hermitian is to say the same thing. We have chosen the second because it is the one in which we shall sooner recognise the quantities we care about.</P>
'''

CODA = '''
    <div class="doc-return">
      <a id="backBottom" href="04-diffrazione.html#nota-8"><span class="it">← Torna al punto di lettura</span><span class="en">← Back to where you were</span></a>
    </div>

    <div class="doc-foot">
      <span class="it">La Quantistica · Nota N.08 · Rev. 2026</span><span class="en">La Quantistica · Note No. 08 · Rev. 2026</span>
      <span>F. Palma</span>
    </div>

  </div>
</main>

</body>
</html>
'''

inline = re.findall(r'\{\{(.+?)\}\}', CORPO)
blocchi = re.findall(r'<EQ>(.+?)</EQ>', CORPO, re.S)
tutte = [(t, False) for t in dict.fromkeys(inline)] + [(t.strip(), True) for t in blocchi]

p = subprocess.run(['node', 'tools/katexgen/tex2katex.js'],
                   input=json.dumps([{'i': i, 'tex': t, 'display': d}
                                     for i, (t, d) in enumerate(tutte)]),
                   capture_output=True, text=True, encoding='utf-8')
if p.returncode:
    raise SystemExit(p.stderr)
reso = {}
for r in json.loads(p.stdout):
    if 'err' in r:
        raise SystemExit('%s\n%s' % (tutte[r['i']][0], r['err']))
    reso[tutte[r['i']][0]] = r['html']


def esc(t):
    return t.replace('&', '&amp;').replace("'", '&#x27;').replace('<', '&lt;').replace('>', '&gt;')


def span_inline(tex):
    return '<span class="eq-inline eq-mml" data-tex="%s">%s</span>' % (esc(tex), reso[tex])


def div_blocco(tex):
    return ('<div class="equation"><span class="eq-mml eq-mml-block" data-tex="%s">%s</span></div>'
            % (esc(tex), reso[tex]))


def formule(t):
    return re.sub(r'\{\{(.+?)\}\}', lambda m: span_inline(m.group(1)), t)


pezzi = []
for blocco in re.split(r'(<EQ>.+?</EQ>)', CORPO, flags=re.S):
    b = blocco.strip()
    if not b:
        continue
    if b.startswith('<EQ>'):
        pezzi.append('    ' + div_blocco(b[4:-5].strip()))
        continue
    for tag, attr, testo in re.findall(r'<(P|H2)(\s[^>]*)?>(.+?)</\1>', b, re.S):
        it, en = testo.split('\n|') if '\n|' in testo else testo.split('|')
        it, en = ' '.join(it.split()), ' '.join(en.split())
        el = 'p' if tag == 'P' else 'h2'
        pezzi.append('    <%s%s><span class="it">%s</span><span class="en">%s</span></%s>'
                     % (el, attr or '', formule(it), formule(en), el))

FUORI.write_text(TESTA + '\n'.join(pezzi) + '\n' + CODA, encoding='utf-8', newline='')
print('scritta', FUORI, len(FUORI.read_text(encoding='utf-8')), 'caratteri')
print('formule:', len(tutte))
