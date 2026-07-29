"""Adegua la configurazione di MathJax al passaggio dalla versione 3 alla 4.

Nella 4 il MathML nascosto per i lettori di schermo non c'è più a meno di
chiederlo, e la lettura ad alta voce viene preparata da un componente esterno
di 4,5 MB che non ospitiamo: senza queste righe la pagina perde
l'accessibilità e va in errore cercando file inesistenti.

La lettura va spenta due volte: il menù contestuale riaccende la propria
impostazione sopra quella del documento.

    python tools/mathjax4_config.py publish/*.html
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

OPEN = 'window.MathJax = {'
LOADER = "\n  loader: { load: ['a11y/assistive-mml'] },"
OPTS = re.compile(r"(options: \{ skipHtmlTags: \[[^\]]*\])( \})")
ADD = (r"\1,"
       "\n    enableAssistiveMml: true, enableSpeech: false, enableBraille: false,"
       "\n    menuOptions: { settings: { speech: false, braille: false } }"
       "\n  }")


def fix(path: Path) -> str:
    src = path.read_text(encoding='utf-8')
    if OPEN not in src:
        return 'senza MathJax'
    if 'assistive-mml' in src:
        return 'già adeguata'
    out = src.replace(OPEN, OPEN + LOADER, 1)
    out, n = OPTS.subn(ADD, out, count=1)
    if not n:
        return 'ATTENZIONE: opzioni non riconosciute'
    path.write_text(out, encoding='utf-8', newline='')
    return 'adeguata'


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        p = Path(arg)
        print(f'{p.name:38} {fix(p)}')
