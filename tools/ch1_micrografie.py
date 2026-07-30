"""Corregge l'affermazione sulla forma delle tracce nelle micrografie del 1922.

Il testo diceva che la coda maxwelliana della traccia da' "esattamente la forma
visibile nelle micrografie storiche": non e' cosi'. Nella cartolina che Gerlach
mando' a Bohr le due tracce non sono parallele ma formano una figura a labbra,
perche' il gradiente del suo magnete variava lungo la fenditura e si annullava
ai bordi. La coda c'e', ma la forma d'insieme nasce da un fatto geometrico
diverso, che in un apparato con gradiente uniforme non si presenta.

    python tools/ch1_micrografie.py
"""
from pathlib import Path

PAGINA = Path('publish/01-stern-gerlach.html')

CAMBI = [
    ('con un massimo netto e una coda diretta verso l\u2019esterno: esattamente '
     'la forma visibile nelle micrografie storiche del 1922.',
     'con un massimo netto e una coda diretta verso l\u2019esterno. Le micrografie '
     'del 1922 mostrano invece una figura a labbra, con le due tracce che si '
     'separano al centro e tornano a toccarsi alle estremit\u00e0: nel magnete di '
     'Gerlach il gradiente variava lungo la fenditura e si annullava ai bordi, '
     'mentre qui le espansioni sono dimensionate per mantenerlo uniforme '
     'sull\u2019intera larghezza del fascio.'),

    ('with a sharp maximum and a tail directed outwards: exactly the shape seen '
     'in the historical 1922 micrographs.',
     'with a sharp maximum and a tail directed outwards. The 1922 micrographs '
     'show instead a lip-shaped figure, the two traces parting in the middle and '
     'meeting again at the ends: in Gerlach\u2019s magnet the gradient varied along '
     'the slit and vanished at its edges, whereas here the pole pieces are sized '
     'to keep it uniform across the whole width of the beam.'),
]

src = PAGINA.read_text(encoding='utf-8')
fatti = 0
for vecchio, nuovo in CAMBI:
    if vecchio in src:
        src = src.replace(vecchio, nuovo)
        fatti += 1
    else:
        print(f'  NON TROVATO: {vecchio[:60]}...')
PAGINA.write_text(src, encoding='utf-8', newline='')
print(f'{fatti} su {len(CAMBI)} corretti')
