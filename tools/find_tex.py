"""Cerca una formula per frammento di LaTeX e ne dice pagina e riga.

    python tools/find_tex.py cases nabla
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

chiavi = sys.argv[1:]
if not chiavi:
    sys.exit('uso: python tools/find_tex.py <frammento> [<frammento> ...]')

trovate = 0
for p in sorted(Path('publish').rglob('*.html')):
    src = p.read_text(encoding='utf-8')
    for m in re.finditer(r'data-tex="([^"]*)"', src):
        tex = html.unescape(m.group(1))
        if all(k in tex for k in chiavi):
            trovate += 1
            print(f'--- {p.name}  riga {src[:m.start()].count(chr(10)) + 1}')
            print(tex)
            print()
print(f'{trovate} formule')
