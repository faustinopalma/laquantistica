"""Scrive sorgenti/nota-07-livelli-idrogeno.html sul modello delle note 05 e 06.

<EQ>...</EQ>      formula uguale nelle due lingue
<EQ2>it~~~en</EQ2> formula con annotazioni, una versione per lingua
{{...}}            formula in linea
"""
import json
import pathlib
import re
import subprocess

FUORI = pathlib.Path('sorgenti/nota-07-livelli-idrogeno.html')

TESTA = '''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://laquantistica.com/nota-07-livelli-idrogeno.html">
<title>Nota 07 &middot; I livelli energetici dell&rsquo;atomo di idrogeno &mdash; La Quantistica</title>
<meta name="description" content="La formula dei livelli dell'idrogeno ricavata dal problema agli autovalori: restrizione agli stati a simmetria sferica, sostituzione u=r&psi;, sviluppo in serie e condizione di troncamento da cui esce il numero intero n.">
<link rel="stylesheet" href="assets/lang.css?v=7">
<link rel="stylesheet" href="assets/note.css?v=5">
<script src="assets/lang.js?v=8"></script>
<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">
<style id="note-math">
html,body{overflow-x:clip;}
</style>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">

    <div class="doc-meta">
      <span class="tag"><span class="it">Nota 07</span><span class="en">Note 07</span></span>
      <span class="it" id="retLabelIt">Cap. 06 &middot; Ulteriori Sviluppi</span><span class="en" id="retLabelEn">Ch. 06 &middot; Further Developments</span>
      <div class="langsw" role="group" aria-label="Lingua / Language">
        <button class="langbtn" type="button" data-l="it" aria-pressed="false">Italiano</button>
        <button class="langbtn" type="button" data-l="en" aria-pressed="true">English</button>
      </div>
      <a class="doc-back-top" id="backTop" href="06-ulteriori-sviluppi.html#nota-7"><span class="it">&larr; Indietro</span><span class="en">&larr; Back</span></a>
    </div>

    <h1 class="doc-title">
      <span class="lead"><span class="it">Approfondimento</span><span class="en">In depth</span></span>
      <span class="it">I livelli energetici dell&rsquo;atomo di idrogeno</span><span class="en">The energy levels of the hydrogen atom</span>
    </h1>

'''

CORPO = r'''
<P>Nella scheda abbiamo posto il problema agli autovalori per l&rsquo;energia e ci siamo limitati a riportare i livelli dell&rsquo;atomo di idrogeno. Qui lo risolviamo.
|In the chapter we set up the eigenvalue problem for the energy and limited ourselves to reporting the levels of the hydrogen atom. Here we solve it.</P>

<P><strong>Il problema.</strong> Il nucleo dell&rsquo;atomo di idrogeno ha carica {{+e}} e genera il potenziale {{V(r)=e/(4\pi\varepsilon_0 r)}}; l&rsquo;elettrone che gli orbita intorno ha carica {{q=-e}}, quindi la sua energia potenziale &egrave; {{qV(r)=-e^2/(4\pi\varepsilon_0 r)}}, negativa come dev&rsquo;essere per un&rsquo;attrazione. Il problema agli autovalori della scheda diventa
|<strong>The problem.</strong> The nucleus of the hydrogen atom has charge {{+e}} and produces the potential {{V(r)=e/(4\pi\varepsilon_0 r)}}; the electron orbiting it has charge {{q=-e}}, so its potential energy is {{qV(r)=-e^2/(4\pi\varepsilon_0 r)}}, negative as it must be for an attraction. The eigenvalue problem of the chapter becomes</P>

<EQ>\left(qV(X)+\frac{1}{2m}{\overline{P}}^2\right)|\psi\rangle=E|\psi\rangle</EQ>

<P>Scriviamolo per le funzioni d&rsquo;onda. L&rsquo;operatore {{\overline{P}}} associa a {{\psi}} la funzione {{-i\hbar\overline{\nabla}\psi}}, quindi {{\overline{P}^2}} le associa {{-\hbar^2\nabla^2\psi}}, e l&rsquo;equazione diventa
|Let us write it for wave functions. The operator {{\overline{P}}} maps {{\psi}} to the function {{-i\hbar\overline{\nabla}\psi}}, so {{\overline{P}^2}} maps it to {{-\hbar^2\nabla^2\psi}}, and the equation becomes</P>

<EQ>-\frac{\hbar^2}{2m}\nabla^2\psi-\frac{1}{4\pi\varepsilon_0}\frac{e^2}{r}\psi=E\psi</EQ>

<P><strong>Prima restrizione.</strong> Restringiamo il campo di ricerca alle funzioni che dipendono solo dalla distanza {{r}} dal nucleo, cio&egrave; agli stati a simmetria sferica. Come nella quarta scheda, restringere il campo non &egrave; un&rsquo;ipotesi sul risultato: alla fine verificheremo sull&rsquo;equazione di partenza quello che avremo trovato.
|<strong>First restriction.</strong> Let us narrow the search to functions that depend only on the distance {{r}} from the nucleus, that is, to spherically symmetric states. As in the fourth chapter, narrowing the search is not an assumption about the result: in the end we shall test what we find against the original equation.</P>

<P>Per una funzione della sola {{r}} il laplaciano si scrive
|For a function of {{r}} alone the Laplacian reads</P>

<EQ>\nabla^2\psi=\frac{d^2\psi}{dr^2}+\frac{2}{r}\frac{d\psi}{dr}=\frac{1}{r}\frac{d^2(r\psi)}{dr^2}</EQ>

<P>L&rsquo;ultima uguaglianza si controlla derivando due volte il prodotto
|The last equality is checked by differentiating the product twice</P>

<EQ>\begin{aligned}
\frac{d^2(r\psi)}{dr^2} & =\frac{d}{dr}\left(\psi+r\frac{d\psi}{dr}\right) \\
 & =2\frac{d\psi}{dr}+r\frac{d^2\psi}{dr^2}
\end{aligned}</EQ>

<P>Questo suggerisce la sostituzione {{u(r)=r\psi(r)}}: moltiplicando per {{r}} l&rsquo;equazione, al posto del laplaciano compare proprio {{d^2u/dr^2}} e otteniamo un&rsquo;equazione in una sola variabile
|This suggests the substitution {{u(r)=r\psi(r)}}: multiplying the equation by {{r}}, in place of the Laplacian we get exactly {{d^2u/dr^2}}, and we obtain an equation in a single variable</P>

<EQ>-\frac{\hbar^2}{2m}\frac{d^2u}{dr^2}-\frac{1}{4\pi\varepsilon_0}\frac{e^2}{r}u=Eu</EQ>

<P>Cerchiamo gli stati legati, quelli in cui l&rsquo;elettrone resta vicino al nucleo: per questi l&rsquo;energia &egrave; negativa, quindi {{-2mE/\hbar^2}} &egrave; una quantit&agrave; positiva. Poniamo allora {{\kappa^2=-2mE/\hbar^2}} e {{A=me^2/(2\pi\varepsilon_0\hbar^2)}}, e moltiplicando per {{-2m/\hbar^2}} l&rsquo;equazione si riscrive
|We look for the bound states, those in which the electron stays near the nucleus: for these the energy is negative, so {{-2mE/\hbar^2}} is a positive quantity. Let us then set {{\kappa^2=-2mE/\hbar^2}} and {{A=me^2/(2\pi\varepsilon_0\hbar^2)}}, and multiplying by {{-2m/\hbar^2}} the equation becomes</P>

<EQ>\frac{d^2u}{dr^2}+\frac{A}{r}u-\kappa^2u=0</EQ>

<P>chiamiamola <strong>1a</strong>. Sulla soluzione abbiamo due richieste: {{u(0)=0}}, perch&eacute; altrimenti {{\psi=u/r}} divergerebbe nel nucleo, e {{u\to0}} per {{r\to\infty}}, perch&eacute; altrimenti l&rsquo;elettrone non sarebbe legato.
|call it <strong>1a</strong>. We make two demands on the solution: {{u(0)=0}}, since otherwise {{\psi=u/r}} would diverge at the nucleus, and {{u\to0}} as {{r\to\infty}}, since otherwise the electron would not be bound.</P>

<P><strong>Seconda restrizione.</strong> Per {{r}} grande il termine {{A/r}} &egrave; trascurabile e la 1a si riduce a {{d^2u/dr^2=\kappa^2u}}, che ha per soluzioni {{e^{\kappa r}}} ed {{e^{-\kappa r}}}: solo la seconda va a zero. Cerchiamo allora {{u}} nella forma
|<strong>Second restriction.</strong> For large {{r}} the term {{A/r}} is negligible and 1a reduces to {{d^2u/dr^2=\kappa^2u}}, whose solutions are {{e^{\kappa r}}} and {{e^{-\kappa r}}}: only the second goes to zero. Let us then look for {{u}} in the form</P>

<EQ>u(r)=w(r)e^{-\kappa r}</EQ>

<P>con {{w}} da determinare. Le derivate sono
|with {{w}} to be determined. The derivatives are</P>

<EQ>\begin{aligned}
\frac{du}{dr} & =\left(\frac{dw}{dr}-\kappa w\right)e^{-\kappa r} \\
\frac{d^2u}{dr^2} & =\left(\frac{d^2w}{dr^2}-2\kappa\frac{dw}{dr}+\kappa^2w\right)e^{-\kappa r}
\end{aligned}</EQ>

<P>e sostituendo nella 1a il termine in {{\kappa^2w}} si cancella con {{-\kappa^2u}}; semplificando poi il fattore {{e^{-\kappa r}}}, che non si annulla mai, resta
|and on substituting into 1a the term in {{\kappa^2w}} cancels against {{-\kappa^2u}}; cancelling then the factor {{e^{-\kappa r}}}, which never vanishes, we are left with</P>

<EQ>\frac{d^2w}{dr^2}-2\kappa\frac{dw}{dr}+\frac{A}{r}w=0</EQ>

<P>chiamiamola <strong>2a</strong>.
|call it <strong>2a</strong>.</P>

<P><strong>Terza restrizione.</strong> Cerchiamo {{w}} tra le funzioni sviluppabili in serie di potenze, e senza termine noto, perch&eacute; {{u(0)=0}}:
|<strong>Third restriction.</strong> Let us look for {{w}} among the functions expandable in a power series, and with no constant term, since {{u(0)=0}}:</P>

<EQ>w(r)=\sum_{k=1}^{\infty}c_kr^k</EQ>

<P>I tre termini della 2a diventano
|The three terms of 2a become</P>

<EQ>\begin{aligned}
\frac{d^2w}{dr^2} & =\sum_{k=1}^{\infty}k(k-1)c_kr^{k-2}=\sum_{k=1}^{\infty}k(k+1)c_{k+1}r^{k-1} \\
-2\kappa\frac{dw}{dr} & =-2\kappa\sum_{k=1}^{\infty}kc_kr^{k-1} \\
\frac{A}{r}w & =A\sum_{k=1}^{\infty}c_kr^{k-1}
\end{aligned}</EQ>

<P>dove nella prima riga abbiamo spostato di uno l&rsquo;indice della somma &mdash; il termine con {{k=1}} &egrave; nullo &mdash; per avere in tutti e tre i termini la stessa potenza {{r^{k-1}}}. La 2a si scrive allora
|where in the first line we shifted the summation index by one &mdash; the term with {{k=1}} vanishes &mdash; so as to have the same power {{r^{k-1}}} in all three terms. Equation 2a then reads</P>

<EQ>\sum_{k=1}^{\infty}\left[k(k+1)c_{k+1}-2\kappa kc_k+Ac_k\right]r^{k-1}=0</EQ>

<P>Questa deve valere per ogni {{r}}, e una serie di potenze &egrave; identicamente nulla solo se sono nulli tutti i suoi coefficienti; quindi
|This must hold for every {{r}}, and a power series vanishes identically only if all its coefficients vanish; therefore</P>

<EQ>c_{k+1}=\frac{2\kappa k-A}{k(k+1)}c_k</EQ>

<P>chiamiamola <strong>3a</strong>. Fissato {{c_1}}, la 3a determina tutti gli altri coefficienti: la soluzione &egrave; una sola, a meno del fattore costante.
|call it <strong>3a</strong>. Once {{c_1}} is fixed, 3a determines all the other coefficients: the solution is unique up to a constant factor.</P>

<P><strong>La serie deve interrompersi.</strong> Supponiamo che non si interrompa. Per {{k}} grande il termine {{A}} diventa trascurabile rispetto a {{2\kappa k}} e la 3a d&agrave;
|<strong>The series must terminate.</strong> Suppose it does not. For large {{k}} the term {{A}} becomes negligible compared with {{2\kappa k}}, and 3a gives</P>

<EQ>\frac{c_{k+1}}{c_k}\cong\frac{2\kappa}{k+1}</EQ>

<P>ma questo &egrave; esattamente il rapporto tra due coefficienti successivi dello sviluppo {{e^{2\kappa r}=\sum_{k=0}^{\infty}(2\kappa)^k r^k/k!}}. Allora {{w}} si comporterebbe come {{e^{2\kappa r}}} e {{u=we^{-\kappa r}}} come {{e^{\kappa r}}}, che non va a zero: la soluzione non sarebbe uno stato legato.
|but this is exactly the ratio between two successive coefficients of the expansion {{e^{2\kappa r}=\sum_{k=0}^{\infty}(2\kappa)^k r^k/k!}}. Then {{w}} would behave like {{e^{2\kappa r}}} and {{u=we^{-\kappa r}}} like {{e^{\kappa r}}}, which does not go to zero: the solution would not be a bound state.</P>

<P>Deve dunque esistere un intero {{n\geq1}} con {{c_n\neq0}} e {{c_{n+1}=0}}. In base alla 3a questo accade se e solo se
|There must then exist an integer {{n\geq1}} with {{c_n\neq0}} and {{c_{n+1}=0}}. By 3a this happens if and only if</P>

<EQ>2\kappa n-A=0\Leftrightarrow \kappa=\frac{A}{2n}</EQ>

<P>Ecco da dove viene il numero intero: non lo abbiamo imposto noi, lo impone la richiesta che l&rsquo;elettrone resti legato al nucleo.
|This is where the integer comes from: we did not impose it, it is imposed by the requirement that the electron stay bound to the nucleus.</P>

<P><strong>I livelli.</strong> Ricordando che {{\kappa^2=-2mE/\hbar^2}} e che {{A=me^2/2\pi\varepsilon_0\hbar^2}}, abbiamo
|<strong>The levels.</strong> Recalling that {{\kappa^2=-2mE/\hbar^2}} and that {{A=me^2/2\pi\varepsilon_0\hbar^2}}, we have</P>

<EQ>\begin{aligned}
E & =-\frac{\hbar^2\kappa^2}{2m}=-\frac{\hbar^2A^2}{8mn^2} \\
 & =-\frac{\hbar^2}{8mn^2}\frac{m^2e^4}{4\pi^2\varepsilon_0^2\hbar^4} \\
 & =-\frac{me^4}{32\pi^2\varepsilon_0^2\hbar^2n^2}
\end{aligned}</EQ>

<P>e infine, sostituendo {{\hbar=h/2\pi}},
|and finally, substituting {{\hbar=h/2\pi}},</P>

<EQ>E_n=-\frac{me^4}{8\varepsilon_0^2h^2n^2}</EQ>

<P>Come volevasi dimostrare.
|Which is what we set out to prove.</P>

<P><strong>Verifica.</strong> Prendiamo il primo livello, {{n=1}}. La 3a d&agrave; subito {{c_2=0}}, quindi {{w=c_1r}}, {{u=c_1re^{-\kappa r}}} e la funzione d&rsquo;onda &egrave; {{\psi=c_1e^{-\kappa r}}} con {{\kappa=A/2=me^2/(4\pi\varepsilon_0\hbar^2)}}. Il laplaciano vale
|<strong>Check.</strong> Take the first level, {{n=1}}. Equation 3a immediately gives {{c_2=0}}, so {{w=c_1r}}, {{u=c_1re^{-\kappa r}}} and the wave function is {{\psi=c_1e^{-\kappa r}}} with {{\kappa=A/2=me^2/(4\pi\varepsilon_0\hbar^2)}}. The Laplacian is</P>

<EQ>\begin{aligned}
\nabla^2\psi & =\frac{c_1}{r}\frac{d^2\left(re^{-\kappa r}\right)}{dr^2} \\
 & =\frac{c_1}{r}\left(\kappa^2r-2\kappa\right)e^{-\kappa r} \\
 & =\left(\kappa^2-\frac{2\kappa}{r}\right)\psi
\end{aligned}</EQ>

<P>e sostituendo nell&rsquo;equazione di partenza
|and substituting into the original equation</P>

<EQ2>\begin{aligned}
-\frac{\hbar^2}{2m}\left(\kappa^2-\frac{2\kappa}{r}\right)\psi-\frac{1}{4\pi\varepsilon_0}\frac{e^2}{r}\psi & =E\psi\Leftrightarrow \\
-\frac{\hbar^2\kappa^2}{2m}\psi+\left(\frac{\hbar^2\kappa}{m}-\frac{e^2}{4\pi\varepsilon_0}\right)\frac{\psi}{r} & =E\psi\Leftrightarrow \\
 & \quad\text{Il termine in }1/r\text{ si annulla} \\
-\frac{\hbar^2\kappa^2}{2m}\psi & =E\psi\quad\text{Verificata.}
\end{aligned}~~~\begin{aligned}
-\frac{\hbar^2}{2m}\left(\kappa^2-\frac{2\kappa}{r}\right)\psi-\frac{1}{4\pi\varepsilon_0}\frac{e^2}{r}\psi & =E\psi\Leftrightarrow \\
-\frac{\hbar^2\kappa^2}{2m}\psi+\left(\frac{\hbar^2\kappa}{m}-\frac{e^2}{4\pi\varepsilon_0}\right)\frac{\psi}{r} & =E\psi\Leftrightarrow \\
 & \quad\text{The }1/r\text{ term vanishes} \\
-\frac{\hbar^2\kappa^2}{2m}\psi & =E\psi\quad\text{Verified.}
\end{aligned}</EQ2>

<P>Il termine in {{1/r}} si annulla perch&eacute; {{\hbar^2\kappa/m=e^2/(4\pi\varepsilon_0)}}, che &egrave; proprio la definizione di {{\kappa}} per {{n=1}}; resta {{E=-\hbar^2\kappa^2/2m}}, cio&egrave; la formula trovata.
|The {{1/r}} term vanishes because {{\hbar^2\kappa/m=e^2/(4\pi\varepsilon_0)}}, which is precisely the definition of {{\kappa}} for {{n=1}}; there remains {{E=-\hbar^2\kappa^2/2m}}, that is, the formula we found.</P>

<P><strong>Cosa abbiamo lasciato fuori.</strong> Abbiamo cercato solo tra le funzioni a simmetria sferica, quelle a momento angolare nullo. Esistono anche soluzioni che dipendono dagli angoli, con momento angolare diverso da zero, e servono per descrivere gli stati dell&rsquo;atomo; ma non danno livelli nuovi: ogni {{E_n}} compare gi&agrave; tra le soluzioni trovate qui. Per i livelli energetici, che &egrave; quello che ci serviva, la restrizione non ha tolto nulla.
|<strong>What we left out.</strong> We searched only among the spherically symmetric functions, those with zero angular momentum. There are also solutions depending on the angles, with non-zero angular momentum, and they are needed to describe the states of the atom; but they give no new levels: every {{E_n}} already appears among the solutions found here. For the energy levels, which is what we needed, the restriction took nothing away.</P>

<P>Il numero {{n}} &egrave; quello che nella nona scheda compare nei salti tra i livelli: un atomo che passa da un livello di energia {{E_i}} a uno di energia {{E_f}} emette un fotone di energia {{E_i-E_f}}.
|The number {{n}} is the one that appears in the ninth chapter in the jumps between levels: an atom passing from a level of energy {{E_i}} to one of energy {{E_f}} emits a photon of energy {{E_i-E_f}}.</P>
'''

CODA = '''
    <div class="doc-return">
      <a id="backBottom" href="06-ulteriori-sviluppi.html#nota-7"><span class="it">&larr; Torna al punto di lettura</span><span class="en">&larr; Back to where you were</span></a>
    </div>

    <div class="doc-foot">
      <span class="it">La Quantistica &middot; Nota N.07 &middot; Rev. 2026</span><span class="en">La Quantistica &middot; Note No. 07 &middot; Rev. 2026</span>
      <span>F. Palma</span>
    </div>

  </div>
</main>

<script>
(function () {
  function safeRet(v) {
    if (!v) return null;
    try { v = decodeURIComponent(v); } catch (e) { return null; }
    if (v.indexOf('..') !== -1 || v.indexOf('//') !== -1) return null;
    if (/^[A-Za-z0-9._\\/-]+\\.html(#[A-Za-z0-9._-]+)?$/.test(v)) return v;
    return null;
  }
  var ret = safeRet(new URLSearchParams(location.search).get('ret')) || '06-ulteriori-sviluppi.html#nota-7';
  ['backTop', 'backBottom'].forEach(function (id) {
    var a = document.getElementById(id);
    if (a) a.setAttribute('href', ret);
  });
  var LABELS = {
    '06-ulteriori-sviluppi.html': ['Cap. 06 \\u00b7 Ulteriori Sviluppi', 'Ch. 06 \\u00b7 Further Developments'],
    '09-spettri-atomici.html': ['Cap. 09 \\u00b7 Spettri Atomici', 'Ch. 09 \\u00b7 Atomic Spectra']
  };
  var label = LABELS[ret.split('#')[0].split('/').pop()];
  if (label) {
    var it = document.getElementById('retLabelIt');
    if (it) it.textContent = label[0];
    var en = document.getElementById('retLabelEn');
    if (en) en.textContent = label[1];
  }
})();
</script>
</body>
</html>
'''

# il delimitatore di chiusura non deve mordere l'ultima graffa della formula
INLINE = r'\{\{(.+?)\}\}(?!\})'
solo_prosa = re.sub(r'<EQ2?>.+?</EQ2?>', '', CORPO, flags=re.S)
inline = re.findall(INLINE, solo_prosa)
blocchi = re.findall(r'<EQ>(.+?)</EQ>', CORPO, re.S)
doppi = []
for coppia in re.findall(r'<EQ2>(.+?)</EQ2>', CORPO, re.S):
    doppi.extend(coppia.split('~~~'))
tutte = ([(t, False) for t in dict.fromkeys(inline)]
         + [(t.strip(), True) for t in blocchi]
         + [(t.strip(), True) for t in doppi])

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
    return t.replace('&', '&amp;').replace("'", '&#x27;')


def span_inline(tex):
    return '<span class="eq-inline eq-mml" data-tex="%s">%s</span>' % (esc(tex), reso[tex])


def blocco_solo(tex, cls=''):
    c = (' ' + cls) if cls else ''
    return '<span class="eq-mml eq-mml-block%s" data-tex="%s">%s</span>' % (c, esc(tex), reso[tex])


pezzi = []
for parte in re.split(r'(<EQ>.+?</EQ>|<EQ2>.+?</EQ2>)', CORPO, flags=re.S):
    b = parte.strip()
    if not b:
        continue
    if b.startswith('<EQ2>'):
        it, en = [x.strip() for x in b[5:-6].split('~~~')]
        pezzi.append('    <div class="equation">%s%s</div>'
                     % (blocco_solo(it, 'it'), blocco_solo(en, 'en')))
        continue
    if b.startswith('<EQ>'):
        pezzi.append('    <div class="equation">%s</div>' % blocco_solo(b[4:-5].strip()))
        continue
    for par in re.findall(r'<P>(.+?)</P>', b, re.S):
        it, en = par.split('\n|')
        it, en = ' '.join(it.split()), ' '.join(en.split())
        it = re.sub(INLINE, lambda m: span_inline(m.group(1)), it)
        en = re.sub(INLINE, lambda m: span_inline(m.group(1)), en)
        pezzi.append('    <p><span class="it">%s</span><span class="en">%s</span></p>' % (it, en))

FUORI.write_text(TESTA + '\n'.join(pezzi) + '\n' + CODA, encoding='utf-8', newline='')
print('scritta', FUORI, len(FUORI.read_text(encoding='utf-8')), 'caratteri')
print('formule:', len(tutte), '| paragrafi:', sum(1 for p in pezzi if p.strip().startswith('<p>')))
