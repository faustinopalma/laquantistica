"""Rimette a posto i collegamenti delle note dopo la divisione delle schede 4 e 5.

Sposta i `?ret=` dei richiami finiti nelle schede nuove, aggiorna il ritorno delle note,
inserisce il richiamo alla Nota 09 e riallinea le etichette dei capitoli.
"""
import pathlib
import re
import sys

RADICE = pathlib.Path('sorgenti')

# file della scheda -> (numero nell'ordine di lettura, titolo it, titolo en)
CAPITOLI = {
    '03-elettroni.html': (1, 'Esperimenti con gli Elettroni', 'Experiments with Electrons'),
    '04-diffrazione.html': (2, 'Diffrazione degli Elettroni', 'Electron Diffraction'),
    '04b-forma-evoluzione.html': (3, 'La forma dell’equazione di evoluzione',
                                  'The Form of the Evolution Equation'),
    '04c-hamiltoniana.html': (4, 'L’hamiltoniana e l’equazione di Schrödinger',
                              'The Hamiltonian and the Schrödinger Equation'),
    '05-rutherford.html': (5, 'Esperimento di Rutherford', 'The Rutherford Experiment'),
    '05b-diffusione.html': (6, 'La formula di diffusione di Rutherford',
                            'Rutherford’s Scattering Formula'),
    '07-franck-hertz.html': (7, 'Esperimento di Franck-Hertz', 'The Franck–Hertz Experiment'),
    '08-effetto-fotoelettrico.html': (8, 'Effetto Fotoelettrico', 'The Photoelectric Effect'),
    '01-stern-gerlach.html': (9, 'Esperimento di Stern-Gerlach', 'The Stern–Gerlach Experiment'),
    '02-stern-gerlach-cascata.html': (10, 'Esperimenti di Stern-Gerlach in cascata',
                                      'Cascaded Stern–Gerlach Experiments'),
    '06-ulteriori-sviluppi.html': (11, 'Ulteriori sviluppi della Teoria',
                                   'Further Developments of the Theory'),
    '09-spettri-atomici.html': (12, 'Spettri atomici di emissione', 'Atomic Emission Spectra'),
}

# richiami di nota finiti in una scheda diversa da quella di partenza
TRASLOCHI = {
    '04b-forma-evoluzione.html': ['nota-5', 'nota-2', 'nota-8'],
    '04c-hamiltoniana.html': ['nota-6'],
}

guasti = []

for scheda, ancore in TRASLOCHI.items():
    percorso = RADICE / scheda
    testo = percorso.read_text(encoding='utf-8')
    for ancora in ancore:
        vecchio = f'?ret=04-diffrazione.html%23{ancora}'
        nuovo = f'?ret={scheda}%23{ancora}'
        if nuovo in testo:
            continue
        if vecchio not in testo:
            guasti.append(f'{scheda}: manca {vecchio}')
            continue
        testo = testo.replace(vecchio, nuovo)
    percorso.write_text(testo, encoding='utf-8', newline='')

# ritorno delle note che puntavano alla scheda 4 non divisa
RITORNI = {
    'nota-05-delta-dirac.html': ('04-diffrazione.html#nota-5', '04b-forma-evoluzione.html#nota-5'),
    'nota-08-matrici-hermitiane.html': ('04-diffrazione.html#nota-8',
                                        '04b-forma-evoluzione.html#nota-8'),
    'nota-06-ehrenfest.html': ('04-diffrazione.html#nota-6', '04c-hamiltoniana.html#nota-6'),
}
for nota, (vecchio, nuovo) in RITORNI.items():
    percorso = RADICE / nota
    testo = percorso.read_text(encoding='utf-8')
    if testo.count(nuovo) == 2:
        continue
    if testo.count(vecchio) != 2:
        guasti.append(f'{nota}: attesi 2 ritorni a {vecchio}, trovati {testo.count(vecchio)}')
        continue
    percorso.write_text(testo.replace(vecchio, nuovo), encoding='utf-8', newline='')

# etichetta del capitolo in testa a ogni nota, allineata alla numerazione nuova
CRUMB = re.compile(r'(<a class="doc-back-crumb" id="backCrumb" href="([^"#]+)[^"]*">.*?)'
                   r'<span class="cap it">[^<]*</span><span class="cap en">[^<]*</span>', re.S)
for percorso in sorted(RADICE.glob('nota-*.html')):
    testo = percorso.read_text(encoding='utf-8')
    trovato = CRUMB.search(testo)
    if not trovato:
        guasti.append(f'{percorso.name}: crumb non riconosciuto')
        continue
    voce = CAPITOLI.get(trovato.group(2))
    if not voce:
        guasti.append(f'{percorso.name}: capitolo sconosciuto {trovato.group(2)}')
        continue
    n, it, en = voce
    nuovo = (f'{trovato.group(1)}<span class="cap it">Cap. {n:02d} · {it}</span>'
             f'<span class="cap en">Ch. {n:02d} · {en}</span>')
    percorso.write_text(CRUMB.sub(lambda _: nuovo, testo, count=1), encoding='utf-8', newline='')

# richiamo alla Nota 09, dove compaiono per la prima volta i numeri complessi
percorso = RADICE / '04b-forma-evoluzione.html'
testo = percorso.read_text(encoding='utf-8')
if 'nota-09-perche-numeri-complessi' in testo:
    print('richiamo alla Nota 09 gia\' presente')
else:
    righe = testo.split('\n')
    posti = [i for i, r in enumerate(righe) if 'detti ampiezze di probabilità' in r]
    if len(posti) != 1:
        guasti.append(f'04b: {len(posti)} paragrafi con "ampiezze di probabilità"')
    else:
        q = 'nota-09-perche-numeri-complessi.html?ret=04b-forma-evoluzione.html%23nota-9'
        righe[posti[0] + 1:posti[0] + 1] = [
            '<div class="nota-link" id="nota-9">',
            '<span class="k"><span class="it">Nota 09</span><span class="en">Note 09</span></span>',
            f'<span class="it">Perché proprio i numeri complessi, e che cosa ci vincola a '
            f'sceglierli: <a href="{q}">la scelta →</a></span>'
            f'<span class="en">Why complex numbers, and what constrains us to choose them: '
            f'<a href="{q}">the choice →</a></span>',
            '</div>',
        ]
        percorso.write_text('\n'.join(righe), encoding='utf-8', newline='')
        print('inserito il richiamo alla Nota 09 in 04b')

# tabella dei capitoli usata dal ritorno dinamico delle note
js = pathlib.Path('publish/assets/note-back.js')
testo = js.read_text(encoding='utf-8')
voci = ',\n'.join(
    f"    '{slug}':".ljust(40) + f"['Cap. {n:02d} \\u00b7 {it}', 'Ch. {n:02d} \\u00b7 {en}']"
    for slug, (n, it, en) in sorted(CAPITOLI.items(), key=lambda x: x[1][0]))
nuovo, quante = re.subn(r'(var CAPITOLI = \{\n).*?(\n  \};)',
                        lambda m: m.group(1) + voci + m.group(2), testo, count=1, flags=re.S)
if quante != 1:
    guasti.append('note-back.js: tabella CAPITOLI non riconosciuta')
else:
    js.write_text(nuovo, encoding='utf-8', newline='')

if guasti:
    sys.exit('PROBLEMI:\n  ' + '\n  '.join(guasti))
print('collegamenti delle note aggiornati')
