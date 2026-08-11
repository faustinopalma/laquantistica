"""Ritaglia e ingrandisce alcune voci del libretto per leggerle meglio.
Lavora su file personali: l'uscita resta nella cartella esclusa da git."""
import pathlib

from PIL import Image

CARTELLA = pathlib.Path('privato/librettouniversitario')
USCITA = CARTELLA / '_ritagli'
USCITA.mkdir(exist_ok=True)

im = Image.open(CARTELLA / 'libretto 3.jpg')
L, A = im.size
print(f'libretto 3: {L}x{A}')

for nome, (y1, y2) in {'alta': (0.0, 0.52), 'bassa': (0.48, 1.0)}.items():
    r = im.crop((0, int(y1 * A), L, int(y2 * A)))
    r = r.resize((int(r.width * 1.7), int(r.height * 1.7)), Image.LANCZOS)
    p = USCITA / f'l3-{nome}.png'
    r.save(p)
    print(f'  {p} {r.size}')
