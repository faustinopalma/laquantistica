"""Prepara ritagli leggibili delle pagine del libretto, raddrizzando l'EXIF."""
import pathlib

from PIL import Image, ImageOps

CARTELLA = pathlib.Path('librettouniversitario')
USCITA = CARTELLA / '_ritagli'
USCITA.mkdir(exist_ok=True)

# per ogni pagina: quali fasce verticali ritagliare (frazioni dell'altezza)
PIANO = {
    'libretto 1.jpg': [('p1', 0.0, 1.0)],
    'libretto 2.jpg': [('p2a', 0.02, 0.52), ('p2b', 0.48, 0.98)],
    'libretto 4.jpg': [('p4', 0.02, 0.98)],
}

for nome, fasce in PIANO.items():
    im = ImageOps.exif_transpose(Image.open(CARTELLA / nome))
    L, A = im.size
    print(f'{nome}: {L}x{A}')
    for etichetta, y1, y2 in fasce:
        r = im.crop((0, int(y1 * A), L, int(y2 * A)))
        fattore = min(2.2, 2600 / r.width)
        r = r.resize((int(r.width * fattore), int(r.height * fattore)), Image.LANCZOS)
        p = USCITA / f'{etichetta}.png'
        r.save(p)
        print(f'   {p.name}  {r.size}')
