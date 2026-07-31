"""Cerca gli id che vivono DENTRO uno span di lingua e sono usati dal JavaScript.

Togliendo l'altra lingua quegli id spariscono: getElementById restituisce null e
lo script si ferma. E' il difetto trovato in lab-02d.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path('build/i18n')))
from split import Potatore  # noqa: E402

RADICE = pathlib.Path('publish')


def intervalli(testo, lingua):
    p = Potatore(testo, lingua)
    p.feed(testo)
    p.close()
    return sorted(p.intervalli)


trovati = 0
for f in sorted(RADICE.glob('*.html')):
    testo = f.read_text(encoding='utf-8')
    if 'class="it"' not in testo:
        continue
    script = ' '.join(re.findall(r'<script\b[^>]*>(.*?)</script>', testo, re.S))
    per_pagina = []
    for lingua in ('it', 'en'):
        for a, b in intervalli(testo, lingua):
            for m in re.finditer(r'\sid="([^"]+)"', testo[a:b]):
                ident = m.group(1)
                usato = re.search(rf'''["']{re.escape(ident)}["']''', script)
                ancora = f'href="#{ident}"' in testo
                if usato or ancora:
                    per_pagina.append((lingua, ident, 'script' if usato else 'ancora'))
    if per_pagina:
        trovati += len(per_pagina)
        print(f'{f.name}:')
        for lingua, ident, come in per_pagina:
            print(f'   dentro .{lingua}  id="{ident}"  usato da: {come}')

print(f'\ntotale id a rischio: {trovati}')
