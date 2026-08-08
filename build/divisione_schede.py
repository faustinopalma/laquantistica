"""Divide le schede 4 e 5 e sposta in note i due blocchi di puro calcolo.

Non riscrive la prosa: sposta blocchi interi di HTML gia' reso. Le uniche parole nuove sono
i cappelli delle schede nuove, i richiami alle note e una frase nella scheda 4c, dove le
dimostrazioni non stanno piu' nel testo.

Barra laterale, numeri di capitolo e navigazione avanti/indietro vengono riscritti dopo,
da build/ordine_schede.py.
"""
import pathlib
import re
import sys

RADICE = pathlib.Path('sorgenti')


def righe(nome):
    return RADICE.joinpath(nome).read_text(encoding='utf-8').split('\n')


def dove(elenco, frammento, da=0):
    for i in range(da, len(elenco)):
        if frammento in elenco[i]:
            return i
    sys.exit(f'ERRORE: non trovato "{frammento}"')


def scomponi(elenco):
    i = dove(elenco, '<article class="page">')
    n = dove(elenco, '<nav class="chapter-nav"')
    if 'eyebrow' not in elenco[i + 1] or 'h1 class="title"' not in elenco[i + 2]:
        sys.exit('ERRORE: struttura di testata inattesa')
    return elenco[:i + 1], elenco[i + 3], elenco[i + 4:n], elenco[n:]


def scheda(testa, slug, t_it, t_en, cappello, corpo, coda):
    t = '\n'.join(testa)
    t = re.sub(r'<link rel="canonical" href="[^"]*">',
               f'<link rel="canonical" href="https://laquantistica.com/{slug}">', t)
    t = re.sub(r'<title>[^<]*</title>', f'<title>{t_it} · {t_en}</title>', t)
    intestazione = [
        '    <p class="eyebrow"><span class="it">Capitolo</span><span class="en">Chapter</span></p>',
        f'    <h1 class="title"><span class="it">{t_it}</span><span class="en">{t_en}</span></h1>',
        cappello,
    ]
    return '\n'.join([t] + intestazione + corpo + coda)


def richiamo(nn, slug_nota, ancora, ritorno, invito_it, invito_en, link_it, link_en):
    q = f'{slug_nota}?ret={ritorno}%23{ancora}'
    return [
        f'<div class="nota-link" id="{ancora}">',
        f'<span class="k"><span class="it">Nota {nn}</span><span class="en">Note {nn}</span></span>',
        f'<span class="it">{invito_it} <a href="{q}">{link_it} →</a></span>'
        f'<span class="en">{invito_en} <a href="{q}">{link_en} →</a></span>',
        '</div>',
    ]


NOTA = '''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="canonical" href="https://laquantistica.com/{slug}">
<title>Nota {nn} · {t_it} — La Quantistica</title>
<meta name="description" content="{descr}">
<link rel="stylesheet" href="assets/lang.css?v=7">
<link rel="stylesheet" href="assets/note.css?v=6">
<script src="assets/lang.js?v=8"></script>
<link rel="stylesheet" href="assets/katex/katex.min.css?v=1">
<style id="note-math">
html,body{{overflow-x:clip;}}
</style>
<script src="assets/note-back.js?v=1" defer></script>
</head>
<body>
<main class="sheet" id="top">
  <div class="sheet-inner">

    <div class="doc-meta">
      <span class="tag"><span class="it">Nota {nn}</span><span class="en">Note {nn}</span></span>
      <a class="doc-back-crumb" id="backCrumb" href="{cap}#{ancora}"><span class="crumb-arrow" aria-hidden="true">&larr;</span><span class="vh"><span class="it">Torna al </span><span class="en">Back to </span></span><span class="cap it">{cap_it}</span><span class="cap en">{cap_en}</span></a>
      <div class="langsw" role="group" aria-label="Lingua / Language">
        <button class="langbtn" type="button" data-l="it" aria-pressed="false">Italiano</button>
        <button class="langbtn" type="button" data-l="en" aria-pressed="true">English</button>
      </div>
    </div>

    <h1 class="doc-title">
      <span class="lead"><span class="it">Il calcolo</span><span class="en">The calculation</span></span>
      <span class="it">{t_it}</span><span class="en">{t_en}</span>
    </h1>

    <p class="lede"><span class="it">{lede_it}</span><span class="en">{lede_en}</span></p>
{corpo}

    <div class="doc-return">
      <a id="backBottom" href="{cap}#{ancora}"><span class="it">← Torna al punto di lettura</span><span class="en">← Back to where you were</span></a>
    </div>

    <div class="doc-foot">
      <span class="it">La Quantistica · Nota N.{nn} · Rev. 2026</span><span class="en">La Quantistica · Note No. {nn} · Rev. 2026</span>
      <span>F. Palma</span>
    </div>

  </div>
</main>
</body>
</html>
'''

scritti = []

# ---------------------------------------------------------------- scheda 4 in tre
r4 = righe('04-diffrazione.html')
testa4, cappello4, corpo4, coda4 = scomponi(r4)
i1 = dove(corpo4, 'sec-interpretazione-probabilistica.')
i2 = dove(corpo4, 'sec-determinazione-della-matrice-hamiltoniana.')
a4, b4, c4 = corpo4[:i1], corpo4[i1:i2], corpo4[i2:]

j_frase = dove(c4, 'Dimostriamo prima queste formule')
j_prova = dove(c4, 'sec-dimostrazione-delle-formule-1a-2a-3a-e-4a.')
j_fine = dove(c4, 'Cerchiamo ora la soluzione dell’equazione')
if not j_frase < j_prova < j_fine:
    sys.exit('ERRORE: blocco delle dimostrazioni fuori ordine')

dimostrazioni = c4[j_prova + 1:j_fine]
frase = ('<p><span class="it">Queste formule si dimostrano per induzione; qui le diamo per '
         'acquisite e passiamo a risolvere l’equazione nell’incognita <em>H</em>.</span>'
         '<span class="en">These formulas are proved by induction; here we take them as '
         'established and go on to solve the equation for the unknown <em>H</em>.</span></p>')
c4 = (c4[:j_frase] + [frase]
      + richiamo('10', 'nota-10-dimostrazione-commutatori.html', 'nota-10',
                 '04c-hamiltoniana.html',
                 'Le dimostrazioni per induzione delle quattro formule:',
                 'The proofs by induction of the four formulas:',
                 'il calcolo', 'the calculation')
      + c4[j_fine:])

scritti += [
    ('04-diffrazione.html',
     scheda(testa4, '04-diffrazione.html', 'Diffrazione degli Elettroni',
            'Electron Diffraction', cappello4, a4, coda4)),
    ('04b-forma-evoluzione.html',
     scheda(testa4, '04b-forma-evoluzione.html', 'La forma dell’equazione di evoluzione',
            'The Form of the Evolution Equation',
            '    <p class="opening"><span class="it">Nella scheda precedente abbiamo visto che '
            'all’elettrone va associata un’onda. Qui traduciamo questo fatto nel linguaggio delle '
            'ampiezze di probabilità e ricaviamo la forma generale della legge di evoluzione, '
            'senza ancora chiederci quali forze agiscano sulla particella.</span>'
            '<span class="en">In the previous card we saw that a wave must be associated with the '
            'electron. Here we translate that fact into the language of probability amplitudes and '
            'derive the general form of the law of evolution, without yet asking which forces act '
            'on the particle.</span></p>', b4, coda4)),
    ('04c-hamiltoniana.html',
     scheda(testa4, '04c-hamiltoniana.html', 'L’hamiltoniana e l’equazione di Schrödinger',
            'The Hamiltonian and the Schrödinger Equation',
            '    <p class="opening"><span class="it">La legge di evoluzione che abbiamo ricavato '
            'contiene una matrice <em>H</em> che ancora non conosciamo. Qui la determiniamo, '
            'chiedendo l’accordo con l’equazione di Newton e usando una sola misura.</span>'
            '<span class="en">The law of evolution we have derived contains a matrix <em>H</em> '
            'that we do not yet know. Here we determine it, by requiring agreement with Newton’s '
            'equation and using a single measurement.</span></p>', c4, coda4)),
    ('nota-10-dimostrazione-commutatori.html',
     NOTA.format(
         slug='nota-10-dimostrazione-commutatori.html', nn='10',
         t_it='Le formule sui commutatori', t_en='The commutator formulas',
         descr='Dimostrazione per induzione delle quattro formule sui commutatori usate per '
               'determinare la matrice hamiltoniana.',
         cap='04c-hamiltoniana.html', ancora='nota-10',
         cap_it='Cap. · L’hamiltoniana e l’equazione di Schrödinger',
         cap_en='Ch. · The Hamiltonian and the Schrödinger Equation',
         lede_it='Nella scheda abbiamo enunciato quattro formule sui commutatori e le abbiamo '
                 'usate per determinare la matrice hamiltoniana. Qui le dimostriamo.',
         lede_en='In the card we stated four formulas about commutators and used them to '
                 'determine the Hamiltonian matrix. Here we prove them.',
         corpo='\n'.join(dimostrazioni))),
]

# ---------------------------------------------------------------- scheda 5 in due
r5 = righe('05-rutherford.html')
testa5, cappello5, corpo5, coda5 = scomponi(r5)
k1 = dove(corpo5, 'sec-equazione-di-schrodinger-in-tre-dimensioni')
kapp = dove(corpo5, 'sec-appendice-1.-equazione-di-helmholtz.')
a5, b5, appendici = corpo5[:k1], corpo5[k1:kapp], corpo5[kapp:]

k_vedi = dove(b5, 'vedi appendice 1')
b5 = (b5[:k_vedi + 1]
      + richiamo('11', 'nota-11-appendici-rutherford.html', 'nota-11',
                 '05b-diffusione.html',
                 'L’equazione di Helmholtz e l’integrale usato più avanti:',
                 'The Helmholtz equation and the integral used further on:',
                 'le due appendici', 'the two appendices')
      + b5[k_vedi + 1:])

scritti += [
    ('05-rutherford.html',
     scheda(testa5, '05-rutherford.html', 'Esperimento di Rutherford',
            'The Rutherford Experiment', cappello5, a5, coda5)),
    ('05b-diffusione.html',
     scheda(testa5, '05b-diffusione.html', 'La formula di diffusione di Rutherford',
            'Rutherford’s Scattering Formula',
            '    <p class="opening"><span class="it">L’esperimento ci ha detto come si distribuiscono '
            'le particelle α diffuse. Qui ricaviamo quella distribuzione dall’equazione di '
            'Schrödinger, estesa alle tre dimensioni, e confrontiamo il risultato con le misure.</span>'
            '<span class="en">The experiment told us how the scattered α particles are distributed. '
            'Here we derive that distribution from the Schrödinger equation, extended to three '
            'dimensions, and compare the result with the measurements.</span></p>', b5, coda5)),
    ('nota-11-appendici-rutherford.html',
     NOTA.format(
         slug='nota-11-appendici-rutherford.html', nn='11',
         t_it='Le due appendici al calcolo della diffusione',
         t_en='The two appendices to the scattering calculation',
         descr='Soluzione generale dell’equazione di Helmholtz e calcolo dell’integrale usato '
               'nella formula di diffusione di Rutherford.',
         cap='05b-diffusione.html', ancora='nota-11',
         cap_it='Cap. · La formula di diffusione di Rutherford',
         cap_en='Ch. · Rutherford’s Scattering Formula',
         lede_it='Il calcolo della formula di diffusione si appoggia a due risultati che qui '
                 'ricaviamo per esteso: la soluzione generale dell’equazione di Helmholtz e un '
                 'integrale che compare due volte nel testo.',
         lede_en='The scattering-formula calculation rests on two results, derived here in full: '
                 'the general solution of the Helmholtz equation and an integral that appears '
                 'twice in the text.',
         corpo='\n'.join(appendici))),
]

for nome, testo in scritti:
    RADICE.joinpath(nome).write_text(testo, encoding='utf-8', newline='')
    print(f'{nome:44} {len(testo) // 1024:>5} KB')
print(f'\nfile scritti: {len(scritti)}')
