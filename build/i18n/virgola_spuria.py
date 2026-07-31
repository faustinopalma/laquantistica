"""Verifica che nelle formule italiane la virgola decimale non sia piu' resa come
punteggiatura (che aggiunge uno spazio: "6, 6")."""
import pathlib
import re

SPURIO = re.compile(
    r'<span class="mord">(\d)</span><span class="mpunct">,</span>'
    r'<span class="mspace"[^>]*></span><span class="mord">(\d)</span>')

for lingua in ('it', 'en'):
    tot = 0
    for f in sorted((pathlib.Path('publish') / lingua).glob('*.html')):
        n = len(SPURIO.findall(f.read_text(encoding='utf-8')))
        if n:
            print(f'  {lingua}/{f.name}: {n}')
        tot += n
    print(f'albero {lingua}: {tot} virgole decimali rese come punteggiatura')
