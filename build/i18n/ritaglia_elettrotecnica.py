"""Ingrandisce la casella di 'Principi di Ing. elettrica' (l'esame di Elettrotecnica).

Le foto hanno l'orientamento nei metadati EXIF: senza exif_transpose PIL le legge
ruotate e i ritagli finiscono nel posto sbagliato.
"""
import pathlib

from PIL import Image, ImageOps

CARTELLA = pathlib.Path('librettouniversitario')
USCITA = CARTELLA / '_ritagli'
USCITA.mkdir(exist_ok=True)

im = ImageOps.exif_transpose(Image.open(CARTELLA / 'libretto 3.jpg'))
L, A = im.size
print(f'libretto 3 raddrizzata: {L}x{A}')

# colonna sinistra: 8 caselle fra y=0.06 e y=0.93 -> la quinta e' Principi di Ing. elettrica
alto, basso, n = 0.055, 0.93, 8
passo = (basso - alto) / n
for indice, nome in ((5, 'principi-ing-elettrica'), (8, 'scienza-costruzioni')):
    y1 = alto + (indice - 1) * passo
    box = (int(0.02 * L), int(y1 * A), int(0.50 * L), int((y1 + passo) * A))
    r = im.crop(box)
    r = r.resize((r.width * 3, r.height * 3), Image.LANCZOS)
    p = USCITA / f'{nome}.png'
    r.save(p)
    print(f'  {p}  {r.size}')
