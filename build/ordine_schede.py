"""Applica l'ordine di lettura: barra dei capitoli, numero in testata, precedente/successivo.

Unica fonte di verita' dell'ordine. Rilanciabile: riscrive sempre gli stessi blocchi.
"""
import pathlib
import re
import sys

RADICE = pathlib.Path('sorgenti')

# Ordine di lettura. Il numero nel nome del file resta quello del 1999: cambia solo l'ordine.
SCHEDE = [
    ('03-elettroni.html', 'Esperimenti con gli Elettroni', 'Experiments with Electrons'),
    ('04-diffrazione.html', 'Diffrazione degli Elettroni', 'Electron Diffraction'),
    ('04b-forma-evoluzione.html', 'La forma dell’equazione di evoluzione',
     'The Form of the Evolution Equation'),
    ('04c-hamiltoniana.html', 'L’hamiltoniana e l’equazione di Schrödinger',
     'The Hamiltonian and the Schrödinger Equation'),
    ('05-rutherford.html', 'Esperimento di Rutherford', 'The Rutherford Experiment'),
    ('05b-diffusione.html', 'La formula di diffusione di Rutherford',
     'Rutherford’s Scattering Formula'),
    ('07-franck-hertz.html', 'Esperimento di Franck-Hertz', 'The Franck–Hertz Experiment'),
    ('08-effetto-fotoelettrico.html', 'Effetto Fotoelettrico', 'The Photoelectric Effect'),
    ('01-stern-gerlach.html', 'Esperimento di Stern-Gerlach', 'The Stern–Gerlach Experiment'),
    ('02-stern-gerlach-cascata.html', 'Esperimenti di Stern-Gerlach in cascata',
     'Cascaded Stern–Gerlach Experiments'),
    ('06-ulteriori-sviluppi.html', 'Ulteriori sviluppi della Teoria',
     'Further Developments of the Theory'),
    ('09-spettri-atomici.html', 'Spettri atomici di emissione', 'Atomic Emission Spectra'),
]


def barra():
    voci = ['<nav aria-labelledby="nav-capitoli"><span id="nav-capitoli" class="sr-only">'
            '<span class="it">Capitoli</span><span class="en">Chapters</span></span>'
            '<a href="index.html"><span class="num"></span><span class="it">Introduzione</span>'
            '<span class="en">Introduction</span></a>']
    for n, (slug, it, en) in enumerate(SCHEDE, 1):
        voci.append(f'<a href="{slug}"><span class="num">{n}</span>'
                    f'<span class="it">{it}</span><span class="en">{en}</span></a>')
    return '\n'.join(voci) + '</nav>'


def avanti_indietro(posizione):
    """posizione: 0 = introduzione, 1..12 = schede."""
    pezzi = ['<nav class="chapter-nav" aria-labelledby="nav-pagina">'
             '<span id="nav-pagina" class="sr-only"><span class="it">Capitolo precedente e '
             'successivo</span><span class="en">Previous and next chapter</span></span>']
    if posizione >= 1:
        if posizione == 1:
            slug, it, en = 'index.html', 'Introduzione', 'Introduction'
        else:
            slug, it, en = SCHEDE[posizione - 2]
        pezzi.append(f'<a class="prev" href="{slug}"><span class="it">Precedente</span>'
                     f'<span class="en">Previous</span><span class="ttl it">{it}</span>'
                     f'<span class="ttl en">{en}</span></a>')
    if posizione < len(SCHEDE):
        slug, it, en = SCHEDE[posizione]
        pezzi.append(f'<a class="next" href="{slug}"><span class="it">Successivo</span>'
                     f'<span class="en">Next</span><span class="ttl it">{it}</span>'
                     f'<span class="ttl en">{en}</span></a>')
    return '    ' + ''.join(pezzi) + '</nav>'


BARRA = re.compile(r'<nav aria-labelledby="nav-capitoli">.*?</nav>', re.S)
NAVPAG = re.compile(r'[ \t]*<nav class="chapter-nav".*?</nav>', re.S)
OCCHIELLO = re.compile(r'[ \t]*<p class="eyebrow">.*?</p>', re.S)

pagine = [('index.html', 0)] + [(s[0], n) for n, s in enumerate(SCHEDE, 1)]
guasti = []
for nome, posizione in pagine:
    percorso = RADICE / nome
    if not percorso.exists():
        guasti.append(f'manca {nome}')
        continue
    testo = percorso.read_text(encoding='utf-8')
    atteso = 1 if nome == 'index.html' else 1
    if len(BARRA.findall(testo)) != 1 or len(NAVPAG.findall(testo)) != atteso:
        guasti.append(f'{nome}: blocchi di navigazione inattesi')
        continue
    testo = BARRA.sub(lambda _: barra(), testo, count=1)
    testo = NAVPAG.sub(lambda _: avanti_indietro(posizione), testo, count=1)
    if posizione:
        occhiello = (f'    <p class="eyebrow"><span class="it">Capitolo {posizione}</span>'
                     f'<span class="en">Chapter {posizione}</span></p>')
        if len(OCCHIELLO.findall(testo)) != 1:
            guasti.append(f'{nome}: occhiello non trovato')
            continue
        testo = OCCHIELLO.sub(lambda _: occhiello, testo, count=1)
    percorso.write_text(testo, encoding='utf-8', newline='')

if guasti:
    sys.exit('PROBLEMI:\n  ' + '\n  '.join(guasti))

for n, (slug, it, _) in enumerate(SCHEDE, 1):
    print(f'{n:>3}. {slug:<32} {it}')
print(f'\nschede: {len(SCHEDE)} · pagine aggiornate: {len(pagine)}')
