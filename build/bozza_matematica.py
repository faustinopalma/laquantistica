"""Monta la BOZZA del capitolo di matematica unendo le note 09 e 13.

Non riscrive nulla: prende il corpo gia' impaginato delle due note (KaTeX
compreso) e lo rimette dentro il guscio di un capitolo. Rilanciabile.
"""
import pathlib
import re

RADICE = pathlib.Path('sorgenti')
USCITA = RADICE / 'bozza-matematica.html'
GUSCIO = RADICE / '04b-forma-evoluzione.html'

APERTURA_IT = (
    'Nel capitolo che segue lo stato di una particella sar\u00e0 una funzione che a ogni punto '
    'dello spazio associa un numero complesso, e la scriveremo come un vettore, con i simboli '
    'di bra e di ket. Prima di adoperarli conviene fissare due cose: quali numeri usiamo, e '
    'come si calcola con i vettori che li hanno per componenti. Sono decisioni nostre, non '
    'risultati sperimentali, e le dichiariamo qui.')
APERTURA_EN = (
    'In the next chapter the state of a particle will be a function assigning a complex number '
    'to each point of space, and we shall write it as a vector, with the bra and ket symbols. '
    'Before using them it is worth settling two things: which numbers we use, and how one '
    'computes with vectors that have them as components. These are our decisions, not '
    'experimental results, and we declare them here.')
APERTURA2_IT = (
    'Vediamo prima quali algebre soddisfano le richieste minime che facciamo a un sistema di '
    'numeri, e perch\u00e9 fra queste scegliamo i complessi. Richiamiamo poi il coniugato e il '
    'modulo quadro, il vettore duale, il prodotto scalare, l\u2019ortogonalit\u00e0 e la '
    'decomposizione su una base: sono le sole operazioni che la deduzione dell\u2019equazione '
    'di evoluzione user\u00e0.')
APERTURA2_EN = (
    'We first see which algebras satisfy the minimal requirements we place on a system of '
    'numbers, and why among them we choose the complex ones. We then recall the conjugate and '
    'the squared modulus, the dual vector, the scalar product, orthogonality and the '
    'decomposition on a basis: these are the only operations the derivation of the evolution '
    'equation will use.')

TITOLO_IT = 'Numeri complessi e vettori di stato'
TITOLO_EN = 'Complex Numbers and State Vectors'

STILE = '''<style id="bozza-math">
.choice-table{width:100%;border-collapse:collapse;margin:1.25rem 0 1.5rem;}
.choice-table th,.choice-table td{padding:.55rem .65rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top;}
.choice-table th{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.78rem;text-transform:uppercase;}
@media(max-width:620px){.choice-table{font-size:.86rem}.choice-table th,.choice-table td{padding:.45rem .3rem;}}
</style>
'''


def corpo_nota(nome, demote_h2=False):
    """Il testo della nota fra </h1> e il piede, senza intestazione ne' ritorni."""
    s = pathlib.Path(RADICE, nome).read_text(encoding='utf-8')
    inizio = s.index('</h1>') + len('</h1>')
    fine = s.index('<div class="doc-return">')
    corpo = s[inizio:fine].strip('\n')
    corpo = corpo.replace('<p class="lede">', '<p>')
    if demote_h2:
        corpo = corpo.replace('<h2>', '<h3>').replace('</h2>', '</h3>')
    return corpo


def bilingue(it, en):
    return f'<span class="it">{it}</span><span class="en">{en}</span>'


guscio = GUSCIO.read_text(encoding='utf-8')
taglio = guscio.index('<article class="page">') + len('<article class="page">')
testa = guscio[:taglio]
coda = guscio[guscio.index('</article>'):]

testa = testa.replace(
    '<link rel="canonical" href="https://laquantistica.com/04b-forma-evoluzione.html">',
    '<link rel="canonical" href="https://laquantistica.com/bozza-matematica.html">')
testa = re.sub(r'<title>.*?</title>',
               f'<title>{TITOLO_IT} \u00b7 {TITOLO_EN}</title>', testa, count=1, flags=re.S)
testa = testa.replace('</head>', STILE + '</head>', 1)

nav = ('<nav class="chapter-nav" aria-labelledby="nav-pagina">'
       '<span id="nav-pagina" class="sr-only">'
       + bilingue('Capitolo precedente e successivo', 'Previous and next chapter') +
       '</span><a class="prev" href="04-diffrazione.html">'
       + bilingue('Precedente', 'Previous')
       + '<span class="ttl it">Diffrazione degli Elettroni</span>'
         '<span class="ttl en">Electron Diffraction</span></a>'
       '<a class="next" href="04b-forma-evoluzione.html">'
       + bilingue('Successivo', 'Next')
       + '<span class="ttl it">La forma dell\u2019equazione di evoluzione</span>'
         '<span class="ttl en">The Form of the Evolution Equation</span></a></nav>')

pezzi = [
    testa,
    '\n    <p class="eyebrow">'
    + bilingue('Bozza \u00b7 capitolo proposto', 'Draft \u00b7 proposed chapter') + '</p>',
    f'    <h1 class="title">{bilingue(TITOLO_IT, TITOLO_EN)}</h1>',
    f'    <p class="opening">{bilingue(APERTURA_IT, APERTURA_EN)}</p>',
    f'<p>{bilingue(APERTURA2_IT, APERTURA2_EN)}</p>',
    '<h2 id="sec-quali-numeri">'
    + bilingue('Quali numeri usiamo', 'Which numbers we use') + '</h2>',
    corpo_nota('nota-09-perche-numeri-complessi.html', demote_h2=True),
    '<h2 id="sec-vettori-bra-ket">'
    + bilingue('Vettori, bra e ket', 'Vectors, bras and kets') + '</h2>',
    corpo_nota('nota-13-vettori-bra-ket.html'),
    '    ' + nav,
    coda,
]
USCITA.write_text('\n'.join(pezzi), encoding='utf-8')
print(f'scritto {USCITA} ({USCITA.stat().st_size} byte)')
