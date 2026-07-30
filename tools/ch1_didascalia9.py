"""Aggiunge alla didascalia della figura 9 la cautela che le spetta.

Diceva gia' che l'immagine non e' una fotografia. Mancava il passo successivo:
mostra cio' che il modello prevede, non cio' che un apparato vero produrrebbe.
E' una distinzione che il lettore ha il diritto di conoscere prima di
confrontarla con la lastra storica.

    python tools/ch1_didascalia9.py
"""
from pathlib import Path

PAGINA = Path('publish/01-stern-gerlach.html')

CAMBI = [
    ('la configurazione \u00e8 quella del terzo pulsante, \u00absdoppiamento leggibile\u00bb.',
     'la configurazione \u00e8 quella del terzo pulsante, \u00absdoppiamento leggibile\u00bb. '
     'Mostra quindi ci\u00f2 che il modello prevede, non ci\u00f2 che uscirebbe da un '
     'apparato costruito davvero: le due bande sono pulite e parallele perch\u00e9 '
     'il modello assume un gradiente uniforme su tutta la larghezza del fascio.'),

    ('the configuration is the third preset, \u201creadable splitting\u201d.',
     'the configuration is the third preset, \u201creadable splitting\u201d. It therefore '
     'shows what the model predicts, not what an apparatus actually built would '
     'produce: the two bands are clean and parallel because the model assumes a '
     'gradient uniform across the whole width of the beam.'),
]

src = PAGINA.read_text(encoding='utf-8')
fatti = 0
for vecchio, nuovo in CAMBI:
    if vecchio in src:
        src = src.replace(vecchio, nuovo, 1)
        fatti += 1
    else:
        print(f'  NON TROVATO: {vecchio[:60]}...')
PAGINA.write_text(src, encoding='utf-8', newline='')
print(f'{fatti} su {len(CAMBI)} aggiornati')
