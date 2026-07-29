"""Aggiunge il link «salta al contenuto» e i punti di riferimento semantici.

Chi naviga da tastiera oggi deve attraversare tutta la navigazione laterale a
ogni pagina. Qui si aggiunge:
- un link «salta al contenuto», invisibile finche' non riceve il fuoco;
- la barra laterale diventa <header> (punto di riferimento "intestazione");
- <main> riceve un id e diventa raggiungibile dal link;
- le due navigazioni ricevono un nome, cosi' si distinguono fra loro.

I nomi delle navigazioni sono bilingui: si usa aria-labelledby verso uno span
nascosto che contiene le due lingue, invece di aria-label che ne ammette una sola.

    python tools/a11y_landmarks.py            # anteprima
    python tools/a11y_landmarks.py --write
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PUBLISH = Path('publish')

SKIP = ('<a class="skip-link" href="#contenuto">'
        '<span class="it">Salta al contenuto</span>'
        '<span class="en">Skip to content</span></a>\n')

NAV_CAP = ('<nav aria-labelledby="nav-capitoli"><span id="nav-capitoli" class="sr-only">'
           '<span class="it">Capitoli</span><span class="en">Chapters</span></span>')

NAV_CH = ('<nav class="chapter-nav" aria-labelledby="nav-pagina">'
          '<span id="nav-pagina" class="sr-only">'
          '<span class="it">Capitolo precedente e successivo</span>'
          '<span class="en">Previous and next chapter</span></span>')

RULES = [
    ('<body>\n', '<body>\n' + SKIP),
    ('<aside class="sidebar">', '<header class="sidebar">'),
    ('</aside>\n<main class="content">',
     '</header>\n<main class="content" id="contenuto" tabindex="-1">'),
    ('  <nav><a href="index.html">', '  ' + NAV_CAP + '<a href="index.html">'),
    ('<nav class="chapter-nav">', NAV_CH),
]


def main() -> None:
    write = '--write' in sys.argv
    for path in sorted(PUBLISH.glob('*.html')):
        src = path.read_text(encoding='utf-8')
        if '<aside class="sidebar">' not in src:
            continue
        out, applied = src, []
        for old, new in RULES:
            n = out.count(old)
            if n:
                out = out.replace(old, new)
            applied.append(f'{n}')
        if 'skip-link' in src:
            print(f'{path.name}: gia\' fatto, salto')
            continue
        print(f'{path.name}: sostituzioni {"/".join(applied)}')
        if write:
            path.write_text(out, encoding='utf-8')
    if not write:
        print('\n(anteprima: usa --write per scrivere)')


if __name__ == '__main__':
    main()
